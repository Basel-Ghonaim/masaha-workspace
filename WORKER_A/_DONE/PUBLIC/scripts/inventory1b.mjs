// Read-only data inventory for PUBLIC PR 1b's real run: plain GETs, no write, no sign-in.
const base = 'http://localhost:3320/api/v1';

async function get(path, headers = {}) {
  const response = await fetch(base + path, { headers });
  return { status: response.status, body: await response.json() };
}

async function total(query, headers) {
  const { status, body } = await get(`/spaces?limit=50&${query}`, headers);
  return status === 200 ? `${body.meta.totalRecords}` : `HTTP ${status} ${JSON.stringify(body.error)}`;
}

const listed = [];
for (let page = 1; ; page += 1) {
  const { body } = await get(`/spaces?limit=50&page=${page}`);
  listed.push(...body.data);
  if (page >= body.meta.totalPages) break;
}
console.log('listed spaces:', listed.length);
const areas = new Map();
for (const space of listed) areas.set(space.area.nameEn, (areas.get(space.area.nameEn) ?? 0) + 1);
console.log('areas with spaces:', JSON.stringify([...areas]));
console.log('verified:', listed.filter((s) => s.isVerified).length, 'unverified:', listed.filter((s) => !s.isVerified).length);
console.log('live AVAILABLE:', listed.filter((s) => s.liveStatus === 'AVAILABLE').map((s) => s.slug).join(' ') || 'none');
console.log('live FULL:', listed.filter((s) => s.liveStatus === 'FULL').length, 'CLOSED:', listed.filter((s) => s.liveStatus === 'CLOSED').length);
console.log('with hours:', listed.filter((s) => s.days !== null).length, 'with a cover:', listed.filter((s) => s.cover !== null).length);
console.log('day budget 10–30 ₪ (period=DAY&priceMin=1000&priceMax=3000):', await total('period=DAY&priceMin=1000&priceMax=3000'));
console.log('studentPrices=true:', await total('studentPrices=true'));
console.log('openFriday=true:', await total('openFriday=true'));
console.log('availableNow=true:', await total('availableNow=true'));
console.log('verified=true:', await total('verified=true'));
const near = await get('/spaces?limit=50&sort=distance', { 'Masaha-Near': '31.5,34.46' });
console.log('sort=distance from 31.5,34.46:', near.status, near.status === 200 ? near.body.data.slice(0, 5).map((s) => `${s.slug}=${s.distanceMeters}`).join(' ') : JSON.stringify(near.body));
