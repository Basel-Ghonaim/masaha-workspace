# WI-B — the berry on the main action: the report

> Plan: `6_PLAN.md`, approved by the owner on 2026-11-25: D1–D7 as recommended, the desk's «تحصيل» rows kept as
> filled ink, and the WhatsApp assertion in `ContactBar`'s own test. **Not merged.**

## 1. The pull request

**[#158](https://github.com/Basel-Ghonaim/masaha/pull/158)**, `feat/berry-main-action` → `main`.

| | |
|---|---|
| Head | `071e9214fb15438e20fa9103e148a50559cb89cd` |
| CI | Green on that head (run 45621477160) |
| Merge state | `CLEAN` |
| Labels | `feat`, `area:design-system`, `area:web`, `area:docs` |
| Assignee | the owner |

60 files, +361 / −72. That is past the workflow's review threshold of about 25. The PR touches no security code,
transaction, schema, dependency or CI.

## 2. The commits

On `origin/main` = `c3968a74`:

1. `d14f7158` — `docs(adr): keep dark main action in the ink`: ADR 0022's *Revised* line, word for word, dated 2026-11-25.
2. `49efa9bb` — `feat(design-system): add the main action role`:
   - `main-action`, `-foreground` and `-hover` in both themes;
   - the fill-only utilities;
   - the token tests;
   - foundation §4, §5 and §11.
3. `44bf4687` — `feat(design-system): add Button's main variant`:
   - `Button`'s `main` variant (the default stays `primary`) and its tests;
   - the showcase;
   - foundation §5's "one main action per screen" rule and §12's Button row.
4. `b284e80a` — `feat(web): mark each screen's main action`:
   - 42 call sites, `StateActions`' first button, the announcements' header button and `HoursSheet`'s confirmation;
   - two tests updated (`StateActions`, About);
   - new assertions for Home, the desk and the new `ContactBar` test.
5. `071e9214` — `feat(directory): lead the contacts with WhatsApp`: D6.
   - From 768 px, a full-width «واتساب» `main` leads the contacts, in the aside from 1024 px and in the contacts
     section below it.
   - Its component test, and `directory.md`'s decision and history lines.

Every subject is ≤ 50 characters and every commit has a body. There is no tool attribution and no `fixup!` left. The
two `#PRNUM` placeholders became #158 and were folded into commits 3 and 5 by autosquash before the push.

## 3. What was run, and what was not

**Locally, on the head, one at a time, through `heavy.mjs b`:**

| Check | Result |
|---|---|
| `format:check` | pass |
| `check:links` | pass, 2808 links |
| `check:conflicts` | pass |
| `check:classes` | pass, 2001 files |
| `lint`, `typecheck` | pass on the head, and on each of the five commits (each checked out in turn) |
| `test:unit` | 1435 (web) + 924 (api) + 384 (shared) passed |
| `test:component` | 2201 passed, 352 files |
| production build (`NODE_ENV=production`) | pass. The built CSS holds `.bg-main-action`, `hover:bg-main-action-hover`, `.text-main-action-foreground`, and both themes' values |
| `check:build` | pass |
| After the `#PRNUM` fold (Markdown only) | `format:check` and `check:links` again |

**CI:** every job passed on `071e9214`, `test:api` included. CodeRabbit skipped, as it usually does.

**Not run locally:** `test:api`, which the prompt leaves to CI, and no API code changed.

**The Chrome pass** used a headless Chrome over CDP, with the API on 3320 and the web on 5320. The script and its
outputs are in `TASKS\BERRY_PRIMARY\scripts\` (`berry.mjs`, `compare.mjs`, `out-before.json`, `out-after.json`,
`compare.txt`).
- **Coverage:** six screens (home, the space page `pal-hub`, the directory, sign-in, the owner's desk, the admin's
  «المساحات»), at 390 and 1440, in Arabic and English, light and dark. That is 48 runs per side, plus the desk's visit
  dialog in light at 1440, in Arabic and English.
- **"Before"** is a detached `origin/main`. **"After"** is the head. In each run, every visible control's painted
  colours were recorded and then diffed.
- **Light:** on each screen with a main action, that action is the only control that changed: `#1a1f25` became
  `#934791`, and its label stayed white.
  - Home: «بحث» / «Search».
  - Space page below 768 px: the bar's «واتساب».
  - Desk: «تسجيل زيارة» in the top bar at 1440 and in the action bar at 390.
  - Admin: «إضافة مساحة».
- **Dark:** nothing changed in any run.
- **The space page from 768 px** adds its «واتساب» (D6): berry in light, the ink's button in dark.
- **Directory and sign-in:** no main action and nothing changed. Sign-in is #157's and waits (§8).
- **Hover** (1440): `#773a75` in light, and the ink's hover in dark (`oklab(0.841 …)`, which is `#c7cbd0`).
- **Focus ring:** `:focus-visible`, solid 2 px at a 2 px offset, in `ring`: `#1a1f25` in light, `#f7fbff` in dark.
- **axe:** 0 violations in all 50 "after" runs, as before. No sideways overflow and no page errors.
- **The visit dialog:** its «تسجيل الزيارة» is berry. The page's «تسجيل زيارة» stays berry behind the scrim, which is
  design issue 2, accepted (D2).
- **Shots:** in `C:\Users\basel\Downloads\berry-shots\`, kept out of the repository.
  - Curated before / after pairs (`<screen>-<width>-<lang>-<theme>-1-before.png` / `-2-after.png`). Each screen has
    Arabic light and dark at 1440, Arabic light at 390 and English light at 390; the dialog has Arabic and English.
  - `hover-focus\`: 13 crops.
  - `raw\before\` and `raw\after\`: every combination.
- **Afterwards:** the servers were stopped by PID (the API's `tsx watch` parent too) and ports 3320 and 5320 checked
  free.

## 4. Breaks made, and tests seen failing first

**Seen failing first:**
- **The token test:** 35 of 232 cases failed before the role existed (key parity, every new contrast, shape and
  distance case, the fill-only and dark-pin tests). All 232 pass after.
- **`Button`:** "draws the main variant with the main action's fill, label and hover" failed before the variant
  existed.
- **The five screens' assertions** failed before the call sites changed:
  - About «Browse spaces»;
  - Home «Search»;
  - the desk's top-bar check-in beside the rows' ink «Collect»;
  - `StateActions`' first button;
  - `ContactBar`'s «WhatsApp».
- **`SpaceDetails`' "from 768 px «واتساب» leads the contacts"** failed before D6 was built.

**Breaks made once, each restored** (the tree is identical afterwards):

| Break | Failed |
|---|---|
| Light `main-action: spark-500` | the label on the fill (4.11 : 1), 1 case |
| Light `main-action-hover: spark-400` | the hover's label and its shape on three grounds, 4 cases |
| Dark `spark-600` + white (B1's rejected option) | shape on card and popover (2.80 : 1), the hover's label, the dark pin: 4 cases |
| Dark `main-action: spark-400` (the superseded P2 dark) | the dark pin only, since it passes contrast: the reason that test exists |
| Light `main-action: red-600` | distance from destructive under normal, protan and deutan vision, 3 cases |
| `--color-main-action` added to `@theme` | the fill-only test, 1 case |
| `Button`'s `defaultVariants.variant: 'main'` | "stays in the ink unless the main action is asked for" |

The plan's "a closer break" for the distance, light hover `spark-800`, passes (0.219 / 0.140 / 0.218), so it is no
break. The `red-600` break stands in for it.

**The hover's distance from `destructive` (N2 of the review):** no hover value was seen failing it. Its case runs on the
same `it.each` as the fill's (`['primary', 'spark', 'main-action', 'main-action-hover']`), whose mechanism the
`red-600` break proved on the fill. The hover's own margin is held only by that shared test.

## 5. Problems met, and how each was solved

- **The refresh limiter (30 per 15 minutes).** The "after" Chrome run's last desk combination (1440, English, dark)
  and the two dialog runs drew the desk's error state, after three `429`s on `/api/v1/auth/refresh`.
  - **Cause:** each page load refreshes the session, and the "before" and "after" desk loads, with a preference load
    before each, all fell inside one window.
  - **Fix:** I waited out the window and reran the whole "after" set once. Every run then passed. The script also
    gained a rerun filter.
- **The first focus-ring reading said white in light** (the label's colour). `transition-colors` animates the outline
  from `currentColor` to `ring` over 150 ms, and the script read it at once; the crop already showed the ink ring. The
  script now reads after 400 ms, and the values are `ring`'s.
- **No browser tool in this session.** The pass ran headless over CDP, as earlier items' scripts did (AXE_FIXES, C2),
  and I looked at the shots myself. The prompt's "browser pane shown" could not be met as written (§8).
- **`jq` is not installed,** so my first CI-wait loop and monitor never ended. I stopped both and used `gh`'s own
  output.
- **A `textwrap` reflow** of `Button`'s comment first broke `main-action-hover` across lines. I rewrapped it without
  breaking hyphenated words, before the commit.
- **Only 3.5 GB was free at the start,** so I did the code first and took the "before" shots from a detached
  `origin/main` afterwards, with 6.7 GB free.

## 6. Anything that behaved unexpectedly

- **The refresh limiter** (§5) is reached by about 30 page loads of one signed-in user in 15 minutes. That is real
  behaviour, not a defect, but a long Chrome pass meets it. A future pass should batch a user's pages, or run them
  apart in time.
- **In the visit dialog's run, two `main` buttons are in the DOM:** the page's, under the scrim, and the dialog's. That
  is expected (design issue 2, D2). A check that counts `.bg-main-action` across a page must count overlays apart.
- **Nothing else.** The before / after diff shows no control changing that was not meant to.

## 7. Early conflict check

`gh pr list --state open`: #157 and #158.
- **#157** (`feat/sign-in-in-place`, head `305c5d3f`): `git merge-tree --write-tree 071e9214 305c5d3f` is **clean**
  (tree `2f3f9023`), with no file in conflict.
- `foundation.md`, the design system's files and `directory.md` are not #157's. Its `SpacePage.component.test.tsx` was
  left untouched, as asked.

## 8. Departures from the prompt and the plan

- **The auth forms are not in this PR (D4).** #157 was open, not merged, at the push. These stay in the ink for now:
  the sign-in, register, forgot and reset forms; the reset and forgot pages' link buttons; `SignInPrompt`; and #157's
  in-place views.
  - **The follow-up**, after both merge, gives `main` to the submit, or to the done state's one link, in each.
  - **Candidate files on #157's head:**
    - `features/auth/components/`: `sign-in/SignInForm.tsx`, `register/RegisterForm.tsx`,
      `forgot-password/ForgotPasswordForm.tsx` and `ForgotPasswordSteps.tsx`,
      `reset-password/ResetPasswordForm.tsx`, `resend-link/ResendLinkForm.tsx`, `set-password/SetPasswordByEmail.tsx`;
    - `pages/site/auth/`: `ForgotPasswordPage.tsx`, `ResetPasswordPage.tsx`, and `in-place/`: `ForgotView.tsx`,
      `InPlaceSignIn.tsx`, `RegisterView.tsx`, `SignInFormView.tsx`;
    - `pages/site/public/SignInPrompt.tsx`.
  - Which button in each is the main one is decided on #157's merged code.
- **"The browser pane shown":** there was no browser tool. The pass was a headless Chrome over CDP, with every shot
  saved and reviewed (§5).
- **The overlay check** covered one dialog (the visit dialog, light, 1440, Arabic and English) beyond the six screens.
  The other overlays' `main` buttons are covered by the diff review and their call sites, not by a shot each. This
  matches the plan's Review Focus.
- **The capability document:** the plan said no capability document changes. D6 changed the space page's behaviour,
  so `directory.md` gained a web decision and a history line (#158), in commit 5.
- **Commit 5 is an extra commit,** D6 on its own. The plan's optional commit 5 (the auth forms) did not happen.
- **The showcase's `primary` sample** became "Filled action" / «إجراء ممتلئ», since "Primary action" beside "Main
  action" would mislead.

---

# Fix round (the review `9_REVIEW.md`, the prompt `10_FIX_ROUND.md`)

## 1. The pull request and its head

**#158**, new head **`ba63b8331fabcd16cf6dc5c7d403ab437d2b5a21`**. It was pushed with
`--force-with-lease=feat/berry-main-action:071e9214…`, and the lease held. CI is green on that head (run 45633789159,
`test:api` included) and GitHub shows `CLEAN`. The pre-fix head is kept locally as
`backup/berry-main-action-pre-fix` (`071e9214`). There is one "Review fixes" comment on the PR, and its description is
updated: the D6 line, the component count, and the fix round's Chrome lines. **Not merged.**

## 2. The commits

Each fix is folded into its own commit by fixup and autosquash on the same base, `c3968a74`. Commit 5's message was
rewritten through `amend!`. No `fixup!` or `amend!` is left.

1. `d14f7158` — `docs(adr): keep dark main action in the ink`: unchanged.
2. `29da3f88` — `feat(design-system): add the main action role`: **N1**, foundation §5's spark rule links ADR 0022 after
   "a step darker".
3. `ea36d6b3` — `feat(design-system): add Button's main variant`: content unchanged; rebased over N1 (see §5).
4. `97139686` — `feat(web): mark each screen's main action`: **S1**.
   - `PackagesSection` draws the header's «باقة جديدة» `main`, and the empty state's copy `primary`.
   - Its new test.
5. `ba63b833` — `feat(directory): lead the contacts with WhatsApp`: **S2**, rebuilt as approved.
   - The page's view gains `contacts.lead`: from 768 px the space's WhatsApp, else its first contact; `null` below 768 px.
     `items` holds the rest, in the owner's order.
   - `ContactList` draws the lead first as Button's `main`, with its word and its number. The others keep their rows.
   - `SpaceDetails`' separate «واتساب» button is gone, and `SpacePageView`'s bar comment is back to its first text.
   - `directory.md`'s behaviour, decision and history lines describe the built shape, and so does the commit's body.

**N2** is in the report only (§4 above).

## 3. What was run, and what was not

**Locally, on `ba63b833`, through `heavy.mjs b`:**

| Check | Result |
|---|---|
| `format:check` · `check:links` (2809) · `check:conflicts` · `check:classes` (2001) | pass |
| `lint` · `typecheck` | pass on the head and on commit 4 (`97139686`), the other rewritten code commit. Commit 2 changed only Markdown |
| `test:unit` | 1435 + 924 + 384 passed |
| `test:component` | **2203** passed: 2201, plus the two new tests |
| production build · `check:build` | pass |

**Not run locally:** `test:api` (CI ran it: pass).

**Chrome** (`berry.mjs fix`), on the head:
- **Coverage:**
  - the space page `pal-hub` at 390, **800** and 1440;
  - the owner's **Packages & prices** at 390 and 1440;
  - Arabic and English, light and dark: 20 runs.
- **The space page, from 768 px:** one WhatsApp link in the page, the filled `main` with its number. In light it is
  `#934791` and hovers to `#773a75`; in dark it is the ink's button. Its focus ring is `ring`.
- **The space page, at 390:** the bar's «واتساب» is the only `main`. The list's WhatsApp row stays a plain row, as
  before.
- **Packages:** one `main`, the header's «باقة جديدة».
- **Everywhere:** axe 0, no overflow, no page errors.
- **Fresh after-shots** are in `Downloads\berry-shots\fix-round\`:
  - `space-1440-ar-light` (the aside, WhatsApp filled once) and `space-1440-en-dark`;
  - `space-800-*-main` (the contacts section);
  - `space-390-ar-light`;
  - `packages-*-main`;
  - the hover and focus crops.
- **The curated `space-*-2-after.png` pairs** in `berry-shots\` were replaced by the fix round's shots. The first
  after-shots stay in `raw\after\`.
- **Not shown:** Packages' empty state. The demo space has packages; the component test holds it.
- **Afterwards:** the servers were stopped by PID (the `tsx watch` parent too), and ports 3320 and 5320 checked free.

## 4. Tests seen failing first, and breaks

Run before the fixes, these three failed and the rest passed (3 failed, 35 passed):
- **`PackagesSection`:** "draws the header's «New package» as the main action, and the empty state's copy in the ink".
- **`useSpacePage`:** "from 768 px leads the contacts with WhatsApp, else the first channel, never repeated; below it
  no lead". It renders phone-then-WhatsApp at 1440, so WhatsApp is moved first; email-then-phone at 800, so the first
  channel leads; and 390, with no lead.
- **`SpaceDetails`:** "from 768 px the first channel, WhatsApp, is the page's main action, drawn once; below it the bar
  holds it". It replaces the first round's D6 test, which asserted the second button.

**One existing case changed, without weakening it:** `useSpacePage`'s email-only case. It proves the bar is `null`
without a WhatsApp or a phone, and it now renders at 390, where the bar lives. At 1440 the email would be the lead and
`items` empty, so its unchanged `items` assertion holds on a phone.

N1 and N2 have no code.

## 5. Problems met

- **The autosquash conflicted twice in `foundation.md`.** N1's line sits next to the bullet that commit 3 adds.
  - The first conflict, applying N1 to commit 2: I kept the linked spark line, without commit 3's bullet.
  - The second, replaying commit 3: the linked spark line, then its bullet.
  - **Result:** `git diff ORIG_HEAD HEAD` was empty (the same tree as before the rebase). Commit 2 carries the link,
    and commit 3 the bullet.
- **`heavy.mjs` runs its command through `cmd`,** which read the filter's `|` as a pipe. The run went through a one-line
  bash script instead.
- **React Router's scroll restoration** carried a path's scroll from the previous run, so the first fix-round shots
  started scrolled down. The script now scrolls to the top before each viewport shot, and adds a `-main` shot centred
  on the main action.
- **The first lint run** waited for its grant and took about three minutes under load. It passed.

## 6. Anything unexpected

- The scroll restoration above. It only matters for scripted shots that revisit a path.
- Nothing else.

## 7. Early conflict check

`gh pr list --state open`: #157 (`305c5d3f`, unchanged) and #158. `git merge-tree --write-tree ba63b833 305c5d3f` is
**clean** (tree `c249c372`).

## 8. Departures

- **"First channel" is read as "WhatsApp when the space has one, else the space's first contact".** The prompt says
  "the list's own first channel (WhatsApp when the space has it)". So when a space lists WhatsApp after another
  channel, WhatsApp is moved to the front from 768 px. The others keep the owner's order. `directory.md` says so.
- **The lead keeps the list's words** (its type's word, then its number), filled, and not the bar's bare «واتساب».
  This is the `PlatformContact` pattern the plan named.
- **Commit 5's body was rewritten** (through `amend!`), since it described the first shape.
