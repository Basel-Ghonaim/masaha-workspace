import os
os.chdir(r'C:\dev\masaha\app-b')

def rep(p, old, new, count=1):
    s = open(p, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (p, old, s.count(old))
    s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)

p = 'apps/api/src/modules/desk/desk.service.ts'
rep(p, "import type { DomainErrorCode } from '@masaha/shared/core';",
    "import { addDays, gazaClockOf, type DomainErrorCode } from '@masaha/shared/core';")
rep(p, """  LeaveToCustomerRequest,
  ReceivedPayment,
  ReceivePaymentRequest,
  UnpaidVisit,
  VisitCheckOut,
} from '@masaha/shared/desk';""", """  LeaveToCustomerRequest,
  NewSubscription,
  ReceivedPayment,
  ReceivePaymentRequest,
  SubscribeRequest,
  SubscriptionWithMoney,
  UnpaidVisit,
  VisitCheckOut,
} from '@masaha/shared/desk';""")
rep(p, """import type { OccupancyService } from '../occupancy/index.ts';
import type { PaymentsService } from '../payments/index.ts';""", """import type { OccupancyService } from '../occupancy/index.ts';
import type { PackageRow, PackagesService } from '../packages/index.ts';
import type { PaymentsService } from '../payments/index.ts';""")
rep(p, """import type { SubscriptionsService } from '../subscriptions/index.ts';""",
    """import type { SubscriptionsService, SubscriptionToCreate } from '../subscriptions/index.ts';""")
rep(p, """  payments: PaymentsService;
  occupancy: OccupancyService;
  /** The one clock (conventions §11). */""", """  payments: PaymentsService;
  occupancy: OccupancyService;
  packages: PackagesService;
  /** The one clock (conventions §11). */""")
rep(p, """  payments,
  occupancy,
  now,
}: Dependencies) {""", """  payments,
  occupancy,
  packages,
  now,
}: Dependencies) {""")
rep(p, """  /**
   * The time a check-out is priced at:""", """  /**
   * A new subscription's terms, from a package of the space (its end `validityDays` after its
   * start, both included), or typed at the desk by whoever may type a price (else
   * `PRICE_TYPING_NOT_ALLOWED`), its end as sent and never before its start, recorded with who typed
   * it and why.
   */
  function termsOf(
    actor: Actor,
    pack: PackageRow | null,
    { custom }: SubscribeRequest,
    startsOn: string,
    mayType: boolean,
  ): Omit<SubscriptionToCreate, 'spaceId' | 'customerId' | 'key' | 'renewalOfId' | 'startsOn'> {
    if (pack) {
      return {
        name: pack.name,
        totalDays: pack.totalDays,
        daysPerWeek: pack.daysPerWeek,
        hoursPerDay: pack.hoursPerDay,
        totalHours: pack.totalHours,
        billing: pack.billing,
        priceAgorot: pack.priceAgorot,
        audience: pack.audience,
        shiftId: pack.shiftId,
        packageId: pack.id,
        endsOn: addDays(startsOn, pack.validityDays - 1),
        priceTyped: null,
      };
    }
    if (!custom) throw AppError.validation({ packageId: ['invalid_choice'] });
    if (!mayType) throw AppError.forbidden('PRICE_TYPING_NOT_ALLOWED');
    if (custom.endsOn !== undefined && custom.endsOn < startsOn) {
      throw AppError.validation({ 'custom.endsOn': ['out_of_range'] });
    }
    return {
      name: custom.name,
      totalDays: custom.totalDays ?? null,
      daysPerWeek: custom.daysPerWeek ?? null,
      hoursPerDay: custom.hoursPerDay ?? null,
      totalHours: custom.totalHours ?? null,
      billing: custom.billing,
      priceAgorot: custom.priceAgorot,
      audience: custom.audience,
      shiftId: custom.shiftId ?? null,
      packageId: null,
      endsOn: custom.endsOn ?? null,
      priceTyped: { byId: actor.id, reason: custom.reason },
    };
  }

  /**
   * A subscribe's answer as of `at`, in the caller's transaction: the subscription with its state
   * and money, the payments given, and the customer's debt.
   */
  async function newSubscription(
    space: LoadedSpace,
    { id, customerId }: { id: number; customerId: number },
    allocated: NewSubscription['payments'],
    at: Date,
    tx: Tx,
  ): Promise<NewSubscription> {
    const [state] = await subscriptions.statesOf(space.id, { ids: [id] }, at, tx);
    if (!state) throw new Error(`The subscription ${String(id)} is not the space's.`);
    const items = await payments.itemBalances(space.id, customerId, at, tx);
    const balances = await payments.customerBalances(space.id, [customerId], at, tx);
    const money = items.find((item) => item.kind === 'SUBSCRIPTION' && item.id === id);
    const subscription: SubscriptionWithMoney = {
      ...state,
      paidAgorot: money?.paidAgorot ?? 0,
      balanceAgorot: money?.balanceAgorot ?? state.dueAgorot,
    };
    return {
      subscription,
      payments: allocated,
      debtAgorot: balances.get(customerId)?.debtAgorot ?? 0,
    };
  }

  /**
   * The time a check-out is priced at:""")
rep(p, """    /**
     * Archives a customer, the owner's,""", """    /**
     * Subscribes a customer, in one transaction and in this order: the space's lock and `can()`
     * (`subscriptions.manage`); the subscription this key already made, for a retry, answered as of
     * now; the customer, the space's (else `not_found`) and not archived (`CUSTOMER_ARCHIVED`); the
     * package, the space's and offered (else `invalid_choice` on `packageId`), or the typed terms
     * (`termsOf`); the start date, the one sent, else today; then the subscription, audited.
     * Answered with its state and money and the customer's debt.
     */
    subscribe(
      actor: Actor,
      space: LoadedSpace,
      customerId: number,
      key: string,
      request: SubscribeRequest,
    ): Promise<{ result: NewSubscription; warnings: DomainErrorCode[] }> {
      return runInTransaction(async (tx) => {
        const links = await lockAtDesk(actor, space, tx, 'subscriptions.manage');
        const at = now();
        const made = await subscriptions.findByKey(space.id, key, tx);
        if (made) return { result: await newSubscription(space, made, [], at, tx), warnings: [] };

        const customer = await customers.findIn(space.id, customerId, tx);
        if (!customer) throw AppError.notFound(undefined, 'Customer not found');
        if (customer.archivedAt) throw AppError.conflict('CUSTOMER_ARCHIVED');

        let pack: PackageRow | null = null;
        if (request.packageId !== undefined) {
          pack = await packages.termsOf(space.id, request.packageId, tx);
          if (!pack?.isActive) throw AppError.validation({ packageId: ['invalid_choice'] });
        }
        const mayType =
          pack === null &&
          can(actor, 'prices.typeByHand', {
            links,
            receptionMayTypePrices: (await spaceSettings.read(space.id, tx))
              .receptionMayTypePrices,
          });
        const startsOn = request.startsOn ?? gazaClockOf(at).date;
        const terms = termsOf(actor, pack, request, startsOn, mayType);

        const created = await subscriptions.create(
          actor.id,
          { ...terms, spaceId: space.id, customerId, key, renewalOfId: null, startsOn },
          tx,
        );
        if ('refused' in created) {
          throw AppError.validation({ 'custom.shiftId': ['invalid_choice'] });
        }
        return {
          result: await newSubscription(space, { id: created.id, customerId }, [], at, tx),
          warnings: [],
        };
      });
    },

    /**
     * Archives a customer, the owner's,""")

p = 'apps/api/src/modules/desk/desk.controller.ts'
rep(p, """  LeaveToCustomerRequest,
  ReceivedPayment,
  ReceivePaymentRequest,
  VisitCheckOut,
} from '@masaha/shared/desk';""", """  LeaveToCustomerRequest,
  NewSubscription,
  ReceivedPayment,
  ReceivePaymentRequest,
  SubscribeRequest,
  VisitCheckOut,
} from '@masaha/shared/desk';""")
rep(p, """    /** 200 with the customer; one already archived is answered as it is. */""", """    /** 201 every time, a retry included; the warnings in `meta` only when there are some. */
    subscribe: async (req: Request, res: Response) => {
      const { userId, role } = signedIn(req);
      const { result, warnings } = await service.subscribe(
        { id: userId, role },
        spaceOf(req),
        parseId(req.params.customerId),
        idempotencyKeyOf(res),
        req.body as SubscribeRequest,
      );
      sendSuccess(res, result satisfies NewSubscription, {
        status: 201,
        ...(warnings.length > 0 && { meta: { warnings } }),
      });
    },

    /** 200 with the customer; one already archived is answered as it is. */""")
p = 'apps/api/src/modules/desk/desk.manage.routes.ts'
rep(p, """  leaveToCustomerSchema,
  receivePaymentSchema,
} from '@masaha/shared/desk';""", """  leaveToCustomerSchema,
  receivePaymentSchema,
  subscribeSchema,
} from '@masaha/shared/desk';""")
rep(p, """    controller.archiveCustomer,
  );
  return router;""", """    controller.archiveCustomer,
  );
  router.post(
    '/customers/:customerId/subscriptions',
    requireCan('subscriptions.manage'),
    requireIdempotencyKey,
    validate(subscribeSchema),
    controller.subscribe,
  );
  return router;""")
p = 'apps/api/src/app.ts'
rep(p, """    payments,
    occupancy,
    now: clock,
  });""", """    payments,
    occupancy,
    packages,
    now: clock,
  });""")
print('ok')
