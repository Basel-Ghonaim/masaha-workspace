"""Commit 6's breaks (plan §10 tests 82–84): each from a backup copy, run, restored by copy."""
import io, shutil, subprocess

APP = 'C:/dev/masaha/app/'
S = 'C:/dev/masaha/workspace/WORKER_A/PAYMENTS_STEP10/scripts/'
W = 'apps/web/src/'
BREAKS_ALL = [
    ('82', W + 'features/announcements/services/runningClosure.ts',
     "(endsAt === null || Date.parse(endsAt) > at)", "(endsAt === null || Date.parse(endsAt) >= at)",
     'test:unit', 'src/features/announcements/services/runningClosure.unit.test.ts'),
    ('83', W + 'features/announcements/hooks/public/usePublicAnnouncements.ts',
     ".filter((announcement) => announcement.id !== closure?.id)", ".filter(() => true)",
     'test:component', 'src/features/announcements/components/public src/pages/site/public/space/SpacePage.component.test.tsx'),
    ('84a', W + 'features/directory/components/page/SpaceDetails.tsx',
     "        {announcements?.(view.announcements)}\n        <PricesSection prices={view.prices} />\n",
     "        <PricesSection prices={view.prices} />\n        {announcements?.(view.announcements)}\n",
     'test:component', 'src/pages/site/public/space/SpacePage.component.test.tsx'),
    ('84b', W + 'features/directory/components/page/SpaceDetails.tsx',
     "        {view.unverified !== null && (",
     "        {notice?.(view.announcements)}\n        {view.unverified !== null && (",
     'test:component', 'src/pages/site/public/space/SpacePage.component.test.tsx'),
]
BREAKS = [b for b in BREAKS_ALL if b[0] == '84b']
for name, f, old, new, lane, tests in BREAKS:
    bak = S + f'bak-c6-break-{name}.txt'
    shutil.copyfile(APP + f, bak)
    try:
        s = io.open(APP + f, encoding='utf8', newline='').read()
        assert s.count(old) == 1, (name, old)
        s = s.replace(old, new)
        if name == '84b':
            # the notice drawn after the head instead of above the page
            s = s.replace(
                '        <div className="empty:hidden lg:col-span-12">{notice(view.announcements)}</div>\n',
                '        null\n')
        io.open(APP + f, 'w', encoding='utf8', newline='').write(s)
        r = subprocess.run(f'npm run {lane} -w @masaha/web -- {tests}', cwd=APP, shell=True,
                           capture_output=True, text=True, encoding='utf8')
        out = r.stdout + r.stderr
        io.open(S + f'c6-break-{name}.txt', 'w', encoding='utf8', newline='').write(out)
        print(f'--- break {name}: exit {r.returncode}')
        for line in out.splitlines():
            if any(k in line for k in ('×', 'Tests ', 'AssertionError', 'expected')):
                print('   ', line.strip()[:200])
    finally:
        shutil.copyfile(bak, APP + f)
        print('    restored', io.open(APP + f, 'rb').read() == io.open(bak, 'rb').read())
