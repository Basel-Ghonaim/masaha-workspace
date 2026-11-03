import os
root = r'C:\dev\masaha\app-lane-t'
def rep(rel, old, new):
    p = os.path.join(root, rel); s = open(p, encoding='utf8').read()
    assert s.count(old) == 1, (rel, old[:60])
    open(p, 'w', encoding='utf8', newline='').write(s.replace(old, new))
A = r'docs\frontend\architecture.md'
rep(A, "and the dashboard-only rule (§3) are enforced by lint, and the dashboard-only rule by `check:build` too;",
       "and the dashboard-only rule and a capability's public entry (§3) are enforced by lint, and both by `check:build` too;")
rep(A, "· **Last Updated:** 2026-10-28  · **Owner:**", "· **Last Updated:** 2026-10-29  · **Owner:**")
rep(A, "The design system's entries are [foundation §3](design-system/foundation.md#3-architecture)'s: its barrel, and the entry of its data components.",
       "The design system's entries are [foundation §3](design-system/foundation.md#3-architecture)'s: its barrel, and the entry of its data components. A capability the site draws may have a second entry, `public.ts` (§3).")
rep(A, "and the module's `index.ts` stays its only entry.",
       "and the module's `index.ts` stays its only entry (a capability's `public.ts` aside, §3).")
old = "It also refuses Leaflet's stylesheet in the first download (§6).\n"
rep(A, old, old + """
**A capability's public entry** ([finding 180](../architecture/findings/180-a-site-pages-chunk-reaches-the-tables-and-the-calendars-libraries.md); 2026-10-29, #PRNUM): a capability both groups draw may export what the site draws from a second entry, `public.ts`, beside its `index.ts`, which keeps what only the dashboard draws, so a site page never loads the dashboard's screens of it: `data-reports` (`ReportAction`, `MyReportsList`), `announcements` (`ClosureNotice`, `SpaceAnnouncements`) and `platform-settings` (`PlatformContact`). The site imports such a capability through `@features/<capability>/public` alone. Two checks hold it:
- **lint** allows the entry beside the index, as it allows the layer's entries, and refuses the site the index of a capability that has one (read from the features' folders);
- **`check:build`** refuses a site page, any chunk made from a module of `pages/site` (its pages, shells and layouts), whose chunk with its static imports, deeply, reaches a heavy library's chunk (`data-table`, `leaflet`, `calendar`). The map loads Leaflet lazily (§6), so the pages that draw one pass.
""")
rep(r'docs\features\data-reports.md',
    "entry `index.ts` (`SpaceReportsList`, `AdminReportsList`, `AdminSpaceFilterSlot`, `MyReportsList`, `ReportAction`), read by",
    "entries `index.ts` (`SpaceReportsList`, `AdminReportsList`, `AdminSpaceFilterSlot`, the counts' hooks) and `public.ts`, the site's (`MyReportsList`, `ReportAction`; [architecture §3](../frontend/architecture.md#3-capabilities-features)), read by")
rep(r'docs\features\announcements.md',
    "entry `index.ts` (`AnnouncementsList`, `ClosureNotice`, `SpaceAnnouncements`), read by",
    "entries `index.ts` (`AnnouncementsList`) and `public.ts`, the site's (`ClosureNotice`, `SpaceAnnouncements`; [architecture §3](../frontend/architecture.md#3-capabilities-features)), read by")
