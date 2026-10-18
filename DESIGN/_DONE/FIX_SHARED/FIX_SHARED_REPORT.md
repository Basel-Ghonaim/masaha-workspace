# Design fix 1 — report

Worker: the design-fix worker · worktree `C:\Users\basel\masaha-design` · branch `design/shared`
PR [#59](https://github.com/Basel-Ghonaim/masaha/pull/59) · 2026-10-11 · CI green on the pushed head, GitHub shows **CLEAN**

## 1. The head and the commits

Head `ac25093543aadc8a4a814d6d282cb8a5a4ced388` · 8 commits · 44 files, every one inside `docs/design/`
· +926 / −370.

| # | Commit | Decisions |
|---|---|---|
| 1 | `docs(design): group the sidebars and account menu` | P3, P4, SH-005, SH-006, SH-018, DI-2 |
| 2 | `docs(design): one page header in the top bar` | P1 (amended), SH-016 |
| 3 | `docs(design): merge the public state control` | P2, `?publicstate=`, `?override=<n>` |
| 4 | `docs(design): one filter bar and paged lists` | P5 (amended), P6, SH-007 |
| 5 | `docs(design): add the missing states and feedback` | P7, P8 (amended), DI-5 |
| 6 | `docs(design): one rule for confirm and undo` | P9 (amended), P10, SH-021, DI-4, DI-7 |
| 7 | `docs(design): say subscription in English` | SH-019 |
| 8 | `docs(design): the prototype is the living design` | README, CHANGES, DI-6 |

All eighteen **prototype** decisions of batch 1 are applied, with the amendments of 2026-10-10 and
2026-10-11, plus the five folded design issues. `docs/design/CHANGES.md` records each in one line.

## 2. What was run

`docs/design/` is excluded from ESLint and Prettier and no test lane owns it, so three checks were
built for this item and run before every commit.

| Check | Result |
|---|---|
| **Babel parse** — every `.jsx` and every page's inline script, with the vendored Babel | 48/48 blocks across 52 files |
| **Class checker** — every class used, against `_ds_bundle.css` + `masaha.css` | 6 dead utility classes left, all pre-existing; DI-2 fixed the two in the shells |
| **Real run** — every page × 390/768/1440 × ar/en × light/dark | **420 page loads, 0 blank renders, 0 console errors** |
| `npm run format:check` | passes |
| `npm run check:links` | passes, 1852 links |

**Measured outcomes**, not just applied code:
- the phone top bar: **112 px → 61 px** (140 px with an override running);
- seven- and eight-column tables show **five** columns at 768–1023, all of them from 1024;
- the four worst lists really page: payments **312**, audit **240**, users **84**, customers **61**;
- an action's button is `aria-busy` and `disabled` mid-flight, so a second tap cannot land;
- the skip link is the first focusable element of four shells and matches `:focus-visible`.

**Not run:** the test lanes and the build. This item has no product code, so
[workflow §2 phase 4](../../../masaha-design/docs/development/workflow.md#phases)'s exception
applies.

**Reported, not claimed:** `format:check` passes, but `.prettierignore` excludes both `*.md` and
`docs/design/`, so it cannot see this item's changes. It is evidence of nothing here.

## 3. The breaks made

- **`?status=open` → `?publicstate=open`** (approved). The old name was the public-state popover's
  opener *and* a list filter on Customers, Data reports and Admin reports, *and* a link target from
  two overview pages. `INDEX.md` and the board follow it; no reference to the old name is left.
- **`?override=<minutes>` now parses** as Full for that long. It used to feed a state key of `"30"`
  into the lookup and blank the badge, which is why README listed two frames as rendering with an
  error; that line is gone from its *Known limits*.
- **`OwnerShell` and `AdminShell` take `actions` as a list**, not a rendered node. Every caller was
  converted; a page passing the old shape blanks, which is how two were caught (below).
- **Sample data grew** in `desk-data.js` and `admin-data.js`. The pages the other reviews are
  reading now show more rows; the rows themselves are generated, deterministic and fictional.

## 4. Problems met, and how they were solved

1. **Chrome served stale `.jsx` files.** `python -m http.server` sends `Last-Modified`, so after an
   edit the browser mixed old and new scripts — which looked exactly like two real bugs (a
   `SkipLink is not defined` and a duplicate React key). Solved by `Network.setCacheDisabled` in the
   capture driver. Nothing was wrong with the code.
2. **Two pages blanked** after P1 changed the `actions` contract: `Staff.html` and `Payments.html`
   still passed a JSX node. Both were edits whose file write had been rolled back when a later edit
   in the same file failed its match. Caught by the smoke check, fixed, and the edit helper was made
   whitespace-tolerant so the class of failure stopped recurring.
3. **The prebuilt CSS has no `lg:table-cell`.** SH-007's column priority needs it, and
   `_ds_bundle.css` only holds the classes the original prototype used. A layout-only `.lg-col` rule
   went into `masaha.css`, where the archive already keeps such helpers.
4. **`AlertDialogAction` cannot show a pending state** — see §6.
5. **The final verification run crashed once** on a port clash with a Chrome instance I had stopped.
   Re-run on a clean process: 420/420.

## 5. Anything that behaved unexpectedly

- **One flaky blank.** `Admin overview.html` at 390 reported BLANK in a single smoke run and was
  clean on two immediate re-runs and in all 420 matrix loads. The cause was most likely the
  readiness poll timing out under load, not the page. Recorded rather than dismissed.
- **The desk's search takes focus on load** (`autoFocus`), so the first Tab there lands on «زبون
  جديد», not the skip link. The link is still first in the DOM and works from a cold start; the
  autofocus simply puts the user past the chrome already. Not changed — it looks deliberate, and it
  serves SH-018's purpose — but worth knowing.
- **`check:links` found a pre-existing broken link.** Eight `INDEX.md` rows pointed at
  `screens/24-new-customer-membership-sheet/`, while the folder on disk is `…-subscription-sheet`.
  SH-019's rename fixed them by accident; I then re-broke them with an over-eager restore and fixed
  them properly by resolving every screenshot path against disk.
- **`npm ci` was run in this worktree**, against the prompt's "no `npm ci`". The reply's instruction
  to run `npm run check:links` on the head made it necessary; it left `package-lock.json` untouched.

## 6. New design issues

Found while working. None is built.

- **DI-8 — an `AlertDialog`'s action cannot show a pending state** *(level: design system)*.
  `AlertDialogAction` renders `Button` with `asChild`, and `Button` returns early on that branch,
  dropping `loading` and `disabled` (`_ds_bundle.js:15555` and `:15393`). So P8's «it is working»
  reaches every action **except** the ten `AlertDialog` confirmations — delete a space, suspend a
  user, stop a staff member, unlink an owner ×2, end a subscription, archive a customer who owes,
  extend subscriptions, issue a temporary password. Better: `Button` should honour `loading` under
  `asChild`, or `AlertDialogAction` should take it directly. For worker A, beside SH-012.
- **DI-9 — six dead utility classes remain** *(level: prototype)*: `-mt-3` (Customer file),
  `h-28` (profile-b), `hover:opacity-90` (Admin and Owner overview), `md:max-w-32`
  (Announcements), `md:w-44` (Customers, profile-a), `md:w-72` (Finance). They are in the markup
  but in no stylesheet, so they do nothing. DI-2's two in the shells were folded because P1 and P4
  rewrote those lines; these six sit in pages no batch-1 decision touches.
- **DI-10 — the page title and the bar's other controls compete at 390** *(level: pattern)*.
  P1's «⋯» and P2's state control share the one row the decisions ask for, and on the four owner
  pages that have both, 390 px holds them only because the state label was shortened and its
  chevron dropped below 768. A third element in that bar would break it. Better: decide an explicit
  order of precedence for the bar — title, state, actions — rather than discovering the limit page
  by page.
- **DI-11 — `prototype/BRIEF.md` now contradicts the design in two places** *(level: docs)*. It
  describes the public state as a badge plus a «ضبط الحالة» button (P2 merged them) and says
  «membership» in English (SH-019). BRIEF is the record of the brief the screens were designed
  against, so it was deliberately not edited — but a reader will take it for current. Better:
  a one-line header saying it is a 2026-09-29 record, superseded where `CHANGES.md` says so.

## 7. Owner's additions

None. No change was asked for while the work ran.

## 8. Rules in doubt

- **foundation §7 makes `heading-1` the page title**, but both dashboard shells render it at
  `text-heading-3` (17 px) in a sticky bar, where 30 px does not fit — and at 390 the bar is full
  even at 17 px (DI-10). Recorded as approved in the plan, and repeated here so the rule and the
  design are known to disagree.
- **foundation §9's coming change**, «a table of more than five columns becomes cards below `lg`»,
  cannot be built with the vendored `DataTable`, which turns to cards at 768 and has no
  column-priority prop. The prototype shows the decision's other branch. The analyst passes the
  wording note to worker A.

## 9. Early conflict check

`gh pr list --state open` returns only PR #59, so there is nothing to conflict with. The branch is
a direct descendant of `origin/main` (`b66ddfe`); no rebase was needed.

## 10. Departures from the prompt

| Departure | Why |
|---|---|
| `npm ci` was run | The reply replaced the by-hand link check with `npm run check:links`, which needs `node_modules`. |
| P2's phone short form is the state word alone, and the control drops its chevron below 768 | The decision asks for «a short form on a phone, inside the one top-bar row» without fixing its wording. Keeping the countdown *and* P1's «⋯» in that row truncated «مكتب الاستقبال» to five characters. The countdown is at the head of the panel and in the control's `aria-label`. |
| SH-021's note was not added to the map's selected card | That card shows no prices, so the note has nothing to attach to. The three lists that show prices have it. |
| The ten `AlertDialog` confirmations have no pending state | Not buildable with the vendored layer — DI-8. |

## 11. Review focus — what no check exercises

- Screen-reader order and announcements; headings and the tab order were read from the DOM only.
- The tablet rail's `Tooltip`, which touch cannot open; the switcher's `aria-label` carries the name.
- Whether the generated sample rows read as plausible to someone who knows the domain. They are
  consistent (312 payments, 3–300 ₪, sorted, never dated ahead of today, 75 names).
- The boundary of P8's exception: which actions genuinely «show the result in the row they changed».
  No switch or toggle raises a success toast now, and the front desk always does.
- Print, zoom, and `prefers-reduced-motion`.

## 12. Review fixes (2026-10-11)

The owner's review of `ac25093` found two items and the analyst one. **F1, F2 and X1 built**; the
fix list's last two sections are records for later batches and were not touched.

**Method, by the owner's stated override:** one new commit on top of the branch — `bc7f291`,
`docs(design): fix the review's three items` (42 characters) — no fixup, no autosquash, no
force-push. Head now `bc7f2919f406ac01a3f55c38dd78a567771694e2`; CI green, GitHub shows **CLEAN**; one "Review fixes" comment posted.

| Fix | What it was | What was done |
|---|---|---|
| **F1** | A card's save footer touched the last field: 0 px where every other card had 20 | `Card` spaces its own children with `gap-(--card-padding)`, but a `<form>` wrapping the content and the footer swallowed it. The form takes the Card's layout back. 15 cards across `Owner space profile`, `Admin space edit` and `Settings` go 0 → 20 px |
| **F2** | **A regression of this PR.** The Directory drew its filter form inline in the toolbar from 1024 *and* in the sidebar | `FilterSheet`'s `always` flag becomes `wide`: `inline` (the default, eight lists), `sheet` (the Directory's map), `none` (its list view, whose sidebar has them). One copy at every width in both views; the other eight pages unchanged at 768 and 1440 |
| **X1** | `npx serve`, which README recommends, redirected `X.html?…` to `X` and dropped the query | `prototype/serve.json` with `{ "cleanUrls": false }`. Without it the request answers 301 to `/Desk`; with it, 200 with the query intact |

**Verified** (light, as the fix list asks): Babel parse 48/48 blocks · the 35-page smoke at 390 and
1440, 0 problems · `format:check` · `check:links` (1852 links) · the Directory at 390, 768, 1023,
1024 and 1440 in both views, and each F1 page at 390 and 1440. Eight new before/after images.

**Added to §5, unexpected:** the 420-load matrix reported nothing for F2 because it checks for
blank renders and console errors, **not for a layout drawn twice**. A regression that is merely
duplicated, misplaced or oversized passes it. That is the check's limit, now known; catching F2
would have needed either the per-width visual review the owner did, or an assertion that a page
draws its filter form once.
