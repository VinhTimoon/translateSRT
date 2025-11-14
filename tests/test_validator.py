"""
Unit tests for validator.
"""

import pytest
from core.validator import (
    TranslationValidator,
    Postprocessor,
    QualityChecker
)


class TestTranslationValidator:
    """Test translation validation."""
    
    def test_valid_response(self):
        """Test valid JSON response."""
        response = '["Xin chào", "Tạm biệt", "Cảm ơn"]'
        valid, cleaned, error = TranslationValidator.validate_response(response, 3)
        
        assert valid
        assert cleaned == ["Xin chào", "Tạm biệt", "Cảm ơn"]
        assert error is None
    
    def test_chinese_detection(self):
        """Test Chinese character detection."""
        response = '["你好", "Tạm biệt", "Cảm ơn"]'
        valid, cleaned, error = TranslationValidator.validate_response(response, 3)
        
        assert not valid
        assert "Chinese" in error
    
    def test_wrong_count(self):
        """Test wrong line count."""
        response = '["Xin chào", "Tạm biệt"]'
        valid, cleaned, error = TranslationValidator.validate_response(response, 3)
        
        assert not valid
        assert "Expected 3" in error
    
    def test_invalid_json(self):
        """Test invalid JSON."""
        response = 'not a json'
        valid, cleaned, error = TranslationValidator.validate_response(response, 1)
        
        assert not valid
        assert "JSON" in error
    
    def test_contains_chinese(self):
        """Test Chinese detection in text."""
        assert TranslationValidator.contains_chinese("你好世界")
        assert TranslationValidator.contains_chinese("Hello 你好")
        assert not TranslationValidator.contains_chinese("Hello world")
        assert not TranslationValidator.contains_chinese("Xin chào")


class TestPostprocessor:
    """Test postprocessing."""
    
    def test_sanitize_leading_numbers(self):
        """Test removing leading numbers."""
        assert Postprocessor.sanitize_line("1. Xin chào") == "Xin chào"
        assert Postprocessor.sanitize_line("01. Xin chào") == "Xin chào"
        assert Postprocessor.sanitize_line("1) Xin chào") == "Xin chào"
        assert Postprocessor.sanitize_line("10、Xin chào") == "Xin chào"
        assert Postprocessor.sanitize_line("Xin chào") == "Xin chào"
    
    def test_normalize_whitespace(self):
        """Test whitespace normalization."""
        assert Postprocessor.sanitize_line("Xin   chào") == "Xin chào"
        assert Postprocessor.sanitize_line("  Xin chào  ") == "Xin chào"
    
    def test_apply_name_mapping(self):
        """Test name mapping."""
        name_map = {"张伟": "Trương Vĩ", "李芳": "Lý Phương"}
        
        result = Postprocessor.apply_name_mapping("张伟 nói với 李芳", name_map)
        assert result == "Trương Vĩ nói với Lý Phương"
    
    def test_process_batch(self):
        """Test batch processing."""
        lines = ["1. Xin chào", "2. Tạm biệt"]
        name_map = {}
        
        processed = Postprocessor.process_batch(lines, name_map, normalize=True)
        
        assert processed[0] == "Xin chào"
        assert processed[1] == "Tạm biệt"


class TestQualityChecker:
    """Test quality checking."""
    
    def test_length_ratio(self):
        """Test length ratio checking."""
        reasonable, ratio = QualityChecker.check_length_ratio("你好世界", "Xin chào thế giới")
        assert reasonable
        
        # Very short translation - suspicious
        reasonable, ratio = QualityChecker.check_length_ratio("这是一个很长的句子", "Hi")
        assert not reasonable
    
    def test_empty_translation(self):
        """Test empty translation detection."""
        assert QualityChecker.check_empty_translation("")
        assert QualityChecker.check_empty_translation("   ")
        assert not QualityChecker.check_empty_translation("Xin chào")
    
    def test_untranslated_detection(self):
        """Test detection of untranslated text."""
        # Identical
        assert QualityChecker.check_likely_untranslated("你好", "你好")
        
        # Very similar
        assert QualityChecker.check_likely_untranslated("Hello world", "Hello world!")
        
        # Actually translated
        assert not QualityChecker.check_likely_untranslated("你好", "Xin chào")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
