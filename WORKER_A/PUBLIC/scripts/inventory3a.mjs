// Read-only data inventory for PUBLIC PR 3a's real run (the space page): plain GETs, no write, no sign-in.
const base = 'http://localhost:3320/api/v1';

async function get(path, headers = {}) {
  const response = await fetch(base + path, { headers });
  return { status: response.status, body: await response.json() };
}

const listed = [];
for (let page = 1; ; page += 1) {
  const { body } = await get(`/spaces?limit=50&page=${page}`);
  listed.push(...body.data);
  if (page >= body.meta.totalPages) break;
}
console.log('listed spaces:', listed.length);
const map = await get('/map/spaces');
console.log('GET /map/spaces:', map.status, 'pins:', map.body.data.pins.length);

const rows = [];
for (const card of listed) {
  const { status, body } = await get(`/spaces/${encodeURIComponent(card.slug)}`);
  if (status !== 200) {
    console.log(card.slug, 'status', status);
    continue;
  }
  const s = body.data;
  const shifts = s.hours?.shifts ?? [];
  const row = {
    slug: s.slug,
    verified: s.isVerified,
    live: card.liveStatus,
    hours: s.hours === null ? 'null' : `${(s.hours.days ?? []).filter(Boolean).length}d/${shifts.length}sh`,
    prices: s.prices === null ? 'HIDDEN' : s.prices.length,
    shiftPrices: (s.prices ?? []).filter((p) => p.shiftId != null).length,
    student: (s.prices ?? []).filter((p) => p.audience === 'STUDENT').length,
    amenities: s.amenities.length,
    contacts: s.contacts.map((c) => c.type).join(','),
    stale: s.staleGroups.join(','),
    photos: s.photos.length,
    desc: s.descriptionAr || s.descriptionEn ? 'y' : 'n',
    nameAr: s.nameAr ? 'y' : 'n',
  };
  rows.push(row);
}
console.table(rows);
const unknown = await get('/spaces/no-such-space');
console.log('GET /spaces/no-such-space:', unknown.status, unknown.body.error?.code);
const one = rows[0] && (await get(`/spaces/${rows[0].slug}`));
console.log('price sample keys:', JSON.stringify(one?.body.data.prices?.[0]));
console.log('hours sample:', JSON.stringify(one?.body.data.hours)?.slice(0, 400));
console.log('contact sample:', JSON.stringify(one?.body.data.contacts?.[0]));
console.log('updatedAt sample:', JSON.stringify(one?.body.data.updatedAt));
