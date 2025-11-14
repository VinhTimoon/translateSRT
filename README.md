# SRT Translator - Chinese to Vietnamese

Desktop application dịch phụ đề SRT từ tiếng Trung sang tiếng Việt sử dụng Gemini API với khả năng xử lý song song, fallback thông minh và giao diện thân thiện.

## Tính năng chính

- ✅ **Parsing thông minh**: Tách file SRT thành timecodes và subtitles (indexed từ 1)
- ✅ **Dịch song song**: 2 API chính (mỗi API 5 luồng = tổng 10 song song)
- ✅ **Fallback tự động**: 2 API phụ chạy song song, retry tối đa 3 lần
- ✅ **Validation nghiêm ngặt**: Kiểm tra số dòng, phát hiện tiếng Trung còn sót
- ✅ **Preview & Edit**: Xem trước, sửa thủ công, dịch lại từng dòng
- ✅ **Name mapping**: Đồng nhất tên Hán-Việt trong toàn bộ phụ đề
- ✅ **Project management**: Lưu/Load project để resume khi cần
- ✅ **4 Modal Gemini**: gemini-2.5-flash, gemini-2.5-flash-lite, gemini-2.0-flash, gemini-2.0-flash-lite

## Yêu cầu hệ thống

- Windows 10/11
- Python 3.10+
- Internet connection (để gọi Gemini API)

## Cài đặt

### 1. Clone/Download project

```powershell
cd e:\MyProj\trs
```

### 2. Tạo virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Cài đặt dependencies

```powershell
pip install -r requirements.txt
```

### 4. Cấu hình API Keys

**⚠️ BẢO MẬT**: Không lưu API keys trực tiếp vào code!

Tạo file `.env` trong thư mục gốc project:

```
# Primary APIs
GEMINI_PRIMARY_API1_KEY=your_api_key_1_here
GEMINI_PRIMARY_API2_KEY=your_api_key_2_here

# Fallback APIs
GEMINI_FALLBACK_API1_KEY=your_api_key_3_here
GEMINI_FALLBACK_API2_KEY=your_api_key_4_here

# API Endpoint (mặc định)
GEMINI_API_ENDPOINT=https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent
```

Hoặc sử dụng biến môi trường Windows:

```powershell
$env:GEMINI_PRIMARY_API1_KEY = "your_key_here"
```

## Chạy ứng dụng

```powershell
python main.py
```

## Sử dụng

### Workflow cơ bản

1. **Upload file SRT**: Click "Open SRT" → chọn file .srt tiếng Trung
2. **Cấu hình**: 
   - Chọn Gemini model (flash/lite variants)
   - Chunk size (số dòng mỗi request, mặc định 10)
   - Threads per API (mặc định 5)
   - Tone (conversational/formal/literal)
3. **Name Mapping**: Thêm mapping tên Hán-Việt nếu cần (ví dụ: 张伟 → Trương Vĩ)
4. **Start Translation**: Click nút "Start" → theo dõi progress bar
5. **Preview & Edit**: 
   - Xem kết quả trong bảng preview
   - Double-click để sửa thủ công
   - Right-click → "Re-translate" để dịch lại dòng cụ thể
6. **Export**: 
   - Click "Export SRT" khi hoàn tất
   - App sẽ cảnh báo nếu còn dòng chưa dịch

### Rules dịch (tự động áp dụng)

- ✅ Giữ nguyên timecodes và thứ tự
- ✅ Không gộp/tách lines
- ✅ Loại bỏ numbering thừa từ model
- ✅ Detect và báo lỗi nếu còn ký tự tiếng Trung
- ✅ Áp dụng name mapping consistently

## Build thành Executable

### Sử dụng PyInstaller

```powershell
# Cài PyInstaller
pip install pyinstaller

# Build single-file executable
pyinstaller build.spec

# Hoặc sử dụng script tự động
.\build.ps1
```

File `.exe` sẽ nằm trong thư mục `dist/`:
- `dist/SRT_Translator.exe` (single file, ~150MB)

### Tạo installer (optional)

Sử dụng Inno Setup (download từ https://jrsoftware.org/isinfo.php):

```powershell
iscc installer.iss
```

## Cấu trúc project

```
trs/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── build.spec             # PyInstaller config
├── build.ps1              # Build script
├── .env                   # API keys (KHÔNG commit!)
├── .gitignore
├── README.md
│
├── core/
│   ├── __init__.py
│   ├── parser.py          # SRT parsing & chunking
│   ├── translator.py      # Async dispatcher, fallback logic
│   ├── validator.py       # Response validation & sanitization
│   ├── config.py          # Config & API key management
│   └── project.py         # Project save/load
│
├── gui/
│   ├── __init__.py
│   ├── main_window.py     # Main GUI window
│   ├── settings_dialog.py # Settings dialog
│   ├── preview_table.py   # Preview & edit table
│   └── name_map_editor.py # Name mapping editor
│
├── tests/
│   ├── __init__.py
│   ├── test_parser.py     # Parser unit tests
│   ├── test_validator.py  # Validator tests
│   ├── test_translator.py # Translator/fallback tests
│   └── test_integration.py # End-to-end tests
│
└── resources/
    ├── icon.ico           # App icon
    └── sample.srt         # Sample SRT for testing
```

## Testing

### Chạy tất cả tests

```powershell
pytest tests/ -v
```

### Chạy tests cụ thể

```powershell
pytest tests/test_parser.py -v
pytest tests/test_validator.py::test_cjk_detection -v
```

### Coverage report

```powershell
pytest tests/ --cov=core --cov=gui --cov-report=html
```

## Troubleshooting

### Lỗi API Key không hợp lệ

Kiểm tra:
1. File `.env` có đúng format không?
2. API keys còn hiệu lực không?
3. Đã enable Gemini API trong Google Cloud Console chưa?

### Lỗi "Still contains Chinese characters"

- Model trả về kết quả không đầy đủ → fallback tự động chạy
- Nếu sau 3 lần retry vẫn lỗi → sửa thủ công hoặc thử model khác
- Kiểm tra chunk_size (giảm xuống nếu quá lớn)

### App chạy chậm

- Giảm threads per API (từ 5 xuống 3)
- Giảm chunk size (từ 10 xuống 5)
- Kiểm tra network connection
- Một số API có rate limit → app tự động throttle

### Export bị block

App chỉ cho export khi:
- Tất cả dòng đã dịch HOẶC
- User xác nhận "Export anyway with unresolved lines"

Kiểm tra status column trong preview table để tìm dòng chưa hoàn tất.

## Security Best Practices

1. **Không commit API keys**: Luôn dùng `.env` hoặc environment variables
2. **Rotate keys định kỳ**: Đặc biệt khi share project
3. **Giới hạn permissions**: Chỉ cấp quyền cần thiết cho API keys
4. **Monitor usage**: Theo dõi API usage để phát hiện abuse

## Known Limitations

- Model đôi khi thêm numbering → app tự động xóa
- Gemini API có rate limit → app tự động throttle nhưng vẫn có thể chậm
- File SRT format phải chuẩn (index, timecode, content, blank line)
- Không hỗ trợ SSA/ASS format (chỉ SRT)

## Roadmap

- [ ] Hỗ trợ batch processing nhiều files
- [ ] Thêm translation memory (cache translations)
- [ ] Export sang formats khác (ASS, VTT)
- [ ] Hỗ trợ thêm ngôn ngữ (Nhật, Hàn)
- [ ] Cloud sync projects
- [ ] Undo/Redo cho manual edits

## License

MIT License - Tự do sử dụng, chỉnh sửa và phân phối.

## Contributing

Mọi đóng góp đều được hoan nghênh! Vui lòng:
1. Fork repo
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## Support

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra phần Troubleshooting trước
2. Xem logs trong tab "Logs" của app
3. Mở issue trên GitHub với đầy đủ thông tin (logs, steps to reproduce)

---

**Lưu ý**: App này sử dụng Gemini API - hãy đảm bảo tuân thủ Terms of Service của Google khi sử dụng.
