// Read-only data inventory for PUBLIC PR 1a: plain GETs, no write.
const base = 'http://localhost:3320/api/v1';

async function get(path) {
  const response = await fetch(base + path);
  const body = await response.json();
  return { status: response.status, body };
}

const listed = [];
for (let page = 1; ; page += 1) {
  const { status, body } = await get(`/spaces?limit=50&page=${page}`);
  if (status !== 200) {
    console.log('list status', status, JSON.stringify(body));
    break;
  }
  listed.push(...body.data);
  const meta = body.meta ?? body.pagination ?? {};
  if (page >= (meta.totalPages ?? 1)) {
    console.log('meta', JSON.stringify(meta));
    break;
  }
}
console.log('listed spaces:', listed.length);
for (const space of listed) {
  console.log(JSON.stringify(space));
}
const pins = await get('/map/spaces');
console.log('pins status', pins.status, 'count', pins.body?.data?.pins?.length ?? JSON.stringify(pins.body).slice(0, 200));
for (const space of listed) {
  const one = await get(`/spaces/${space.slug}`);
  console.log('space', space.slug, one.status, JSON.stringify(one.body).slice(0, 1500));
}
const lookups = await get('/lookups');
console.log('lookups', lookups.status, JSON.stringify(lookups.body).slice(0, 1500));
