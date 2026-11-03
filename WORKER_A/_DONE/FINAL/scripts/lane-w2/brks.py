# Breaks from a spec: python brks.py <repo> <spec.json>
# spec: [{"label": "B150", "file": "apps/web/...", "old": "...", "new": "...", "cmd": "npm run ..."}]
# Each break: the file backed up, old replaced by new (once), the command run, the file restored by copy.
import json, shutil, subprocess, sys, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
repo, spec_path = sys.argv[1:3]
out_dir = os.path.dirname(os.path.abspath(__file__))
for brk in json.load(open(spec_path, encoding='utf8')):
    label = brk['label']
    path = os.path.join(repo, brk['file'])
    bak = os.path.join(out_dir, 'bak-' + label)
    shutil.copyfile(path, bak)
    try:
        s = open(path, encoding='utf8').read()
        if s.count(brk['old']) != 1:
            print(label, 'old text found', s.count(brk['old']), 'times'); continue
        open(path, 'w', encoding='utf8', newline='').write(s.replace(brk['old'], brk['new']))
        r = subprocess.run(brk['cmd'], cwd=repo, shell=True, capture_output=True, text=True, encoding='utf8', errors='replace')
        out = r.stdout + r.stderr
        open(os.path.join(out_dir, 'break-' + label + '.txt'), 'w', encoding='utf8').write(out)
        print('==', label, 'exit', r.returncode)
        for l in out.splitlines():
            if any(k in l for k in ('Test Files', 'Tests ', 'AssertionError', '×', 'Error:')):
                print('  ', l.strip()[:200])
    finally:
        shutil.copyfile(bak, path)
