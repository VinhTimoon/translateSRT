# 🇻🇳 Hướng dẫn Chi tiết - Tiếng Việt

## Giới thiệu

**SRT Translator** là ứng dụng desktop dịch phụ đề SRT từ tiếng Trung sang tiếng Việt, sử dụng Gemini API với khả năng:
- Dịch song song 10 luồng
- Tự động retry khi lỗi
- Kiểm tra chất lượng tự động
- Giao diện đồ họa thân thiện

## Yêu cầu hệ thống

- **Hệ điều hành**: Windows 10/11
- **Python**: Phiên bản 3.10 trở lên
- **RAM**: Tối thiểu 4GB
- **Internet**: Cần kết nối để gọi API
- **Dung lượng**: ~500MB (bao gồm Python + dependencies)

## Hướng dẫn cài đặt từng bước

### Bước 1: Kiểm tra Python

Mở PowerShell và gõ:
```powershell
python --version
```

Nếu hiện `Python 3.10.x` hoặc cao hơn → OK!

Nếu chưa có Python:
1. Tải từ: https://www.python.org/downloads/
2. Chạy installer
3. **✅ QUAN TRỌNG**: Tích vào "Add Python to PATH"
4. Click "Install Now"

### Bước 2: Tải project

Nếu có Git:
```powershell
git clone <repository-url>
cd trs
```

Hoặc download ZIP và giải nén vào `e:\MyProj\trs`

### Bước 3: Chạy script setup tự động

Mở PowerShell **tại thư mục project**:
```powershell
cd e:\MyProj\trs
.\setup.ps1
```

Script sẽ tự động:
- ✅ Kiểm tra Python
- ✅ Tạo virtual environment
- ✅ Cài đặt tất cả dependencies
- ✅ Tạo file .env
- ✅ Tạo thư mục config

**Chờ 2-3 phút cho quá trình cài đặt hoàn tất.**

### Bước 4: Lấy API keys

1. Mở trình duyệt, vào: https://makersuite.google.com/app/apikey
2. Đăng nhập bằng Google account
3. Click "**Create API Key**"
4. Chọn project (hoặc tạo mới)
5. Copy API key (dạng: `AIzaSy...`)

💡 **Tip**: Có thể tạo nhiều keys để tăng tốc độ

### Bước 5: Cấu hình API keys

Mở file `.env` (đã tạo tự động):
```powershell
notepad .env
```

Điền các keys của bạn:
```env
# API chính (2 keys này chạy song song)
GEMINI_PRIMARY_API1_KEY=AIzaSyABC123...your_key_1
GEMINI_PRIMARY_API2_KEY=AIzaSyDEF456...your_key_2

# API dự phòng (khi API chính fail)
GEMINI_FALLBACK_API1_KEY=AIzaSyGHI789...your_key_3
GEMINI_FALLBACK_API2_KEY=AIzaSyJKL012...your_key_4
```

💡 **Có thể dùng cùng 1 key cho cả 4 nếu chỉ test**:
```env
GEMINI_PRIMARY_API1_KEY=AIzaSy...mykey
GEMINI_PRIMARY_API2_KEY=AIzaSy...mykey
GEMINI_FALLBACK_API1_KEY=AIzaSy...mykey
GEMINI_FALLBACK_API2_KEY=AIzaSy...mykey
```

Lưu file (Ctrl+S) và đóng Notepad.

### Bước 6: Chạy ứng dụng

```powershell
python main.py
```

Cửa sổ ứng dụng sẽ mở ra!

## Hướng dẫn sử dụng chi tiết

### A. Upload file SRT

1. Click nút **📁 Open SRT**
2. Chọn file `.srt` tiếng Trung của bạn
3. Đợi app parse file (1-2 giây)
4. Thông tin file hiện ở panel bên trái

**File info hiển thị**:
- Tên file
- Số dòng subtitle
- Model đang dùng
- Chunk size
- Tone

### B. Cấu hình settings (Optional)

**Model** (dropdown):
- `gemini-2.5-flash` ⭐ - Khuyên dùng: nhanh + chính xác
- `gemini-2.5-flash-lite` - Rất nhanh nhưng ít chính xác hơn
- `gemini-2.0-flash` - Cân bằng
- `gemini-2.0-flash-lite` - Nhanh nhất

**Chunk Size** (số dòng/lần gửi):
- `5` - Nhỏ: chậm nhưng ổn định
- `10` ⭐ - Mặc định: cân bằng
- `20` - Lớn: nhanh nhưng dễ lỗi

**Threads/API** (số luồng song song):
- `3` - Ít: chậm nhưng ít vượt quota
- `5` ⭐ - Mặc định: vừa phải
- `8` - Nhiều: nhanh nhưng dễ vượt quota

**Tone** (phong cách dịch):
- `conversational` ⭐ - Tự nhiên, khẩu ngữ (phim ảnh)
- `formal` - Lịch sự, trang trọng (phim tài liệu)
- `literal` - Sát nghĩa gốc

### C. Bắt đầu dịch

1. Click nút **▶ Start Translation** (màu xanh)
2. Thanh progress bar sẽ chạy
3. Logs hiển thị tiến trình real-time
4. Có thể click **⏹ Stop** để dừng giữa chừng

**Trong quá trình dịch**:
- Progress bar: % hoàn thành
- Status: Chunk nào đang dịch
- Logs: Chi tiết từng chunk (thành công/thất bại)

**Thời gian dự kiến**:
- 100 dòng: ~30-60 giây
- 500 dòng: ~2-5 phút
- 1000 dòng: ~5-10 phút

### D. Xem preview và sửa

Khi dịch xong, bảng preview hiển thị:

| Index | Time | Original (Chinese) | Translated (Vietnamese) | Status |
|-------|------|-------------------|------------------------|--------|
| 1 | 00:00:01 | 加班猝死 | Làm thêm giờ đến chết | done ✅ |
| 2 | 00:00:03 | 我串到了... | Tôi xuyên vào... | done ✅ |

**Màu sắc status**:
- 🟢 **Xanh lá** (done) - Dịch thành công
- 🔴 **Đỏ** (failed) - Dịch thất bại
- 🟡 **Vàng** (in-progress) - Đang dịch

**Sửa thủ công**:
1. **Double-click** vào ô Translated
2. Sửa nội dung
3. Enter để lưu

**Re-translate 1 dòng** (coming soon):
1. **Right-click** vào dòng
2. Chọn "Re-translate This Line"

### E. Name Mapping (đồng nhất tên)

Nếu muốn tên nhân vật nhất quán (VD: 张伟 luôn là "Trương Vĩ"):

1. Click **Edit Name Mapping**
2. Hoặc mở file: `C:\Users\<YourName>\.srt_translator\name_map.json`
3. Thêm mapping:

```json
{
  "张伟": "Trương Vĩ",
  "李芳": "Lý Phương",
  "王小明": "Vương Tiểu Minh"
}
```

4. Lưu file
5. Khởi động lại app
6. Dịch lại → Tên sẽ thống nhất

### F. Lưu project (để resume sau)

Nếu file lớn và muốn dịch từng đợt:

1. Dịch một phần
2. Click **💾 Save Project**
3. Chọn nơi lưu file `.json`
4. Thoát app

**Để tiếp tục sau**:
1. Mở lại app
2. Click **📂 Load Project**
3. Chọn file `.json` đã lưu
4. Tiếp tục dịch từ chỗ dừng

### G. Export file SRT

Khi tất cả dòng đã dịch xong:

1. Click **📤 Export SRT** (nút xanh dương)
2. Chọn nơi lưu file output
3. Nhập tên file (VD: `output_vietnamese.srt`)
4. Click Save

**App sẽ kiểm tra**:
- ✅ Tất cả dòng đã dịch?
- ✅ Không còn chữ Hán?

Nếu vẫn còn dòng chưa dịch:
- ⚠️ App sẽ cảnh báo
- Có thể chọn "Export anyway" để export luôn
- Hoặc Cancel để sửa các dòng còn thiếu

## Xử lý lỗi thường gặp

### 1. "Configuration Error: No API keys"

**Nguyên nhân**: Chưa cấu hình `.env` hoặc key không hợp lệ

**Cách sửa**:
```powershell
# Kiểm tra file .env có tồn tại không
dir .env

# Nếu không có, tạo từ template
copy .env.example .env

# Mở và chỉnh sửa
notepad .env
```

Đảm bảo:
- Key không có dấu cách đầu/cuối
- Key bắt đầu bằng `AIzaSy`
- Không có dấu ngoặc kép

### 2. "Still contains Chinese characters"

**Nguyên nhân**: Model trả kết quả chưa đầy đủ

**App tự động**: Retry với fallback APIs (tối đa 3 lần)

**Nếu vẫn lỗi**:
1. Giảm chunk size: 10 → 5
2. Thử model khác: flash → lite
3. Kiểm tra internet
4. Sửa thủ công dòng bị lỗi

### 3. App chạy rất chậm

**Nguyên nhân**: Internet chậm hoặc API bận

**Cách khắc phục**:
- Giảm threads: 5 → 3
- Giảm chunk size: 10 → 5
- Kiểm tra tốc độ mạng
- Thử vào giờ khác

### 4. "Quota exceeded" / "Rate limit"

**Nguyên nhân**: Vượt giới hạn API (free tier: 60 req/phút)

**Cách khắc phục**:
- Đợi 1 phút rồi thử lại
- Dùng nhiều API keys khác nhau
- Giảm threads để chậm lại
- Upgrade lên paid tier

### 5. Export bị chặn

**Nguyên nhân**: Còn dòng chưa dịch hoặc vẫn còn chữ Hán

**Cách kiểm tra**:
- Xem cột Status trong bảng
- Tìm dòng màu đỏ (failed) hoặc vàng (in-progress)
- Scroll xuống xem có dòng nào còn tiếng Trung

**Cách sửa**:
1. Sửa thủ công các dòng lỗi
2. Hoặc re-translate các dòng đó
3. Hoặc force export bằng "Export anyway"

### 6. App không mở được

**Kiểm tra**:
```powershell
# Virtual environment đã activate?
.\venv\Scripts\Activate.ps1

# Dependencies đã cài?
pip list | Select-String "PySide6"

# Nếu chưa có, cài lại
pip install -r requirements.txt
```

### 7. Import errors khi chạy

```
ModuleNotFoundError: No module named 'PySide6'
```

**Cách sửa**:
```powershell
# Đảm bảo virtual env đã activate
.\venv\Scripts\Activate.ps1

# Cài lại dependencies
pip install -r requirements.txt --upgrade
```

## Tips & Tricks nâng cao

### 1. Dùng nhiều API keys để tăng tốc

Nếu có 4 keys khác nhau:
```env
PRIMARY_API1 = key_1  # Key riêng
PRIMARY_API2 = key_2  # Key riêng
FALLBACK_API1 = key_3 # Key riêng
FALLBACK_API2 = key_4 # Key riêng
```

→ Tốc độ gấp 2-3 lần so với dùng 1 key

### 2. Test với file nhỏ trước

```powershell
# Copy sample file ra
copy resources\sample.srt test_input.srt

# Dịch thử 10 dòng này trước
# Nếu OK → dịch file lớn
```

### 3. Batch processing nhiều files (manual)

```powershell
# Dịch file 1
python main.py  # Load file1.srt, dịch, export

# Dịch file 2
python main.py  # Load file2.srt, dịch, export
```

### 4. Check logs để debug

Tab "Logs" hiển thị:
- `✓` - Thành công
- `✗` - Thất bại
- API nào được dùng
- Thời gian mỗi chunk
- Tổng thống kê cuối

Copy logs nếu cần hỗ trợ!

### 5. Keyboard shortcuts (trong preview table)

- **Double-click**: Edit translation
- **Right-click**: Context menu
- **Ctrl+C**: Copy (nếu select cell)
- **Scroll**: Xem toàn bộ

### 6. Save project thường xuyên

Đối với file >500 dòng:
- Dịch 100-200 dòng → Save project
- Nếu crash → Load lại và tiếp tục
- Không mất công dịch lại từ đầu

## Build thành file .exe

Nếu muốn chạy trên máy khác không có Python:

```powershell
# 1. Cài PyInstaller
pip install pyinstaller

# 2. Chạy build script
.\build.ps1

# 3. File output: dist\SRT_Translator.exe
```

**Lưu ý quan trọng**:
- File .exe cần file `.env` trong cùng folder!
- Copy cả 2 files:
  - `SRT_Translator.exe`
  - `.env` (với API keys của bạn)

**Chia sẻ cho người khác**:
- Đừng share file `.env` (có API keys)
- Chỉ share `.exe` + hướng dẫn tạo `.env`

## Tài liệu tham khảo

- **QUICK_START.md** - Hướng dẫn nhanh (tiếng Anh)
- **README.md** - Tài liệu đầy đủ
- **API_SETUP.md** - Chi tiết về API
- **PROMPTS.md** - Giải thích cách dịch
- **PROJECT_SUMMARY.md** - Tổng quan kỹ thuật

## Hỗ trợ

Nếu gặp vấn đề:

1. **Đọc phần "Xử lý lỗi" ở trên**
2. **Kiểm tra logs trong app**
3. **Test với file sample**: `resources/sample.srt`
4. **Kiểm tra API keys** hợp lệ không
5. **Thử giảm chunk size** xuống 5

## Checklist hoàn chỉnh

- [ ] Python 3.10+ đã cài
- [ ] Chạy `setup.ps1` thành công
- [ ] File `.env` đã tạo và điền keys
- [ ] Chạy `python main.py` mở được app
- [ ] Test với `resources/sample.srt` thành công
- [ ] Dịch file của bạn
- [ ] Preview xem kết quả
- [ ] Export file output
- [ ] Kiểm tra file output mở được trong media player

---

**Chúc bạn dịch phụ đề thành công! 🎬✨**

*Nếu có thắc mắc, đọc README.md hoặc các file docs khác.*
