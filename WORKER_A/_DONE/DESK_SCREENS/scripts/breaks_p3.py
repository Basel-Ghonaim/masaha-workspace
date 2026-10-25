# Applies one break to a file, runs a test command, records its output, restores the file.
# Usage: python breaks_p3.py <name> <file> <lane> <test path>  (old/new from breaks_p3.json)
import io, json, shutil, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")

APP = 'C:/dev/masaha/app'
OUT = 'C:/dev/masaha/workspace/WORKER_A/DESK_SCREENS/scripts'

name = sys.argv[1]
spec = json.load(io.open(f'{OUT}/breaks_p3.json', encoding='utf-8'))[name]
path = f"{APP}/{spec['file']}"
backup = f'{OUT}/bak-p3-break-{name}'
shutil.copyfile(path, backup)
try:
    text = io.open(path, encoding='utf-8', newline='').read()
    for old, new in spec['edits']:
        assert text.count(old) == 1, (name, old[:60], text.count(old))
        text = text.replace(old, new)
    io.open(path, 'w', encoding='utf-8', newline='').write(text)
    command = f"npm run {spec['lane']} -w @masaha/web -- {spec['test']}"
    run = subprocess.run(command, cwd=APP, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
    io.open(f'{OUT}/p3-break-{name}.txt', 'w', encoding='utf-8').write(run.stdout + run.stderr)
    print(f'{name}: exit {run.returncode}')
    for line in (run.stdout + run.stderr).splitlines():
        if any(mark in line for mark in ('×', 'Tests ', 'AssertionError', 'Unable to find', 'Expected', 'Received')):
            print('   ', line.strip()[:200])
finally:
    shutil.copyfile(backup, path)
