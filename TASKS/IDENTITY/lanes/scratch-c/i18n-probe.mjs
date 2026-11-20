// Runs the prototype's i18n.js in a stub page (node:vm) for each ?identity= and reports what it sets.
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const source = readFileSync('C:/dev/masaha/app-design-lane-c/docs/design/prototype/masaha/i18n.js', 'utf8');

for (const search of ['', '?identity=slate-berry', '?identity=sea', '?identity=slate-coral', '?identity=bogus', '?lang=en&theme=dark']) {
  for (const dark of [false, true]) {
    const icon = { href: 'masaha/favicon.svg' };
    const root = { dataset: {}, lang: '', dir: '' };
    const context = {
      location: { search },
      URLSearchParams,
      document: { documentElement: root, querySelector: () => icon, addEventListener: () => {} },
      matchMedia: () => ({ matches: dark }),
      window: {},
    };
    vm.runInNewContext(source, context);
    const carry = context.window.carryParams;
    console.log(
      `${(search || '(none)').padEnd(22)} ${dark ? 'dark ' : 'light'}  data-identity=${String(root.dataset.identity).padEnd(11)} icon=${icon.href.padEnd(40)} link=${carry('Directory.html')}  kept=${carry('Directory.html?identity=sea')}`,
    );
  }
}
