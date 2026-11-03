p = r'C:\dev\masaha\app-lane-t\apps\web\scripts\checkBuild.unit.test.ts'
s = open(p, encoding='utf8').read()
old = """  it('names a chunk made from a dashboard module when the first download imports it', () => {"""
new = """  it("names the chunk of what only the dashboard imports when the first download imports it", () => {
    const manifest = {
      ...site,
      '_shared.js': { name: 'dashboard-shared', imports: ['_react.js'] },
      '_react.js': { imports: ['_shared.js'] },
    };

    expect(dashboardProblems(manifest)).toEqual([
      "_shared.js is dashboard code in the site's first download.",
    ]);
  });

""" + old
assert s.count(old) == 1
s = s.replace(old, new, 1)
open(p, 'w', encoding='utf8', newline='').write(s)
