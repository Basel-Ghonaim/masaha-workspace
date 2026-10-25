import os
os.chdir(r'C:\dev\masaha\app-b')

def rep(p, old, new, count=1):
    s = open(p, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (p, old, s.count(old))
    s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)

# shared: the statement's shape
p = 'packages/shared/src/desk/responses.ts'
s = open(p, encoding='utf-8', newline='').read().rstrip('\n')
s += """

/** One check-in of a statement; `minutes` are a closed stay's whole minutes, `null` while open. */
export interface StatementCheckIn {
  id: number;
  checkedInAt: string;
  checkedOutAt: string | null;
  checkoutMethod: 'MANUAL' | 'AUTO' | null;
  minutes: number | null;
}

/**
 * A subscription's statement, as of the answer: its state and money, its customer, every check-in
 * (the earliest first) and every payment (voided ones marked), and the renewal's proposed start
 * while it is not renewed, or who renewed it.
 */
export type SubscriptionStatement = SubscriptionWithMoney & {
  customer: { id: number; name: string; phone: string | null };
  checkIns: StatementCheckIn[];
  payments: ItemPayment[];
  renewal: { startsOn: string } | null;
  renewedById: number | null;
};
"""
open(p, 'w', encoding='utf-8', newline='').write(s)

# subscriptions: the check-ins and the renewal of one subscription
p = 'apps/api/src/modules/subscriptions/subscriptions.repository.ts'
rep(p, """    /** The space's open check-ins, the earliest first, then by id. */
    openCheckInsIn(""", """    /** Every check-in of the space's subscription, the earliest first, then by id. */
    checkInsOf(spaceId: number, subscriptionId: number): Promise<SubscriptionCheckIn[]> {
      return prisma.checkIn.findMany({
        where: { spaceId, subscriptionId },
        select: { id: true, checkedInAt: true, checkedOutAt: true, checkoutMethod: true },
        orderBy: [{ checkedInAt: 'asc' }, { id: 'asc' }],
      });
    },

    /** The subscription that renewed this one of the space, or `null`. */
    async renewedBy(spaceId: number, subscriptionId: number): Promise<number | null> {
      const renewal = await prisma.subscription.findFirst({
        where: { spaceId, renewalOfId: subscriptionId },
        select: { id: true },
      });
      return renewal?.id ?? null;
    },

    /** The space's open check-ins, the earliest first, then by id. */
    openCheckInsIn(""")
rep(p, """/** A subscription's row as its lock answers it. */""", """/** A check-in of a subscription, as a statement shows it. */
export interface SubscriptionCheckIn {
  id: number;
  checkedInAt: Date;
  checkedOutAt: Date | null;
  checkoutMethod: 'MANUAL' | 'AUTO' | null;
}

/** A subscription's row as its lock answers it. */""")
p = 'apps/api/src/modules/subscriptions/subscriptions.service.ts'
rep(p, """    /** The space's open check-ins, the earliest first, then by id. */
    openCheckInsIn(""", """    /** Every check-in of the space's subscription, the earliest first, then by id. */
    checkInsOf(spaceId: number, subscriptionId: number): Promise<SubscriptionCheckIn[]> {
      return repository.checkInsOf(spaceId, subscriptionId);
    },

    /** The subscription that renewed this one of the space, or `null` while none has. */
    renewedBy(spaceId: number, subscriptionId: number): Promise<number | null> {
      return repository.renewedBy(spaceId, subscriptionId);
    },

    /** The space's open check-ins, the earliest first, then by id. */
    openCheckInsIn(""")
rep(p, """  type OpenCheckIn,
  type SubscriptionToCreate,
} from './subscriptions.repository.ts';""", """  type OpenCheckIn,
  type SubscriptionCheckIn,
  type SubscriptionToCreate,
} from './subscriptions.repository.ts';""")
p = 'apps/api/src/modules/subscriptions/index.ts'
rep(p, "  OpenCheckIn,\n  SubscriptionToCreate,", "  OpenCheckIn,\n  SubscriptionCheckIn,\n  SubscriptionToCreate,")

# payments: a subscription's payments
p = 'apps/api/src/modules/payments/payments.repository.ts'
rep(p, """    /** Every payment of these visits of the space, voided ones too, the earliest received first. */""",
    """    /** Every payment of the space's subscription, voided ones too, the earliest received first. */
    paymentsOfSubscription(spaceId: number, subscriptionId: number): Promise<ItemPaymentRow[]> {
      return prisma.payment.findMany({
        where: { spaceId, subscriptionId },
        select: { ...VISIT_PAYMENT, voidedAt: true, voidedById: true, voidReason: true },
        orderBy: [{ receivedAt: 'asc' }, { id: 'asc' }],
      });
    },

    /** Every payment of these visits of the space, voided ones too, the earliest received first. */""")
p = 'apps/api/src/modules/payments/payments.service.ts'
rep(p, """    /** Records a payment on a visit or a subscription,""", """    /** Every payment of the space's subscription, voided ones marked, the earliest received first. */
    async paymentsOfSubscription(spaceId: number, subscriptionId: number): Promise<ItemPayment[]> {
      return (await repository.paymentsOfSubscription(spaceId, subscriptionId)).map(toItemPayment);
    },

    /** Records a payment on a visit or a subscription,""")

# desk: the statement
p = 'apps/api/src/modules/desk/desk.service.ts'
rep(p, """  SubscribeRequest,
  SubscriptionWithMoney,""", """  SubscribeRequest,
  SubscriptionStatement,
  SubscriptionWithMoney,""")
rep(p, """    /**
     * Undoes a visit's write-off,""", """    /**
     * A subscription's statement (docs/backend/conventions.md › Composed reads): the subscription,
     * the space's (else `not_found`), with its state and money; its customer; its check-ins, each with
     * a closed stay's whole minutes; its payments, voided ones marked; and, while it is not renewed,
     * the start its renewal would take (`proposedStart`), else who renewed it. Its lists are whole,
     * bounded by one subscription. Read without a lock.
     */
    async statement(space: LoadedSpace, subscriptionId: number): Promise<SubscriptionStatement> {
      const at = now();
      const [state] = await subscriptions.statesOf(space.id, { ids: [subscriptionId] }, at);
      if (!state) throw AppError.notFound(undefined, 'Subscription not found');
      const [subscription, customer, checkIns, paymentsMade, renewedById] = await Promise.all([
        withMoney(space, state, at),
        customers.findIn(space.id, state.customerId),
        subscriptions.checkInsOf(space.id, subscriptionId),
        payments.paymentsOfSubscription(space.id, subscriptionId),
        subscriptions.renewedBy(space.id, subscriptionId),
      ]);
      if (!customer) throw new Error(`The subscription ${String(subscriptionId)} has no customer.`);
      return {
        ...subscription,
        customer: { id: customer.id, name: customer.name, phone: customer.phone },
        checkIns: checkIns.map(({ id, checkedInAt, checkedOutAt, checkoutMethod }) => ({
          id,
          checkedInAt: checkedInAt.toISOString(),
          checkedOutAt: checkedOutAt?.toISOString() ?? null,
          checkoutMethod,
          minutes: checkedOutAt
            ? Math.floor((checkedOutAt.getTime() - checkedInAt.getTime()) / 60_000)
            : null,
        })),
        payments: paymentsMade,
        renewal:
          renewedById === null ? { startsOn: proposedStart(state, gazaClockOf(at).date) } : null,
        renewedById,
      };
    },

    /**
     * Undoes a visit's write-off,""")
# withMoney: the transaction optional (a read)
rep(p, """    { id, customerId }: { id: number; customerId: number },
    at: Date,
    tx: Tx,
  ): Promise<SubscriptionWithMoney> {""", """    { id, customerId }: { id: number; customerId: number },
    at: Date,
    tx?: Tx,
  ): Promise<SubscriptionWithMoney> {""")

p = 'apps/api/src/modules/desk/desk.controller.ts'
rep(p, """  SubscribeRequest,
  VisitCheckOut,
} from '@masaha/shared/desk';""", """  SubscribeRequest,
  SubscriptionStatement,
  VisitCheckOut,
} from '@masaha/shared/desk';""")
rep(p, """    /** 200 with the customer; one already archived is answered as it is. */""", """    statement: async (req: Request, res: Response) => {
      const statement = await service.statement(spaceOf(req), parseId(req.params.subscriptionId));
      sendSuccess(res, statement satisfies SubscriptionStatement);
    },

    /** 200 with the customer; one already archived is answered as it is. */""")
p = 'apps/api/src/modules/desk/desk.manage.routes.ts'
rep(p, """    controller.subscribe,
  );
  return router;""", """    controller.subscribe,
  );
  router.get('/subscriptions/:subscriptionId', controller.statement);
  return router;""")
print('ok')
