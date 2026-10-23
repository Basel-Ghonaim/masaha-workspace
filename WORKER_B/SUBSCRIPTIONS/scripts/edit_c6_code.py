import os
os.chdir(r'C:\dev\masaha\app-b')

def rep(p, old, new, count=1):
    s = open(p, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (p, old, s.count(old))
    s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)

def write(p, text):
    open(p, 'w', encoding='utf-8', newline='').write(text)

# shared: the requests
write('packages/shared/src/subscriptions/requests.ts', """import { z } from 'zod';

import { dateSchema, textSchema } from '../core/index.ts';
import {
  MAX_DAYS_PER_WEEK,
  MAX_HOURS_PER_DAY,
  PACKAGE_NAME_MAX_LENGTH,
  SUBSCRIPTION_BILLINGS,
} from '../packages/index.ts';
import { PRICE_MAX_AGOROT } from '../spaces/index.ts';

// The requests that correct a subscription (docs/api/api-contract.md §5, Subscriptions (managed)).

/** The longest reason a corrected price carries. */
export const PRICE_CORRECTION_REASON_MAX_LENGTH = 200;

// A count of days or hours: whole, from 1, at most the Int column's bound, as a package's.
const count = z.number().int().min(1).max(2_147_483_647);

/**
 * The staff's correction of a subscription's limits, dates and name: each optional; `null` clears a
 * limit or the end. The start stays (a subscription that has one keeps one).
 */
export const correctSubscriptionSchema = z
  .object({
    name: textSchema(1, PACKAGE_NAME_MAX_LENGTH),
    startsOn: dateSchema,
    endsOn: dateSchema.nullable(),
    totalDays: count.nullable(),
    daysPerWeek: count.max(MAX_DAYS_PER_WEEK).nullable(),
    hoursPerDay: count.max(MAX_HOURS_PER_DAY).nullable(),
    totalHours: count.nullable(),
  })
  .partial();
export type CorrectSubscriptionRequest = z.infer<typeof correctSubscriptionSchema>;

/** The owner's correction of a subscription's price and billing, together, with why. */
export const correctPriceSchema = z.object({
  billing: z.enum(SUBSCRIPTION_BILLINGS),
  priceAgorot: z.number().int().min(1).max(PRICE_MAX_AGOROT),
  reason: textSchema(1, PRICE_CORRECTION_REASON_MAX_LENGTH),
});
export type CorrectPriceRequest = z.infer<typeof correctPriceSchema>;
""")
write('packages/shared/src/subscriptions/index.ts', "export * from './requests.ts';\nexport * from './responses.ts';\n")

# shared: the codes
rep('packages/shared/src/core/errors.ts', """  // warning only: the customer still owes on an earlier item after a subscribe's payment (desk)
  'CUSTOMER_HAS_DEBT',
] as const;""", """  // warning only: the customer still owes on an earlier item after a subscribe's payment (desk)
  'CUSTOMER_HAS_DEBT',
  // a subscription ended early: corrected no more (subscriptions)
  'SUBSCRIPTION_ENDED',
  // a fixed price below what was paid on it, from the database (subscriptions)
  'PRICE_BELOW_PAID',
] as const;""")
rep('apps/web/src/shared/copy/arabic/errors.ts', "  CUSTOMER_HAS_DEBT: 'ما زال على الزبون دين سابق.',\n",
    "  CUSTOMER_HAS_DEBT: 'ما زال على الزبون دين سابق.',\n  SUBSCRIPTION_ENDED: 'أُنهي هذا الاشتراك مبكرًا، فلم يعد يُعدَّل.',\n  PRICE_BELOW_PAID: 'السعر الجديد أقل مما دُفع؛ تُلغى دفعة أولًا.',\n")
rep('apps/web/src/shared/copy/english/errors.ts', "  CUSTOMER_HAS_DEBT: 'The customer still owes on an earlier item.',\n",
    "  CUSTOMER_HAS_DEBT: 'The customer still owes on an earlier item.',\n  SUBSCRIPTION_ENDED: 'This subscription was ended early; it is no longer corrected.',\n  PRICE_BELOW_PAID: 'The new price is less than what was already paid; void a payment first.',\n")

# the translation line
rep('apps/api/src/shared/errors/constraintCodes.ts', "  payments_within_due: { type: 'conflict', code: 'PAYMENT_EXCEEDS_DUE' },\n",
    "  payments_within_due: { type: 'conflict', code: 'PAYMENT_EXCEEDS_DUE' },\n  subscriptions_price_below_paid: { type: 'conflict', code: 'PRICE_BELOW_PAID' },\n")

# can()
rep('apps/api/src/shared/auth/can.ts', """  /** A customer archived, and restored. */
  'customers.archive': 'owner',""", """  /** A customer archived, and restored. */
  'customers.archive': 'owner',
  /** A subscription's price and billing corrected, with a reason. */
  'subscriptions.correctPrice': 'owner',""")

# the pure change rule
write('apps/api/src/modules/subscriptions/subscriptionChange.ts', """import type { CorrectSubscriptionRequest } from '@masaha/shared/subscriptions';

import type { AuditValues } from '../../shared/audit/index.ts';

/** The fields the staff correct: the name, the dates (Gaza dates) and the limits. */
export interface CorrectableTerms {
  name: string;
  startsOn: string | null;
  endsOn: string | null;
  totalDays: number | null;
  daysPerWeek: number | null;
  hoursPerDay: number | null;
  totalHours: number | null;
}

/** What a correction changes, and what its audit entry records of it. */
export interface SubscriptionChange {
  /** Only the fields set to a new value. */
  data: Partial<CorrectableTerms>;
  /** Those fields, as they were. */
  before: AuditValues;
  /** Those fields, as they become. */
  after: AuditValues;
}

const FIELDS = [
  'name',
  'startsOn',
  'endsOn',
  'totalDays',
  'daysPerWeek',
  'hoursPerDay',
  'totalHours',
] as const satisfies readonly (keyof CorrectableTerms)[];

/**
 * What a correction changes, as `packageChange` decides an edit: a field set to a value other than
 * the current one. An absent field is kept, and `null` clears a limit or the end. A correction that
 * changes nothing has empty `data`.
 */
export function subscriptionChange(
  current: CorrectableTerms,
  edit: CorrectSubscriptionRequest,
): SubscriptionChange {
  const changed = FIELDS.filter(
    (field) => edit[field] !== undefined && edit[field] !== current[field],
  );
  const pick = (from: Partial<CorrectableTerms>) =>
    Object.fromEntries(changed.map((field) => [field, from[field]])) as Partial<CorrectableTerms>;
  const data = pick(edit);
  return { data, before: { ...pick(current) }, after: { ...data } };
}
""")

# repository: read the terms under the lock; write a correction
p = 'apps/api/src/modules/subscriptions/subscriptions.repository.ts'
rep(p, """    /** Every check-in of the space's subscription, the earliest first, then by id. */
    checkInsOf(""", """    /**
     * A locked subscription's correctable terms, its price and billing, and whether it was ended, in
     * the caller's transaction (dates as Gaza dates).
     */
    async termsOf(
      id: number,
      tx: Tx,
    ): Promise<
      CorrectableTerms & { billing: SubscriptionToCreate['billing']; priceAgorot: number; ended: boolean }
    > {
      const row = await tx.subscription.findUniqueOrThrow({
        where: { id },
        select: {
          name: true,
          startsOn: true,
          endsOn: true,
          totalDays: true,
          daysPerWeek: true,
          hoursPerDay: true,
          totalHours: true,
          billing: true,
          priceAgorot: true,
          endedAt: true,
        },
      });
      const { startsOn, endsOn, endedAt, ...rest } = row;
      return {
        ...rest,
        startsOn: calendarDateOf(startsOn),
        endsOn: calendarDateOf(endsOn),
        ended: endedAt !== null,
      };
    },

    /** Writes a correction of the terms (dates as Gaza dates). */
    async correct(id: number, data: Partial<CorrectableTerms>, tx: Tx): Promise<void> {
      const { startsOn, endsOn, ...rest } = data;
      await tx.subscription.update({
        where: { id },
        data: {
          ...rest,
          ...(startsOn !== undefined && { startsOn: dateOf(startsOn) }),
          ...(endsOn !== undefined && { endsOn: dateOf(endsOn) }),
        },
        select: { id: true },
      });
    },

    /** Writes a corrected price and billing, with who typed the price and why. */
    async correctPrice(
      id: number,
      price: { billing: SubscriptionToCreate['billing']; priceAgorot: number; byId: number; reason: string },
      tx: Tx,
    ): Promise<void> {
      await tx.subscription.update({
        where: { id },
        data: {
          billing: price.billing,
          priceAgorot: price.priceAgorot,
          priceSetById: price.byId,
          priceReason: price.reason,
        },
        select: { id: true },
      });
    },

    /** Every check-in of the space's subscription, the earliest first, then by id. */
    checkInsOf(""")
rep(p, """/** A Gaza calendar date as a `@db.Date` value: its UTC midnight (conventions §11). */
const dateOf = (date: string | null) => (date === null ? null : new Date(`${date}T00:00:00.000Z`));""",
    """/** A Gaza calendar date as a `@db.Date` value: its UTC midnight (conventions §11). */
const dateOf = (date: string | null) => (date === null ? null : new Date(`${date}T00:00:00.000Z`));

/** A `@db.Date` as its calendar date, read at UTC, never through a zone (conventions §11). */
const calendarDateOf = (date: Date | null) => date?.toISOString().slice(0, 10) ?? null;""")
rep(p, "import { isForeignKeyViolation, prisma, type Tx } from '../../db/index.ts';",
    "import { isForeignKeyViolation, prisma, type Tx } from '../../db/index.ts';\nimport type { CorrectableTerms } from './subscriptionChange.ts';")

# service: the two corrections
p = 'apps/api/src/modules/subscriptions/subscriptions.service.ts'
rep(p, "import type { SubscriptionState, SubscriptionStatus } from '@masaha/shared/subscriptions';",
    """import type {
  CorrectPriceRequest,
  CorrectSubscriptionRequest,
  SubscriptionState,
  SubscriptionStatus,
} from '@masaha/shared/subscriptions';""")
rep(p, "import type { AuditValues, AuditWriter } from '../../shared/audit/index.ts';",
    """import type { AuditValues, AuditWriter } from '../../shared/audit/index.ts';
import { can, type Actor, type LoadedSpace, type SpaceAction } from '../../shared/auth/index.ts';
import { AppError } from '../../shared/errors/index.ts';""")
rep(p, "import { currentSubscription } from './currentSubscription.ts';",
    "import { currentSubscription } from './currentSubscription.ts';\nimport { subscriptionChange } from './subscriptionChange.ts';")
rep(p, """  spaceSettings: SpaceSettingsService;
  logger: Logger;
}""", """  spaceSettings: SpaceSettingsService;
  logger: Logger;
  /** The one clock (conventions §11). */
  now: () => Date;
}""")
rep(p, """  spaceSettings,
  logger,
}: Dependencies) {
  const repository = createSubscriptionsRepository();
""", """  spaceSettings,
  logger,
  now,
}: Dependencies) {
  const repository = createSubscriptionsRepository();

  /**
   * Opens a correction, in its transaction: the space's lock, `can()` of the action on the links read
   * under it (a link ended meanwhile still decides), then the subscription's row (`FOR UPDATE`), not
   * the space's → `not_found`; ended → `SUBSCRIPTION_ENDED`. Answers its terms.
   */
  async function lockForCorrection(
    actor: Actor,
    space: LoadedSpace,
    subscriptionId: number,
    action: SpaceAction,
    tx: Tx,
  ) {
    if (!(await spaces.lock(space.id, tx))) throw AppError.notFound(undefined, 'Space not found');
    if (!can(actor, action, { links: await space.linksUnder(tx) })) throw AppError.forbidden();
    if (!(await repository.lockIn(space.id, subscriptionId, tx))) {
      throw AppError.notFound(undefined, 'Subscription not found');
    }
    const terms = await repository.termsOf(subscriptionId, tx);
    if (terms.ended) throw AppError.conflict('SUBSCRIPTION_ENDED');
    return terms;
  }

  /** The subscription's state as of now, in the caller's transaction. */
  async function stateNow(spaceId: number, subscriptionId: number, tx: Tx) {
    const [state] = await statesOf(spaceId, { ids: [subscriptionId] }, now(), tx);
    if (!state) throw new Error(`The subscription ${String(subscriptionId)} is not the space's.`);
    return state;
  }
""")
rep(p, """    /** Every check-in of the space's subscription, the earliest first, then by id. */
    checkInsOf(""", """    /**
     * The staff's correction of a subscription's limits, dates and name, in one transaction:
     * `lockForCorrection` (`subscriptions.manage`); only the fields set to a new value
     * (`subscriptionChange`), `null` clearing a limit or the end; an end before the start →
     * `out_of_range` on `endsOn`; nothing changed → nothing written; else audited
     * `subscription.corrected` with the changed fields before and after. Answers its state.
     */
    correct(
      actor: Actor,
      space: LoadedSpace,
      subscriptionId: number,
      edit: CorrectSubscriptionRequest,
    ): Promise<SubscriptionState> {
      return runInTransaction(async (tx) => {
        const current = await lockForCorrection(
          actor,
          space,
          subscriptionId,
          'subscriptions.manage',
          tx,
        );
        const { data, before, after } = subscriptionChange(current, edit);
        if (Object.keys(data).length === 0) return stateNow(space.id, subscriptionId, tx);
        const startsOn = data.startsOn === undefined ? current.startsOn : data.startsOn;
        const endsOn = data.endsOn === undefined ? current.endsOn : data.endsOn;
        if (startsOn !== null && endsOn !== null && endsOn < startsOn) {
          throw AppError.validation({ endsOn: ['out_of_range'] });
        }
        await repository.correct(subscriptionId, data, tx);
        await audit(
          {
            actorId: actor.id,
            action: 'subscription.corrected',
            entityType: 'subscription',
            entityId: subscriptionId,
            spaceId: space.id,
            before,
            after,
          },
          tx,
        );
        return stateNow(space.id, subscriptionId, tx);
      });
    },

    /**
     * The owner's correction of a subscription's price and billing, in one transaction:
     * `lockForCorrection` (`subscriptions.correctPrice`); the same billing and price → nothing
     * written; else both, recorded as a price typed by the owner with the reason, audited
     * `subscription.priceCorrected`. A fixed price below what was paid is the database's refusal
     * (`PRICE_BELOW_PAID`). Answers its state.
     */
    correctPrice(
      actor: Actor,
      space: LoadedSpace,
      subscriptionId: number,
      { billing, priceAgorot, reason }: CorrectPriceRequest,
    ): Promise<SubscriptionState> {
      return runInTransaction(async (tx) => {
        const current = await lockForCorrection(
          actor,
          space,
          subscriptionId,
          'subscriptions.correctPrice',
          tx,
        );
        if (current.billing === billing && current.priceAgorot === priceAgorot) {
          return stateNow(space.id, subscriptionId, tx);
        }
        await repository.correctPrice(
          subscriptionId,
          { billing, priceAgorot, byId: actor.id, reason },
          tx,
        );
        await audit(
          {
            actorId: actor.id,
            action: 'subscription.priceCorrected',
            entityType: 'subscription',
            entityId: subscriptionId,
            spaceId: space.id,
            before: { billing: current.billing, priceAgorot: current.priceAgorot },
            after: { billing, priceAgorot, reason },
          },
          tx,
        );
        return stateNow(space.id, subscriptionId, tx);
      });
    },

    /** Every check-in of the space's subscription, the earliest first, then by id. */
    checkInsOf(""")

# controller and router
write('apps/api/src/modules/subscriptions/subscriptions.controller.ts', """import type {
  CorrectPriceRequest,
  CorrectSubscriptionRequest,
  SubscriptionState,
} from '@masaha/shared/subscriptions';
import type { Request, Response } from 'express';

import { signedIn, spaceOf } from '../../shared/auth/index.ts';
import { sendSuccess } from '../../shared/http/index.ts';
import { parseId } from '../../shared/validation/index.ts';
import type { SubscriptionsService } from './subscriptions.service.ts';

export function createSubscriptionsController(service: SubscriptionsService) {
  return {
    /** 200 with the subscription's state; a correction that changes nothing answers it as it is. */
    correct: async (req: Request, res: Response) => {
      const { userId, role } = signedIn(req);
      const state = await service.correct(
        { id: userId, role },
        spaceOf(req),
        parseId(req.params.subscriptionId),
        req.body as CorrectSubscriptionRequest,
      );
      sendSuccess(res, state satisfies SubscriptionState);
    },

    /** 200 with the subscription's state; the same price and billing answer it as it is. */
    correctPrice: async (req: Request, res: Response) => {
      const { userId, role } = signedIn(req);
      const state = await service.correctPrice(
        { id: userId, role },
        spaceOf(req),
        parseId(req.params.subscriptionId),
        req.body as CorrectPriceRequest,
      );
      sendSuccess(res, state satisfies SubscriptionState);
    },
  };
}

export type SubscriptionsController = ReturnType<typeof createSubscriptionsController>;
""")
write('apps/api/src/modules/subscriptions/subscriptions.manage.routes.ts', """import { correctPriceSchema, correctSubscriptionSchema } from '@masaha/shared/subscriptions';
import { Router } from 'express';

import { requireCan } from '../../shared/auth/index.ts';
import { validate } from '../../shared/validation/index.ts';
import type { SubscriptionsController } from './subscriptions.controller.ts';

/**
 * The subscriptions' writes of one module, mounted below `/manage/spaces/:spaceId`, behind that
 * boundary (docs/backend/security.md › Authorization). Each asks `can()` here first, before its body
 * is read; the service asks `can()` again under the space's lock. The price is the owner's
 * (`subscriptions.correctPrice`). Subscribing and the statement span modules: they are the desk's.
 */
export function createSubscriptionsManageRouter(controller: SubscriptionsController): Router {
  const router = Router();
  router.patch(
    '/subscriptions/:subscriptionId',
    requireCan('subscriptions.manage'),
    validate(correctSubscriptionSchema),
    controller.correct,
  );
  router.put(
    '/subscriptions/:subscriptionId/price',
    requireCan('subscriptions.correctPrice'),
    validate(correctPriceSchema),
    controller.correctPrice,
  );
  return router;
}
""")
p = 'apps/api/src/modules/subscriptions/index.ts'
s = open(p, encoding='utf-8', newline='').read()
s = "export {\n  createSubscriptionsController,\n  type SubscriptionsController,\n} from './subscriptions.controller.ts';\nexport { createSubscriptionsManageRouter } from './subscriptions.manage.routes.ts';\n" + s
open(p, 'w', encoding='utf-8', newline='').write(s)

p = 'apps/api/src/app.ts'
rep(p, "import { createSubscriptionsService } from './modules/subscriptions/index.ts';",
    "import {\n  createSubscriptionsController,\n  createSubscriptionsManageRouter,\n  createSubscriptionsService,\n} from './modules/subscriptions/index.ts';")
rep(p, """  const subscriptions = createSubscriptionsService({
    runInTransaction,
    audit: writeAudit,
    spaces,
    spaceSettings,
    logger,
  });""", """  const subscriptions = createSubscriptionsService({
    runInTransaction,
    audit: writeAudit,
    spaces,
    spaceSettings,
    logger,
    now: clock,
  });""")
rep(p, "  manage.use(createDeskManageRouter(createDeskController(desk)));",
    "  manage.use(createDeskManageRouter(createDeskController(desk)));\n  manage.use(createSubscriptionsManageRouter(createSubscriptionsController(subscriptions)));")
print('ok')
