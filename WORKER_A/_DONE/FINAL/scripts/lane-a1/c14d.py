def edit(p, pairs):
    s = open(p, encoding='utf8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)
R = r'C:\dev\masaha\app-lane-a1'
D = R + r'\docs'
edit(R + r'\apps\api\src\modules\audit\platformEvents.unit.test.ts', [
("""    for (const action of ['user.created', 'user.temporaryPasswordIssued', 'user.suspended']) {""",
 """    for (const action of [
      'user.created',
      'user.temporaryPasswordIssued',
      'user.suspended',
      'user.replaced',
    ]) {"""),
])
edit(D + r'\backend\security.md', [
("""  **While a temporary password is pending, the account has no recovery by email and no Google link.**""",
"""  **An expired pending account that never acted gives its address up** to whoever creates an account at it, by registering or by a first Google sign-in (finding 91, the owner's 91 (a), narrowed by S1): an account whose temporary password is pending **and expired**, with no Google account linked, holding **no active `OWNER` link**, that **never acted** — no audit entry with it as actor, no favourite, no data report. Registration verifies no inbox, so the narrow rule keeps a real account (an owner whose admin-issued password expired, or one used before) from being taken by a stranger who types its address. In the new account's transaction, the space of its reception link is locked, then the account, which is checked again under the lock; its active reception link ends by the system (`space.staffDeactivated`, no actor: the owner's log shows the system), every session ends, it is suspended, its address becomes `replaced-{id}@replaced.invalid` (`.invalid` is reserved, RFC 2606), and `user.replaced` is audited (`before: { email }`, `after: { replacedById }`, no space); then the new account is created as any other. Otherwise registration answers `EMAIL_TAKEN` and Google `GOOGLE_LINK_NOT_ALLOWED`, as before; the owner's staff add and the admin's owner add create for a free address only. 2026-10-29, #PRNUM.

  **While a temporary password is pending, the account has no recovery by email and no Google link.**"""),
])
edit(D + r'\api\api-contract.md', [
("""- **201:** `Session`, for a new `USER`.
- **Errors:** `validation` (422); `conflict` (409) `EMAIL_TAKEN`, with `errors.email = ["not_unique"]`.""",
"""- **201:** `Session`, for a new `USER`. An address held by an expired pending account that never acted and owns no space is freed first, and that account retired ([security › Passwords](../backend/security.md#passwords); 2026-10-29, #PRNUM).
- **Errors:** `validation` (422); `conflict` (409) `EMAIL_TAKEN`, with `errors.email = ["not_unique"]`, for any other holder."""),
("""else a new `USER` without a password ([security.md](../backend/security.md#sign-in-methods)), `created: true` exactly when this sign-in created the account""",
"""else a new `USER` without a password ([security.md](../backend/security.md#sign-in-methods)), also in place of an expired pending account that never acted and owns no space, which is retired ([security › Passwords](../backend/security.md#passwords)); `created: true` exactly when this sign-in created the account"""),
])
edit(D + r'\features\auth.md', [
("- #PRNUM — a replay within the grace gets its token's one successor; the ended tokens and recoveries swept by a timed job; Google's answer says `created`.",
 "- #PRNUM — a replay within the grace gets its token's one successor; the ended tokens and recoveries swept by a timed job; Google's answer says `created`; registration and a first Google sign-in free an expired pending account's address."),
("""- **Whether the reset email may open an account is asked of `users` (`mayRecoverByEmail`)""",
"""- **Registration and a first Google sign-in free an address held by an expired pending account that never acted and owns no space,** in the new account's transaction ([security › Passwords](../backend/security.md#passwords)). `auth` orchestrates it: `users` judges the account by its own rule and retires it, `space-links` ends its reception link by the system, and whether it ever acted is the audit reader's, a level above, passed in as a port. *Why:* the owner's 91 (a), narrowed by S1 so a real account is never taken by a stranger; the audit reader is the one read model that already reads the actor of every entry. 2026-10-29, #PRNUM.
- **Whether the reset email may open an account is asked of `users` (`mayRecoverByEmail`)"""),
])
p = D + r'\architecture\findings\91-an-address-held-by-a-pending-account-is-locked-out-until-the-admin-acts.md'
s = open(p, encoding='utf8').read()
import re
m = re.search(r'\*\*Status:\*\* Open( · \*\*Date:\*\* [0-9-]+)', s)
assert m
s = s.replace(m.group(0), '**Status:** Resolved' + m.group(1) + ' · **Resolved:** 2026-10-29', 1)
s = s.rstrip('\n') + '\n\n**Resolution (#PRNUM):** An expired pending account that never acted and owns no space is replaced by the account its address\'s holder creates (D1.4, S1).\n'
open(p, 'w', encoding='utf8', newline='').write(s)
