// PR 2's real run, cleanup: the package the run added stays (no delete), paused; its shift is cleared
// so it holds no shift of the demo space.
import { byText, log, OWNER, start, stop } from './common.mjs';

const PATH = '/dashboard/spaces/7/packages';
const NAME = 'مسائي طلاب';
const row = `[...document.querySelectorAll('li')].find((li) => li.querySelector('span.text-label')?.textContent === ${JSON.stringify(NAME)})`;
const { b, d } = await start({ language: 'ar', theme: 'light', width: 1440, who: OWNER, path: PATH });

await d.until(`!!${row}`, 'the run’s package');
await d.click(byText('li button', '^إزالة الوردية$'), 'clear shift');
await d.until(`!${row}.innerText.includes('ما زالت تحجز')`, 'shift cleared');
log('row:', (await d.text(row))?.replace(/\n/g, ' / '));
log('page errors:', b.errors.length, '· admin requests:', d.requests.filter((r) => r.includes('/admin/')).length);
stop(b);
