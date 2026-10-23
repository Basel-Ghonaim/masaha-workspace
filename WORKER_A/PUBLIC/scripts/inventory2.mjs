// Read-only data inventory for PUBLIC PR 2's real run (the map): plain GETs, no write, no sign-in.
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
const pins = map.body.data.pins;
console.log('GET /map/spaces:', map.status, 'pins:', pins.length, 'truncated:', map.body.data.truncated);
for (const state of ['AVAILABLE', 'FULL', 'CLOSED', null]) {
  const these = pins.filter((pin) => pin.liveStatus === state);
  console.log(`pins ${state ?? 'none'}:`, these.length, these.slice(0, 6).map((p) => p.slug).join(' '));
}
console.log('pins with a cover:', pins.filter((p) => p.cover !== null).length);
const verified = await get('/map/spaces?verified=true');
console.log('GET /map/spaces?verified=true:', verified.status, verified.body.data.pins.length);
const none = await get('/map/spaces?q=zzzzqqqq');
console.log('GET /map/spaces?q=zzzzqqqq (no match):', none.status, none.body.data.pins.length);
const box = await get('/map/spaces?bounds=31.4,34.3,31.55,34.5');
console.log('GET /map/spaces?bounds=31.4,34.3,31.55,34.5:', box.status, box.body.data.pins.length);
for (const slug of ['sada-space', 'tal-al-hawa-desks', 'radwan-study-hall', 'shati-sea-view']) {
  const pin = pins.find((p) => p.slug === slug);
  console.log(`${slug}:`, pin ? `${pin.liveStatus} at ${pin.location.lat},${pin.location.lng}` : 'not on the map');
}
