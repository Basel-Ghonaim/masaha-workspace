import io

R = 'C:/dev/masaha/app-b/apps/api/src/'


def edit(path, pairs):
    p = R + path
    s = io.open(p, encoding='utf-8', newline='').read()
    for a, b in pairs:
        n = s.count(a)
        assert n == 1, (path, n, a[:70])
        s = s.replace(a, b)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)


edit('modules/subscriptions/closures/closures.service.ts', [
    ("""import {
  EXTENSION_MAX_DAYS,
  type AnnouncementsQuery,
  type AnnouncementsSummary,
  type ExtensionPreview,
  type ManagedAnnouncement,
} from '@masaha/shared/announcements';

import { AppError } from '../../../shared/errors/index.ts';
import { closureSpan, type AnnouncementsService } from '../../announcements/index.ts';
import type { UsersService } from '../../users/index.ts';
import { toExtensionApplied, toManagedAnnouncement } from './closures.mapper.ts';
import { createClosuresRepository } from './closures.repository.ts';

interface Dependencies {
  announcements: AnnouncementsService;
  users: UsersService;
""", """import {
  EXTENSION_MAX_DAYS,
  type AnnouncementsQuery,
  type AnnouncementsSummary,
  type ClosureExtension,
  type ExtendSubscriptionsRequest,
  type ExtensionPreview,
  type ManagedAnnouncement,
} from '@masaha/shared/announcements';

import type { RunInTransaction } from '../../../db/index.ts';
import type { AuditWriter } from '../../../shared/audit/index.ts';
import { can, type Actor, type LoadedSpace } from '../../../shared/auth/index.ts';
import { AppError } from '../../../shared/errors/index.ts';
import { closureSpan, type AnnouncementsService } from '../../announcements/index.ts';
import type { SpacesService } from '../../spaces/index.ts';
import type { UsersService } from '../../users/index.ts';
import { toClosureExtension, toExtensionApplied, toManagedAnnouncement } from './closures.mapper.ts';
import { createClosuresRepository } from './closures.repository.ts';

interface Dependencies {
  runInTransaction: RunInTransaction;
  audit: AuditWriter;
  spaces: SpacesService;
  announcements: AnnouncementsService;
  users: UsersService;
"""),
    (""" * The closures as `subscriptions` sees them (docs/backend/conventions.md §9): the managed
 * announcements list, each closure with the extension of the subscriptions it covered, and the
 * summary of the list's tabs. It composes `announcements`' rows with the extensions it owns; the
 * writes stay `announcements`'.
 */
export function createClosuresService({ announcements, users, now }: Dependencies) {""",
     """ * The closures as `subscriptions` sees them (docs/backend/conventions.md §9): the managed
 * announcements list, each closure with the extension of the subscriptions it covered, and the
 * summary of the list's tabs; a closure's extension, previewed and applied. It composes
 * `announcements`' rows with the extensions it owns; the announcements' writes stay theirs.
 */
export function createClosuresService({
  runInTransaction,
  audit,
  spaces,
  announcements,
  users,
  now,
}: Dependencies) {"""),
    ("""    /**
     * The managed list's counts at `at`,""",
     """    /**
     * Extends the subscriptions a closure covered by the days typed, once per closure, in one
     * transaction and in this order (conventions §13: the space, the closure, the subscriptions by
     * id): the space's lock; `can()` on the links read under it; the extension this key applied, for
     * a retry, answered as it was (another closure's → `conflict`); the closure, locked (else
     * `not_found`); one extended already → `CLOSURE_ALREADY_EXTENDED`; one not started yet →
     * `ANNOUNCEMENT_NOT_STARTED`; its span at now; the covered subscriptions locked, their ends moved
     * in one statement; the extension and its links; its audit entry.
     */
    extend(
      actor: Actor,
      space: LoadedSpace,
      announcementId: number,
      key: string,
      { days }: ExtendSubscriptionsRequest,
    ): Promise<ClosureExtension> {
      return runInTransaction(async (tx) => {
        if (!(await spaces.lock(space.id, tx))) {
          throw AppError.notFound(undefined, 'Space not found');
        }
        const links = await space.linksUnder(tx);
        if (!can(actor, 'subscriptions.extendAfterClosure', { links })) throw AppError.forbidden();
        const recorded = await repository.findByKey(key, tx);
        if (recorded) {
          if (recorded.announcementId !== announcementId) {
            throw AppError.conflict(undefined, 'This idempotency key extended another closure');
          }
          const [applier] = await users.namesFor([recorded.appliedById], tx);
          return toClosureExtension(recorded, applier?.name ?? '');
        }

        const closure = await announcements.lockClosure(space.id, announcementId, tx);
        if (await repository.isExtended(closure.id, tx)) {
          throw AppError.conflict('CLOSURE_ALREADY_EXTENDED');
        }
        const at = now();
        if (closure.startsAt.getTime() > at.getTime()) {
          throw AppError.conflict('ANNOUNCEMENT_NOT_STARTED');
        }
        const ids = await repository.lockCovered(space.id, closureSpan(closure, at), tx);
        await repository.moveEnds(ids, days, at, tx);
        await repository.createExtension(
          { announcementId, days, appliedById: actor.id, key, appliedAt: at },
          ids,
          tx,
        );
        await audit(
          {
            actorId: actor.id,
            action: 'closure.subscriptionsExtended',
            entityType: 'announcement',
            entityId: announcementId,
            spaceId: space.id,
            after: { days, subscriptionIds: ids },
          },
          tx,
        );
        const [applier] = await users.namesFor([actor.id], tx);
        return toClosureExtension(
          { announcementId, days, subscriptions: ids.length, appliedAt: at, appliedById: actor.id },
          applier?.name ?? '',
        );
      });
    },

    /**
     * The managed list's counts at `at`,"""),
])

edit('modules/subscriptions/closures/closures.mapper.ts', [
    ("""import type {
  Announcement,
  ExtensionApplied,
  ManagedAnnouncement,
} from '@masaha/shared/announcements';""",
     """import type {
  Announcement,
  ClosureExtension,
  ExtensionApplied,
  ManagedAnnouncement,
} from '@masaha/shared/announcements';"""),
    ("""/** An announcement of the managed list:""",
     """/** An extension's row, with its applier's name, as the extension's answer shows it. */
export function toClosureExtension(row: ExtensionRow, name: string): ClosureExtension {
  return { announcementId: row.announcementId, ...toExtensionApplied(row, name) };
}

/** An announcement of the managed list:"""),
])

edit('modules/subscriptions/closures/closures.controller.ts', [
    ("""import type {
  AnnouncementsQuery,
  AnnouncementsSummary,
  ExtensionPreview,
  ManagedAnnouncement,
} from '@masaha/shared/announcements';""",
     """import type {
  AnnouncementsQuery,
  AnnouncementsSummary,
  ClosureExtension,
  ExtendSubscriptionsRequest,
  ExtensionPreview,
  ManagedAnnouncement,
} from '@masaha/shared/announcements';"""),
    ("import { spaceOf } from '../../../shared/auth/index.ts';\nimport { buildPaginationMeta, sendSuccess } from '../../../shared/http/index.ts';",
     "import { signedIn, spaceOf } from '../../../shared/auth/index.ts';\nimport {\n  buildPaginationMeta,\n  idempotencyKeyOf,\n  sendSuccess,\n} from '../../../shared/http/index.ts';"),
    ("""      sendSuccess(res, preview satisfies ExtensionPreview);
    },
""", """      sendSuccess(res, preview satisfies ExtensionPreview);
    },

    /** 201 every time, a retry included, with the extension as it was applied. */
    extend: async (req: Request, res: Response) => {
      const { userId, role } = signedIn(req);
      const extension = await service.extend(
        { id: userId, role },
        spaceOf(req),
        parseId(req.params.announcementId),
        idempotencyKeyOf(res),
        req.body as ExtendSubscriptionsRequest,
      );
      sendSuccess(res, extension satisfies ClosureExtension, { status: 201 });
    },
"""),
])

edit('modules/subscriptions/closures/closures.manage.routes.ts', [
    ("import { announcementsQuerySchema } from '@masaha/shared/announcements';\nimport { Router } from 'express';\n\nimport { validate } from '../../../shared/validation/index.ts';",
     "import { announcementsQuerySchema, extendSubscriptionsSchema } from '@masaha/shared/announcements';\nimport { Router } from 'express';\n\nimport { requireCan } from '../../../shared/auth/index.ts';\nimport { requireIdempotencyKey } from '../../../shared/http/index.ts';\nimport { validate } from '../../../shared/validation/index.ts';"),
    ("""closure's extension, which is `subscriptions`' (docs/backend/conventions.md §9). Reads of the
 * space's staff, asking no `can()`.""",
     """closure's extension, which is `subscriptions`' (docs/backend/conventions.md §9). The reads are
 * the space's staff's, asking no `can()`; the extension is the owner's, asked here first, before its
 * key and body are read, and again under the space's lock."""),
    ("  router.get('/:announcementId/extend-subscriptions', controller.preview);\n",
     """  router.get('/:announcementId/extend-subscriptions', controller.preview);
  router.post(
    '/:announcementId/extend-subscriptions',
    requireCan('subscriptions.extendAfterClosure'),
    requireIdempotencyKey,
    validate(extendSubscriptionsSchema),
    controller.extend,
  );
"""),
])

edit('app.ts', [
    ("  const closures = createClosuresService({ announcements, users, now: clock });\n",
     """  const closures = createClosuresService({
    runInTransaction,
    audit: writeAudit,
    spaces,
    announcements,
    users,
    now: clock,
  });
"""),
])
print('ok')
