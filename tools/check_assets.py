"""Check deterministic control assets, examples, source links and executable docs."""
import json,sys
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from orderlab.controls import controls
from orderlab import analyze,verify
cs=controls();assert json.loads((ROOT/'docs/controls.json').read_text())==cs
for c in cs:
 assert json.loads((ROOT/'examples'/f"{c['id']}.json").read_text())==c['input']
 assert verify(analyze(c['input']))
class Page(HTMLParser):
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag in ['link','script']:
   f=a.get('src')or a.get('href')
   if f and not f.startswith('http'):assert(ROOT/'docs'/f).is_file(),f
Page().feed((ROOT/'docs/index.html').read_text())
for f in ['README.md','METHOD.md','SOURCES.md','VALIDATION.md','LICENSE','requirements-reference.txt','.github/workflows/ci.yml','pyproject.toml']:
 assert(ROOT/f).is_file(),f
assert 'orderlab' in (ROOT/'docs/index.html').read_text().lower()
print(json.dumps(dict(control_assets=len(cs),example_files=len(cs),source='deterministic native controls',checks='pass')))
