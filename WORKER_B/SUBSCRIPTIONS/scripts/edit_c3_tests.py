import os
os.chdir(r'C:\dev\masaha\app-b')

def rep(p, old, new, count=1):
    s = open(p, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (p, old, s.count(old))
    s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)

# U5, the payment part (shared)
p = 'packages/shared/src/desk/requests.unit.test.ts'
rep(p, """    expect(errorsOf({ visitId: 7, ...payment, phone: '12345' })).toEqual({
      phone: ['invalid_format'],
    });
  });
});""", """    expect(errorsOf({ visitId: 7, ...payment, phone: '12345' })).toEqual({
      phone: ['invalid_format'],
    });
  });

  it('a payment names exactly one item: a visit or a subscription', () => {
    const errorsOf = (input: unknown) => {
      const result = receivePaymentSchema.safeParse(input);
      return result.success ? null : toFieldErrors(result.error.issues, input);
    };
    const payment = { amountAgorot: 1_000, method: 'CASH' };
    expect(receivePaymentSchema.parse({ subscriptionId: 4, ...payment })).toEqual({
      subscriptionId: 4,
      ...payment,
    });
    expect(errorsOf({ visitId: 7, subscriptionId: 4, ...payment })).toEqual({
      subscriptionId: ['invalid_choice'],
    });
    expect(errorsOf({ subscriptionId: 0, ...payment })).toEqual({
      subscriptionId: ['out_of_range'],
    });
    // Neither: the visit's field is required, beside the body's other errors.
    expect(errorsOf({ amountAgorot: 0, method: 'CASH' })).toEqual({
      visitId: ['required'],
      amountAgorot: ['out_of_range'],
    });
  });
});""")

# T10–T14 (the desk's payments file)
p = 'apps/api/src/modules/desk/payments.api.test.ts'
rep(p, "import { createCustomer, createSpace, createVisit, stay } from '../../../test/factories.ts';",
    "import {\n  createCustomer,\n  createSpace,\n  createSubscription,\n  createVisit,\n  stay,\n} from '../../../test/factories.ts';")
rep(p, """    expect(dataOf(response)).toMatchObject({
      visit: { id, customer: null, charge: { amountAgorot: 2_500 } },
      payment: {""", """    expect(dataOf(response)).toMatchObject({
      visit: { id, customer: null, charge: { amountAgorot: 2_500 } },
      subscription: null,
      payment: {""")
s = open(p, encoding='utf-8', newline='').read().rstrip('\n')
s += """

describe("receiving a subscription's payment", () => {
  /** Sara's subscription of the space (another's when told): a month at ₪300, unless overridden. */
  async function subscription(more: Record<string, unknown> = {}, space = spaceId) {
    const customer = await createCustomer(space, { name: 'Sara', phone: PHONE });
    return createSubscription(customer, {
      startsOn: new Date('2026-10-01'),
      endsOn: new Date('2026-10-30'),
      billing: 'FIXED',
      priceAgorot: 30_000,
      ...more,
    });
  }

  const onSubscription = (subscriptionId: number, amountAgorot: number) => ({
    subscriptionId,
    amountAgorot,
    method: 'CASH',
  });

  it('a payment on a subscription of the space is recorded, 201, with what remains; audited payment.recorded; a retry answers it', async () => {
    const { id, customerId } = await subscription();
    const key = randomUUID();

    const response = await receive(reception, onSubscription(id, 10_000), key);
    expect(response.status).toBe(201);
    const payment = await prisma.payment.findFirstOrThrow();
    expect(payment).toMatchObject({ subscriptionId: id, visitId: null, amountAgorot: 10_000 });
    expect(dataOf(response)).toEqual({
      visit: null,
      subscription: expect.objectContaining({
        id,
        customerId,
        status: 'ACTIVE',
        dueAgorot: 30_000,
      }) as unknown,
      payment: {
        id: payment.id,
        amountAgorot: 10_000,
        method: 'CASH',
        note: null,
        receivedAt: '2026-10-18T07:20:00.000Z',
        recordedById: reception.id,
      },
      paidAgorot: 10_000,
      balanceAgorot: 20_000,
    });
    expect(await auditEntries()).toEqual([
      {
        actorId: reception.id,
        action: 'payment.recorded',
        entityType: 'payment',
        entityId: payment.id,
        spaceId,
        before: null,
        after: { subscriptionId: id, amountAgorot: 10_000, method: 'CASH' },
      },
    ]);

    const retry = await receive(reception, onSubscription(id, 10_000), key);
    expect(retry.status).toBe(201);
    expect(dataOf(retry)).toEqual(dataOf(response));
    expect(await paymentCount()).toBe(1);
  });

  it('a fixed subscription is never paid above its price: PAYMENT_EXCEEDS_DUE, writing nothing; a per-hour one takes credit', async () => {
    const { id } = await subscription();
    expect((await receive(owner, onSubscription(id, 25_000))).status).toBe(201);

    const above = await receive(owner, onSubscription(id, 10_000));
    expect(above.status).toBe(409);
    expect(errorOf(above).code).toBe('PAYMENT_EXCEEDS_DUE');
    expect(await paymentCount()).toBe(1);

    // Nothing attended yet: ₪50 paid ahead is credit, a balance below zero.
    const hourly = await createSubscription(
      await createCustomer(spaceId, { name: 'Rami' }),
      { billing: 'PER_HOUR', priceAgorot: 500 },
    );
    const credit = await receive(owner, onSubscription(hourly.id, 5_000));
    expect(credit.status).toBe(201);
    expect(dataOf(credit)).toMatchObject({ paidAgorot: 5_000, balanceAgorot: -5_000 });
  });

  it('exactly one item: both or neither refused 422 before anything is read', async () => {
    const { id } = await subscription();
    const visit = await closed(2_500);

    const both = await receive(owner, { ...onSubscription(id, 1_000), visitId: visit.id });
    expect(both.status).toBe(422);
    expect(errorOf(both).errors).toEqual({ subscriptionId: ['invalid_choice'] });
    const neither = await receive(owner, { amountAgorot: 1_000, method: 'CASH' });
    expect(neither.status).toBe(422);
    expect(errorOf(neither).errors).toEqual({ visitId: ['required'] });
    expect(await paymentCount()).toBe(0);
  });

  it("another space's subscription is invalid_choice on subscriptionId; a key that paid a visit is a conflict, and the reverse", async () => {
    const theirs = await subscription({}, otherSpaceId);
    const foreign = await receive(owner, onSubscription(theirs.id, 1_000));
    expect(foreign.status).toBe(422);
    expect(errorOf(foreign).errors).toEqual({ subscriptionId: ['invalid_choice'] });

    const { id } = await subscription();
    const visit = await closed(2_500);
    const visitKey = randomUUID();
    expect((await receive(owner, cash(visit.id, 1_000, { phone: OTHER_PHONE }), visitKey)).status).toBe(
      201,
    );
    const reused = await receive(owner, onSubscription(id, 1_000), visitKey);
    expect(reused.status).toBe(409);
    expect(errorOf(reused).code).toBeUndefined();

    const subscriptionKey = randomUUID();
    expect((await receive(owner, onSubscription(id, 1_000), subscriptionKey)).status).toBe(201);
    const reusedForVisit = await receive(owner, cash(visit.id, 500), subscriptionKey);
    expect(reusedForVisit.status).toBe(409);
    expect(await paymentCount()).toBe(2);
  });

  it("an ended subscription, and an archived customer's, still take a payment", async () => {
    const ended = await subscription({
      endsOn: new Date('2026-10-12'),
      endedAt: new Date('2026-10-12T09:00:00+03:00'),
      endedById: owner.id,
    });
    const response = await receive(owner, onSubscription(ended.id, 5_000));
    expect(response.status).toBe(201);
    expect(dataOf(response)).toMatchObject({ subscription: { status: 'EXPIRED' } });

    await prisma.customer.update({
      where: { id: ended.customerId },
      data: { archivedAt: new Date() },
    });
    expect((await receive(owner, onSubscription(ended.id, 5_000))).status).toBe(201);
    expect(await paymentCount()).toBe(2);
  });
});
"""
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
