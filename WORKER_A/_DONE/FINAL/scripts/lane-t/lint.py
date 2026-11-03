p = r'C:\dev\masaha\app-lane-t\eslint.config.js'
s = open(p, encoding='utf8').read()
def rep(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new)
rep("""import js from '@eslint/js';
""", """import { existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

import js from '@eslint/js';
""")
rep("""/** The web zones of `types` a zone may import, each only through its entries. */
const zoneEntries = (types) => [
  { element: { type: types, fileInternalPath: 'index.ts' } },
  ...(types.includes('design-system')
    ? [{ element: { type: 'design-system', fileInternalPath: LAYER_ENTRIES } }]
    : []),
];
""", """// The capabilities with a second entry, public.ts, beside their index.ts: what the site draws of
// them, apart from what only the dashboard draws, so a site page's chunk never reaches the
// dashboard's heavy libraries (finding 180, docs/frontend/architecture.md §3). Read from the
// features' folders, so an entry added is held at once.
const FEATURES = `${import.meta.dirname}/apps/web/src/features`;
const PUBLIC_ENTRY_CAPABILITIES = readdirSync(FEATURES).filter((name) =>
  existsSync(join(FEATURES, name, 'public.ts')),
);

/** The web zones of `types` a zone may import, each only through its entries. */
const zoneEntries = (types) => [
  { element: { type: types, fileInternalPath: 'index.ts' } },
  ...(types.includes('feature')
    ? [{ element: { type: 'feature', fileInternalPath: 'public.ts' } }]
    : []),
  ...(types.includes('design-system')
    ? [{ element: { type: 'design-system', fileInternalPath: LAYER_ENTRIES } }]
    : []),
];
""")
rep("""              message:
                'site → {{ to.captured.capability }} is not allowed. The site never imports a dashboard-only capability (docs/frontend/architecture.md §3, apps/web/scripts/dashboardOnly.ts).',
            },
""", """              message:
                'site → {{ to.captured.capability }} is not allowed. The site never imports a dashboard-only capability (docs/frontend/architecture.md §3, apps/web/scripts/dashboardOnly.ts).',
            },
            // A capability with a public entry is the site's through it alone: its index.ts holds
            // what the dashboard draws (finding 180). check:build proves the same of the build.
            {
              from: { element: { type: 'page', captured: { group: 'site' } } },
              disallow: {
                to: {
                  element: {
                    type: 'feature',
                    captured: { capability: PUBLIC_ENTRY_CAPABILITIES },
                    fileInternalPath: 'index.ts',
                  },
                },
              },
              message:
                'site → {{ to.captured.capability }} ({{ to.internalPath }}) is not allowed. The site imports a capability with a public entry through @features/<capability>/public (docs/frontend/architecture.md §3).',
            },
""")
rep("""    // The four zones of apps/web and their one-way dependency rule (docs/frontend/architecture.md §1).
    // Another zone is entered only through its index.ts barrel, the design-system layer also through
    // its data components' entry (LAYER_ENTRIES).""", """    // The four zones of apps/web and their one-way dependency rule (docs/frontend/architecture.md §1).
    // Another zone is entered only through its index.ts barrel, the design-system layer also through
    // its data components' entry (LAYER_ENTRIES), a capability also through its public entry.""")
open(p, 'w', encoding='utf8', newline='').write(s)
