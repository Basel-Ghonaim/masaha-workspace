# Red step for code written first: python red.py <repo> <label> <file,file,...> -- <test command...>
# Backs each file up, removes it, runs the command, restores every file by copy.
import shutil, subprocess, sys, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
repo, label, rels = sys.argv[1:4]
cmd = sys.argv[sys.argv.index('--')+1:]
out_dir = os.path.dirname(os.path.abspath(__file__))
files = rels.split(',')
backups = []
try:
    for i, rel in enumerate(files):
        path = os.path.join(repo, rel)
        bak = os.path.join(out_dir, 'bak-red-' + label + '-' + str(i))
        shutil.copyfile(path, bak)
        backups.append((bak, path))
        os.remove(path)
    r = subprocess.run(' '.join(cmd), cwd=repo, shell=True, capture_output=True, text=True, encoding='utf8', errors='replace')
    out = r.stdout + r.stderr
    open(os.path.join(out_dir, 'red-' + label + '.txt'), 'w', encoding='utf8').write(out)
    print('exit', r.returncode)
    for l in out.splitlines():
        if any(k in l for k in ('FAIL', 'Test Files', 'Tests ', 'AssertionError', 'Error:', '×')):
            print(l[:220])
finally:
    for bak, path in backups:
        shutil.copyfile(bak, path)
