# 🎬 SRT Translator - Tổng quan Project

## 📁 Cấu trúc hoàn chỉnh

```
trs/
├── README.md                 # Tài liệu chính (đầy đủ)
├── QUICK_START.md           # Hướng dẫn nhanh 5 phút
├── API_SETUP.md             # Chi tiết về API keys
├── PROMPTS.md               # Giải thích prompts dịch
├── requirements.txt         # Dependencies Python
├── .env.example             # Mẫu cấu hình API
├── .gitignore              # Git ignore rules
│
├── main.py                  # Entry point - chạy app
├── test_demo.py            # Script test components
├── build.spec              # PyInstaller config
├── build.ps1               # Build script
│
├── core/                    # Core logic
│   ├── __init__.py
│   ├── parser.py           # Parse SRT → arrays, chunking
│   ├── validator.py        # Validate response, sanitize
│   ├── translator.py       # Async dispatcher, fallback
│   ├── config.py           # Config & API management
│   └── project.py          # Project save/load
│
├── gui/                     # GUI interface
│   ├── __init__.py
│   └── main_window.py      # PySide6 main window
│
├── tests/                   # Unit tests
│   ├── __init__.py
│   ├── test_parser.py
│   └── test_validator.py
│
└── resources/               # Resources
    └── sample.srt          # Sample SRT file
```

## ✨ Tính năng đã implement

### Core Features ✅
- [x] Parse SRT thành arrays 1-indexed (times[], subs[])
- [x] Chunking thông minh (configurable chunk size)
- [x] Dual primary APIs với 5 threads mỗi API = 10 parallel
- [x] Dual fallback APIs chạy song song
- [x] Retry logic tối đa 3 rounds
- [x] Validation: JSON format + số dòng + phát hiện CJK
- [x] Postprocessing: xóa numbering + normalize
- [x] Name mapping (Hán-Việt consistency)
- [x] 4 Gemini models: flash/lite variants 2.0/2.5
- [x] Project save/load (resume capability)
- [x] Export SRT với validation

### GUI Features ✅
- [x] Upload SRT file
- [x] Settings panel (model, chunk, threads, tone)
- [x] Progress bar + real-time logs
- [x] Preview table (5 columns)
- [x] Manual edit capability
- [x] Export với safety checks
- [x] Save/Load project
- [x] Context menu (right-click)
- [x] Color-coded status

### Quality Features ✅
- [x] CJK detection (Chinese chars)
- [x] Response validation (count, format)
- [x] Automatic retry on failure
- [x] Fallback to original on total failure
- [x] Quality checks (length ratio, empty, etc.)
- [x] Statistics tracking
- [x] Comprehensive logging

### Security & Best Practices ✅
- [x] Environment variables for API keys
- [x] .env.example template
- [x] Config stored in ~/.srt_translator
- [x] No hardcoded secrets
- [x] .gitignore properly configured
- [x] Rate limiting per API
- [x] Semaphore concurrency control

### Testing ✅
- [x] Unit tests for parser
- [x] Unit tests for validator
- [x] Test demo script
- [x] Sample SRT file
- [x] Pytest configuration

### Build & Deploy ✅
- [x] PyInstaller spec
- [x] PowerShell build script
- [x] Single-file executable
- [x] README with build instructions

## 🎯 Workflow hoàn chỉnh

```
1. User opens SRT file
   ↓
2. Parser extracts times[] + subs[] (1-indexed)
   ↓
3. Create project with metadata
   ↓
4. Chunker splits into chunks (chunk_size=10)
   ↓
5. Dispatcher sends to 2 primary APIs (parallel, 5 threads each)
   ↓
6. Validator checks response (JSON + count + CJK)
   ↓
7. If valid → Postprocess (sanitize + name map)
   ↓
8. If invalid → Fallback: 2 APIs parallel, retry 3x
   ↓
9. If still fails → Keep original Chinese + mark unresolved
   ↓
10. Merge results into subs_translated[]
   ↓
11. Preview table shows results with status
   ↓
12. User can edit manually
   ↓
13. Export SRT if all done (or force export)
```

## 🔑 Các thành phần chính

### 1. Parser (`core/parser.py`)
- `SRTParser.parse()` → (times, subs)
- `Chunker.chunkify()` → List[Chunk]
- `export_srt()` → SRT string
- Auto-detect encoding

### 2. Validator (`core/validator.py`)
- `TranslationValidator.validate_response()` → (valid, cleaned, error)
- `Postprocessor.sanitize_line()` → remove numbering
- `QualityChecker` → length ratio, empty, untranslated

### 3. Translator (`core/translator.py`)
- `TranslationDispatcher` → async context manager
- `translate_chunks()` → Dict[key, lines]
- Primary → Fallback logic
- Semaphore per API
- Progress callback
- Statistics tracking

### 4. Config (`core/config.py`)
- `ConfigManager` → load from env
- `build_user_prompt()` → format prompt
- Settings management
- Name mapping

### 5. Project (`core/project.py`)
- `ProjectManager` → save/load JSON
- Track status per line
- Resume capability
- Export validation

### 6. GUI (`gui/main_window.py`)
- PySide6 QMainWindow
- Worker thread for async
- Progress signals
- Preview table
- File dialogs

## 📊 Prompts sử dụng

### System Prompt
```
You are a professional translator model. 
Translate Chinese subtitle lines to Vietnamese. 
Output must be a JSON array of strings only.
[... xem PROMPTS.md cho chi tiết ...]
```

### User Prompt Template
```
NameMap: {name_map}
Tone: {tone}
ChunkIndices: [{start}-{end}]
Lines: {array}

Translate the Lines array...
[... xem PROMPTS.md cho chi tiết ...]
```

## 🔧 Cấu hình mặc định

```python
model = "gemini-2.5-flash"
chunk_size = 10
threads_per_api = 5
retry_rounds = 3
tone = "conversational"
strict_cjk_check = True
timeout = 30.0
```

## 📈 Performance

**Ví dụ**: File 100 dòng

- Chunk size = 10 → 10 chunks
- Primary APIs = 2 → 10 threads total
- Mỗi chunk ~2-3s
- Total time: ~20-30s (parallel)
- Success rate: ~95%

**With fallback**: 5% failed → retry 2-3 APIs → +10-15s

**Total**: ~30-45s cho 100 dòng

## 🚀 Quick Start Commands

```powershell
# Setup
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your API keys

# Run
python main.py

# Test
pytest tests/ -v
python test_demo.py

# Build
.\build.ps1
```

## 📚 Documentation Files

1. **README.md** - Main documentation (setup, usage, troubleshooting)
2. **QUICK_START.md** - 5-minute quick start guide
3. **API_SETUP.md** - Detailed API key setup
4. **PROMPTS.md** - Prompt engineering guide
5. **PROJECT_SUMMARY.md** - This file (overview)

## 🎓 Kiến thức yêu cầu

- **Python**: async/await, typing, dataclasses
- **PySide6**: QMainWindow, signals/slots, threading
- **Async IO**: asyncio, httpx
- **API**: REST, JSON, authentication
- **SRT format**: Understanding subtitle structure

## 🔮 Future Enhancements (Roadmap)

- [ ] Batch processing (multiple files)
- [ ] Translation memory / cache
- [ ] More output formats (ASS, VTT)
- [ ] More languages (Japanese, Korean)
- [ ] Cloud sync
- [ ] Undo/Redo for edits
- [ ] Better name mapping UI
- [ ] Single-line re-translation
- [ ] Auto-detect tone from content
- [ ] Progress persistence across restarts

## 🐛 Known Issues

1. **Chardet dependency**: For encoding detection (optional)
2. **Import errors before pip install**: Normal, run pip first
3. **Model occasionally adds numbering**: Auto-sanitized
4. **Rate limits with free tier**: Use multiple keys
5. **Large files (>1000 lines)**: Use save/load project

## 💡 Tips cho Developer

1. **Modify prompts**: Edit `core/config.py` → `SYSTEM_PROMPT`
2. **Add new model**: Add to `TranslationSettings.AVAILABLE_MODELS`
3. **Custom validation**: Extend `TranslationValidator`
4. **New language**: Modify prompts + validation regex
5. **GUI tweaks**: Edit `gui/main_window.py`
6. **Add tests**: Follow pattern in `tests/`

## 🤝 Contribution

To contribute:
1. Fork repo
2. Create feature branch
3. Add tests for new features
4. Update documentation
5. Submit pull request

## 📜 License

MIT License - Free to use, modify, distribute

## 🙏 Credits

- **Gemini API**: Google AI
- **PySide6**: Qt for Python
- **httpx**: Modern HTTP client
- **python-dotenv**: Environment management

---

**Made with ❤️ for subtitle translators worldwide**

Version: 1.0.0
Date: 2025-01-14
