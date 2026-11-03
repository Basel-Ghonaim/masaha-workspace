import os, runpy, sys
REPO = r'C:\dev\masaha\app-lane-w1'
spec = runpy.run_path(sys.argv[1])
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
for rel, change in spec['VARIANTS'].items():
    text = open(os.path.join(REPO, rel), encoding='utf8', newline='').read()
    open(os.path.join(out, rel.replace('/', '__')), 'w', encoding='utf8', newline='').write(change(text))
for rel in spec.get('PLAIN', []):
    if not os.path.exists(os.path.join(REPO, rel)):
        print('MISSING', rel)
print('ok')
