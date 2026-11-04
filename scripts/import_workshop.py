"""Export an explicitly allowed public subset, failing before replacement."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import zipfile

DOCS=['WorkBuddy安装说明.md','授权网页与原文获取.md','Skills研究入门与工作流程.md','三类缺口与科研外脑.md','数据来源与领域期刊.md','数据口径与来源.md','日报如何筛选.md']
PATTERNS=[r'gh[pousr]_[A-Za-z0-9]{30,}',r'-----BEGIN (?:OPENSSH |RSA |EC )?PRIVATE KEY-----',r'wbSeedToken=[A-Za-z0-9_-]{12,}',r'(?i)Bearer\s+[A-Za-z0-9._-]{30,}']
def check_text(text):
    if any(re.search(p,text) for p in PATTERNS):raise ValueError('Potential credential: export refused')
def export(source,target):
    source=source.resolve()
    files=[source/'workshop/index.html',source/'poster/index.html',source/'poster/copy.json',source/'workshop/handouts/manifest.json']
    files += [source/'workshop'/n for n in DOCS]
    files += list((source/'workshop/assets').rglob('*'))+list((source/'poster/assets').rglob('*'))
    files += [source/'workshop/handouts'/n for n in ('paperdaily.zip','paperdaily-deep-research.zip')]
    if (source/'video/output/PaperDaily-workshop.mp4').exists():
        files += [source/'video/output'/n for n in ('PaperDaily-workshop.mp4','index.html','poster.png','workshop.srt','workshop.vtt','chapters.json')]
    selected={}
    for p in files:
        if p.is_dir():continue
        if p.is_symlink() or not p.is_file():raise ValueError('Missing file or symlink in allowlist')
        if p.suffix.lower() not in {'.html','.json','.md','.jpg','.jpeg','.png','.svg','.woff2','.txt','.zip','.mp4','.vtt','.srt'}:raise ValueError('Unsupported asset')
        name=str(p.relative_to(source));data=p.read_bytes()
        if p.suffix in {'.html','.json','.md','.svg','.txt','.vtt','.srt'}:
            text=data.decode('utf-8').replace('\r\n','\n').replace('\r','\n')
            if p.suffix=='.txt':text='\n'.join(line.rstrip() for line in text.splitlines())+'\n'
            if name=='workshop/index.html':text=re.sub(r'<aside\b[^>]*class="notes"[^>]*>.*?</aside>','',text,flags=re.S)
            text=re.sub(r'/Users/alone/[^\s<>）)]+','[制作路径]',text);check_text(text);data=text.encode()
        selected[name]=data
    for pkg in json.loads(selected['workshop/handouts/manifest.json'])['packages']:
        if hashlib.sha256(selected['workshop/handouts/'+pkg['file']]).hexdigest()!=pkg['sha256']:raise ValueError('ZIP manifest hash mismatch')
        with zipfile.ZipFile(source/'workshop/handouts'/pkg['file']) as z:
            if z.testzip():raise ValueError('Bad ZIP')
            for e in z.infolist():
                if e.filename.startswith('/') or '..' in Path(e.filename).parts or Path(e.filename).name in {'.env','credentials.json','settings.json'}:raise ValueError('Unsafe ZIP entry')
                if Path(e.filename).suffix in {'.md','.py','.json','.sh','.txt'}:check_text(z.read(e).decode())
    if target.exists():shutil.rmtree(target)
    for name,data in selected.items():
        p=target/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    sha=subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip()
    report={'source_sha':sha,'source_repository':'alonegg/paperdaily-research-workshop','files':{k:hashlib.sha256(v).hexdigest() for k,v in sorted(selected.items())},'publication':'allowlist; notes removed; no historical archive'}
    (target/'manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'source_sha':sha,'public_files':len(selected)}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--target',type=Path,default=Path(__file__).resolve().parents[1]/'content');a=p.parse_args();export(a.source,a.target)
