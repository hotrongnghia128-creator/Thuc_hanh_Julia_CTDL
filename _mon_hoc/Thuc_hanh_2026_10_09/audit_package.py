"""Kiểm tra lệnh README từ các gói đã giải nén, bằng Julia thực tế."""
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import subprocess, csv, json, sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
QA = HERE/'qa'
sys.stdout.reconfigure(encoding='utf-8')
JULIA = Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'classroom/Cau truc du lieu va giai thuat/Giao trinh/_julia_runtime/julia-1.13.1/bin/julia.exe'
assert JULIA.is_file(), 'Truyền đường dẫn julia.exe làm đối số.'
logs = []
with TemporaryDirectory(prefix='package-check-', dir=QA) as tmp:
    location = Path(tmp).resolve()
    assert location.is_relative_to(QA.resolve())
    for role in ['Sinh_vien','Giang_vien']:
        target = location/role
        target.mkdir()
        with ZipFile(ROOT/f'Bo_Thuc_hanh_Julia_2026_10_09_{role}.zip') as z:
            for name in z.namelist():
                assert '..' not in PurePosixPath(name).parts
                assert (target/name).resolve().is_relative_to(target.resolve())
            z.extractall(target)
        commands = ([['TH_2026_10_09_Sinh_vien.jl','--data'],
                     ['TH_2026_10_09_Kiem_thu.jl','--phase=data']]
                    if role=='Sinh_vien' else
                    [['TH_2026_10_09_Kiem_thu.jl','--teacher','--phase=all'],
                     ['TH_2026_10_09_Loi_giai.jl','--mini']])
        for args in commands:
            done = subprocess.run([str(JULIA),*args],cwd=target,capture_output=True,
                                  text=True,encoding='utf-8',errors='replace',timeout=120)
            assert done.returncode==0,(role,args,done.stdout,done.stderr)
            logs.append({'role':role,'args':args,'exit':done.returncode,'output':done.stdout})
        if role=='Giang_vien':
            with (target/'data/MINI001/ket_qua.csv').open(encoding='utf-8',newline='') as f:
                rows=list(csv.DictReader(f))
            assert len(rows)==3 and len(rows[0])==9
            assert sum(int(r['chi_phi']) for r in rows if r['da_giao']=='1')==8
            assert sum(int(r['loi_ich']) for r in rows if r['da_giao']=='1')==14
result={'status':'EXTRACTED_PACKAGES_PASS','commands':logs,'csv':{'rows':3,'columns':9,'spent':8,'earned':14}}
(QA/'extracted_packages.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':result['status'],'commands':len(logs),'csv':result['csv']}))
