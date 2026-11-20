"""Commit 2 (C3) edits: a link in running text is underlined at rest. newline='' keeps line endings."""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
WEB = ROOT / 'apps' / 'web' / 'src'


def edit(path, old, new, count=1):
    with open(path, encoding='utf-8', newline='') as f:
        s = f.read()
    n = s.count(old)
    if n != count:
        raise SystemExit(f'{path}: expected {count} occurrence(s), found {n}: {old[:80]!r}')
    s = s.replace(old, new)
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(s)
    print('edited', path.relative_to(ROOT), f'({count})')


edit(WEB / 'shared/design-system/components/actions/Button/Button.tsx',
     "link: 'text-primary underline-offset-4 hover:underline',",
     "link: 'text-primary underline underline-offset-4',")

INK_LINK = 'className="text-primary"'
UNDERLINED = 'className="text-primary underline underline-offset-4"'
edit(WEB / 'pages/site/auth/RegisterPage.tsx', INK_LINK, UNDERLINED, count=2)
edit(WEB / 'pages/site/public/about/AboutPage.tsx',
     '<a href={`#${CONTACT_ANCHOR}`} className="text-primary">',
     '<a href={`#${CONTACT_ANCHOR}`} className="text-primary underline underline-offset-4">')
edit(WEB / 'pages/site/shell/SiteFooter.tsx', INK_LINK, UNDERLINED, count=4)
edit(WEB / 'pages/showcase/sections/fields/FieldSection.tsx',
     'className="text-caption text-primary underline-offset-4 hover:underline"',
     'className="text-caption text-primary underline underline-offset-4"')
