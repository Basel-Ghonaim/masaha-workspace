# Runs a list of breaks: python runbreaks.py <spec.py>
# The spec defines BREAKS = [(label, rel_file, old, new, test_cmd)] and REPO.
# Each break: backup by copy, replace (old once), run, record, restore by copy.
import shutil, subprocess, sys, os, runpy
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
spec = runpy.run_path(sys.argv[1])
repo = spec['REPO']
out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'breaks')
os.makedirs(out_dir, exist_ok=True)
only = sys.argv[2:]
for label, rel, old, new, cmd in spec['BREAKS']:
    if only and label not in only:
        continue
    path = os.path.join(repo, rel)
    bak = os.path.join(out_dir, 'bak-' + label)
    shutil.copyfile(path, bak)
    try:
        s = open(path, encoding='utf8', newline='').read()
        n = s.count(old)
        if n != 1:
            print(label, 'OLD TEXT FOUND', n, 'TIMES'); continue
        open(path, 'w', encoding='utf8', newline='').write(s.replace(old, new))
        r = subprocess.run(cmd, cwd=repo, shell=True, capture_output=True, text=True, encoding='utf8', errors='replace')
        out = r.stdout + r.stderr
        open(os.path.join(out_dir, label + '.txt'), 'w', encoding='utf8').write(out)
        lines = [l.strip() for l in out.splitlines() if any(k in l for k in ('×', 'Tests ', 'AssertionError', 'Expected', 'error TS', 'Error:'))]
        print('==', label, 'exit', r.returncode)
        for l in lines[:8]:
            print('   ', l[:200])
    finally:
        shutil.copyfile(bak, path)
