"""Verify canonical public release and complete download body hashes."""
from pathlib import Path
import hashlib,json,time,urllib.request
ROOT=Path(__file__).resolve().parents[1]
base='https://workshop.paperdaily.org'
expected=json.loads((ROOT/'dist/version.json').read_text())
def get(path):
    with urllib.request.urlopen(urllib.request.Request(base+path,headers={'User-Agent':'PaperDaily-Workshop-ReleaseCheck/1.0'}),timeout=60) as r:
        assert r.status==200;return r.read()
for attempt in range(6):
    actual=json.loads(get('/version.json'))
    if actual['source_sha']==expected['source_sha'] and actual['site_sha']==expected['site_sha']:break
    if attempt==5:raise ValueError('Served release does not match deployment')
    time.sleep(5)
for path in ['/','/prepare/','/poster/','/workshop/']:
    data=get(path);assert b'<html' in data.lower()
for pkg in expected['skill_packages']:
    body=get('/workshop/handouts/'+pkg['file'])
    assert hashlib.sha256(body).hexdigest()==pkg['sha256'],pkg['file']
video_path=ROOT/'dist/video/PaperDaily-workshop.mp4'
video_sha=None
if video_path.exists():
    video_body=get('/video/PaperDaily-workshop.mp4')
    video_sha=hashlib.sha256(video_body).hexdigest()
    assert video_sha==hashlib.sha256(video_path.read_bytes()).hexdigest(),'Public video hash mismatch'
print(json.dumps({'canonical_https':'passed','source_sha':actual['source_sha'],'site_sha':actual['site_sha'],'full_download_hashes':'passed','video_sha256':video_sha}))
