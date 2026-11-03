import io
import os

os.chdir(r'C:\dev\masaha\app-b\apps\api\src')


def edit(path, reps):
    s = io.open(path, encoding='utf-8', newline='').read()
    for a, b in reps:
        assert s.count(a) == 1, (path, a[:90])
        s = s.replace(a, b)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)


edit('modules/audit/audit.mapper.ts', [
("""import type { AuditActor, AuditEntityType, AuditEntry } from '@masaha/shared/audit';

import type { ActorRow, AuditRow } from './audit.repository.ts';
""", """import type {
  AuditActor,
  AuditEntityType,
  AuditEntry,
  PlatformAuditEntry,
} from '@masaha/shared/audit';

import type { ActorRow, AuditRow, PlatformAuditRow } from './audit.repository.ts';
"""),
("""function toActor(""", """/** An entry as the admin's log shows it, with the space it names. */
export function toPlatformAuditEntry(row: PlatformAuditRow): PlatformAuditEntry {
  return { ...toAuditEntry(row), space: row.space };
}

function toActor("""),
])

edit('modules/audit/audit.service.ts', [
("""import type { AuditActor, AuditEntry, SpaceAuditQuery } from '@masaha/shared/audit';
""", """import type {
  AuditActor,
  AuditEntry,
  PlatformAuditEntry,
  PlatformAuditQuery,
  SpaceAuditQuery,
} from '@masaha/shared/audit';
"""),
("""import { toAuditActor, toAuditEntry } from './audit.mapper.ts';""",
 """import { toAuditActor, toAuditEntry, toPlatformAuditEntry } from './audit.mapper.ts';"""),
("""      return { rows: rows.map(toAuditEntry), total, actors: actors.map(toAuditActor) };
    },
""", """      return { rows: rows.map(toAuditEntry), total, actors: actors.map(toAuditActor) };
    },

    /**
     * A page of the admin's log: the platform's events only, by the default-deny list
     * (`platformEvents.ts`), of every space and of none, each with its space; filtered as the
     * owner's, the actor a person's id; with the period's actors.
     */
    async platformLog({
      period,
      q,
      actions,
      actor,
      page,
      limit,
    }: PlatformAuditQuery): Promise<{
      rows: PlatformAuditEntry[];
      total: number;
      actors: AuditActor[];
    }> {
      const { rows, total, actors } = await repository.platformLog(
        { since: auditPeriodStart(period, now()), q, actions, actor },
        { skip: toSkip({ page, limit }), take: limit },
      );
      return { rows: rows.map(toPlatformAuditEntry), total, actors: actors.map(toAuditActor) };
    },
"""),
])

edit('modules/audit/audit.controller.ts', [
("""import type { AuditEntry, AuditMeta, SpaceAuditQuery } from '@masaha/shared/audit';""",
 """import type {
  AuditEntry,
  AuditMeta,
  PlatformAuditEntry,
  PlatformAuditQuery,
  SpaceAuditQuery,
} from '@masaha/shared/audit';"""),
("""      sendSuccess(res, rows satisfies AuditEntry[], { meta });
    },
""", """      sendSuccess(res, rows satisfies AuditEntry[], { meta });
    },

    /** 200 with a page of the platform's events and its `meta`, with the period's actors. */
    platformLog: async (req: Request, res: Response) => {
      const query = req.query as unknown as PlatformAuditQuery;
      const { rows, total, actors } = await service.platformLog(query);
      const meta: AuditMeta = { ...buildPaginationMeta(query, total), actors };
      sendSuccess(res, rows satisfies PlatformAuditEntry[], { meta });
    },
"""),
])

io.open('modules/audit/audit.admin.routes.ts', 'w', encoding='utf-8', newline='').write(
"""import { platformAuditQuerySchema } from '@masaha/shared/audit';
import { Router } from 'express';

import { validate } from '../../shared/validation/index.ts';
import type { AuditController } from './audit.controller.ts';

/**
 * The platform's audit log, mounted at `/audit-log` inside `/admin`, behind `requireRole('ADMIN')`
 * (docs/backend/security.md › Authorization): the platform's events only, by the default-deny list.
 */
export function createAuditAdminRouter(controller: AuditController): Router {
  const router = Router();
  router.get('/', validate(platformAuditQuerySchema, 'query'), controller.platformLog);
  return router;
}
""")

edit('modules/audit/index.ts', [
("""export { createAuditController, type AuditController } from './audit.controller.ts';
""", """export { createAuditAdminRouter } from './audit.admin.routes.ts';
export { createAuditController, type AuditController } from './audit.controller.ts';
"""),
])

edit('app.ts', [
("""import {
  createAuditController,
  createAuditManageRouter,""", """import {
  createAuditAdminRouter,
  createAuditController,
  createAuditManageRouter,"""),
("""  admin.use('/data-reports', createDataReportsAdminRouter(dataReportsController));
""", """  admin.use('/data-reports', createDataReportsAdminRouter(dataReportsController));
  admin.use('/audit-log', createAuditAdminRouter(auditController));
"""),
])
print('ok')
