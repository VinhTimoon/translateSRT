"""
Unit tests for SRT parser.
"""

import pytest
from core.parser import SRTParser, Chunker, export_srt


class TestSRTParser:
    """Test SRT parsing functionality."""
    
    def test_basic_parsing(self):
        """Test basic SRT parsing."""
        srt_content = """1
00:00:01,000 --> 00:00:03,000
加班猝死

2
00:00:03,000 --> 00:00:05,000
我串到了狗血大同小说

3
00:00:05,000 --> 00:00:07,000
好消息猝死后穿越活了坏消息
"""
        
        times, subs = SRTParser.parse(srt_content)
        
        assert len(times) == 4  # Index 0 (None) + 3 subtitles
        assert len(subs) == 4
        assert times[0] is None
        assert subs[0] is None
        assert times[1] == "00:00:01,000 --> 00:00:03,000"
        assert subs[1] == "加班猝死"
        assert subs[3] == "好消息猝死后穿越活了坏消息"
    
    def test_multiline_subtitle(self):
        """Test parsing multiline subtitles."""
        srt_content = """1
00:00:01,000 --> 00:00:03,000
第一行
第二行
第三行
"""
        
        times, subs = SRTParser.parse(srt_content)
        
        assert subs[1] == "第一行\n第二行\n第三行"
    
    def test_validation(self):
        """Test SRT validation."""
        times = [None, "00:00:01,000 --> 00:00:03,000"]
        subs = [None, "Test"]
        
        assert SRTParser.validate(times, subs)
        
        # Invalid: mismatched lengths
        invalid_times = [None]
        invalid_subs = [None, "Test"]
        assert not SRTParser.validate(invalid_times, invalid_subs)
        
        # Invalid: missing data
        incomplete_times = [None, None]
        incomplete_subs = [None, "Test"]
        assert not SRTParser.validate(incomplete_times, incomplete_subs)
    
    def test_get_count(self):
        """Test subtitle count."""
        subs = [None, "Line 1", "Line 2", "Line 3"]
        assert SRTParser.get_count(subs) == 3


class TestChunker:
    """Test chunking functionality."""
    
    def test_basic_chunking(self):
        """Test basic chunking."""
        subs = [None, "Line 1", "Line 2", "Line 3", "Line 4", "Line 5"]
        chunks = Chunker.chunkify(subs, chunk_size=2)
        
        assert len(chunks) == 3
        assert chunks[0].start_idx == 1
        assert chunks[0].end_idx == 2
        assert chunks[0].lines == ["Line 1", "Line 2"]
        
        assert chunks[2].start_idx == 5
        assert chunks[2].end_idx == 5
        assert chunks[2].lines == ["Line 5"]
    
    def test_exact_division(self):
        """Test when count divides evenly."""
        subs = [None, "A", "B", "C", "D"]
        chunks = Chunker.chunkify(subs, chunk_size=2)
        
        assert len(chunks) == 2
        assert chunks[0].lines == ["A", "B"]
        assert chunks[1].lines == ["C", "D"]
    
    def test_merge_results(self):
        """Test merging chunk results."""
        subs = [None, "原1", "原2", "原3"]
        chunks = Chunker.chunkify(subs, chunk_size=2)
        
        results = {
            (1, 2): ["译1", "译2"],
            (3, 3): ["译3"]
        }
        
        merged = Chunker.merge_results(subs, chunks, results)
        
        assert merged[1] == "译1"
        assert merged[2] == "译2"
        assert merged[3] == "译3"


class TestExport:
    """Test SRT export."""
    
    def test_export_srt(self):
        """Test exporting SRT."""
        times = [None, "00:00:01,000 --> 00:00:03,000", "00:00:03,000 --> 00:00:05,000"]
        subs = [None, "First line", "Second line"]
        
        result = export_srt(times, subs)
        
        assert "1\n" in result
        assert "00:00:01,000 --> 00:00:03,000" in result
        assert "First line" in result
        assert "2\n" in result
        assert "Second line" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
