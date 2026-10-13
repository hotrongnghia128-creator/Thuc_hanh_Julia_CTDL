from pathlib import Path
from docx import Document
import json,pdfplumber
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent;QA=HERE/'qa'
spec=json.loads((HERE/'lab_content.json').read_text(encoding='utf-8-sig'))
teacher=json.loads((HERE/'teacher_notes.json').read_text(encoding='utf-8-sig'))
assert sum(x['minutes'] for x in teacher['timeline90'])==90
assert sum(x['minutes'] for x in teacher['timeline225'])==225
student=(ROOT/'TH_2026_10_09_Sinh_vien.jl').read_text(encoding='utf8')
assert student.count('CHUA_HOAN_THANH:')==4
pages={}
for name in ('Thuc_hanh_CTDL_GT_Julia_2026_10_09','Phieu_thuc_hanh_CTDL_GT_2026_10_09','Huong_dan_giang_vien_CTDL_GT_2026_10_09'):
 with pdfplumber.open(ROOT/(name+'.pdf')) as pdf:
  pages[name]=len(pdf.pages)
  for i,page in enumerate(pdf.pages):
   assert page.extract_text().strip(),(name,i,'blank')
   for c in page.chars:
    assert c['x0']>=-1 and c['x1']<=page.width+1 and c['top']>=-1 and c['bottom']<=page.height+1,(name,i,'clipped')
  pdf.pages[0].to_image(resolution=100).save(QA/(name+'_page1.png'))
 doc=Document(ROOT/(name+'.docx'))
 assert doc.styles['Normal'].font.name=='Times New Roman' and doc.styles['Normal'].font.size.pt==14
 assert any('PAGE' in p._p.xml for p in doc.sections[0].footer.paragraphs)
 if not name.startswith('Huong_dan'):
  assert 'Đáp án câu hỏi cuối buổi' not in doc._element.xml
assert len(Document(ROOT/'Thuc_hanh_CTDL_GT_Julia_2026_10_09.docx').inline_shapes)==1
(QA/'validation.json').write_text(json.dumps({'status':'FILES_PASS','pdf_pages':pages,'todo':4,'timeline':[90,180,225]},ensure_ascii=False),encoding='utf8')
print(json.dumps({'status':'FILES_PASS','pdf_pages':pages,'todo':4,'timeline':[90,180,225]}))
