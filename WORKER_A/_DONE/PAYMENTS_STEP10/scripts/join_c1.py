"""Join lane C's commit 1 onto lane B's commit 3: keep both sides, the admin's (B) first, then the user's (C)."""
import io, re

R = 'C:/dev/masaha/app-lane-c/'
C = re.compile(r'<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n', re.S)


def fix(path, fn):
    p = R + path
    s = io.open(p, encoding='utf8', newline='').read()
    t = C.sub(fn, s)
    assert '<<<<<<<' not in t and '>>>>>>>' not in t, path
    io.open(p, 'w', encoding='utf8', newline='').write(t)
    print('ok', path)


def both(m):
    return m.group(1) + m.group(2)


def imports(m):
    o, t = m.group(1), m.group(2)
    if o.startswith('import type {') and t.startswith('import type {') and o.count('\n') == 1:
        names = lambda x: [n.strip() for n in x[x.index('{') + 1:x.index('}')].split(',')]
        merged = sorted(set(names(o)) | set(names(t)))
        return o[:o.index('{') + 1] + ' ' + ', '.join(merged) + ' ' + o[o.index('}'):]
    return o + t


fix('apps/web/src/features/data-reports/hooks/queryKeys.ts', imports)
fix('apps/web/src/features/data-reports/index.ts', both)
fix('apps/web/src/features/data-reports/repository/dataReportsRepository.ts', both)


def fixture(m):
    o, t = m.group(1), m.group(2)
    if o.startswith('import type'):
        return imports(m)
    # ours: the admin's function up to its `...change` (the shared tail follows the markers); close it and
    # reopen the docblock for the user's.
    return o + '    ...change,\n  };\n}\n\n/**\n' + t


fix('apps/web/src/test/dataReport.ts', fixture)
