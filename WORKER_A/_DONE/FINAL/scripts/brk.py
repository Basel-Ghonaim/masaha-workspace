# Break helper: python brk.py <repo> <label> <file> <old-file> <new-file> -- <test command...>
# Backs the file up, replaces old with new (texts read from files), runs the command, restores by copy.
import shutil, subprocess, sys, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
repo, label, rel, oldf, newf = sys.argv[1:6]
cmd = sys.argv[sys.argv.index('--')+1:]
out_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(repo, rel)
bak = os.path.join(out_dir, 'lead', 'bak-' + label)
shutil.copyfile(path, bak)
try:
    s = open(path, encoding='utf8').read()
    old = open(oldf, encoding='utf8').read(); new = open(newf, encoding='utf8').read()
    assert s.count(old) == 1, 'old text not found once'
    open(path, 'w', encoding='utf8', newline='').write(s.replace(old, new))
    r = subprocess.run(' '.join(cmd), cwd=repo, shell=True, capture_output=True, text=True, encoding='utf8', errors='replace')
    out = r.stdout + r.stderr
    open(os.path.join(out_dir, 'lead', 'break-' + label + '.txt'), 'w', encoding='utf8').write(out)
    print('exit', r.returncode)
    for l in out.splitlines():
        if any(k in l for k in ('FAIL', 'Tests ', 'AssertionError', 'Expected', 'error TS', '✗', '×')):
            print(l[:220])
finally:
    shutil.copyfile(bak, path)
