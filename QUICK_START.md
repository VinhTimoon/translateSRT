# Quick Start Guide - Hướng dẫn nhanh

## 🚀 Cài đặt nhanh (5 phút)

### 1. Chuẩn bị

Yêu cầu:
- Windows 10/11
- Python 3.10+ đã cài
- Gemini API key (miễn phí tại https://makersuite.google.com/app/apikey)

### 2. Clone/Download project

```powershell
cd e:\MyProj\trs
```

### 3. Setup môi trường

```powershell
# Tạo virtual environment
python -m venv venv

# Kích hoạt
.\venv\Scripts\Activate.ps1

# Cài dependencies
pip install -r requirements.txt
```

### 4. Cấu hình API keys

```powershell
# Copy file mẫu
copy .env.example .env

# Mở và chỉnh sửa .env bằng notepad
notepad .env
```

Điền API keys của bạn:
```
GEMINI_PRIMARY_API1_KEY=AIzaSy...your_key_here
GEMINI_PRIMARY_API2_KEY=AIzaSy...your_key_here
GEMINI_FALLBACK_API1_KEY=AIzaSy...your_key_here
GEMINI_FALLBACK_API2_KEY=AIzaSy...your_key_here
```

💡 **Tip**: Có thể dùng cùng 1 key cho tất cả nếu chỉ test.

### 5. Chạy app

```powershell
python main.py
```

## 📖 Sử dụng cơ bản

### Workflow đơn giản:

1. **📁 Open SRT** → Chọn file .srt tiếng Trung
2. **⚙️ Settings** → Chọn model, chunk size, tone
3. **▶️ Start Translation** → Đợi progress bar chạy xong
4. **👁️ Preview** → Xem kết quả, sửa nếu cần
5. **📤 Export SRT** → Lưu file tiếng Việt

### Giải thích settings:

- **Model**: 
  - `gemini-2.5-flash` - Nhanh, chính xác (khuyên dùng)
  - `gemini-2.5-flash-lite` - Rất nhanh, ít chính xác
  - `gemini-2.0-flash` - Cân bằng
  - `gemini-2.0-flash-lite` - Nhanh nhất
  
- **Chunk Size**: Số dòng mỗi lần gửi (10 = tốt)
  - Nhỏ (5): Chậm nhưng ổn định
  - Vừa (10): Cân bằng
  - Lớn (20): Nhanh nhưng dễ lỗi

- **Threads/API**: Số luồng song song (5 = tốt)
  - Nhiều → Nhanh nhưng dễ vượt quota
  - Ít → Chậm nhưng ổn định

- **Tone**: Phong cách dịch
  - `conversational` - Tự nhiên, khẩu ngữ
  - `formal` - Lịch sự, trang trọng
  - `literal` - Sát nghĩa gốc

## 🔧 Xử lý lỗi thường gặp

### "Configuration Error: No API keys"
→ Chưa tạo file `.env` hoặc key không hợp lệ
→ Xem lại bước 4

### "Still contains Chinese characters"
→ Model trả kết quả chưa đầy đủ
→ App tự động retry, nếu vẫn lỗi → giảm chunk size

### App chạy chậm
→ Giảm threads từ 5 xuống 3
→ Giảm chunk size từ 10 xuống 5
→ Kiểm tra internet

### "Export blocked"
→ Còn dòng chưa dịch xong
→ Xem cột Status trong bảng Preview
→ Có thể force export bằng "Export anyway"

## 💾 Lưu/Load project

### Khi nào cần?
- File SRT quá lớn (>1000 dòng)
- Muốn dịch từng đợt
- Cần tắt app giữa chừng

### Cách dùng:
1. Dịch một phần
2. **💾 Save Project** → Lưu file .json
3. Thoát app
4. Mở lại app
5. **📂 Load Project** → Chọn file .json đã lưu
6. Tiếp tục dịch

## 🎯 Tips & Tricks

### 1. Name Mapping (đồng nhất tên)

Chỉnh file: `~/.srt_translator/name_map.json`

```json
{
  "张伟": "Trương Vĩ",
  "李芳": "Lý Phương",
  "王小明": "Vương Tiểu Minh"
}
```

App sẽ tự động thay tên nhất quán trong toàn bộ phụ đề.

### 2. Dùng nhiều API keys

Nếu có nhiều keys → performance tốt hơn:
```
PRIMARY_API1 = key1
PRIMARY_API2 = key2  # Key khác
FALLBACK_API1 = key3
FALLBACK_API2 = key4
```

### 3. Test với file nhỏ trước

Sample file: `resources/sample.srt` (10 dòng)
→ Test xem cấu hình có OK không

### 4. Sửa thủ công

Double-click vào ô Translated để sửa trực tiếp
Right-click → "Re-translate" để dịch lại 1 dòng

### 5. Monitor logs

Tab "Logs" hiển thị:
- Progress
- API nào được dùng
- Lỗi gì xảy ra
- Thống kê cuối

## 🏗️ Build thành .exe

```powershell
# Cài PyInstaller nếu chưa có
pip install pyinstaller

# Build
.\build.ps1

# File output: dist\SRT_Translator.exe
```

**Lưu ý**: File .exe cần file `.env` trong cùng thư mục!

## 📚 Tài liệu đầy đủ

- `README.md` - Tài liệu chính
- `API_SETUP.md` - Hướng dẫn API keys chi tiết
- `PROMPTS.md` - Giải thích prompts dịch
- `QUICK_START.md` - File này

## 🆘 Cần trợ giúp?

1. Đọc phần Troubleshooting trong README.md
2. Kiểm tra logs trong app
3. Test API key bằng curl (xem API_SETUP.md)

## ✅ Checklist hoàn chỉnh

- [ ] Python 3.10+ đã cài
- [ ] Clone project về máy
- [ ] Tạo virtual environment
- [ ] Cài requirements.txt
- [ ] Tạo file .env với API keys
- [ ] Chạy `python main.py`
- [ ] Test với sample.srt
- [ ] Dịch file SRT của bạn
- [ ] Export kết quả
- [ ] (Optional) Build .exe

---

**Chúc bạn dịch phụ đề vui vẻ! 🎬✨**
