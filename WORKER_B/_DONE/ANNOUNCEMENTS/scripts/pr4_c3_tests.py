import io

R = 'C:/dev/masaha/app-b/'
p = R + 'apps/api/src/modules/subscriptions/closures/extension.api.test.ts'
s = io.open(p, encoding='utf-8', newline='').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)


rep("import { createCustomer, createSpace, createSubscription } from '../../../../test/factories.ts';\n",
    "import { createCustomer, createSpace, createSubscription } from '../../../../test/factories.ts';\nimport { waitingOnLock, whileHeld } from '../../../../test/locks.ts';\n")
rep("// A closure's extension of the subscriptions it covered (docs/api/api-contract.md › Announcements\n// (managed)): the preview of the days and how many it covered. Gaza is UTC+2 in November.",
    "// A closure's extension of the subscriptions it covered (docs/api/api-contract.md › Announcements\n// (managed)): the preview of the days and how many it covered, and the extension itself, once per\n// closure under one key. Gaza is UTC+2 in November.")
rep("""const preview = (caller: { authorization: string }, announcementId: number) =>
  request(app).get(pathOf(announcementId)).set('Authorization', caller.authorization);
""", """const preview = (caller: { authorization: string }, announcementId: number) =>
  request(app).get(pathOf(announcementId)).set('Authorization', caller.authorization);

function extend(
  caller: { authorization: string },
  announcementId: number,
  body: object = { days: 4 },
  key: string | null = randomUUID(),
) {
  const call = request(app)
    .post(pathOf(announcementId))
    .set('Authorization', caller.authorization)
    .send(body);
  return key === null ? call : call.set('Idempotency-Key', key);
}

const lockSpace = (tx: Pick<typeof prisma, '$queryRaw'>) =>
  tx.$queryRaw`SELECT id FROM spaces WHERE id = ${spaceId} FOR NO KEY UPDATE`;
""")
rep("""const ends = () =>
  prisma.subscription.findMany({ select: { id: true, endsOn: true }, orderBy: { id: 'asc' } });
""", """const ends = () =>
  prisma.subscription.findMany({ select: { id: true, endsOn: true }, orderBy: { id: 'asc' } });

/** Each subscription's end, `YYYY-MM-DD` or null, by id. */
async function endsById(): Promise<Map<number, string | null>> {
  return new Map(
    (await ends()).map(({ id, endsOn }) => [id, endsOn?.toISOString().slice(0, 10) ?? null]),
  );
}

const links = () =>
  prisma.subscriptionExtension.findMany({
    select: { subscriptionId: true },
    orderBy: { subscriptionId: 'asc' },
  });
""")
rep("""  it("an upcoming closure is ANNOUNCEMENT_NOT_STARTED; an announcement of another type, a deleted one, another space's, not_found", async () => {
    const upcoming = await closure({ startsAt: new Date('2026-11-11T08:00:00+02:00') });
    const response = await preview(owner, upcoming.id);
    expect(response.status).toBe(409);
    expect(errorOf(response).code).toBe('ANNOUNCEMENT_NOT_STARTED');

    const outage = await closure({ type: 'OUTAGE' });
    const deleted = await closure({ deletedAt: new Date('2026-11-09T08:00:00+02:00') });
    const elsewhere = await closure({ spaceId: otherSpaceId });
    for (const id of [outage.id, deleted.id, elsewhere.id, 999_999]) {
      const missing = await preview(owner, id);
      expect(missing.status).toBe(404);
      expect(errorOf(missing).type).toBe('not_found');
    }
""", """  it("an upcoming closure is ANNOUNCEMENT_NOT_STARTED; an announcement of another type, a deleted one, another space's, not_found; 0 or 366 days 422", async () => {
    await subscriptionsAround();
    const before = await ends();
    const upcoming = await closure({ startsAt: new Date('2026-11-11T08:00:00+02:00') });
    for (const response of [await preview(owner, upcoming.id), await extend(owner, upcoming.id)]) {
      expect(response.status).toBe(409);
      expect(errorOf(response).code).toBe('ANNOUNCEMENT_NOT_STARTED');
    }

    const outage = await closure({ type: 'OUTAGE' });
    const deleted = await closure({ deletedAt: new Date('2026-11-09T08:00:00+02:00') });
    const elsewhere = await closure({ spaceId: otherSpaceId });
    for (const id of [outage.id, deleted.id, elsewhere.id, 999_999]) {
      for (const missing of [await preview(owner, id), await extend(owner, id)]) {
        expect(missing.status).toBe(404);
        expect(errorOf(missing).type).toBe('not_found');
      }
    }

    const { id: running } = await closure();
    for (const days of [0, 366]) {
      const invalid = await extend(owner, running, { days });
      expect(invalid.status).toBe(422);
      expect(errorOf(invalid).errors).toEqual({ days: ['out_of_range'] });
    }
    expect(await ends()).toEqual(before);
    expect(await prisma.closureExtension.count()).toBe(0);
""")
s += """
describe('the extension', () => {
  it("the owner extends: each covered subscription's end moves by the days typed, one link each, audited closure.subscriptionsExtended; 201 with the count", async () => {
    const { id } = await closure();
    const { covered } = await subscriptionsAround();
    const { name } = await prisma.user.findUniqueOrThrow({ where: { id: owner.id } });

    // Four days, though three are proposed.
    const response = await extend(owner, id, { days: 4 });

    expect(response.status).toBe(201);
    expect(dataOf(response)).toEqual({
      announcementId: id,
      days: 4,
      subscriptions: 5,
      appliedAt: NOW.toISOString(),
      appliedBy: { id: owner.id, name },
    });
    const after = await endsById();
    expect(after.get(covered.through.id)).toBe('2026-12-04');
    expect(after.get(covered.endsDuring.id)).toBe('2026-11-13');
    expect(after.get(covered.endsOnFirstDay.id)).toBe('2026-11-12');
    expect(after.get(covered.startsOnLastDay.id)).toBe('2026-12-14');
    expect(after.get(covered.noStart.id)).toBe('2026-11-24');
    const coveredIds = Object.values(covered)
      .map((row) => row.id)
      .sort((a, b) => a - b);
    expect(await links()).toEqual(coveredIds.map((subscriptionId) => ({ subscriptionId })));
    expect(await auditEntries()).toEqual([
      {
        actorId: owner.id,
        action: 'closure.subscriptionsExtended',
        entityType: 'announcement',
        entityId: id,
        spaceId,
        before: null,
        after: { days: 4, subscriptionIds: coveredIds },
      },
    ]);
  });

  it("which move: one running through, one ending during it; not one starting after its last day, one ended before its first, one ended early, one with no end, another space's", async () => {
    const { id } = await closure();
    const { covered, notCovered } = await subscriptionsAround();
    const before = await endsById();

    expect((await extend(owner, id, { days: 2 })).status).toBe(201);

    const after = await endsById();
    expect(after.get(covered.through.id)).toBe('2026-12-02');
    expect(after.get(covered.endsDuring.id)).toBe('2026-11-11');
    for (const { id: untouched } of Object.values(notCovered)) {
      expect(after.get(untouched)).toBe(before.get(untouched));
    }
  });

  it('reception is 403 before the key or body is read; a stranger and the admin not_found', async () => {
    const { id } = await closure();
    await subscriptionsAround();
    const before = await ends();

    const refused = await extend(reception, id, { days: 'many' }, null);
    expect(refused.status).toBe(403);
    expect(errorOf(refused).type).toBe('forbidden');
    for (const caller of [stranger, admin]) {
      expect((await extend(caller, id)).status).toBe(404);
    }
    expect(await ends()).toEqual(before);
    expect(await prisma.closureExtension.count()).toBe(0);
  });

  it('a retry with the same key answers the first, 201, moving nothing twice; another key is CLOSURE_ALREADY_EXTENDED; a key that extended another closure is a conflict', async () => {
    const { id } = await closure();
    const { covered } = await subscriptionsAround();
    const key = randomUUID();
    const first = await extend(owner, id, { days: 4 }, key);
    expect(first.status).toBe(201);

    const retry = await extend(owner, id, { days: 4 }, key);
    expect(retry.status).toBe(201);
    expect(dataOf(retry)).toEqual(dataOf(first));
    expect((await endsById()).get(covered.through.id)).toBe('2026-12-04');

    const again = await extend(owner, id, { days: 4 });
    expect(again.status).toBe(409);
    expect(errorOf(again).code).toBe('CLOSURE_ALREADY_EXTENDED');

    const other = await closure();
    const reused = await extend(owner, other.id, { days: 4 }, key);
    expect(reused.status).toBe(409);
    expect(errorOf(reused).code).toBeUndefined();

    expect((await endsById()).get(covered.through.id)).toBe('2026-12-04');
    expect(await prisma.closureExtension.count()).toBe(1);
    expect(await auditEntries()).toHaveLength(1);
  });

  it('two owners at once with two keys make one extension', async () => {
    const { id } = await closure();
    const { covered } = await subscriptionsAround();
    let both: Promise<request.Response[]> | undefined;
    await prisma.$transaction(
      async (tx) => {
        await lockSpace(tx);
        both = Promise.all([extend(owner, id), extend(owner, id)]);
        await waitingOnLock({ count: 2 });
      },
      { timeout: 10_000 },
    );
    if (!both) throw new Error('The requests never started');
    const answers = await both;

    expect(answers.map(({ status }) => status).sort()).toEqual([201, 409]);
    const refused = answers.find(({ status }) => status === 409);
    expect(refused && errorOf(refused).code).toBe('CLOSURE_ALREADY_EXTENDED');
    expect(await prisma.closureExtension.count()).toBe(1);
    expect((await endsById()).get(covered.through.id)).toBe('2026-12-04');
  });

  it('a subscription ended early, or added, while the extension waits is read as committed', async () => {
    const { id } = await closure();
    const { covered } = await subscriptionsAround();
    let added = 0;

    const response = await whileHeld(
      lockSpace,
      () => extend(owner, id, { days: 4 }),
      async (tx) => {
        await tx.subscription.update({
          where: { id: covered.through.id },
          data: { endedAt: new Date('2026-11-10T09:00:00+02:00'), endedById: owner.id },
        });
        const customer = await tx.customer.findFirstOrThrow({ where: { spaceId } });
        ({ id: added } = await tx.subscription.create({
          data: {
            spaceId,
            customerId: customer.id,
            idempotencyKey: randomUUID(),
            name: 'أسبوعي',
            billing: 'FIXED',
            priceAgorot: 10_000,
            startsOn: day('2026-11-10'),
            endsOn: day('2026-11-16'),
          },
        }));
      },
    );

    expect(response.status).toBe(201);
    expect(dataOf(response)).toMatchObject({ subscriptions: 5 });
    const after = await endsById();
    expect(after.get(covered.through.id)).toBe('2026-11-30');
    expect(after.get(added)).toBe('2026-11-20');
  });

  it('a closure whose end moved earlier while the extension waits is extended on its new span', async () => {
    const { id } = await closure();
    const { covered } = await subscriptionsAround();

    const response = await whileHeld(
      lockSpace,
      () => extend(owner, id, { days: 4 }),
      // Ended at Monday's midnight: Sunday only.
      (tx) =>
        tx.announcement.update({
          where: { id },
          data: { endsAt: new Date('2026-11-09T00:00:00+02:00') },
        }),
    );

    expect(response.status).toBe(201);
    expect(dataOf(response)).toMatchObject({ subscriptions: 4 });
    const after = await endsById();
    expect(after.get(covered.startsOnLastDay.id)).toBe('2026-12-10');
    expect(after.get(covered.endsOnFirstDay.id)).toBe('2026-11-12');
  });

  it('an owner whose link ended while waiting is refused 403', async () => {
    const { id } = await closure();
    await subscriptionsAround();
    const before = await ends();

    const response = await whileHeld(
      lockSpace,
      () => extend(owner, id),
      (tx) =>
        tx.spaceManager.update({
          where: { spaceId_userId: { spaceId, userId: owner.id } },
          data: { deactivatedAt: new Date() },
        }),
    );

    expect(response.status).toBe(403);
    expect(await ends()).toEqual(before);
    expect(await prisma.closureExtension.count()).toBe(0);
    expect(await auditEntries()).toEqual([]);
  });
});
"""
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
