"""Đóng gói bài thực hành; chạy sau build_lab.py và audit_render.cjs."""
from pathlib import Path, PurePosixPath
from zipfile import ZipFile, ZIP_DEFLATED
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
BASE = 'Thuc_hanh_CTDL_GT_Julia_2026_10_09'
STUDENT_ZIP = 'Bo_Thuc_hanh_Julia_2026_10_09_Sinh_vien.zip'
TEACHER_ZIP = 'Bo_Thuc_hanh_Julia_2026_10_09_Giang_vien.zip'

STUDENT_README = '''# Thực hành Cấu trúc dữ liệu và giải thuật — 09/10/2026

Một ứng dụng Julia: điều phối giao đơn trong khuôn viên trường.
Khung trên lớp: 180 phút. Trình bày theo notebook Julia/Pluto mẫu sau buổi học.

## 1. Mở bài học

Giải nén toàn bộ gói, giữ thư mục data. Mở Thuc_hanh_CTDL_GT_Julia_2026_10_09.html
bằng trình duyệt. Bấm Trình chiếu; dùng phím mũi tên để chuyển trang, Esc để trở về
chế độ đọc. Trong khung minh họa, chọn thuật toán rồi dùng Trước/Tiếp/Tự chạy để
xem từng bước. Có nút đổi cỡ chữ và bản PDF/Word để đọc, in.

Yêu cầu: Julia chạy được trong terminal. Mã lõi chỉ dùng Base, không cần cài gói
CSV. Có thể dùng VS Code hoặc trình soạn thảo khác để sửa tệp .jl.

## 2. Tạo và đọc hai CSV trước khi viết thuật toán

Mở terminal ở thư mục giải nén và chạy:

```text
julia TH_2026_10_09_Sinh_vien.jl --data
julia TH_2026_10_09_Kiem_thu.jl --phase=data
```

Lệnh đầu tạo hoặc đọc lại data/MINI001/don_hang.csv và ban_do.csv.
Hai tệp mẫu đã kèm trong gói. Lệnh thứ hai phải đạt 12 kiểm tra dữ liệu dù bốn
hàm còn trống. Nếu Julia chưa có trong PATH, dùng đường dẫn đầy đủ tới julia.exe.
Trong Julia REPL, đọc cùng dữ liệu bằng:

```julia
include("TH_2026_10_09_Sinh_vien.jl")
data_dir = GiaoDon.mini_data()
data = GiaoDon.read_data(data_dir)
data.orders
data.edges
```

Mở các hàm write_data, integer_csv, read_data trong file chung để xem cách
open/println tạo tệp, readlines/split/parse đọc số và kiểm tra dữ liệu. CSV này chỉ
có số nguyên và tiêu đề cố định; không dùng bộ đọc đơn giản này cho CSV có ô chứa
dấu phẩy hoặc xuống dòng. Không tự điền CSV kết quả để thay cho chạy ứng dụng.

## 3. Hoàn thiện bốn hàm theo thứ tự

Chỉ sửa bốn vị trí TODO trong TH_2026_10_09_Sinh_vien.jl.
Các bài cùng dùng một danh mục đơn, một bản đồ và một bộ điều phối.

| Nhiệm vụ | Hàm | Lệnh kiểm tra |
|---|---|---|
| NV1: sắp xếp trộn | merge_sort(a, before) | julia TH_2026_10_09_Kiem_thu.jl --phase=sort |
| NV2: tìm kiếm nhị phân | binary_search(a, id) | julia TH_2026_10_09_Kiem_thu.jl --phase=search |
| NV3: đường ít cạnh nhất | bfs_routes(graph, source=1) | julia TH_2026_10_09_Kiem_thu.jl --phase=bfs |
| NV4: chọn đơn trong ngân sách | knapsack(orders, costs, budget) | julia TH_2026_10_09_Kiem_thu.jl --phase=dp |

Đọc điều kiện đầu vào, kiểu kết quả, ví dụ, gợi ý và lỗi thường gặp trong bài HTML
trước khi viết mỗi hàm. costs là Dict tra theo ID, không phải mảng theo vị trí đơn.
binary_search trả về Order hoặc nothing. BFS trả về distance, parent, routes;
đường hợp lệ có ít cạnh nhất được chấp nhận dù khác thứ tự duyệt minh họa.
knapsack trả về ids, value, cost, table; nếu có nhiều tập tối ưu, có thể chọn một
tập tối ưu hợp lệ. Ô F(i,b) nằm ở table[i+1,b+1] của Julia.

Sau khi lưu code, khởi động lại Julia REPL rồi chạy lại phần include/đọc dữ liệu
trước khi gọi ví dụ. Lưu file không tự cập nhật hàm trong phiên REPL đã mở.
Mỗi lệnh kiểm tra trong terminal tự mở một phiên Julia mới.
Khung chưa cài thuật toán báo CHUA_HOAN_THANH; đây là vị trí cần hoàn thiện.

## 4. Chạy một luồng ứng dụng hoàn chỉnh

```text
julia TH_2026_10_09_Sinh_vien.jl --mini
julia TH_2026_10_09_Kiem_thu.jl --phase=app
julia TH_2026_10_09_Kiem_thu.jl --phase=all
```

Mini có ba đơn A/B/C (ID 1/2/3), sáu đỉnh, bảy cạnh, ngân sách 8. Mỗi đơn là
một chuyến từ kho 1 tới điểm giao rồi về kho. Thời gian = 2 × số cạnh + phục vụ.
Theo dõi kết quả BFS → chi phí → kế hoạch → hàng đợi → giao → hoàn tác → giao hết.
Ghi trạng thái hàng đợi/ngăn xếp/thời gian/lợi ích trên phiếu, đối chiếu đầu ra
thực. ket_qua.csv được chương trình xuất trong data/MINI001 với chín cột.
Không gọi đây là tối ưu tuyến giao nhiều điểm trong một chuyến.

## 5. Trình bày bằng Julia và viết báo cáo

Mẫu bắt buộc: TH_2026_10_09_Pluto.jl, gọi cùng lõi đã cài đặt. Sau khi dữ liệu
đã tạo và bốn hàm đã chạy đúng, mở mẫu trong Pluto, đổi READ_DATA = true và
RUN_APP = true để xem chi phí, tuyến, tập chọn và bốn trạng thái giao/hoàn tác.
Sau khi sửa lõi, nạp lại notebook/khởi động lại Julia để dùng phiên bản vừa lưu.
Nếu chưa cài Pluto, vẫn dùng mẫu này: đổi hai cờ, lưu rồi chạy trực tiếp:

```text
julia TH_2026_10_09_Pluto.jl
```

Mẫu sẽ in kết quả từ cùng lõi. Bổ sung phần giải thích dưới dạng ô notebook hoặc
chuỗi văn bản/comment Julia: bài toán và dữ liệu → ý tưởng/giả mã bốn hàm →
truy vết → chi phí → kiểm thử → kết quả. Không thay đầu ra bằng số gõ tay.
Trên lớp tập trung code và kiểm tra; hoàn thiện notebook và báo cáo sau lớp.

Báo cáo gợi ý 3–5 trang, sáu mục được hướng dẫn trong bài học. Phiếu thực hành
Word/PDF dùng để ghi tay ý tưởng, truy vết, kiểm thử và trả lời năm câu cuối buổi.

## 6. Mở rộng cá nhân theo MSSV sau bộ mini

Thay B23DCCN001 bằng MSSV của chính mình, giữ nguyên chuỗi (kể cả số 0 đầu).
MSSV nhận 6–20 ký tự chữ/số ASCII. Code sinh 8–10 đơn và ngân sách 24–30
từ MSSV, có thể tạo lại cùng dữ liệu. Nêu hồ sơ và tham số trong báo cáo.

```text
julia TH_2026_10_09_Sinh_vien.jl --data B23DCCN001
julia TH_2026_10_09_Sinh_vien.jl B23DCCN001 --menu
```

Chỉ mở rộng sau khi mini chạy đúng. Menu sử dụng cùng lõi, không viết một app
khác cho từng thuật toán. Hai CSV tạo trong data/<MSSV>.

## 7. Nộp trên GitHub

Lưu toàn bộ code .jl (lõi, sinh/đọc CSV, kiểm thử, notebook), hai CSV đầu vào,
CSV kết quả, báo cáo/phiếu và README hướng dẫn tái lập trong một repository.
Ghi MSSV, URL repository và commit SHA trong phần nộp. Có thể khởi tạo Git tại
thư mục bài của mình, tạo commit và đẩy lên repository GitHub do mình tạo.
Giảng viên đánh giá ý tưởng, tính đúng đắn và mối liên hệ giữa các bước;
giao diện đẹp cần có kết quả đúng và minh chứng kiểm tra để được công nhận.

Nguồn sử dụng: chương trình học phần và bài tập tổng hợp của lớp; Julia Manual
(Getting Started, Functions) và Julia Base (I/O and Network), liên kết trong bài.
'''

TEACHER_README = '''# Bộ giảng viên — Thực hành Julia 09/10/2026

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
'''

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k in ('href', 'src') and v:
                self.refs.append(v)

def validate_links(entries):
    count = 0
    for name, blob in entries.items():
        if not name.endswith('.html'):
            continue
        parser = Links();parser.feed(blob.decode('utf-8'))
        for ref in parser.refs:
            url = urlsplit(ref)
            if url.scheme or url.netloc or not url.path:
                continue
            target = str(PurePosixPath(name).parent / unquote(url.path))
            assert target in entries, (name, ref, 'missing link')
            count += 1
    return count

def write_zip(name, entries):
    links = validate_links(entries)
    with ZipFile(ROOT/name, 'w', ZIP_DEFLATED, compresslevel=9) as z:
        for target, blob in entries.items():
            assert '..' not in PurePosixPath(target).parts and not target.startswith('/')
            z.writestr(target, blob)
    with ZipFile(ROOT/name) as z:
        assert z.testzip() is None
        assert len(z.namelist()) == len(entries) == len(set(z.namelist()))
        for target, blob in entries.items():
            assert z.read(target) == blob
    return {'name': name, 'files': len(entries), 'bytes': (ROOT/name).stat().st_size, 'local_links': links}

student = {}
for name in [*(BASE+ext for ext in ['.html','.docx','.pdf','.md']),
             'Phieu_thuc_hanh_CTDL_GT_2026_10_09.docx',
             'Phieu_thuc_hanh_CTDL_GT_2026_10_09.pdf',
             'TH_2026_10_09_Sinh_vien.jl','TH_2026_10_09_Kiem_thu.jl',
             'TH_2026_10_09_Pluto.jl']:
    student[name] = (ROOT/name).read_bytes()
for name in ['don_hang.csv', 'ban_do.csv']:
    student['data/MINI001/'+name] = (HERE/'data/MINI001'/name).read_bytes()
student['README.md'] = STUDENT_README.encode('utf-8')
page = student[BASE+'.html'].decode('utf-8')
page = page.replace('href="'+STUDENT_ZIP+'">Tải bộ sinh viên',
                    'href="README.md">Hướng dẫn trong gói')
student[BASE+'.html'] = page.encode('utf-8')
assert all('Loi_giai' not in n and 'teacher' not in n and 'giang_vien' not in n for n in student)
assert student['TH_2026_10_09_Sinh_vien.jl'].decode('utf-8').count('CHUA_HOAN_THANH:') == 4
student_result = write_zip(STUDENT_ZIP, student)
(ROOT/'README_Thuc_hanh_2026_10_09_Sinh_vien.md').write_text(STUDENT_README, encoding='utf-8')

teacher = dict(student)
teacher[BASE+'.html'] = (ROOT/(BASE+'.html')).read_bytes()
teacher['README.md'] = TEACHER_README.encode('utf-8')
teacher['README_Sinh_vien.md'] = student['README.md']
teacher[STUDENT_ZIP] = (ROOT/STUDENT_ZIP).read_bytes()
for name in ['TH_2026_10_09_Loi_giai.jl',
             'Huong_dan_giang_vien_CTDL_GT_2026_10_09.docx',
             'Huong_dan_giang_vien_CTDL_GT_2026_10_09.pdf']:
    teacher[name] = (ROOT/name).read_bytes()
sources = ['build_lab.py','package_lab.py','audit_package.py','audit_render.cjs','audit_files.py',
           'audit_notebook.jl','animations.js','animations.css','animation_frames.json',
           'lesson.js','lesson.css','lab_content.json','teacher_notes.json',
           'code_snippets.json','lab_solution.jl','lab_student.jl','test_lab.jl',
           'notebook_template.jl','worksheet_preview.html','teacher_preview.html',
           'qa/roadmap.png','qa/validation.json','qa/animation_final_states.json',
           'qa/undo_state.json','data/MINI001/don_hang.csv','data/MINI001/ban_do.csv']
for name in sources:
    teacher['_mon_hoc/Thuc_hanh_2026_10_09/'+name] = (HERE/name).read_bytes()
teacher_result = write_zip(TEACHER_ZIP, teacher)
(ROOT/'README_Thuc_hanh_2026_10_09_Giang_vien.md').write_text(TEACHER_README, encoding='utf-8')
result = {'status':'PACKAGES_PASS','student':student_result,'teacher':teacher_result}
(HERE/'qa/package_validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result))
