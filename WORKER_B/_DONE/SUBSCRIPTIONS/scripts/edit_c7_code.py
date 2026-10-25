import os
os.chdir(r'C:\dev\masaha\app-b')

def rep(p, old, new, count=1):
    s = open(p, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (p, old, s.count(old))
    s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)

p = 'apps/api/src/modules/subscriptions/subscriptions.service.ts'
rep(p, """  /**
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
""", """  /**
   * Opens a write of one subscription, in its transaction: the space's lock, `can()` of the action on
   * the links read under it (a link ended meanwhile still decides), then the subscription's row
   * (`FOR UPDATE`), not the space's → `not_found`. Answers its terms.
   */
  async function lockSubscription(
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
    return repository.termsOf(subscriptionId, tx);
  }

  /** Opens a correction (`lockSubscription`); one ended early is `SUBSCRIPTION_ENDED`. */
  async function lockForCorrection(
    actor: Actor,
    space: LoadedSpace,
    subscriptionId: number,
    action: SpaceAction,
    tx: Tx,
  ) {
    const terms = await lockSubscription(actor, space, subscriptionId, action, tx);
    if (terms.ended) throw AppError.conflict('SUBSCRIPTION_ENDED');
    return terms;
  }
""")
rep(p, """    /** Every check-in of the space's subscription, the earliest first, then by id. */
    checkInsOf(""", """    /**
     * Ends a subscription early («إنهاء الاشتراك», decision 5), in one transaction:
     * `lockSubscription` (`subscriptions.manage`); one already ended answered as it is, writing
     * nothing; else its end becomes today — its start, if it has not started; never later than its
     * end was — with who ended it and when, audited `subscription.ended`. No payment, refund or
     * proration; an open check-in on it stays open. It is `EXPIRED` from then (S5).
     */
    end(actor: Actor, space: LoadedSpace, subscriptionId: number): Promise<SubscriptionState> {
      return runInTransaction(async (tx) => {
        const terms = await lockSubscription(
          actor,
          space,
          subscriptionId,
          'subscriptions.manage',
          tx,
        );
        if (terms.ended) return stateNow(space.id, subscriptionId, tx);
        const endedAt = now();
        const today = gazaClockOf(endedAt).date;
        let endsOn = terms.startsOn !== null && terms.startsOn > today ? terms.startsOn : today;
        if (terms.endsOn !== null && terms.endsOn < endsOn) endsOn = terms.endsOn;
        await repository.end(subscriptionId, { endsOn, endedAt, endedById: actor.id }, tx);
        await audit(
          {
            actorId: actor.id,
            action: 'subscription.ended',
            entityType: 'subscription',
            entityId: subscriptionId,
            spaceId: space.id,
            before: { endsOn: terms.endsOn },
            after: { endsOn, endedAt: endedAt.toISOString() },
          },
          tx,
        );
        return stateNow(space.id, subscriptionId, tx);
      });
    },

    /** Every check-in of the space's subscription, the earliest first, then by id. */
    checkInsOf(""")
rep(p, """import type {
  CorrectPriceRequest,""", """import { gazaClockOf } from '@masaha/shared/core';
import type {
  CorrectPriceRequest,""")

p = 'apps/api/src/modules/subscriptions/subscriptions.repository.ts'
rep(p, """    /** Writes a corrected price and billing, with who typed the price and why. */""", """    /** Ends the subscription early: its new end (a Gaza date), when and by whom. */
    async end(
      id: number,
      { endsOn, endedAt, endedById }: { endsOn: string; endedAt: Date; endedById: number },
      tx: Tx,
    ): Promise<void> {
      await tx.subscription.update({
        where: { id },
        data: { endsOn: dateOf(endsOn), endedAt, endedById },
        select: { id: true },
      });
    },

    /** Writes a corrected price and billing, with who typed the price and why. */""")

p = 'apps/api/src/modules/subscriptions/subscriptions.controller.ts'
rep(p, """    /** 200 with the subscription's state; the same price and billing answer it as it is. */""", """    /** 200 with the subscription's state; one already ended is answered as it is. */
    end: async (req: Request, res: Response) => {
      const { userId, role } = signedIn(req);
      const state = await service.end(
        { id: userId, role },
        spaceOf(req),
        parseId(req.params.subscriptionId),
      );
      sendSuccess(res, state satisfies SubscriptionState);
    },

    /** 200 with the subscription's state; the same price and billing answer it as it is. */""")
p = 'apps/api/src/modules/subscriptions/subscriptions.manage.routes.ts'
rep(p, """export function createSubscriptionsManageRouter(controller: SubscriptionsController): Router {
  const router = Router();
  router.patch(
    '/subscriptions/:subscriptionId',
    requireCan('subscriptions.manage'),""", """export function createSubscriptionsManageRouter(controller: SubscriptionsController): Router {
  const router = Router();
  const mayManage = requireCan('subscriptions.manage');
  router.patch(
    '/subscriptions/:subscriptionId',
    mayManage,""")
rep(p, """    controller.correctPrice,
  );
  return router;""", """    controller.correctPrice,
  );
  router.post('/subscriptions/:subscriptionId/end', mayManage, controller.end);
  return router;""")
rep(p, "is read; the service asks `can()` again under the space's lock. The price is the owner's",
    "is read; the service asks `can()` again under the space's lock. The corrections of the limits,\n * dates and name and the end are the staff's; the price is the owner's")
print('ok')
