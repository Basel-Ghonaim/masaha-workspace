import io, os
os.chdir('C:/dev/masaha/app-b')


def sub(p, old, new):
    s = io.open(p, encoding='utf-8', newline='').read()
    assert s.count(old) == 1, (p, old[:60], s.count(old))
    io.open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new))


# shared: the price request, in visits; desk's typed charge reuses it
p = 'packages/shared/src/visits/requests.ts'
sub(p, "import { PRICE_AUDIENCES } from '../spaces/index.ts';", "import { PRICE_AUDIENCES, PRICE_MAX_AGOROT } from '../spaces/index.ts';")
sub(p, "export const VISITOR_NAME_MAX_LENGTH = 60;\n", "export const VISITOR_NAME_MAX_LENGTH = 60;\nexport const CHARGE_REASON_MAX_LENGTH = 200;\n")
s = io.open(p, encoding='utf-8', newline='').read()
s += """
/**
 * A visit's charge typed by hand, with why: whole agorot from 1 to a price's largest, and a reason
 * of 1–200 characters. The desk's check-out sends it for a visit with no rate; the owner prices an
 * unpriced visit with it.
 */
export const priceVisitSchema = z.object({
  amountAgorot: z.number().int().min(1).max(PRICE_MAX_AGOROT),
  reason: textSchema(1, CHARGE_REASON_MAX_LENGTH),
});
export type PriceVisitRequest = z.infer<typeof priceVisitSchema>;
"""
io.open(p, 'w', encoding='utf-8', newline='').write(s)

p = 'packages/shared/src/desk/requests.ts'
sub(p, "import { paymentSchema, PAYMENT_MAX_AGOROT } from '../payments/index.ts';\nimport { VISITOR_NAME_MAX_LENGTH } from '../visits/index.ts';",
    "import { paymentSchema } from '../payments/index.ts';\nimport { priceVisitSchema, VISITOR_NAME_MAX_LENGTH } from '../visits/index.ts';")
sub(p, "export const CHARGE_REASON_MAX_LENGTH = 200;\n\n", "")
sub(p, """  charge: z
    .object({
      amountAgorot: z.number().int().min(1).max(PAYMENT_MAX_AGOROT),
      reason: textSchema(1, CHARGE_REASON_MAX_LENGTH),
    })
    .optional(),""", "  charge: priceVisitSchema.optional(),")

# the code
sub('packages/shared/src/core/errors.ts', "  'VISIT_NOT_PRICED',\n", "  'VISIT_NOT_PRICED',\n  // the visit's charge typed later (visits)\n  'VISIT_ALREADY_PRICED',\n")
sub('apps/web/src/shared/copy/arabic/errors.ts', "  VISIT_ALREADY_CLOSED:", "  VISIT_ALREADY_PRICED: 'لهذه الزيارة سعر بالفعل.',\n  VISIT_ALREADY_CLOSED:")
sub('apps/web/src/shared/copy/english/errors.ts', "  VISIT_ALREADY_CLOSED:", "  VISIT_ALREADY_PRICED: 'This visit already has a price.',\n  VISIT_ALREADY_CLOSED:")

# repository
p = 'apps/api/src/modules/visits/visits.repository.ts'
sub(p, """    /** The space's open visits, the earliest checked in first, then by id. */
    openIn(""", """    /**
     * A page of the space's closed visits with no charge, the latest closed first, then by id, and
     * how many there are.
     */
    async unpricedIn(
      spaceId: number,
      { skip, take }: { skip: number; take: number },
    ): Promise<{ rows: DeskVisitRow[]; total: number }> {
      const where = { spaceId, checkedOutAt: { not: null }, chargeAgorot: null };
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

    /** Sets a closed visit's charge typed by hand, with who typed it and why. */
    price(
      visitId: number,
      { amountAgorot, typedById, reason }: { amountAgorot: number; typedById: number; reason: string },
      tx: Tx,
    ): Promise<DeskVisitRow> {
      return tx.visit.update({
        where: { id: visitId },
        data: {
          chargeAgorot: amountAgorot,
          chargeSetById: typedById,
          chargeReason: reason,
          roundingRule: null,
          roundingMinutes: null,
          capApplied: null,
        },
        select: DESK_VISIT,
      });
    },

    /** The space's open visits, the earliest checked in first, then by id. */
    openIn(""")

# service
p = 'apps/api/src/modules/visits/visits.service.ts'
sub(p, """import type { SpaceSettings } from '@masaha/shared/space-settings';
import type {
  CheckInVisitRequest,
  DeskVisit,
  QuotedVisit,""", """import type { PaginationQuery } from '@masaha/shared/core';
import type { SpaceSettings } from '@masaha/shared/space-settings';
import type {
  CheckInVisitRequest,
  DeskVisit,
  PriceVisitRequest,
  QuotedVisit,""")
sub(p, "import { AppError } from '../../shared/errors/index.ts';\n", "import { AppError } from '../../shared/errors/index.ts';\nimport { toSkip } from '../../shared/http/index.ts';\n")
sub(p, """    /** The space's open visits, the earliest checked in first, then by id. */
    openIn(spaceId: number, tx?: Tx)""", """    /**
     * A page of the space's closed visits with no charge, for the owner to price: the latest closed
     * first, then by id; and how many there are. Read without a lock.
     */
    async unpricedIn(
      spaceId: number,
      query: PaginationQuery,
    ): Promise<{ rows: DeskVisit[]; total: number }> {
      const { rows, total } = await repository.unpricedIn(spaceId, {
        skip: toSkip(query),
        take: query.limit,
      });
      return { rows: rows.map(toDeskVisit), total };
    },

    /**
     * Prices a closed visit with no charge, in one transaction and in this order: the space's lock;
     * `can()` on the links read under it, the staff's, then `prices.typeByHand` by the space's
     * switch; the visit's row (`FOR UPDATE`), not the space's → 404, still open → 409, already
     * charged → `VISIT_ALREADY_PRICED`; its charge typed with who typed it and why, audited
     * `visit.priced`.
     */
    price(
      actor: Actor,
      space: LoadedSpace,
      visitId: number,
      { amountAgorot, reason }: PriceVisitRequest,
    ): Promise<DeskVisit> {
      return runInTransaction(async (tx) => {
        if (!(await spaces.lock(space.id, tx))) {
          throw AppError.notFound(undefined, 'Space not found');
        }
        const links = await space.linksUnder(tx);
        if (!can(actor, 'attendance.record', { links })) throw AppError.forbidden();
        const { receptionMayTypePrices } = await spaceSettings.read(space.id, tx);
        if (!can(actor, 'prices.typeByHand', { links, receptionMayTypePrices })) {
          throw AppError.forbidden('PRICE_TYPING_NOT_ALLOWED');
        }
        const locked = await repository.lockIn(space.id, visitId, tx);
        if (!locked) throw AppError.notFound(undefined, 'Visit not found');
        if (locked.checkedOutAt === null) {
          throw AppError.conflict(undefined, 'An open visit is priced at its check-out');
        }
        if (locked.chargeAgorot !== null) throw AppError.conflict('VISIT_ALREADY_PRICED');

        const row = await repository.price(visitId, { amountAgorot, typedById: actor.id, reason }, tx);
        await audit(
          {
            actorId: actor.id,
            action: 'visit.priced',
            entityType: 'visit',
            entityId: visitId,
            spaceId: space.id,
            after: { chargeAgorot: amountAgorot, reason },
          },
          tx,
        );
        return toDeskVisit(row);
      });
    },

    /** The space's open visits, the earliest checked in first, then by id. */
    openIn(spaceId: number, tx?: Tx)""")

# controller and routes
p = 'apps/api/src/modules/visits/visits.controller.ts'
sub(p, "import type { QuotedVisit, VisitTerms } from '@masaha/shared/visits';", "import type { PaginationQuery } from '@masaha/shared/core';\nimport type { DeskVisit, PriceVisitRequest, QuotedVisit, VisitTerms } from '@masaha/shared/visits';")
sub(p, "import { sendSuccess } from '../../shared/http/index.ts';", "import { buildPaginationMeta, sendSuccess } from '../../shared/http/index.ts';")
sub(p, """      sendSuccess(res, terms satisfies VisitTerms);
    },
""", """      sendSuccess(res, terms satisfies VisitTerms);
    },

    unpriced: async (req: Request, res: Response) => {
      const query = req.query as unknown as PaginationQuery;
      const { rows, total } = await service.unpricedIn(spaceOf(req).id, query);
      sendSuccess(res, rows satisfies DeskVisit[], { meta: buildPaginationMeta(query, total) });
    },

    price: async (req: Request, res: Response) => {
      const { userId, role } = signedIn(req);
      const visit = await service.price(
        { id: userId, role },
        spaceOf(req),
        parseId(req.params.visitId),
        req.body as PriceVisitRequest,
      );
      sendSuccess(res, visit satisfies DeskVisit);
    },
""")
p = 'apps/api/src/modules/visits/visits.manage.routes.ts'
sub(p, "import { Router } from 'express';\n", "import { paginationQuerySchema } from '@masaha/shared/core';\nimport { priceVisitSchema } from '@masaha/shared/visits';\nimport { Router } from 'express';\n\nimport { requireCan } from '../../shared/auth/index.ts';\nimport { validate } from '../../shared/validation/index.ts';\n")
sub(p, """/**
 * The visits' reads, mounted below `/manage/spaces/:spaceId`, behind that boundary
 * (docs/backend/security.md › Authorization): the staff's, so the boundary is their check.
 */""", """/**
 * The visits' routes, mounted below `/manage/spaces/:spaceId`, behind that boundary
 * (docs/backend/security.md › Authorization): the reads are the staff's, so the boundary is their
 * check; the pricing asks `can()` first, before its body is read.
 */""")
sub(p, "  router.get('/visit-terms', controller.terms);\n", """  router.get('/visit-terms', controller.terms);
  router.get('/unpriced-visits', validate(paginationQuerySchema, 'query'), controller.unpriced);
  router.put(
    '/visits/:visitId/charge',
    requireCan('attendance.record'),
    validate(priceVisitSchema),
    controller.price,
  );
""")
print('ok')
