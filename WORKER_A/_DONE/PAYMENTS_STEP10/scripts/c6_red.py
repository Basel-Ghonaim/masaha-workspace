"""Commit 6's red step: its implementation moved aside (new files removed, changed ones as at HEAD),
its tests run, then everything restored by copy and checked."""
import io, os, shutil, subprocess

APP = 'C:/dev/masaha/app/'
S = 'C:/dev/masaha/workspace/WORKER_A/PAYMENTS_STEP10/scripts/'
BAK = S + 'bak-c6-red/'
NEW = [
    'apps/web/src/features/announcements/components/public/SpaceAnnouncements.tsx',
    'apps/web/src/features/announcements/hooks/public/usePublicAnnouncements.ts',
    'apps/web/src/features/announcements/services/runningClosure.ts',
    'apps/web/src/features/announcements/types/PublicAnnouncement.ts',
]
CHANGED = [
    'apps/web/src/features/announcements/components/public/ClosureNotice.tsx',
    'apps/web/src/features/announcements/components/sheet/AnnouncementSheet.tsx',
    'apps/web/src/features/announcements/index.ts',
    'apps/web/src/features/directory/components/page/SpaceDetails.tsx',
    'apps/web/src/features/directory/hooks/page/useSpacePage.ts',
    'apps/web/src/features/directory/types/SpacePageView.ts',
    'apps/web/src/pages/site/public/space/SpacePage.tsx',
]
os.makedirs(BAK, exist_ok=True)
for f in NEW + CHANGED:
    os.makedirs(os.path.dirname(BAK + f), exist_ok=True)
    shutil.copyfile(APP + f, BAK + f)
try:
    for f in NEW:
        os.remove(APP + f)
    for f in CHANGED:
        head = subprocess.run(['git', 'show', f'HEAD:{f}'], cwd=APP, capture_output=True).stdout
        io.open(APP + f, 'wb').write(head)
    r = subprocess.run(
        'npm run test:component -w @masaha/web -- src/features/announcements/components/public '
        'src/pages/site/public/space/SpacePage.component.test.tsx',
        cwd=APP, shell=True, capture_output=True, text=True, encoding='utf8')
    u = subprocess.run(
        'npm run test:unit -w @masaha/web -- src/features/announcements/services/runningClosure.unit.test.ts',
        cwd=APP, shell=True, capture_output=True, text=True, encoding='utf8')
    out = r.stdout + r.stderr + '\n=== unit\n' + u.stdout + u.stderr
    io.open(S + 'c6-red.txt', 'w', encoding='utf8', newline='').write(out)
    for line in out.splitlines():
        if any(k in line for k in ('×', 'FAIL', 'Test Files', 'Tests ', 'Error:', 'Unable')):
            print(line[:220])
finally:
    for f in NEW + CHANGED:
        os.makedirs(os.path.dirname(APP + f), exist_ok=True)
        shutil.copyfile(BAK + f, APP + f)
    same = all(io.open(APP + f, 'rb').read() == io.open(BAK + f, 'rb').read() for f in NEW + CHANGED)
    print('restored', same)
