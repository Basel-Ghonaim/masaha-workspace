"""Make one break, run the given vitest files, restore the file from its copy, print the result lines.

Usage: brk.py <project> <file> <old> <new> <test path>...
The file is copied aside first and restored after the run, whatever the run's outcome.
"""
import shutil
import subprocess
import sys

project, path, old, new, *tests = sys.argv[1:]
backup = path + '.brkbak'
shutil.copyfile(path, backup)
try:
    with open(path, encoding='utf-8', newline='') as handle:
        text = handle.read()
    if text.count(old) != 1:
        print('BREAK NOT APPLIED: old text found', text.count(old), 'times')
        sys.exit(2)
    with open(path, 'w', encoding='utf-8', newline='') as handle:
        handle.write(text.replace(old, new))
    run = subprocess.run(
        ['npx.cmd', 'vitest', 'run', '--project', project, *tests],
        cwd=r'C:\dev\masaha\app\apps\web',
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
    )
    for line in (run.stdout + run.stderr).splitlines():
        if any(mark in line for mark in ('×', 'Tests ', 'Test Files ', 'AssertionError', 'Error:')):
            print(line.strip())
finally:
    shutil.copyfile(backup, path)
    import os
    os.remove(backup)
