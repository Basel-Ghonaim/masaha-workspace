"""Resolve every conflict hunk in the given files by keeping both sides, ours (HEAD) first.

Only for files where both sides add lines (History lists, export lists). Prints each hunk resolved.
"""
import re
import sys

PAT = re.compile(r"<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n", re.S)
for path in sys.argv[1:]:
    s = open(path, encoding='utf8').read()
    n = len(PAT.findall(s))
    s = PAT.sub(lambda m: m.group(1) + m.group(2), s)
    assert '<<<<<<<' not in s and '>>>>>>>' not in s, path
    open(path, 'w', encoding='utf8', newline='').write(s)
    print(f'{path}: {n} hunk(s) kept both')
