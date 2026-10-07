# 🀄 HSK Flashcards & Reading Analysis (HSK 1–9)

Ứng dụng web Single Page Application (SPA) mã nguồn mở, hoạt động **100% Offline (PWA)**, không cần bước build hay cài đặt package, chuyên sâu cho người Việt học và ôn luyện từ vựng tiếng Trung, ngữ pháp, luyện viết chữ Hán và đọc hiểu HSK chuẩn Hanban.

🔗 **Trải nghiệm trực tuyến ngay:** [https://nguyenhau442001.github.io/HSK-Flashcards-Generator/](https://nguyenhau442001.github.io/HSK-Flashcards-Generator/)

---

## 🌟 Điểm nổi bật & Tính năng chính

### 1. 🧠 Thuật toán Lặp lại ngắt quãng hiện đại (FSRS v5)
- Tích hợp chuẩn **FSRS (Free Spaced Repetition Scheduler)** v5 tối tân (vượt trội hơn hẳn so với thuật toán SuperMemo SM-2 truyền thống).
- 4 nút đánh giá chuẩn khoa học: **Lại (Again)**, **Khó (Hard)**, **Tốt (Good)**, **Dễ (Easy)** đi kèm nhãn dự đoán thời gian lặp lại trực quan (vd: `10m`, `1d`, `4d`, `12d`...).
- **Đường cong trí nhớ (SRS Memory Curve):** Biểu đồ mô phỏng độ suy giảm trí nhớ Ebbinghaus và độ ổn định từ vựng theo thời gian thực.
- Tự do tùy chỉnh **Mục tiêu ghi nhớ (Desired Retention)** từ 80% đến 95%.

### 2. 📚 Dữ liệu từ vựng toàn diện (HSK 2.0, HSK 3.0 & Bộ thủ)
- **HSK 2.0 (Cấp 1–6):** Đầy đủ 5.000 từ vựng cốt lõi chuẩn đề thi truyền thống.
- **HSK 3.0 mới (Cấp 1–9):** Hơn 11.000 từ vựng phân loại theo 3 bậc 9 cấp (Sơ cấp 1–3, Trung cấp 4–6, Cao cấp 7–9) theo khung khảo thí quốc tế mới nhất.
- **Bộ thủ chữ Hán (Radicals):** 50 bộ thủ cơ bản thường dùng và trọn bộ 214 bộ thủ Khang Hy theo số nét, có thống kê tiến độ riêng.
- **Từ vựng theo chủ đề:** Công nghệ thông tin (IT), Du lịch, Kinh doanh, Đời sống...

### 3. 📖 Đọc hiểu & Phân tích ngữ pháp HSK 4 (Chuẩn Hanban)
- Phân tích cú pháp chuyên sâu từng câu: Chủ ngữ (S), Vị ngữ (V), Tân ngữ (O), Trạng ngữ, Định ngữ, Bổ ngữ và các cặp liên từ logic.
- Phân tích từ vựng ngữ cảnh: Chữ Hán, Pinyin, Âm Hán - Việt, Từ loại và Nghĩa ngữ cảnh chính xác.
- Bộ lọc dạng bài thi: Sắp xếp câu (Hoàn thành câu), Chọn từ vào chỗ trống, Sắp xếp thứ tự đoạn văn, Đọc hiểu văn bản.
- **Zen Mode (Chế độ tập trung):** Tối đa hóa không gian đọc hiểu, ẩn thanh công cụ thừa, cho phép tùy chỉnh cỡ chữ và bật/tắt pinyin linh hoạt.

### 4. ✍️ Luyện viết chữ Hán tương tác (Hanzi Writer & Canvas)
- Trực quan hóa thứ tự từng nét viết (Stroke Order) chuẩn quy tắc bút thuận bằng animation qua thư viện `hanzi-writer`.
- **Canvas tập viết:** Tự do luyện viết trực tiếp bằng chuột hoặc màn hình cảm ứng, có hỗ trợ chấm nét, hiển thị nét mờ và tự động xóa vẽ lại.
- **Hỗ trợ từ ghép (Multichar Grid):** Chuyển đổi nhanh để xem và luyện viết từng chữ đơn lẻ bên trong một từ vựng ghép.

### 5. 漢 Tra cứu & Hiển thị Âm Hán - Việt tự động
- Tự động liên kết và hiển thị âm Hán - Việt cho toàn bộ từ vựng và câu văn, hỗ trợ người Việt học nghĩa gốc sâu sắc và ghi nhớ nhanh gấp đôi.
- Phím tắt tiện lợi `H` để bật/tắt nhanh âm Hán - Việt trên giao diện học.

### 6. 🎮 Phòng thực hành & Trò chơi củng cố phản xạ
- **Xếp câu (Sentence Game):** Rèn luyện tư duy ngữ pháp qua thao tác sắp xếp các khối từ thành câu hoàn chỉnh.
- **Đoán từ (Guess Word Game):** Đoán chữ Hán qua gợi ý nghĩa và pinyin.
- **Speed Quiz:** Trắc nghiệm tốc độ chọn nghĩa phản xạ nhanh trong thời gian giới hạn.
- **Ôn tập nhanh (Fast Review) & Ôn tập lỗi sai:** Lọc riêng các từ hay quên / từ yếu (Weak Words) để luyện tập tập trung.

### 7. 📱 Trải nghiệm người dùng (UX) hiện đại & PWA
- **SPA Router (History API):** Hỗ trợ nút Back/Forward trên trình duyệt mượt mà mà không tải lại trang; hỗ trợ deep linking chia sẻ trực tiếp liên kết bài học (vd: `?level=hsk4`, `?mode=reading`...).
- **Cài đặt như App (PWA):** Tương thích hoàn hảo trên iPhone, iPad, Android, macOS và Windows; mở lên học ngay lập tức không cần mạng.
- **Giao diện Hero Flashcard & Dark/Light Mode:** Thiết kế gọn gàng, độ tương phản cao, chuyển đổi ban ngày/ban đêm tự động theo giờ hoặc thủ công (`🌙/☀️`).
- **Phát âm chuẩn bản xứ:** Tích hợp audio giọng thật MP3 dựng sẵn và Web Speech API tự nhiên, tùy chỉnh tốc độ từ 0.25x đến 2x.

---

## ⌨️ Phím tắt bàn phím (Desktop Shortcuts)

Khi đang học flashcard trên máy tính, bạn có thể điều khiển hoàn toàn bằng bàn phím:

| Phím | Chức năng |
| :---: | :--- |
| `Space` hoặc `Enter` | Lật thẻ để xem mặt sau (nghĩa, ví dụ, phân tích) |
| `1` | Đánh giá **Lại (Again)** - Chưa nhớ |
| `2` | Đánh giá **Khó (Hard)** - Nhớ mang máng |
| `3` | Đánh giá **Tốt (Good)** - Nhớ chuẩn |
| `4` | Đánh giá **Dễ (Easy)** - Rất dễ dàng |
| `←` / `→` | Chuyển sang từ trước / từ tiếp theo |
| `R` | Ngẫu nhiên nhảy đến một từ bất kỳ |
| `H` | Bật / Tắt hiển thị âm Hán - Việt |
| `W` | Mở / Đóng bảng luyện viết chữ Hán |
| `B` | Mở / Đóng ngăn kéo danh sách từ vựng |

---

## 💻 Hướng dẫn chạy cục bộ (Local Development)

Vì ứng dụng được xây dựng hoàn toàn bằng **Vanilla HTML, CSS, JavaScript thuần**, bạn **không cần cài Node.js, npm, webpack hay vite**:

1. Clone kho lưu trữ về máy:
   ```bash
   git clone https://github.com/nguyenhau442001/HSK-Flashcards-Generator.git
   cd HSK-Flashcards-Generator
   ```

2. Khởi chạy một máy chủ HTTP tĩnh:
   ```bash
   # Dùng Python 3 (khuyên dùng)
   python3 -m http.server 8000
   
   # Hoặc dùng npx
   npx serve .
   ```

3. Mở trình duyệt và truy cập:
   ```
   http://localhost:8000/
   ```

*(Lưu ý: Không nên mở trực tiếp file `index.html` bằng giao thức `file://` vì trình duyệt sẽ chặn nạp các file JSON do chính sách bảo mật CORS).*

---

## 📂 Cấu trúc thư mục dự án

```text
HSK-Flashcards-Generator/
├── index.html                   # Trang chủ ứng dụng chính (SPA)
├── flashcards.html              # Trang ứng dụng đồng bộ 100% với index.html
├── sw.js                        # Service Worker quản lý offline cache (PWA)
├── config/
│   └── pwa-manifest.json        # Cấu hình PWA cài đặt ứng dụng
├── assets/
│   ├── flashcards.css           # File tổng hợp CSS chính
│   ├── flashcards.js            # Khởi tạo và liên kết các module
│   ├── css/                     # Các module stylesheet riêng biệt
│   │   ├── base.css             # Biến màu sắc, Typography, Dark/Light mode
│   │   ├── flashcard.css        # Khung thẻ Hero Flashcard, nút bấm SRS FSRS
│   │   ├── reading-analysis.css # Giao diện Đọc hiểu & Phân tích ngữ pháp HSK 4
│   │   ├── workstation.css      # Bố cục giao diện Workstation & Drawer trượt
│   │   ├── radicals.css         # Thẻ và lưới 214 bộ thủ Khang Hy
│   │   ├── sentence-game.css    # Mini-game xếp câu
│   │   └── ...
│   └── js/                      # Các module JavaScript nghiệp vụ
│       ├── spa-router.js        # Điều hướng SPA qua History API & deep linking
│       ├── srs.js               # Thuật toán lặp lại ngắt quãng FSRS v5
│       ├── storage.js           # Quản lý LocalStorage & an toàn dữ liệu
│       ├── reading-analysis.js  # Nghiệp vụ Đọc hiểu & Phân tích ngữ pháp HSK 4
│       ├── hanviet-dict.js      # Từ điển tra cứu Hán - Việt tự động
│       ├── stroke-canvas.js     # Bảng vẽ canvas luyện viết chữ Hán
│       ├── card-interactions.js # Thao tác lật thẻ, chạm vuốt di động
│       ├── levels.js / hsk30.js # Danh mục cấp độ HSK 2.0 & 3.0
│       └── ...
└── database/                    # Dữ liệu tĩnh JSON
    ├── vocabs/                  # HSK 1–6, HSK 3.0 (Cấp 1–9), Chủ đề
    ├── reading/                 # Dữ liệu phân tích đọc hiểu HSK 4
    ├── grammar/                 # Ngữ pháp mẫu & cấu trúc câu
    ├── radicals/                # 50 bộ thủ cơ bản & 214 bộ thủ Khang Hy
    └── prebuilt_audio/          # Audio giọng người thật chất lượng cao
```

---

## 🔒 Tiến trình học tập & Bảo mật dữ liệu

- **Không cần tài khoản:** Toàn bộ tiến trình học tập được lưu tự động và an toàn trong `localStorage` trên chính thiết bị của bạn.
- **Sao lưu & Chuyển thiết bị:** 
  - Vào phần **Sao lưu và chuyển thiết bị** $\rightarrow$ Bấm **💾 Tải bản sao tiến trình** để xuất file JSON.
  - Sang thiết bị mới $\rightarrow$ Bấm **📂 Khôi phục từ bản sao** để tiếp tục học ngay lập tức mà không mất chuỗi ngày học!

---

## 🤝 Đóng góp & Phát triển

Mọi ý kiến đóng góp, báo cáo lỗi từ vựng hoặc đề xuất tính năng mới đều được hoan nghênh nồng nhiệt qua [GitHub Issues](https://github.com/nguyenhau442001/HSK-Flashcards-Generator/issues) hoặc Pull Requests.

- **Tác giả:** [Nguyễn Ngọc Hậu (haunguyenngoc442001)](https://github.com/nguyenhau442001)
- **Giấy phép:** Open Source - MIT License.
