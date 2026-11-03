# The owner's notes for the future refactor table

Raw notes from the owner's use of the live site, kept until the refactor table is planned (after the 2026-11-03
presentation). Each one is checked in the code and becomes a finding or a work item then.

- **2026-11-02 — Home's «المتاحة الآن» is empty on the live site.** A space's live status shows only on a verified
  space (an owner linked — v1's rule); the live site's 13 spaces are all unverified, so the section stays empty and
  every card reads "No live status". The owner: an empty section is not sensible. Options to weigh then: a fallback
  for the section (e.g. the spaces open now by their hours, marked unverified), a status by hours for unverified
  spaces, or default hours. Not for tomorrow: the local demo has verified spaces.
- **2026-11-02 — The pagination bar shows with a single page** (the directory, one page of results: «Previous 1
  Next»). It should hide when there is only one page. Check every paged list (the directory and the dashboard's
  tables).
- **2026-11-02 — "many problems" seen while browsing the live site** — the owner will list them for the table.
