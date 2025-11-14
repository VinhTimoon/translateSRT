"""
Async Translation Dispatcher
Handles parallel translation with fallback logic.
"""

import asyncio
import json
import time
from typing import List, Dict, Optional, Tuple, Callable
from dataclasses import dataclass
import httpx

from .parser import Chunk
from .validator import TranslationValidator, Postprocessor
from .config import APIConfig, ConfigManager


@dataclass
class TranslationResult:
    """Result of translating a chunk."""
    chunk: Chunk
    success: bool
    translated_lines: Optional[List[str]]
    error: Optional[str]
    api_used: Optional[str]
    attempts: int
    duration: float


class TranslationStats:
    """Track translation statistics."""
    
    def __init__(self):
        self.total_chunks = 0
        self.success_count = 0
        self.failed_count = 0
        self.api_usage: Dict[str, int] = {}
        self.total_duration = 0.0
        self.start_time: Optional[float] = None
    
    def record_result(self, result: TranslationResult):
        """Record a translation result."""
        self.total_chunks += 1
        
        if result.success:
            self.success_count += 1
        else:
            self.failed_count += 1
        
        if result.api_used:
            self.api_usage[result.api_used] = self.api_usage.get(result.api_used, 0) + 1
        
        self.total_duration += result.duration
    
    def get_summary(self) -> str:
        """Get statistics summary."""
        elapsed = time.time() - self.start_time if self.start_time else 0
        
        summary = f"""Translation Statistics:
- Total Chunks: {self.total_chunks}
- Successful: {self.success_count}
- Failed: {self.failed_count}
- Success Rate: {self.success_count / self.total_chunks * 100:.1f}% (if self.total_chunks > 0 else 0)
- Total Duration: {self.total_duration:.2f}s
- Elapsed Time: {elapsed:.2f}s
- API Usage: {self.api_usage}
"""
        return summary


class TranslationDispatcher:
    """Dispatches translation requests with concurrency control."""
    
    def __init__(self, config: ConfigManager):
        """
        Initialize dispatcher.
        
        Args:
            config: Configuration manager
        """
        self.config = config
        self.stats = TranslationStats()
        self.client: Optional[httpx.AsyncClient] = None
        
        # Semaphores for rate limiting per API
        self.semaphores: Dict[str, asyncio.Semaphore] = {}
        
        # Progress callback
        self.progress_callback: Optional[Callable[[int, int, str], None]] = None
        
        # Cancellation flag
        self.cancelled = False
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.client = httpx.AsyncClient(timeout=self.config.settings.timeout)
        
        # Create semaphores for each API
        for api in self.config.apis:
            self.semaphores[api.name] = asyncio.Semaphore(api.max_threads)
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.client:
            await self.client.aclose()
    
    def set_progress_callback(self, callback: Callable[[int, int, str], None]):
        """
        Set progress callback.
        
        Args:
            callback: Function(current, total, message)
        """
        self.progress_callback = callback
    
    def cancel(self):
        """Cancel translation."""
        self.cancelled = True
    
    async def _call_gemini_api(
        self, 
        api: APIConfig, 
        user_prompt: str
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Call Gemini API.
        
        Args:
            api: API configuration
            user_prompt: User prompt
            
        Returns:
            Tuple of (success, response_text, error)
        """
        try:
            endpoint = self.config.get_api_endpoint(api)
            
            # Build request payload for Gemini API
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": self.config.SYSTEM_PROMPT},
                            {"text": user_prompt}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.3,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 2048,
                }
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            # Add API key to URL (Gemini style)
            url = f"{endpoint}?key={api.key}"
            
            response = await self.client.post(
                url,
                json=payload,
                headers=headers
            )
            
            response.raise_for_status()
            
            # Parse Gemini response
            data = response.json()
            
            # Extract text from response
            if "candidates" in data and len(data["candidates"]) > 0:
                candidate = data["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    parts = candidate["content"]["parts"]
                    if len(parts) > 0 and "text" in parts[0]:
                        text = parts[0]["text"]
                        return True, text, None
            
            return False, None, "Invalid response format"
            
        except httpx.HTTPError as e:
            return False, None, f"HTTP error: {e}"
        except Exception as e:
            return False, None, f"Unexpected error: {e}"
    
    async def _translate_with_api(
        self, 
        chunk: Chunk, 
        api: APIConfig
    ) -> Optional[TranslationResult]:
        """
        Translate a chunk using a specific API.
        
        Args:
            chunk: Chunk to translate
            api: API to use
            
        Returns:
            TranslationResult if successful, None otherwise
        """
        start_time = time.time()
        
        # Build prompt
        user_prompt = self.config.build_user_prompt(
            chunk.lines,
            chunk.start_idx,
            chunk.end_idx
        )
        
        # Acquire semaphore for this API
        async with self.semaphores[api.name]:
            # Call API
            success, response_text, error = await self._call_gemini_api(api, user_prompt)
            
            if not success:
                return None
            
            # Validate response
            valid, cleaned, validation_error = TranslationValidator.validate_response(
                response_text,
                len(chunk.lines),
                strict_cjk=self.config.settings.strict_cjk_check
            )
            
            if not valid:
                return None
            
            # Postprocess
            processed = Postprocessor.process_batch(
                cleaned,
                name_map=self.config.name_map,
                normalize=self.config.settings.normalize_punctuation
            )
            
            duration = time.time() - start_time
            
            return TranslationResult(
                chunk=chunk,
                success=True,
                translated_lines=processed,
                error=None,
                api_used=api.name,
                attempts=chunk.attempts + 1,
                duration=duration
            )
    
    async def _translate_chunk_primary(self, chunk: Chunk) -> Optional[TranslationResult]:
        """
        Try translating with primary APIs.
        
        Args:
            chunk: Chunk to translate
            
        Returns:
            TranslationResult if any primary API succeeds
        """
        primary_apis = self.config.get_primary_apis()
        
        if not primary_apis:
            return None
        
        # Try each primary API in sequence (or could be parallel)
        for api in primary_apis:
            if self.cancelled:
                return None
            
            result = await self._translate_with_api(chunk, api)
            if result:
                return result
        
        return None
    
    async def _translate_chunk_fallback(self, chunk: Chunk) -> Optional[TranslationResult]:
        """
        Try translating with fallback APIs (parallel).
        
        Args:
            chunk: Chunk to translate
            
        Returns:
            TranslationResult if any fallback API succeeds
        """
        fallback_apis = self.config.get_fallback_apis()
        
        if not fallback_apis:
            return None
        
        # Try all fallback APIs in parallel
        tasks = [
            self._translate_with_api(chunk, api)
            for api in fallback_apis
        ]
        
        if not tasks:
            return None
        
        # Wait for first successful result
        done, pending = await asyncio.wait(
            tasks,
            return_when=asyncio.FIRST_COMPLETED,
            timeout=self.config.settings.timeout
        )
        
        # Check completed tasks
        for task in done:
            if self.cancelled:
                # Cancel pending
                for p in pending:
                    p.cancel()
                return None
            
            try:
                result = task.result()
                if result:
                    # Cancel other pending tasks
                    for p in pending:
                        p.cancel()
                    return result
            except:
                pass
        
        # Cancel any remaining
        for p in pending:
            p.cancel()
        
        return None
    
    async def _translate_chunk_with_retry(self, chunk: Chunk) -> TranslationResult:
        """
        Translate a chunk with retry logic.
        
        Args:
            chunk: Chunk to translate
            
        Returns:
            TranslationResult (may be unsuccessful)
        """
        start_time = time.time()
        
        # Try primary APIs first
        result = await self._translate_chunk_primary(chunk)
        if result:
            return result
        
        # If primary failed, try fallback with retries
        for attempt in range(self.config.settings.retry_rounds):
            if self.cancelled:
                break
            
            chunk.attempts += 1
            
            result = await self._translate_chunk_fallback(chunk)
            if result:
                return result
            
            # Small delay between retries
            await asyncio.sleep(0.5)
        
        # All attempts failed - return failure result with original lines
        duration = time.time() - start_time
        
        return TranslationResult(
            chunk=chunk,
            success=False,
            translated_lines=chunk.lines,  # Keep original Chinese
            error="All translation attempts failed",
            api_used=None,
            attempts=chunk.attempts,
            duration=duration
        )
    
    async def translate_chunks(
        self, 
        chunks: List[Chunk]
    ) -> Dict[Tuple[int, int], List[str]]:
        """
        Translate all chunks.
        
        Args:
            chunks: List of chunks to translate
            
        Returns:
            Dict mapping (start_idx, end_idx) -> translated_lines
        """
        self.stats = TranslationStats()
        self.stats.start_time = time.time()
        self.stats.total_chunks = len(chunks)
        self.cancelled = False
        
        results: Dict[Tuple[int, int], List[str]] = {}
        
        # Process chunks
        completed = 0
        
        for chunk in chunks:
            if self.cancelled:
                break
            
            # Update progress
            if self.progress_callback:
                self.progress_callback(
                    completed,
                    len(chunks),
                    f"Translating chunk {chunk.start_idx}-{chunk.end_idx}..."
                )
            
            # Translate chunk
            result = await self._translate_chunk_with_retry(chunk)
            
            # Record stats
            self.stats.record_result(result)
            
            # Store result
            key = (chunk.start_idx, chunk.end_idx)
            results[key] = result.translated_lines or chunk.lines
            
            completed += 1
            
            # Update progress
            if self.progress_callback:
                status = "✓" if result.success else "✗"
                self.progress_callback(
                    completed,
                    len(chunks),
                    f"{status} Chunk {chunk.start_idx}-{chunk.end_idx} ({result.api_used or 'failed'})"
                )
        
        return results
    
    def get_stats(self) -> TranslationStats:
        """Get translation statistics."""
        return self.stats
