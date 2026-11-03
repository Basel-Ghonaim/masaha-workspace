p = r'C:\dev\masaha\app-lane-t\docs\architecture\findings\180-a-site-pages-chunk-reaches-the-tables-and-the-calendars-libraries.md'
s = open(p, encoding='utf8').read()
assert s.count('**Status:** Open · **Date:** 2026-10-28') == 1
s = s.replace('**Status:** Open · **Date:** 2026-10-28', '**Status:** Resolved · **Date:** 2026-10-28', 1)
s = s.rstrip('\n') + '\n\n**Resolution (2026-10-29, #PRNUM):** the site draws three capabilities through their `public` entries (`data-reports`, `announcements`, `platform-settings`), lint refusing the site their `index.ts`; `check:build` refuses a site page whose chunk, with its static imports, reaches the table\'s, the calendar\'s or Leaflet\'s chunk ([architecture §3](../../frontend/architecture.md#3-capabilities-features)).\n'
open(p, 'w', encoding='utf8', newline='').write(s)
