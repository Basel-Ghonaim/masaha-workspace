// Read-only data inventory for PUBLIC PR 4's real run (Home, About, errors, #108's carried gaps): plain GETs only.
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
const states = {};
for (const card of listed) states[card.liveStatus ?? 'none'] = (states[card.liveStatus ?? 'none'] ?? 0) + 1;
console.log('live states on the cards:', JSON.stringify(states));

const available = await get('/spaces?availableNow=true&limit=6');
console.log('availableNow=true limit=6:', available.status, 'got', available.body.data?.length, 'total', available.body.meta?.total);

const near = await get('/spaces?sort=distance&limit=6', { 'Masaha-Near': '31.515,34.450' });
console.log('sort=distance near Gaza City:', near.status, near.body.data?.map((c) => `${c.slug}@${c.distanceMeters}`).join(' '));

const map = await get('/map/spaces');
const pins = map.body.data.pins;
console.log('GET /map/spaces:', map.status, 'pins:', pins.length, 'truncated:', map.body.data.truncated);
console.log('pin keys:', Object.keys(pins[0] ?? {}).join(','));
const byArea = {};
for (const pin of pins) byArea[pin.areaId] = (byArea[pin.areaId] ?? 0) + 1;
console.log('pins by areaId:', JSON.stringify(byArea));

const lookups = await get('/lookups');
const areas = lookups.body.data.areas ?? [];
console.log('catalogue areas:', areas.length, 'with spaces:', areas.filter((a) => byArea[a.id]).length);

const rows = [];
for (const card of listed) {
  const { status, body } = await get(`/spaces/${encodeURIComponent(card.slug)}`);
  if (status !== 200) continue;
  const s = body.data;
  rows.push({
    slug: s.slug,
    verified: s.isVerified,
    live: card.liveStatus ?? 'none',
    photos: s.photos.length,
    bar: s.contacts.some((c) => c.type === 'PHONE' || c.type === 'WHATSAPP') ? 'y' : 'n',
    contacts: s.contacts.map((c) => c.type).join(','),
  });
}
console.table(rows.filter((r) => r.photos > 0 || r.bar === 'n' || r.live !== 'none').slice(0, 40));
console.log('spaces with no phone/whatsapp:', rows.filter((r) => r.bar === 'n').map((r) => r.slug).join(' '));
console.log('spaces with 3+ photos:', rows.filter((r) => r.photos >= 3).map((r) => `${r.slug}(${r.photos})`).join(' '));
console.log('spaces with 6+ photos:', rows.filter((r) => r.photos >= 6).map((r) => `${r.slug}(${r.photos})`).join(' '));
console.log('verified with a live status:', rows.filter((r) => r.verified && r.live !== 'none').map((r) => `${r.slug}:${r.live}`).join(' '));
