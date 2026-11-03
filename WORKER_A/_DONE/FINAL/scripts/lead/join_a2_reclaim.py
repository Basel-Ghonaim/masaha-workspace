import re

ROOT = 'C:/dev/masaha/app-lane-a2/'
PAT = re.compile(r"<<<<<<< HEAD\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n", re.S)


def both(p, special=None):
    path = ROOT + p
    s = open(path, encoding='utf8').read()

    def pick(m):
        ours, theirs = m.group(1), m.group(2)
        if special:
            r = special(ours, theirs)
            if r is not None:
                return r
        return ours + theirs

    s = PAT.sub(pick, s)
    assert '<<<<<<<' not in s and '>>>>>>>' not in s
    open(path, 'w', encoding='utf8', newline='').write(s)


both('apps/api/src/app.ts')


def jobs_test(ours, theirs):
    if '{},' in ours:
        return ours.replace('        {},\n        {},\n        {},\n', '        {},\n        {},\n        {},\n        {},\n')
    return None


both('apps/api/src/shared/jobs/jobs.api.test.ts', jobs_test)


def contract(ours, theirs):
    reclaim = [l for l in theirs.splitlines(keepends=True) if l.startswith('- **`photos.reclaimOrphans`**')]
    assert len(reclaim) == 1
    return ours + reclaim[0]


both('docs/api/api-contract.md', contract)
print('ok')
