"""Check deployable links, audience boundaries, ZIP hashes and credentials."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import hashlib,json,re
from import_workshop import check_text
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'dist';fail=[]
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        for k in ['href','src']:
            if a.get(k):self.links.append(a[k])
for p in OUT.rglob('*'):
    if not p.is_file():continue
    if p.suffix in {'.html','.css','.json','.svg','.txt'}:
        t=p.read_text();check_text(t)
        if '/Users/alone/' in t or 'wbSeedToken=' in t:fail.append('Private path/token in '+str(p))
    if p.suffix=='.html':
        a=Links();a.feed(p.read_text())
        for link in a.links:
            u=urlsplit(link);rel=unquote(u.path)
            if u.scheme or not rel:continue
            target=OUT/rel.lstrip('/') if rel.startswith('/') else p.parent/rel
            if not target.is_file() and not (target/'index.html').is_file():fail.append(str(p.relative_to(OUT))+': '+rel)
manifest=json.loads((OUT/'workshop/handouts/manifest.json').read_text())
for pkg in manifest['packages']:
    assert hashlib.sha256((OUT/'workshop/handouts'/pkg['file']).read_bytes()).hexdigest()==pkg['sha256']
deck=(OUT/'workshop/index.html').read_text();assert '<aside class="notes"' not in deck
assert '300积分' in (OUT/'index.html').read_text()
assert not fail,'\n'.join(fail)
print(json.dumps({'local_links':'passed','zip_hashes':'passed','credential_scan':'passed','presenter_notes':'removed','slides':len(re.findall(r'<section class="slide\b',deck))}))
