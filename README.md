# Bộ giảng viên — Thực hành Julia 09/10/2026

Phát Bo_Thuc_hanh_Julia_2026_10_09_Sinh_vien.zip cho lớp. Gói hiện tại có lời
giải, đáp án và nguồn soạn; sử dụng làm tài liệu giảng viên.

## Tổ chức buổi học

Mở Thuc_hanh_CTDL_GT_Julia_2026_10_09.html, chọn Trình chiếu và cỡ chữ.
Khung đề xuất 180 phút; phương án 90/225 phút trong hướng dẫn giảng viên.
Có 14 trang nội dung và bốn minh họa với 74 bước: trộn, BFS, DP, giao/hoàn tác.
Các trang lý thuyết chi tiết có thể cuộn trong trình chiếu; dùng Trước/Tiếp
trong minh họa để điều khiển thuật toán. Esc trở về đọc toàn bài.

Một ứng dụng, cùng dữ liệu, bốn TODO trong một file. Danh sách/hàng đợi/ngăn xếp,
BST, DFS/đệ quy và vét cạn đã cung cấp để đọc và vận dụng; bảng cuối bài đối chiếu
bảy chương. Trong 180 phút tập trung mini ba đơn. Dữ liệu theo MSSV và trình bày
notebook/báo cáo hoàn thiện sau buổi học.

## Kiểm tra và trình diễn

```text
julia TH_2026_10_09_Loi_giai.jl --mini
julia TH_2026_10_09_Kiem_thu.jl --teacher --phase=all
```

Đã chạy trên Julia thực tế: lời giải đạt 60 kiểm tra
(data 12, sort 8, search 5, BFS 7, DP 12, app 16).
Khung sinh viên chỉ đạt pha data trước khi hoàn thiện bốn TODO.
BFS chấp nhận các đường ít cạnh nhất hợp lệ, không ép tuyến theo đúng animation.
Bộ mini: chi phí theo ID 1/2/3 là 3/5/7; B=8, chọn 1+2, tổng lợi ích 14.
Sau giao đơn 1: thời gian 3/lợi ích 6; hoàn tác trở về 0/0, hàng đợi [1,2];
giao hết: 8/14. CSV kết quả chín cột được xuất từ trạng thái Session.

Notebook mặc định để hai cờ false, không tự chạy ứng dụng. Sau khi hoàn thiện
code/dữ liệu, bật READ_DATA/RUN_APP; mẫu gọi cùng lõi và hiển thị/in truy vết.
Không có Pluto vẫn chạy trực tiếp tệp notebook .jl bằng Julia.

Chấm theo minh chứng trong phiếu, báo cáo, kiểm thử và GitHub. Dùng đáp án quiz,
bảng DP, phản ví dụ tham lam và đổi bản đồ trong hướng dẫn giảng viên để trao đổi.

## Nguồn tái tạo tài liệu

Thư mục _mon_hoc/Thuc_hanh_2026_10_09 chứa nguồn JSON nội dung/đáp án/khung hình,
code Julia, CSS/JS, hình sơ đồ, script tạo tài liệu, kiểm tra và đóng gói.
Giữ nguyên bố cục này để đường dẫn ROOT trong script trỏ đúng thư mục gói.

```text
python _mon_hoc/Thuc_hanh_2026_10_09/build_lab.py
node _mon_hoc/Thuc_hanh_2026_10_09/audit_render.cjs
python _mon_hoc/Thuc_hanh_2026_10_09/audit_files.py
python _mon_hoc/Thuc_hanh_2026_10_09/package_lab.py
```

Python cần python-docx, pdfplumber; render cần Playwright và trình duyệt Chromium
hoặc Edge. Sửa đường dẫn require Playwright trong audit_render.cjs cho máy mới.
build_lab.py tạo HTML/DOCX/Markdown và hai bản HTML dùng xuất PDF; audit_render
tạo ba PDF cùng hình QA; audit_files kiểm tra trang/kiểu chữ và tính đầy đủ.
PNG roadmap đã kèm để Word có hình ngay từ lần build đầu. PDF là bản xuất HTML,
DOCX là bản chỉnh sửa được; bố cục phân trang có thể khác nhau.

Đã xác minh 1.115 điều kiện của khung minh họa, bốn trạng thái cuối so với Julia,
74 bước, không có lỗi JavaScript, hiển thị ở 390/900/1366px, không gọi mạng để
tải tài nguyên. Kiểm tra tích hợp có tải .jl đúng byte, phím trình chiếu, in và
khôi phục chế độ trình chiếu. Ba PDF không có trang trắng hay chữ vượt khổ giấy.
Thư mục qa có báo cáo kiểm tra. Archive được kiểm CRC, byte và liên kết cục bộ.

## Các skill đã áp dụng

Tên và nguồn trên máy soạn:
- Soạn bài: C:/Users/DELL/.codex/skills/soan-bai-giang-giao-trinh-3-buoi/SKILL.md
  (điều chỉnh thành một buổi theo yêu cầu).
- Viết: C:/Users/DELL/.codex/skills/agency-technical-writer/SKILL.md.
- Code và tương tác: C:/Users/DELL/.codex/skills/agency-frontend-developer/SKILL.md.
- Hình và animation: C:/Users/DELL/.codex/skills/agency-visual-storyteller/SKILL.md.
- Tài liệu: C:/Users/DELL/.codex/skills/agency-document-generator/SKILL.md.
- Rà soát code: C:/Users/DELL/.codex/skills/agency-code-reviewer/SKILL.md.

Animation dùng SVG/HTML/CSS/JavaScript để mô tả chính xác trạng thái thuật toán;
chương trình bài tập và notebook đều viết bằng Julia.
