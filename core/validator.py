"""
Validator & Postprocessor
Validates translation responses and sanitizes output.
"""

import re
import json
from typing import List, Tuple, Optional


# CJK Unified Ideographs (common Chinese characters)
CJK_PATTERN = re.compile(r'[\u4E00-\u9FFF]')

# Additional CJK ranges (if needed for comprehensive detection)
CJK_EXTENDED_PATTERN = re.compile(
    r'[\u4E00-\u9FFF'  # CJK Unified Ideographs
    r'\u3400-\u4DBF'  # CJK Extension A
    r'\U00020000-\U0002A6DF'  # CJK Extension B
    r'\uF900-\uFAFF'  # CJK Compatibility Ideographs
    r']'
)

# Leading numbering patterns: "1. ", "01. ", "1) ", "1、", etc.
LEADING_NUMBER_PATTERN = re.compile(
    r'^\s*\d+\s*[\.\)、]\s*'
)


class TranslationValidator:
    """Validates translation API responses."""
    
    @staticmethod
    def validate_response(
        response_text: str, 
        expected_count: int,
        strict_cjk: bool = True
    ) -> Tuple[bool, Optional[List[str]], Optional[str]]:
        """
        Validate translation response.
        
        Args:
            response_text: Raw response from API (expected JSON array)
            expected_count: Expected number of translated lines
            strict_cjk: If True, use extended CJK detection
            
        Returns:
            Tuple of (is_valid, cleaned_lines, error_message)
        """
        # Try to parse JSON
        try:
            data = json.loads(response_text)
        except json.JSONDecodeError as e:
            return False, None, f"Invalid JSON: {e}"
        
        # Must be an array
        if not isinstance(data, list):
            return False, None, "Response is not a JSON array"
        
        # Check count
        if len(data) != expected_count:
            return False, None, f"Expected {expected_count} lines, got {len(data)}"
        
        # Check each line
        pattern = CJK_EXTENDED_PATTERN if strict_cjk else CJK_PATTERN
        
        for i, line in enumerate(data):
            # Convert to string
            line_str = str(line)
            
            # Check for Chinese characters
            if pattern.search(line_str):
                return False, None, f"Line {i+1} still contains Chinese characters: {line_str[:50]}"
        
        # All checks passed - sanitize and return
        cleaned = [Postprocessor.sanitize_line(str(line)) for line in data]
        return True, cleaned, None
    
    @staticmethod
    def contains_chinese(text: str, strict: bool = False) -> bool:
        """
        Check if text contains Chinese characters.
        
        Args:
            text: Text to check
            strict: Use extended CJK range
            
        Returns:
            True if Chinese detected
        """
        pattern = CJK_EXTENDED_PATTERN if strict else CJK_PATTERN
        return bool(pattern.search(text))
    
    @staticmethod
    def quick_validate_array(lines: List[str], strict: bool = False) -> Tuple[bool, List[int]]:
        """
        Quick check if any lines contain Chinese.
        
        Args:
            lines: List of translated lines
            strict: Use extended CJK range
            
        Returns:
            Tuple of (all_valid, indices_with_chinese)
        """
        pattern = CJK_EXTENDED_PATTERN if strict else CJK_PATTERN
        chinese_indices = []
        
        for i, line in enumerate(lines):
            if pattern.search(str(line)):
                chinese_indices.append(i)
        
        return len(chinese_indices) == 0, chinese_indices


class Postprocessor:
    """Post-processes translation output."""
    
    @staticmethod
    def sanitize_line(line: str) -> str:
        """
        Remove leading numbering and normalize whitespace.
        
        Args:
            line: Raw translated line
            
        Returns:
            Cleaned line
        """
        # Remove leading numbers
        line = LEADING_NUMBER_PATTERN.sub('', line)
        
        # Normalize whitespace
        line = ' '.join(line.split())
        
        # Remove leading/trailing spaces
        line = line.strip()
        
        return line
    
    @staticmethod
    def normalize_punctuation(line: str) -> str:
        """
        Normalize Vietnamese punctuation.
        
        Args:
            line: Line to normalize
            
        Returns:
            Normalized line
        """
        # Replace multiple spaces
        line = re.sub(r'\s+', ' ', line)
        
        # Normalize quotes
        line = line.replace('"', '"').replace('"', '"')
        line = line.replace(''', "'").replace(''', "'")
        
        # Ensure space after punctuation (Vietnamese style)
        line = re.sub(r'([,;:!?])([^\s])', r'\1 \2', line)
        
        # Remove space before punctuation
        line = re.sub(r'\s+([,;:!?.])', r'\1', line)
        
        return line.strip()
    
    @staticmethod
    def apply_name_mapping(line: str, name_map: dict) -> str:
        """
        Apply consistent name mapping.
        
        Args:
            line: Line to process
            name_map: Dict mapping Chinese names to Vietnamese
            
        Returns:
            Line with names replaced
        """
        for chinese, vietnamese in name_map.items():
            # Simple replacement (can be improved with word boundaries)
            line = line.replace(chinese, vietnamese)
        
        return line
    
    @staticmethod
    def process_batch(
        lines: List[str], 
        name_map: Optional[dict] = None,
        normalize: bool = True
    ) -> List[str]:
        """
        Process a batch of lines.
        
        Args:
            lines: Lines to process
            name_map: Optional name mapping
            normalize: Whether to normalize punctuation
            
        Returns:
            Processed lines
        """
        processed = []
        
        for line in lines:
            # Sanitize
            line = Postprocessor.sanitize_line(line)
            
            # Apply name mapping
            if name_map:
                line = Postprocessor.apply_name_mapping(line, name_map)
            
            # Normalize punctuation
            if normalize:
                line = Postprocessor.normalize_punctuation(line)
            
            processed.append(line)
        
        return processed
    
    @staticmethod
    def remove_html_tags(line: str) -> str:
        """
        Remove common HTML tags from subtitles.
        
        Args:
            line: Line possibly containing HTML
            
        Returns:
            Cleaned line
        """
        # Remove common subtitle HTML tags
        line = re.sub(r'</?(?:i|b|u|font)[^>]*>', '', line)
        
        # Remove \N (ASS format line break that sometimes appears)
        line = line.replace('\\N', ' ')
        
        return line.strip()


class QualityChecker:
    """Checks translation quality."""
    
    @staticmethod
    def check_length_ratio(original: str, translated: str) -> Tuple[bool, float]:
        """
        Check if translation length is reasonable.
        
        Args:
            original: Original text
            translated: Translated text
            
        Returns:
            Tuple of (is_reasonable, ratio)
        """
        if not original or not translated:
            return False, 0.0
        
        ratio = len(translated) / len(original)
        
        # Vietnamese translations are usually 0.5x to 2x original length
        is_reasonable = 0.3 <= ratio <= 3.0
        
        return is_reasonable, ratio
    
    @staticmethod
    def check_empty_translation(translated: str) -> bool:
        """
        Check if translation is empty or just whitespace.
        
        Args:
            translated: Translated text
            
        Returns:
            True if empty
        """
        return not translated or not translated.strip()
    
    @staticmethod
    def check_likely_untranslated(original: str, translated: str) -> bool:
        """
        Check if translation looks suspiciously similar (possible failure).
        
        Args:
            original: Original text
            translated: Translated text
            
        Returns:
            True if likely not translated
        """
        # If identical, definitely not translated
        if original == translated:
            return True
        
        # If >80% same characters, suspicious
        if len(original) > 5:
            same_chars = sum(1 for a, b in zip(original, translated) if a == b)
            similarity = same_chars / len(original)
            if similarity > 0.8:
                return True
        
        return False
    
    @staticmethod
    def batch_quality_check(
        originals: List[str], 
        translations: List[str]
    ) -> List[Tuple[bool, str]]:
        """
        Check quality of batch translations.
        
        Args:
            originals: Original lines
            translations: Translated lines
            
        Returns:
            List of (is_good, issue_description) tuples
        """
        if len(originals) != len(translations):
            raise ValueError("Arrays must have same length")
        
        results = []
        
        for orig, trans in zip(originals, translations):
            # Check if empty
            if QualityChecker.check_empty_translation(trans):
                results.append((False, "Empty translation"))
                continue
            
            # Check if still Chinese
            if TranslationValidator.contains_chinese(trans):
                results.append((False, "Contains Chinese"))
                continue
            
            # Check length ratio
            reasonable, ratio = QualityChecker.check_length_ratio(orig, trans)
            if not reasonable:
                results.append((False, f"Unusual length ratio: {ratio:.2f}"))
                continue
            
            # Check if untranslated
            if QualityChecker.check_likely_untranslated(orig, trans):
                results.append((False, "Possibly untranslated"))
                continue
            
            # All checks passed
            results.append((True, "OK"))
        
        return results
