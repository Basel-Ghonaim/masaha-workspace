import os
os.chdir(r'C:\dev\masaha\app-b')

def rep(p, old, new, count=1):
    s = open(p, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (p, old, s.count(old))
    s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)

# shared: the schema
p = 'packages/shared/src/desk/requests.ts'
rep(p, """/**
 * Subscribes a customer: from a package of the space, or custom terms, exactly one of them (both or
 * neither: `invalid_choice` on `packageId`); a start date, else the server's.
 */
export const subscribeSchema = z
  .object({
    packageId: id.optional(),
    custom: customTermsSchema.optional(),
    startsOn: dateSchema.optional(),
  })""", """/**
 * Subscribes a customer: from a package of the space, or custom terms, exactly one of them (both or
 * neither: `invalid_choice` on `packageId`); a start date, else the server's; the subscription it
 * renews, if any; and a payment, which the server allocates over the customer's debts, oldest first.
 */
export const subscribeSchema = z
  .object({
    packageId: id.optional(),
    custom: customTermsSchema.optional(),
    startsOn: dateSchema.optional(),
    renewalOfId: id.optional(),
    payment: paymentSchema.optional(),
  })""")

# shared: the codes
p = 'packages/shared/src/core/errors.ts'
rep(p, """  // a customer archived: edited no more until restored (customers, desk)
  'CUSTOMER_ARCHIVED',
] as const;""", """  // a customer archived: edited no more until restored (customers, desk)
  'CUSTOMER_ARCHIVED',
  // a subscription renewed already: each is renewed at most once (desk)
  'SUBSCRIPTION_ALREADY_RENEWED',
  // warning only: the customer still owes on an earlier item after a subscribe's payment (desk)
  'CUSTOMER_HAS_DEBT',
] as const;""")
p = 'apps/web/src/shared/copy/arabic/errors.ts'
rep(p, "  CUSTOMER_ARCHIVED: 'هذا الزبون مؤرشف؛ يسترجعه المالك أولًا.',\n",
    "  CUSTOMER_ARCHIVED: 'هذا الزبون مؤرشف؛ يسترجعه المالك أولًا.',\n  SUBSCRIPTION_ALREADY_RENEWED: 'جُدّد هذا الاشتراك بالفعل.',\n  CUSTOMER_HAS_DEBT: 'ما زال على الزبون دين سابق.',\n")
p = 'apps/web/src/shared/copy/english/errors.ts'
rep(p, "  CUSTOMER_ARCHIVED: 'This customer is archived; the owner restores them first.',\n",
    "  CUSTOMER_ARCHIVED: 'This customer is archived; the owner restores them first.',\n  SUBSCRIPTION_ALREADY_RENEWED: 'This subscription was already renewed.',\n  CUSTOMER_HAS_DEBT: 'The customer still owes on an earlier item.',\n")

# subscriptions: lockIn answers who renewed it
p = 'apps/api/src/modules/subscriptions/subscriptions.repository.ts'
rep(p, """    /** Locks the space's subscription's row (`FOR UPDATE`): its id and customer, or `null`. */
    async lockIn(
      spaceId: number,
      id: number,
      tx: Tx,
    ): Promise<{ id: number; customerId: number } | null> {
      const [locked] = await tx.$queryRaw<{ id: number; customer_id: number }[]>`
        SELECT id, customer_id FROM subscriptions WHERE id = ${id} AND space_id = ${spaceId}
        FOR UPDATE`;
      return locked ? { id: locked.id, customerId: locked.customer_id } : null;
    },""", """    /**
     * Locks the space's subscription's row (`FOR UPDATE`): its id, its customer and the subscription
     * that renewed it (`null` while none has), or `null` when it is not the space's.
     */
    async lockIn(spaceId: number, id: number, tx: Tx): Promise<LockedSubscription | null> {
      const [locked] = await tx.$queryRaw<
        { id: number; customer_id: number; renewed_by_id: number | null }[]
      >`
        SELECT s.id, s.customer_id,
               (SELECT r.id FROM subscriptions r WHERE r.renewal_of_id = s.id) AS renewed_by_id
        FROM subscriptions s WHERE s.id = ${id} AND s.space_id = ${spaceId}
        FOR UPDATE OF s`;
      return locked
        ? { id: locked.id, customerId: locked.customer_id, renewedById: locked.renewed_by_id }
        : null;
    },""")
rep(p, """/** A Gaza calendar date as a `@db.Date` value""", """/** A subscription's row as its lock answers it. */
export interface LockedSubscription {
  id: number;
  customerId: number;
  /** The subscription that renewed it; `null` while none has. */
  renewedById: number | null;
}

/** A Gaza calendar date as a `@db.Date` value""")
p = 'apps/api/src/modules/subscriptions/subscriptions.service.ts'
rep(p, """  type OpenCheckIn,
  type SubscriptionToCreate,
} from './subscriptions.repository.ts';""", """  type LockedSubscription,
  type OpenCheckIn,
  type SubscriptionToCreate,
} from './subscriptions.repository.ts';""")
rep(p, """    /**
     * Locks the space's subscription's row (`FOR UPDATE`), after the space's lock: its id and
     * customer, or `null` when it is not the space's.
     */
    lockIn(
      spaceId: number,
      id: number,
      tx: Tx,
    ): Promise<{ id: number; customerId: number } | null> {
      return repository.lockIn(spaceId, id, tx);
    },""", """    /**
     * Locks the space's subscription's row (`FOR UPDATE`), after the space's lock: its id, its
     * customer and the one that renewed it, or `null` when it is not the space's.
     */
    lockIn(spaceId: number, id: number, tx: Tx): Promise<LockedSubscription | null> {
      return repository.lockIn(spaceId, id, tx);
    },""")
p = 'apps/api/src/modules/subscriptions/index.ts'
rep(p, "export type { Now, OpenCheckIn, SubscriptionToCreate } from './subscriptions.repository.ts';",
    "export type {\n  LockedSubscription,\n  Now,\n  OpenCheckIn,\n  SubscriptionToCreate,\n} from './subscriptions.repository.ts';\nexport { proposedStart } from './renewal.ts';")

# payments: findByKeys
p = 'apps/api/src/modules/payments/payments.repository.ts'
rep(p, """    /** What was paid on each of these visits of the space, voided payments left out; none is absent. */""", """    /** The space's payments recorded with these idempotency keys, each with its key; one query. */
    findByKeys(
      spaceId: number,
      keys: readonly string[],
      tx: Tx,
    ): Promise<(VisitPaymentRow & { idempotencyKey: string })[]> {
      return tx.payment.findMany({
        where: { spaceId, idempotencyKey: { in: [...keys] } },
        select: { ...VISIT_PAYMENT, idempotencyKey: true },
      });
    },

    /** What was paid on each of these visits of the space, voided payments left out; none is absent. */""")
p = 'apps/api/src/modules/payments/payments.service.ts'
rep(p, """    /**
     * A page of the space's uncollected visits""", """    /**
     * The space's payments recorded with these keys, in the keys' order, each with its item (a visit
     * or a subscription); a key that recorded none is left out. One query: a renewal's retry.
     */
    async findByKeys(
      spaceId: number,
      keys: readonly string[],
      tx: Tx,
    ): Promise<{ item: { visitId: number } | { subscriptionId: number }; payment: VisitPayment }[]> {
      const rows = new Map(
        (await repository.findByKeys(spaceId, keys, tx)).map((row) => [row.idempotencyKey, row]),
      );
      return keys.flatMap((key) => {
        const row = rows.get(key);
        if (!row) return [];
        const item =
          row.visitId !== null
            ? { visitId: row.visitId }
            : { subscriptionId: row.subscriptionId ?? 0 };
        return [{ item, payment: toVisitPayment(row) }];
      });
    },

    /**
     * A page of the space's uncollected visits""")
print('ok')
