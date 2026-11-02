"""Build static publication; resolve public links and retain provenance."""
from pathlib import Path
import hashlib
import html
import json
import re
import shutil
import subprocess
from urllib.parse import unquote,urlsplit
import markdown
ROOT=Path(__file__).resolve().parents[1];CONTENT=ROOT/'content';OUT=ROOT/'dist'
if OUT.exists():shutil.rmtree(OUT)
OUT.mkdir()
for folder in ['workshop/assets','workshop/handouts','poster']:
    shutil.copytree(CONTENT/folder,OUT/folder)
shutil.copy2(ROOT/'site/style.css',OUT/'style.css')
manifest=json.loads((CONTENT/'manifest.json').read_text());pkg=json.loads((CONTENT/'workshop/handouts/manifest.json').read_text())
versions={p['skill']:p['version'] for p in pkg['packages']}
nav='''<header class="nav"><div class="wrap"><a class="brand" href="/"><img src="/workshop/assets/paperdaily-mark.svg" alt="">知新 PaperDaily</a><nav class="links" aria-label="主导航"><a href="/prepare/">会前准备</a><a href="/#downloads">Skills下载</a><a href="/workshop/">讲解课件</a><a href="/poster/">海报</a></nav></div></header>'''
def shell(title,body):
    footer=f'<footer class="footer"><div class="wrap">11月5日 上午 · 陈春林 · PaperDaily研究工作坊<br>内容版本 {manifest["source_sha"][:7]} · <a href="https://github.com/alonegg/paperdaily-workshop-site">网站源码</a> · <a href="/version.json">发布信息</a></div></footer>'
    return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="PaperDaily科研外脑工作坊：会前准备、skills下载、在线课件与研究指南。"><title>'+html.escape(title)+' · PaperDaily工作坊</title><link rel="stylesheet" href="/style.css"><link rel="icon" href="/workshop/assets/paperdaily-mark.svg" type="image/svg+xml"></head><body>'+nav+body+footer+'</body></html>'
def write(path,text):
    p=OUT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
body=(ROOT/'site/index.html').read_text().replace('{{paperdaily_version}}',versions['paperdaily']).replace('{{deep_version}}',versions['paperdaily-deep-research'])
write('index.html',shell('如何把PaperDaily作为你的科研外脑',body));write('prepare/index.html',shell('会前准备',(ROOT/'site/prepare.html').read_text()))
def rewrite_link(link):
    parts=urlsplit(html.unescape(link));path=unquote(parts.path)
    if parts.scheme or link.startswith('#'):return link
    if path.endswith('.md'):
        if (CONTENT/'workshop'/Path(path).name).exists():return '/guides/'+Path(path).stem+'.html'+('#'+parts.fragment if parts.fragment else '')
        return None
    if path.startswith('assets/'):return '/workshop/'+path
    if path.startswith('handouts/'):return '/workshop/'+path
    if path.startswith('../materials/') or path.startswith('../plan/') or path.startswith('data/'):return None
    return link
for doc in (CONTENT/'workshop').glob('*.md'):
    body=markdown.markdown(doc.read_text(),extensions=['tables','fenced_code'])
    def anchor(m):
        link=rewrite_link(m[1])
        return '<a href="'+html.escape(link,quote=True)+'"'+m[2]+'>'+m[3]+'</a>' if link is not None else '<span class="unpublished">'+m[3]+'（制作核验档案未公开）</span>'
    body=re.sub(r'<a href="([^"]+)"([^>]*)>(.*?)</a>',anchor,body,flags=re.S)
    body=re.sub(r'src="assets/','src="/workshop/assets/',body)
    write('guides/'+doc.stem+'.html',shell(doc.stem,'<article class="article">'+body+'</article>'))
deck=(CONTENT/'workshop/index.html').read_text()
deck=re.sub(r'href="([^"]+\.md)"',lambda m:'href="/guides/'+html.escape(Path(m[1]).stem)+'.html"',deck)
write('workshop/index.html',deck)
try:site_sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True,stderr=subprocess.DEVNULL).strip()
except subprocess.CalledProcessError:site_sha='local'
version={'source_sha':manifest['source_sha'],'site_sha':site_sha,'skill_packages':pkg['packages']}
write('version.json',json.dumps(version,ensure_ascii=False,indent=2)+'\n')
write('404.html',shell('页面未找到','<div class="article"><h1>页面未找到</h1><p><a href="/">返回工作坊首页</a></p></div>'))
write('_headers','''/*
  Cache-Control: public, max-age=0, must-revalidate, no-transform
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
/workshop/handouts/*.zip
  Content-Disposition: attachment
  Cache-Control: public, max-age=0, must-revalidate, no-transform
''')
print(json.dumps({'source_sha':manifest['source_sha'],'static_files':sum(p.is_file() for p in OUT.rglob('*'))}))
