def edit(p, pairs):
    s = open(p, encoding='utf8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)
R = r'C:\dev\masaha\app-lane-a1'
U = R + r'\apps\api\src\modules\users\users.service.ts'
edit(U, [
("""/** A person Google has verified (the auth module's Google port). */""",
"""/**
 * Frees an address held by an account its holder may replace (S1), in the caller's transaction,
 * after `users` found the holder replaceable by its own rule: the orchestrator above (`auth`) locks
 * what the replacement changes, checks what `users` cannot see (the links, whether it ever acted),
 * and retires it (`retireReplaced`). The account as it was, or nothing when it may not be replaced.
 */
export type FreeAddress = (holderId: number, tx: Tx) => Promise<Account | undefined>;

/**
 * Whether the account may be replaced by whoever creates an account at its address, by the
 * account's own rule (finding 91, S1): its temporary password is pending and has expired, so no one
 * ever chose a password for it, and no Google account was ever linked. Its links and its footprint
 * are its orchestrator's to check.
 */
export function replaceableHolder(
  holder: { account: Account; googleSubject: string | null },
  now: Date,
): boolean {
  return holder.googleSubject === null && temporaryPasswordExpired(holder.account, now);
}

/** The address a replaced account takes, so its own is free: `.invalid` is reserved (RFC 2606). */
export function replacedEmail(id: number): string {
  return `replaced-${String(id)}@replaced.invalid`;
}

/** A person Google has verified (the auth module's Google port). */"""),
("""    /** A new USER with a password. A taken email is EMAIL_TAKEN. */
    async register({ name, email, password, language }: Registration): Promise<Account> {
      const passwordHash = await hashPassword(password);
      const created = await repository.create({ name, email, passwordHash, language });
      if ('account' in created) return created.account;
      throw AppError.conflict('EMAIL_TAKEN', 'Email taken', { email: ['not_unique'] });
    },""",
"""    /**
     * A new USER with a password, hashed before the transaction. A taken email is EMAIL_TAKEN,
     * unless its holder may be replaced (`free`, S1): it is then retired and the account created in
     * one transaction. The holder is read first, so the insert meets no unique violation, which would
     * end the transaction; a racing registration still meets the unique key, EMAIL_TAKEN too.
     */
    async register(
      { name, email, password, language }: Registration,
      free?: FreeAddress,
    ): Promise<Account> {
      const passwordHash = await hashPassword(password);
      const taken = () =>
        AppError.conflict('EMAIL_TAKEN', 'Email taken', { email: ['not_unique'] });
      return runInTransaction(async (tx) => {
        const replaced = await replaceHolder(email, free, tx);
        if (replaced === null) throw taken();
        const created = await repository.create({ name, email, passwordHash, language }, tx);
        if (!('account' in created)) throw taken();
        if (replaced) await recordReplaced(replaced, created.account.id, tx);
        return created.account;
      });
    },"""),
("""    async accountForGoogle(
      google: GoogleAccount,
      language: Language | undefined,
    ): Promise<{ userId: number; link: boolean; created: boolean }> {""",
"""    async accountForGoogle(
      google: GoogleAccount,
      language: Language | undefined,
      free?: FreeAddress,
    ): Promise<{ userId: number; link: boolean; created: boolean }> {"""),
("""            // Another Google account is already linked to this email's account: never replaced.
            throw AppError.unauthorized('GOOGLE_TOKEN_INVALID', 'Linked to another Google account');
          }
          assertMayLinkGoogle(byEmail.account);""",
"""            // Another Google account is already linked to this email's account: never replaced.
            throw AppError.unauthorized('GOOGLE_TOKEN_INVALID', 'Linked to another Google account');
          }
          // An expired pending account its holder may replace (S1): retired, and the Google
          // account created in its place, in one transaction.
          if (free && replaceableHolder(byEmail, now())) {
            const userId = await runInTransaction(async (tx) => {
              const replaced = await replaceHolder(google.email, free, tx);
              if (!replaced) return undefined;
              const created = await repository.create(googleAccount(google, language), tx);
              if (!('account' in created)) {
                throw AppError.conflict(undefined, 'Account created concurrently');
              }
              await recordReplaced(replaced, created.account.id, tx);
              return created.account.id;
            });
            if (userId !== undefined) return { userId, link: false, created: true };
          }
          assertMayLinkGoogle(byEmail.account);"""),
("""        const parsedName = googleName.safeParse(google.name);
        const created = await repository.create({
          email: google.email,
          name: parsedName.success ? parsedName.data : (google.email.split('@')[0] ?? google.email),
          passwordHash: null,
          googleSubject: google.subject,
          language,
        });""",
"""        const created = await repository.create(googleAccount(google, language));"""),
("""  /** The account, or a 401 when it no longer exists. */""",
"""  /**
   * The holder of `email`, replaced through `free` when it may be (S1): the account as it was;
   * `undefined` when no one holds the address; `null` when its holder keeps it.
   */
  async function replaceHolder(
    email: string,
    free: FreeAddress | undefined,
    tx: Tx,
  ): Promise<Account | null | undefined> {
    const holder = await repository.findByEmail(email, tx);
    if (!holder) return undefined;
    if (!free || !replaceableHolder(holder, now())) return null;
    return (await free(holder.account.id, tx)) ?? null;
  }

  /** The new account `replacedById` took the replaced one's address: audited, with no actor. */
  async function recordReplaced(replaced: Account, replacedById: number, tx: Tx): Promise<void> {
    await audit(
      {
        actorId: null,
        action: 'user.replaced',
        entityType: 'user',
        entityId: replaced.id,
        before: { email: replaced.email },
        after: { replacedById },
      },
      tx,
    );
  }

  /** The account, or a 401 when it no longer exists. */"""),
])
edit(U, [
("""export function createUsersService({""",
"""/** A new Google-only USER: Google's name when it is valid user text, else the email's local part. */
function googleAccount(google: GoogleAccount, language: Language | undefined) {
  const parsedName = googleName.safeParse(google.name);
  return {
    email: google.email,
    name: parsedName.success ? parsedName.data : (google.email.split('@')[0] ?? google.email),
    passwordHash: null,
    googleSubject: google.subject,
    language,
  };
}

export function createUsersService({"""),
("""    get,

    /**
     * Changes the account's global role,""",
"""    get,

    /**
     * The account under its session lock, still replaceable by its own rule (S1): read again under
     * the lock, so a password set or a Google link made meanwhile keeps it. Nothing otherwise.
     */
    async lockReplaceable(id: number, tx: Tx): Promise<Account | undefined> {
      const locked = await lockAccount(id, tx);
      if (!locked) return undefined;
      const googleSubject = await repository.findGoogleSubject(id, tx);
      return replaceableHolder({ account: locked, googleSubject }, now()) ? locked : undefined;
    },

    /**
     * Retires a replaced account, under its session lock, which the caller took: every session
     * ends, it is suspended, and its address becomes `replaced-{id}@replaced.invalid`, so the person
     * who holds the address may create their own (finding 91).
     */
    async retireReplaced(account: Account, tx: Tx): Promise<void> {
      await endSessions(account.id, tx);
      await repository.setSuspendedAt(account.id, now(), tx);
      if ((await repository.setEmail(account.id, replacedEmail(account.id), tx)) === 'taken') {
        throw new Error(`The replaced address of account ${String(account.id)} is taken`);
      }
    },

    /**
     * Changes the account's global role,"""),
])
edit(R + r'\apps\api\src\modules\users\index.ts', [("""  createUsersService,
  type AccountListing,
  type UsersService,""", """  createUsersService,
  type AccountListing,
  type FreeAddress,
  type UsersService,""")])
