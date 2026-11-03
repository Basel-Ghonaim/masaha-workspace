def edit(p, pairs):
    s = open(p, encoding='utf8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)
R = r'C:\dev\masaha\app-lane-a1'
edit(R + r'\packages\shared\src\space-links\requests.unit.test.ts', [
("takes editable and the five others", "takes editable and the four others"),
])
edit(R + r'\packages\shared\src\space-links\requests.ts', [
("""/**
 * The admin's list's status filter: whether an owner has joined, of the spaces shown; hidden; or
 * soft-deleted, the only status that lists them.
 */
export const SPACE_STATUSES = ['verified', 'unverified', 'hidden', 'deleted'] as const;""",
"""/**
 * The admin's list's status filter: whether an owner has joined, of the spaces shown; hidden;
 * soft-deleted, the only status that lists them; or `editable`, the spaces the admin keeps the
 * facts of — unverified, hidden ones included — which with `stale=true` is the admin overview's
 * «اكتمال البيانات» in full (its «عرض الكل»). One list, the server's and the screen's (finding 158).
 */
export const SPACE_STATUSES = ['verified', 'unverified', 'hidden', 'deleted', 'editable'] as const;"""),
("""/**
 * `?q=&status=&governorateId=&areaId=&stale=&page=&limit=`. `q` searches the names in both
 * languages; `verified` and `unverified` leave hidden spaces out; `deleted` lists the soft-deleted
 * spaces, which every other status leaves out; `stale=true` keeps the spaces with a stale fact group.
 */""", """/**
 * `?q=&status=&governorateId=&areaId=&stale=&page=&limit=`. `q` searches the names in both
 * languages; `verified` and `unverified` leave hidden spaces out; `deleted` lists the soft-deleted
 * spaces, which every other status leaves out; `editable` keeps the unverified ones, hidden or not;
 * `stale=true` keeps the spaces with a stale fact group.
 */"""),
("""/**
 * The statuses the server reads besides the list's choices: `editable`, the spaces the admin keeps
 * the facts of — unverified, hidden ones included — which with `stale=true` is the admin overview's
 * «اكتمال البيانات» in full (its «عرض الكل»). The list screen does not offer it yet.
 */
export const ADMIN_SPACES_STATUSES = [...SPACE_STATUSES, 'editable'] as const;

/** `adminSpacesQuerySchema` as `GET /admin/spaces` reads it: any of `ADMIN_SPACES_STATUSES`. */
export const adminSpacesListQuerySchema = adminSpacesQuerySchema.extend({
  status: z.enum(ADMIN_SPACES_STATUSES).optional(),
});

export type AdminSpacesListQuery = z.infer<typeof adminSpacesListQuerySchema>;

""", ""),
])
A = R + r'\apps\api\src\modules\space-links'
edit(A + r'\space-links.admin.routes.ts', [
("  adminSpacesListQuerySchema,\n", "  adminSpacesQuerySchema,\n"),
("validate(adminSpacesListQuerySchema, 'query')", "validate(adminSpacesQuerySchema, 'query')"),
])
for f in [r'\admin-spaces\adminSpaces.controller.ts', r'\admin-spaces\adminSpaces.service.ts', r'\admin-spaces\listingQuery.ts']:
    p = A + f
    s = open(p, encoding='utf8').read()
    assert 'AdminSpacesListQuery' in s
    s = s.replace('AdminSpacesListQuery', 'AdminSpacesQuery')
    open(p, 'w', encoding='utf8', newline='').write(s)
# the web: the list keeps offering its four choices until its own commit words `editable` (D6.4)
edit(R + r'\apps\web\src\features\space-links\services\filtersOf.ts', [
("""/**
 * The statuses this list offers, the contract's own: the soft-deleted spaces, which `status=deleted`
 * lists alone, are a choice of it like any other.
 */
export const LIST_STATUSES = SPACE_STATUSES;""", """/**
 * The statuses this list offers, the contract's own: the soft-deleted spaces, which `status=deleted`
 * lists alone, are a choice of it like any other. `editable` is read from the address, as the
 * server reads it, but not yet offered: its words come with the list's own change (D6.4).
 */
export const LIST_STATUSES = SPACE_STATUSES.filter(
  (status): status is Exclude<SpaceStatus, 'editable'> => status !== 'editable',
);"""),
])
