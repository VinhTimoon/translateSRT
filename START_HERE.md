# ⭐ START HERE - BẮT ĐẦU TẠI ĐÂY

## 👋 Chào mừng đến với SRT Translator!

Ứng dụng dịch phụ đề SRT từ **tiếng Trung** sang **tiếng Việt** sử dụng AI.

---

## 🎯 Bạn muốn làm gì?

### 1️⃣ Tôi muốn SỬ DỤNG app (End User)

**Người Việt 🇻🇳:**
→ Đọc file: **[HUONG_DAN_TIENG_VIET.md](HUONG_DAN_TIENG_VIET.md)**
   - Hướng dẫn từng bước bằng tiếng Việt
   - Rất chi tiết, dễ hiểu
   - Có xử lý lỗi thường gặp

**English speakers:**
→ Read: **[QUICK_START.md](QUICK_START.md)**
   - 5-minute quick setup guide
   - Essential commands
   - Troubleshooting

### 2️⃣ Tôi muốn HIỂU CÁCH HOẠT ĐỘNG (Developer)

→ Read: **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)**
   - Architecture overview
   - Code structure
   - Technical details

### 3️⃣ Tôi muốn CUSTOM/MỞ RỘNG (Advanced)

→ Start with:
   1. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Architecture
   2. **[PROMPTS.md](PROMPTS.md)** - How translation works
   3. **[core/](core/)** folder - Source code

### 4️⃣ Tôi GẶP LỖI (Troubleshooting)

→ Check:
   1. **[QUICK_START.md](QUICK_START.md)** - Troubleshooting section
   2. **[HUONG_DAN_TIENG_VIET.md](HUONG_DAN_TIENG_VIET.md)** - Phần xử lý lỗi
   3. **[API_SETUP.md](API_SETUP.md)** - API problems

---

## ⚡ Super Quick Start (3 phút)

```powershell
# Bước 1: Chạy setup tự động
.\setup.ps1

# Bước 2: Lấy API key
# Mở: https://makersuite.google.com/app/apikey
# Copy key của bạn

# Bước 3: Điền API key
notepad .env
# Paste key vào file, Ctrl+S để lưu

# Bước 4: Chạy app
python main.py
```

**Done! 🎉**

---

## 📚 Tất cả tài liệu có sẵn

Xem **[INDEX.md](INDEX.md)** để có danh sách đầy đủ tất cả tài liệu.

---

## ✅ Checklist nhanh

- [ ] Python 3.10+ đã cài?
- [ ] Chạy `.\setup.ps1`
- [ ] Có API key từ Google?
- [ ] Đã điền vào file `.env`?
- [ ] Chạy `python main.py` thành công?
- [ ] Test với file sample?

Nếu tất cả ✅ → Bạn đã sẵn sàng dịch phụ đề! 🎬

---

## 🆘 Cần giúp đỡ ngay?

**Lỗi về API keys?**
→ Đọc **[API_SETUP.md](API_SETUP.md)**

**Lỗi khi chạy app?**
→ Đọc phần Troubleshooting trong **[QUICK_START.md](QUICK_START.md)**

**Không biết làm gì?**
→ Đọc **[HUONG_DAN_TIENG_VIET.md](HUONG_DAN_TIENG_VIET.md)** (tiếng Việt)

---

## 🎯 Mục tiêu của project này

Tạo một app **đơn giản, dễ dùng** để:
- ✅ Dịch phụ đề SRT Trung → Việt
- ✅ Tự động xử lý lỗi
- ✅ Giao diện đồ họa thân thiện
- ✅ Miễn phí (dùng Gemini API free tier)

---

## 📊 Thông số nhanh

- **Ngôn ngữ**: Chinese → Vietnamese
- **Format**: SRT (SubRip)
- **Engine**: Gemini AI
- **Speed**: ~30-60 giây cho 100 dòng
- **Accuracy**: ~95% với chunk size 10

---

## 💡 Tips nhanh

1. **Test với file nhỏ trước** (`resources/sample.srt`)
2. **Dùng nhiều API keys** để nhanh hơn
3. **Save project** nếu file >500 dòng
4. **Giảm chunk size** nếu gặp lỗi
5. **Đọc logs** để hiểu chuyện gì đang xảy ra

---

## 🎬 Let's Go!

**Chọn hướng dẫn phù hợp với bạn:**

| Bạn là | Đọc file này |
|--------|-------------|
| 🇻🇳 Người Việt muốn dùng | **[HUONG_DAN_TIENG_VIET.md](HUONG_DAN_TIENG_VIET.md)** |
| 🌍 English speaker | **[QUICK_START.md](QUICK_START.md)** |
| 👨‍💻 Developer | **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** |
| 🔧 Gặp lỗi | **[QUICK_START.md](QUICK_START.md)** Troubleshooting |
| 📚 Xem tất cả docs | **[INDEX.md](INDEX.md)** |

---

**Chúc bạn dịch phụ đề thành công! 🎉✨**

*Questions? Read the documentation files above. They're comprehensive!*
