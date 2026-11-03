"""The red step taken by moving a commit's implementation aside (PR 1's D2): each file is copied to
bak-<set>-aside, removed, the tests run, then every file restored by copying back.

Usage: python aside.py <set> <file ...> -- <lane>:<test path>[::filter] ...
Paths are relative to apps/web.
"""
import io
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = r'C:\dev\masaha\app-lane-a'
WEB = APP + r'\apps\web'

name = sys.argv[1]
rest = sys.argv[2:]
cut = rest.index('--')
files, runs = rest[:cut], rest[cut + 1:]
store = os.path.join(HERE, 'bak-%s-aside' % name)
os.makedirs(store, exist_ok=True)
saved = []
try:
    for f in files:
        src = os.path.join(WEB, f.replace('/', '\\'))
        dst = os.path.join(store, f.replace('/', '__'))
        shutil.copyfile(src, dst)
        saved.append((src, dst))
        os.remove(src)
    out_all = ''
    for run in runs:
        lane, test = run.split(':', 1)
        flt = None
        if '::' in test:
            test, flt = test.split('::', 1)
        cmd = 'npm run test:%s -w @masaha/web -- %s' % (lane, test)
        if flt:
            cmd += ' -t "%s"' % flt
        out = subprocess.run(cmd, cwd=APP, shell=True, capture_output=True, text=True,
                             encoding='utf8', errors='replace')
        text = out.stdout + out.stderr
        out_all += '##### ' + cmd + ' (exit %d)\n' % out.returncode + text
        print('== %s (exit %d)' % (cmd, out.returncode))
        for l in text.splitlines():
            if 'FAIL' in l or 'Tests ' in l or 'Test Files' in l or 'Error:' in l:
                print('   ' + l.strip()[:220])
    io.open(os.path.join(HERE, 'red-%s.txt' % name), 'w', encoding='utf8').write(out_all)
finally:
    for src, dst in saved:
        shutil.copyfile(dst, src)
    print('restored %d files' % len(saved))
