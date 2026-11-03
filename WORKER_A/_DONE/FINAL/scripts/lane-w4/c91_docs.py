import re
R = r'C:\dev\masaha\app-lane-w4'
def edit(rel, pairs):
    p = R + '\' + rel
    s = open(p, encoding='utf8', newline='').read()
    for a, b in pairs:
        assert s.count(a) == 1, (rel, a[:60])
        s = s.replace(a, b)
    open(p, 'w', encoding='utf8', newline='').write(s)

edit(r'docs\features\users.md', [
 ("- **The new operations take their own folders** (`suspend/`, `issue-password/`, `account-actions/`), the older flat files left alone ([finding 82](../architecture/findings/82-the-users-feature-keeps-several-operations-flat.md)). 2026-10-19, #93.",
  "- **The new operations take their own folders** (`suspend/`, `issue-password/`, `account-actions/`), the older flat files left alone ([finding 82](../architecture/findings/82-the-users-feature-keeps-several-operations-flat.md)). 2026-10-19, #93.\n- **Every operation keeps its own folder, the older ones moved too** (`account/`, `account-menu/`, `password-change/`, `forced-change/`, `sign-out/`), with no change of behaviour; `useRefreshAdmin` stays at the top of `hooks/`, as in `spaces` and `space-links`, since several operations share it. *Why:* architecture §3's rule, and the account's settings add four operations ([finding 82](../architecture/findings/82-the-users-feature-keeps-several-operations-flat.md)). 2026-10-29, #PRNUM."),
 ("- **Web:** `apps/web/src/features/users/`, entry `index.ts`: `AccountMenu`, `AccountMenuSection`, `CompactAccountMenu`, `SignOutButton`, `ForcedPasswordChangeForm`, and `TemporaryPasswordDialog`",
  "- **Web:** `apps/web/src/features/users/`, entry `index.ts`, one folder per operation: the account's menus (`AccountMenu`, `AccountMenuSection`, `CompactAccountMenu`, `DrawerAccountMenu`) in `components/account-menu/`, with `useAccount` in `hooks/account/`; `SignOutButton` in `components/sign-out/`, with `useSignOutAction` in `hooks/sign-out/`; `ForcedPasswordChangeForm` in `components/forced-change/`, with its hook in `hooks/forced-change/` and the change's write in `hooks/password-change/`; and `TemporaryPasswordDialog`"),
 ("## Open findings\n\n- [82. The users feature keeps several operations flat](../architecture/findings/82-the-users-feature-keeps-several-operations-flat.md) — the new dialog takes `temporary-password/` folders; the older files are left alone.\n",
  "## Open findings\n\nNone.\n"),
 ("- 2026-10-28, #129 — the site's account menu and its phone section link «المفضّلة» and «بلاغاتي».",
  "- 2026-10-28, #129 — the site's account menu and its phone section link «المفضّلة» and «بلاغاتي».\n- 2026-10-29, #PRNUM — one folder per operation ([finding 82](../architecture/findings/82-the-users-feature-keeps-several-operations-flat.md))."),
])
edit(r'docs\architecture\findings\82-the-users-feature-keeps-several-operations-flat.md', [
 ("**Status:** Open · **Date:** 2026-10-18", "**Status:** Resolved · **Date:** 2026-10-18 · **Resolved:** 2026-10-29"),
 ("shape for a capability this small.", "shape for a capability this small.\n\n**Resolution (#PRNUM):** The users feature keeps one folder per operation (D9.1)."),
])
