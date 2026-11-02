"""Tests for public-export failure boundaries."""
import hashlib,json,tempfile,unittest,zipfile
from pathlib import Path
from import_workshop import check_text,export,DOCS
class ExportSafety(unittest.TestCase):
    def test_credential_refused(self):
        with self.assertRaises(ValueError):check_text('gh'+'p_'+'A'*36)
    def fixture(self,root,unsafe=False):
        for name in ['workshop/index.html','poster/index.html','poster/copy.json']+['workshop/'+n for n in DOCS]:
            p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('{}' if p.suffix=='.json' else 'public')
        (root/'workshop/assets').mkdir();(root/'poster/assets').mkdir();h=root/'workshop/handouts';h.mkdir()
        packages=[]
        for name in ['paperdaily.zip','paperdaily-deep-research.zip']:
            with zipfile.ZipFile(h/name,'w') as z:z.writestr('../escape.txt' if unsafe else 'SKILL.md','safe')
            packages.append({'file':name,'sha256':hashlib.sha256((h/name).read_bytes()).hexdigest()})
        (h/'manifest.json').write_text(json.dumps({'packages':packages}))
    def test_mismatch_preserves_previous_export(self):
        with tempfile.TemporaryDirectory() as d:
            r=Path(d);source=r/'source';target=r/'target';source.mkdir();target.mkdir();(target/'previous').write_text('keep');self.fixture(source)
            (source/'workshop/handouts/paperdaily.zip').write_bytes(b'invalid')
            with self.assertRaisesRegex(ValueError,'hash mismatch'):export(source,target)
            self.assertEqual((target/'previous').read_text(),'keep')
    def test_zip_traversal_refused_before_replace(self):
        with tempfile.TemporaryDirectory() as d:
            r=Path(d);source=r/'source';source.mkdir();self.fixture(source,unsafe=True)
            with self.assertRaisesRegex(ValueError,'Unsafe ZIP'):export(source,r/'target')
if __name__=='__main__':unittest.main()
