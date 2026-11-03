"""Red step from backups: `python red.py <name> aside|restore`.

aside: copies every listed implementation file to bak-<name>\\, then puts each modified one back to
HEAD's content (`git show`) and removes each new one. restore: copies the backups back.
"""
import json
import os
import shutil
import subprocess
import sys

WT = r'C:\dev\masaha\app-lane-c'
HERE = os.path.dirname(os.path.abspath(__file__))

name, action = sys.argv[1], sys.argv[2]
with open(os.path.join(HERE, f'red-{name}.json'), encoding='utf8') as f:
    spec = json.load(f)
bak = os.path.join(HERE, f'bak-{name}')

files = spec['modified'] + spec['new']
if action == 'aside':
    if os.path.exists(bak):
        sys.exit(f'{bak} exists: restore first')
    for rel in files:
        dest = os.path.join(bak, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(os.path.join(WT, rel), dest)
    for rel in spec['modified']:
        base = subprocess.run(['git', '-C', WT, 'show', f'HEAD:{rel}'], capture_output=True, check=True).stdout
        with open(os.path.join(WT, rel), 'wb') as f:
            f.write(base)
    for rel in spec['new']:
        os.remove(os.path.join(WT, rel))
    print('aside', len(files))
elif action == 'restore':
    for rel in files:
        shutil.copy2(os.path.join(bak, rel), os.path.join(WT, rel))
    shutil.rmtree(bak)
    print('restored', len(files))
