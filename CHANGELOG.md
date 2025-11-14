# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-01-14

### Added
- Initial release of SRT Translator
- Chinese to Vietnamese translation support
- Dual primary API system with 10 parallel threads
- Dual fallback API system with automatic retry (3 rounds)
- 4 Gemini model variants support (flash/lite, 2.0/2.5)
- Smart chunking with configurable chunk size
- Response validation (JSON format, line count, CJK detection)
- Automatic postprocessing (numbering removal, normalization)
- Name mapping system for consistent Hán-Việt names
- Project save/load capability for resume
- PySide6 GUI with real-time progress tracking
- Preview table with manual edit capability
- Export validation (blocks if lines contain Chinese)
- Statistics tracking per translation session
- Comprehensive logging system
- Unit tests for parser and validator
- PyInstaller build configuration
- PowerShell setup and build scripts
- Complete documentation (README, Quick Start, API Setup, Prompts)

### Features
- **Parser**: SRT → 1-indexed arrays (times[], subs[])
- **Chunker**: Configurable chunk size (default: 10 lines)
- **Dispatcher**: Async translation with semaphore control
- **Validator**: JSON + count + CJK character detection
- **Postprocessor**: Remove numbering, normalize punctuation
- **Config**: Environment variable based (secure)
- **Project**: JSON-based save/load for resume
- **GUI**: Upload, settings, progress, preview, export
- **Quality**: Length ratio check, empty detection, similarity check
- **Security**: No hardcoded keys, .env support, .gitignore

### Technical
- Python 3.10+ required
- PySide6 for GUI
- httpx for async HTTP
- python-dotenv for config
- pytest for testing
- PyInstaller for builds

### Documentation
- README.md - Complete guide
- QUICK_START.md - 5-minute setup
- API_SETUP.md - API key details
- PROMPTS.md - Prompt engineering
- PROJECT_SUMMARY.md - Technical overview
- LICENSE - MIT License
- CHANGELOG.md - This file

### Known Issues
- chardet dependency optional (encoding detection)
- Import errors before pip install (expected)
- Model occasionally adds numbering (auto-sanitized)
- Rate limits with free tier (use multiple keys)

### Future
- Batch processing multiple files
- Translation memory/cache
- More output formats (ASS, VTT)
- More languages (Japanese, Korean)
- Cloud sync
- Undo/Redo

---

## [Unreleased]

### Planned
- Single-line re-translation feature
- Better name mapping UI dialog
- Auto-save on interval
- Export to multiple formats
- Tone detection from content
- Translation preview before full run

---

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
