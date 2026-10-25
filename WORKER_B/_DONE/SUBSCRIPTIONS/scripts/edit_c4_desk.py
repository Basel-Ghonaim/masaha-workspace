import os, re
os.chdir(r'C:\dev\masaha\app-b')
p = 'apps/api/src/modules/desk/desk.service.ts'
s = open(p, encoding='utf-8', newline='').read()

start = s.index("    /**\n     * Subscribes a customer, in one transaction and in this order:")
end = s.index("    /**\n     * Archives a customer, the owner's,")
new = """    /**
     * Subscribes a customer, in one transaction and in this order: the space's lock and `can()`
     * (`subscriptions.manage`); the subscription this key already made, for a retry, answered with
     * the payments of its derived keys and the money as of now; the customer, the space's (else
     * `not_found`) and not archived (`CUSTOMER_ARCHIVED`); the subscription it renews, locked, the
     * customer's own (else `invalid_choice` on `renewalOfId`) and not renewed yet
     * (`SUBSCRIPTION_ALREADY_RENEWED`); the package, the space's and offered (else `invalid_choice`
     * on `packageId`), or the typed terms (`termsOf`); the start date, the one sent, else the
     * renewal's proposal (`proposedStart`); the subscription, audited; then the payment, allocated
     * over the customer's older debts oldest first and the rest to the new one, one payment each
     * under a key derived from the request's, which the ledger checks. Warns `CUSTOMER_HAS_DEBT`
     * while an older item still owes.
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
        if (made) {
          const allocated = await payments.findByKeys(space.id, derivedKeys(key), tx);
          return subscribed(space, made, allocated, at, tx);
        }

        const customer = await customers.findIn(space.id, customerId, tx);
        if (!customer) throw AppError.notFound(undefined, 'Customer not found');
        if (customer.archivedAt) throw AppError.conflict('CUSTOMER_ARCHIVED');

        let renewed: SubscriptionState | null = null;
        if (request.renewalOfId !== undefined) {
          const locked = await subscriptions.lockIn(space.id, request.renewalOfId, tx);
          if (locked?.customerId !== customerId) {
            throw AppError.validation({ renewalOfId: ['invalid_choice'] });
          }
          if (locked.renewedById !== null) throw AppError.conflict('SUBSCRIPTION_ALREADY_RENEWED');
          [renewed = null] = await subscriptions.statesOf(space.id, { ids: [locked.id] }, at, tx);
        }

        let pack: PackageRow | null = null;
        if (request.packageId !== undefined) {
          pack = await packages.termsOf(space.id, request.packageId, tx);
          if (!pack?.isActive) throw AppError.validation({ packageId: ['invalid_choice'] });
        }
        const mayType =
          pack === null &&
          can(actor, 'prices.typeByHand', {
            links,
            receptionMayTypePrices: (await spaceSettings.read(space.id, tx)).receptionMayTypePrices,
          });
        const startsOn = request.startsOn ?? proposedStart(renewed, gazaClockOf(at).date);
        const terms = termsOf(actor, pack, request, startsOn, mayType);

        const created = await subscriptions.create(
          actor.id,
          {
            ...terms,
            spaceId: space.id,
            customerId,
            key,
            renewalOfId: renewed?.id ?? null,
            startsOn,
          },
          tx,
        );
        if ('refused' in created) {
          throw AppError.validation({ 'custom.shiftId': ['invalid_choice'] });
        }
        const subscription = { id: created.id, customerId };
        const allocated = request.payment
          ? await allocatePayment(actor, space, subscription, key, request.payment, at, tx)
          : [];
        return subscribed(space, subscription, allocated, at, tx);
      });
    },

"""
s = s[:start] + new + s[end:]

# helpers: replace newSubscription by subscribed, add allocatePayment
old_start = s.index("  /**\n   * A subscribe's answer as of `at`, in the caller's transaction:")
old_end = s.index("  /**\n   * A payment on a subscription, under the space's lock,")
helpers = """  /**
   * A subscribe's answer as of `at`, in the caller's transaction (a retry's too): the subscription
   * with its state and money, the payments given, and the customer's debt; and `CUSTOMER_HAS_DEBT`
   * while an item older than the subscription still owes (ADR 0010 rule 7).
   */
  async function subscribed(
    space: LoadedSpace,
    made: { id: number; customerId: number },
    allocated: NewSubscription['payments'],
    at: Date,
    tx: Tx,
  ): Promise<{ result: NewSubscription; warnings: DomainErrorCode[] }> {
    const subscription = await withMoney(space, made, at, tx);
    const items = await payments.itemBalances(space.id, made.customerId, at, tx);
    const balances = await payments.customerBalances(space.id, [made.customerId], at, tx);
    const olderDebt = items.some(
      (item) =>
        !(item.kind === 'SUBSCRIPTION' && item.id === made.id) && (item.balanceAgorot ?? 0) > 0,
    );
    return {
      result: {
        subscription,
        payments: allocated,
        debtAgorot: balances.get(made.customerId)?.debtAgorot ?? 0,
      },
      warnings: olderDebt ? ['CUSTOMER_HAS_DEBT'] : [],
    };
  }

  /**
   * A subscribe's payment (K3, the owner's decision 8): the customer's items that still owe, read
   * under the space's lock, oldest first, each paid at most its balance, the rest to the new
   * subscription (`allocate`); one payment per part, in that order, under the key derived from the
   * request's and the part's place, each checked by the ledger (above a fixed new price:
   * `PAYMENT_EXCEEDS_DUE`, the whole request undone). Answered in that order.
   */
  async function allocatePayment(
    actor: Actor,
    space: LoadedSpace,
    made: { id: number; customerId: number },
    key: string,
    { amountAgorot, ...payment }: PaymentRequest,
    at: Date,
    tx: Tx,
  ): Promise<NewSubscription['payments']> {
    const items = await payments.itemBalances(space.id, made.customerId, at, tx);
    const debts = items.flatMap(({ kind, id, balanceAgorot }) =>
      (kind === 'SUBSCRIPTION' && id === made.id) || balanceAgorot === null || balanceAgorot <= 0
        ? []
        : [{ item: kind === 'VISIT' ? { visitId: id } : { subscriptionId: id }, balanceAgorot }],
    );
    const { parts } = allocate<AllocatedPayment['item']>(amountAgorot, debts, {
      subscriptionId: made.id,
    });
    const allocated: NewSubscription['payments'] = [];
    for (const [index, part] of parts.entries()) {
      const recorded = await payments.record(
        {
          spaceId: space.id,
          item: part.item,
          key: derivedKey(key, index),
          ...payment,
          amountAgorot: part.amountAgorot,
          recordedById: actor.id,
          receivedAt: at,
        },
        tx,
      );
      allocated.push({ item: part.item, payment: recorded });
    }
    return allocated;
  }

"""
s = s[:old_start] + helpers + s[old_end:]

def rep(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new)

rep("""  LeaveToCustomerRequest,
  NewSubscription,""", """  AllocatedPayment,
  LeaveToCustomerRequest,
  NewSubscription,""")
rep("""import type { PaymentRequest } from '@masaha/shared/payments';""",
    """import type { PaymentRequest } from '@masaha/shared/payments';
import type { SubscriptionState } from '@masaha/shared/subscriptions';""")
rep("""import { AppError } from '../../shared/errors/index.ts';""",
    """import { AppError } from '../../shared/errors/index.ts';
import { derivedKey } from '../../shared/http/index.ts';""")
rep("""import type { PaymentsService } from '../payments/index.ts';""",
    """import { allocate, ALLOCATION_MAX_ITEMS, type PaymentsService } from '../payments/index.ts';""")
rep("""import type { SubscriptionsService, SubscriptionToCreate } from '../subscriptions/index.ts';""",
    """import {
  proposedStart,
  type SubscriptionsService,
  type SubscriptionToCreate,
} from '../subscriptions/index.ts';""")
rep("""/** How old the quote a check-out is priced at may be (the owner's bound, P6). */""",
    """/** The keys a subscribe's payments may have taken: one per item an allocation pays at most. */
const derivedKeys = (key: string) =>
  Array.from({ length: ALLOCATION_MAX_ITEMS }, (_, index) => derivedKey(key, index));

/** How old the quote a check-out is priced at may be (the owner's bound, P6). */""")
open(p, 'w', encoding='utf-8', newline='').write(s)

p = 'apps/api/src/modules/payments/index.ts'
s = open(p, encoding='utf-8', newline='').read()
s = s.replace("export type { NewPayment } from './payments.repository.ts';",
              "export { allocate, ALLOCATION_MAX_ITEMS } from './allocation.ts';\nexport type { NewPayment } from './payments.repository.ts';")
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
