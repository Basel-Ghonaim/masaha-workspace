"""The fix round's document pass, run at rebase stops.
  python docpass.py admin    — at «list every space's reports»: finding 184's file, its index line, and
                                data-reports.md's Open findings with 167 and 184
  python docpass.py list     — at «list a user's favourite spaces»: finding 187's index line
  python docpass.py resolve  — a conflict in the findings index or a capability's Open findings: the union
                                of both sides' finding lines, by number ("None." dropped)"""
import io, os, re, subprocess, sys

APP = 'C:/dev/masaha/app/'
HERE = os.path.dirname(os.path.abspath(__file__))
F184 = 'docs/architecture/findings/184-a-reports-edit-the-field-link-may-not-scroll-to-its-section.md'
INDEX = 'docs/architecture/findings/README.md'
DR = 'docs/features/data-reports.md'
L167 = ("- [167. The admin's reports cannot be filtered by who handles them](../architecture/findings/"
        "167-the-admins-reports-cannot-be-filtered-by-who-handles-them.md) — no `verified` parameter on "
        "`GET /admin/data-reports`; «يعالجه» per row only.")
L184 = ("- [184. A report's «تعديل الحقل» may not scroll to its section](../architecture/findings/"
        "184-a-reports-edit-the-field-link-may-not-scroll-to-its-section.md) — the editor does not scroll to "
        "the address's anchor once its cards have drawn.")
I184 = "- [184. A report's «تعديل الحقل» may not scroll to its section](184-a-reports-edit-the-field-link-may-not-scroll-to-its-section.md)"
I187 = "- [187. A favourite just removed cannot be saved again for an undo](187-a-favourite-just-removed-cannot-be-saved-again-for-an-undo.md)"
NUM = re.compile(r'^- \[(\d+)\.')


def read(f):
    return io.open(APP + f, encoding='utf8', newline='').read()


def write(f, s):
    io.open(APP + f, 'w', encoding='utf8', newline='').write(s)


def add_to_open(index_text, line):
    """Adds `line` to the index's Open group, in number order."""
    lines = index_text.split('\n')
    start = lines.index('## Open')
    end = next(k for k in range(start + 1, len(lines)) if lines[k].startswith('## '))
    n = int(NUM.match(line).group(1))
    entries = [k for k in range(start + 1, end) if NUM.match(lines[k])]
    at = next((k for k in entries if int(NUM.match(lines[k]).group(1)) > n), entries[-1] + 1)
    lines.insert(at, line)
    return '\n'.join(lines)


how = sys.argv[1]
if how == 'admin':
    src = os.path.join(HERE, 'f184.md')
    io.open(APP + F184, 'w', encoding='utf8', newline='').write(io.open(src, encoding='utf8').read())
    write(INDEX, add_to_open(read(INDEX), I184))
    s = read(DR)
    a = '## Open findings\n\nNone.\n'
    assert s.count(a) == 1
    write(DR, s.replace(a, f'## Open findings\n\n{L167}\n{L184}\n'))
    print('admin docs')
elif how == 'list':
    write(INDEX, add_to_open(read(INDEX), I187))
    print('list docs')
else:
    C = re.compile(r'<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n', re.S)
    files = subprocess.run(['git', 'diff', '--name-only', '--diff-filter=U'], cwd=APP, capture_output=True,
                           text=True).stdout.split()
    for f in files:
        s = read(f)

        def union(m):
            lines = [l for l in (m.group(1) + m.group(2)).split('\n') if l.strip()]
            assert all(NUM.match(l) or l == 'None.' for l in lines), (f, lines)
            keep = {}
            for l in lines:
                if l != 'None.':
                    keep[int(NUM.match(l).group(1))] = l
            return ''.join(keep[k] + '\n' for k in sorted(keep))

        t = C.sub(union, s)
        assert '<<<<<<<' not in t
        write(f, t)
        subprocess.run(['git', 'add', f], cwd=APP, check=True)
        print('resolved', f)
