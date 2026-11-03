import re
pat = re.compile(r'<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n', re.S)

def resolve(path, fns):
    s = open(path, encoding='utf-8', newline='').read()
    i = iter(fns)
    out, n = pat.subn(lambda m: next(i)(m.group(1), m.group(2)), s)
    assert n == len(fns), (path, n)
    assert '<<<<<<<' not in out
    open(path, 'w', encoding='utf-8', newline='').write(out)
    print(path, n)

# gazaTime: F's functions, closed, then O's
resolve('packages/shared/src/core/gazaTime.ts', [lambda o, t: o + '}\n\n' + t])

# the test: the imports' union in order; F's describe closed, then O's
def imports(o, t):
    names = sorted(set(re.findall(r'^\s+(\w+),$', o + t, re.M)))
    return ''.join(f'  {n},\n' for n in names)
resolve('packages/shared/src/core/gazaTime.unit.test.ts', [imports, lambda o, t: o + '  });\n});\n\n' + t])

# data-reports: O's openCounts first, then L's doc of pageAll
def reports(o, t):
    head, _sep, _old_doc = t.partition('    /**\n     * A page of every report')
    return head + '    /**\n' + o
resolve('apps/api/src/modules/data-reports/data-reports.repository.ts', [reports])
