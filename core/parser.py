"""
SRT Parser & Chunker
Parses SRT files into indexed arrays (1-based) and splits into chunks for batch translation.
"""

import re
from typing import List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class Chunk:
    """Represents a chunk of subtitles for batch translation."""
    start_idx: int  # 1-based start index
    end_idx: int    # 1-based end index (inclusive)
    lines: List[str]  # Original subtitle texts
    attempts: int = 0
    
    def __repr__(self):
        return f"Chunk({self.start_idx}-{self.end_idx}, {len(self.lines)} lines, {self.attempts} attempts)"


class SRTParser:
    """Parse and validate SRT subtitle files."""
    
    # SRT block pattern: index, timecode, content (1+ lines), blank line
    BLOCK_PATTERN = re.compile(
        r'(\d+)\s*\n'  # Index
        r'([\d:,\s]+-->[\d:,\s]+)\s*\n'  # Timecode
        r'((?:.+\n?)+?)'  # Content (one or more lines)
        r'(?:\n|$)',  # Blank line or EOF
        re.MULTILINE
    )
    
    @staticmethod
    def parse(text: str) -> Tuple[List[Optional[str]], List[Optional[str]]]:
        """
        Parse SRT text into two 1-indexed arrays: times and subs.
        
        Args:
            text: Raw SRT file content
            
        Returns:
            Tuple of (times, subs) where:
            - times[0] = None, times[1..N] = timecodes
            - subs[0] = None, subs[1..N] = subtitle texts
        """
        # Normalize line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Initialize with None at index 0 (unused, for 1-based indexing)
        times = [None]
        subs = [None]
        
        # Split by double newlines to get blocks
        blocks = re.split(r'\n\s*\n', text.strip())
        
        for block in blocks:
            if not block.strip():
                continue
                
            lines = block.strip().split('\n')
            if len(lines) < 3:
                continue  # Invalid block
            
            try:
                # Parse index
                idx_str = lines[0].strip()
                idx = int(idx_str)
                
                # Parse timecode
                timecode = lines[1].strip()
                
                # Parse content (may be multiple lines)
                content = '\n'.join(lines[2:]).strip()
                
                # Ensure arrays are large enough
                while len(times) <= idx:
                    times.append(None)
                    subs.append(None)
                
                # Store at 1-based index
                times[idx] = timecode
                subs[idx] = content
                
            except (ValueError, IndexError) as e:
                # Skip malformed blocks
                print(f"Warning: Skipped malformed block: {e}")
                continue
        
        return times, subs
    
    @staticmethod
    def validate(times: List[Optional[str]], subs: List[Optional[str]]) -> bool:
        """
        Validate parsed SRT data.
        
        Args:
            times: Timecode array
            subs: Subtitle array
            
        Returns:
            True if valid, False otherwise
        """
        if len(times) != len(subs):
            return False
        
        if len(times) < 2:  # Must have at least index 0 (None) and index 1
            return False
        
        # Check that all indices from 1 to N are filled
        for i in range(1, len(times)):
            if times[i] is None or subs[i] is None:
                return False
        
        return True
    
    @staticmethod
    def get_count(subs: List[Optional[str]]) -> int:
        """Get count of subtitles (excluding index 0)."""
        return len(subs) - 1 if len(subs) > 0 else 0


class Chunker:
    """Split subtitles into chunks for batch processing."""
    
    @staticmethod
    def chunkify(subs: List[Optional[str]], chunk_size: int = 10) -> List[Chunk]:
        """
        Split subtitles into chunks of specified size.
        
        Args:
            subs: 1-indexed subtitle array
            chunk_size: Maximum number of subtitles per chunk
            
        Returns:
            List of Chunk objects
        """
        if chunk_size < 1:
            raise ValueError("chunk_size must be >= 1")
        
        N = len(subs) - 1  # Total count (excluding index 0)
        chunks = []
        
        i = 1  # Start from index 1
        while i <= N:
            # Calculate end index for this chunk
            end = min(i + chunk_size - 1, N)
            
            # Extract lines for this chunk
            chunk_lines = [subs[j] if subs[j] is not None else "" for j in range(i, end + 1)]
            
            # Create chunk
            chunk = Chunk(start_idx=i, end_idx=end, lines=chunk_lines)
            chunks.append(chunk)
            
            i = end + 1  # Move to next chunk
        
        return chunks
    
    @staticmethod
    def merge_results(
        subs: List[Optional[str]], 
        chunks: List[Chunk], 
        results: dict
    ) -> List[Optional[str]]:
        """
        Merge translated chunks back into subtitle array.
        
        Args:
            subs: Original 1-indexed subtitle array
            chunks: List of chunks
            results: Dict mapping (start_idx, end_idx) -> List[translated_lines]
            
        Returns:
            New subtitle array with translations merged
        """
        # Create copy
        merged = subs.copy()
        
        for chunk in chunks:
            key = (chunk.start_idx, chunk.end_idx)
            if key not in results:
                continue
            
            translated = results[key]
            if len(translated) != len(chunk.lines):
                print(f"Warning: Result length mismatch for chunk {chunk}")
                continue
            
            # Merge into array
            for i, line in enumerate(translated):
                idx = chunk.start_idx + i
                if idx < len(merged):
                    merged[idx] = line
        
        return merged


def export_srt(times: List[Optional[str]], subs: List[Optional[str]]) -> str:
    """
    Export times and subs arrays back to SRT format.
    
    Args:
        times: 1-indexed timecode array
        subs: 1-indexed subtitle array
        
    Returns:
        SRT formatted string
    """
    if len(times) != len(subs):
        raise ValueError("times and subs arrays must have same length")
    
    N = len(times) - 1
    blocks = []
    
    for i in range(1, N + 1):
        if times[i] is None or subs[i] is None:
            continue
        
        block = f"{i}\n{times[i]}\n{subs[i]}\n"
        blocks.append(block)
    
    return "\n".join(blocks)


# Utility functions

def detect_encoding(file_path: str) -> str:
    """
    Detect file encoding (UTF-8, GBK, etc.).
    
    Args:
        file_path: Path to file
        
    Returns:
        Encoding name
    """
    import chardet
    
    with open(file_path, 'rb') as f:
        raw = f.read()
        result = chardet.detect(raw)
        return result['encoding'] or 'utf-8'


def read_srt_file(file_path: str) -> str:
    """
    Read SRT file with automatic encoding detection.
    
    Args:
        file_path: Path to SRT file
        
    Returns:
        File content as string
    """
    try:
        # Try UTF-8 first
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Fallback to detection
        try:
            import chardet
            encoding = detect_encoding(file_path)
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except:
            # Last resort: try common encodings
            for enc in ['gbk', 'gb2312', 'big5', 'latin-1']:
                try:
                    with open(file_path, 'r', encoding=enc) as f:
                        return f.read()
                except:
                    continue
            
            raise ValueError(f"Unable to decode file: {file_path}")


def write_srt_file(file_path: str, content: str) -> None:
    """
    Write SRT file with UTF-8 encoding.
    
    Args:
        file_path: Path to output file
        content: SRT content
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
