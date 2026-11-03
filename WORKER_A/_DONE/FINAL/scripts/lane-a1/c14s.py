def edit(p, pairs):
    s = open(p, encoding='utf8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)
R = r'C:\dev\masaha\app-lane-a1'
A = R + r'\apps\api\src'
# space-links service
edit(A + r'\modules\space-links\space-links.service.ts', [
("""import type { Tx } from '../../db/index.ts';
import type { SpaceManagerRole } from '../../generated/prisma/enums.ts';""",
"""import type { Tx } from '../../db/index.ts';
import type { SpaceManagerRole } from '../../generated/prisma/enums.ts';
import type { AuditWriter } from '../../shared/audit/index.ts';"""),
("""interface Dependencies {
  repository?: SpaceLinksRepository;""",
"""interface Dependencies {
  /** The audit writer: a reception link ended by the system (a replaced account's). */
  audit: AuditWriter;
  /** The one clock (conventions §11): when such a link ends. */
  now: () => Date;
  repository?: SpaceLinksRepository;"""),
("""export function createSpaceLinksService({
  repository = createSpaceLinksRepository(),
  spaces = createSpacesService(),
  lookups = createLookupsService(),
}: Dependencies = {}) {""",
"""export function createSpaceLinksService({
  audit,
  now,
  repository = createSpaceLinksRepository(),
  spaces = createSpacesService(),
  lookups = createLookupsService(),
}: Dependencies) {"""),
("""    /**
     * The links loader of the space routes""",
"""    /**
     * Locks the space of the user's reception link, active or not, if they have one (one desk per
     * person, finding 84): a link change takes the space's lock before the person's (conventions
     * §13). The space's id, or nothing.
     */
    async lockReceptionSpaceOf(userId: number, tx: Tx): Promise<number | null> {
      const spaceId = await repository.findReceptionSpaceOf(userId, tx);
      if (spaceId === null) return null;
      return (await spaces.lock(spaceId, tx)) ? spaceId : null;
    },

    /** Whether the user holds an active OWNER link, a soft-deleted space's included. */
    async ownsASpace(userId: number, tx: Tx): Promise<boolean> {
      return (await repository.countOwnerLinks(userId, tx)) > 0;
    },

    /**
     * Ends the user's active reception link at the space, by the system: a replaced account's
     * (finding 91). Under the space's lock and the person's, which the caller took; audited
     * `space.staffDeactivated` with no actor, so the owner's log shows the system ended it.
     */
    async endReceptionBySystem(spaceId: number, userId: number, tx: Tx): Promise<void> {
      const link = await repository.findReceptionLink(spaceId, userId, tx);
      if (!link || link.deactivatedAt !== null) return;
      await repository.deactivateReceptionLink(spaceId, userId, now(), tx);
      await audit(
        {
          actorId: null,
          action: 'space.staffDeactivated',
          entityType: 'space',
          entityId: spaceId,
          spaceId,
          before: { userId, isActive: true },
          after: { userId, isActive: false },
        },
        tx,
      );
    },

    /**
     * The links loader of the space routes"""),
])
edit(A + r'\app.ts', [("  const spaceLinks = createSpaceLinksService({ spaces, lookups });",
 "  const spaceLinks = createSpaceLinksService({ audit: writeAudit, now: clock, spaces, lookups });")])
# audit read model: hasActed
edit(A + r'\modules\audit\audit.service.ts', [
("""import { toSkip } from '../../shared/http/index.ts';""",
"""import type { Tx } from '../../db/index.ts';
import { toSkip } from '../../shared/http/index.ts';"""),
("""      return { rows: rows.map(toPlatformAuditEntry), total, actors: actors.map(toAuditActor) };
    },
  };""",
"""      return { rows: rows.map(toPlatformAuditEntry), total, actors: actors.map(toAuditActor) };
    },

    /**
     * Whether the person ever acted on the platform (finding 91, S1): an audit entry with them as
     * its actor, a favourite, or a data report they wrote. In the caller's transaction.
     */
    hasActed(userId: number, tx: Tx): Promise<boolean> {
      return repository.hasActed(userId, tx);
    },
  };"""),
])
edit(A + r'\modules\audit\audit.repository.ts', [
("""import { prisma } from '../../db/index.ts';""", """import { prisma, type Tx } from '../../db/index.ts';"""),
("""export function createAuditRepository() {
  return {""",
"""export function createAuditRepository() {
  return {
    /**
     * Whether the user is the actor of an audit entry, has a favourite or wrote a data report: one
     * statement, each an indexed lookup (R7: a read model reads other modules' tables).
     */
    async hasActed(userId: number, tx: Tx = prisma): Promise<boolean> {
      const [row] = await tx.$queryRaw<{ acted: boolean }[]>`
        SELECT EXISTS (SELECT 1 FROM audit_logs WHERE actor_id = ${userId})
          OR EXISTS (SELECT 1 FROM favorites WHERE user_id = ${userId})
          OR EXISTS (SELECT 1 FROM data_reports WHERE user_id = ${userId}) AS acted`;
      return row?.acted ?? false;
    },
"""),
])
# platform account actions
edit(A + r'\modules\audit\platformEvents.ts', [("""  'user.temporaryPasswordHandedOver',
  'user.emailChanged',
] as const;""", """  'user.temporaryPasswordHandedOver',
  'user.emailChanged',
  'user.replaced',
] as const;""")])
edit(R + r'\packages\shared\src\audit\actions.ts', [("""  'user.profileEdited',
  'user.roleChanged',""", """  'user.profileEdited',
  'user.replaced',
  'user.roleChanged',""")])
# auth
edit(A + r'\modules\auth\auth.service.ts', [
("""  /** The timer (conventions §11): resolves once `ms` have passed. */
  wait: (ms: number) => Promise<void>;
}""", """  /** The timer (conventions §11): resolves once `ms` have passed. */
  wait: (ms: number) => Promise<void>;
  /**
   * Whether the person ever acted on the platform (`audit`'s read model, a level above): an
   * account that did is never replaced (S1). A port, wired in the composition root.
   */
  hasActed: (userId: number, tx: Tx) => Promise<boolean>;
}"""),
("""  webOrigin,
  wait,
}: Dependencies) {""", """  webOrigin,
  wait,
  hasActed,
}: Dependencies) {"""),
("""  /** Opens a session for the user, under their session lock (conventions §13). */""",
"""  /**
   * Frees an address its holder may lose (finding 91, S1), in the caller's transaction: an expired
   * pending account (`users`' rule) that holds no active OWNER link and never acted. The space of
   * its reception link is locked first, then the account, which is checked again under the lock;
   * its reception link ends by the system, and it is retired. The account as it was, or nothing.
   */
  const freeAddress: FreeAddress = async (holderId, tx) => {
    const spaceId = await spaceLinks.lockReceptionSpaceOf(holderId, tx);
    const account = await users.lockReplaceable(holderId, tx);
    if (!account) return undefined;
    if ((await spaceLinks.ownsASpace(holderId, tx)) || (await hasActed(holderId, tx))) {
      return undefined;
    }
    if (spaceId !== null) await spaceLinks.endReceptionBySystem(spaceId, holderId, tx);
    await users.retireReplaced(account, tx);
    return account;
  };

  /** Opens a session for the user, under their session lock (conventions §13). */"""),
("""        signIn((await users.register(request)).id),""", """        signIn((await users.register(request, freeAddress)).id),"""),
("""        const { userId, link, created } = await users.accountForGoogle(profile, language);""",
"""        const { userId, link, created } = await users.accountForGoogle(
          profile,
          language,
          freeAddress,
        );"""),
])
edit(A + r'\app.ts', [("""    emailSender: createCappedEmailSender(email, { limiter, logger }),
    webOrigin,
    wait,
  });""", """    emailSender: createCappedEmailSender(email, { limiter, logger }),
    webOrigin,
    wait,
    // Whether a person ever acted is the audit reader's (L5), a level above auth: passed in.
    hasActed: (userId: number, tx: Tx) => auditLog.hasActed(userId, tx),
  });""")])
