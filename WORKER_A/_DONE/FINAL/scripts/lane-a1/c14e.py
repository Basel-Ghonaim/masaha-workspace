def edit(p, pairs):
    s = open(p, encoding='utf8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)
D = r'C:\dev\masaha\app-lane-a1\docs\features'
edit(D + r'\users.md', [
("""- #131 — `GET` and `PATCH /me`: one's own account, its name and language edited and audited.
""", """- #131 — `GET` and `PATCH /me`: one's own account, its name and language edited and audited.
- #PRNUM — an expired pending account that never acted gives its address up: judged by `users`' rule (`replaceableHolder`), re-read under its lock, retired (sessions ended, suspended, its address `replaced-{id}@replaced.invalid`) and audited `user.replaced`.
"""),
("""- **One's own name and language are edited at `PATCH /me`""",
"""- **An expired pending account with no Google account gives its address up to whoever registers it or first signs in with Google at it, when its orchestrator finds it owns no space and never acted** ([security › Passwords](../backend/security.md#passwords)). `users` judges the account's half of the rule, reads it again under its lock, retires it and audits `user.replaced` (no actor, no space, the old address and the new account's id), in the new account's transaction; the address is read before the insert, so the insert meets no unique violation. *Why:* finding 91 (the owner's 91 (a), narrowed by S1). 2026-10-29, #PRNUM.
- **One's own name and language are edited at `PATCH /me`"""),
])
edit(D + r'\audit.md', [
("""- #130 — the platform's settings' saves on the admin's log, their target with no id.
""", """- #130 — the platform's settings' saves on the admin's log, their target with no id.
- #PRNUM — `user.replaced` on the admin's account events; `hasActed`, whether a person is an entry's actor, has a favourite or wrote a data report, for `auth`'s replacement of an expired pending account.
"""),
])
edit(D + r'\space-links.md', [
("""- #90 — the owner's staff: created, listed, deactivated and re-activated; a pending temporary password re-issued, and its handover; the reception links in the admin's users list.
""", """- #90 — the owner's staff: created, listed, deactivated and re-activated; a pending temporary password re-issued, and its handover; the reception links in the admin's users list.
- #PRNUM — a replaced account's reception link ended by the system (`space.staffDeactivated`, no actor), under its space's lock.
"""),
("""- [91](../architecture/findings/91-an-address-held-by-a-pending-account-is-locked-out-until-the-admin-acts.md): an address held by a pending account is locked out until the admin acts.
""", ""),
])
