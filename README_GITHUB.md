# 🎬 SRT Translator - Chinese to Vietnamese

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PySide6](https://img.shields.io/badge/PySide6-6.6+-green.svg)](https://pypi.org/project/PySide6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Desktop application for translating SRT subtitle files from Chinese to Vietnamese using Gemini AI.

![Demo](https://via.placeholder.com/800x450?text=SRT+Translator+Demo)

## ✨ Features

- 🚀 **Fast Translation**: 10 parallel threads (2 primary APIs × 5 threads)
- 🔄 **Auto Retry**: Dual fallback APIs with up to 3 retry rounds
- ✅ **Smart Validation**: JSON format + line count + Chinese character detection
- 🏷️ **Name Mapping**: Consistent Hán-Việt name translation
- 💾 **Save/Resume**: Project save/load for large files
- 🖥️ **User-Friendly GUI**: PySide6-based desktop interface
- 📊 **Real-time Progress**: Visual feedback and comprehensive logging
- ✏️ **Manual Editing**: Fix translations directly in the app
- 🎯 **Export Validation**: Won't export if Chinese characters remain

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone <repository-url>
cd trs
.\setup.ps1  # Automated setup (Windows PowerShell)
```

### 2. Configure API Keys
Get your Gemini API key from: https://makersuite.google.com/app/apikey

Edit `.env`:
```env
GEMINI_PRIMARY_API1_KEY=your_key_here
GEMINI_PRIMARY_API2_KEY=your_key_here
GEMINI_FALLBACK_API1_KEY=your_key_here
GEMINI_FALLBACK_API2_KEY=your_key_here
```

### 3. Run
```bash
python main.py
```

## 📖 Documentation

- **[START_HERE.md](START_HERE.md)** - Start here!
- **[QUICK_START.md](QUICK_START.md)** - 5-minute setup guide
- **[HUONG_DAN_TIENG_VIET.md](HUONG_DAN_TIENG_VIET.md)** - Hướng dẫn tiếng Việt
- **[INDEX.md](INDEX.md)** - All documentation organized

## 🎯 Usage

1. **Open SRT** → Select Chinese subtitle file
2. **Configure** → Choose model, chunk size, tone
3. **Start Translation** → Watch progress bar
4. **Preview & Edit** → Review results, fix if needed
5. **Export** → Save Vietnamese subtitle file

## 🏗️ Architecture

```
┌─────────────┐
│   GUI (Qt)  │
└──────┬──────┘
       │
┌──────▼────────────────────────┐
│  Translation Dispatcher       │
│  (Async, 10 parallel threads) │
└──────┬────────────────────────┘
       │
   ┌───┴───┐
   │       │
┌──▼──┐ ┌──▼──┐
│ API1│ │ API2│  ← Primary (parallel)
└─────┘ └─────┘
   │       │
   └───┬───┘
       │ (on failure)
   ┌───┴───┐
   │       │
┌──▼──┐ ┌──▼──┐
│ API3│ │ API4│  ← Fallback (retry 3x)
└─────┘ └─────┘
```

## 🛠️ Tech Stack

- **Python 3.10+**
- **PySide6** - Qt for Python (GUI)
- **httpx** - Async HTTP client
- **python-dotenv** - Environment variables
- **pytest** - Testing framework
- **PyInstaller** - Executable builder

## 📊 Performance

- **Speed**: ~30-60 seconds for 100 lines
- **Success Rate**: ~95% with default settings
- **Concurrency**: 10 parallel threads
- **Retry**: Up to 3 fallback rounds

## 🧪 Testing

```bash
# Run unit tests
pytest tests/ -v

# Test without GUI
python test_demo.py

# Test with sample file
python main.py  # Then load resources/sample.srt
```

## 📦 Build Executable

```bash
.\build.ps1
# Output: dist/SRT_Translator.exe
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Update documentation
5. Submit a pull request

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Credits

- **Gemini API** by Google AI
- **PySide6** - Qt for Python
- **httpx** - Modern HTTP client

## 📧 Support

- **Documentation**: See [INDEX.md](INDEX.md)
- **Issues**: Open a GitHub issue
- **API Setup**: See [API_SETUP.md](API_SETUP.md)

## 🌟 Star History

If this project helps you, consider giving it a star! ⭐

---

**Made with ❤️ for subtitle translators worldwide**

🇻🇳 Tiếng Việt: Đọc [HUONG_DAN_TIENG_VIET.md](HUONG_DAN_TIENG_VIET.md)
