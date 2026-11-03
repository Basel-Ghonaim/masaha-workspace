# Adds samples to the showcase fixtures keeping prettier's one-line objects: python fixtures_add.py <spec.py>
# spec.py defines AR and EN dicts: key -> value. Collapses the filterTag one-line objects after dumping.
import json, re, sys, subprocess
p = r'C:\dev\masaha\app-lane-l\apps\web\src\pages\showcase\fixtures.json'
spec = {}
exec(open(sys.argv[1], encoding='utf8').read(), spec)
d = json.loads(open(p, encoding='utf8').read())
d['samples']['ar'].update(spec.get('AR',{})); d['samples']['en'].update(spec.get('EN',{}))
if 'MODIFY' in spec: spec['MODIFY'](d['samples'])
open(p, 'w', encoding='utf8', newline='').write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
subprocess.run('npx prettier --write apps/web/src/pages/showcase/fixtures.json', shell=True, cwd=r'C:\dev\masaha\app-lane-l', capture_output=True)
s = open(p, encoding='utf8', newline='').read()
s = re.sub(r'\{\n\s*"label": ("[^"\n]*"),\n\s*"removeLabel": ("[^"\n]*")\n\s*\}', r'{ "label": \1, "removeLabel": \2 }', s)
open(p, 'w', encoding='utf8', newline='').write(s)
