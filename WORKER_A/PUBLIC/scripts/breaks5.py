"""PR 1a commit 5's breaks: each made, its tests run, the file restored from its copy.

Usage: python -I breaks5.py [number ...]   (all when none given)
"""
import os
import shutil
import subprocess
import sys

WEB = r'C:\dev\masaha\app\apps\web'
D = 'src/features/directory'
LIST = f'{D}/hooks/list/useDirectoryList.ts'
LIST_TEST = f'{D}/hooks/list/useDirectoryList.component.test.tsx'
FILTERS = f'{D}/hooks/list/useDirectoryFilters.ts'
FILTERS_TEST = f'{D}/hooks/list/useDirectoryFilters.component.test.tsx'
COMPONENT_TEST = f'{D}/components/DirectoryList.component.test.tsx'

BREAKS = {
    '10': ('unit', f'{D}/services/filtersOf.ts',
           "sort: sort === 'relevance' && q === undefined ? undefined : sort,", 'sort,',
           [f'{D}/services/filtersOf.unit.test.ts']),
    '11': ('unit', f'{D}/services/filtersOf.ts',
           "if (filters.page !== 1) params.set('page', String(filters.page));",
           "params.set('page', String(filters.page));",
           [f'{D}/services/filtersOf.unit.test.ts']),
    '12': ('unit', f'{D}/services/filtersOf.ts',
           ': { q: undefined, refused: true };', ': { q: text, refused: true };',
           [f'{D}/services/filtersOf.unit.test.ts']),
    '13': ('unit', f'{D}/services/requestOf.ts',
           'priceMin: filters.min * 100', 'priceMin: filters.min',
           [f'{D}/services/requestOf.unit.test.ts']),
    '14': ('unit', f'{D}/repository/directoryRepository.ts',
           "{ params: request }", '{}',
           [f'{D}/repository/directoryRepository.unit.test.ts']),
    '15': ('unit', f'{D}/services/cardView.ts',
           "FULL: { word: 'full', variant: 'warning' }", "FULL: { word: 'full', variant: 'destructive' }",
           [f'{D}/services/cardView.unit.test.ts']),
    '16': ('unit', f'{D}/services/todayHours.ts',
           'days[gazaClockOf(now).dayOfWeek]', 'days[now.getUTCDay()]',
           [f'{D}/services/todayHours.unit.test.ts']),
    '18': ('component', FILTERS,
           'write({ ...filtersOf(latest.current), ...change, page: 1 });',
           'write({ ...filtersOf(latest.current), ...change });',
           [FILTERS_TEST]),
    '19': ('component', FILTERS,
           '      change: search.change,\n',
           '      change: (text: string) => {\n        search.change(text);\n'
           '        write({ ...filtersOf(latest.current), q: searchOf(text).q, page: 1 });\n      },\n',
           [FILTERS_TEST]),
    '20': ('component', LIST,
           "        query.isPending || pastLast\n          ? 'loading'",
           "        pastLast\n          ? 'loading'",
           [LIST_TEST]),
    '21': ('component', LIST, '              void query.refetch();\n', '', [LIST_TEST]),
    '22': ('component', LIST, 'line: view.view.message,', 'line: copy.errors.server,', [LIST_TEST]),
    '23': ('component', LIST,
           "              : filters.anyApplied\n                ? 'noMatch'\n                : 'empty',",
           "              : 'noMatch',",
           [LIST_TEST]),
    '24': ('component', f'{D}/hooks/list/useDirectoryQuery.ts',
           '    placeholderData: keepPreviousData,\n', '', [LIST_TEST]),
    '25': ('component', LIST, 'if (pastLast) replacePage(lastPage);', 'if (pastLast) return;',
           [LIST_TEST]),
    '26': ('component', LIST,
           "        : filters.anyApplied\n          ? words.count.matching",
           "        : false\n          ? words.count.matching",
           [LIST_TEST]),
    '27': ('component', f'{D}/components/list/DirectoryResults.tsx',
           '      <h2 ref={heading} id={headingId} tabIndex={-1} className="sr-only">\n'
           '        {results.heading}\n      </h2>\n',
           '', [COMPONENT_TEST]),
    '28': ('component', f'{D}/components/list/DirectoryResults.tsx',
           '    if (placed.current === page) return;\n', '', [COMPONENT_TEST]),
    '29': ('component', f'{D}/components/card/SpaceCover.tsx',
           '          onError={() => {\n            setFailed(cover);\n          }}\n', '',
           [COMPONENT_TEST]),
    '30': ('component', LIST,
           "  const orders: DirectoryOrder[] = searching\n    ? ['relevance', 'updated', 'name']\n"
           "    : ['updated', 'name'];",
           "  const orders: DirectoryOrder[] = ['relevance', 'updated', 'name'];",
           [COMPONENT_TEST]),
    '44': ('component', 'src/pages/site/routes.tsx',
           '            handle: { title: (copy) => copy.site.links.spaces } satisfies TitledHandle,\n',
           '', ['src/pages/site/routes.component.test.tsx']),
}

chosen = sys.argv[1:] or list(BREAKS)
for number in chosen:
    project, rel, old, new, tests = BREAKS[number]
    path = os.path.join(WEB, rel)
    backup = path + '.brkbak'
    shutil.copyfile(path, backup)
    try:
        with open(path, encoding='utf-8', newline='') as handle:
            text = handle.read()
        if text.count(old) != 1:
            print(f'--{number} BREAK NOT APPLIED: found {text.count(old)} times')
            continue
        with open(path, 'w', encoding='utf-8', newline='') as handle:
            handle.write(text.replace(old, new))
        run = subprocess.run(
            ['npx.cmd', 'vitest', 'run', '--project', project, *tests],
            cwd=WEB, capture_output=True, text=True, encoding='utf-8', errors='replace',
        )
        print(f'--{number}')
        for line in (run.stdout + run.stderr).splitlines():
            if any(mark in line for mark in ('×', 'Tests ', 'AssertionError', 'Error:')):
                print('  ' + line.strip()[:220])
    finally:
        shutil.copyfile(backup, path)
        os.remove(backup)
