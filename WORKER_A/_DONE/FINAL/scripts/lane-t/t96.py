import os
web = r'C:\dev\masaha\app-lane-t\apps\web\scripts'
def rd(n): return open(os.path.join(web, n), encoding='utf8').read()
def wr(n, s): open(os.path.join(web, n), 'w', encoding='utf8', newline='').write(s)

s = rd('checkBuild.unit.test.ts')
s = s.replace("import {\n  dashboardProblems,\n", "import {\n  dashboardCycleProblems,\n  dashboardProblems,\n", 1)
s += r'''
describe('dashboardCycleProblems', () => {
  const build: Record<string, ManifestChunk> = {
    'index.html': { isEntry: true, imports: ['_react.js'] },
    '_react.js': {},
    '_dashboard-shared.js': { name: 'dashboard-shared', imports: ['_react.js'] },
    '_dashboard.js': {
      name: 'dashboard',
      imports: ['_react.js', '_dashboard-shared.js', 'index.html'],
    },
    'src/pages/dashboard/shell/SpaceLayout.tsx': {
      src: 'src/pages/dashboard/shell/SpaceLayout.tsx',
      isDynamicEntry: true,
      imports: ['_react.js', '_dashboard.js'],
    },
  };

  it('finds nothing when what the dashboard imports never imports it back', () => {
    expect(dashboardCycleProblems(build)).toEqual([]);
  });

  it('refuses a chunk the dashboard imports that imports it back', () => {
    const manifest = {
      ...build,
      '_dashboard.js': {
        name: 'dashboard',
        imports: ['_react.js', 'src/pages/dashboard/shell/SpaceLayout.tsx'],
      },
    };

    expect(dashboardCycleProblems(manifest)).toEqual([
      'src/pages/dashboard/shell/SpaceLayout.tsx imports the dashboard chunk (_dashboard.js), which imports it.',
    ]);
  });

  it('refuses a cycle closed deeper down', () => {
    const manifest = {
      ...build,
      '_dashboard-shared.js': { name: 'dashboard-shared', imports: ['_react.js'] },
      '_react.js': { imports: ['_dashboard.js'] },
    };

    expect(dashboardCycleProblems(manifest)).toEqual([
      '_react.js imports the dashboard chunk (_dashboard.js), which imports it.',
    ]);
  });
});
'''
wr('checkBuild.unit.test.ts', s)

c = rd('checkBuild.ts')
anchor = "/**\n * What is wrong with the heavy libraries' place in the build"
assert c.count(anchor) == 1
c = c.replace(anchor, """export function dashboardCycleProblems(_manifest: Record<string, ManifestChunk>): string[] {
  return [];
}

""" + anchor, 1)
wr('checkBuild.ts', c)

t = rd('dashboardOnly.unit.test.ts')
t = t.replace("import { isDashboardModule } from './dashboardOnly';", "import { isDashboardModule, isDashboardShared, type ModuleGraph } from './dashboardOnly';", 1)
t += r'''
describe('isDashboardShared', () => {
  const PAGE = '/repo/apps/web/src/pages/dashboard/space/SettingsPage.tsx';
  const SITE = '/repo/apps/web/src/pages/site/public/space/SpacePage.tsx';
  const SCHEMA = '/repo/packages/shared/src/space-settings/settings.ts';
  const RULE = '/repo/packages/shared/src/space-settings/reminder.ts';
  const CORE = '/repo/packages/shared/src/core/index.ts';
  const PICKER = '/repo/apps/web/src/shared/map/components/LeafletPointPicker.tsx';
  const LEAFLET = '/repo/node_modules/react-leaflet/lib/index.js';

  // The graph by each module's static and dynamic importers.
  const graph = (importers: Record<string, string[]>, dynamic: Record<string, string[]> = {}) => {
    const of: ModuleGraph = (id) =>
      id in importers || id in dynamic
        ? { importers: importers[id] ?? [], dynamicImporters: dynamic[id] ?? [] }
        : null;
    return of;
  };

  it('takes a module only dashboard code imports, directly or through such modules', () => {
    const of = graph({ [SCHEMA]: [PAGE], [RULE]: [SCHEMA], [PAGE]: [] });
    const known = new Map<string, boolean>();

    expect(isDashboardShared(SCHEMA, of, known)).toBe(true);
    expect(isDashboardShared(RULE, of, known)).toBe(true);
  });

  it('leaves a module the site also imports, and what it imports', () => {
    const of = graph({ [SCHEMA]: [PAGE, SITE], [RULE]: [SCHEMA], [PAGE]: [], [SITE]: [] });

    expect(isDashboardShared(SCHEMA, of, new Map())).toBe(false);
    expect(isDashboardShared(RULE, of, new Map())).toBe(false);
  });

  it('leaves dashboard code itself to the dashboard chunk', () => {
    expect(isDashboardShared(PAGE, graph({ [PAGE]: [] }), new Map())).toBe(false);
  });

  it('leaves a module loaded lazily, and what only it imports, so it stays lazy', () => {
    const of = graph({ [PICKER]: [], [LEAFLET]: [PICKER] }, { [PICKER]: [PAGE] });

    expect(isDashboardShared(PICKER, of, new Map())).toBe(false);
    expect(isDashboardShared(LEAFLET, of, new Map())).toBe(false);
  });

  it('holds a cycle of such modules that only dashboard code enters', () => {
    const of = graph({ [SCHEMA]: [PAGE, RULE], [RULE]: [SCHEMA], [PAGE]: [] });

    expect(isDashboardShared(RULE, of, new Map())).toBe(true);
  });

  it('leaves a module with no importer, or none known', () => {
    expect(isDashboardShared(CORE, graph({ [CORE]: [] }), new Map())).toBe(false);
    expect(isDashboardShared(CORE, graph({}), new Map())).toBe(false);
  });
});
'''
wr('dashboardOnly.unit.test.ts', t)

d = rd('dashboardOnly.ts')
d += """
export type ModuleGraph = (
  id: string,
) => { importers: readonly string[]; dynamicImporters: readonly string[] } | null;

export function isDashboardShared(
  _id: string,
  _graph: ModuleGraph,
  _known: Map<string, boolean>,
): boolean {
  return false;
}
"""
wr('dashboardOnly.ts', d)
