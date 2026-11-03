p = r'C:\dev\masaha\app-lane-t\docs\development\setup.md'
s = open(p, encoding='utf8').read()
old = "or if the site's first download, read from the build's manifest, reaches the dashboard's code or a heavy library's chunk, or a library's chunk is missing ([architecture §3]"
new = "or if the site's first download, read from the build's manifest, reaches the dashboard's code or a heavy library's chunk, or a library's chunk is missing, or a site page's chunk reaches a heavy library's through its static imports, or a chunk the dashboard's reaches imports it back ([architecture §3]"
assert s.count(old) == 1
s = s.replace(old, new, 1)
s = s.replace("> **Status:** Active · **Last Updated:** 2026-10-21 ·", "> **Status:** Active · **Last Updated:** 2026-10-29 ·", 1)
open(p, 'w', encoding='utf8', newline='').write(s)
