import os
import re

ROOT = 'C:/dev/masaha/app/apps/web/src/'


def edit(p, old, new):
    path = ROOT + p
    s = open(path, encoding='utf8').read()
    assert s.count(old) == 1, (p, old[:70])
    s = s.replace(old, new)
    open(path, 'w', encoding='utf8', newline='').write(s)


def write(p, text):
    path = ROOT + p
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf8', newline='').write(text)


# Arabic site.account: add settings after reports.
p = ROOT + 'shared/copy/arabic/site.ts'
s = open(p, encoding='utf8').read()
m = re.search(r"(  account: \{\n(?:    .*\n)*?    reports: '[^']*',\n)", s)
assert m, 'account block'
s = s.replace(m.group(1), m.group(1) + "    settings: 'إعدادات حسابي',\n", 1)
open(p, 'w', encoding='utf8', newline='').write(s)

for name, const, about in (
    ('overview', 'OVERVIEW', "The owner's and the admin's overviews (screens 12 and 25): U5's words."),
    ('finance', 'FINANCE', "Finance (screen 19), the owner's alone: U5's words."),
    ('audit', 'AUDIT', "The audit logs, the owner's and the admin's (O13, screen 31): U6's words."),
):
    write(f'shared/copy/english/{name}.ts', f"""/** {about} */
export const {const} = {{}} as const;
""")
    write(f'shared/copy/arabic/{name}.ts', f"""import type {{ Catalogue }} from '../shape';

export const {const} = {{}} satisfies Catalogue['{name}'];
""")

for lang in ('english', 'arabic'):
    f = f'shared/copy/{lang}/index.ts'
    edit(f, "import { AUTH } from './auth';", "import { AUDIT } from './audit';\nimport { AUTH } from './auth';")
    edit(f, "import { FAVORITES } from './favorites';", "import { FAVORITES } from './favorites';\nimport { FINANCE } from './finance';")
    edit(f, "import { OCCUPANCY } from './occupancy';", "import { OCCUPANCY } from './occupancy';\nimport { OVERVIEW } from './overview';")
    edit(f, "  auth: AUTH,", "  audit: AUDIT,\n  auth: AUTH,")
    edit(f, "  favorites: FAVORITES,", "  favorites: FAVORITES,\n  finance: FINANCE,")
    edit(f, "  occupancy: OCCUPANCY,", "  occupancy: OCCUPANCY,\n  overview: OVERVIEW,")
print('done')
