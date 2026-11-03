import os
root = 'C:/dev/masaha/app-lane-t/'
def rep(rel, old, new, count=1):
    p = root + rel; s = open(p, encoding='utf8').read()
    assert s.count(old) == 1, (rel, old[:60])
    open(p, 'w', encoding='utf8', newline='').write(s.replace(old, new))
def resolve(rel, date, text):
    p = root + rel; s = open(p, encoding='utf8').read()
    old = '**Status:** Open · **Date:** ' + date
    assert s.count(old) == 1
    s = s.replace(old, '**Status:** Resolved · **Date:** ' + date, 1)
    s = s.rstrip('\n') + '\n\n' + text + '\n'
    open(p, 'w', encoding='utf8', newline='').write(s)
T = 'docs/development/testing.md'
rep(T, '> **Status:** Active · **Last Updated:** 2026-10-17 ·', '> **Status:** Active · **Last Updated:** 2026-10-29 ·')
old = "never after a fixed time.\n"
rep(T, old, old + "8. **A lazy route's first load is paid before the waits.** A web test file that renders lazily loaded routes loads the modules its tests open once, in a `beforeAll` with a 60 s timeout, before any test waits: `warm(...)` in `apps/web/src/test/warmLazy.ts`, with the modules' imports, or with `routeLoaders(routes, path)` where the file may not import the pages (`app/`). On a busy machine a module's first transform can outlast a 3 s wait for what it draws ([findings 55](../architecture/findings/55-a-files-first-wait-for-a-lazy-shell-outlasts-three-seconds-on-a-busy-machine.md) and [87](../architecture/findings/87-the-owners-shell-cold-loads-the-space-links-index.md)); no test's own wait or timeout is raised for it (2026-10-29, #PRNUM).\n")
resolve('docs/architecture/findings/55-a-files-first-wait-for-a-lazy-shell-outlasts-three-seconds-on-a-busy-machine.md', '2026-10-12',
 "**Resolution (2026-10-29, #PRNUM):** each route test file pays its lazy shells' and pages' first transform in a `beforeAll` before its tests wait ([testing §3](../../development/testing.md#3-rules-that-bind-every-test), rule 8). Measured locally: the site shell's first test, 3,814 ms cold before, 369 ms after; the CI run's slowest of these files is recorded in the PR's report.")
resolve('docs/architecture/findings/87-the-owners-shell-cold-loads-the-space-links-index.md', '2026-10-18',
 "**Resolution (2026-10-29, #PRNUM):** the route tests pay the shells' and pages' first load before their waits ([testing §3](../../development/testing.md#3-rules-that-bind-every-test), rule 8), so the 3 s budget is left to the page's own work.")
