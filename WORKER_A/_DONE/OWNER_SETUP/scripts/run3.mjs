// PR 2's real run, part 3: reception opens Packages & prices, the owner's page, and is refused.
import { log, RECEPTION, start, stop } from './common.mjs';

const PATH = '/dashboard/spaces/7/packages';
const { b, d } = await start({ language: 'ar', theme: 'light', width: 1440, who: RECEPTION, path: PATH });

await d.until(`document.querySelector('main')?.innerText.includes('لا تملك صلاحية')`, 'the 403');
log('main:', (await d.text(`document.querySelector('main')`))?.replace(/\n/g, ' / '));
log('sidebar has the page:', await d.evaluate(`[...document.querySelectorAll('nav a')].some((a) => a.textContent.includes('الباقات والأسعار'))`));
await d.shot('ar-light-1440-reception-packages-403');
log('requests:', d.requests.filter((r) => r.includes('/packages')).length, 'to /packages');
stop(b);
