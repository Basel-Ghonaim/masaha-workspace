"""Break for finding 169: the site's shell draws the calendar; the build's check must refuse it.
Backup copy, break, build, check:build, restore by copy, rebuild."""
import io, os, shutil, subprocess

APP = r'C:\dev\masaha\app'
F = APP + r'\apps\web\src\pages\site\shell\SiteLayout.tsx'
S = r'C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\scripts'
BAK = S + r'\bak-l0-break-169-SiteLayout.tsx'

shutil.copyfile(F, BAK)
s = io.open(F, encoding='utf8', newline='').read()
s = s.replace(
    "import { Outlet } from 'react-router';\n",
    "import { Outlet } from 'react-router';\nimport { Calendar } from '@shared/design-system/calendar';\n",
    1,
)
s = s.replace(
    '  return (\n',
    "  if (window.name === 'calendar-break') {\n"
    '    return <Calendar mode="single" lang="ar" previousMonthLabel="" nextMonthLabel="" />;\n'
    '  }\n  return (\n',
    1,
)
io.open(F, 'w', encoding='utf8', newline='').write(s)
env = dict(os.environ, NODE_ENV='production')
try:
    b = subprocess.run('npm run build', cwd=APP, shell=True, env=env, capture_output=True, text=True, encoding='utf8')
    c = subprocess.run('npm run check:build', cwd=APP, shell=True, capture_output=True, text=True, encoding='utf8')
    out = f'build exit {b.returncode}\ncheck:build exit {c.returncode}\n{c.stdout}\n{c.stderr}'
    io.open(S + r'\l0-break-169.txt', 'w', encoding='utf8', newline='').write(out)
    print(out[-1500:])
finally:
    shutil.copyfile(BAK, F)
    print('restored', io.open(F, encoding='utf8').read() == io.open(BAK, encoding='utf8').read())
