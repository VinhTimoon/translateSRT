"""
Configuration Management
Handles API keys, settings, and name mappings.
"""

import os
import json
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


@dataclass
class APIConfig:
    """Configuration for a single API."""
    name: str
    key: str
    endpoint: str
    is_primary: bool = True
    max_threads: int = 5
    requests_per_second: float = 5.0
    timeout: float = 30.0


@dataclass
class TranslationSettings:
    """Translation behavior settings."""
    model: str = "gemini-2.5-flash"  # Default model
    chunk_size: int = 10
    threads_per_api: int = 5
    retry_rounds: int = 3
    tone: str = "conversational"  # conversational, formal, literal
    strict_cjk_check: bool = True
    normalize_punctuation: bool = True
    remove_html_tags: bool = True
    timeout: float = 30.0
    
    # Available models
    AVAILABLE_MODELS = [
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite"
    ]


class ConfigManager:
    """Manages application configuration."""
    
    # System prompts for Gemini
    SYSTEM_PROMPT = """You are a professional translator model. Translate Chinese subtitle lines to Vietnamese. Output must be a JSON array of strings only (e.g. ["...", "..."]). Do NOT include indices, timestamps, explanations, or any other text. Preserve the number and order of lines exactly as input. Remove any leading numbering in the input lines before translating. Use natural conversational Vietnamese fitting film subtitles. Keep translations concise, preserve tone, and maintain name consistency (use provided name_map). If unsure, translate literally but natural. If input is empty string, output empty string for that line. Output must be valid JSON."""
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize config manager.
        
        Args:
            config_dir: Directory for config files (default: ~/.srt_translator)
        """
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = Path.home() / ".srt_translator"
        
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.config_dir / "config.json"
        self.name_map_file = self.config_dir / "name_map.json"
        
        # Load configurations
        self.apis: List[APIConfig] = []
        self.settings = TranslationSettings()
        self.name_map: Dict[str, str] = {}
        
        self._load_from_env()
        self._load_settings()
        self._load_name_map()
    
    def _load_from_env(self):
        """Load API configurations from environment variables."""
        # Get endpoint template
        endpoint_template = os.getenv(
            'GEMINI_API_ENDPOINT',
            'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent'
        )
        
        # Primary APIs
        primary_keys = [
            os.getenv('GEMINI_PRIMARY_API1_KEY'),
            os.getenv('GEMINI_PRIMARY_API2_KEY')
        ]
        
        for i, key in enumerate(primary_keys):
            if key and key != 'your_primary_api_key_1_here' and key != 'your_primary_api_key_2_here':
                self.apis.append(APIConfig(
                    name=f"Primary-{i+1}",
                    key=key,
                    endpoint=endpoint_template,
                    is_primary=True,
                    max_threads=5
                ))
        
        # Fallback APIs
        fallback_keys = [
            os.getenv('GEMINI_FALLBACK_API1_KEY'),
            os.getenv('GEMINI_FALLBACK_API2_KEY')
        ]
        
        for i, key in enumerate(fallback_keys):
            if key and key != 'your_fallback_api_key_3_here' and key != 'your_fallback_api_key_4_here':
                self.apis.append(APIConfig(
                    name=f"Fallback-{i+1}",
                    key=key,
                    endpoint=endpoint_template,
                    is_primary=False,
                    max_threads=2
                ))
        
        # Load default model
        default_model = os.getenv('DEFAULT_GEMINI_MODEL', 'gemini-2.5-flash')
        if default_model in TranslationSettings.AVAILABLE_MODELS:
            self.settings.model = default_model
        
        # Load rate limit
        rate_limit = os.getenv('RATE_LIMIT_PER_API')
        if rate_limit:
            try:
                self.settings.threads_per_api = int(float(rate_limit))
            except:
                pass
    
    def _load_settings(self):
        """Load settings from config file."""
        if not self.config_file.exists():
            self._save_settings()
            return
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Update settings
            for key, value in data.items():
                if hasattr(self.settings, key):
                    setattr(self.settings, key, value)
        except Exception as e:
            print(f"Warning: Could not load settings: {e}")
    
    def _save_settings(self):
        """Save settings to config file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.settings), f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save settings: {e}")
    
    def _load_name_map(self):
        """Load name mapping from file."""
        if not self.name_map_file.exists():
            self._save_name_map()
            return
        
        try:
            with open(self.name_map_file, 'r', encoding='utf-8') as f:
                self.name_map = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load name map: {e}")
            self.name_map = {}
    
    def _save_name_map(self):
        """Save name mapping to file."""
        try:
            with open(self.name_map_file, 'w', encoding='utf-8') as f:
                json.dump(self.name_map, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save name map: {e}")
    
    def get_primary_apis(self) -> List[APIConfig]:
        """Get primary API configurations."""
        return [api for api in self.apis if api.is_primary]
    
    def get_fallback_apis(self) -> List[APIConfig]:
        """Get fallback API configurations."""
        return [api for api in self.apis if not api.is_primary]
    
    def has_valid_apis(self) -> bool:
        """Check if at least one API is configured."""
        return len(self.apis) > 0
    
    def update_settings(self, **kwargs):
        """
        Update settings.
        
        Args:
            **kwargs: Settings to update
        """
        for key, value in kwargs.items():
            if hasattr(self.settings, key):
                setattr(self.settings, key, value)
        
        self._save_settings()
    
    def add_name_mapping(self, chinese: str, vietnamese: str):
        """
        Add or update name mapping.
        
        Args:
            chinese: Chinese name
            vietnamese: Vietnamese equivalent
        """
        self.name_map[chinese] = vietnamese
        self._save_name_map()
    
    def remove_name_mapping(self, chinese: str):
        """
        Remove name mapping.
        
        Args:
            chinese: Chinese name to remove
        """
        if chinese in self.name_map:
            del self.name_map[chinese]
            self._save_name_map()
    
    def clear_name_mappings(self):
        """Clear all name mappings."""
        self.name_map = {}
        self._save_name_map()
    
    def build_user_prompt(
        self, 
        lines: List[str], 
        start_idx: int, 
        end_idx: int
    ) -> str:
        """
        Build user prompt for translation API.
        
        Args:
            lines: Lines to translate
            start_idx: Starting index (1-based)
            end_idx: Ending index (1-based)
            
        Returns:
            Formatted prompt
        """
        prompt = f"""NameMap: {json.dumps(self.name_map, ensure_ascii=False)}
Tone: {self.settings.tone}
ChunkIndices: [{start_idx}-{end_idx}]
Lines: {json.dumps(lines, ensure_ascii=False)}

Translate the Lines array from Chinese to Vietnamese. Return a JSON array of {len(lines)} strings only. Ensure the i-th output corresponds to the i-th input line. DO NOT add numbering or timestamps. DO NOT change punctuation meaningfully. If a name appears that is in NameMap, use that Hán-Việt mapping. If the translated line still contains Chinese characters, that counts as invalid."""
        
        return prompt
    
    def get_api_endpoint(self, api: APIConfig) -> str:
        """
        Get full API endpoint with model substituted.
        
        Args:
            api: API configuration
            
        Returns:
            Full endpoint URL
        """
        return api.endpoint.replace('{model}', self.settings.model)
    
    def validate_config(self) -> List[str]:
        """
        Validate configuration.
        
        Returns:
            List of error messages (empty if valid)
        """
        errors = []
        
        if not self.has_valid_apis():
            errors.append("No API keys configured. Please set environment variables.")
        
        if len(self.get_primary_apis()) == 0:
            errors.append("No primary APIs configured.")
        
        if self.settings.chunk_size < 1:
            errors.append("chunk_size must be >= 1")
        
        if self.settings.threads_per_api < 1:
            errors.append("threads_per_api must be >= 1")
        
        if self.settings.retry_rounds < 0:
            errors.append("retry_rounds must be >= 0")
        
        if self.settings.model not in TranslationSettings.AVAILABLE_MODELS:
            errors.append(f"Invalid model: {self.settings.model}")
        
        return errors
    
    def get_summary(self) -> str:
        """
        Get configuration summary.
        
        Returns:
            Summary string
        """
        primary = len(self.get_primary_apis())
        fallback = len(self.get_fallback_apis())
        
        summary = f"""Configuration Summary:
- Model: {self.settings.model}
- Primary APIs: {primary}
- Fallback APIs: {fallback}
- Chunk Size: {self.settings.chunk_size}
- Threads per API: {self.settings.threads_per_api}
- Retry Rounds: {self.settings.retry_rounds}
- Tone: {self.settings.tone}
- Name Mappings: {len(self.name_map)}
"""
        return summary


# Global config instance (can be initialized once)
_config_instance: Optional[ConfigManager] = None


def get_config() -> ConfigManager:
    """Get global config instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigManager()
    return _config_instance


def reset_config():
    """Reset global config instance."""
    global _config_instance
    _config_instance = None
