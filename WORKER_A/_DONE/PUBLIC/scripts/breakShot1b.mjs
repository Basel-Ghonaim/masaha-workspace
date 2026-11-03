// One 1440 shot of the Directory, for a width break: node breakShot1b.mjs <name>
import { driver, launch } from './cdp1b.mjs';
const b = await launch();
const d = driver(b);
try {
  await d.viewport(1440, 900);
  await d.go('/');
  await d.prefs('ar', 'light');
  await d.go('/spaces');
  await d.until(`document.querySelectorAll('section[aria-labelledby] a[href^="/spaces/"]').length > 0`, 'cards');
  await d.sleep(1500);
  const box = await d.evaluate(`(() => { const a = document.querySelector('aside#directory-filters').getBoundingClientRect(); const r = document.querySelector('section[aria-labelledby]').getBoundingClientRect(); return { sidebar: [Math.round(a.x), Math.round(a.y), Math.round(a.width)], results: [Math.round(r.x), Math.round(r.y), Math.round(r.width)] }; })()`);
  console.log(process.argv[2], JSON.stringify(box));
  await d.shot(process.argv[2], 1700);
} finally {
  b.chrome.kill();
}
