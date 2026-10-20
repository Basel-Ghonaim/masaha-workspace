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

append('packages/shared/src/desk/requests.ts', """
/**
 * «تسجيل دينًا»: a closed visit's unpaid rest left to the customer with this phone, found or
 * created with this name (else the visit's), with no payment.
 */
export const leaveToCustomerSchema = z.object({
  phone: phoneSchema,
  customerName: textSchema(1, VISITOR_NAME_MAX_LENGTH).optional(),
});
export type LeaveToCustomerRequest = z.infer<typeof leaveToCustomerSchema>;
""")

edit('apps/api/src/modules/desk/desk.service.ts', [
("""import type {
  CheckOutVisitRequest,
  ReceivedPayment,""",
"""import type {
  CheckOutVisitRequest,
  LeaveToCustomerRequest,
  ReceivedPayment,"""),
("""    /**
     * Writes off what a closed, priced visit still owes (K6), the owner's, in one transaction and""",
"""    /**
     * «تسجيل دينًا» (DK-012): leaves a closed visit's unpaid rest to the phone's customer, with no
     * payment, in one transaction and in this order: the space's lock and `can()`; the visit's row;
     * open → `conflict`; written off → `VISIT_WRITTEN_OFF`; nothing owed → `VISIT_ALREADY_PAID` (an
     * unpriced visit has a debt to leave); the unpaid-part rule; the visit's own customer again →
     * the visit as it is.
     */
    leaveToCustomer(
      actor: Actor,
      space: LoadedSpace,
      visitId: number,
      request: LeaveToCustomerRequest,
    ): Promise<DeskVisit> {
      return runInTransaction(async (tx) => {
        await lockAtDesk(actor, space, tx, 'payments.record');
        const locked = await lockClosed(space, visitId, tx);
        if (locked.visit.writeOff) throw AppError.conflict('VISIT_WRITTEN_OFF');
        const { balanceAgorot } = await balanceOf(space, locked, tx);
        if (balanceAgorot !== null && balanceAgorot <= 0) {
          throw AppError.conflict('VISIT_ALREADY_PAID');
        }
        const customerId = await customerFor(actor, space, locked, request, tx);
        if (customerId === locked.customerId) return locked.visit;
        return visits.leaveTo(actor.id, space.id, visitId, customerId, tx);
      });
    },

    /**
     * Writes off what a closed, priced visit still owes (K6), the owner's, in one transaction and"""),
])
edit('apps/api/src/modules/desk/desk.controller.ts', [
("""import type {
  CheckOutVisitRequest,
  ReceivedPayment,""",
"""import type {
  CheckOutVisitRequest,
  LeaveToCustomerRequest,
  ReceivedPayment,"""),
("""    /** 200 with the visit; a second write-off answers it as it is. */""",
"""    /** 200 with the visit; the same phone again answers it as it is. */
    leaveToCustomer: async (req: Request, res: Response) => {
      const { userId, role } = signedIn(req);
      const visit = await service.leaveToCustomer(
        { id: userId, role },
        spaceOf(req),
        parseId(req.params.visitId),
        req.body as LeaveToCustomerRequest,
      );
      sendSuccess(res, visit satisfies DeskVisit);
    },

    /** 200 with the visit; a second write-off answers it as it is. */"""),
])
edit('apps/api/src/modules/desk/desk.manage.routes.ts', [
("""import { checkOutVisitSchema, receivePaymentSchema } from '@masaha/shared/desk';""",
"""import {
  checkOutVisitSchema,
  leaveToCustomerSchema,
  receivePaymentSchema,
} from '@masaha/shared/desk';"""),
("""  const mayWriteOff = requireCan('visits.writeOff');""",
"""  router.put(
    '/visits/:visitId/customer',
    requireCan('payments.record'),
    validate(leaveToCustomerSchema),
    controller.leaveToCustomer,
  );
  const mayWriteOff = requireCan('visits.writeOff');"""),
])
print('ok')
