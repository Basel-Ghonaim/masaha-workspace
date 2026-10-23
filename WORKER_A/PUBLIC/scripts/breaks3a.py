"""Make one planned break in a file, run a vitest command, restore the file from its copy.

usage: python breaks3a.py <file> <old> <new> <vitest args...>
"""
import io
import shutil
import subprocess
import sys

path, old, new, *args = sys.argv[1:]
backup = path + '.bak3a'
shutil.copyfile(path, backup)
try:
    text = io.open(path, encoding='utf-8', newline='').read()
    assert text.count(old) == 1, f'break target found {text.count(old)} times'
    io.open(path, 'w', encoding='utf-8', newline='').write(text.replace(old, new))
    run = subprocess.run(['npx', 'vitest', 'run', *args], capture_output=True, text=True,
                         encoding='utf-8', errors='replace', shell=True)
    out = run.stdout + run.stderr
    for line in out.splitlines():
        if any(key in line for key in ('×', 'Tests ', 'Error', 'Expected', 'Received', 'expected', 'Unable')):
            print(line.strip()[:220])
    print('exit', run.returncode)
finally:
    shutil.move(backup, path)
