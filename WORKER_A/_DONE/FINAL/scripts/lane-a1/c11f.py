def edit(p, pairs):
    s = open(p, encoding='utf8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)
D = r'C:\dev\masaha\app-lane-a1\docs'
edit(D + r'\backend\security.md', [
("| Rotation grace | A token rotated less than 30 s ago is still honoured: its refresh gets a new token of the same family, so two tabs refreshing together, or a refresh retried after a lost answer, stay signed in |",
 "| Rotation grace | A token rotated less than 30 s ago is still honoured: its refresh gets **the same successor** it got the first time, so two tabs refreshing together, or a refresh retried after a lost answer, stay signed in. A token's successor is named by the token itself: an HMAC-SHA256 of it under a key derived once at start-up from `JWT_SECRET` (HKDF-SHA256, its own label `masaha refresh successor`), so the deployment adds no setting and every instance derives the same key. The first presentation stores the successor's hash; one within the grace finds that row and answers it as it is, adding none; a successor gone with its session answers 401. 2026-10-29, #PRNUM |"),
("This cuts a stolen chain once either holder presents a token rotated more than 30 s ago. It does not hold inside the grace: a copy presented within 30 s of a rotation gets its own successor, and from then on thief and owner each rotate their own branch, which reuse detection never sees, until a logout, a password change or a reset ends the session ([finding 21](../architecture/findings/21-a-token-replayed-within-the-grace-window-starts-its-own-branch.md)) |",
 "This cuts a stolen chain once either holder presents a token rotated more than 30 s ago. Inside the grace a copy gains nothing it can keep apart: it gets the one successor the holder got, so the two share one chain, and the next rotation of either leaves the other holding a token that reuse detection sees ([finding 21](../architecture/findings/21-a-token-replayed-within-the-grace-window-starts-its-own-branch.md), resolved 2026-10-29, #PRNUM) |"),
])
edit(D + r'\features\auth.md', [
("""- **Whether the reset email may open an account is asked of `users` (`mayRecoverByEmail`)""",
 """- **A token presented again within the grace gets the same successor,** an HMAC of it under a key `sessions` is handed, derived at start-up from `JWT_SECRET` ([security › Tokens and cookies](../backend/security.md#tokens-and-cookies)). *Why:* a copy replayed within the window gained a branch of its own that reuse detection never saw ([finding 21](../architecture/findings/21-a-token-replayed-within-the-grace-window-starts-its-own-branch.md)); a key of its own from the one secret adds no setting (S7). 2026-10-29, #PRNUM.
- **Whether the reset email may open an account is asked of `users` (`mayRecoverByEmail`)"""),
("""- #118 — the access token names its session (`sid`); reception's session ends after 15 minutes idle (`SESSION_IDLE`).
""", """- #118 — the access token names its session (`sid`); reception's session ends after 15 minutes idle (`SESSION_IDLE`).
- #PRNUM — a replay within the grace gets its token's one successor.
"""),
])
p = D + r'\architecture\findings\21-a-token-replayed-within-the-grace-window-starts-its-own-branch.md'
s = open(p, encoding='utf8').read()
assert s.count('**Status:** Open · **Date:** 2026-10-02') == 1
s = s.replace('**Status:** Open · **Date:** 2026-10-02', '**Status:** Resolved · **Date:** 2026-10-02 · **Resolved:** 2026-10-29')
s = s.rstrip('\n') + '\n\n**Resolution (#PRNUM):** A token presented again within the grace gets the same successor, an HMAC of it under a key derived from `JWT_SECRET` (D1.1).\n'
open(p, 'w', encoding='utf8', newline='').write(s)
