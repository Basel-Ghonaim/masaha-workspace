"""Resolve a join's text conflicts by keeping both sides, in the plan's order (ours = the PR branch, first; theirs =
the lane being joined, after). For a conflict of one long line on each side (a document's list line), the lane's
added clause is found as the text theirs has beyond the common base and inserted at the same anchor in ours.
Usage: python join_resolve.py <worktree> <file> [<file> ...]"""
import io, re, subprocess, sys

root, files = sys.argv[1], sys.argv[2:]
CONFLICT = re.compile(r'<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n', re.S)


def base_of(path):
    # The stage-1 (common ancestor) version of the file.
    return subprocess.run(['git', 'show', f':1:{path}'], cwd=root, capture_output=True, text=True,
                          encoding='utf8').stdout


def merge_line(ours, theirs, base_lines):
    """ours/theirs: one line each. Find base line b they both changed; theirs = b with an insertion."""
    for b in base_lines:
        # longest common prefix/suffix of b and theirs
        p = 0
        while p < min(len(b), len(theirs)) and b[p] == theirs[p]:
            p += 1
        s = 0
        while s < min(len(b), len(theirs)) - p and b[-1 - s] == theirs[-1 - s]:
            s += 1
        if p + s == len(b) and len(theirs) > len(b) and p > 40:
            added = theirs[p:len(theirs) - s]
            tail = b[p:]  # what follows the insertion point in the base
            anchor = tail[:60]
            i = ours.find(anchor, 0)
            # the same anchor in ours: the last occurrence after the common prefix
            i = ours.rfind(anchor)
            if i < 0:
                return None
            return ours[:i] + added + ours[i:]
    return None


for f in files:
    p = f'{root}/{f}'
    s = io.open(p, encoding='utf8', newline='').read()
    base_lines = base_of(f).split('\n')

    def resolve(m):
        ours, theirs = m.group(1), m.group(2)
        o, t = ours.rstrip('\n').split('\n'), theirs.rstrip('\n').split('\n')
        if len(o) == 1 and len(t) == 1 and len(o[0]) > 300:
            merged = merge_line(o[0], t[0], base_lines)
            if merged is None:
                raise SystemExit(f'{f}: could not place the clause')
            return merged + '\n'
        return ours + theirs

    t = CONFLICT.sub(resolve, s)
    assert '<<<<<<<' not in t and '>>>>>>>' not in t, f
    io.open(p, 'w', encoding='utf8', newline='').write(t)
    print('resolved', f)
