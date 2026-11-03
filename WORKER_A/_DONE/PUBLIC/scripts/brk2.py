"""Make one break, run the given vitest command, restore the file from a copy, print the red lines.

Usage: python -X utf8 brk2.py <file> <old> <new> <vitest args...>
"""
import io
import shutil
import subprocess
import sys

path, old, new, *args = sys.argv[1:]
backup = path + '.bak-break'
shutil.copyfile(path, backup)
try:
    s = io.open(path, encoding='utf-8', newline='').read()
    assert s.count(old) == 1, ('break text found', s.count(old))
    io.open(path, 'w', encoding='utf-8', newline='').write(s.replace(old, new))
    out = subprocess.run(
        ['npx.cmd', 'vitest', 'run', *args],
        cwd='C:/dev/masaha/app/apps/web',
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
    )
    for line in (out.stdout + out.stderr).splitlines():
        if any(k in line for k in ('×', 'Tests ', 'Test Files', 'Error', 'expected')):
            print(line)
finally:
    shutil.move(backup, path)
    print('restored')
