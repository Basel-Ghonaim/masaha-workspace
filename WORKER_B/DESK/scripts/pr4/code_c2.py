import io, os
os.chdir('C:/dev/masaha/app-b')
def edit(path, pairs):
    t = io.open(path, encoding='utf-8', newline='').read()
    for old, new in pairs:
        assert t.count(old) == 1, (path, old[:70], t.count(old))
        t = t.replace(old, new)
    io.open(path, 'w', encoding='utf-8', newline='').write(t)

# shared
edit('packages/shared/src/visits/requests.ts', [
("export const CHARGE_REASON_MAX_LENGTH = 200;\n", "export const CHARGE_REASON_MAX_LENGTH = 200;\nexport const WRITE_OFF_REASON_MAX_LENGTH = 200;\n"),
])
t = io.open('packages/shared/src/visits/requests.ts', encoding='utf-8', newline='').read()
t = t.rstrip('\n') + """

/** The owner's write-off of what a closed visit still owes (K6): why, 1–200 characters. */
export const writeOffVisitSchema = z.object({
  reason: textSchema(1, WRITE_OFF_REASON_MAX_LENGTH),
});
export type WriteOffVisitRequest = z.infer<typeof writeOffVisitSchema>;
"""
io.open('packages/shared/src/visits/requests.ts', 'w', encoding='utf-8', newline='').write(t)
edit('packages/shared/src/core/errors.ts', [
("  // the check-out (desk)\n  'VISIT_ALREADY_CLOSED',\n",
 "  // the check-out (desk)\n  'VISIT_ALREADY_CLOSED',\n  // a visit's debt: its write-off (desk)\n  'VISIT_ALREADY_PAID',\n"),
])
edit('apps/web/src/shared/copy/arabic/errors.ts', [
("  VISIT_NOT_PRICED: 'لا تُستلم دفعة لزيارة بلا سعر؛ سعّرها أولًا.',", "  VISIT_NOT_PRICED: 'لم تُسعَّر هذه الزيارة بعد؛ سعّرها أولًا.',"),
("  VISIT_ALREADY_CLOSED: 'سُجّل خروج هذه الزيارة من قبل، ولم تُسجَّل هذه الدفعة.',\n",
 "  VISIT_ALREADY_CLOSED: 'سُجّل خروج هذه الزيارة من قبل، ولم تُسجَّل هذه الدفعة.',\n  VISIT_ALREADY_PAID: 'دُفع مبلغ هذه الزيارة كاملًا.',\n"),
])
edit('apps/web/src/shared/copy/english/errors.ts', [
("  VISIT_NOT_PRICED: 'A visit without a price takes no payment; price it first.',", "  VISIT_NOT_PRICED: 'This visit has no price yet; price it first.',"),
("  VISIT_ALREADY_CLOSED: 'This visit was already checked out; this payment was not recorded.',\n",
 "  VISIT_ALREADY_CLOSED: 'This visit was already checked out; this payment was not recorded.',\n  VISIT_ALREADY_PAID: 'This visit is already paid in full.',\n"),
])

# can
edit('apps/api/src/shared/auth/can.ts', [
("  'space.auditLog.read': 'owner',\n", "  'space.auditLog.read': 'owner',\n  /** A visit's unpaid rest written off, and the write-off undone (K6). */\n  'visits.writeOff': 'owner',\n"),
])

# visits repository
edit('apps/api/src/modules/visits/visits.repository.ts', [
("""    /** The space's visits closed by the auto check-out, each with its charge. */
    autoClosedIn(spaceId: number): Promise<{ id: number; chargeAgorot: number | null }[]> {
      return prisma.visit.findMany({
        where: { spaceId, checkoutMethod: 'AUTO' },""",
"""    /** The space's visits closed by the auto check-out and not written off, each with its charge. */
    autoClosedIn(spaceId: number): Promise<{ id: number; chargeAgorot: number | null }[]> {
      return prisma.visit.findMany({
        where: { spaceId, checkoutMethod: 'AUTO', writtenOffAt: null },"""),
("""     * A page of the space's visits closed by the auto check-out, but these, the latest closed
     * first, then by id, and how many there are.""",
"""     * A page of the space's visits closed by the auto check-out and not written off, but these,
     * the latest closed first, then by id, and how many there are."""),
("""      const where = { spaceId, checkoutMethod: 'AUTO' as const, id: { notIn: [...exceptIds] } };""",
"""      const where = {
        spaceId,
        checkoutMethod: 'AUTO' as const,
        writtenOffAt: null,
        id: { notIn: [...exceptIds] },
      };"""),
("""    /** The space's open visits, the earliest checked in first, then by id. */""",
"""    /** Writes the visit off: when, by whom and why. */
    writeOff(
      visitId: number,
      { at, byId, reason }: { at: Date; byId: number; reason: string },
      tx: Tx,
    ): Promise<DeskVisitRow> {
      return tx.visit.update({
        where: { id: visitId },
        data: { writtenOffAt: at, writtenOffById: byId, writeOffReason: reason },
        select: DESK_VISIT,
      });
    },

    /** Clears the visit's write-off. */
    undoWriteOff(visitId: number, tx: Tx): Promise<DeskVisitRow> {
      return tx.visit.update({
        where: { id: visitId },
        data: { writtenOffAt: null, writtenOffById: null, writeOffReason: null },
        select: DESK_VISIT,
      });
    },

    /** The space's open visits, the earliest checked in first, then by id. */"""),
])

# visits service
edit('apps/api/src/modules/visits/visits.service.ts', [
("""    /**
     * Closes the visit at the desk, in the caller's transaction, audited `visit.checkedOut` with the""",
"""    /**
     * Writes the visit off, in the caller's transaction (under the space's lock and the visit's),
     * now, by the actor, with why; audited `visit.writtenOff` with the balance written off.
     */
    async writeOff(
      actorId: number,
      spaceId: number,
      visitId: number,
      { reason, balanceAgorot }: { reason: string; balanceAgorot: number },
      tx: Tx,
    ): Promise<DeskVisit> {
      const row = await repository.writeOff(visitId, { at: now(), byId: actorId, reason }, tx);
      await audit(
        {
          actorId,
          action: 'visit.writtenOff',
          entityType: 'visit',
          entityId: visitId,
          spaceId,
          after: { reason, balanceAgorot },
        },
        tx,
      );
      return toDeskVisit(row);
    },

    /**
     * Undoes the visit's write-off, in the caller's transaction; audited `visit.writeOffUndone`
     * with what the write-off was.
     */
    async undoWriteOff(
      actorId: number,
      spaceId: number,
      visitId: number,
      writeOff: VisitWriteOff,
      tx: Tx,
    ): Promise<DeskVisit> {
      const row = await repository.undoWriteOff(visitId, tx);
      await audit(
        {
          actorId,
          action: 'visit.writeOffUndone',
          entityType: 'visit',
          entityId: visitId,
          spaceId,
          before: {
            writtenOffAt: writeOff.at,
            writtenOffById: writeOff.byId,
            reason: writeOff.reason,
          },
        },
        tx,
      );
      return toDeskVisit(row);
    },

    /**
     * Closes the visit at the desk, in the caller's transaction, audited `visit.checkedOut` with the"""),
("""  VisitTerms,
} from '@masaha/shared/visits';""", """  VisitTerms,
  VisitWriteOff,
} from '@masaha/shared/visits';"""),
])

# payments
edit('apps/api/src/modules/payments/payments.repository.ts', [
("""    async paidFor(spaceId: number, visitIds: readonly number[]): Promise<Map<number, number>> {
      if (visitIds.length === 0) return new Map();
      const groups = await prisma.payment.groupBy({""",
"""    async paidFor(
      spaceId: number,
      visitIds: readonly number[],
      tx: Tx = prisma,
    ): Promise<Map<number, number>> {
      if (visitIds.length === 0) return new Map();
      const groups = await tx.payment.groupBy({"""),
])
edit('apps/api/src/modules/payments/payments.service.ts', [
("""    /** Records a visit's payment, in the caller's transaction, audited `payment.recorded`. */""",
"""    /**
     * What was paid on each of these visits of the space and what is still owed, by id, in the
     * caller's transaction (under the visits' locks, so it is what the ledger checks against);
     * `balanceAgorot` is `null` for a visit with no charge.
     */
    async balancesOf(
      spaceId: number,
      visits: readonly { id: number; chargeAgorot: number | null }[],
      tx: Tx,
    ): Promise<Map<number, { paidAgorot: number; balanceAgorot: number | null }>> {
      const paid = await repository.paidFor(
        spaceId,
        visits.map(({ id }) => id),
        tx,
      );
      return new Map(
        visits.map(({ id, chargeAgorot }) => {
          const paidAgorot = paid.get(id) ?? 0;
          return [id, { paidAgorot, balanceAgorot: balanceOf(chargeAgorot, paidAgorot) }];
        }),
      );
    },

    /** Records a visit's payment, in the caller's transaction, audited `payment.recorded`. */"""),
])
print('ok')
