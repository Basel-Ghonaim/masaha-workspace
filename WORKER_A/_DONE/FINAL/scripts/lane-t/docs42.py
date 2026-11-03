import os
root = r'C:\dev\masaha\app-lane-t'
def rep(rel, old, new):
    p = os.path.join(root, rel); s = open(p, encoding='utf8').read()
    assert s.count(old) == 1, (rel, old[:60])
    open(p, 'w', encoding='utf8', newline='').write(s.replace(old, new))
rep(r'docs\frontend\architecture.md',
 "what only the dashboard uses besides, such as TanStack Query's `useQuery`, lands in a chunk the dashboard loads beside it ([finding 27](../architecture/findings/27-two-dashboard-chunks-import-each-other.md)). `check:build` reads the build's manifest: the site's first download, its entry and every chunk the entry imports statically, must not reach the dashboard's chunk, nor a chunk made from a dashboard module.",
 "what only the dashboard imports besides (a capability's dashboard parts, `@masaha/shared`'s dashboard schemas, TanStack Query's `useQuery`: each module whose every chain of static importers ends in dashboard code, none loaded lazily) is a second chunk, `dashboard-shared`, that the dashboard loads beside it and that never imports the dashboard's chunk back ([finding 27](../architecture/findings/27-two-dashboard-chunks-import-each-other.md); 2026-10-29, #PRNUM). `check:build` reads the build's manifest: the site's first download, its entry and every chunk the entry imports statically, must not reach either chunk, nor a chunk made from a dashboard module; and no chunk the dashboard's chunk reaches through its static imports may import it back, a cycle that would fail the first page loaded at a module-level use.")
p = os.path.join(root, r'docs\architecture\findings\27-two-dashboard-chunks-import-each-other.md')
s = open(p, encoding='utf8').read()
assert s.count('**Status:** Open · **Date:** 2026-10-05') == 1
s = s.replace('**Status:** Open · **Date:** 2026-10-05', '**Status:** Resolved · **Date:** 2026-10-05', 1)
s = s.rstrip('\n') + "\n\n**Resolution (2026-10-29, #PRNUM):** what only the dashboard imports has a chunk of its own, `dashboard-shared`, which never imports the dashboard's back; `check:build` refuses a chunk the dashboard's chunk reaches that imports it back ([architecture §3](../../frontend/architecture.md#3-capabilities-features)). The build before it had the cycle through two lazy pages' chunks (the space settings' and the announcements' pages), holding `@masaha/shared`'s space-settings schemas and the announcements' dashboard parts.\n"
open(p, 'w', encoding='utf8', newline='').write(s)
