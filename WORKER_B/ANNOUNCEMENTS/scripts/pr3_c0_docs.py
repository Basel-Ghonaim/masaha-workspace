import io, sys
def edit(path, pairs):
    with open(path, encoding='utf-8', newline='') as f: t = f.read()
    for old, new in pairs:
        assert t.count(old) == 1, (path, old[:60], t.count(old))
        t = t.replace(old, new)
    with open(path, 'w', encoding='utf-8', newline='') as f: f.write(t)

edit('docs/features/data-reports.md', [
 ("The owner and the admin at once: the second waits on the space's lock and finds the report decided.",
  "The owner and the admin at once: both wait on the space's lock, and the links are read under it before the report is. An owner's decision while the admin's waits makes the admin's `forbidden` (403) while the owner is still linked, and `REPORT_ALREADY_DECIDED` once the space is unverified again; the admin's decision first makes the owner's `REPORT_ALREADY_DECIDED`."),
 ("an owner linked while the admin's decision waits must win. 2026-10-25, #120. The repository's select leaves the reporter out, so no mapper can leak them. 2026-10-25, #120.",
  "an owner linked while the admin's decision waits must win. 2026-10-25, #120."),
 ("*Why:* a reporter must not fear the space; the admin, who answers for the platform, sees them.",
  "*Why:* a reporter must not fear the space; the admin, who answers for the platform, sees them. The repository's select leaves the reporter out, so no mapper can leak them. 2026-10-25, #120. The owner still sees a report's exact time ([finding 150](../architecture/findings/150-the-owner-sees-a-reports-exact-time.md), accepted)."),
])
edit('docs/api/api-contract.md', [
 ("`conflict` (409) `REPORT_ALREADY_DECIDED`, also when the owner decided it first. Built 2026-10-25, #120.",
  "`conflict` (409) `REPORT_ALREADY_DECIDED`. An owner's decision while this one waits makes it `forbidden` while the owner is still linked, and `REPORT_ALREADY_DECIDED` once the space is unverified again. Built 2026-10-25, #120."),
])
edit('docs/architecture/findings/README.md', [
 ("## Accepted\n\n- [5. In dark",
  "## Accepted\n\n- [5. In dark"),
])
