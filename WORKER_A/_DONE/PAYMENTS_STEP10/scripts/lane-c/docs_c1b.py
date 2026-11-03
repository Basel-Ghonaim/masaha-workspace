"""Commit 1's documents: users.md, architecture §2, overview, foundation §13."""
import sys

ROOT = r'C:\dev\masaha\app-lane-c\docs'


def edit(path, old, new):
    full = ROOT + '\\' + path
    with open(full, encoding='utf8', newline='') as f:
        text = f.read()
    if text.count(old) != 1:
        sys.exit(f'{path}: anchor found {text.count(old)} times: {old[:70]}')
    text = text.replace(old, new, 1)
    with open(full, 'w', encoding='utf8', newline='') as f:
        f.write(text)


U = 'features\\users.md'
edit(U, "**The account menu** shows the name's first word, an initial as the avatar, and the email. It leads the admin, and anyone with an active space link, to the dashboard, by a path the page passes. The phone menu shows the same account as a section; the dashboard's top bar shows the avatar alone.",
     "**The account menu** shows the name's first word, an initial as the avatar, and the email. On the site it links the account's pages the shell passes — «بلاغاتي» — after the name (P4); the dashboard's passes none. It leads the admin, and anyone with an active space link, to the dashboard, by a path the page passes. The phone menu shows the same account as a section, with the same links; the dashboard's top bar shows the avatar alone.")
edit(U, """- **A "password saved" toast follows the forced change.** 2026-10-06, #42.
""", """- **A "password saved" toast follows the forced change.** 2026-10-06, #42.
- **The site's account menu links the account's pages** (P4), passed by the site's shell as `links` and worded by `useAccount`; the dashboard's menu passes none. *Why:* the account's pages are the site's, and `users` knows no route. 2026-10-28, #PRNUM.
""")
edit(U, """- #99 — the one-time dialog's handover recorded through its caller's write, the admin's or a space's; the forced change's line names no issuer.""",
     """- #99 — the one-time dialog's handover recorded through its caller's write, the admin's or a space's; the forced change's line names no issuer.
- 2026-10-28, #PRNUM — the site's account menu and its phone section link «بلاغاتي».""")
print('ok')
