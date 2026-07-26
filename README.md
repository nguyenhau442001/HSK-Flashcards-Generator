# HSK Flashcards

Ứng dụng flashcard tĩnh dành cho người Việt học từ vựng HSK. Mỗi thẻ gồm chữ Hán, pinyin, nghĩa tiếng Việt và câu ví dụ có phiên âm lẫn bản dịch.

Không cần cài package hay chạy bước build. Toàn bộ dữ liệu từ vựng nằm trong repository.

## Học trực tuyến

Mở ứng dụng tại:

https://nguyenhau442001.github.io/HSK-Flashcards-Generator/flashcards.html

## Cấp độ

| Cấp độ | Số từ | Trạng thái |
|--------|------:|------------|
| HSK1 | 150 | Có sẵn |
| HSK2 | 150 | Có sẵn |
| HSK3 | 300 | Có sẵn |
| HSK4 | 600 | Có sẵn |
| HSK5 | 1.300 | Có sẵn |
| HSK6 | 2.500 | Có sẵn |

Tổng cộng: **5.000 từ vựng**.

## Tính năng

- Chọn và học riêng từng cấp độ HSK1–HSK6.
- Hiển thị tiến độ đã nhớ của từng cấp độ ngay tại màn hình chọn.
- Chào người học bằng thông điệp vui theo thời gian, tiến độ và chuỗi ngày quay lại.
- Theo dõi tổng số từ, đã nhớ, chưa nhớ và chưa học.
- Lọc thẻ theo trạng thái: tất cả, chưa học, chưa nhớ hoặc đã nhớ.
- Nhấn vào thẻ để xem nghĩa, câu ví dụ và nút phát âm tiếng Trung.
- Vuốt sang phải để đánh dấu **Đã nhớ**, vuốt sang trái để đánh dấu **Chưa nhớ**.
- Chuyển thẻ bằng nút trước/sau, xáo trộn thứ tự học và ẩn/hiện pinyin để tự kiểm tra.
- Hiển thị danh sách có đánh số của các từ chưa nhớ.
- Phát âm bằng Web Speech API, ưu tiên giọng `zh-CN` khi trình duyệt cung cấp.
- Tự động lưu tiến trình, thứ tự thẻ và tùy chọn pinyin riêng cho từng cấp độ.
- Tải bản sao tiến trình dưới dạng JSON và khôi phục trên thiết bị khác.
- Học lại từ đầu với bước xác nhận trước khi xóa tiến trình của cấp độ hiện tại.
- Giao diện sáng/tối, bố cục responsive và hỗ trợ `prefers-reduced-motion`.
- Hiệu ứng chuyển thẻ, kéo thả và chúc mừng khi hoàn thành toàn bộ cấp độ.

## Chạy trên máy

Clone repository và khởi chạy bằng một static HTTP server:

```bash
git clone https://github.com/nguyenhau442001/HSK-Flashcards-Generator.git
cd HSK-Flashcards-Generator
python3 -m http.server 8000
```

Sau đó mở:

http://localhost:8000/flashcards.html

Các chức năng học cốt lõi không cần kết nối Internet sau khi source code và dữ liệu đã có trên máy. Nên dùng HTTP server thay vì mở trực tiếp `flashcards.html` bằng `file://`, vì một số trình duyệt chặn việc tải các tệp JSON cục bộ.

## Tiến trình và sao lưu

Tiến trình được lưu bằng `localStorage` của trình duyệt, vì vậy dữ liệu gắn với trình duyệt và thiết bị đang sử dụng.

Để chuyển thiết bị:

1. Chọn **Sao lưu** và tải bản sao tiến trình.
2. Mở đúng cấp độ trên thiết bị mới.
3. Chọn **Khôi phục từ bản sao** và chọn tệp JSON đã tải.

Danh sách **Từ chưa nhớ** chỉ được hiển thị trong ứng dụng; chức năng này không tạo tệp tải xuống.

## Cấu trúc dự án

```text
.
├── flashcards.html
├── assets/
│   ├── flashcards.css
│   └── flashcards.js
└── database/
    └── text/
        ├── hsk1_vocabularies.json
        ├── hsk2_vocabularies.json
        ├── hsk3_vocabularies.json
        ├── hsk4_vocabularies.json
        ├── hsk5_vocabularies.json
        └── hsk6_vocabularies.json
```

## Lưu ý về phát âm

Khả năng phát âm phụ thuộc vào Web Speech API và các giọng đọc được cài trên thiết bị. Chrome và Safari được khuyến nghị nếu nút phát âm không hoạt động trên trình duyệt hiện tại.

## Lỗi đã biết

- **Không nghe được phát âm khi mở liên kết từ Facebook trên Android:** trình duyệt tích hợp của Facebook có thể không hỗ trợ phát âm qua Web Speech API. Hãy mở menu của trang, chọn mở bằng trình duyệt bên ngoài và tiếp tục học bằng Google Chrome.

## Đóng góp

Issue và đề xuất cải tiến đều được chào đón trên GitHub.
