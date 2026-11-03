// Shared by build-demo.ts and today.ts. Run from <app>/apps/api with the app's own tsx:
//   npx tsx --conditions=@masaha/source --env-file=.env <this folder>/<script>.ts
// It imports the app's own modules by path, so every value is computed by the app's rules.
import { createHash } from 'node:crypto';
import { createRequire } from 'node:module';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

export const API_DIR = process.cwd();
export const APP_DIR = join(API_DIR, '..', '..');

async function app(path: string): Promise<any> {
  return import(pathToFileURL(join(API_DIR, 'src', path)).href);
}
async function shared(path: string): Promise<any> {
  return import(pathToFileURL(join(APP_DIR, 'packages', 'shared', 'src', path)).href);
}

/** Refuses anything but a development database, and production. */
export function guard(): { dbName: string } {
  if (!API_DIR.replace(/\\/g, '/').endsWith('/apps/api')) {
    throw new Error(`Run from <app>/apps/api (cwd is ${API_DIR}).`);
  }
  if (process.env.NODE_ENV === 'production') throw new Error('Refusing NODE_ENV=production.');
  const url = process.env.DATABASE_URL;
  if (!url) throw new Error('DATABASE_URL is not set (run with --env-file=.env).');
  const dbName = new URL(url).pathname.replace(/^\//, '');
  if (!dbName.endsWith('_dev')) throw new Error(`Refusing database "${dbName}": not *_dev.`);
  const host = new URL(url).hostname;
  if (host !== 'localhost' && host !== '127.0.0.1') throw new Error(`Refusing host ${host}.`);
  if (!process.env.SEED_DEMO_PASSWORD) throw new Error('SEED_DEMO_PASSWORD is not set.');
  return { dbName };
}

export async function loadApp() {
  const { createPrismaClient } = await app('db/prisma.ts');
  const { hashPassword } = await app('modules/users/index.ts');
  const { chargeOf } = await app('modules/visits/visitCharge.ts');
  const { gazaClock } = await app('db/seed/demo.ts');
  const { normaliseContact } = await shared('spaces/index.ts');
  const require = createRequire(join(API_DIR, 'package.json'));
  const sharp = require('sharp');
  const db = createPrismaClient(process.env.DATABASE_URL);
  return { db, hashPassword, chargeOf, gazaClock, normaliseContact, sharp };
}

/** A UUID derived from a name: the same name, the same key, so a re-run finds what it made. */
export function keyOf(name: string): string {
  const h = createHash('sha256').update(`masaha-demo/${name}`).digest('hex');
  return `${h.slice(0, 8)}-${h.slice(8, 12)}-4${h.slice(13, 16)}-a${h.slice(17, 20)}-${h.slice(20, 32)}`;
}

/** A seeded random source, so a run repeats. */
export function rngOf(seed: string) {
  let a = createHash('sha256').update(seed).digest().readUInt32LE(0);
  const next = () => {
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  return {
    next,
    int: (min: number, max: number) => min + Math.floor(next() * (max - min + 1)),
    pick: <T>(list: readonly T[]): T => list[Math.floor(next() * list.length)] as T,
    chance: (p: number) => next() < p,
  };
}

/** One audit entry, as the app's writer appends it, dated when its action happened. */
export function auditAt(db: any) {
  return (
    at: Date,
    entry: {
      actorId: number | null;
      action: string;
      entityType: string;
      entityId: number | null;
      spaceId?: number;
      before?: unknown;
      after?: unknown;
    },
  ) => db.auditLog.create({ data: { ...entry, createdAt: at }, select: { id: true } });
}

export const hhmm = (minutes: number) =>
  `${String(Math.floor(minutes / 60)).padStart(2, '0')}:${String(minutes % 60).padStart(2, '0')}`;

// ─── The managed space's day ──────────────────────────────────────────────────────────────────

export const MANAGED_SLUG = 'pal-hub';
export const OWNER_EMAIL = 'demo-owner@example.com';
export const RECEPTION_EMAIL = 'demo-reception@example.com';

export const WALK_INS = [
  'محمود سالم', 'لين أبو حصيرة', 'عبد الرحمن شعت', 'تسنيم الأسطل', 'أسامة مهنا', 'رهف الجمل',
  'معاذ أبو جراد', 'ديما الريس', 'حسن الكفارنة', 'بيسان عليان', 'أيمن الفرا', 'نغم أبو العمرين',
  'صهيب عودة', 'ملك الحايك', 'مصطفى سكيك', 'هالة النخالة', 'زياد البرعي', 'أمل الدحدوح',
  'وسيم حلس', 'شيماء العطار', 'ثائر الصوراني', 'جود المدهون', 'رامي السقا', 'سما ياغي',
  'علاء أبو مصطفى', 'ريتال أبو ستة', 'إياد المصري', 'روان الطويل', 'مهند العجلة', 'غدير قديح',
];

export interface DayContext {
  db: any;
  audit: ReturnType<typeof auditAt>;
  at: any; // gazaClock(now)
  chargeOf: any;
  spaceId: number;
  ownerId: number;
  receptionId: number;
  rule: { rounding: string; roundingMinutes: number | null; capAtDayPrice: boolean };
  /** By day of week: [opens, closes] minutes, or null closed. */
  week: (readonly [number, number] | null)[];
  shifts: Map<number, { startsMinute: number; endsMinute: number }>;
  /** Rates a visit copies, by audience; null before the prices were published. */
  ratesOn: (offset: number, audience: 'GENERAL' | 'STUDENT') => { hourAgorot: number | null; dayAgorot: number | null };
  /** Days a closure covered (offsets): nothing happens on them. */
  closedOffsets: Set<number>;
}

/** Who is at the desk: reception Saturday to Thursday until 17:00, the owner otherwise. */
export function staffAt(ctx: DayContext, offset: number, minute: number, rng: ReturnType<typeof rngOf>) {
  const weekday = ctx.at.date(offset).getUTCDay();
  if (weekday === 5 || minute >= 17 * 60) return ctx.ownerId;
  return rng.chance(0.12) ? ctx.ownerId : ctx.receptionId;
}

export function weekdayOf(ctx: DayContext, offset: number): number {
  return ctx.at.date(offset).getUTCDay();
}

/**
 * Writes one visit, from check-in to its payment, as the desk does: `visit.checkedIn`, then at its
 * end `visit.checkedOut` (by staff) or `visit.autoCheckedOut` (the system, at closing), then
 * `payment.recorded`. Returns the visit.
 */
export async function writeVisit(
  ctx: DayContext,
  v: {
    key: string;
    offset: number;
    name: string;
    audience?: 'GENERAL' | 'STUDENT';
    inMinute: number;
    /** null: still present. */
    outMinute: number | null;
    auto?: boolean;
    pay?: { amount?: number; method: 'CASH' | 'TRANSFER'; byId?: number } | null;
    /** The customer the unpaid rest is left to (a phone's), set at check-out. */
    customerId?: number | null;
    /** A typed charge, when the visit has no rate. */
    typed?: { amountAgorot: number; reason: string } | null;
    checkInBy: number;
    checkOutBy?: number;
    /** For a visit present now: the instant it checked in (overrides inMinute). */
    checkedInAt?: Date;
  },
) {
  const { db, audit, at } = ctx;
  const found = await db.visit.findUnique({
    where: { spaceId_idempotencyKey: { spaceId: ctx.spaceId, idempotencyKey: v.key } },
  });
  if (found) return found;
  const audience = v.audience ?? 'GENERAL';
  const rates = ctx.ratesOn(v.offset, audience);
  const checkedInAt = v.checkedInAt ?? at.time(v.offset, hhmm(v.inMinute));
  const visit = await db.visit.create({
    data: {
      spaceId: ctx.spaceId,
      idempotencyKey: v.key,
      visitorName: v.name,
      audience,
      hourRateAgorot: rates.hourAgorot,
      dayRateAgorot: rates.dayAgorot,
      checkedInAt,
      createdAt: checkedInAt,
      updatedAt: checkedInAt,
    },
  });
  await audit(checkedInAt, {
    actorId: v.checkInBy,
    action: 'visit.checkedIn',
    entityType: 'visit',
    entityId: visit.id,
    spaceId: ctx.spaceId,
    after: {
      visitorName: v.name,
      audience,
      shiftId: null,
      hourRateAgorot: rates.hourAgorot,
      dayRateAgorot: rates.dayAgorot,
    },
  });
  if (v.outMinute === null) return visit;

  const checkedOutAt = at.time(v.offset, hhmm(v.outMinute));
  const computed = ctx.chargeOf({ from: checkedInAt, to: checkedOutAt }, rates, ctx.rule);
  let charge: any = null;
  if (v.typed && !computed && !v.auto) {
    charge = {
      amountAgorot: v.typed.amountAgorot,
      roundingRule: null,
      roundingMinutes: null,
      capApplied: null,
      typedById: v.checkOutBy ?? ctx.ownerId,
      reason: v.typed.reason,
    };
  } else if (computed) {
    charge = { ...computed, typedById: null, reason: null };
  }
  const amount = charge?.amountAgorot ?? 0;
  const paid = v.pay ? Math.min(v.pay.amount ?? amount, amount) : 0;
  const leftUnpaid = !v.auto && (charge === null || paid < amount);
  const customerId = leftUnpaid ? (v.customerId ?? null) : null;
  if (leftUnpaid && customerId === null) {
    throw new Error(`Visit ${v.key}: an unpaid rest needs a customer (a phone).`);
  }
  const closed = await db.visit.update({
    where: { id: visit.id },
    data: {
      checkedOutAt,
      checkoutMethod: v.auto ? 'AUTO' : 'MANUAL',
      roundingRule: charge?.roundingRule ?? null,
      roundingMinutes: charge?.roundingMinutes ?? null,
      capApplied: charge?.capApplied ?? null,
      chargeAgorot: charge?.amountAgorot ?? null,
      chargeSetById: charge?.typedById ?? null,
      chargeReason: charge?.reason ?? null,
      customerId,
      updatedAt: checkedOutAt,
    },
  });
  const outBy = v.checkOutBy ?? v.checkInBy;
  if (v.auto) {
    await audit(checkedOutAt, {
      actorId: null,
      action: 'visit.autoCheckedOut',
      entityType: 'visit',
      entityId: visit.id,
      spaceId: ctx.spaceId,
      after: { checkedOutAt: checkedOutAt.toISOString(), chargeAgorot: charge?.amountAgorot ?? null },
    });
  } else {
    const requestedAt = new Date(checkedOutAt.getTime() + 4_000);
    await audit(requestedAt, {
      actorId: outBy,
      action: 'visit.checkedOut',
      entityType: 'visit',
      entityId: visit.id,
      spaceId: ctx.spaceId,
      after: {
        checkedOutAt: checkedOutAt.toISOString(),
        requestedAt: requestedAt.toISOString(),
        chargeAgorot: charge?.amountAgorot ?? null,
        capApplied: charge?.capApplied ?? null,
        typedById: charge?.typedById ?? null,
        reason: charge?.reason ?? null,
        customerId,
      },
    });
  }
  if (paid > 0 && v.pay) {
    await writePayment(ctx, {
      key: keyOf(`${v.key}/pay`),
      item: { visitId: visit.id },
      amountAgorot: paid,
      method: v.pay.method,
      byId: v.pay.byId ?? outBy ?? ctx.receptionId,
      at: new Date(checkedOutAt.getTime() + 5_000),
    });
  }
  return closed;
}

/** A payment, as the desk records it: the ledger's triggers check it; `payment.recorded`. */
export async function writePayment(
  ctx: DayContext,
  p: {
    key: string;
    item: { visitId: number } | { subscriptionId: number };
    amountAgorot: number;
    method: 'CASH' | 'TRANSFER';
    byId: number;
    at: Date;
  },
) {
  const found = await ctx.db.payment.findUnique({
    where: { spaceId_idempotencyKey: { spaceId: ctx.spaceId, idempotencyKey: p.key } },
  });
  if (found) return found;
  const row = await ctx.db.payment.create({
    data: {
      spaceId: ctx.spaceId,
      idempotencyKey: p.key,
      ...p.item,
      amountAgorot: p.amountAgorot,
      method: p.method,
      recordedById: p.byId,
      receivedAt: p.at,
      createdAt: p.at,
    },
  });
  await ctx.audit(p.at, {
    actorId: p.byId,
    action: 'payment.recorded',
    entityType: 'payment',
    entityId: row.id,
    spaceId: ctx.spaceId,
    after: { ...p.item, amountAgorot: p.amountAgorot, method: p.method },
  });
  return row;
}

/** A subscriber's stay: `checkIn.checkedIn`, then `checkIn.checkedOut` or the system's auto one. */
export async function writeCheckIn(
  ctx: DayContext,
  c: {
    key: string;
    customerId: number;
    subscriptionId: number;
    checkedInAt: Date;
    checkedOutAt: Date | null;
    auto?: boolean;
    inBy: number;
    outBy?: number;
  },
) {
  const { db, audit } = ctx;
  const found = await db.checkIn.findUnique({
    where: { spaceId_idempotencyKey: { spaceId: ctx.spaceId, idempotencyKey: c.key } },
  });
  if (found) return found;
  const row = await db.checkIn.create({
    data: {
      spaceId: ctx.spaceId,
      idempotencyKey: c.key,
      customerId: c.customerId,
      subscriptionId: c.subscriptionId,
      checkedInAt: c.checkedInAt,
      checkedOutAt: c.checkedOutAt,
      checkoutMethod: c.checkedOutAt ? (c.auto ? 'AUTO' : 'MANUAL') : null,
      createdAt: c.checkedInAt,
      updatedAt: c.checkedOutAt ?? c.checkedInAt,
    },
  });
  await audit(c.checkedInAt, {
    actorId: c.inBy,
    action: 'checkIn.checkedIn',
    entityType: 'checkIn',
    entityId: row.id,
    spaceId: ctx.spaceId,
    after: { subscriptionId: c.subscriptionId, customerId: c.customerId },
  });
  if (c.checkedOutAt) {
    if (c.auto) {
      await audit(c.checkedOutAt, {
        actorId: null,
        action: 'checkIn.autoCheckedOut',
        entityType: 'checkIn',
        entityId: row.id,
        spaceId: ctx.spaceId,
        after: { checkedOutAt: c.checkedOutAt.toISOString() },
      });
    } else {
      const requestedAt = new Date(c.checkedOutAt.getTime() + 3_000);
      await audit(requestedAt, {
        actorId: c.outBy ?? c.inBy,
        action: 'checkIn.checkedOut',
        entityType: 'checkIn',
        entityId: row.id,
        spaceId: ctx.spaceId,
        after: {
          checkedOutAt: c.checkedOutAt.toISOString(),
          requestedAt: requestedAt.toISOString(),
        },
      });
    }
  }
  return row;
}

/** The subscriptions running on a day (by its Gaza date), each with what it has used before it. */
export async function runningOn(ctx: DayContext, offset: number) {
  const day = ctx.at.date(offset);
  const subs = await ctx.db.subscription.findMany({
    where: {
      spaceId: ctx.spaceId,
      startsOn: { lte: day },
      OR: [{ endsOn: null }, { endsOn: { gte: day } }],
      customer: { archivedAt: null },
    },
    orderBy: { id: 'asc' },
  });
  const result = [];
  for (const sub of subs) {
    // A subscription ended early is not used after its end (its end is that day).
    const before = await ctx.db.checkIn.findMany({
      where: { subscriptionId: sub.id, checkedInAt: { lt: ctx.at.time(offset, '00:00') } },
      select: { checkedInAt: true, checkedOutAt: true },
    });
    const days = new Set(before.map((c: any) => c.checkedInAt.toLocaleDateString('en-CA', { timeZone: 'Asia/Gaza' })));
    const minutes = before.reduce(
      (sum: number, c: any) =>
        sum + (c.checkedOutAt ? Math.floor((c.checkedOutAt - c.checkedInAt) / 60_000) : 0),
      0,
    );
    // This week, Saturday to Friday.
    const weekday = ctx.at.date(offset).getUTCDay();
    const sinceSaturday = (weekday + 1) % 7;
    const weekStart = ctx.at.time(offset - sinceSaturday, '00:00');
    const thisWeek = new Set(
      before
        .filter((c: any) => c.checkedInAt >= weekStart)
        .map((c: any) => c.checkedInAt.toLocaleDateString('en-CA', { timeZone: 'Asia/Gaza' })),
    );
    result.push({ sub, daysUsed: days.size, minutesUsed: minutes, daysThisWeek: thisWeek.size });
  }
  return result;
}

/** A subscriber's stay window on a day: their shift's, else the space's day. */
export function stayFor(
  ctx: DayContext,
  sub: any,
  open: readonly [number, number],
  rng: ReturnType<typeof rngOf>,
): [number, number] {
  let [from, to] = open;
  const shift = sub.shiftId ? ctx.shifts.get(sub.shiftId) : undefined;
  if (shift) {
    from = Math.max(from, shift.startsMinute);
    to = Math.min(to, shift.endsMinute);
  }
  const span = to - from;
  if (span < 90) return [from, to];
  const inM = from + rng.int(0, Math.min(120, Math.floor(span / 3)));
  let length = rng.int(150, 360);
  if (sub.hoursPerDay) length = Math.min(length, sub.hoursPerDay * 60 - 10);
  if (sub.billing === 'PER_HOUR') length = rng.int(110, 240);
  const outM = Math.min(to, inM + length);
  return [inM, Math.max(inM + 45, outM)];
}

/**
 * One whole day of the managed space: its subscribers' stays and its walk-in visitors, each paid at
 * check-out, by whoever is at the desk. Skips a closed day, and any customer with a stay that day.
 * `until` (minutes) cuts the day short: what starts after it is not written.
 */
export async function writeDay(
  ctx: DayContext,
  offset: number,
  opts: { tag: string; until?: number; walkIns?: number },
) {
  const weekday = weekdayOf(ctx, offset);
  const open = ctx.week[weekday];
  if (!open || ctx.closedOffsets.has(offset)) return { checkIns: 0, visits: 0 };
  const date = ctx.at.date(offset).toISOString().slice(0, 10);
  const rng = rngOf(`${opts.tag}/${date}`);
  const until = opts.until ?? open[1];
  let checkIns = 0;
  let visits = 0;

  const dayStart = ctx.at.time(offset, '00:00');
  const dayEnd = ctx.at.time(offset + 1, '00:00');
  const busy = new Set<number>(
    (
      await ctx.db.checkIn.findMany({
        where: { spaceId: ctx.spaceId, checkedInAt: { gte: dayStart, lt: dayEnd } },
        select: { customerId: true },
      })
    ).map((c: any) => c.customerId),
  );

  // Subscribers.
  const attendance = weekday === 5 ? 0.3 : weekday === 6 ? 0.6 : 0.82;
  for (const { sub, daysUsed, minutesUsed, daysThisWeek } of await runningOn(ctx, offset)) {
    if (busy.has(sub.customerId)) continue;
    if (sub.totalDays && daysUsed >= sub.totalDays) continue;
    if (sub.daysPerWeek && daysThisWeek >= sub.daysPerWeek) continue;
    if (sub.totalHours && minutesUsed >= sub.totalHours * 60 - 60) continue;
    const isDaily = sub.startsOn && sub.endsOn && +sub.startsOn === +sub.endsOn;
    const p = isDaily ? 1 : sub.totalHours ? 0.45 : sub.daysPerWeek ? 0.55 : attendance;
    if (!rng.chance(p)) continue;
    let [inM, outM0] = stayFor(ctx, sub, open, rng);
    // Never before the subscription was made that day.
    const madeAt = sub.createdAt.getTime();
    if (ctx.at.time(offset, hhmm(inM)).getTime() <= madeAt) {
      const madeMinute = Math.ceil((madeAt - ctx.at.time(offset, '00:00').getTime()) / 60_000) + 2;
      if (madeMinute >= open[1] - 30) continue;
      inM = madeMinute;
      outM0 = Math.min(open[1], Math.max(outM0, inM + 90));
    }
    if (inM >= until) continue;
    let outM = outM0;
    let auto = false;
    // Now and then a subscriber stays until closing and the system checks them out.
    if (!sub.shiftId && rng.chance(0.05)) {
      outM = open[1];
      auto = true;
    }
    if (sub.totalHours) {
      const left = sub.totalHours * 60 - minutesUsed;
      outM = Math.min(outM, inM + Math.max(60, left - 30));
      auto = false;
    }
    const present = opts.until !== undefined && outM > until;
    const inBy = staffAt(ctx, offset, inM, rng);
    await writeCheckIn(ctx, {
      key: keyOf(`${opts.tag}/${date}/checkin/${sub.id}`),
      customerId: sub.customerId,
      subscriptionId: sub.id,
      checkedInAt: ctx.at.time(offset, hhmm(inM)),
      checkedOutAt: present ? null : ctx.at.time(offset, hhmm(outM)),
      auto,
      inBy,
      outBy: staffAt(ctx, offset, outM, rng),
    });
    busy.add(sub.customerId);
    checkIns += 1;
  }

  // Walk-in visitors.
  const count =
    opts.walkIns ?? (weekday === 5 ? rng.int(2, 4) : weekday === 6 ? rng.int(5, 8) : rng.int(8, 13));
  for (let i = 0; i < count; i += 1) {
    const inM = open[0] + rng.int(0, Math.max(30, open[1] - open[0] - 120));
    if (inM >= until) continue;
    let outM = Math.min(open[1] - rng.int(5, 45), inM + rng.int(55, 300));
    if (outM - inM < 40) outM = Math.min(open[1] - 2, inM + 45);
    const student = rng.chance(0.25);
    const rates = ctx.ratesOn(offset, student ? 'STUDENT' : 'GENERAL');
    // Before the prices were published, the owner typed each charge at the desk.
    const unpriced = rates.hourAgorot === null && rates.dayAgorot === null;
    let auto = !unpriced && rng.chance(0.035);
    if (unpriced && outM >= open[1]) outM = open[1] - 15;
    if (auto) outM = open[1];
    const present = opts.until !== undefined && outM > until;
    const inBy = staffAt(ctx, offset, inM, rng);
    const outBy = unpriced ? ctx.ownerId : staffAt(ctx, offset, outM, rng);
    const typed = unpriced
      ? {
          amountAgorot: Math.min(Math.ceil((outM - inM) / 60) * 500, 2_500),
          reason: 'قبل نشر الأسعار: السعر المتفق عليه مع الزائر',
        }
      : null;
    await writeVisit(ctx, {
      key: keyOf(`${opts.tag}/${date}/visit/${i}`),
      offset,
      name: rng.pick(WALK_INS),
      audience: student ? 'STUDENT' : 'GENERAL',
      inMinute: inM,
      outMinute: present ? null : outM,
      auto,
      // An auto check-out is left uncollected; most of those are paid the next day (below).
      pay: auto ? null : { method: rng.chance(0.18) ? 'TRANSFER' : 'CASH', byId: outBy },
      typed,
      checkInBy: inBy,
      checkOutBy: outBy,
    });
    visits += 1;
  }
  return { checkIns, visits };
}
