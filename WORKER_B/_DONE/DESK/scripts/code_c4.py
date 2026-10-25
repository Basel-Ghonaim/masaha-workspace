import io, os
os.chdir('C:/dev/masaha/app-b')


def sub(p, old, new):
    s = io.open(p, encoding='utf-8', newline='').read()
    assert s.count(old) == 1, (p, old[:60], s.count(old))
    io.open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new))


# shared: the answer
p = 'packages/shared/src/payments/responses.ts'
sub(p, "import type { PAYMENT_METHODS } from './requests.ts';\n",
    "import type { DeskVisit } from '../visits/index.ts';\nimport type { PAYMENT_METHODS } from './requests.ts';\n")
s = io.open(p, encoding='utf-8', newline='').read()
s += """
/**
 * A visit closed by the auto check-out and not fully paid: the visit, what was paid on it, and what
 * is still owed, `null` while it has no charge (unpriced).
 */
export interface UncollectedVisit {
  visit: DeskVisit;
  paidAgorot: number;
  balanceAgorot: number | null;
}
"""
io.open(p, 'w', encoding='utf-8', newline='').write(s)

# visits: the auto-closed reads
p = 'apps/api/src/modules/visits/visits.repository.ts'
sub(p, """    /** Sets a closed visit's charge typed by hand,""", """    /** The space's visits closed by the auto check-out, each with its charge. */
    autoClosedIn(spaceId: number): Promise<{ id: number; chargeAgorot: number | null }[]> {
      return prisma.visit.findMany({
        where: { spaceId, checkoutMethod: 'AUTO' },
        select: { id: true, chargeAgorot: true },
      });
    },

    /**
     * A page of the space's visits closed by the auto check-out, but these, the latest closed
     * first, then by id, and how many there are.
     */
    async autoClosedPage(
      spaceId: number,
      exceptIds: readonly number[],
      { skip, take }: { skip: number; take: number },
    ): Promise<{ rows: DeskVisitRow[]; total: number }> {
      const where = { spaceId, checkoutMethod: 'AUTO' as const, id: { notIn: [...exceptIds] } };
      const [rows, total] = await Promise.all([
        prisma.visit.findMany({
          where,
          select: DESK_VISIT,
          orderBy: [{ checkedOutAt: 'desc' }, { id: 'desc' }],
          skip,
          take,
        }),
        prisma.visit.count({ where }),
      ]);
      return { rows, total };
    },

    /** Sets a closed visit's charge typed by hand,""")

p = 'apps/api/src/modules/visits/visits.service.ts'
sub(p, """    /**
     * Prices a closed visit with no charge,""", """    /** The space's visits closed by the auto check-out, each with its charge (or none). */
    autoClosedIn(spaceId: number): Promise<{ id: number; chargeAgorot: number | null }[]> {
      return repository.autoClosedIn(spaceId);
    },

    /**
     * A page of the space's visits closed by the auto check-out, but these (the settled ones, which
     * `payments` decides), the latest closed first, then by id; and how many there are.
     */
    async autoClosedPage(
      spaceId: number,
      exceptIds: readonly number[],
      query: PaginationQuery,
    ): Promise<{ rows: DeskVisit[]; total: number }> {
      const { rows, total } = await repository.autoClosedPage(spaceId, exceptIds, {
        skip: toSkip(query),
        take: query.limit,
      });
      return { rows: rows.map(toDeskVisit), total };
    },

    /**
     * Prices a closed visit with no charge,""")

# payments: repository, service, controller, routes, index
p = 'apps/api/src/modules/payments/payments.repository.ts'
sub(p, "import type { Tx } from '../../db/index.ts';\n", "import { prisma, type Tx } from '../../db/index.ts';\n")
sub(p, """    /** Inserts the payment; the insert trigger checks it against the visit's charge. */""", """    /** What was paid on each of these visits of the space, voided payments left out; none is absent. */
    async paidFor(spaceId: number, visitIds: readonly number[]): Promise<Map<number, number>> {
      if (visitIds.length === 0) return new Map();
      const groups = await prisma.payment.groupBy({
        by: ['visitId'],
        where: { spaceId, visitId: { in: [...visitIds] }, voidedAt: null },
        _sum: { amountAgorot: true },
      });
      return new Map(
        groups.flatMap(({ visitId, _sum }) =>
          visitId === null ? [] : [[visitId, _sum.amountAgorot ?? 0] as const],
        ),
      );
    },

    /** Inserts the payment; the insert trigger checks it against the visit's charge. */""")

p = 'apps/api/src/modules/payments/payments.service.ts'
sub(p, "import type { VisitPayment } from '@masaha/shared/payments';\n",
    "import type { PaginationQuery } from '@masaha/shared/core';\nimport type { UncollectedVisit, VisitPayment } from '@masaha/shared/payments';\n")
sub(p, "import type { AuditWriter } from '../../shared/audit/index.ts';\n",
    "import type { AuditWriter } from '../../shared/audit/index.ts';\nimport type { VisitsService } from '../visits/index.ts';\nimport { balanceOf } from './balance.ts';\n")
sub(p, """interface Dependencies {
  audit: AuditWriter;
}""", """interface Dependencies {
  audit: AuditWriter;
  visits: VisitsService;
}""")
sub(p, """ * The payment ledger (ADR 0010; docs/backend/conventions.md › The ledger's rules). So far a visit's
 * payment, taken at its check-out. The database owns the ledger's rules: nothing here repeats them.
 */
export function createPaymentsService({ audit }: Dependencies) {""", """ * The payment ledger (ADR 0010; docs/backend/conventions.md › The ledger's rules). So far a visit's
 * payment, taken at its check-out, and the uncollected visits. The database owns the ledger's rules:
 * nothing here repeats them.
 */
export function createPaymentsService({ audit, visits }: Dependencies) {""")
sub(p, """    /** Records a visit's payment,""", """    /**
     * A page of the space's uncollected visits (data model › Uncollected visits; conventions §9,
     * composed reads): `visits` names the ones closed by the auto check-out, with their charges;
     * this ledger sums what was paid on each, voided payments left out, and leaves out the settled
     * ones (balance ≤ 0); `visits` then pages the rest, the unpriced ones included.
     */
    async uncollectedIn(
      spaceId: number,
      query: PaginationQuery,
    ): Promise<{ rows: UncollectedVisit[]; total: number }> {
      const closed = await visits.autoClosedIn(spaceId);
      const paid = await repository.paidFor(
        spaceId,
        closed.map(({ id }) => id),
      );
      const settled = closed.flatMap(({ id, chargeAgorot }) => {
        const balance = balanceOf(chargeAgorot, paid.get(id) ?? 0);
        return balance !== null && balance <= 0 ? [id] : [];
      });
      const { rows, total } = await visits.autoClosedPage(spaceId, settled, query);
      return {
        rows: rows.map((visit) => {
          const paidAgorot = paid.get(visit.id) ?? 0;
          return {
            visit,
            paidAgorot,
            balanceAgorot: balanceOf(visit.charge?.amountAgorot ?? null, paidAgorot),
          };
        }),
        total,
      };
    },

    /** Records a visit's payment,""")

io.open('apps/api/src/modules/payments/payments.controller.ts', 'w', encoding='utf-8', newline='').write("""import type { PaginationQuery } from '@masaha/shared/core';
import type { UncollectedVisit } from '@masaha/shared/payments';
import type { Request, Response } from 'express';

import { spaceOf } from '../../shared/auth/index.ts';
import { buildPaginationMeta, sendSuccess } from '../../shared/http/index.ts';
import type { PaymentsService } from './payments.service.ts';

export function createPaymentsController(service: PaymentsService) {
  return {
    uncollected: async (req: Request, res: Response) => {
      const query = req.query as unknown as PaginationQuery;
      const { rows, total } = await service.uncollectedIn(spaceOf(req).id, query);
      sendSuccess(res, rows satisfies UncollectedVisit[], {
        meta: buildPaginationMeta(query, total),
      });
    },
  };
}

export type PaymentsController = ReturnType<typeof createPaymentsController>;
""")
io.open('apps/api/src/modules/payments/payments.manage.routes.ts', 'w', encoding='utf-8', newline='').write("""import { paginationQuerySchema } from '@masaha/shared/core';
import { Router } from 'express';

import { validate } from '../../shared/validation/index.ts';
import type { PaymentsController } from './payments.controller.ts';

/**
 * The ledger's reads, mounted below `/manage/spaces/:spaceId`, behind that boundary
 * (docs/backend/security.md › Authorization): the staff's, so the boundary is their check.
 */
export function createPaymentsManageRouter(controller: PaymentsController): Router {
  const router = Router();
  router.get('/uncollected-visits', validate(paginationQuerySchema, 'query'), controller.uncollected);
  return router;
}
""")
io.open('apps/api/src/modules/payments/index.ts', 'w', encoding='utf-8', newline='').write("""export { createPaymentsController, type PaymentsController } from './payments.controller.ts';
export { createPaymentsManageRouter } from './payments.manage.routes.ts';
export type { NewVisitPayment } from './payments.repository.ts';
export { createPaymentsService, type PaymentsService } from './payments.service.ts';
""")

p = 'apps/api/src/app.ts'
sub(p, "import { createPaymentsService } from './modules/payments/index.ts';",
    "import {\n  createPaymentsController,\n  createPaymentsManageRouter,\n  createPaymentsService,\n} from './modules/payments/index.ts';")
sub(p, """  const desk = createDeskService({""", """  const payments = createPaymentsService({ audit: writeAudit, visits });
  const desk = createDeskService({""")
sub(p, "    payments: createPaymentsService({ audit: writeAudit }),\n", "    payments,\n")
sub(p, "  manage.use(createVisitsManageRouter(createVisitsController(visits)));\n",
    "  manage.use(createVisitsManageRouter(createVisitsController(visits)));\n  manage.use(createPaymentsManageRouter(createPaymentsController(payments)));\n")
print('ok')
