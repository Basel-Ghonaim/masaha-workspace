// today: the managed space's morning. Safe to run more than once: every record it makes has a key
// derived from the date, so a second run finds them and adds nothing.
//   cd <app>/apps/api
//   npx tsx --conditions=@masaha/source --env-file=.env <folder>/scripts/today.ts
import {
  auditAt,
  guard,
  hhmm,
  keyOf,
  loadApp,
  MANAGED_SLUG,
  OWNER_EMAIL,
  RECEPTION_EMAIL,
  rngOf,
  runningOn,
  WALK_INS,
  writeCheckIn,
  writeDay,
  writePayment,
  writeVisit,
  type DayContext,
} from './lib.ts';

guard();
const { db, chargeOf, gazaClock } = await loadApp();
// DEMO_NOW (an ISO instant) only rehearses a later morning on the dry-run database.
const NOW = process.env.DEMO_NOW ? new Date(process.env.DEMO_NOW) : new Date();
const at = gazaClock(NOW);
const audit = auditAt(db);
const log = (...a: unknown[]) => console.log(`[${new Date().toISOString().slice(11, 19)}]`, ...a);

try {
  const space = await db.space.findUnique({
    where: { slug: MANAGED_SLUG },
    include: { hours: true, shifts: true, prices: true, settings: true, occupancy: true },
  });
  if (!space) throw new Error('No pal-hub: run build-demo first.');
  const owner = await db.user.findUniqueOrThrow({ where: { email: OWNER_EMAIL } });
  const reception = await db.user.findUniqueOrThrow({ where: { email: RECEPTION_EMAIL } });
  const price = (period: string, audience: string) =>
    space.prices.find((p: any) => p.period === period && p.audience === audience && p.shiftId === null && p.labelAr === null)?.amountAgorot ?? null;
  const rate = (audience: 'GENERAL' | 'STUDENT') => ({
    hourAgorot: price('HOUR', audience) ?? price('HOUR', 'GENERAL'),
    dayAgorot: price('DAY', audience) ?? price('DAY', 'GENERAL'),
  });
  const week: (readonly [number, number] | null)[] = [0, 1, 2, 3, 4, 5, 6].map((d) => {
    const row = space.hours.find((h: any) => h.dayOfWeek === d);
    return row && !row.isClosed ? ([row.opensMinute, row.closesMinute] as const) : null;
  });
  const settings = space.settings;
  const rule = { rounding: settings.visitRounding, roundingMinutes: settings.visitRoundingMinutes, capAtDayPrice: settings.visitCapAtDayPrice };

  // The days a closure covered, among the last week.
  const closures = await db.announcement.findMany({ where: { spaceId: space.id, type: 'CLOSURE', deletedAt: null } });
  const closedOffsets = new Set<number>();
  for (let offset = -7; offset <= 0; offset += 1) {
    const from = at.time(offset, '00:00');
    const to = at.time(offset + 1, '00:00');
    const open = week[at.date(offset).getUTCDay()];
    if (!open) continue;
    const opensAt = at.time(offset, hhmm(open[0]));
    for (const c of closures) {
      if (c.startsAt <= opensAt && (c.endsAt === null || c.endsAt >= to)) closedOffsets.add(offset);
      void from;
    }
  }

  const ctx: DayContext = {
    db, audit, at, chargeOf, spaceId: space.id, ownerId: owner.id, receptionId: reception.id, rule, week,
    shifts: new Map(space.shifts.map((s: any) => [s.id, { startsMinute: s.startsMinute, endsMinute: s.endsMinute }])),
    ratesOn: (_offset, audience) => rate(audience),
    closedOffsets,
  };

  // 1. Stays left open from an earlier day close at their day's closing, as the app's job closes them.
  const startOfToday = at.time(0, '00:00');
  const dueOf = (checkedInAt: Date) => {
    const offset = Math.round((at.date(0).getTime() - new Date(`${checkedInAt.toLocaleDateString('en-CA', { timeZone: 'Asia/Gaza' })}T00:00:00Z`).getTime()) / 86_400_000);
    const open = week[at.date(-offset).getUTCDay()];
    return open ? at.time(-offset, hhmm(Math.min(open[1], 1439))) : at.time(-offset + 1, '00:00');
  };
  let closed = 0;
  for (const v of await db.visit.findMany({ where: { spaceId: space.id, checkedOutAt: null, checkedInAt: { lt: startOfToday } } })) {
    const dueAt = dueOf(v.checkedInAt);
    const charge = chargeOf({ from: v.checkedInAt, to: dueAt }, { hourAgorot: v.hourRateAgorot, dayAgorot: v.dayRateAgorot }, rule);
    await db.visit.update({
      where: { id: v.id },
      data: { checkedOutAt: dueAt, checkoutMethod: 'AUTO', roundingRule: charge?.roundingRule ?? null, roundingMinutes: charge?.roundingMinutes ?? null, capApplied: charge?.capApplied ?? null, chargeAgorot: charge?.amountAgorot ?? null, updatedAt: dueAt },
    });
    await audit(dueAt, { actorId: null, action: 'visit.autoCheckedOut', entityType: 'visit', entityId: v.id, spaceId: space.id, after: { checkedOutAt: dueAt.toISOString(), chargeAgorot: charge?.amountAgorot ?? null } });
    closed += 1;
  }
  for (const c of await db.checkIn.findMany({ where: { spaceId: space.id, checkedOutAt: null, checkedInAt: { lt: startOfToday } } })) {
    const dueAt = dueOf(c.checkedInAt);
    await db.checkIn.update({ where: { id: c.id }, data: { checkedOutAt: dueAt, checkoutMethod: 'AUTO', updatedAt: dueAt } });
    await audit(dueAt, { actorId: null, action: 'checkIn.autoCheckedOut', entityType: 'checkIn', entityId: c.id, spaceId: space.id, after: { checkedOutAt: dueAt.toISOString() } });
    closed += 1;
  }
  log(`stays left open from earlier days, closed at closing: ${closed}`);

  // 2. A whole day for any of the last week's open days with no history yet.
  let filled = 0;
  for (let offset = -7; offset <= -1; offset += 1) {
    const date = at.date(offset).toISOString().slice(0, 10);
    const open = week[at.date(offset).getUTCDay()];
    if (!open || closedOffsets.has(offset)) continue;
    const marker = await db.visit.findUnique({ where: { spaceId_idempotencyKey: { spaceId: space.id, idempotencyKey: keyOf(`hist/${date}/visit/0`) } } });
    if (marker) continue;
    const done = await writeDay(ctx, offset, { tag: 'hist' });
    log(`filled ${date}: ${done.checkIns} check-ins, ${done.visits} visits`);
    filled += 1;
  }

  // 3. Yesterday's visits the system closed at closing: most paid this morning.
  const today = at.date(0).toISOString().slice(0, 10);
  const open = week[at.date(0).getUTCDay()];
  const minuteNow = Math.floor((NOW.getTime() - startOfToday.getTime()) / 60_000);
  const rng = rngOf(`today/${today}`);
  if (open && minuteNow > open[0] + 30) {
    const late = await db.visit.findMany({
      where: { spaceId: space.id, checkoutMethod: 'AUTO', customerId: null, chargeAgorot: { not: null }, payments: { none: {} }, checkedOutAt: { gte: at.time(-1, '00:00'), lt: startOfToday } },
      orderBy: { id: 'asc' },
    });
    for (const v of late) {
      if (!rngOf(`late/${v.id}`).chance(0.6)) continue;
      await writePayment(ctx, { key: keyOf(`late/${v.id}`), item: { visitId: v.id }, amountAgorot: v.chargeAgorot, method: 'CASH', byId: reception.id, at: at.time(0, hhmm(open[0] + 25)) });
    }
  }

  // 4. Today: people present now, a few who came and went, a payment on a debt.
  let present = 0;
  if (!open || closedOffsets.has(0)) {
    log('pal-hub is closed today: nobody present.');
  } else {
    if (minuteNow < open[0] || minuteNow >= open[1]) {
      log(`warning: now (${hhmm(Math.max(0, minuteNow))}) is outside today's hours ${hhmm(open[0])}–${hhmm(open[1])}; the app's auto check-out closes stays past closing.`);
    }
    const nowM = Math.min(Math.max(minuteNow, open[0] + 15), open[1] - 5);
    const windowFrom = Math.max(open[0], nowM - 240);
    const target = rng.int(5, 7);
    const staffNow = nowM >= 17 * 60 || at.date(0).getUTCDay() === 5 ? owner.id : reception.id;
    const instant = (m: number) => new Date(Math.min(NOW.getTime() - 60_000, at.time(0, hhmm(m)).getTime()));

    // Subscribers first (up to 3), then visitors.
    const running = (await runningOn(ctx, 0)).filter(({ sub, daysUsed, minutesUsed, daysThisWeek }) =>
      !(sub.totalDays && daysUsed >= sub.totalDays) && !(sub.daysPerWeek && daysThisWeek >= sub.daysPerWeek) && !(sub.totalHours && minutesUsed >= sub.totalHours * 60 - 60) && sub.billing !== 'PER_HOUR' && !sub.shiftId);
    const chosen = running.filter((_, i) => rngOf(`today/${today}/sub/${i}`).chance(0.5)).slice(0, 3);
    for (const [i, { sub }] of chosen.entries()) {
      const inM = windowFrom + Math.floor(((nowM - 10 - windowFrom) * (i + 1)) / (target + 1));
      const key = keyOf(`today/${today}/checkin/${sub.id}`);
      const openStay = await db.checkIn.findFirst({ where: { customerId: sub.customerId, checkedOutAt: null } });
      if (openStay && openStay.idempotencyKey !== key) continue;
      await writeCheckIn(ctx, { key, customerId: sub.customerId, subscriptionId: sub.id, checkedInAt: instant(inM), checkedOutAt: null, inBy: staffNow });
      present += 1;
    }
    for (let i = present; i < target; i += 1) {
      const inM = windowFrom + Math.floor(((nowM - 10 - windowFrom) * (i + 1)) / (target + 1));
      await writeVisit(ctx, {
        key: keyOf(`today/${today}/present/${i}`), offset: 0, name: WALK_INS[(i * 7 + at.date(0).getUTCDate()) % WALK_INS.length]!,
        audience: i % 3 === 1 ? 'STUDENT' : 'GENERAL', inMinute: inM, outMinute: null, checkedInAt: instant(inM), checkInBy: staffNow,
      });
      present += 1;
    }
    // Earlier today: visitors who came and went, paid at the desk.
    if (nowM - open[0] >= 150) {
      for (let i = 0; i < 3; i += 1) {
        const inM = open[0] + 10 + i * 25;
        const outM = Math.min(nowM - 20, inM + 75 + i * 40);
        if (outM - inM < 45) continue;
        await writeVisit(ctx, {
          key: keyOf(`today/${today}/left/${i}`), offset: 0, name: WALK_INS[(i * 11 + 3 + at.date(0).getUTCDate()) % WALK_INS.length]!,
          inMinute: inM, outMinute: outM, checkInBy: reception.id, checkOutBy: reception.id,
          pay: { method: i === 1 ? 'TRANSFER' : 'CASH', byId: reception.id },
        });
      }
    }
    // A subscriber settles part of a debt (never above what is owed).
    const samer = await db.customer.findFirst({ where: { spaceId: space.id, name: 'سامر جودة' }, include: { subscriptions: { include: { payments: { where: { voidedAt: null } } } } } });
    const sub = samer?.subscriptions[0];
    if (sub && sub.billing === 'FIXED') {
      const owed = sub.priceAgorot - sub.payments.reduce((s: number, p: any) => s + p.amountAgorot, 0);
      const key = keyOf(`today/${today}/samer`);
      const exists = await db.payment.findUnique({ where: { spaceId_idempotencyKey: { spaceId: space.id, idempotencyKey: key } } });
      if (exists || owed >= 3_000) {
        await writePayment(ctx, { key, item: { subscriptionId: sub.id }, amountAgorot: 3_000, method: 'CASH', byId: staffNow, at: instant(Math.max(open[0] + 20, nowM - 35)) });
      }
    }
  }

  // 5. Nothing full.
  const open2 = (await db.visit.count({ where: { spaceId: space.id, checkedOutAt: null } })) + (await db.checkIn.count({ where: { spaceId: space.id, checkedOutAt: null } }));
  const capacity = space.occupancy?.capacity ?? null;
  if (capacity !== null && open2 >= capacity) throw new Error(`pal-hub would read full: ${open2} of ${capacity}`);
  log(`today ${today}: ${open2} present at pal-hub (capacity ${capacity}); filled ${filled} day(s).`);
} finally {
  await db.$disconnect();
}
