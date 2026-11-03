import re
R = 'C:/dev/masaha/app-b-lane-o/'
TAG = '(2026-10-29, #PRNUM)'
def edit(path, pairs):
    p = R + path
    s = open(p, encoding='utf-8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old[:70], s.count(old))
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)

def feature(name, who, behaviour, extra=()):
    p = R + 'docs/features/' + name
    s = open(p, encoding='utf-8', newline='').read()
    s, n = re.subn(r'(\*\*Last Updated:\*\* )\d{4}-\d{2}-\d{2}', r'\g<1>2026-10-29', s, count=1)
    assert n == 1
    if who:
        i = s.index('\n## Who uses it\n'); j = s.index('\n## ', i + 5)
        s = s[:i] + s[i:j].rstrip('\n') + '\n' + who + '\n' + s[j:]
    i = s.index('\n## Behaviour and flows\n'); j = s.index('\n## ', i + 5)
    s = s[:i] + s[i:j].rstrip('\n') + '\n\n' + behaviour + '\n' + s[j:]
    for old, new in extra:
        assert s.count(old) == 1, (name, old[:60])
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)

edit('docs/api/api-contract.md', [(
 "  - `status`: `verified` or `unverified`, both leaving hidden spaces out; `hidden`, verified or not; or `deleted`, the soft-deleted spaces only, hidden or not, verified or not;",
 "  - `status`: `verified` or `unverified`, both leaving hidden spaces out; `editable`, the unverified spaces, hidden ones included — those whose facts the admin keeps — which with `stale=true` is the admin overview's «اكتمال البيانات» in full (`adminSpacesListQuerySchema`; the list screen does not offer it yet, [finding 158](../architecture/findings/158-the-admins-spaces-list-does-not-offer-the-editable-status.md); 2026-10-29, #PRNUM); `hidden`, verified or not; or `deleted`, the soft-deleted spaces only, hidden or not, verified or not;")])

feature('space-links.md',
 "- **The admin's overview** (`overview`), which counts the spaces by status and reads the first spaces whose facts the admin keeps with a group stale or missing " + TAG + ".",
 "**The admin overview's spaces** (`adminSpaces.counts`, `staleEditable`). The verified spaces' ids read once, then the list's own query (`listingQueryOf`) counted through `spaces`' `listing.count`, four in parallel: `status=verified`, `unverified`, `hidden` and `stale=true`, so each tile is its list's total and a deleted space is never counted. `staleEditable` pages `status=editable&stale=true` — the unverified spaces, hidden ones included, with a group stale or missing — by English name, then id: the first five, each with its missing groups, its stale ones with their Gaza days, and whether it is hidden, and how many there are " + TAG + ".",
 extra=[("- [106](../architecture/findings/106-two-approved-owner-lines-miss-a-case-or-the-label-in-name.md): a re-issue refused for an admin's account says it holds another space.\n",
         "- [106](../architecture/findings/106-two-approved-owner-lines-miss-a-case-or-the-label-in-name.md): a re-issue refused for an admin's account says it holds another space.\n- [158](../architecture/findings/158-the-admins-spaces-list-does-not-offer-the-editable-status.md): the admin's spaces list does not offer the `editable` status.\n")])

feature('data-reports.md', None,
 "**The open counts** (`openCounts`, for the admin's overview): the open reports of the live spaces, in all, those the admin handles (an unverified space's) and those the owners handle (a verified one's), by the verified spaces' ids from [`space-links`](space-links.md) and one condition (`handledByWhere`): three counts in parallel " + TAG + ".",
 extra=[("- **The owner's overview** (`overview`), which counts the space's open reports " + TAG + ".",
         "- **The overviews** (`overview`): the owner's counts the space's open reports, the admin's the platform's, by who handles them " + TAG + ".")])

feature('users.md',
 "- **The admin's overview** (`overview`), which counts the accounts created in the last 30 Gaza days " + TAG + ".",
 "**The new accounts** (`countCreatedSince`, for the admin's overview): how many accounts, of every role, were created at the instant given or after it, one `count` " + TAG + ".")

feature('spaces.md', None,
 "**The listing's count** (`listing.count`, for the admin's overview): how many spaces pass a list query, by the page's own `where` and its \"stale only\" rule, without the page. Each listed row also carries its stale groups' Gaza days " + TAG + ".")
print('ok')
