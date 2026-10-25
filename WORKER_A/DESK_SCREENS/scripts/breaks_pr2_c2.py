import io, shutil, subprocess, sys, filecmp
S='C:/dev/masaha/workspace/WORKER_A/DESK_SCREENS/scripts'
W='C:/dev/masaha/app/apps/web/src/features/desk/'
BREAKS = [
  ('45', 'hooks/search/useDeskSearch.ts',
   "        : answer === undefined\n          ? ('failed' as const)\n          : ('ready' as const);",
   "        : ('ready' as const);",
   ['component', 'src/features/desk/hooks/search']),
  ('46', 'hooks/search/useDeskSearch.ts',
   "      autoFocus: wide,", "      autoFocus: wide || true,",
   ['component', 'src/features/desk/components/search']),
  ('47', 'services/balanceView.ts',
   "  return { label: words.settled, tone: 'neutral' };",
   "  return null as unknown as BalanceView;",
   ['unit', 'src/features/desk/services/balanceView']),
]
only = sys.argv[1:]
for name, rel, a, b, (lane, path) in BREAKS:
    if only and name not in only: continue
    f = W + rel; bak = f'{S}/bak-pr2-break-{name}'
    shutil.copyfile(f, bak)
    s = io.open(f, encoding='utf-8', newline='').read()
    assert s.count(a) == 1, (name, a)
    io.open(f, 'w', encoding='utf-8', newline='').write(s.replace(a, b))
    out = subprocess.run(f'npm run test:{lane} -w @masaha/web -- {path}', shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace', cwd='C:/dev/masaha/app')
    io.open(f'{S}/break-pr2-{name}.txt', 'w', encoding='utf-8').write(out.stdout + out.stderr)
    shutil.copyfile(bak, f)
    assert filecmp.cmp(f, bak, shallow=False)
    lines = [l for l in (out.stdout + out.stderr).splitlines() if '×' in l or 'Tests ' in l or 'Test Files' in l]
    print(f'break {name}:', *lines, 'restored', sep='\n  ')
