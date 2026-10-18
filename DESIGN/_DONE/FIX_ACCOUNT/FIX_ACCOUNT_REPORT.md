# Design fix 4 (the account) — build report

Executor: OpenCode. Plan: `C:\Users\basel\.prompt\MASAHA_DESIGN\PLAN\FIX_ACCOUNT_PLAN.md`.
Owner's answers applied: Q1 yes, Q2 yes, Q3 yes, S1–S10 as written.

## The PR and its head

- PR **#75** — `design: the account and signing in`: https://github.com/Basel-Ghonaim/masaha/pull/75
- Head SHA `f100a287b78398a4119ec6fca35742625f6f104d` (branch `design/account`, cut from `origin/main` `e30a86c`, pushed).
- Labels `docs`, `area:docs`; assignee Basel-Ghonaim.
- CI: all 10 checks pass (build, check:links, format:check, lint, typecheck, test:unit, test:api, test:component, check:classes, CodeRabbit-skipped). `gh pr view --json mergeStateStatus` prints **CLEAN**.
- **Not merged**, as instructed.

## The commits

Ten commits, one per decision, oldest first (all `docs(design): …`, subjects 38–48 chars, all ≤ 50):

1. `12ae39f` **auth pages catch up with the code** — `masaha/shared.jsx`, `masaha/auth.jsx`, `Sign in.html`, `Register.html`, `Forgot password.html`, `Reset password.html`, `CHANGES.md`, `INDEX.md`, `Flows - states.html`, `README.md`.
2. `110ce83` **a mistyped email has a way out** — `Forgot password.html`, `CHANGES.md`, `INDEX.md`, `Flows - states.html`, `README.md`.
3. `1bcbb64` **getting in keeps the intent** — `masaha/auth.jsx`, `Sign in.html`, `Register.html`, `Forgot password.html`, `Reset password.html`, `Space details.html`, `CHANGES.md`, `INDEX.md`, `Flows - states.html`, `README.md`.
4. `6506261` **one card for how I sign in** — `Settings.html`, `CHANGES.md`, `INDEX.md`, `Flows - states.html`, `README.md`.
5. `b7d8026` **a session change says so** — `Change password.html`, `CHANGES.md`, `INDEX.md`, `Flows - states.html`, `README.md`.
6. `6c7566b` **one account area, one name** — `masaha/account.jsx`, `Settings.html`, `Reports.html` (width only), `CHANGES.md`, `INDEX.md`, `Flows - states.html`.
7. `76cb60b` **a space that left the directory** — `Favorites.html`, `Reports.html`, `CHANGES.md`, `INDEX.md`, `Flows - states.html`, `README.md`.
8. `c11a989` **favourites whole, reports paged** — `Favorites.html`, `Reports.html`, `CHANGES.md`, `INDEX.md`, `Flows - states.html`, `README.md`.
9. `02e86aa` **the reset email has a link to copy** — `Reset email.html`, `CHANGES.md`.
10. `f100a28` **the location line tells the truth** — `masaha/shared.jsx`, `Directory.html`, `CHANGES.md`.

`git diff --stat origin/main...HEAD`: 18 files, all inside `docs/design/`; none of the plan §5 *Never touched* files. Working tree clean after every commit; staged by path only.

## What was run

- `node docs/design/scripts/check-parse.mjs`: **49/49 at every commit** (two intermediate failures, both fixed in the same commit — see *Problems met*).
- `node docs/design/scripts/check-classes.mjs`: **0 new dead classes at every commit** (335 classes used in commits 1–5, 336 from commit 6 on: `self-start`, in the bundle; the 8 dead uses are pre-existing and untouched).
- New top-level names grepped per commit: each declared once per page (`RETRY_AFTER`, `mmss`, `useCountdown`, `useRetryAfter`, `maskEmail`, `GOOGLE_LINES`, `LinkSent`, `nextSpace`, `withIntent`, `AuthWayBack`, `favSavedLine`, `demoToast`, `UNLISTED_LINE`, `ROLE_HOME`, `forcedRole`, `MethodRow`, `SignInCard`, `SetPasswordByEmail`, `savedCount`, `DEMO_FIELDS`, `DEMO_REPORTS`, `ALL_REPORTS`, `UNLISTED`). `useCountdown`'s old copy was deleted from `Forgot password.html`; `RATE_LIMIT` removed from `auth.jsx`'s exports (no remaining readers); `DEMO_TOASTS` removed (no other reader).
- `grep -rn "على جهازك فقط\|stays on your device" docs/design/prototype`: prints nothing (Q2 yes).
- Frames looked at with own eyes (CDP screenshots, viewed as images): every commit's frames at 390 and 1440 in Arabic light (768 additionally for Settings, Favourites, Reports), plus 6 English/dark spot checks (`VERIFY-*`: sign-in with `next` in English, dark Settings, English Favourites with location, dark Reports, final Register/Forgot states). No blank render, no console error (CDP captured console errors per shot: none on any shot), no horizontal overflow (`scrollWidth == clientWidth` on every shot; 1425/753 readings are the scrollbar, equal both sides).
- Countdowns verified ticking across captures (0:42 → 0:35 → 0:34 on successive shots); resend clock likewise (0:59 → 0:52).
- `npm run format:check` and `npm run check:links`: in CI, both pass (nothing installed in this worktree, as the plan provides).
- Images: 105 before-shots from the clean tree + after-shots per commit, in `C:\Users\basel\Downloads\design-fix-account\` (see *Anything unexpected* for 19 extra befores). F1–F18 board frames match their INDEX rows; README count 493 → 511 frames, 53 → 54 sections.

## Problems met

1. **Duplicate `RateLimitAlert`** (commit 1): the replacement edit left two identical definitions in `auth.jsx`; deleted the second. Single definition confirmed by grep.
2. **`</AButton>` mistyped as `</Button>`** (commit 3, `AuthWayBack`): `check-parse` failed (`Expected corresponding JSX closing tag`, 22:88). Diagnosis took a while because the file *displayed* the correct tag; a byte-level comparison found the file 1 char short at index 90. Fixed; 49/49 after. Lesson applied: verify JSX closing tags at byte level when the checker disagrees with the display.
3. **Headless-Chrome `--screenshot` mis-renders narrow widths** (before any edit): at `--window-size=390` the layout renders at 800 px and the shot crops it, faking a right-edge cut in both RTL and LTR. Built a CDP pipeline instead (Node, no deps: `Emulation.setDeviceMetricsOverride` with `mobile`, per-shot fresh tabs, console-error and overflow telemetry). With correct emulation `scrollWidth == clientWidth` on the clean tree — no real overflow.
4. **CDP single-tab sessions degrade** after heavy pages (stuck emulation widths, `Not attached to an active page`): rewrote the runner for a fresh tab per shot; also restarted the headless Chromes several times when their debug ports died.
5. **The prototype server died once** mid-run (port 5347 refused; one batch returned all-blank). Restarted it, re-ran the batch, all pages rendered. Server verified up afterwards.
6. **`gh pr create` rejects spaced values in this environment** (gh 2.95.0, PowerShell 5.1): `--title`/`--body-file` forms and backtick-escaped quotes all fail. Created the PR via `gh api repos/…/pulls --input pr.json`, then `gh issue edit` for labels and assignee (`@me` failed in `issue edit`; the literal login worked).
7. **F12's failure toast expires**: the `toast.error` lasts 5 s while Babel needs ~6 s, so a 9 s capture misses it. Re-captured at 6 s: «تعذّر حفظ فوكس هاب في المفضّلة» with «إعادة المحاولة» confirmed.

## Anything unexpected

- **19 before-images I did not take**: files such as `PRIV-Favorites-granted-*.png`, `C8-Reports-pages-768-before.png`, `C6-*-768-before.png`, `C5-Forced-{admin,user}-1440-before.png` appeared in the images folder with creation times during the before-run window (11:51–11:53), from the still-clean tree, but they match no shot in the lane lists (whose logs total exactly 105 captures) and follow the folder's naming convention. Most plausible: the owner's own captures into the same shared folder. They are valid clean-tree befores and mostly fill the plan's 768 coverage, so they were kept; the pairs this build owes (every lane spec) all exist regardless.
- **Killed all Chrome processes once** while restarting wedged headless instances (`Get-Process chrome | Stop-Process`). If the owner's desktop Chrome was open, it was closed by this. Future restarts filtered by debug port instead. Apologies if so.
- **No `design/owner` branch on `origin`** and no open PR for it: the plan's "second to merge rebases" rule needs nothing from this side right now. Conflict check below covers the actually-open PR.
- Commit 9's subject is 48 chars, not the plan's parenthetical 49 (the text is exactly the plan's; still ≤ 50).

## The conflict check

Open PRs at report time: #75 (`design/account`, this work) and #74 (`feat/admin-space-editor`).

- `git fetch origin feat/admin-space-editor`; `git merge-tree --write-tree --name-only HEAD origin/feat/admin-space-editor` printed only a tree hash, no file names → **no conflicts**.
- Expected shared files with `design/owner` (`CHANGES.md`, `INDEX.md`, `Flows - states.html`, `README.md`) do not apply: that branch is not on `origin`. When it lands, the second to merge rebases per plan §5 (keep both `CHANGES.md` sections, renumber the INDEX section, move board `top`s, sum README's count).

## Departures from the plan

1. **`LinkSent` (with `maskEmail`) was defined in commit 1, not commit 2** — §3.0's own rule ("built in the commit that first needs them"): commit 1's rebuilt forgot `sent` step *is* 3.2's block. Commit 2 therefore only wires `onOtherEmail` + the focus effect (and keeps the `?email=` prefill built in commit 1). Consequence: commit 2's file list has no `masaha/auth.jsx` (nothing changed there in commit 2).
2. **Forgot `?email=` prefill landed in commit 1** as part of the above (needed for the masked display); strictly a C3 piece one commit early.
3. **Commit 7 carries two minimal guards** the plan assigns to commit 8's `ReportItem` rework (`r.message &&` on the length check; `s && s.verified` on the reply label): without them the new messageless/unlisted reports blank the page in commit 7. Commit 8 replaces both with the specified implementation.
4. **Screenshot pipeline**: CDP with device emulation instead of headless-Chrome CLI (the CLI fakes overflow at 390 — see *Problems met* 3). Coverage actually taken: every commit's frames at 390+1440 Arabic-light (+768 for Settings/Favourites/Reports); English and dark only spot-checked (6 shots), not the plan's full ar/en × light/dark × 3-width matrix.
5. **`problem === 'exists'` stays in Register's init list** (plan-literal) although nothing renders it anymore; harmless.
6. **`PasswordForm` keeps the demo's wrong-password submit failure** (pre-existing behaviour; the plan is silent on it).
7. PR created via `gh api` + `gh issue edit` instead of `gh pr create` (tooling failure, same resulting PR content, body from the plan's `PR_BODY.md`).
8. The 19 extra before-files (§ *Anything unexpected*): kept, not committed.

## Q1–Q3 as answered

- **Q1 yes** (`Space details.html` in this batch): AC-018's report-variant line («سجّل الدخول لتجد الردّ على بلاغك في «بلاغاتي».»), `?dialog=signin-report` handling, and the `?fav=1&fail=fav` failure toast with «إعادة المحاولة» (F11, F12; verified by eye). No Q1-no `CHANGES.md` sentence.
- **Q2 yes** (`Directory.html:353`): the map's picking card now reads «… نرتّب المساحات حسب المسافة منه، ويُرسَل مقرَّبًا ولا يُحفظ.» / «… We sort the spaces by distance from it; it is sent rounded and never stored.» (verified by eye; grep for the old promise is empty).
- **Q3 yes** (AC-020 in the prototype's `auth.jsx`): fourth `PASSWORD_RULES` entry (`bytes`, 72 UTF-8 bytes, `onlyBroken`), shown only once broken in `text-destructive` with `ACircleAlert`; `DEMO.toolong` (40 × «ب» + «1» = 81 bytes) and `Register.html?state=toolong` (verified by eye); INDEX parameter row added; `CHANGES.md` AC-022 row carries the Q3 appendage.
- **S1–S10**: built as written; DI-30 recorded (dashboards' `RateLimitNote` untouched) and listed in `CHANGES.md` › *Notes* with DI-31, DI-32.
