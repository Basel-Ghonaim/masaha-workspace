"""Sequence editor: git's autosquash order kept; the commits named on the command line marked `edit`
(after their fixups, which are folded first by an `exec` amend is not needed: fixups follow the pick)."""
import io, sys

path = sys.argv[-1]
subjects = sys.argv[1:-1]
lines = io.open(path, encoding='utf8').read().split('\n')
out = []
for i, line in enumerate(lines):
    out.append(line)
    if line.startswith('pick ') and any(line.endswith(s) or s in line for s in subjects):
        # Stop after this commit and its fixups: an `exec false`-free way is a `break` after the last fixup.
        j = i + 1
        while j < len(lines) and lines[j].startswith('fixup '):
            j += 1
        out.append(f'#MARK-BREAK-AFTER {j}')
# Move each mark after its fixups.
result = []
pending = {}
for k, line in enumerate(out):
    if line.startswith('#MARK-BREAK-AFTER '):
        continue
    result.append(line)
marks = []
for i, line in enumerate(lines):
    if line.startswith('pick ') and any(s in line for s in subjects):
        j = i + 1
        while j < len(lines) and lines[j].startswith('fixup '):
            j += 1
        marks.append(lines[j - 1])
final = []
for line in lines:
    final.append(line)
    if line in marks:
        final.append('break')
io.open(path, 'w', encoding='utf8', newline='\n').write('\n'.join(final))
