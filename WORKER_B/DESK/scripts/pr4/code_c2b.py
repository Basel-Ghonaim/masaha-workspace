import io, os
os.chdir('C:/dev/masaha/app-b')
def edit(path, pairs):
    t = io.open(path, encoding='utf-8', newline='').read()
    for old, new in pairs:
        assert t.count(old) == 1, (path, old[:70], t.count(old))
        t = t.replace(old, new)
    io.open(path, 'w', encoding='utf-8', newline='').write(t)

edit('apps/api/src/modules/payments/payments.service.ts', [
("""    /**
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
""",
"""    /**
     * What was paid on this visit of the space and what is still owed, in the caller's transaction
     * (under the visit's lock, so it is what the ledger checks against); `balanceAgorot` is `null`
     * for a visit with no charge.
     */
    async balanceOfVisit(
      spaceId: number,
      { id, chargeAgorot }: { id: number; chargeAgorot: number | null },
      tx: Tx,
    ): Promise<{ paidAgorot: number; balanceAgorot: number | null }> {
      const paidAgorot = (await repository.paidFor(spaceId, [id], tx)).get(id) ?? 0;
      return { paidAgorot, balanceAgorot: balanceOf(chargeAgorot, paidAgorot) };
    },
"""),
])

edit('apps/api/src/modules/desk/desk.service.ts', [
("""import type { CheckInVisitRequest, DeskVisit, VisitCharge } from '@masaha/shared/visits';""",
"""import type {
  CheckInVisitRequest,
  DeskVisit,
  VisitCharge,
  WriteOffVisitRequest,
} from '@masaha/shared/visits';"""),
("""import { can, type Actor, type LoadedSpace, type SpaceLink } from '../../shared/auth/index.ts';""",
"""import {
  can,
  type Actor,
  type LoadedSpace,
  type SpaceAction,
  type SpaceLink,
} from '../../shared/auth/index.ts';"""),
("""import type { VisitsService } from '../visits/index.ts';""",
"""import type { LockedVisit, VisitsService } from '../visits/index.ts';"""),
("""  /**
   * Opens a desk write: the space's lock, which also serialises the space's desk creates, then
   * `can()` on the links read under it, so a link ended meanwhile still decides (finding 43).
   */
  async function lockAtDesk(
    actor: Actor,
    space: LoadedSpace,
    tx: Tx,
  ): Promise<readonly SpaceLink[]> {
    if (!(await spaces.lock(space.id, tx))) {
      throw AppError.notFound(undefined, 'Space not found');
    }
    const links = await space.linksUnder(tx);
    if (!can(actor, 'attendance.record', { links })) throw AppError.forbidden();
    return links;
  }
""",
"""  /**
   * Opens a desk write: the space's lock, which also serialises the space's desk creates, then
   * `can()` of the write's action on the links read under it, so a link ended meanwhile still
   * decides (finding 43).
   */
  async function lockAtDesk(
    actor: Actor,
    space: LoadedSpace,
    tx: Tx,
    action: SpaceAction = 'attendance.record',
  ): Promise<readonly SpaceLink[]> {
    if (!(await spaces.lock(space.id, tx))) {
      throw AppError.notFound(undefined, 'Space not found');
    }
    const links = await space.linksUnder(tx);
    if (!can(actor, action, { links })) throw AppError.forbidden();
    return links;
  }

  /**
   * Locks a closed visit of the space whose money the desk finishes (`FOR UPDATE`, after the
   * space's lock): not the space's → `not_found`; still open → `conflict`, no code, as it is
   * settled at its check-out.
   */
  async function lockClosed(space: LoadedSpace, visitId: number, tx: Tx): Promise<LockedVisit> {
    const locked = await visits.lockIn(space.id, visitId, tx);
    if (!locked) throw AppError.notFound(undefined, 'Visit not found');
    if (locked.open) throw AppError.conflict(undefined, 'An open visit is settled at its check-out');
    return locked;
  }

  /** What the locked visit was paid and still owes, read under its lock. */
  function balanceOf(space: LoadedSpace, { visit }: LockedVisit, tx: Tx) {
    return payments.balanceOfVisit(
      space.id,
      { id: visit.id, chargeAgorot: visit.charge?.amountAgorot ?? null },
      tx,
    );
  }
"""),
("""        return { visit, payment };
      });
    },
  };
}""",
"""        return { visit, payment };
      });
    },

    /**
     * Writes off what a closed, priced visit still owes (K6), the owner's, in one transaction and
     * in this order: the space's lock and `can()`; the visit's row; open → `conflict`; already
     * written off → the visit as it is; no charge → `VISIT_NOT_PRICED`; nothing owed →
     * `VISIT_ALREADY_PAID`. Its payments stay.
     */
    writeOffVisit(
      actor: Actor,
      space: LoadedSpace,
      visitId: number,
      { reason }: WriteOffVisitRequest,
    ): Promise<DeskVisit> {
      return runInTransaction(async (tx) => {
        await lockAtDesk(actor, space, tx, 'visits.writeOff');
        const locked = await lockClosed(space, visitId, tx);
        if (locked.visit.writeOff) return locked.visit;
        if (!locked.visit.charge) throw AppError.conflict('VISIT_NOT_PRICED');
        const { balanceAgorot } = await balanceOf(space, locked, tx);
        if (balanceAgorot === null || balanceAgorot <= 0) {
          throw AppError.conflict('VISIT_ALREADY_PAID');
        }
        return visits.writeOff(actor.id, space.id, visitId, { reason, balanceAgorot }, tx);
      });
    },

    /**
     * Undoes a visit's write-off, the owner's, in one transaction: the space's lock and `can()`;
     * the visit's row; not written off → the visit as it is.
     */
    undoWriteOff(actor: Actor, space: LoadedSpace, visitId: number): Promise<DeskVisit> {
      return runInTransaction(async (tx) => {
        await lockAtDesk(actor, space, tx, 'visits.writeOff');
        const locked = await visits.lockIn(space.id, visitId, tx);
        if (!locked) throw AppError.notFound(undefined, 'Visit not found');
        const { writeOff } = locked.visit;
        if (!writeOff) return locked.visit;
        return visits.undoWriteOff(actor.id, space.id, visitId, writeOff, tx);
      });
    },
  };
}"""),
])

edit('apps/api/src/modules/desk/desk.controller.ts', [
("""import type { CheckInVisitRequest, DeskVisit } from '@masaha/shared/visits';""",
"""import type { CheckInVisitRequest, DeskVisit, WriteOffVisitRequest } from '@masaha/shared/visits';"""),
("""      sendSuccess(res, checkOut satisfies VisitCheckOut);
    },
  };""",
"""      sendSuccess(res, checkOut satisfies VisitCheckOut);
    },

    /** 200 with the visit; a second write-off answers it as it is. */
    writeOffVisit: async (req: Request, res: Response) => {
      const { userId, role } = signedIn(req);
      const visit = await service.writeOffVisit(
        { id: userId, role },
        spaceOf(req),
        parseId(req.params.visitId),
        req.body as WriteOffVisitRequest,
      );
      sendSuccess(res, visit satisfies DeskVisit);
    },

    /** 200 with the visit; one not written off is answered as it is. */
    undoWriteOff: async (req: Request, res: Response) => {
      const { userId, role } = signedIn(req);
      const visit = await service.undoWriteOff(
        { id: userId, role },
        spaceOf(req),
        parseId(req.params.visitId),
      );
      sendSuccess(res, visit satisfies DeskVisit);
    },
  };"""),
])

edit('apps/api/src/modules/desk/desk.manage.routes.ts', [
("""import { checkInVisitSchema } from '@masaha/shared/visits';""",
"""import { checkInVisitSchema, writeOffVisitSchema } from '@masaha/shared/visits';"""),
("""    controller.checkOutVisit,
  );
  return router;""",
"""    controller.checkOutVisit,
  );
  const mayWriteOff = requireCan('visits.writeOff');
  router.post(
    '/visits/:visitId/write-off',
    mayWriteOff,
    validate(writeOffVisitSchema),
    controller.writeOffVisit,
  );
  router.delete('/visits/:visitId/write-off', mayWriteOff, controller.undoWriteOff);
  return router;"""),
])
print('ok')
