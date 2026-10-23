import os
os.chdir(r'C:\dev\masaha\app-b')

def rep(p, old, new, count=1):
    s = open(p, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (p, old, s.count(old))
    s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)

# shared: ReceivedPayment
p = 'packages/shared/src/desk/responses.ts'
rep(p, """/**
 * A visit's payment after its check-out: the visit, the payment, and what was paid on the visit and
 * what it still owes, as of the answer (a retry's too).
 */
export interface ReceivedPayment {
  visit: DeskVisit;
  payment: VisitPayment;
  paidAgorot: number;
  balanceAgorot: number;
}""", """/**
 * A payment on one item: the visit it paid after its check-out, or the subscription, the other
 * `null`; the payment; and what was paid on the item and what it still owes, as of the answer (a
 * retry's too). A usage-based subscription's balance is below zero while it holds credit.
 */
export interface ReceivedPayment {
  visit: DeskVisit | null;
  subscription: SubscriptionState | null;
  payment: VisitPayment;
  paidAgorot: number;
  balanceAgorot: number;
}""")

# payments repository
p = 'apps/api/src/modules/payments/payments.repository.ts'
rep(p, """const VISIT_PAYMENT = {
  id: true,
  visitId: true,
  amountAgorot: true,""", """const VISIT_PAYMENT = {
  id: true,
  visitId: true,
  subscriptionId: true,
  amountAgorot: true,""")
rep(p, """/** A payment of a visit, as it is stored. */
export interface VisitPaymentRow {
  id: number;
  visitId: number | null;
  amountAgorot: number;""", """/** A payment of an item, as it is stored: its visit or its subscription, the other `null`. */
export interface VisitPaymentRow {
  id: number;
  visitId: number | null;
  subscriptionId: number | null;
  amountAgorot: number;""")
rep(p, """/** A visit's payment to record, with its idempotency key. */
export interface NewVisitPayment extends PaymentRequest {
  spaceId: number;
  visitId: number;
  key: string;
  recordedById: number;
  receivedAt: Date;
}""", """/** A payment to record on one item, a visit or a subscription, with its idempotency key. */
export interface NewPayment extends PaymentRequest {
  spaceId: number;
  item: { visitId: number } | { subscriptionId: number };
  key: string;
  recordedById: number;
  receivedAt: Date;
}""")
rep(p, """    /** Inserts the payment; the insert trigger checks it against the visit's charge. */
    createForVisit(payment: NewVisitPayment, tx: Tx): Promise<VisitPaymentRow> {
      const { spaceId, visitId, key, amountAgorot, method, note, recordedById, receivedAt } =
        payment;
      return tx.payment.create({
        data: {
          spaceId,
          visitId,
          idempotencyKey: key,""", """    /** Inserts the payment; the insert trigger checks it against its item's due. */
    create(payment: NewPayment, tx: Tx): Promise<VisitPaymentRow> {
      const { spaceId, item, key, amountAgorot, method, note, recordedById, receivedAt } = payment;
      return tx.payment.create({
        data: {
          spaceId,
          ...item,
          idempotencyKey: key,""")

# payments service
p = 'apps/api/src/modules/payments/payments.service.ts'
rep(p, """  type ItemBalanceRow,
  type NewVisitPayment,
} from './payments.repository.ts';""", """  type ItemBalanceRow,
  type NewPayment,
} from './payments.repository.ts';""")
rep(p, """/**
 * The payment ledger (ADR 0010; docs/backend/conventions.md › The ledger's rules). So far a visit's
 * payment, taken at its check-out, and the uncollected visits. The database owns the ledger's rules:
 * nothing here repeats them.
 */""", """/**
 * The payment ledger (ADR 0010; docs/backend/conventions.md › The ledger's rules): a payment on a
 * visit or a subscription, the balances and the uncollected visits. The database owns the ledger's
 * rules: nothing here repeats them.
 */""")
rep(p, """    /**
     * The space's payment recorded with this idempotency key, with the visit it settles, or `null`:
     * a retried check-out's payment.
     */
    async findByKey(
      spaceId: number,
      key: string,
      tx: Tx,
    ): Promise<{ visitId: number | null; payment: VisitPayment } | null> {
      const row = await repository.findByKey(spaceId, key, tx);
      return row && { visitId: row.visitId, payment: toVisitPayment(row) };
    },""", """    /**
     * The space's payment recorded with this idempotency key, with the item it settles (a visit or a
     * subscription, the other `null`), or `null`: a retried request's payment.
     */
    async findByKey(
      spaceId: number,
      key: string,
      tx: Tx,
    ): Promise<{
      visitId: number | null;
      subscriptionId: number | null;
      payment: VisitPayment;
    } | null> {
      const row = await repository.findByKey(spaceId, key, tx);
      return (
        row && {
          visitId: row.visitId,
          subscriptionId: row.subscriptionId,
          payment: toVisitPayment(row),
        }
      );
    },""")
rep(p, """    /** Records a visit's payment, in the caller's transaction, audited `payment.recorded`. */
    async recordForVisit(payment: NewVisitPayment, tx: Tx): Promise<VisitPayment> {
      const row = await repository.createForVisit(payment, tx);
      await audit(
        {
          actorId: payment.recordedById,
          action: 'payment.recorded',
          entityType: 'payment',
          entityId: row.id,
          spaceId: payment.spaceId,
          after: {
            visitId: payment.visitId,
            amountAgorot: payment.amountAgorot,
            method: payment.method,
          },
        },
        tx,
      );
      return toVisitPayment(row);
    },""", """    /**
     * Records a payment on a visit or a subscription, in the caller's transaction, audited
     * `payment.recorded` with its item; the ledger's trigger checks it against the item's due.
     */
    async record(payment: NewPayment, tx: Tx): Promise<VisitPayment> {
      const row = await repository.create(payment, tx);
      await audit(
        {
          actorId: payment.recordedById,
          action: 'payment.recorded',
          entityType: 'payment',
          entityId: row.id,
          spaceId: payment.spaceId,
          after: { ...payment.item, amountAgorot: payment.amountAgorot, method: payment.method },
        },
        tx,
      );
      return toVisitPayment(row);
    },""")

# subscriptions: lockIn
p = 'apps/api/src/modules/subscriptions/subscriptions.repository.ts'
rep(p, """    /** The space's open check-ins, the earliest first, then by id. */
    openCheckInsIn(""", """    /** Locks the space's subscription's row (`FOR UPDATE`): its id and customer, or `null`. */
    async lockIn(
      spaceId: number,
      id: number,
      tx: Tx,
    ): Promise<{ id: number; customerId: number } | null> {
      const [locked] = await tx.$queryRaw<{ id: number; customer_id: number }[]>`
        SELECT id, customer_id FROM subscriptions WHERE id = ${id} AND space_id = ${spaceId}
        FOR UPDATE`;
      return locked ? { id: locked.id, customerId: locked.customer_id } : null;
    },

    /** The space's open check-ins, the earliest first, then by id. */
    openCheckInsIn(""")
p = 'apps/api/src/modules/subscriptions/subscriptions.service.ts'
rep(p, """    /** The space's subscription made with this idempotency key, in the caller's transaction. */""", """    /**
     * Locks the space's subscription's row (`FOR UPDATE`), after the space's lock: its id and
     * customer, or `null` when it is not the space's.
     */
    lockIn(
      spaceId: number,
      id: number,
      tx: Tx,
    ): Promise<{ id: number; customerId: number } | null> {
      return repository.lockIn(spaceId, id, tx);
    },

    /** The space's subscription made with this idempotency key, in the caller's transaction. */""")

# desk: check-out's record, and the payment's subscription branch
p = 'apps/api/src/modules/desk/desk.service.ts'
rep(p, """        const payment = request.payment
          ? await payments.recordForVisit(
              {
                spaceId: space.id,
                visitId,
                key,""", """        const payment = request.payment
          ? await payments.record(
              {
                spaceId: space.id,
                item: { visitId },
                key,""")
rep(p, """    /**
     * Receives a payment for a closed visit after its check-out, in one transaction and in this
     * order: the space's lock and `can()`; the visit's row (`FOR UPDATE`); the payment this key
     * recorded, for a retry, answered with the visit and the sums as they are now; open →
     * `conflict`; the payment, which the ledger checks (written off, unpriced, above the balance)
     * before any phone is asked; then, if anything remains, the customer it is left to.
     */
    receivePayment(
      actor: Actor,
      space: LoadedSpace,
      key: string,
      { visitId, phone, customerName, ...payment }: ReceivePaymentRequest,
    ): Promise<ReceivedPayment> {
      return runInTransaction(async (tx) => {
        await lockAtDesk(actor, space, tx, 'payments.record');
        const locked = await visits.lockIn(space.id, visitId, tx);""", """    /**
     * Receives a payment on one item, in one transaction: the space's lock and `can()`, then the
     * subscription's branch (`subscriptionPayment`), or, in this order: the visit's row (`FOR
     * UPDATE`); the payment this key recorded, for a retry, answered with the visit and the sums as
     * they are now; open → `conflict`; the payment, which the ledger checks (written off, unpriced,
     * above the balance) before any phone is asked; then, if anything remains, the customer it is
     * left to.
     */
    receivePayment(
      actor: Actor,
      space: LoadedSpace,
      key: string,
      { visitId, subscriptionId, phone, customerName, ...payment }: ReceivePaymentRequest,
    ): Promise<ReceivedPayment> {
      return runInTransaction(async (tx) => {
        await lockAtDesk(actor, space, tx, 'payments.record');
        if (subscriptionId !== undefined) {
          return subscriptionPayment(actor, space, subscriptionId, key, payment, tx);
        }
        // The schema lets no request name neither item.
        if (visitId === undefined) throw AppError.validation({ visitId: ['required'] });
        const locked = await visits.lockIn(space.id, visitId, tx);""")
rep(p, """        if (recorded) {
          const { paidAgorot, balanceAgorot } = await balanceOf(space, locked, tx);
          return {
            visit: locked.visit,
            payment: recorded.payment,
            paidAgorot,
            balanceAgorot: balanceAgorot ?? 0,
          };
        }
        if (locked.open) {
          throw AppError.conflict(undefined, 'An open visit is paid at its check-out');
        }

        const received = await payments.recordForVisit(
          {
            spaceId: space.id,
            visitId,
            key,""", """        if (recorded) {
          const { paidAgorot, balanceAgorot } = await balanceOf(space, locked, tx);
          return {
            visit: locked.visit,
            subscription: null,
            payment: recorded.payment,
            paidAgorot,
            balanceAgorot: balanceAgorot ?? 0,
          };
        }
        if (locked.open) {
          throw AppError.conflict(undefined, 'An open visit is paid at its check-out');
        }

        const received = await payments.record(
          {
            spaceId: space.id,
            item: { visitId },
            key,""")
rep(p, """        return { visit, payment: received, paidAgorot, balanceAgorot: rest };
      });
    },""", """        return { visit, subscription: null, payment: received, paidAgorot, balanceAgorot: rest };
      });
    },""")
rep(p, """  /**
   * The time a check-out is priced at:""", """  /**
   * A payment on a subscription, under the space's lock, in this order: the subscription's row (`FOR
   * UPDATE`), not the space's → `invalid_choice` on `subscriptionId`; the payment this key recorded,
   * for another item → `conflict`, for this one a retry, answered with the sums as of now; then the
   * payment, which the ledger checks (above a fixed price: `PAYMENT_EXCEEDS_DUE`; a usage-based one
   * takes any amount, its credit). An ended or expired subscription, or an archived customer's,
   * still takes one: its debt is owed.
   */
  async function subscriptionPayment(
    actor: Actor,
    space: LoadedSpace,
    subscriptionId: number,
    key: string,
    payment: PaymentRequest,
    tx: Tx,
  ): Promise<ReceivedPayment> {
    const locked = await subscriptions.lockIn(space.id, subscriptionId, tx);
    if (!locked) throw AppError.validation({ subscriptionId: ['invalid_choice'] });
    const recorded = await payments.findByKey(space.id, key, tx);
    if (recorded && recorded.subscriptionId !== subscriptionId) {
      throw AppError.conflict(undefined, 'This idempotency key paid another item');
    }
    const at = now();
    const received =
      recorded?.payment ??
      (await payments.record(
        {
          spaceId: space.id,
          item: { subscriptionId },
          key,
          ...payment,
          recordedById: actor.id,
          receivedAt: at,
        },
        tx,
      ));
    const { paidAgorot, balanceAgorot, ...subscription } = await withMoney(space, locked, at, tx);
    return { visit: null, subscription, payment: received, paidAgorot, balanceAgorot };
  }

  /**
   * The time a check-out is priced at:""")
rep(p, """  /**
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
  }""", """  /**
   * A subscription of the space with its state, what was paid on it and what it still owes, as of
   * `at`, in the caller's transaction (its customer's items, one query).
   */
  async function withMoney(
    space: LoadedSpace,
    { id, customerId }: { id: number; customerId: number },
    at: Date,
    tx: Tx,
  ): Promise<SubscriptionWithMoney> {
    const [state] = await subscriptions.statesOf(space.id, { ids: [id] }, at, tx);
    if (!state) throw new Error(`The subscription ${String(id)} is not the space's.`);
    const items = await payments.itemBalances(space.id, customerId, at, tx);
    const money = items.find((item) => item.kind === 'SUBSCRIPTION' && item.id === id);
    return {
      ...state,
      paidAgorot: money?.paidAgorot ?? 0,
      balanceAgorot: money?.balanceAgorot ?? state.dueAgorot,
    };
  }

  /**
   * A subscribe's answer as of `at`, in the caller's transaction: the subscription with its state
   * and money, the payments given, and the customer's debt.
   */
  async function newSubscription(
    space: LoadedSpace,
    made: { id: number; customerId: number },
    allocated: NewSubscription['payments'],
    at: Date,
    tx: Tx,
  ): Promise<NewSubscription> {
    const subscription = await withMoney(space, made, at, tx);
    const balances = await payments.customerBalances(space.id, [made.customerId], at, tx);
    return {
      subscription,
      payments: allocated,
      debtAgorot: balances.get(made.customerId)?.debtAgorot ?? 0,
    };
  }""")
rep(p, "import type { Customer } from '@masaha/shared/customers';", "import type { Customer } from '@masaha/shared/customers';")
rep(p, """import type {
  CheckInVisitRequest,""", """import type { PaymentRequest } from '@masaha/shared/payments';
import type {
  CheckInVisitRequest,""")
print('ok')
