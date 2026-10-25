// Probe: does opening and activating a second tab hide the first in headless Chrome?
import { driver, launch } from './cdp4.mjs';

const b = await launch();
const d = driver(b);
try {
  await d.go('/');
  console.log('first tab:', await d.evaluate('document.visibilityState'));
  await d.evaluate(`window.__events = []; document.addEventListener('visibilitychange', () => window.__events.push(document.visibilityState)); true`);
  const { targetId } = await b.send('Target.createTarget', { url: 'about:blank' });
  await d.sleep(800);
  console.log('after a second tab:', await d.evaluate('document.visibilityState'), await d.evaluate('JSON.stringify(window.__events)'));
  const targets = await b.send('Target.getTargets');
  const first = targets.targetInfos.find((t) => t.type === 'page' && t.targetId !== targetId);
  await b.send('Target.activateTarget', { targetId: first.targetId });
  await d.sleep(800);
  console.log('after activating the first again:', await d.evaluate('document.visibilityState'), await d.evaluate('JSON.stringify(window.__events)'));
} catch (error) {
  console.log('FAILED', error.message);
} finally {
  b.chrome.kill();
}
