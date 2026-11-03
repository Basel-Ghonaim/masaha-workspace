// build-demo: turns a freshly seeded development database (db:reset + db:seed with SEED_DEMO=true)
// into the presentation demo. Phases: `data` (Prisma, backdated, audited as the services audit),
// then `photos` (through the running local API). Default: both.
//   cd <app>/apps/api
//   npx tsx --conditions=@masaha/source --env-file=.env <folder>/scripts/build-demo.ts [--phase=data|photos]
import { existsSync } from 'node:fs';
import { readdir, readFile, writeFile } from 'node:fs/promises';
import { dirname, extname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

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
  writeCheckIn,
  writeDay,
  writePayment,
  writeVisit,
  type DayContext,
} from './lib.ts';
import { PHOTO_MAP, REAL_SPACES, USERS, type RealSpace } from './spaces-config.ts';

const HERE = dirname(fileURLToPath(import.meta.url));
const PHOTO_DIR = 'C:/Users/basel/Downloads/spaceImg';
const phase = (process.argv.find((a) => a.startsWith('--phase=')) ?? '--phase=all').slice(8);

const { dbName } = guard();
const { db, hashPassword, chargeOf, gazaClock, normaliseContact, sharp } = await loadApp();
const NOW = new Date();
const at = gazaClock(NOW);
const audit = auditAt(db);
const DAY_MS = 86_400_000;
const ago = (days: number, time = '10:00') => at.time(-days, time);
const ymd = (offset: number) => at.date(offset).toISOString().slice(0, 10);
const minutesOf = (s: string) => {
  const [h = 0, m = 0] = s.split(':').map(Number);
  return h * 60 + m;
};
const summaryPath = join(HERE, `build-summary-${dbName}.json`);
const decisions: string[] = [];

function log(...args: unknown[]) {
  console.log(`[${new Date().toISOString().slice(11, 19)}]`, ...args);
}

// ─── Data ────────────────────────────────────────────────────────────────────────────────────

async function buildData() {
  const admin = await db.user.findUniqueOrThrow({
    where: { email: process.env.SEED_ADMIN_EMAIL!.toLowerCase() },
  });
  const ahmad = await db.user.findUniqueOrThrow({ where: { email: OWNER_EMAIL } });
  const laila = await db.user.findUniqueOrThrow({ where: { email: RECEPTION_EMAIL } });
  const sami = await db.user.findUniqueOrThrow({ where: { email: 'demo-directory-owner@example.com' } });
  const demoSpace = await db.space.findUniqueOrThrow({ where: { slug: 'masaha-demo' } });
  if (await db.space.findUnique({ where: { slug: MANAGED_SLUG } })) {
    throw new Error('pal-hub exists: build-demo runs once, after db:reset + db:seed.');
  }
  if (!(await db.space.findUnique({ where: { slug: 'noor-hub' } }))) {
    throw new Error("The seed's directory set is missing: run db:seed with SEED_DEMO=true.");
  }
  const areas = new Map<string, number>(
    (await db.area.findMany()).map((a: any) => [a.nameEn, a.id] as [string, number]),
  );
  const amenities = await db.amenity.findMany();
  const amenityByKey = new Map<string, number>(amenities.map((a: any) => [a.key, a.id] as [string, number]));
  const amenityByEn = new Map<string, string>(amenities.map((a: any) => [a.nameEn, a.key] as [string, string]));
  const defaults = (await db.setting.findUniqueOrThrow({ where: { key: 'newSpaceDefaults' } })).value as any;
  const settingsData = {
    autoCheckoutAtClosing: defaults.autoCheckoutAtClosing,
    visitRounding: defaults.visitRounding,
    visitRoundingMinutes: defaults.visitRoundingMinutes ?? null,
    visitCapAtDayPrice: defaults.visitCapAtDayPrice,
  };
  const hash = await hashPassword(process.env.SEED_DEMO_PASSWORD!);
  const rng = rngOf(`build/${ymd(0)}`);

  // 1. The seed's directory set, dated 20 days back as a whole, so the real spaces list first.
  const seedIds: number[] = (
    await db.space.findMany({ where: { slug: { not: 'masaha-demo' } }, select: { id: true } })
  ).map((s: any) => s.id);
  await db.$executeRawUnsafe(
    `UPDATE spaces SET created_at = created_at - interval '20 days',
       profile_updated_at = profile_updated_at - interval '20 days',
       hours_updated_at = hours_updated_at - interval '20 days',
       prices_updated_at = prices_updated_at - interval '20 days',
       amenities_updated_at = amenities_updated_at - interval '20 days',
       contacts_updated_at = contacts_updated_at - interval '20 days'
     WHERE id = ANY($1::int[])`,
    seedIds,
  );
  await db.$executeRawUnsafe(
    `UPDATE space_managers SET created_at = created_at - interval '20 days', updated_at = updated_at - interval '20 days' WHERE space_id = ANY($1::int[])`,
    seedIds,
  );
  await db.user.update({ where: { id: sami.id }, data: { createdAt: ago(21, '11:00') } });
  decisions.push("The seed's 24 directory spaces are dated 20 days back as a whole (their staleness unchanged), so the 13 real spaces, entered over the last 17 days, list first.");

  // 2. Users.
  const users: any[] = [];
  for (const [index, [name, email]] of USERS.entries()) {
    const createdAt = email === 'demo-user@example.com' ? ago(41, '20:15') : ago(rng.int(2, 78), hhmm(rng.int(8 * 60, 23 * 60)));
    users.push(
      await db.user.create({
        data: { email, name, passwordHash: hash, role: 'USER', language: index % 9 === 4 ? 'en' : 'ar', createdAt, updatedAt: createdAt },
      }),
    );
  }
  log(`users: ${users.length}`);

  // 3. The 13 real spaces.
  const live = JSON.parse(await readFile(join(HERE, 'live-spaces.json'), 'utf8'));
  const liveBySlug = new Map<string, any>(live.spaces.map((s: any) => [s.page.slug, s.page]));
  const spaceIds = new Map<string, number>();
  const spaceCreated = new Map<string, Date>();
  const owners = new Map<string, number>();
  let palShifts = new Map<string, number>();

  for (const config of REAL_SPACES) {
    const page = liveBySlug.get(config.slug);
    if (!page) throw new Error(`${config.slug} is not in live-spaces.json`);
    const isPal = config.slug === MANAGED_SLUG;
    const created = ago(config.createdDaysAgo, isPal ? '10:00' : hhmm(9 * 60 + rng.int(0, 9 * 60)));
    const step = (seconds: number) => new Date(created.getTime() + seconds * 1000);
    const areaId = areas.get(page.area.nameEn);
    if (!areaId) throw new Error(`No area ${page.area.nameEn}`);
    const profile = {
      nameEn: page.nameEn,
      nameAr: page.nameAr ?? null,
      descriptionAr: page.descriptionAr ?? null,
      descriptionEn: page.descriptionEn ?? null,
      areaId,
      addressAr: page.addressAr,
      addressEn: page.addressEn ?? config.addressEn,
      landmarkAr: page.landmarkAr ?? null,
      landmarkEn: page.landmarkEn ?? null,
      lat: page.location.lat,
      lng: page.location.lng,
    };
    const space = await db.space.create({
      data: {
        slug: config.slug,
        ...profile,
        profileUpdatedAt: created,
        createdAt: created,
        updatedAt: created,
        settings: { create: { ...settingsData, createdAt: created, updatedAt: created } },
      },
    });
    const spaceId = space.id;
    spaceIds.set(config.slug, spaceId);
    spaceCreated.set(config.slug, created);
    await audit(created, {
      actorId: admin.id, action: 'space.created', entityType: 'space', entityId: spaceId, spaceId,
      after: { ...profile, slug: config.slug },
    });

    // Hours and shifts.
    const days = weekOf(config, page);
    await db.spaceHours.createMany({
      data: days.map((range, dayOfWeek) =>
        range
          ? { spaceId, dayOfWeek, opensMinute: range[0], closesMinute: range[1], createdAt: step(60), updatedAt: step(60) }
          : { spaceId, dayOfWeek, isClosed: true, createdAt: step(60), updatedAt: step(60) },
      ),
    });
    const shifts: any[] = [];
    for (const [sortOrder, shift] of (config.shifts ?? []).entries()) {
      shifts.push(
        await db.spaceShift.create({
          data: {
            spaceId, nameAr: shift.nameAr, nameEn: shift.nameEn,
            startsMinute: minutesOf(shift.range[0]), endsMinute: minutesOf(shift.range[1]),
            sortOrder, createdAt: step(60), updatedAt: step(60),
          },
        }),
      );
    }
    if (isPal) palShifts = new Map(shifts.map((s) => [s.nameEn, s.id]));
    await audit(step(60), {
      actorId: admin.id, action: 'space.hoursEdited', entityType: 'space', entityId: spaceId, spaceId,
      before: { days: [], shifts: [] },
      after: {
        days: days.map((d) => d && { opensMinute: d[0], closesMinute: d[1] }),
        shifts: shifts.map((s) => ({ id: s.id, nameAr: s.nameAr, nameEn: s.nameEn, startsMinute: s.startsMinute, endsMinute: s.endsMinute })),
      },
    });

    // Amenities: the live ones, and the completion.
    const keys = new Set<string>([
      ...page.amenities.filter((a: any) => a.icon).map((a: any) => amenityByEn.get(a.nameEn)!),
      ...config.amenities,
    ]);
    const amenityIds = [...keys].map((k) => {
      const id = amenityByKey.get(k);
      if (!id) throw new Error(`No amenity ${k}`);
      return id;
    });
    const own = [
      ...page.amenities.filter((a: any) => !a.icon).map((a: any) => [a.nameAr, a.nameEn ?? undefined]),
      ...(config.ownAmenities ?? []),
    ] as [string, string?][];
    await db.spaceAmenity.createMany({
      data: amenityIds.map((amenityId) => ({ spaceId, amenityId, createdAt: step(120), updatedAt: step(120) })),
    });
    await db.spaceOwnAmenity.createMany({
      data: own.map(([nameAr, nameEn], sortOrder) => ({ spaceId, nameAr, nameEn: nameEn ?? null, sortOrder, createdAt: step(120), updatedAt: step(120) })),
    });
    await audit(step(120), {
      actorId: admin.id, action: 'space.amenitiesEdited', entityType: 'space', entityId: spaceId, spaceId,
      before: { amenityIds: [], ownAmenities: [] },
      after: {
        amenityIds: [...amenityIds].sort((a, b) => a - b),
        ownAmenities: own.map(([nameAr, nameEn]) => ({ nameAr, nameEn: nameEn ?? null })),
      },
    });

    // Contacts: the live ones; a fictional number only where there is no phone and no WhatsApp.
    const contacts: { type: string; value: string }[] = page.contacts.map((c: any) => ({ type: c.type, value: c.value }));
    if (!contacts.some((c) => c.type === 'PHONE' || c.type === 'WHATSAPP')) {
      for (const [type, typed] of config.fictional ?? []) {
        const value = normaliseContact(type, typed);
        if (!value) throw new Error(`Not a valid ${type}: ${typed}`);
        contacts.push({ type, value });
      }
    }
    await db.spaceContact.createMany({
      data: contacts.map((c, sortOrder) => ({ spaceId, type: c.type, value: c.value, sortOrder, createdAt: step(180), updatedAt: step(180) })),
    });
    await audit(step(180), {
      actorId: admin.id, action: 'space.contactsEdited', entityType: 'space', entityId: spaceId, spaceId,
      before: { contacts: [] }, after: { contacts },
    });

    // Prices: the managed space's owner publishes its own later (below).
    let pricesAt: Date | null = null;
    if (!isPal && config.prices) {
      pricesAt = step(240);
      const rows = priceRows(config, page, shifts);
      await db.spacePrice.createMany({
        data: rows.map((p, sortOrder) => ({ spaceId, ...p, sortOrder, createdAt: pricesAt, updatedAt: pricesAt })),
      });
      await audit(pricesAt, {
        actorId: admin.id, action: 'space.pricesEdited', entityType: 'space', entityId: spaceId, spaceId,
        before: { prices: [] }, after: { prices: rows.map(priceValue) },
      });
    }
    await db.space.update({
      where: { id: spaceId },
      data: {
        hoursUpdatedAt: step(60), amenitiesUpdatedAt: step(120), contactsUpdatedAt: step(180),
        pricesUpdatedAt: pricesAt, updatedAt: pricesAt ?? step(180),
      },
    });

    // The owner: an account the admin created (a temporary password, since changed), then linked.
    if (config.owner && !isPal) {
      const linkedAt = new Date(created.getTime() + DAY_MS + 3_600_000);
      const owner = await db.user.create({
        data: { email: config.owner.email, name: config.owner.name, passwordHash: hash, role: 'OWNER', createdAt: linkedAt, updatedAt: linkedAt },
      });
      owners.set(config.slug, owner.id);
      await audit(linkedAt, {
        actorId: admin.id, action: 'user.created', entityType: 'user', entityId: owner.id,
        after: { name: owner.name, email: owner.email, role: 'OWNER', mustChangePassword: true },
      });
      const linkAt = new Date(linkedAt.getTime() + 60_000);
      await db.spaceManager.create({ data: { spaceId, userId: owner.id, role: 'OWNER', createdAt: linkAt, updatedAt: linkAt } });
      await audit(linkAt, {
        actorId: admin.id, action: 'space.ownerLinked', entityType: 'space', entityId: spaceId, spaceId,
        after: { userId: owner.id },
      });
      const capacityAt = new Date(linkAt.getTime() + 5 * 3_600_000);
      await db.spaceOccupancy.create({ data: { spaceId, capacity: config.owner.capacity, createdAt: capacityAt, updatedAt: capacityAt } });
      await audit(capacityAt, {
        actorId: owner.id, action: 'space.capacityEdited', entityType: 'space', entityId: spaceId, spaceId,
        before: { capacity: null }, after: { capacity: config.owner.capacity },
      });
    }
  }
  log('real spaces: 13');

  // 4. The managed space: Pal Hub.
  const palId = spaceIds.get(MANAGED_SLUG)!;
  const pal = REAL_SPACES.find((s) => s.slug === MANAGED_SLUG)!;
  await db.user.update({ where: { id: ahmad.id }, data: { createdAt: ago(67, '19:20'), updatedAt: ago(65, '11:00') } });
  await db.user.update({ where: { id: laila.id }, data: { createdAt: ago(64, '12:10'), updatedAt: ago(64, '12:10') } });
  owners.set(MANAGED_SLUG, ahmad.id);
  await db.spaceManager.create({ data: { spaceId: palId, userId: ahmad.id, role: 'OWNER', createdAt: ago(65, '11:00'), updatedAt: ago(65, '11:00') } });
  await audit(ago(65, '11:00'), {
    actorId: admin.id, action: 'space.ownerLinked', entityType: 'space', entityId: palId, spaceId: palId,
    after: { userId: ahmad.id },
  });
  await audit(ago(65, '11:00'), {
    actorId: admin.id, action: 'user.roleChanged', entityType: 'user', entityId: ahmad.id,
    before: { role: 'USER' }, after: { role: 'OWNER' },
  });
  await audit(ago(64, '12:10'), {
    actorId: ahmad.id, action: 'user.created', entityType: 'user', entityId: laila.id, spaceId: palId,
    after: { name: laila.name, email: laila.email, role: 'USER', mustChangePassword: true },
  });
  await db.spaceManager.create({ data: { spaceId: palId, userId: laila.id, role: 'RECEPTION', createdAt: ago(64, '12:10'), updatedAt: ago(64, '12:10') } });
  await audit(ago(64, '12:10'), {
    actorId: ahmad.id, action: 'space.staffAdded', entityType: 'space', entityId: palId, spaceId: palId,
    after: { userId: laila.id },
  });
  await db.spaceOccupancy.create({ data: { spaceId: palId, capacity: 40, createdAt: ago(64, '12:30'), updatedAt: ago(64, '12:30') } });
  await audit(ago(64, '12:30'), {
    actorId: ahmad.id, action: 'space.capacityEdited', entityType: 'space', entityId: palId, spaceId: palId,
    before: { capacity: null }, after: { capacity: 40 },
  });
  // Prices, published by the owner a week after the space opened (the first days were typed by hand).
  const palShiftRows = [...palShifts.entries()].map(([nameEn, id]) => ({ id, nameEn }));
  const palPrices = priceRows(pal, null, palShiftRows.map((s) => ({ id: s.id, nameEn: s.nameEn })));
  const pricesAt = ago(58, '07:45');
  await db.spacePrice.createMany({
    data: palPrices.map((p, sortOrder) => ({ spaceId: palId, ...p, sortOrder, createdAt: pricesAt, updatedAt: pricesAt })),
  });
  await audit(pricesAt, {
    actorId: ahmad.id, action: 'space.pricesEdited', entityType: 'space', entityId: palId, spaceId: palId,
    before: { prices: [] }, after: { prices: palPrices.map(priceValue) },
  });
  await db.space.update({ where: { id: palId }, data: { pricesUpdatedAt: pricesAt } });

  // Packages.
  const morning = palShifts.get('Morning')!;
  const evening = palShifts.get('Evening')!;
  const packageDefs = [
    { name: 'يومي', validityDays: 1, billing: 'FIXED', priceAgorot: 2_500 },
    { name: 'أسبوعي', validityDays: 7, billing: 'FIXED', priceAgorot: 12_000 },
    { name: 'شهري صباحي', validityDays: 30, billing: 'FIXED', priceAgorot: 22_000, shiftId: morning },
    { name: 'شهري مسائي', validityDays: 30, billing: 'FIXED', priceAgorot: 20_000, shiftId: evening },
    { name: 'شهري طلاب', validityDays: 30, billing: 'FIXED', priceAgorot: 28_000, audience: 'STUDENT' },
    { name: '10 أيام خلال شهر', validityDays: 30, totalDays: 10, billing: 'FIXED', priceAgorot: 15_000 },
  ];
  const packages = new Map<string, any>();
  for (const [sortOrder, def] of packageDefs.entries()) {
    const when = ago(63, hhmm(11 * 60 + sortOrder * 3));
    const terms = {
      name: def.name, validityDays: def.validityDays, totalDays: (def as any).totalDays ?? null,
      daysPerWeek: null, hoursPerDay: null, totalHours: null, billing: def.billing,
      priceAgorot: def.priceAgorot, audience: (def as any).audience ?? 'GENERAL', shiftId: (def as any).shiftId ?? null,
    };
    const row = await db.package.create({ data: { spaceId: palId, ...terms, sortOrder, createdAt: when, updatedAt: when } });
    packages.set(def.name, row);
    await audit(when, {
      actorId: ahmad.id, action: 'package.created', entityType: 'package', entityId: row.id, spaceId: palId,
      after: terms,
    });
  }

  const week = [0, 1, 2, 3, 4, 5, 6].map((d) => (d === 5 ? ([720, 1200] as const) : ([480, 1320] as const)));
  const ctx: DayContext = {
    db, audit, at, chargeOf, spaceId: palId, ownerId: ahmad.id, receptionId: laila.id,
    rule: { rounding: settingsData.visitRounding, roundingMinutes: settingsData.visitRoundingMinutes, capAtDayPrice: settingsData.visitCapAtDayPrice },
    week,
    shifts: new Map([...palShifts.values()].map((id) => {
      const s = (pal.shifts ?? []).find((x) => palShifts.get(x.nameEn) === id)!;
      return [id, { startsMinute: minutesOf(s.range[0]), endsMinute: minutesOf(s.range[1]) }];
    })),
    ratesOn: (offset, audience) =>
      offset <= -59
        ? { hourAgorot: null, dayAgorot: null }
        : audience === 'STUDENT'
          ? { hourAgorot: 400, dayAgorot: 2_000 }
          : { hourAgorot: 500, dayAgorot: 2_500 },
    closedOffsets: new Set([-25, -24]),
  };
  const staff = (who: 'o' | 'r') => (who === 'o' ? ahmad.id : laila.id);

  // Customers and their subscriptions.
  type Pay = [offset: number, amount: number, method: 'CASH' | 'TRANSFER', by: 'o' | 'r', time?: string];
  interface SubPlan {
    pkg?: string;
    published?: 'MONTH' | 'WEEK';
    custom?: { name: string; billing: 'FIXED' | 'PER_HOUR'; price: number; reason: string; ends: number | null; totalHours?: number; daysPerWeek?: number; hoursPerDay?: number; audience?: 'STUDENT' };
    start: number;
    created?: [number, string];
    by?: 'o' | 'r';
    renews?: boolean;
    pays: Pay[];
    endEarly?: number;
  }
  const plans: { name: string; phone?: string; archived?: [number, 'o' | 'r']; subs: SubPlan[] }[] = [
    { name: 'محمد عوض', phone: '+970599000201', subs: [
      { published: 'MONTH', start: -58, pays: [[-58, 35_000, 'CASH', 'r']] },
      { published: 'MONTH', start: -28, created: [-29, '18:30'], by: 'o', renews: true, pays: [[-29, 35_000, 'TRANSFER', 'o', '18:31']] },
    ] },
    { name: 'سارة خالد', phone: '+970599000202', subs: [
      { pkg: 'شهري طلاب', start: -50, pays: [[-50, 28_000, 'CASH', 'r']] },
      { pkg: 'شهري طلاب', start: -18, created: [-19, '16:40'], renews: true, pays: [[-19, 20_000, 'CASH', 'r', '16:41']] },
    ] },
    { name: 'أحمد ياسين', phone: '+970599000203', subs: [{ pkg: 'شهري صباحي', start: -40, pays: [[-40, 22_000, 'CASH', 'r']] }] },
    { name: 'رنا عبد الهادي', phone: '+970599000204', subs: [{ pkg: 'شهري مسائي', start: -20, created: [-20, '15:20'], by: 'o', pays: [[-20, 20_000, 'TRANSFER', 'o', '15:21']] }] },
    { name: 'يوسف أبو علي', phone: '+970599000205', subs: [{ custom: { name: 'باقة 30 ساعة', billing: 'FIXED', price: 12_000, reason: 'باقة ساعات لعميل دائم', ends: null, totalHours: 30 }, start: -30, by: 'o', created: [-30, '17:10'], pays: [[-30, 12_000, 'CASH', 'o', '17:11']] }] },
    { name: 'لينا حسونة', phone: '+970599000206', subs: [{ custom: { name: 'امتحانات بالساعة', billing: 'PER_HOUR', price: 400, reason: 'سعر الطالب بالساعة لفترة الامتحانات', ends: 14, hoursPerDay: 5, audience: 'STUDENT' }, start: -6, by: 'o', created: [-6, '17:30'], pays: [[-6, 12_000, 'CASH', 'o', '17:31']] }] },
    { name: 'عمر الحلبي', phone: '+970599000207', subs: [{ published: 'MONTH', start: -35, pays: [[-35, 35_000, 'CASH', 'r']] }] },
    { name: 'هبة الشريف', phone: '+970599000208', subs: [
      { pkg: 'أسبوعي', start: -9, pays: [[-9, 12_000, 'CASH', 'r']] },
      { pkg: 'أسبوعي', start: -2, created: [-3, '17:30'], by: 'o', renews: true, pays: [[-3, 12_000, 'CASH', 'o', '17:31']] },
    ] },
    { name: 'خالد منصور', phone: '+970599000209', subs: [{ published: 'MONTH', start: -15, by: 'o', created: [-15, '18:05'], pays: [[-15, 35_000, 'TRANSFER', 'o', '18:06']], endEarly: -6 }] },
    { name: 'نور حسن', phone: '+970599000210', subs: [{ custom: { name: '3 أيام أسبوعيًا', billing: 'FIXED', price: 20_000, reason: 'سعر متفق عليه لثلاثة أيام في الأسبوع', ends: 20, daysPerWeek: 3 }, start: -10, by: 'o', created: [-10, '17:45'], pays: [[-10, 10_000, 'CASH', 'o', '17:46']] }] },
    { name: 'إبراهيم قنديل', phone: '+970599000211', subs: [{ pkg: '10 أيام خلال شهر', start: -27, pays: [[-27, 15_000, 'CASH', 'r']] }] },
    { name: 'آية مطر', subs: [{ pkg: 'شهري طلاب', start: -5, pays: [[-5, 28_000, 'CASH', 'r']] }] },
    { name: 'سامر جودة', phone: '+970599000213', subs: [{ pkg: 'شهري صباحي', start: -3, pays: [[-3, 15_000, 'CASH', 'r']] }] },
    { name: 'دينا الشامي', phone: '+970599000214', subs: [{ published: 'MONTH', start: -21, by: 'o', created: [-21, '17:20'], pays: [[-21, 35_000, 'TRANSFER', 'o', '17:21']] }] },
    { name: 'طارق النجار', phone: '+970599000215', subs: [
      { pkg: 'يومي', start: -7, pays: [[-7, 2_500, 'CASH', 'r']] },
      { pkg: 'يومي', start: -4, pays: [[-4, 2_500, 'CASH', 'r']] },
      { pkg: 'يومي', start: -1, pays: [[-1, 2_500, 'CASH', 'r']] },
    ] },
    { name: 'مريم أبو سمرة', phone: '+970599000216', archived: [-40, 'r'], subs: [{ pkg: 'أسبوعي', start: -60, pays: [[-60, 12_000, 'CASH', 'r']] }] },
    { name: 'فادي الرنتيسي', phone: '+970599000217', archived: [-20, 'o'], subs: [{ published: 'MONTH', start: -57, pays: [[-57, 35_000, 'CASH', 'r']] }] },
    { name: 'جنى البطة', phone: '+970599000218', subs: [{ pkg: 'شهري طلاب', start: -45, pays: [[-45, 28_000, 'CASH', 'r']] }] },
    { name: 'أنس المصري', phone: '+970599000219', subs: [{ pkg: 'شهري مسائي', start: -14, by: 'o', created: [-14, '17:05'], pays: [[-14, 20_000, 'CASH', 'o', '17:06']] }] },
    { name: 'ريم السويركي', phone: '+970599000220', subs: [
      { pkg: 'شهري صباحي', start: -55, pays: [[-55, 22_000, 'CASH', 'r']] },
      { pkg: 'شهري صباحي', start: -25, created: [-26, '13:00'], renews: true, pays: [[-26, 22_000, 'TRANSFER', 'r', '13:01']] },
    ] },
    { name: 'بلال عاشور', phone: '+970599000221', subs: [{ published: 'MONTH', start: -8, created: [-8, '10:00'], pays: [] }] },
    { name: 'سلمى عياد', phone: '+970599000222', subs: [{ pkg: 'أسبوعي', start: -1, pays: [[-1, 12_000, 'CASH', 'r']] }] },
    { name: 'عبد الله الكحلوت', phone: '+970599000229', subs: [
      { pkg: 'يومي', start: -50, pays: [[-50, 2_500, 'CASH', 'r']] },
      { pkg: 'يومي', start: -33, pays: [[-33, 2_500, 'CASH', 'r']] },
      { pkg: 'يومي', start: -12, pays: [[-12, 2_500, 'CASH', 'r']] },
      { pkg: 'يومي', start: -2, pays: [[-2, 2_500, 'CASH', 'r']] },
    ] },
    { name: 'ميس الغول', phone: '+970599000230', subs: [{ pkg: '10 أيام خلال شهر', start: -50, pays: [[-50, 15_000, 'CASH', 'r']] }] },
  ];

  const customers = new Map<string, any>();
  const subsCreated: { sub: any; origEnd: string | null; plan: SubPlan; customerId: number }[] = [];
  const extensionAt = ago(23, '07:10');
  const firstClosed = ymd(-25);
  const lastClosed = ymd(-23);
  for (const [ci, plan] of plans.entries()) {
    let previous: any = null;
    for (const [si, sp] of plan.subs.entries()) {
      const startDay = sp.start;
      const weekday = at.date(startDay).getUTCDay();
      const created = sp.created ? ago(-sp.created[0], sp.created[1]) : ago(-startDay, hhmm((weekday === 5 ? 12 * 60 + 20 : 9 * 60 + 5) + ((ci * 7 + si * 3) % 50)));
      const by = staff(sp.by ?? (weekday === 5 ? 'o' : 'r'));
      let customer = customers.get(plan.name);
      if (!customer) {
        customer = await db.customer.create({
          data: { spaceId: palId, idempotencyKey: keyOf(`customer/${plan.name}`), name: plan.name, phone: plan.phone ?? null, createdAt: created, updatedAt: created },
        });
        customers.set(plan.name, customer);
        await audit(created, {
          actorId: by, action: 'customer.created', entityType: 'customer', entityId: customer.id, spaceId: palId,
          after: { name: plan.name, phone: plan.phone ?? null },
        });
      }
      let terms: any;
      if (sp.pkg) {
        const pack = packages.get(sp.pkg);
        terms = {
          name: pack.name, totalDays: pack.totalDays, daysPerWeek: pack.daysPerWeek, hoursPerDay: pack.hoursPerDay,
          totalHours: pack.totalHours, billing: pack.billing, priceAgorot: pack.priceAgorot, audience: pack.audience,
          shiftId: pack.shiftId, packageId: pack.id, publishedPeriod: null, endsOn: ymd(startDay + pack.validityDays - 1), priceTyped: null,
        };
      } else if (sp.published) {
        const days = sp.published === 'MONTH' ? 30 : 7;
        terms = {
          name: sp.published === 'MONTH' ? 'شهري' : 'أسبوعي', totalDays: null, daysPerWeek: null, hoursPerDay: null, totalHours: null,
          billing: 'FIXED', priceAgorot: sp.published === 'MONTH' ? 35_000 : 12_000, audience: 'GENERAL', shiftId: null,
          packageId: null, publishedPeriod: sp.published, endsOn: ymd(startDay + days - 1), priceTyped: null,
        };
      } else {
        const c = sp.custom!;
        terms = {
          name: c.name, totalDays: null, daysPerWeek: c.daysPerWeek ?? null, hoursPerDay: c.hoursPerDay ?? null,
          totalHours: c.totalHours ?? null, billing: c.billing, priceAgorot: c.price, audience: c.audience ?? 'GENERAL',
          shiftId: null, packageId: null, publishedPeriod: null, endsOn: c.ends === null ? null : ymd(c.ends),
          priceTyped: { byId: by, reason: c.reason },
        };
      }
      const startsOn = ymd(startDay);
      const renewalOfId = sp.renews ? previous.id : null;
      const sub = await db.subscription.create({
        data: {
          spaceId: palId, idempotencyKey: keyOf(`sub/${plan.name}/${si}`), customerId: customer.id,
          packageId: terms.packageId, publishedPeriod: terms.publishedPeriod, name: terms.name,
          startsOn: new Date(`${startsOn}T00:00:00Z`), endsOn: terms.endsOn ? new Date(`${terms.endsOn}T00:00:00Z`) : null,
          totalDays: terms.totalDays, daysPerWeek: terms.daysPerWeek, hoursPerDay: terms.hoursPerDay, totalHours: terms.totalHours,
          billing: terms.billing, priceAgorot: terms.priceAgorot, audience: terms.audience, shiftId: terms.shiftId,
          priceSetById: terms.priceTyped?.byId ?? null, priceReason: terms.priceTyped?.reason ?? null,
          renewalOfId, createdAt: created, updatedAt: created,
        },
      });
      await audit(created, {
        actorId: by, action: 'subscription.created', entityType: 'subscription', entityId: sub.id, spaceId: palId,
        after: {
          customerId: customer.id, packageId: terms.packageId, renewalOfId, name: terms.name, startsOn,
          endsOn: terms.endsOn, totalDays: terms.totalDays, daysPerWeek: terms.daysPerWeek, hoursPerDay: terms.hoursPerDay,
          totalHours: terms.totalHours, billing: terms.billing, priceAgorot: terms.priceAgorot, audience: terms.audience,
          shiftId: terms.shiftId, reason: terms.priceTyped?.reason ?? null,
        },
      });
      for (const [pi, [offset, amount, method, who, time]] of sp.pays.entries()) {
        const when = time ? ago(-offset, time) : new Date(created.getTime() + 60_000 + pi * 1000);
        await writePayment(ctx, { key: keyOf(`sub/${plan.name}/${si}/pay/${pi}`), item: { subscriptionId: sub.id }, amountAgorot: amount, method, byId: staff(who), at: when });
      }
      subsCreated.push({ sub, origEnd: terms.endsOn, plan: sp, customerId: customer.id });
      previous = sub;
    }
  }
  log(`customers: ${customers.size}, subscriptions: ${subsCreated.length}`);

  // The announcements: an ended notice, the closure (ended, its subscriptions extended), a running
  // offer and an upcoming event.
  const announce = async (data: { type: string; textAr: string; textEn: string; startsAt: Date; endsAt: Date | null; created: Date }, name: string) => {
    const row = await db.announcement.create({
      data: { spaceId: palId, type: data.type, textAr: data.textAr, textEn: data.textEn, startsAt: data.startsAt, endsAt: data.endsAt, idempotencyKey: keyOf(`announcement/${name}`), createdAt: data.created, updatedAt: data.created },
    });
    await audit(data.created, {
      actorId: ahmad.id, action: 'announcement.created', entityType: 'announcement', entityId: row.id, spaceId: palId,
      after: { type: data.type, startsAt: data.startsAt.toISOString(), endsAt: data.endsAt?.toISOString() ?? null },
    });
    return row;
  };
  await announce({ type: 'GENERAL', textAr: 'ركّبنا مكيفات جديدة في القاعة الرئيسية، أهلًا بكم.', textEn: 'New air conditioners in the main hall. Welcome!', startsAt: ago(45, '09:00'), endsAt: ago(38, '22:00'), created: ago(45, '08:50') }, 'ac');
  const closure = await announce({ type: 'CLOSURE', textAr: 'مغلقون اليوم وغدًا بسبب انقطاع الكهرباء وعطل في منظومة الطاقة الشمسية.', textEn: 'Closed today and tomorrow: a power outage and a fault in the solar system.', startsAt: ago(25, '07:30'), endsAt: null, created: ago(25, '07:30') }, 'closure');
  const closureEnd = ago(23, '07:00');
  await db.announcement.update({ where: { id: closure.id }, data: { endsAt: closureEnd, updatedAt: closureEnd } });
  await audit(closureEnd, {
    actorId: ahmad.id, action: 'announcement.ended', entityType: 'announcement', entityId: closure.id, spaceId: palId,
    before: { endsAt: null }, after: { endsAt: closureEnd.toISOString() },
  });
  // Covered: not ended early, existing then, an end on or after the closure's first day and a start
  // on or before its last.
  const covered = subsCreated.filter(({ sub, origEnd }) =>
    sub.createdAt < extensionAt && origEnd !== null && origEnd >= firstClosed && sub.startsOn.toISOString().slice(0, 10) <= lastClosed,
  );
  const extension = await db.closureExtension.create({
    data: { announcementId: closure.id, days: 2, appliedById: ahmad.id, idempotencyKey: keyOf('closure/extension'), createdAt: extensionAt, updatedAt: extensionAt },
  });
  for (const { sub, origEnd } of covered) {
    const moved = new Date(`${origEnd}T00:00:00Z`);
    moved.setUTCDate(moved.getUTCDate() + 2);
    await db.subscription.update({ where: { id: sub.id }, data: { endsOn: moved, updatedAt: extensionAt } });
    await db.subscriptionExtension.create({ data: { closureExtensionId: extension.id, subscriptionId: sub.id, createdAt: extensionAt, updatedAt: extensionAt } });
  }
  await audit(extensionAt, {
    actorId: ahmad.id, action: 'closure.subscriptionsExtended', entityType: 'announcement', entityId: closure.id, spaceId: palId,
    after: { days: 2, subscriptionIds: covered.map(({ sub }) => sub.id), renewalIds: [] },
  });
  await announce({ type: 'OFFER', textAr: 'خصم 15% على الاشتراك الشهري للطلاب لفترة محدودة.', textEn: '15% off the students’ monthly subscription, for a limited time.', startsAt: ago(5, '10:00'), endsAt: ago(-25, '22:00'), created: ago(5, '09:55') }, 'offer');
  await announce({ type: 'EVENT', textAr: 'ورشة مجانية: أساسيات العمل الحر عبر الإنترنت، الساعة 5 مساءً في قاعة التدريب.', textEn: 'Free workshop: freelancing basics, 5 pm in the training hall.', startsAt: ago(-3, '17:00'), endsAt: ago(-3, '20:00'), created: ago(1, '19:00') }, 'event');
  log(`closure extension: ${covered.length} subscriptions`);

  // Ended early.
  for (const { sub, plan } of subsCreated) {
    if (plan.endEarly === undefined) continue;
    const endedAt = ago(-plan.endEarly, '11:00');
    const current = await db.subscription.findUniqueOrThrow({ where: { id: sub.id } });
    const endsOn = ymd(plan.endEarly);
    await db.subscription.update({ where: { id: sub.id }, data: { endsOn: new Date(`${endsOn}T00:00:00Z`), endedAt, endedById: ahmad.id, updatedAt: endedAt } });
    await audit(endedAt, {
      actorId: ahmad.id, action: 'subscription.ended', entityType: 'subscription', entityId: sub.id, spaceId: palId,
      before: { endsOn: current.endsOn?.toISOString().slice(0, 10) ?? null }, after: { endsOn, endedAt: endedAt.toISOString() },
    });
  }

  // A package retired.
  const retired = packages.get('10 أيام خلال شهر');
  await db.package.update({ where: { id: retired.id }, data: { isActive: false, updatedAt: ago(20, '21:00') } });
  await audit(ago(20, '21:00'), {
    actorId: ahmad.id, action: 'package.edited', entityType: 'package', entityId: retired.id, spaceId: palId,
    before: { isActive: true }, after: { isActive: false },
  });

  // 60 days of history, ending yesterday.
  let totals = { checkIns: 0, visits: 0 };
  for (let offset = -60; offset <= -1; offset += 1) {
    const done = await writeDay(ctx, offset, { tag: 'hist' });
    totals = { checkIns: totals.checkIns + done.checkIns, visits: totals.visits + done.visits };
  }
  log(`history: ${totals.checkIns} check-ins, ${totals.visits} walk-in visits`);

  // Special visits: debts left to a phone's customer, a partial payment, a write-off, a voided payment,
  // and a stay closed by the system before the prices were published, priced by hand.
  const debtor = async (name: string, phone: string, when: Date, by: number) => {
    const row = await db.customer.create({ data: { spaceId: palId, name, phone, createdAt: when, updatedAt: when } });
    await audit(when, { actorId: by, action: 'customer.created', entityType: 'customer', entityId: row.id, spaceId: palId, after: { name, phone } });
    customers.set(name, row);
    return row;
  };
  const special = async (name: string, offset: number, inM: string, outM: string, opts: { phone?: string; pay?: number; by: 'o' | 'r'; method?: 'CASH' | 'TRANSFER'; auto?: boolean; audience?: 'STUDENT' }) => {
    const by = staff(opts.by);
    let customerId: number | null = null;
    if (opts.phone) customerId = (await debtor(name, opts.phone, ago(-offset, outM), by)).id;
    return writeVisit(ctx, {
      key: keyOf(`special/${name}`), offset, name, audience: opts.audience, inMinute: minutesOf(inM), outMinute: minutesOf(outM),
      auto: opts.auto, customerId, checkInBy: by, checkOutBy: by,
      pay: opts.pay === undefined ? null : opts.pay === 0 ? null : { amount: opts.pay, method: opts.method ?? 'CASH', byId: by },
    });
  };
  const mutaz = await special('معتز الكرد', -12, '10:00', '13:10', { phone: '+970599000223', by: 'r' });
  await writePayment(ctx, { key: keyOf('special/mutaz/pay'), item: { visitId: mutaz.id }, amountAgorot: 1_000, method: 'CASH', byId: laila.id, at: ago(5, '12:30') });
  await special('ياسمين عوض', -6, '09:15', '15:40', { phone: '+970599000224', pay: 1_000, by: 'r' });
  await special('حمزة شبير', -3, '12:00', '16:20', { phone: '+970599000225', by: 'r' });
  const israa = await special('إسراء دلول', -40, '10:00', '14:00', { phone: '+970599000226', by: 'r' });
  await writePayment(ctx, { key: keyOf('special/israa/pay'), item: { visitId: israa.id }, amountAgorot: israa.chargeAgorot, method: 'CASH', byId: laila.id, at: ago(38, '11:00') });
  const kareem = await special('كريم الزعانين', -18, '13:00', '17:30', { phone: '+970599000227', by: 'o' });
  await special('شهد أبو ندى', -9, '16:00', '18:00', { phone: '+970599000228', by: 'o' });
  const writeOffAt = ago(2, '11:30');
  const writeOffReason = 'زائر غادر ولا يمكن التواصل معه';
  await db.visit.update({ where: { id: kareem.id }, data: { writtenOffAt: writeOffAt, writtenOffById: ahmad.id, writeOffReason, updatedAt: writeOffAt } });
  await audit(writeOffAt, { actorId: ahmad.id, action: 'visit.writtenOff', entityType: 'visit', entityId: kareem.id, spaceId: palId, after: { reason: writeOffReason, balanceAgorot: kareem.chargeAgorot } });

  // A voided visit payment: recorded as cash, it was a transfer.
  const louay = await writeVisit(ctx, {
    key: keyOf('special/louay'), offset: -14, name: 'لؤي حمد', inMinute: 600, outMinute: 810,
    checkInBy: laila.id, checkOutBy: laila.id, pay: { method: 'CASH', byId: laila.id },
  });
  const wrong = await db.payment.findFirstOrThrow({ where: { visitId: louay.id } });
  await voidPayment(wrong, ahmad.id, ago(14, '18:20'), 'سُجّلت نقدًا والدفع كان تحويلًا', { visitId: louay.id });
  await writePayment(ctx, { key: keyOf('special/louay/pay/2'), item: { visitId: louay.id }, amountAgorot: louay.chargeAgorot, method: 'TRANSFER', byId: ahmad.id, at: ago(14, '18:21') });
  // Bilal: a payment typed as 100 ₪ when 200 ₪ was received, voided and recorded again; 100 ₪ more later.
  const bilal = subsCreated.find(({ plan }) => plan === plans.find((p) => p.name === 'بلال عاشور')!.subs[0])!.sub;
  const b1 = await writePayment(ctx, { key: keyOf('bilal/pay/1'), item: { subscriptionId: bilal.id }, amountAgorot: 10_000, method: 'CASH', byId: laila.id, at: ago(8, '10:01') });
  await voidPayment(b1, ahmad.id, ago(8, '17:40'), 'المبلغ المستلم 200 ₪ وليس 100 ₪', { subscriptionId: bilal.id });
  await writePayment(ctx, { key: keyOf('bilal/pay/2'), item: { subscriptionId: bilal.id }, amountAgorot: 20_000, method: 'CASH', byId: ahmad.id, at: ago(8, '17:41') });
  await writePayment(ctx, { key: keyOf('bilal/pay/3'), item: { subscriptionId: bilal.id }, amountAgorot: 10_000, method: 'TRANSFER', byId: ahmad.id, at: ago(1, '18:10') });

  // Before the prices: a stay the system closed at closing with no rate, priced by hand the next morning.
  const sameh = await writeVisit(ctx, { key: keyOf('special/sameh'), offset: -59, name: 'سامح عيد', inMinute: 15 * 60, outMinute: 22 * 60, auto: true, checkInBy: ahmad.id, pay: null });
  const pricedAt = ago(58, '09:10');
  const pricedReason = 'بقي حتى الإغلاق قبل نشر الأسعار: سعر اليوم';
  await db.visit.update({ where: { id: sameh.id }, data: { chargeAgorot: 2_500, chargeSetById: ahmad.id, chargeReason: pricedReason, updatedAt: pricedAt } });
  await audit(pricedAt, { actorId: ahmad.id, action: 'visit.priced', entityType: 'visit', entityId: sameh.id, spaceId: palId, after: { chargeAgorot: 2_500, reason: pricedReason } });
  await writePayment(ctx, { key: keyOf('special/sameh/pay'), item: { visitId: sameh.id }, amountAgorot: 2_500, method: 'CASH', byId: ahmad.id, at: ago(58, '09:12') });

  // Most of the visits the system closed at closing were paid the next day; a few stay uncollected.
  const uncollected = await db.visit.findMany({
    where: { spaceId: palId, checkoutMethod: 'AUTO', customerId: null, chargeAgorot: { not: null }, payments: { none: {} }, checkedOutAt: { lt: ago(2, '00:00') } },
    orderBy: { id: 'asc' },
  });
  let paidLater = 0;
  for (const v of uncollected) {
    if (!rng.chance(0.7)) continue;
    const next = new Date(v.checkedOutAt.getTime() + 12 * 3_600_000);
    await writePayment(ctx, { key: keyOf(`late/${v.id}`), item: { visitId: v.id }, amountAgorot: v.chargeAgorot, method: 'CASH', byId: laila.id, at: next });
    paidLater += 1;
  }
  log(`auto-closed visits: ${uncollected.length}, paid the next day: ${paidLater}`);

  // Archived customers.
  for (const plan of plans) {
    if (!plan.archived) continue;
    const c = customers.get(plan.name);
    const when = ago(-plan.archived[0], '20:30');
    await db.customer.update({ where: { id: c.id }, data: { archivedAt: when, updatedAt: when } });
    await audit(when, { actorId: staff(plan.archived[1]), action: 'customer.archived', entityType: 'customer', entityId: c.id, spaceId: palId, after: { archivedAt: when.toISOString() } });
  }
  {
    const c = customers.get('إسراء دلول');
    const when = ago(30, '20:40');
    await db.customer.update({ where: { id: c.id }, data: { archivedAt: when, updatedAt: when } });
    await audit(when, { actorId: laila.id, action: 'customer.archived', entityType: 'customer', entityId: c.id, spaceId: palId, after: { archivedAt: when.toISOString() } });
  }

  // The owner keeps the facts fresh: every group confirmed yesterday evening.
  const confirmedAt = ago(1, '21:30');
  const palNow = await db.space.findUniqueOrThrow({ where: { id: palId } });
  for (const [group, column] of [['profile', 'profileUpdatedAt'], ['hours', 'hoursUpdatedAt'], ['prices', 'pricesUpdatedAt'], ['amenities', 'amenitiesUpdatedAt'], ['contacts', 'contactsUpdatedAt']] as const) {
    await audit(confirmedAt, {
      actorId: ahmad.id, action: `space.${group}Confirmed`, entityType: 'space', entityId: palId, spaceId: palId,
      before: { [column]: (palNow as any)[column].toISOString() }, after: { [column]: confirmedAt.toISOString() },
    });
  }
  await db.space.update({
    where: { id: palId },
    data: { profileUpdatedAt: confirmedAt, hoursUpdatedAt: confirmedAt, pricesUpdatedAt: confirmedAt, amenitiesUpdatedAt: confirmedAt, contactsUpdatedAt: confirmedAt, updatedAt: confirmedAt },
  });

  // 5. The seed's demo space leaves every list: soft-deleted by the admin, as the app deletes.
  // Seconds after the seed made it: before every entry this build writes tonight.
  const deletedAt = new Date(demoSpace.createdAt.getTime() + 5_000);
  await db.space.update({ where: { id: demoSpace.id }, data: { deletedAt, updatedAt: deletedAt } });
  await audit(deletedAt, { actorId: admin.id, action: 'space.deleted', entityType: 'space', entityId: demoSpace.id, spaceId: demoSpace.id, before: { deletedAt: null }, after: { deletedAt: deletedAt.toISOString() } });
  decisions.push('«مساحة تجريبية» (masaha-demo) is soft-deleted by the admin (space.deleted), right after the seed made it; its links are kept and count for nothing (the app’s rule), so the demo owner and reception see only Pal Hub. It remains only in the admin’s deleted-spaces filter and that one audit entry.');

  // 6. No space full: the seed's full one gets a capacity above its people; no override stays.
  const sada = await db.space.findUniqueOrThrow({ where: { slug: 'sada-space' }, include: { occupancy: true } });
  const capAt = ago(10, '13:00');
  await db.spaceOccupancy.update({ where: { spaceId: sada.id }, data: { capacity: 12, updatedAt: capAt } });
  await audit(capAt, { actorId: sami.id, action: 'space.capacityEdited', entityType: 'space', entityId: sada.id, spaceId: sada.id, before: { capacity: sada.occupancy.capacity }, after: { capacity: 12 } });
  const overrides = await db.spaceOccupancy.findMany({ where: { stateOverride: { not: null } } });
  for (const o of overrides) {
    await db.spaceOccupancy.update({ where: { spaceId: o.spaceId }, data: { stateOverride: null, stateOverrideUntil: null, stateOverrideById: null } });
    await audit(new Date(), { actorId: o.stateOverrideById, action: 'space.statusOverrideCleared', entityType: 'space', entityId: o.spaceId, spaceId: o.spaceId, before: { state: o.stateOverride } });
  }
  decisions.push(`sada-space (the seed's full one: 4 present of 4) has its capacity raised to 12 by its owner (space.capacityEdited); ${overrides.length} manual override(s) cleared.`);

  // 7. Data reports and favourites.
  const allSpaces = await db.space.findMany({ where: { deletedAt: null, isHidden: false } });
  const bySlug = new Map<string, any>(allSpaces.map((s: any) => [s.slug, s]));
  const userByEmail = new Map<string, any>(users.map((u) => [u.email, u]));
  const demoUser = userByEmail.get('demo-user@example.com');
  const u = (i: number) => users[i]!;
  const verifiedOwner = (slug: string) => owners.get(slug) ?? (bySlug.get(slug) && slug !== MANAGED_SLUG ? sami.id : null);
  const report = async (r: { slug: string; user: any; field: string; message?: string; created: Date; decision?: { status: 'RESOLVED' | 'DISMISSED'; by: number; as: 'OWNER' | 'ADMIN'; at: Date; note: string | null } }) => {
    const space = bySlug.get(r.slug);
    if (!space) throw new Error(`report: no space ${r.slug}`);
    const created = r.created < space.createdAt ? new Date(space.createdAt.getTime() + 3 * 3_600_000) : r.created;
    const row = await db.dataReport.create({
      data: {
        spaceId: space.id, userId: r.user.id, field: r.field, message: r.message ?? null,
        status: r.decision?.status ?? 'OPEN', resolvedById: r.decision?.by ?? null, resolvedAt: r.decision?.at ?? null,
        resolutionNote: r.decision?.note ?? null, resolvedAs: r.decision?.as ?? null,
        createdAt: created, updatedAt: r.decision?.at ?? created,
      },
    });
    if (r.decision) {
      await audit(r.decision.at, {
        actorId: r.decision.by, action: r.decision.status === 'RESOLVED' ? 'dataReport.resolved' : 'dataReport.dismissed',
        entityType: 'dataReport', entityId: row.id, spaceId: space.id, after: { note: r.decision.note },
      });
    }
  };
  // The managed space's: one pending, one resolved with a note, one dismissed with a reply.
  await report({ slug: MANAGED_SLUG, user: u(5), field: 'HOURS', message: 'مكتوب أنكم تفتحون يوم الجمعة الساعة 12 ظهرًا، هل هذا صحيح؟', created: ago(2, '14:05') });
  await report({ slug: MANAGED_SLUG, user: u(8), field: 'PRICES', message: 'سعر الطالب اليومي غير واضح.', created: ago(40, '13:20'), decision: { status: 'RESOLVED', by: ahmad.id, as: 'OWNER', at: ago(39, '10:15'), note: 'شكرًا لك، أضفنا سعر الطالب اليومي إلى الأسعار المنشورة.' } });
  await report({ slug: MANAGED_SLUG, user: u(11), field: 'LOCATION', message: 'الدبوس على الخريطة ليس عند المدخل.', created: ago(15, '18:40'), decision: { status: 'DISMISSED', by: ahmad.id, as: 'OWNER', at: ago(14, '09:30'), note: 'الموقع صحيح: المدخل من جهة مول الرحاب، الطابق الثاني.' } });
  // Pending for the admin (unverified spaces).
  await report({ slug: 'jreas-hub', user: u(2), field: 'PRICES', message: 'هل المساحة مجانية فعلًا؟ لا توجد أسعار منشورة.', created: ago(1, '11:40') });
  await report({ slug: 'masahat', user: u(9), field: 'HOURS', message: 'هل تعمل المساحة على مدار الساعة فعلًا؟', created: ago(2, '22:10') });
  await report({ slug: 'white-space', user: u(14), field: 'CONTACT', created: ago(1, '16:25') });
  await report({ slug: 'golden-hub', user: u(17), field: 'LOCATION', message: 'الدبوس بعيد قليلًا عن مدخل العمارة.', created: ago(3, '12:00') });
  await report({ slug: 'coma-io', user: u(20), field: 'OTHER', message: 'يوجد دورات تدريبية مسائية غير مذكورة في الصفحة.', created: ago(2, '19:30') });
  // Decided by the admin.
  await report({ slug: 'masar-tech', user: u(3), field: 'AMENITIES', message: 'لديهم طاقة شمسية وكهرباء مستقرة.', created: ago(7, '15:00'), decision: { status: 'RESOLVED', by: admin.id, as: 'ADMIN', at: ago(6, '10:20'), note: 'تم التحقق وإضافة المرافق، شكرًا.' } });
  await report({ slug: 'nasr-coworking', user: u(12), field: 'CONTACT', created: ago(12, '09:45'), decision: { status: 'DISMISSED', by: admin.id, as: 'ADMIN', at: ago(11, '13:00'), note: 'الرقم صحيح وتم التأكد منه هاتفيًا.' } });
  // The demo user's own: one pending, one resolved, one dismissed.
  await report({ slug: 'al-salam-hub', user: demoUser, field: 'HOURS', message: 'أعتقد أنهم يفتحون يوم الجمعة أيضًا.', created: ago(1, '20:05') });
  await report({ slug: 'palm-space', user: demoUser, field: 'PRICES', message: 'السعر اليومي أصبح 20 شيكل.', created: ago(13, '17:00'), decision: { status: 'RESOLVED', by: admin.id, as: 'ADMIN', at: ago(12, '11:30'), note: 'شكرًا، سنراجع الأسعار مع المساحة.' } });
  await report({ slug: 'beit-lahia-desk', user: demoUser, field: 'HOURS', created: ago(7, '10:10'), decision: { status: 'DISMISSED', by: admin.id, as: 'ADMIN', at: ago(6, '12:45'), note: 'المواعيد مؤكدة من المساحة نفسها.' } });
  // Decided by owners.
  await report({ slug: 'focus-hub', user: u(6), field: 'PRICES', message: 'لا يوجد سعر شهري للطلاب.', created: ago(4, '13:00'), decision: { status: 'RESOLVED', by: owners.get('focus-hub')!, as: 'OWNER', at: ago(3, '09:40'), note: 'أضفنا سعر الطلاب الشهري، شكرًا.' } });
  await report({ slug: 'noor-hub', user: u(16), field: 'HOURS', created: ago(9, '20:00'), decision: { status: 'DISMISSED', by: verifiedOwner('noor-hub')!, as: 'OWNER', at: ago(8, '10:00'), note: 'المواعيد المنشورة صحيحة.' } });
  await report({ slug: 'deir-al-balah-campus', user: u(22), field: 'AMENITIES', message: 'عندهم قاعة اجتماعات كبيرة.', created: ago(11, '12:00'), decision: { status: 'RESOLVED', by: verifiedOwner('deir-al-balah-campus')!, as: 'OWNER', at: ago(10, '09:15'), note: 'صحيح، شكرًا للتنبيه.' } });
  await report({ slug: 'tuffah-place', user: u(25), field: 'PRICES', message: 'الأسعار المنشورة قديمة.', created: ago(4, '18:30') });
  await report({ slug: 'branch-hub', user: u(27), field: 'OTHER', message: 'يوجد موقف سيارات قريب، يُستحسن ذكره.', created: ago(2, '12:30') });

  // Favourites: the real spaces most, the directory's too.
  const realSlugs = REAL_SPACES.map((s) => s.slug);
  const seedSlugs = allSpaces.map((s: any) => s.slug).filter((s: string) => !realSlugs.includes(s));
  let favourites = 0;
  const favourite = async (user: any, slug: string) => {
    const space = bySlug.get(slug);
    const from = Math.max(user.createdAt.getTime(), space.createdAt.getTime());
    const when = new Date(from + rng.next() * (NOW.getTime() - from - 60_000));
    await db.favorite.create({ data: { userId: user.id, spaceId: space.id, createdAt: when, updatedAt: when } });
    favourites += 1;
  };
  for (const slug of ['pal-hub', 'branch-hub', 'masahat', 'focus-hub', 'noor-hub']) await favourite(demoUser, slug);
  for (const user of users.slice(1)) {
    const chosen = new Set<string>();
    const n = rng.int(1, 5);
    while (chosen.size < n) chosen.add(rng.chance(0.65) ? rng.pick(realSlugs) : rng.pick(seedSlugs));
    for (const slug of chosen) await favourite(user, slug);
  }
  log(`favourites: ${favourites}`);

  await writeFile(summaryPath, JSON.stringify({ builtAt: NOW.toISOString(), dbName, decisions, photos: null }, null, 2));
}

// ─── Helpers ────────────────────────────────────────────────────────────────────────────────

function weekOf(config: RealSpace, page: any): ([number, number] | null)[] {
  if (config.hours === 'around-the-clock') return [0, 1, 2, 3, 4, 5, 6].map(() => [0, 1440]);
  if (config.hours === 'live') {
    if (!page.hours) throw new Error(`${config.slug}: no live hours`);
    return page.hours.days.map((d: any) => (d ? [d.opensMinute, d.closesMinute] : null));
  }
  const h = config.hours;
  return [0, 1, 2, 3, 4, 5, 6].map((day) => {
    const range = day === 5 && h.friday !== undefined ? h.friday : day === 6 && h.saturday !== undefined ? h.saturday : h.open;
    return range ? [minutesOf(range[0]), minutesOf(range[1])] : null;
  });
}

function priceRows(config: RealSpace, page: any, shifts: { id: number; nameEn: string }[]) {
  const rows: { period: string; audience: string; shiftId: number | null; labelAr: null; labelEn: null; amountAgorot: number }[] = [];
  const p = config.prices!;
  const add = (period: string, audience: string, shekels: number | undefined, shiftId: number | null = null) => {
    if (shekels === undefined) return;
    if (rows.some((r) => r.period === period && r.audience === audience && r.shiftId === shiftId)) return;
    rows.push({ period, audience, shiftId, labelAr: null, labelEn: null, amountAgorot: Math.round(shekels * 100) });
  };
  if (p.keepLive && page?.prices) {
    for (const lp of page.prices) add(lp.period, lp.audience, lp.amountAgorot / 100, null);
  }
  add('HOUR', 'GENERAL', p.hour);
  add('DAY', 'GENERAL', p.day);
  add('WEEK', 'GENERAL', p.week);
  add('MONTH', 'GENERAL', p.month);
  add('HOUR', 'STUDENT', p.studentHour);
  add('DAY', 'STUDENT', p.studentDay);
  add('MONTH', 'STUDENT', p.studentMonth);
  for (const shift of config.shifts ?? []) {
    const id = shifts.find((s: any) => s.nameEn === shift.nameEn)?.id;
    if (id === undefined) throw new Error(`${config.slug}: no shift ${shift.nameEn}`);
    add('MONTH', 'GENERAL', shift.month, id);
  }
  return rows;
}

function priceValue(p: any) {
  return { period: p.period, audience: p.audience, shiftId: p.shiftId, labelAr: p.labelAr, labelEn: p.labelEn, amountAgorot: p.amountAgorot };
}

async function voidPayment(row: any, byId: number, when: Date, reason: string, item: object) {
  await db.payment.update({ where: { id: row.id }, data: { voidedAt: when, voidedById: byId, voidReason: reason } });
  await audit(when, {
    actorId: byId, action: 'payment.voided', entityType: 'payment', entityId: row.id, spaceId: row.spaceId,
    after: { ...item, amountAgorot: row.amountAgorot, method: row.method, reason },
  });
}

// ─── Photos (through the local API) ─────────────────────────────────────────────────────────

const API = `http://localhost:${process.env.PORT ?? '3000'}/api/v1`;

async function call(method: string, path: string, token: string | null, body?: any, form?: FormData): Promise<any> {
  for (let attempt = 0; ; attempt += 1) {
    const res = await fetch(API + path, {
      method,
      headers: { ...(token ? { authorization: `Bearer ${token}` } : {}), ...(body ? { 'content-type': 'application/json' } : {}) },
      body: form ?? (body ? JSON.stringify(body) : undefined),
    });
    if (res.status === 429 && attempt < 40) {
      const wait = Math.min(Number(res.headers.get('retry-after') ?? 60), 120);
      log(`429 on ${method} ${path}: waiting ${wait}s`);
      await new Promise((r) => setTimeout(r, wait * 1000));
      continue;
    }
    const text = await res.text();
    const json = text ? JSON.parse(text) : null;
    if (!res.ok) throw new Error(`${method} ${path}: ${res.status} ${text.slice(0, 300)}`);
    return json?.data ?? json;
  }
}

async function login(email: string, password: string): Promise<string> {
  const session = await call('POST', '/auth/login', null, { email, password });
  return session.accessToken;
}

const normalise = (s: string) =>
  s
    .normalize('NFC')
    .replace(/[\u064B-\u065F\u0670\u0640]/g, '')
    .replace(/[أإآٱ]/g, 'ا')
    .replace(/ة/g, 'ه')
    .replace(/ى/g, 'ي')
    .replace(/\bهب\b/g, 'هاب')
    .replace(/[^\p{L}\p{N}]+/gu, '')
    .toLowerCase();

function distance(a: string, b: string): number {
  const d = Array.from({ length: a.length + 1 }, (_, i) => [i, ...Array(b.length).fill(0)]);
  for (let j = 1; j <= b.length; j += 1) d[0]![j] = j;
  for (let i = 1; i <= a.length; i += 1)
    for (let j = 1; j <= b.length; j += 1)
      d[i]![j] = Math.min(d[i - 1]![j]! + 1, d[i]![j - 1]! + 1, d[i - 1]![j - 1]! + (a[i - 1] === b[j - 1] ? 0 : 1));
  return d[a.length]![b.length]!;
}

async function thumb(buffer: Buffer): Promise<Buffer> {
  return sharp(buffer).resize(16, 16, { fit: 'fill' }).grayscale().raw().toBuffer();
}
async function same(a: Buffer, b: Buffer): Promise<boolean> {
  const [x, y] = [await thumb(a), await thumb(b)];
  let diff = 0;
  for (let i = 0; i < x.length; i += 1) diff += Math.abs(x[i]! - y[i]!);
  return diff / x.length < 14;
}

/** As the web does before sending: at most 1600 on the longest side, a JPEG. */
async function shrink(buffer: Buffer): Promise<Buffer> {
  return sharp(buffer).rotate().resize({ width: 1600, height: 1600, fit: 'inside', withoutEnlargement: true }).jpeg({ quality: 86 }).toBuffer();
}

async function buildPhotos() {
  const statePath = join(HERE, `photos-done-${dbName}.json`);
  const done: Record<string, string[]> = existsSync(statePath) ? JSON.parse(await readFile(statePath, 'utf8')) : {};
  const summary = existsSync(summaryPath) ? JSON.parse(await readFile(summaryPath, 'utf8')) : { decisions: [] };

  const files: string[] = [];
  for (const dir of [PHOTO_DIR, join(PHOTO_DIR, 'generated')]) {
    if (!existsSync(dir)) continue;
    for (const f of await readdir(dir, { withFileTypes: true })) {
      if (f.isFile() && /\.(jpe?g|png|webp)$/i.test(f.name)) files.push(join(dir, f.name));
    }
  }
  const spaces = await db.space.findMany({ where: { deletedAt: null }, include: { managers: { where: { deactivatedAt: null, role: 'OWNER' } } } });
  const bySlug = new Map<string, any>(spaces.map((s: any) => [s.slug, s]));
  const realSlugs = REAL_SPACES.map((s) => s.slug);

  // Match every file to a space.
  const matches: { file: string; slug: string; order: number; how: string }[] = [];
  const unmatched: string[] = [];
  for (const path of files) {
    const name = path.split(/[\\/]/).pop()!;
    const base = name.slice(0, -extname(name).length);
    const bySlugName = /^([a-z0-9]+(?:-[a-z0-9]+)*?)(?:-(\d+))?$/.exec(base);
    if (PHOTO_MAP[name.normalize('NFC')]) {
      matches.push({ file: path, slug: PHOTO_MAP[name.normalize('NFC')]!, order: 1, how: 'the supervisor’s table' });
    } else if (bySlugName && bySlug.has(bySlugName[1]!)) {
      matches.push({ file: path, slug: bySlugName[1]!, order: Number(bySlugName[2] ?? 1), how: 'slug file name' });
    } else if (bySlug.has(base)) {
      matches.push({ file: path, slug: base, order: 1, how: 'slug file name' });
    } else {
      const n = normalise(base);
      let best: { slug: string; d: number } | null = null;
      for (const s of spaces) {
        for (const candidate of [s.nameAr, s.nameEn, s.slug]) {
          if (!candidate) continue;
          const d = distance(n, normalise(candidate));
          if (!best || d < best.d) best = { slug: s.slug, d };
        }
      }
      if (best && best.d <= 2) matches.push({ file: path, slug: best.slug, order: 1, how: `name match (distance ${best.d})` });
      else unmatched.push(name);
    }
  }

  // Tokens: the admin, and each verified space's owner.
  const tokens = new Map<number, string>();
  const admin = await db.user.findUniqueOrThrow({ where: { email: process.env.SEED_ADMIN_EMAIL!.toLowerCase() } });
  tokens.set(admin.id, await login(admin.email, process.env.SEED_ADMIN_PASSWORD!));
  const tokenFor = async (userId: number) => {
    if (!tokens.has(userId)) {
      const user = await db.user.findUniqueOrThrow({ where: { id: userId } });
      tokens.set(userId, await login(user.email, process.env.SEED_DEMO_PASSWORD!));
    }
    return tokens.get(userId)!;
  };

  const report: Record<string, string[]> = {};
  const live = join(HERE, 'live-covers');
  for (const space of spaces) {
    if (done[space.slug]) {
      report[space.slug] = done[space.slug]!;
      continue;
    }
    const isReal = realSlugs.includes(space.slug);
    const own = matches.filter((m) => m.slug === space.slug).sort((a, b) => (a.how === 'slug file name' ? 1 : 0) - (b.how === 'slug file name' ? 1 : 0) || a.order - b.order);
    const queue: { label: string; buffer: Buffer }[] = [];
    for (const m of own) queue.push({ label: m.file.split(/[\\/]/).pop()!, buffer: await readFile(m.file) });
    if (isReal) {
      const coverPath = join(live, `${space.slug}.webp`);
      if (existsSync(coverPath)) {
        const cover = await readFile(coverPath);
        let duplicate = false;
        for (const q of queue) if (await same(q.buffer, cover)) duplicate = true;
        if (duplicate) report[space.slug] = [...(report[space.slug] ?? []), 'live cover: the same picture as the owner’s file, not added twice'];
        else queue.push({ label: 'live cover', buffer: cover });
      }
    }
    if (queue.length === 0) {
      report[space.slug] = ['no file: the seed’s pictures kept'];
      continue;
    }
    const ownerId = space.managers[0]?.userId as number | undefined;
    const actorId = ownerId ?? admin.id;
    const token = ownerId ? await tokenFor(ownerId) : tokens.get(admin.id)!;
    const base = ownerId ? `/manage/spaces/${space.id}/photos` : `/admin/spaces/${space.id}/photos`;
    // The seed's drawn pictures go first, through the API.
    const existing = await call('GET', base, token);
    for (const photo of existing) await call('DELETE', `${base}/${photo.id}`, token);
    const added: string[] = [];
    for (const q of queue) {
      const form = new FormData();
      form.append('photo', new Blob([await shrink(q.buffer)], { type: 'image/jpeg' }), 'photo.jpg');
      await call('POST', base, token, undefined, form);
      added.push(q.label);
    }
    const line = [`removed ${existing.length}`, ...added.map((a) => `+ ${a}`), `by ${actorId === admin.id ? 'admin' : 'owner'}`];
    report[space.slug] = [...(report[space.slug] ?? []), ...line];
    done[space.slug] = report[space.slug]!;
    await writeFile(statePath, JSON.stringify(done, null, 2));
    log(`${space.slug}: ${line.join(', ')}`);
  }
  summary.photos = { files: files.length, matches: matches.map((m) => ({ file: m.file.split(/[\\/]/).pop(), slug: m.slug, how: m.how })), unmatched, perSpace: report };
  await writeFile(summaryPath, JSON.stringify(summary, null, 2));
  log(`photos: ${files.length} files, ${matches.length} matched, unmatched: ${unmatched.join(', ') || 'none'}`);
}

// ─── Checks ─────────────────────────────────────────────────────────────────────────────────

async function checks() {
  const rows = await db.$queryRawUnsafe(`
    SELECT s.slug, o.capacity, o.state_override,
      (SELECT count(*) FROM visits v WHERE v.space_id = s.id AND v.checked_out_at IS NULL)::int AS visits,
      (SELECT count(*) FROM check_ins c WHERE c.space_id = s.id AND c.checked_out_at IS NULL)::int AS checkins
    FROM spaces s LEFT JOIN space_occupancy o ON o.space_id = s.id WHERE s.deleted_at IS NULL`);
  const full = (rows as any[]).filter((r) => r.state_override === 'FULL' || (r.capacity !== null && r.visits + r.checkins >= r.capacity));
  if (full.length) throw new Error(`Full: ${full.map((r) => r.slug).join(', ')}`);
  const counts: Record<string, number> = {};
  const pal = await db.space.findUniqueOrThrow({ where: { slug: MANAGED_SLUG } });
  counts.spaces = await db.space.count({ where: { deletedAt: null } });
  counts.verified = (await db.$queryRawUnsafe(`SELECT count(DISTINCT space_id)::int AS n FROM space_managers m JOIN spaces s ON s.id = m.space_id WHERE m.role = 'OWNER' AND m.deactivated_at IS NULL AND s.deleted_at IS NULL`) as any[])[0].n;
  counts.users = await db.user.count();
  counts.customers = await db.customer.count({ where: { spaceId: pal.id } });
  counts.subscriptions = await db.subscription.count({ where: { spaceId: pal.id } });
  counts.visits = await db.visit.count({ where: { spaceId: pal.id } });
  counts.checkIns = await db.checkIn.count({ where: { spaceId: pal.id } });
  counts.payments = await db.payment.count({ where: { spaceId: pal.id } });
  counts.reports = await db.dataReport.count();
  counts.favourites = await db.favorite.count();
  counts.audit = await db.auditLog.count();
  counts.photos = await db.spacePhoto.count();
  log('no space full; counts', counts);
  const summary = existsSync(summaryPath) ? JSON.parse(await readFile(summaryPath, 'utf8')) : {};
  summary.counts = counts;
  await writeFile(summaryPath, JSON.stringify(summary, null, 2));
}

try {
  if (phase === 'all' || phase === 'data') await buildData();
  if (phase === 'all' || phase === 'photos') await buildPhotos();
  await checks();
} finally {
  await db.$disconnect();
}
