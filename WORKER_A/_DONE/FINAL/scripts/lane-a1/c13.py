def edit(p, pairs):
    s = open(p, encoding='utf8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)
R = r'C:\dev\masaha\app-lane-a1'
edit(R + r'\apps\api\src\modules\users\users.service.ts', [
("""     * one already linked to it; else the account with its email, which is to be linked (`link`)
     * only where Google is authoritative for the address; else a new USER without a password.""",
"""     * one already linked to it; else the account with its email, which is to be linked (`link`)
     * only where Google is authoritative for the address; else a new USER without a password
     * (`created`)."""),
("""    ): Promise<{ userId: number; link: boolean }> {
      for (let attempt = 0; ; attempt++) {
        const known = await repository.findByGoogleSubject(google.subject);
        if (known) return { userId: known.id, link: false };""",
"""    ): Promise<{ userId: number; link: boolean; created: boolean }> {
      for (let attempt = 0; ; attempt++) {
        const known = await repository.findByGoogleSubject(google.subject);
        if (known) return { userId: known.id, link: false, created: false };"""),
("""            if (byEmail.googleSubject === google.subject) {
              return { userId: byEmail.account.id, link: false };
            }""", """            if (byEmail.googleSubject === google.subject) {
              return { userId: byEmail.account.id, link: false, created: false };
            }"""),
("""          return { userId: byEmail.account.id, link: true };""", """          return { userId: byEmail.account.id, link: true, created: false };"""),
("""        if ('account' in created) return { userId: created.account.id, link: false };""",
 """        if ('account' in created) return { userId: created.account.id, link: false, created: true };"""),
])
edit(R + r'\apps\api\src\modules\auth\auth.service.ts', [
("""    ): Promise<SignedIn & { linked: boolean }> {""", """    ): Promise<SignedIn & { linked: boolean; created: boolean }> {"""),
("""        const { userId, link } = await users.accountForGoogle(profile, language);
        if (!link) return { ...(await signIn(userId)), linked: false };""",
"""        const { userId, link, created } = await users.accountForGoogle(profile, language);
        if (!link) return { ...(await signIn(userId)), linked: false, created };"""),
("""          refreshToken: issued.token,
          linked,
        };""", """          refreshToken: issued.token,
          linked,
          created: false,
        };"""),
])
edit(R + r'\apps\api\src\modules\auth\auth.controller.ts', [
("""      const { session, refreshToken, linked } = await auth.google(""", """      const { session, refreshToken, linked, created } = await auth.google("""),
("""      sendSuccess(res, { ...session, linked } satisfies GoogleSession);""", """      sendSuccess(res, { ...session, linked, created } satisfies GoogleSession);"""),
])
edit(R + r'\packages\shared\src\auth\responses.ts', [
("""/** A Google sign-in's answer: `linked` when it has just joined Google to an existing account. */
export interface GoogleSession extends Session {
  linked: boolean;
}""", """/**
 * A Google sign-in's answer: `linked` when it has just joined Google to an existing account,
 * `created` when this sign-in created the account, so the web welcomes it as a registration.
 */
export interface GoogleSession extends Session {
  linked: boolean;
  created: boolean;
}"""),
])
edit(R + r'\docs\api\api-contract.md', [
("""- **200:** `Session & { linked }`. The account linked to this Google account; else the account with its email, linked now where security allows it (`linked: true`); else a new `USER` without a password ([security.md](../backend/security.md#sign-in-methods)).""",
"""- **200:** `Session & { linked, created }` (`GoogleSession`). The account linked to this Google account; else the account with its email, linked now where security allows it (`linked: true`); else a new `USER` without a password ([security.md](../backend/security.md#sign-in-methods)), `created: true` exactly when this sign-in created the account, so the web welcomes it as a registration (2026-10-29, #PRNUM)."""),
])
edit(R + r'\docs\features\auth.md', [
("- #PRNUM — a replay within the grace gets its token's one successor; the ended tokens and recoveries swept by a timed job.",
 "- #PRNUM — a replay within the grace gets its token's one successor; the ended tokens and recoveries swept by a timed job; Google's answer says `created`."),
])
