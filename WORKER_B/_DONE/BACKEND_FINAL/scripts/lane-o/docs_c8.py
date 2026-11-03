import re, sys
ROOT = 'C:/dev/masaha/app-b-lane-o/docs/features/'
TAG = '(2026-10-29, #PRNUM)'
EDITS = {
 'spaces.md': (
  "- **The owner's overview** (`overview`), which reads one space's freshness: its groups missing, and stale with their days " + TAG + ".",
  "**One space's freshness** (`listing.freshnessOf`, for the owner's overview). The space's row, read by the listing's own query, and the thresholds saved now: its groups never saved, and its stale ones, each with its Gaza days from its date to now (`staleness.ts`' `staleDays`, pure: whole days on Gaza's calendar, never 24-hour spans); a soft-deleted space is `not_found` " + TAG + "."),
 'data-reports.md': (
  "- **The owner's overview** (`overview`), which counts the space's open reports " + TAG + ".",
  "**The open count** (`openCountOf`, for the owner's overview): how many of the space's reports are `OPEN`, on the owner's list's own status condition, in one `count`: its `status=OPEN` total " + TAG + "."),
 'visits.md': (
  "- **The owner's overview** (`overview`), which counts the space's unpriced visits " + TAG + ".",
  "**The unpriced count** (`unpricedCount`, for the owner's overview): the unpriced list's total, one `count` on the list's own condition (one `const` for both) " + TAG + "."),
 'subscriptions.md': (
  "- **The owner's overview** (`overview`), which counts the customers whose subscription is ending soon and names the first five " + TAG + ".",
  "**Ending soon** (`endingSoon`, for the owner's overview): the customers whose current subscription is `ENDING_SOON` at the instant asked — the customers list's `status=ENDING_SOON`: the space's subscriptions read once, as `customerIdsBy` reads them, then [`customers`](customers.md)' own page of those ids, archived ones left out, so the count is that list's total — and the first five by end date (one with none last), then by subscription id, each with its customer's name " + TAG + "."),
 'announcements.md': (
  "- **The owner's overview** (`overview`), which reads the running announcements' types, beside the summary's running count " + TAG + ".",
  "**The running types** (`runningTypes`, for the owner's overview): the types of the space's announcements running at the instant asked, not deleted, each once — one `DISTINCT` query on the list's own `RUNNING` condition — in `ANNOUNCEMENT_TYPES`' order " + TAG + "."),
 'occupancy.md': (
  "- **The owner's overview** (`overview`), which reads the space's state at a glance: how many are present, its capacity and its live status, never a name " + TAG + ".",
  "**The glance** (`glance`, for the owner's overview): the state now without anyone's row — the space's row, its open visits and open check-ins counted (`present.countsIn`, one query each), the closures in force and the week, read in parallel with no lock; it answers the capacity, the live status by the same rule and inputs as the state now, and *present* as visits, members and their total; no name and no charge " + TAG + "."),
}
for name, (who, behaviour) in EDITS.items():
    p = ROOT + name
    s = open(p, encoding='utf-8', newline='').read()
    s, n = re.subn(r'(\*\*Last Updated:\*\* )\d{4}-\d{2}-\d{2}', r'\g<1>2026-10-29', s, count=1)
    assert n == 1, name
    # Who uses it: append a bullet at the end of its list.
    i = s.index('\n## Who uses it\n')
    j = s.index('\n## ', i + 5)
    block = s[i:j].rstrip('\n')
    s = s[:i] + block + '\n' + who + '\n' + s[j:]
    # Behaviour: a paragraph at its end, before the next section.
    i = s.index('\n## Behaviour and flows\n')
    j = s.index('\n## ', i + 5)
    block = s[i:j].rstrip('\n')
    s = s[:i] + block + '\n\n' + behaviour + '\n' + s[j:]
    open(p, 'w', encoding='utf-8', newline='').write(s)
    print('ok', name)
