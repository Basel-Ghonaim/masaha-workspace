p = r'C:\dev\masaha\app-lane-t\apps\web\scripts\checkBuild.unit.test.ts'
s = open(p, encoding='utf8').read()
s = s.replace("  showcaseOnly,\n  stringsIn,\n", "  showcaseOnly,\n  sitePageProblems,\n  stringsIn,\n", 1)
s += r'''
describe('sitePageProblems', () => {
  const site: Record<string, ManifestChunk> = {
    'index.html': { isEntry: true, imports: ['_react.js'] },
    '_react.js': {},
    '_table.js': { name: 'data-table', imports: ['_react.js'] },
    '_calendar.js': { name: 'calendar', imports: ['_react.js'] },
    '_reports.js': { imports: ['_react.js'] },
    'src/pages/site/public/space/SpacePage.tsx': {
      src: 'src/pages/site/public/space/SpacePage.tsx',
      isDynamicEntry: true,
      imports: ['_react.js', '_reports.js'],
      dynamicImports: ['_table.js'],
    },
    'src/pages/dashboard/space/reports/DataReportsPage.tsx': {
      src: 'src/pages/dashboard/space/reports/DataReportsPage.tsx',
      isDynamicEntry: true,
      imports: ['_react.js', '_table.js', '_calendar.js'],
    },
  };

  it("finds nothing when a site page reaches a library only lazily, and the dashboard's do", () => {
    expect(sitePageProblems(site, ['data-table', 'calendar'])).toEqual([]);
  });

  it("names a site page that reaches a library's chunk through its static imports", () => {
    const manifest = { ...site, '_reports.js': { imports: ['_react.js', '_table.js'] } };

    expect(sitePageProblems(manifest, ['data-table', 'calendar'])).toEqual([
      "src/pages/site/public/space/SpacePage.tsx reaches data-table's chunk (_table.js).",
    ]);
  });

  it('names each library a site page reaches, deeply', () => {
    const manifest = {
      ...site,
      '_reports.js': { imports: ['_react.js', '_table.js'] },
      '_react.js': { imports: ['_calendar.js'] },
    };

    expect(sitePageProblems(manifest, ['data-table', 'calendar']).sort()).toEqual([
      "src/pages/site/public/space/SpacePage.tsx reaches calendar's chunk (_calendar.js).",
      "src/pages/site/public/space/SpacePage.tsx reaches data-table's chunk (_table.js).",
    ]);
  });
});
'''
open(p, 'w', encoding='utf8', newline='').write(s)
