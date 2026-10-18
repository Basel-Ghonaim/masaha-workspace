# ADMINLIST — final report (worker A)

**Work item:** the admin's deleted-spaces list and its restore path (`feat/admin-deleted-spaces`).
**PR:** [#84](https://github.com/Basel-Ghonaim/masaha/pull/84) — `feat(space-links): show deleted space facts`.
**Head:** `60b2236c933cb03b0a92183980af94dabfb7fccb` (`60b2236c`), rebased on `origin/main` `72ceb047`.
**Merge state:** `MERGEABLE` · **`mergeStateStatus: CLEAN`** · **all 10 CI checks pass on that head.**
**Not merged** — merging is the owner's.

## 1. Commits

| Commit | Subject | Chars |
|---|---|---:|
| `0c062c7f` | `feat(space-links): show deleted space facts` | 42 |
| `60b2236c` | `feat(spaces): restore deleted space rows` | 40 |

Two commits, as the owner amended the plan (the docs commit folded into the two code commits, each
carrying the document lines it makes true).

## 2. What was built

- **Commit 1 — the list.** `LIST_STATUSES` is the contract's four statuses; `?status=deleted` is read
  by the contract's own rule, so it reaches `GET /admin/spaces` and survives the filters' and pages'
  links. A row's state is badges, one per fact — verification always, «مخفية» when hidden, «محذوفة»
  when deleted — decided once in `rowView`, so the table and the card cannot disagree. A deleted row
  is muted: its name is text that leads nowhere, its date is worded by the list's own short date on
  Gaza's calendar. Missing fact groups are `warning`. Stale-or-missing is a `ToggleGroup` chip beside
  the count (the count moved to the toolbar with it), not a switch field.
- **Commit 2 — the restore.** `SpaceRef` carries `deletedAt`; `useSpaceActionsMenu` returns a deleted
  branch whose only action is **Restore**, rendered as a button named after the space, busy while it
  works, `aria-disabled` while it waits, keeping the focus. It reuses `useRestoreSpace` — the Undo's
  mutation — so the endpoint, the admin-scope refresh, the 429 hold and the named toasts are one code
  path. Findings **44** and **50** are resolved in their own files and in the index.

## 3. Evidence

### 3.1 Automated lanes (run locally on the head, once each)

| Lane | Result |
|---|---|
| `npm run lint` | pass |
| `npm run typecheck` | pass |
| `npm run test:unit` | pass — 129 files, **1721 tests** |
| `npm run test:component` | pass — 142 files, **944 tests** |
| `npm run build` | pass |
| `npm run check:build` | pass — "No showcase code in 37 build files" |
| `npm run check:classes` | pass — 794 files |
| `npm run check:links` | pass — 2069 links, 155 documents, 1151 source files |
| `npm run format:check` | pass |

Not run locally, and why: **`npm run test:api`** — no API or shared code changed; CI ran it anyway
and it passed.

`check:build` caveat, reproduced on clean `origin/main`: on this Windows machine `vite build` emits a
**development** build unless `NODE_ENV=production` is set, and `check:build` then fails with 1014
showcase strings. With `NODE_ENV=production` it passes. CI runs it on Linux and passes. Not a defect
of this branch; recorded because it is the one command whose local result depended on the shell.

### 3.2 CI on the pushed head `60b2236c`

`format:check` · `lint` · `typecheck` · `test:unit` · `test:component` · `check:classes` ·
`check:links` · `build` (+ its `check:build` step) · `test:api` — **all pass**.

### 3.3 Real browser run (two rounds, seeded API + web, seeded admin)

Screenshots: **`C:\Users\basel\Downloads\adminlist-shots\`**, 23 files (`01-`…`16-` Round 1,
`17-`…`23-` Round 2). Reports: `…\MASAHA_WORKER_A\REPORT\ADMINLIST_BROWSER_REPORT.md` and
`…\ADMINLIST_BROWSER_ROUND2_REPORT.md`.

Proven on screen: the fourth status is offered and sent
(`GET /api/v1/admin/spaces?status=deleted&page=1`) and survives reload; a deleted row is muted,
non-linked, shows the verification badge with «محذوفة» beside it, names its owners, dates itself
«حُذفت في …» (compared against the server's `deletedAt` for a row deleted that day and one deleted
earlier — equal in both locales), and offers **Restore** alone; Restore is busy while it works, focus
retained, the admin scope refetched, then a toast naming the space («استُرجعت …»), with the focus
moving to the list region when the row disappears (not `body`); a forced 409 shows «تعذّر استرجاع …»
with «رقم المرجع: ⁨r2-fake-0001⁩» and leaves the row in place; the place filter still applies while
`status=deleted` (`?status=deleted&governorate=1` → `?status=deleted&governorateId=1&page=1`);
RTL/LTR × light/dark × phone/desktop checked.

Not exercised in the browser: the **429 wait above the list**. It is recorded only by a row *write's*
429, which neither round produced. The component lane covers it:
`SpaceActionsMenu.component.test.tsx` › "waits its button while a 429 counts down". Round 1's report
calls this I2 and marks it *Fail*; the evidence shows the failure was on a list **read**
(`429 GET /api/v1/admin/spaces`, plus `429 POST /api/v1/auth/refresh`), where the documented behaviour
is the list's own failure state with a retry that waits — so that finding is **not a defect of this
change** and should not travel into the review as one.

## 4. The breaks each test catches (seen failing first)

- `filtersOf.unit.test.ts` — `?status=deleted` read, serialized and requested; break: the deleted
  list could show or be sent under the wrong status, or silently fall back.
- `rowView.unit.test.ts` — the state badges apart, the deleted date in both languages, missing =
  `warning`; break: the two facts collapse again, the deletion metadata is lost, or A8 regresses.
- `AdminSpacesList.component.test.tsx` — five status choices; a deleted row's cells (muted name,
  owners, date, restore-only); the chip by the count and no switch; the phone card; break: filter
  wiring, table/card rendering, deletion metadata, action seam, or A7 as a field.
- `useAdminSpacesList.component.test.tsx` — the four statuses, the stale chip's view, `count`, and the
  deleted request with the rows kept busy; break: hook wiring disagreeing with the toolbar.
- `SpaceActionsMenu.component.test.tsx` — restore-only for a deleted row, pending + focus, the
  success toast after the refresh, the named failure with its reference, the 429 hold, accessibility;
  break: a deleted row could still edit, hide or delete, or restore bypasses the mutation.

Red evidence: 10 unit failures before `filtersOf`/`rowView`/`copy` were changed; 11 component failures
with the seven component files stashed; 4 menu failures before the restore branch existed.

## 5. Conflicts

- **At push:** PR #84 opened `CONFLICTING` — `origin/main` had moved two commits (worker B's MANAGE
  item, PR #83). Rebased onto `72ceb047` and resolved **keeping both sides**:
  `docs/features/spaces.md` (Authority header: B's managed routes and "owner/reception web screen
  planned" kept, my web sentences and the later date kept) and `docs/project/overview.md` (the Spaces
  Built line merged so every fact from both sides survives). `docs/features/space-links.md` merged
  cleanly. After the rebase: `format:check`, `check:links`, `typecheck` and `lint` pass, then one
  `--force-with-lease` push.
- **Early check against other open PRs** (plan §12.9): at report time **#84 is the only open PR**, so
  there is nothing to collide with. `git merge-tree --write-tree 60b2236c origin/main` → tree
  `cedaf528`, exit 0.

## 6. Teardown and environment

- API (3320) and web (5320) were started by this implementation session for the verification run and
  are **stopped**; `Test-NetConnection` returns `False` for both. Round 2 deliberately left them
  running because it had not started them; this session stopped them after Round 2 finished.
- Docker Desktop was started for the run (PostgreSQL on 5433, `masaha_dev`) and is still running.
- Test data residue, and what was done about it: Round 2's throwaways `R2 Owner Desk` (42) and
  `R2 Keyboard Desk` (43) are soft-deleted, and owner 17 was unlinked from 42 first, so no leftover
  account is left holding only a deleted space. Round 1's `Verify Delete Desk` (40) and
  `Verify Hidden Desk` (41) remain as Round 1 left them; the pre-existing spaces were not edited.
- The repository is clean: `git status --short` empty at `60b2236c`.

## 7. Departures from the plan, and why

1. **`restore` / `restoreNamed` live in `spaces.menu`,** not `spaceLinks.adminList` as the plan's copy
   table said: they are rendered by `SpaceActionsMenu`, whose other labels live there, and a `spaces`
   component must not read another capability's catalogue namespace. The plan allows the catalogue to
   follow its current organization. Two extra files: `shared/copy/{english,arabic}/spaces.ts`.
2. **Three files outside the plan's list,** all forced by the change: `SpaceNameText.tsx` (a deleted
   name's muted, non-link form), `DeleteSpaceDialog.tsx` (one type import, for the menu's union), and
   the two `spaces` catalogues above.
3. **The result count moved from the table footer to the toolbar,** beside the stale chip, because A7
   puts the chip "by the count" and the design's P5 puts the count "up beside the toolbar".
4. **A deleted row keeps its freshness badges** (`غير مُدخلة: …` on a warning badge) where the
   prototype drew a dash. The plan's list of a deleted row's facts does not remove them and the facts
   are the server's; the browser shows what that looks like, and it is the one point where the screen
   is noisier than the prototype. **The owner may want to decide otherwise** — a dash, or freshness
   dropped, for a space that is gone rather than incomplete.
5. **PR title** is the plan's §12.7 title (commit 1's subject), not workflow §3's "same as the main
   commit"; the plan was explicit and approved.
6. The verification was split across three sessions (implementation, Round 1 browser, Round 2 browser)
   because of session time limits.

## 8. Anything that behaved unexpectedly

- **Round 2's C4 evidence contradicts its own text.** Its report claims the target row showed
  *Verified + Hidden + Deleted*; the row it names shows **two** badges (verified + deleted) because
  that space was never hidden — `is_hidden = false` in the database. The three-badge combination **is**
  visible in the same screenshot, on a different (pre-existing hidden) deleted row, and the unit and
  component lanes assert it deterministically. The API now reports that pre-existing row as
  `isVerified: false` while the screenshot shows it verified: unexplained in the development
  database, **not** a rendering defect (the row view prints what the server sends). Recorded, not
  chased further.
- Round 2's report also says the pre-existing deleted spaces were "left untouched" and that both
  throwaways were deleted; the database shows pre-existing space 37 restored and space 42 left live.
  I cleaned 42 up (unlink, then soft delete) and record 37's restore here.
- A Vite `404` for one local resource appears on page load in both rounds, unidentified; no visible
  effect and no claim made about it.
- Worth the owner's eye: `Verify Hidden Desk` (41) rendered as **verified with no owner link** at
  capture time. If it reproduces on a fresh database it is an API finding, not a screen one.

## 9. What remains for the owner

Review and merge #84. Merging is deliberately not done.