// One screenshot of /spaces at 1440, Arabic light, for a width break: `node breakShot.mjs <name>`.
import { driver, launch } from './cdp.mjs';
const b = await launch();
const d = driver(b);
try {
  await d.viewport(1440, 900);
  await d.go('/');
  await d.prefs('ar', 'light');
  await d.go('/spaces');
  await d.until(`document.querySelectorAll('section[aria-labelledby] a[href^="/spaces/"]').length > 0`, 'cards');
  await d.sleep(1500);
  console.log('columns:', await d.evaluate(`getComputedStyle(document.querySelector('section[aria-labelledby] .grid')).gridTemplateColumns`));
  await d.shot(process.argv[2], 1200);
} finally {
  b.chrome.kill();
}
