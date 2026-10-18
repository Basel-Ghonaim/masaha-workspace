F-6c1 — review fixes for PR #36 (the ONE list)

Two independent reviews ran against 024fd04: authorization and correctness; conformance and documents. No blockers. Every authorization path was traced and is correct. The owner's analyst verified S1 and S4 in the code. Apply everything below on this branch and PR, each fix with its test. Don't merge.

## Should-fix

S1 — A test gap: nothing checks that each space gets its own area. Every test puts the spaces in one area, so a bug pairing every space with the first area returned would pass.
- Make the composing unit test use two areas, and assert each space's area names.
- Add a second area to the API case, and assert both.
- Order the unit test's links 3, 7 (not the summaries' order), so "in the links' order" is proven there too, not only in the API lane.

S2 — architecture.md §2 says "an unknown space gets a 404 page". That contradicts K4 and the guard. Write: "a `:spaceId` that is not a positive integer gets a 404; a space the user holds no active link to, whether it exists or not, gets a 403." Also, where §2 says "`DashboardLayout`, with the dashboard shells (F-6c)", write F-6c2.

S3 — Give the §3 gap an owner. `features/space-links` is a capability §3's table doesn't list yet, and §3 is PR #35's section. In foundation.md's F-6c2 entry (which this PR already edits), add: "adds `space-links` to architecture.md §3's capability table, and decides whether it is dashboard-only". Don't edit §3 here.

S4 — No production parameter that only tests pass (the owner's rule, testing.md §3 rules 2 and 4). `landingPath(user, search, storage?)`, `lastSpace(…, storage)` and `rememberSpace(…, storage)` take a `storage` that only tests ever pass.
- Remove the parameter.
- The functions use the browser's storage, reached lazily and wrapped in try/catch, as now.
- Tests stub the platform's own seam: `vi.stubGlobal('localStorage', …)`, or a jsdom environment for those files. That stands in for the browser API the way `fakeAdapter` stands in for the transport, and needs no production change.
- Unexport `browserStorage` if it becomes internal.

S5 — `docs/README.md` still says foundation.md has "sixteen Work Items". The F-6c split makes it seventeen.

## Nits (fix all)

N1 — Add an API case: a pending temporary password gets 403 `PASSWORD_CHANGE_REQUIRED` on `GET /manage/spaces`, as the contract states.
N2 — Add a `lastSpace` test where the stored value is garbage (`'abc'`, `'07'`, `' 7'`, another user's id): each falls back to the oldest link.
N3 — Add a `landingPath` test where an explicit `?next=/` wins over the role-based landing. That is why `returnUrlOf` exists. In architecture.md §2, say the landing reads the return URL with `returnUrlOf`, and that an explicit `next=/` wins.
N4 — finding 18 (`docs/architecture/findings.md`): update its evidence.
- `mySpaces` now asks `spaces` and leaves soft-deleted spaces out.
- But the session's links, which feed `RequireSpaceRole` and the landing's oldest-link fallback, still include them. So after F-6c2 a user could land on a space their switcher doesn't list.
- The finding stays Open. Don't change the code.
N5 — Rename the API's internal `SpaceSummary` in `spaces.repository.ts`. shared-package.md R7 uses `SpaceSummary` as its example response name, which invites a clash when `@masaha/shared/spaces` arrives. Use a name such as `SpaceRow` or `SpaceSummaryRow`.
N6 — Record a finding: `signedIn(req)` is now duplicated in `users.controller.ts` and `space-links.controller.ts`. Don't refactor here.
N7 — The commit subject `docs(plans): split f-6c and move account settings out` is 53 characters. Reword it to 50 or fewer (for example `docs(plans): split f-6c, move account settings`).
N8 — The PR body: drop "whoever merges second" for §3 (S3 gives it an owner). Keep the `fakeEndpoints` → `fakeSessionRepository` note: whoever merges second renames it.

## History and reporting (the owner's rules)

- Fold each fix into the commit it corrects (fixup + autosquash; N7 with `--fixup=reword:`). Every commit still passes on its own.
- Push with `--force-with-lease`.
- Report only once CI is green on the new head.
- ONE "Review fixes" comment: the reviewed head `024fd04`, the new head, and each id (S1–S5, N1–N8) with its severity and the commit it folded into.
