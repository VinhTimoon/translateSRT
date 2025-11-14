# 📚 Documentation Index - Mục lục tài liệu

Chọn tài liệu phù hợp với nhu cầu của bạn:

## 🚀 Bắt đầu nhanh (START HERE!)

### Tiếng Việt 🇻🇳
- **[HUONG_DAN_TIENG_VIET.md](HUONG_DAN_TIENG_VIET.md)** ⭐
  - Hướng dẫn đầy đủ bằng tiếng Việt
  - Từng bước chi tiết
  - Xử lý lỗi thường gặp
  - **ĐỌC FILE NÀY NẾU BẠN LÀ NGƯỜI VIỆT**

### English / Quick Start
- **[QUICK_START.md](QUICK_START.md)** ⭐
  - 5-minute quick setup
  - Essential commands
  - Troubleshooting tips
  - **READ THIS FOR FASTEST SETUP**

## 📖 Tài liệu chính

### Toàn diện
- **[README.md](README.md)**
  - Complete documentation
  - Features, requirements, installation
  - Usage guide, troubleshooting
  - Build instructions

### Tổng quan kỹ thuật
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)**
  - Architecture overview
  - Code structure
  - Components explanation
  - Developer guide

### Hoàn thành
- **[COMPLETION.md](COMPLETION.md)**
  - Project completion checklist
  - Success metrics
  - Next steps
  - Final notes

## 🔧 Cấu hình & Setup

### API Keys
- **[API_SETUP.md](API_SETUP.md)**
  - How to get Gemini API keys
  - Configuration methods
  - Security best practices
  - Troubleshooting API issues

### Prompts
- **[PROMPTS.md](PROMPTS.md)**
  - System & user prompt templates
  - Examples with expected outputs
  - Tone guidelines
  - Customization guide

## 📝 Lịch sử & Pháp lý

### Changelog
- **[CHANGELOG.md](CHANGELOG.md)**
  - Version history
  - Features added
  - Known issues
  - Roadmap

### License
- **[LICENSE](LICENSE)**
  - MIT License
  - Terms of use
  - Free to use, modify, distribute

## 🎯 Scripts & Tools

### Setup
- **[setup.ps1](setup.ps1)**
  - Automated setup script
  - Creates venv, installs dependencies
  - Creates .env file
  - Run: `.\setup.ps1`

### Build
- **[build.ps1](build.ps1)**
  - Build executable script
  - Uses PyInstaller
  - Creates single-file .exe
  - Run: `.\build.ps1`

### Demo Test
- **[test_demo.py](test_demo.py)**
  - Test core components
  - No GUI needed
  - Good for debugging
  - Run: `python test_demo.py`

## 📂 Code Structure

### Core Logic (`core/`)
- **[core/parser.py](core/parser.py)**
  - SRT parsing
  - Chunking
  - Export

- **[core/validator.py](core/validator.py)**
  - Response validation
  - Sanitization
  - Quality checks

- **[core/translator.py](core/translator.py)**
  - Async dispatcher
  - Fallback logic
  - Statistics

- **[core/config.py](core/config.py)**
  - Configuration management
  - API keys
  - Prompt building

- **[core/project.py](core/project.py)**
  - Project save/load
  - Progress tracking
  - Status management

### GUI (`gui/`)
- **[gui/main_window.py](gui/main_window.py)**
  - PySide6 main window
  - All UI logic
  - Worker threads

### Tests (`tests/`)
- **[tests/test_parser.py](tests/test_parser.py)**
  - Parser unit tests
  - Chunker tests
  - Export tests

- **[tests/test_validator.py](tests/test_validator.py)**
  - Validation tests
  - Postprocessor tests
  - Quality checker tests

## 🗂️ Resources

### Sample Files
- **[resources/sample.srt](resources/sample.srt)**
  - Sample Chinese SRT file (10 lines)
  - Good for testing
  - Copy to test your setup

## ⚙️ Configuration Files

### Environment
- **[.env.example](.env.example)**
  - Template for API keys
  - Copy to .env and fill in
  - Never commit .env!

### Build Config
- **[build.spec](build.spec)**
  - PyInstaller configuration
  - Controls how .exe is built
  - Advanced users only

- **[requirements.txt](requirements.txt)**
  - Python dependencies
  - Install: `pip install -r requirements.txt`

### Git
- **[.gitignore](.gitignore)**
  - Files to ignore in Git
  - Includes .env, venv, etc.

## 📊 Workflow Guides

### For End Users
1. **[HUONG_DAN_TIENG_VIET.md](HUONG_DAN_TIENG_VIET.md)** (Tiếng Việt) hoặc
2. **[QUICK_START.md](QUICK_START.md)** (English)
3. Run: `.\setup.ps1`
4. Edit: `.env`
5. Run: `python main.py`

### For Developers
1. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Architecture
2. **[PROMPTS.md](PROMPTS.md)** - How translation works
3. **[core/](core/)** - Read source code
4. **[tests/](tests/)** - See test examples
5. Modify and contribute!

### For Troubleshooting
1. Check **[QUICK_START.md](QUICK_START.md)** troubleshooting section
2. Check **[HUONG_DAN_TIENG_VIET.md](HUONG_DAN_TIENG_VIET.md)** phần xử lý lỗi
3. Check **[API_SETUP.md](API_SETUP.md)** for API issues
4. Run `python test_demo.py` to test components
5. Check logs in app

## 🎓 Learning Path

### Beginner
1. **[QUICK_START.md](QUICK_START.md)** or **[HUONG_DAN_TIENG_VIET.md](HUONG_DAN_TIENG_VIET.md)**
2. **[README.md](README.md)** - Full guide
3. Use the app!

### Intermediate
1. **[API_SETUP.md](API_SETUP.md)** - Understand API
2. **[PROMPTS.md](PROMPTS.md)** - Understand translation
3. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Architecture

### Advanced
1. **[core/](core/)** - Read source
2. **[tests/](tests/)** - Write tests
3. **[build.spec](build.spec)** - Customize build
4. Extend and contribute!

## 🔍 Quick Reference

| Need | File |
|------|------|
| Setup app | [QUICK_START.md](QUICK_START.md) |
| Setup (Tiếng Việt) | [HUONG_DAN_TIENG_VIET.md](HUONG_DAN_TIENG_VIET.md) |
| Get API keys | [API_SETUP.md](API_SETUP.md) |
| Understand prompts | [PROMPTS.md](PROMPTS.md) |
| Architecture | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) |
| Troubleshoot | README.md, QUICK_START.md |
| Code structure | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) |
| Test app | [test_demo.py](test_demo.py) |
| Build exe | [build.ps1](build.ps1) |

## 📞 Support

1. **Read docs** - Start with appropriate guide above
2. **Check logs** - In app's Logs tab
3. **Test components** - Run `test_demo.py`
4. **Review code** - Check [core/](core/) files

## ✨ Quick Commands

```powershell
# Setup
.\setup.ps1

# Run app
python main.py

# Test
python test_demo.py
pytest tests/ -v

# Build
.\build.ps1
```

---

**Choose your starting point and enjoy! 🎬✨**

*All documents are in English except HUONG_DAN_TIENG_VIET.md which is in Vietnamese.*
