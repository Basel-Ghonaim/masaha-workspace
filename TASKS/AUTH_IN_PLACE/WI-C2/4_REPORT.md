# WI-C2 — Report: sign in where the action is

> Worker: Claude Code (Opus 5.5), worktree `C:\dev\masaha\app-design`. Plan `2_PLAN.md`, approved with D1 (the
> one line everywhere), D2 = B, D3–D8 and design issues 1–7 as recommended. Resumed on 2026-11-25 after the
> machine's restart (`3_RESUME_MESSAGE.md`). **Not merged.**

## 1. Pull request and head

- **#157**: https://github.com/Basel-Ghonaim/masaha/pull/157, `feat/sign-in-in-place` → `main`.
- **Head:** `305c5d3f39fd133e94f0a14b36c6a12914346fde`. `gh pr checks 157`: every check passed on this head
  (build, check:classes, check:conflicts, check:links, format:check, lint, test:api, test:component, test:unit,
  typecheck; CodeRabbit skipping). `mergeStateStatus`: **CLEAN**.
- **Size:** 90 files, +2,817 / −429. Branched from `65288e70` (#155).
  - `main` has since moved to `c3968a74` (#156, ADR 0022), changing `docs/README.md`, ADR 0019 and ADR 0022 only.
  - None of those is a file of this PR, and none it links was renamed: a merge apart, so no rebase.

## 2. Commits

1. `acffae08` **feat(forms): password condition as one line:** D1's line in `shared/forms` (`PasswordRules`,
   `usePasswordRules`, the view), both catalogues, the checklist tests rewritten, architecture §3, `users.md`.
2. `07e89a1d` **feat(site): sign in where the action is:**
   - the shell (`SignInPrompt`, `inPlaceHeading`, `SignInBody`) and the lazy body (`pages/site/auth/in-place/`);
   - `features/auth`'s options (`defaultEmail`, `onEmailChange`, `focus`, `onRequested`, `onResent`), plus
     `useSignInBusy`, `ForgotPasswordSteps` and `linkRefusedAction`, and `FormFailure`'s `action`;
   - `intentMayRun`, `heldIntentPreview`, `renewHeldIntent`, `onRecoveryDoneElsewhere`, the report's name;
   - the tests; architecture §2 and §4; `auth.md`, `favorites.md`, `data-reports.md`; finding 230.
3. `57ccca6e` **feat(auth): sign in on the reset page:**
   - the card's `signIn`, `returnNote` and `doneDescription` slots, and the page's sign-in and landing;
   - S1 (the held path read as `next`);
   - their tests, the auth catalogue, and the documents.
4. `305c5d3f` **chore(build): keep the sign-in off site pages:** `scripts/signInChunk.ts`, the `vite.config.ts`
   group, `signInProblems`, its unit tests, architecture §3.

Every subject is ≤ 50 characters, with a body, no attribution and no `fixup!` left. `#PRNUM` was replaced by
`#157` in each commit's tree (filter-branch) just before the push, after checking both lists (PRs to #156,
Issues to #151).

## 3. What was run

All heavy runs went through `heavy.mjs c2`, one at a time, on the head:

| Check | Result |
|---|---|
| `format:check` · `check:classes` (2,020 files) · `check:links` (2,816 links) · `check:conflicts` | clean |
| `lint` · `typecheck` | clean |
| `test:unit` | web 1,442 in 199 files, API 924 in 77, shared 384 in 29 |
| `test:component` | 2,256 in 353 files |
| `build` (`NODE_ENV=production`) | clean |
| `check:build` | clean; its new line: *No sign-in code in the site's first download, nor in a public page's or the shell's static imports.* The `sign-in` chunk is 21.29 kB, 6.30 kB gzipped |

Lint and typecheck ran on the head, not on each commit. The memory floor kept heavy runs scarce, and the four
commits were cut from one finished tree.

**Chrome.** The Chrome extension is not part of a worker's launch, so this was headless Chrome over CDP
(`chrome.mjs` beside this report; outputs `chrome-out-{matrix,flows,google}.json`). It ran with the API on 3323
and the web on 5323 against `masaha_dev`, as the guest and then as the demo owner, on `/spaces/pal-hub`. Shots
are in `C:\Users\basel\Downloads\c2-shots\`.
- **Matrix:** 390 and 1440 × Arabic and English × light and dark × the sign-in, register and forgot views (24).
  - The form is `panel` below 768 px and `dialog` above it.
  - The focus is on the title at every opening and every switch.
  - **axe: no violation in any of the 24.**
- **Flows** (390 Arabic, 1440 English):
  - Opening adds one history entry; Back (390) and Escape (1440) close it, keep `/spaces/pal-hub`, and remove
    `masaha.heldIntent`.
  - A wrong password shows its alert.
  - A real sign-in from the heart closes it, keeps the URL, presses the heart and puts the focus on it, with
    one toast «حُفظت بال هاب في المفضّلة». The favourite was then removed again, to leave the demo data as it was.
  - The report opens its dialog after the sign-in.
  - The link sent shows `d•••@example.com` and the NEW line naming the space.
  - A1, from a second tab writing `masaha.recoveredAt`, brings the sign-in back with the e-mail filled and the
    notice.
  - The reset page, opened from the e-mail's link in the API's log, says «بعد الحفظ سجّل الدخول هنا، ونعيدك إلى
    بال هاب…».
  - axe is clean on wrong, sent, changed and the reset form.
- **Google, at both widths:**
  - Google's frame draws inside the overlay.
  - Shift+Tab from the e-mail reaches Google's own button ("Continue with Google. Opens in new tab"), inside the
    trap, and Tab comes back to the e-mail.
  - Enter on it opens Google's window from inside the trap. That window lands on Google's OAuth error page, since
    `localhost:5323` is not an authorised origin of the client id.
  - With the window closed, the overlay is still open and no alert shows.
  - Page errors: none.

**Not run:**
- `test:api`: no API change; CI ran it, green.
- In Chrome, kept off the demo data:
  - completing a registration, which would create an account in `masaha_dev`;
  - completing a reset, which would change the demo owner's password;
  - a temporary password's sign-in, which needs the admin to issue one.

  The component lane proves all three.
- Google's real credential return: it needs an authorised origin and a Google account, which is never used in
  a browser here. `fakeGoogle` in the component lane proves it.

## 4. Breaks made, tests seen failing first

Each break was applied by script (`breaks.py`), each file backed up first and restored from that copy.

| Batch | The breaks | Seen failing |
|---|---|---|
| **U** (unit) | `intentMayRun` without the change clause · the old held-path check (S1) † · `renewHeldIntent` creating an intent · the preview taking it · `checkBuild` without the page reach · the report's name dropped · `onRecoveryDoneElsewhere` without its key check · the generic register title | 13 failed, every one a target: S1's backslash and dot cases, the renew and preview cases, the `check:build` page and shell cases, the register titles, the report name, the key cases, and `intentMayRun`'s pending change |
| **C1** (component) | `intentMayRun` † · `useSignInBusy` never busy · Google's refusal slot not drawn · `FormFailure` without its action · the password line stuck on "needs" · `useEmailReport` a no-op · the reset form's note dropped · the reset page landing without the intent · `onRequested` / `onResent` / the focus option removed | 36 failed, the targets listed in the PR |
| **C2** (component) | no A1 listener · the prompt not closed by the session · no renewal · the privacy link without `target` · no focus on a switch · Google remounted per view · the sent note never shown | 12 failed |
| **G** | Google remounted per view, alone (its C2 failure was shared with another break) | its test alone failed |
| **`check:build`** | a static `@features/auth` import in `SignInPrompt.tsx` | the rule failed, naming DirectoryPage, HomePage and SpacePage; restored from a copy, tree clean |

**Not caught by its own test.** With `intentMayRun` broken, the overlay's temporary-password test still passed.
The gate unmounts the site shell in the same render, so no request leaves even without the rule. The hook tests
of the favourite and the report fail. The rule now holds by itself, not by render order.

**At the resume (step 1 of the resume message):** no deliberate break was still applied.
- Each break of the three batches was checked against the working tree: every original text was in place.
- The backup folder held empty directories only, because the C2 script had restored its files before the run
  ended.
- The one `key={view}` in `InPlaceSignIn.tsx` is the sign-in form's own, intended.

## 5. Problems met, and how each was solved

- **Memory.**
  - The machine stayed at 2.8–3.9 GB free (other sessions, Chrome, Copilot), under the grant's 4 GB floor, for
    most of 2026-11-24, so most runs waited a long time.
  - Background runs reached their 10-minute limit while still waiting and were stopped; none held a slot.
  - The headless run then ended (exit 4) while it waited.
  - On the resume, every heavy run went in the foreground with a long limit, as the message asked.
- **A local `.env` broke the Google tests.** `apps/web/.env` has a real `VITE_GOOGLE_CLIENT_ID`.
  - The overlay's earlier tests therefore started loading Google's real script, which never answers in jsdom.
  - That pending load is cached in `googleIdentity`'s module map, and the later fake waited behind it.
  - CI has no `.env`. The test file now sets the client id empty in `beforeEach`; the Google tests set the test
    one.
- **A held report lingered between tests.** The report test's dialog was left open, so the held report stayed in
  the module's memory, and the next test's sign-in opened it. The test now closes the dialog (Escape). See §6 for
  what this says about production.
- **The `sr-only` "(opens in a new tab)" lost its space** in the accessible name ("policy(opens…"). The space is
  now a separate text node.
- **The 15-minute test:** the stored time was first written on the fake clock. It is now written after the real
  clock is back.
- **A test with five axe passes timed out in the full lane** (5 s), though it passed alone. It was split into a
  focus test per width and one axe test per width and view (10). No timeout was raised.
- **Lint found a real bug:** `signInChunk.ts`'s regex had lost its doubled backslash (`[\/]`), so it matched
  only `/`. It was fixed to `[\\/]` and folded into its commit. The other lint findings were test style
  (hook-named properties, void arrows).
- **Splitting files between commits.** Interactive add is unavailable, so each split file's version for each
  commit was staged with `git hash-object -w` and `update-index`, still by path. Each review fix was folded into
  its commit (fixup and autosquash).

## 6. What behaved unexpectedly

- **A held report survives a sign-out in the tab's memory.** `reportIntent` drops its memory only when it is
  taken, after 15 minutes, or when the guest leaves the page; `dropHeldIntent` on a sign-out clears the storage
  only.
  - So a guest who held a report, signed in (the dialog open), and signed out without closing it would see the
    dialog open again at the next sign-in on that page, within its 15 minutes.
  - This was in production before this item, with the round trip. Unrelated, so not fixed: a finding at the
    supervisor's word.
- **Google's frame draws late at 390.** Half a second after opening, the frame is still blank (the matrix's first
  Arabic shot). It draws a moment later (the Google run's shot).
- **A1 after the reset tab signs in first.** If the reset tab signs in before the waiting tab, the waiting tab's
  sign-in saves the same favourite again: idempotent, with a second toast. Stated in the plan's Review Focus, not
  fixed.
- **The CDP mouse click on Google's frame centre opened no window.** The keyboard path (Enter) did. Google's
  visible button is its own element over the frame.

## 7. Early conflict check

`gh pr list --state open`: only #157. No other head to check. WI-B's ADR (#156) merged before; WI-B's code PR is
not open yet. It will touch the design system and `foundation.md`, which this PR does not.

## 8. Departures from the prompt and the plan, with reasons

- **The order of the work.** The prompt put the Google checks first. They need the overlay built, and on
  2026-11-24 even the typecheck waited an hour for memory. The item was built first, and the Google checks ran
  in Chrome before the PR. Nothing in the result depended on them failing; they passed.
- **Commits: 4, not 6.** The plan's "sign in in place" and "the reset link's request" became one commit (the
  overlay's body serves both, in the same files). D1 stayed its own commit, and so did the reset page and the
  build rule.
- **No `enterKeyHint`** on the fields (plan §4.8). A "next" key whose Enter submits the form on iOS would show
  the empty password's error. The browsers' own keyboards already move between fields.
- **The ✓ of «✓ كلمة المرور مناسبة»** is the layer's `CircleCheckIcon` in the success colour, hidden from
  assistive technology, not a typed character. The words are as approved.
- **The password line is the field's description, not a live region**, as the checklist was. A count that
  changes on every keystroke would be read aloud on every keystroke.
- **The A1 notice** is the layer's `info` alert with the success tick: the layer has no success variant
  (finding 230, Open), and this item touches no design-system file.
- **The report's held intent's `name` is optional** when read, so a report held before this deploy (within its
  15 minutes) still runs.
- **Three existing tests' comments or setup changed** beyond D6's list:
  - the space page's test warms the overlay's body (testing rule 8), and its comment "the prompt stays open
    here" now says it closes;
  - `SignInPrompt`'s test got a QueryClient wrapper, since the body's forms use mutations.

**Left for the owner:**
- Finding 230: a success `Alert` variant.
- The held report surviving a sign-out (§6): a finding to record, if the supervisor agrees.


---

# Fix round (2026-11-25) — R1 (security) and R2 (experience), `7_FIX_ROUND.md`

## 1. Pull request and head

- **#157, new head `ad0ba75e3e4f50d072fb86d0d6e81825bd88020b`.** It was pushed with `--force-with-lease` pinned
  to `305c5d3f39fd133e94f0a14b36c6a12914346fde`. The pre-fix head is kept on `backup/sign-in-in-place-pre-fix`.
- `gh pr checks 157`: every check passed on `ad0ba75e`. `mergeStateStatus`: **CLEAN**.
- One "Review fixes" comment lists each point and its commit:
  https://github.com/Basel-Ghonaim/masaha/pull/157#issuecomment-7166230315 (its text is `review-fixes.md` beside
  this report).
- The PR description was updated to the final state: the held intent's mark, the gate's fix, the counts, and the
  Review Focus checks.

## 2. Commits

Each fix is folded into its commit (fixup and autosquash on `65288e70`). Four commits again:
1. **`0c78eb6e` feat(forms): password condition as one line:** + `users.md:42`.
2. **`7100c799` feat(site): sign in where the action is:**
   - S-1 (`guestLeaving.ts`, two hook tests);
   - N-1 (Google inert, the switches disabled, the shell's «العودة إلى تسجيل الدخول» too; one test);
   - the focus on the forgotten password's step and on the chunk's retry; N-3 and the focus in test 10;
   - **the gate's redirect** (§5a below; its test, architecture §2's gate bullet);
   - the `RegisterForm` comment; findings 231–234;
   - the `sign-in` chunk line taken out of `auth.md` here.
3. **`28f9d4e6` feat(auth): sign in on the reset page:**
   - S-2 (the tab's mark, `heldIntentPreview('tab')`, the link sent's note) and N-2 (the path `returnUrlOf` yields
     is the one followed), with their unit cases; the existing "kept in storage" case now expects the mark;
   - the reset page reading the held action again once the password is set, and its test;
   - the held-favourite test expecting `post /me/favorites/7` once;
   - the `ResetPasswordForm` comment;
   - architecture `:139` and §4 (the tab's mark, the path followed).
4. **`ad0ba75e` chore(build): keep the sign-in off site pages:** + the `sign-in` chunk line in `auth.md`, where the
   chunk arrives.

S-2 and N-2 went into commit 3, not 2. They rework how the held intent is read, as that commit's S1 already does;
and N-2 replaces S1's `isOwnPage`, so in commit 2 it would not have applied.

## 3. What was run

All in the foreground through `heavy.mjs c2`, on `ad0ba75e`:

| Check | Result |
|---|---|
| `format:check` · `check:classes` · `check:links` (2,822) · `check:conflicts` | clean |
| `lint` · `typecheck` | clean (lint first caught `expect.any` in the new held-intent case; rewritten and folded) |
| `test:unit` | web 1,446, API 924, shared 384 |
| `test:component` | 2,261 in 353 files |
| `build` (`NODE_ENV=production`) and `check:build` | clean; `sign-in` 21.29 kB, 6.30 kB gzipped |

**Not run:** `test:api` (no API change; CI green).

**Chrome:** `chrome2.mjs` beside this report; outputs `chrome2-out-{temporary,cards,network}.json`; shots in
`Downloads\c2-shots\`. The servers were stopped by PID afterwards, both ports checked free, and no `cdp-` Chrome
left.

## 4. Breaks and tests seen failing first

| Point | Test | Before the fix |
|---|---|---|
| S-1 | `useResumeFavorite`: sign-out → another account → no post; `useReportAction`: no dialog | both failed |
| S-2 | unit: another tab's hold runs nothing; the preview by tab | failed (2) |
| N-2 | unit: `/spaces/./noor-hub` followed as `/spaces/noor-hub` | failed |
| N-1 | Google inert, the switches disabled while a password sign-in is pending | failed |
| R2-1 | test 10: the focus on «Check your email» | failed (see the note below) |
| R2-11 | the reset page with the held action let go before the set: no return line | failed |
| R2-2 | the reset page's held favourite: `post /me/favorites/7` once | **passed at once**: a strengthened assertion; the save was already happening, now proven |
| N-3 | test 10: no e-mail in `masaha.heldIntent` | passes, as nothing writes it (D2 = B); no code to break |
| §5a | the gate's interrupted redirect (a browser router, an entry pushed as the overlay pushes it, Back while the change page loads) | failed; the first, memory-router version did **not** reproduce the real case (§5a) |

Note on R2-1: the run that pinned its failure point only reported the test's line, because it ran alongside the
fixes. Of test 10's two new assertions, only the focus one can fail, since no e-mail is ever written. The full run
before the fixes showed the test failing.

## 5. Problems met, and how each was solved

- **(a) A temporary password's history: a real bug, beyond what R2 suspected.**
  - **What Chrome showed:** after an in-place sign-in with a temporary password, the address stayed
    `/spaces/pal-hub`, the title was the space route's, and `main` was empty: **a blank page**, not the change
    page.
  - **The history log** (`pushState`, `replaceState`, `back` and `popstate` wrapped in the page): only the
    overlay's `back()` and its `popstate` ran, and the router never wrote the change page.
  - **The cause:**
    - the gate's `<Navigate>` redirect waited for the lazy change page;
    - the overlay's step back interrupted it, landing on the page's own entry, with the same router key the
      overlay's entry had copied (#155);
    - the router then rested idle at the same location, and the same `<Navigate>` element never fired again.
  - **First attempts:** keying `<Navigate>` by `location.key` (the key is the same, so no change); then an effect
    on the location object (the router keeps the same object, so no re-render with anything new). The
    memory-router test passed with the first attempt but did not reproduce the real case. It was rewritten with a
    browser router and an entry pushed exactly as the overlay pushes it, and then it failed as Chrome did.
  - **The fix:** `PasswordChangeGate` redirects in an effect whenever the router's navigation is `idle` away from
    the change (`useNavigation`).
  - **In Chrome after the fix:** `back` → `popstate` → `replaceState` to `/change-password?next=%2Fspaces%2Fpal-hub`
    within ~70 ms, and the change page renders. Back from it reaches Home, which the gate redirects, as for any page
    while a change is pending. Forward reaches the overlay's old entry, which the gate redirects too. No blank page.
  - **The demo data:** the admin issued a temporary password to `demo-reception@example.com` for the check; the
    forced change set it back to the demo password, checked by an API sign-in.
- **(b) Home and the directory:** the first run clicked «Nearest to me», also a toggle with `aria-pressed`; the
  selector was narrowed to the hearts. The second compared names in English, while the sign-in had switched the
  page to the owner's Arabic (finding 231); the heart is now found by its space.
  - Result, at 390 and 1440 on both: the page stays, the heart is saved, and the focus is on that same heart after
    the grid re-renders.
- **(c) Slow 3G and offline:**
  - **Slow 3G** (2 s latency, 500 kb/s): the overlay opens at once with its title (focused) and the loading line.
    The forms took ~26 s from the **dev server**, which serves dozens of unbundled modules each paying the latency;
    production loads one 6.3 kB gzipped chunk.
  - **Offline:** «تعذّر تحميل تسجيل الدخول…» and «إعادة المحاولة».
    - One retry ran before the browser saw the connection back (`ERR_INTERNET_DISCONNECTED`), a script timing
      issue.
    - Waiting for `navigator.onLine` first, the retry refetches (64 module requests) and loads the forms, the focus
      on the title. Twice in a row.
    - One earlier run also showed no forms 20 s after the retry, with no network log taken; the instrumented runs
      after it all loaded.
- **Commit placement:** N-2 replaces C's `isOwnPage`, so S-2 and N-2 went to C (§2). The `auth.md` chunk line was
  moved by two fixups: removed in B, added in D.

## 6. What behaved unexpectedly

- **The gate's blank page (§5a).** It was not visible in the component lane: there the change page's route is
  warmed, so the redirect lands before the step back. Only a real browser showed it.
- **The overlay's old entry stays as a forward entry** after a temporary-password sign-in. It is #155's known limit:
  no `AdaptiveDialog` is mounted on the change page to step back from it. Forward reaches it and the gate redirects
  it, so it does no harm.
- **The language switch** on a sign-in over the page (finding 231), seen again in (b).

## 7. Early conflict check

`gh pr list --state open`: only #157. `main` moved to `169d6aa7` with #158 (WI-B, the berry), merged at 14:44 UTC,
before this push. It shares no file with this PR and deletes or renames nothing (one file added): a merge apart. CI
on `ad0ba75e` ran after it, green; `CLEAN`.

## 8. Departures, and what is left for the owner

- **N-4:** accepted as is. The rule "the action waits for a forced change" is proven by the two hook tests, since
  the gate unmounts the site shell first in the page test.
- **`site.signInPrompt.loadFailed`:** kept, listed for the owner (R2 nit 3).
- **The field error «كلمة المرور لا تستوفي الشروط أدناه»:** left as is, listed for the owner (R2 nit 4).
- **`enterKeyHint`:** still not set (report §8), for the owner to confirm (R2 nit 8).
- **The gate's change** (`shared/routing/guards/PasswordChangeGate.tsx`) is outside the plan's file list. It was
  needed to make (a) right; architecture §2's gate bullet states it.
- **Findings 230–234** are open for the owner.
- **Never merged.**
