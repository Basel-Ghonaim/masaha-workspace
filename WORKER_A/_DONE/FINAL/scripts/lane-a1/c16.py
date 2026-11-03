def edit(p, pairs):
    s = open(p, encoding='utf8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)
R = r'C:\dev\masaha\app-lane-a1'
edit(R + r'\packages\shared\src\users\responses.ts', [
("""/** The signed-in user's own account, as its settings read and edit it. */
export interface MyAccount {
  id: number;
  name: string;
  email: string;
  language: Language;
  role: Role;
}""", """/** The signed-in user's own account, as its settings read and edit it. */
export interface MyAccount {
  id: number;
  name: string;
  email: string;
  language: Language;
  role: Role;
  /** It signs in with a password: false for a Google-only account. */
  hasPassword: boolean;
  /** A Google account is linked to it. */
  hasGoogle: boolean;
}"""),
])
U = R + r'\apps\api\src\modules\users'
edit(U + r'\users.mapper.ts', [
("""/** The account as its own settings read it. */
export function toMyAccount({ id, name, email, language, role }: Account): MyAccount {
  return { id, name, email, language, role };
}""", """/** How an account signs in: with a password, with Google, or both. */
export interface SignInMethods {
  hasPassword: boolean;
  hasGoogle: boolean;
}

/** The account as its own settings read it, with how it signs in. */
export function toMyAccount(
  { id, name, email, language, role }: Account,
  { hasPassword, hasGoogle }: SignInMethods,
): MyAccount {
  return { id, name, email, language, role, hasPassword, hasGoogle };
}"""),
])
edit(U + r'\users.repository.ts', [
("""    async hasPassword(id: number, tx: Tx = db): Promise<boolean> {""",
"""    /** How the account signs in, without reading any hash. */
    async findSignInMethods(
      id: number,
      tx: Tx = db,
    ): Promise<{ hasPassword: boolean; hasGoogle: boolean }> {
      const [hasPassword, hasGoogle] = [
        await tx.user.count({ where: { id, passwordHash: { not: null } } }),
        await tx.user.count({ where: { id, googleSubject: { not: null } } }),
      ];
      return { hasPassword: hasPassword === 1, hasGoogle: hasGoogle === 1 };
    },

    async hasPassword(id: number, tx: Tx = db): Promise<boolean> {"""),
])
edit(U + r'\users.service.ts', [
("""    /** The signed-in user's own account, for its settings. */
    async myAccount(userId: number): Promise<MyAccount> {
      return toMyAccount(await get(userId));
    },""", """    /** The signed-in user's own account, for its settings, with how it signs in. */
    async myAccount(userId: number): Promise<MyAccount> {
      const account = await get(userId);
      return toMyAccount(account, await repository.findSignInMethods(userId));
    },"""),
("""        if (Object.keys(after).length === 0) return toMyAccount(account);""",
"""        const methods = await repository.findSignInMethods(userId, tx);
        if (Object.keys(after).length === 0) return toMyAccount(account, methods);"""),
("""        return toMyAccount(edited);""", """        return toMyAccount(edited, methods);"""),
])
