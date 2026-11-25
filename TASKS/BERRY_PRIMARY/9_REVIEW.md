# WI-B — the review of PR #158 (head `071e9214`)

**Verdict: after a fix round.** It is a small round: one variant to change, and one look by the owner at how D6 was built.
Everything else holds. CI is green on `071e9214` (run 45621477160), the PR is `CLEAN`, and a test merge with #157's head
`305c5d3f` is clean (tree `2f3f9023`, the same tree the report gives).

Read-only. I read the diff `origin/main...071e9214` (merge base `c3968a74` = `origin/main`), the five commits, the files
at the head, `gh pr view` / `gh pr checks`, and four after-shots. I edited nothing and ran nothing.

## Requirements

**B1 — PASS.**
- Light: `main-action` `spark-600`, foreground `white`, hover `spark-700` (`semantic.css:57-60`).
- Dark: `neutral-50` / `neutral-950`, and the hover is `color-mix(in oklab, n-50, n-950 18%)`. That is the same text as
  `--primary-hover` (`semantic.css:140-144`), written from the primitives and not as `var(--primary)`, as the plan says.
- The dark pin is written by hand: `#f7fbff`, `#0d1217`, `#c7cbd0` (`semantic.unit.test.ts:633-637`). The report's
  measured dark hover is `#c7cbd0` too.

**B2 — PASS** (one nit, N2).
- The label on the fill comes from the `-foreground` rule (`:101-103`) once `ROLES` has the three keys (`:24-26`).
- The label on the hover: `:119`.
- The shape ≥ 3 on `background`, `card` and `popover`, for the fill and the hover: `:149-151`.
- The distance from `destructive` in three visions and both themes, for the fill and the hover: `:563`, at `APART` 0.10
  and `APART_CVD` 0.08 (`:188-189`).
- The report's breaks fail where they should:
  - `s-500`: the label, 4.11;
  - `s-400` as the hover;
  - dark `s-600` with white: 2.80 on card and popover;
  - dark `s-400`: the pin only;
  - `red-600`: the distance.

**B3 — PASS.**
- The only utilities are `@utility bg-main-action` and `bg-main-action-hover` (`tailwind.css:190-196`). Only
  `--color-main-action-foreground` is a theme colour (`:61`).
- Tests hold it: `semantic.unit.test.ts:616-631`.
- A grep of `apps/web/src` finds no `text-`, `border-`, `ring-` or `outline-main-action`.
- No link component, control, Meter, Heatmap, Toast, Badge or `link` variant was touched. `primary` is unchanged.

**B4 — PASS.**
- `defaultVariants` still says `primary`. `Button.component.test.tsx` has the test "stays in the ink unless the main
  action is asked for".
- `AlertDialogAction` callers: `HoursSheet.tsx:161` passes `main`. The other five are `destructive`: DeleteSpace,
  Discard, Leave, PhotoRemove, and the showcase.

**B5 — WEAK.** I walked §4.3 against all 46 `variant="main"` sites and every overlay footer in `features/**`.
- **Matches the plan:**
  - Home «بحث»; About «تصفّح المساحات»; the space page bar's «واتساب»; the forced password change; admin «إضافة مساحة»;
    Add space; the Packages add.
  - The desk's top-bar and action-bar check-in. They show at different widths, and the desk test holds the bar's.
  - The customer file's first state action; the toolbar adds for Customers, Staff, Announcements (header) and Owners
    (`AddOwner`).
  - **Overlays, all present:**
    - the desk: visit, check-out, collect, debt, pay, price, usage-out, edit-customer, correct, subscription, and
      pre-check-in («تسجيل كزيارة», already `autoFocus`, the others outline/ghost);
    - space and admin: announcement, package, AddStaff, AddOwner, link-owner, reissue, issue-password,
      temporary-password, EditSheet, HoursSheet, amenity, lookup, DecideSheet;
    - public: the report dialog;
    - the six filter sheets: directory, customers, ledger, audit, admin reports, and `space-links/admin-list`.
  - **Stay ink, as the plan says:**
    - the desk's «تحصيل» rows, as the owner decided (`DeskPage.component.test.tsx:177-187` asserts `bg-primary`; the
      desk shot agrees);
    - DeskSearch, the map cards, settings cards (`ProfileCard`, `PasswordChangeForm`, `SettingsCard*`), the lookups' add;
    - the empty states that repeat a toolbar: Staff `StaffList.tsx:188`, Customers `CustomersList.tsx:111`,
      Announcements `NewButton` with no `main`.
  - Every overlay left without `main` has a red confirm: Archive, End, Void, WriteOff, Role, Unlink, Deactivate, Suspend,
    Delete, Extension.
  - No main action named by the plan is missing.
- **Two departures:**
  - Packages' empty state draws `main`. See S1.
  - D6 is built differently from the plan's proposal. See S2.
- **No screen has two `main`s at once.** The one exception is an overlay over its page (design issue 2, accepted, D2).

**B6 — PASS.** No file under `features/auth/**`, `pages/site/auth/**`, `shared/routing/guest/**`, `*SignInPrompt*` or
`SpacePage.component.test.tsx` is in the diff. The WhatsApp assertion is in `ContactBar.component.test.tsx`, a new file.

**B7 — PASS** (one nit, N1).
- ADR 0022's line 4 is the approved text word for word, dated 2026-11-25. It is the only change in `d14f7158`, and it has
  the same shape as 0019's *Revised* line.
- Foundation matches the code:
  - §4 (`:126`);
  - §5: Actions `:183-184`, Values `:223-224`, Verified `:248-251`, the dark pin `:251`, the new rule `:257`;
  - §11 (`:390`) and §12 (`:406`).
- The showcase puts `main` first among the variants, and the fixtures have both languages. `primary` became «إجراء
  ممتلئ» / "Filled action", a sensible rename that the report states.
- §5's spark rule (`:256`) now narrows to "the `spark` role" and points to `main-action`.

**B8 — PASS.**
- Five commits, all Conventional, subjects 41–48 characters, each with a body.
- No attribution, no `fixup!`, no `#PRNUM` (git grep finds none at the head).
- The scope per commit is what the plan gives, plus commit 5 for D6: `SpaceDetails` and its test, `SpacePageView`,
  `directory.md`. The report states it.

**B9 — PASS.**
- The report's claims match the PR: 60 files, +361 / −72, labels, `CLEAN`, the CI run, and #157's clean merge tree.
- 46 `main` sites = the "42 + StateActions + header + HoursSheet" of commit 4, plus `SpaceDetails` in commit 5.
- The shots, seen:
  - **desk 1440 light:** berry «تسجيل زيارة» in the top bar; three ink «تحصيل»; the others outline.
  - **desk dialog:** berry «تسجيل الزيارة». The page's berry stays faintly visible under the light scrim (D2).
  - **home 390:** a full-width berry «بحث», and nothing else berry but the logo dots.
  - **space 1440 light:** a full-width berry «واتساب» heads the aside's contacts, and right under it is the list's own
    «واتساب +970599000010» row (S2).
- I did not re-run the local check counts.

## Findings

**Blocker:** none.

**Should-fix**

- **S1 — Packages' empty state draws the main action, against the rule this PR writes.**
  - Where: `PackagesSection.tsx:25-29`, `:82`. One `add` element with `variant="main"` is drawn in the header and also,
    when the list is empty, inside `EmptyState`.
  - The rule in foundation §5 (`:257`) says an empty state has none, and Staff (`StaffList.tsx:188`) keeps its empty
    copy ink in the same case. So an empty Packages page shows a berry button inside an empty state, and an empty
    Staff page does not.
  - **Fix:** keep `main` on the header copy only, for example with `const add = (variant: 'main' | 'primary') => …`,
    `add('main')` at `:40` and `add('primary')` at `:82`. It is one commit, folded into `b284e80a`.

- **S2 — D6 is built as a second WhatsApp, not as the first channel filled, and the report does not list it as a
  departure.**
  - **The plan (§8 issue 1)**, which the owner approved as D6: "make the first contact channel in the side panel a
    `main` Button … the same pattern `PlatformContact` already uses: first channel filled, the others outline."
  - **The build** (`SpaceDetails.tsx:92-99`, `:139-142`, `:160`) adds a separate «واتساب» button above `ContactList`.
    The list keeps its own WhatsApp row, so WhatsApp shows twice, one under the other (shot `space-1440-ar-light`).
    `directory.md` records this shape; the report's §8 does not.
  - **Fix:** the owner looks at the shot and chooses:
    - **(a)** keep it, and add one line to the report's §8 (no code change);
    - **(b)** drop the WhatsApp item from `ContactList` while the lead shows, to match the plan. That changes the
      component and its `directory.md` line.

**Nit**

- **N1** — Foundation §5's rule still opens with the bold "The spark is never … on an action" (`:256`). It points to
  `main-action` with "(below)", not to ADR 0022 as the plan's §5 asked; the link is in the next bullet. Fix: write
  "([ADR 0022](…))" after "a step darker".
- **N2** — The hover's distance from `destructive` has no break of its own. The plan's "closer break", hover `spark-800`
  under protan, passes (0.140). `red-600` broke the fill only. The hover shares the same `it.each`, so the mechanism is
  proven, but no hover value was seen failing it. Fix: none needed; or the report's §4 says plainly that the hover case
  stands on the shared test.
