"""Break for finding 169 (b): the calendar served again by the main barrel and drawn through it by a
site page (Home). Backup copies, break, build, check:build, restore by copy."""
import io, os, shutil, subprocess

APP = r'C:\dev\masaha\app'
S = r'C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\scripts'
INDEX = APP + r'\apps\web\src\shared\design-system\index.ts'
HOME = APP + r'\apps\web\src\pages\site\public\home\HomePage.tsx'
files = {INDEX: S + r'\bak-l0-break-169b-index.ts', HOME: S + r'\bak-l0-break-169b-HomePage.tsx'}
for f, b in files.items():
    shutil.copyfile(f, b)


def edit(path, fn):
    s = io.open(path, encoding='utf8', newline='').read()
    t = fn(s)
    assert t != s, path
    io.open(path, 'w', encoding='utf8', newline='').write(t)


edit(INDEX, lambda s: s + "export { Calendar } from './components/fields/Calendar';\n")


def home(s):
    i = s.index('\nexport function HomePage')
    s = "import { Calendar } from '@shared/design-system';\n" + s
    i = s.index('\nexport function HomePage')
    j = s.index('{\n', i) + 2
    return (
        s[:j]
        + "  if (window.name === 'calendar-break') {\n"
        + '    return <Calendar mode="single" lang="ar" previousMonthLabel="" nextMonthLabel="" />;\n'
        + '  }\n'
        + s[j:]
    )


edit(HOME, home)
env = dict(os.environ, NODE_ENV='production')
try:
    b = subprocess.run('npm run build', cwd=APP, shell=True, env=env, capture_output=True, text=True, encoding='utf8')
    c = subprocess.run('npm run check:build', cwd=APP, shell=True, capture_output=True, text=True, encoding='utf8')
    out = f'build exit {b.returncode}\n{b.stderr[-800:]}\ncheck:build exit {c.returncode}\n{c.stdout}\n{c.stderr}'
    io.open(S + r'\l0-break-169b.txt', 'w', encoding='utf8', newline='').write(out)
    print(out[-1800:])
finally:
    for f, b in files.items():
        shutil.copyfile(b, f)
        print('restored', io.open(f, encoding='utf8').read() == io.open(b, encoding='utf8').read())
