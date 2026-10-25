import io, os
os.chdir('C:/dev/masaha/app-b')
def edit(path, pairs):
    t = io.open(path, encoding='utf-8', newline='').read()
    for old, new in pairs:
        assert t.count(old) == 1, (path, old[:70], t.count(old))
        t = t.replace(old, new)
    io.open(path, 'w', encoding='utf-8', newline='').write(t)
def append(path, text):
    t = io.open(path, encoding='utf-8', newline='').read()
    io.open(path, 'w', encoding='utf-8', newline='').write(t.rstrip('\n') + '\n' + text)

# --- shared
append('packages/shared/src/desk/requests.ts', """
// The largest id an Int column holds.
const id = z.number().int().positive().max(2_147_483_647);

/**
 * A visit's payment after its check-out: the visit it pays, the payment, and the phone, and the
 * customer's name, when part of the charge stays unpaid on a visit with no customer.
 */
export const receivePaymentSchema = paymentSchema.extend({
  visitId: id,
  phone: phoneSchema.optional(),
  customerName: textSchema(1, VISITOR_NAME_MAX_LENGTH).optional(),
});
export type ReceivePaymentRequest = z.infer<typeof receivePaymentSchema>;
""")
append('packages/shared/src/desk/responses.ts', """
/**
 * A visit's payment after its check-out: the visit, the payment, and what was paid on the visit and
 * what it still owes, as of the answer (a retry's too).
 */
export interface ReceivedPayment {
  visit: DeskVisit;
  payment: VisitPayment;
  paidAgorot: number;
  balanceAgorot: number;
}
""")
edit('packages/shared/src/core/errors.ts', [
("  // a visit's debt: its write-off (desk)\n  'VISIT_ALREADY_PAID',\n",
 "  // a visit's debt: its write-off (desk)\n  'VISIT_ALREADY_PAID',\n  // a visit's debt: a payment, from the ledger, or a customer for it (desk)\n  'VISIT_WRITTEN_OFF',\n  'VISIT_HAS_CUSTOMER',\n"),
])
edit('apps/web/src/shared/copy/arabic/errors.ts', [
("  VISIT_ALREADY_PAID: 'دُفع مبلغ هذه الزيارة كاملًا.',\n",
 "  VISIT_ALREADY_PAID: 'دُفع مبلغ هذه الزيارة كاملًا.',\n  VISIT_WRITTEN_OFF:\n    'سُجّلت هذه الزيارة «لن يُحصَّل»؛ يتراجع المالك عن ذلك أولًا قبل استلام أي دفعة لها.',\n  VISIT_HAS_CUSTOMER: 'هذه الزيارة دينٌ على زبون آخر بالفعل.',\n"),
])
edit('apps/web/src/shared/copy/english/errors.ts', [
("  VISIT_ALREADY_PAID: 'This visit is already paid in full.',\n",
 "  VISIT_ALREADY_PAID: 'This visit is already paid in full.',\n  VISIT_WRITTEN_OFF:\n    'This visit was written off; the owner must undo the write-off before it takes a payment.',\n  VISIT_HAS_CUSTOMER: \"This visit is already another customer's debt.\",\n"),
])
edit('apps/api/src/shared/errors/constraintCodes.ts', [
("  payments_visit_uncharged: { type: 'conflict', code: 'VISIT_NOT_PRICED' },\n",
 "  payments_visit_uncharged: { type: 'conflict', code: 'VISIT_NOT_PRICED' },\n  payments_visit_written_off: { type: 'conflict', code: 'VISIT_WRITTEN_OFF' },\n"),
])

# --- visits
edit('apps/api/src/modules/visits/visits.repository.ts', [
("""    /** Clears the visit's write-off. */""",
"""    /** Sets the customer the visit's unpaid rest is left to. */
    leaveTo(visitId: number, customerId: number, tx: Tx): Promise<DeskVisitRow> {
      return tx.visit.update({ where: { id: visitId }, data: { customerId }, select: DESK_VISIT });
    },

    /** Clears the visit's write-off. */"""),
])
edit('apps/api/src/modules/visits/visits.service.ts', [
("""    /**
     * Writes the visit off, in the caller's transaction (under the space's lock and the visit's),""",
"""    /**
     * Leaves a closed visit's unpaid rest to this customer, in the caller's transaction (under the
     * space's lock and the visit's); audited `visit.leftToCustomer`.
     */
    async leaveTo(
      actorId: number,
      spaceId: number,
      visitId: number,
      customerId: number,
      tx: Tx,
    ): Promise<DeskVisit> {
      const row = await repository.leaveTo(visitId, customerId, tx);
      await audit(
        {
          actorId,
          action: 'visit.leftToCustomer',
          entityType: 'visit',
          entityId: visitId,
          spaceId,
          after: { customerId },
        },
        tx,
      );
      return toDeskVisit(row);
    },

    /**
     * Writes the visit off, in the caller's transaction (under the space's lock and the visit's),"""),
])

# --- desk
edit('apps/api/src/modules/desk/desk.service.ts', [
("""import type { CheckOutVisitRequest, VisitCheckOut } from '@masaha/shared/desk';""",
"""import type {
  CheckOutVisitRequest,
  ReceivedPayment,
  ReceivePaymentRequest,
  VisitCheckOut,
} from '@masaha/shared/desk';"""),
("""  /** What the locked visit was paid and still owes, read under its lock. */""",
"""  /**
   * The customer a visit's unpaid part is left to (data model › Unpaid visit), one rule for the
   * check-out and the later payment: a visit with a customer keeps it, and needs no phone, but a
   * phone that is not its customer's is refused (`VISIT_HAS_CUSTOMER`); a visit with none needs a
   * phone, whose customer is found among those not archived, or created with the name given, else
   * the visit's (which a visit with no customer has, by its `CHECK`).
   */
  async function customerFor(
    actor: Actor,
    space: LoadedSpace,
    { visit, visitorName }: LockedVisit,
    { phone, customerName }: { phone?: string | undefined; customerName?: string | undefined },
    tx: Tx,
  ): Promise<number> {
    if (visit.customer) {
      if (phone !== undefined && phone !== visit.customer.phone) {
        throw AppError.conflict('VISIT_HAS_CUSTOMER');
      }
      return visit.customer.id;
    }
    if (!phone) throw AppError.validation({ phone: ['required'] });
    const name = customerName ?? visitorName ?? '';
    return (
      await customers.findOrCreateByPhone(
        { spaceId: space.id, phone, name, actorId: actor.id },
        tx,
      )
    ).id;
  }

  /** What the locked visit was paid and still owes, read under its lock. */"""),
("""        const paid = request.payment?.amountAgorot ?? 0;
        const leftUnpaid = charge === null || paid < charge.amountAgorot;
        let customerId = locked.customerId;
        if (leftUnpaid) {
          if (!request.phone) throw AppError.validation({ phone: ['required'] });
          const name = request.customerName ?? locked.visitorName ?? '';
          customerId = (
            await customers.findOrCreateByPhone(
              { spaceId: space.id, phone: request.phone, name, actorId: actor.id },
              tx,
            )
          ).id;
        }
""",
"""        const paid = request.payment?.amountAgorot ?? 0;
        const leftUnpaid = charge === null || paid < charge.amountAgorot;
        const customerId = leftUnpaid
          ? await customerFor(actor, space, locked, request, tx)
          : locked.customerId;
"""),
("""    /**
     * Writes off what a closed, priced visit still owes (K6), the owner's, in one transaction and""",
"""    /**
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
        const locked = await visits.lockIn(space.id, visitId, tx);
        if (!locked) throw AppError.notFound(undefined, 'Visit not found');

        const recorded = await payments.findByKey(space.id, key, tx);
        if (recorded && recorded.visitId !== visitId) {
          throw AppError.conflict(undefined, 'This idempotency key paid another item');
        }
        if (recorded) {
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
          { spaceId: space.id, visitId, key, ...payment, recordedById: actor.id, receivedAt: now() },
          tx,
        );
        const { paidAgorot, balanceAgorot } = await balanceOf(space, locked, tx);
        // The ledger took the payment, so the visit has a charge, and a balance.
        const rest = balanceAgorot ?? 0;
        let { visit } = locked;
        if (rest > 0) {
          const customerId = await customerFor(actor, space, locked, { phone, customerName }, tx);
          if (customerId !== locked.customerId) {
            visit = await visits.leaveTo(actor.id, space.id, visitId, customerId, tx);
          }
        }
        return { visit, payment: received, paidAgorot, balanceAgorot: rest };
      });
    },

    /**
     * Writes off what a closed, priced visit still owes (K6), the owner's, in one transaction and"""),
])
edit('apps/api/src/modules/desk/desk.controller.ts', [
("""import type { CheckOutVisitRequest, VisitCheckOut } from '@masaha/shared/desk';""",
"""import type {
  CheckOutVisitRequest,
  ReceivedPayment,
  ReceivePaymentRequest,
  VisitCheckOut,
} from '@masaha/shared/desk';"""),
("""    /** 200 with the visit; a second write-off answers it as it is. */""",
"""    /** 201 every time, a retry included, with the first payment and the sums as of now. */
    receivePayment: async (req: Request, res: Response) => {
      const { userId, role } = signedIn(req);
      const received = await service.receivePayment(
        { id: userId, role },
        spaceOf(req),
        idempotencyKeyOf(res),
        req.body as ReceivePaymentRequest,
      );
      sendSuccess(res, received satisfies ReceivedPayment, { status: 201 });
    },

    /** 200 with the visit; a second write-off answers it as it is. */"""),
])
edit('apps/api/src/modules/desk/desk.manage.routes.ts', [
("""import { checkOutVisitSchema } from '@masaha/shared/desk';""",
"""import { checkOutVisitSchema, receivePaymentSchema } from '@masaha/shared/desk';"""),
("""  const mayWriteOff = requireCan('visits.writeOff');""",
"""  router.post(
    '/payments',
    requireCan('payments.record'),
    requireIdempotencyKey,
    validate(receivePaymentSchema),
    controller.receivePayment,
  );
  const mayWriteOff = requireCan('visits.writeOff');"""),
])
print('ok')
