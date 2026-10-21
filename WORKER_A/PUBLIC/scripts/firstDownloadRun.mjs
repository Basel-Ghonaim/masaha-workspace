// The site's first download on the production build (vite preview, 5321): every request the browser
// makes on opening /spaces, before any other page. Reads only.
import { writeFileSync } from 'node:fs';
import { driver, launch, SHOTS } from './cdp.mjs';

const BASE = 'http://localhost:5321';
const b = await launch();
const d = driver(b);
const requests = [];
await b.send('Network.enable');
b.on((m) => {
  if (m.method === 'Network.requestWillBeSent') requests.push(m.params.request.url.replace(BASE, ''));
});
try {
  await d.viewport(1440, 1000);
  await b.send('Page.navigate', { url: `${BASE}/spaces` });
  await d.until(`document.querySelectorAll('section[aria-labelledby] a[href^="/spaces/"]').length > 0`, 'cards', 20000);
  await d.sleep(1500);
  const scripts = requests.filter((url) => /\.(js|css)(\?|$)/.test(url));
  writeFileSync(`${SHOTS}/1a-first-download-log.txt`, requests.join('\n') + '\n');
  console.log('requests:', requests.length, 'scripts and styles:', scripts.length);
  for (const url of scripts) console.log('  ', url);
  for (const word of ['leaflet', 'dashboard', 'data-table', 'Leaflet']) {
    console.log(`${word}:`, scripts.some((url) => url.includes(word)));
  }
  await d.shot('1a-first-download-preview-ar-light-1440');
} finally {
  b.chrome.kill();
}
