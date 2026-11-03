"""Lane A's breaks: each copies its file to a backup, makes one edit, runs the test file(s) that must
fail, records the output, and restores the file from the backup copy (never git checkout).

Usage: python breaks.py <set> [name ...]   (the set is a module next to this file: breaks_<set>.py)
"""
import importlib
import io
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = r'C:\dev\masaha\app-lane-a'
WEB = APP + r'\apps\web'
sys.path.insert(0, HERE)

which = sys.argv[1]
only = set(sys.argv[2:])
BREAKS = importlib.import_module('breaks_' + which).BREAKS

for b in BREAKS:
    if only and b['name'] not in only:
        continue
    path = WEB + '\\' + b['file'].replace('/', '\\')
    backup = os.path.join(HERE, 'bak-' + b['name'] + '-' + os.path.basename(path))
    shutil.copyfile(path, backup)
    try:
        s = io.open(path, encoding='utf8', newline='').read()
        for old, new in b['edits']:
            assert s.count(old) == 1, (b['name'], old)
            s = s.replace(old, new)
        io.open(path, 'w', encoding='utf8', newline='').write(s)
        lane = b['lane']
        cmd = 'npm run test:%s -w @masaha/web -- %s' % (lane, ' '.join(b['tests']))
        if b.get('filter'):
            cmd += ' -t "%s"' % b['filter']
        out = subprocess.run(cmd, cwd=APP, shell=True, capture_output=True, text=True,
                             encoding='utf8', errors='replace')
        text = out.stdout + out.stderr
        io.open(os.path.join(HERE, 'break-' + b['name'] + '.txt'), 'w', encoding='utf8').write(text)
        lines = [l for l in text.splitlines() if ('FAIL' in l or 'Error' in l or 'Tests ' in l
                                                   or 'Test Files' in l or 'expected' in l)]
        print('== %s (exit %d)' % (b['name'], out.returncode))
        for l in lines[:12]:
            print('   ' + l.strip()[:220])
    finally:
        shutil.copyfile(backup, path)
print('restored all')
