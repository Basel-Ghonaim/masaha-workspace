# Review — ANNOUNCEMENTS PR 3 (`feat/favorites`, #121), one independent reviewer (Claude Code)

You are the **independent reviewer** of worker B's favourites PR in Basel-Ghonaim/masaha (build map step 10,
PR 3 of 4): a signed-in user saves a publicly listed space (`POST /me/favorites/:spaceId`, 204, idempotent, at
most `FAVORITES_MAX` = 200 under the user's row lock, `FAVORITES_LIMIT_REACHED` 409), removes one (`DELETE`,
204 whether saved or not), and reads them whole (`GET /me/favorites`, in `directory`: a listed space as the
directory's card with its live status, one that left with `listed: false` and its name; `sort=distance` with
`Masaha-Near`, nearest first, `Cache-Control: no-store`). No migration. It opens with items carried from #120's
review (the data-reports router renamed `me`, document fixes, finding 150 recorded as accepted). **Authorization,
privacy (a user's location) and a transaction:** trust nothing you have not seen in the code. Find the PR: `gh
pr view 121 --json number,headRefOid,mergeStateStatus` (head expected `91d9b27f`). Write the report to
`C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\6_REVIEW_PR3_CLAUDE_CODE.md`. **Work alone — no subagents.**
This is a review, not a Work Item: run no project skill, no branch.

## Rules

- **Read only, from `C:\dev\masaha\app-design`, commit objects only:** `git fetch origin` and `git fetch origin
  pull/121/head`; base = `origin/main`; **pin every read to the head's sha** (`git show <sha>:<path>`, `git diff
  origin/main...<sha>`; another process's fetch may overwrite `FETCH_HEAD`). No edits, checkout, switch or reset,
  no installs, no npm or test runs, no servers, no database commands, no comments on GitHub. The only file you
  write is the report. A `git` command failing on a `.lock` file: wait 30 s, retry once.
- First `gh pr checks 121` — a red or pending check: say so and stop. At the end, `gh pr view 121 --json
  headRefOid` again: say whether the head moved.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario (inputs →
  wrong result), severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say
  what you saw in the code and what you only read in the executor's report.** No praise, no tool attribution.
- Think like: a user reading or removing **another user's** favourites (ids in the path, the list's filter); a
  user filling the ceiling with two tabs at once at 199; a user saving a hidden, deleted, unverified, or
  inactive-area space, or one that is listed now and hidden a moment later; a space restored after deletion; an
  anonymous caller; **a user's point (`Masaha-Near`) leaking** — cached by a proxy or the browser (on a 200, a
  401, a 422), logged, or echoed; a card carrying a capacity or a count the directory never shows; a
  reception session idle-bound since #118.

## What to read

1. The project's rules: `git show origin/main:CLAUDE.md`.
2. The plan `C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\2_PLAN.md` — **the owner's approval note at its top
   binds** (Q1's code, Q9's distance rule) — and for PR 3 only: §2 *Scope* and *Acceptance criteria*; §4
   decision 12, D1–D2's PR 3 parts, D9, D13, D15's PR 3 part; §5 S9, S12; §9 *PR 3* (U1, T1–T10, breaks B1–B9)
   and *Not tested, and said*; §12.2's PR 3 checks; Appendix A *PR 3*.
3. The carried file `0_CARRIED_FROM_120.md` (same folder; items 1–5) and, for its items, findings 1–5 of
   `6_REVIEW_PR2_CLAUDE_CODE.md` (same folder).
4. The executor's prompt `3_EXEC_PROMPT_PR3.md` and report `4_REPORT_PR3.md` (same folder): judge **every
   departure** — `now` in favourites' dependencies; `no-store` set **before** `requireAuth` on `GET
   /me/favorites`; T7's `GET` added in C2; "site" → "me" also in `data-reports.md`'s placement and code-map
   lines; the carried item 4 left (no commit touched `apps/api/test/app.ts`); **the `Masaha-Near` rule extracted**
   from `GET /spaces`' schema (a shared `checkNear`, the API's `parseWithNear`) — does `GET /spaces` behave
   exactly as before (its existing tests unchanged?); U1's red taken by moving the file aside; lint and
   typecheck not re-run after the docs-only fixup.

## Look hardest at

- **Authorization and ownership:** every route `requireAuth()`; the user is always `req.actor`, never a path or
  body id; `remove` filters by the user (B6); `of` filters by the user (B9); `favorites.manage` (`self`) where
  the plan puts it.
- **The save's transaction:** `users.lockAccount(actor.id, tx)` first; "already saved" answered before the
  listed check and the ceiling (204 at 200 for one already saved); the ceiling counted under the lock (`≥`, not
  `>`); **`isListed` reads through `publicListing.upTo` outside the transaction** — can a race between it and a
  space being hidden matter, and is a unique `(user_id, space_id)` key the backstop for two saves (B2: a 500 if
  the check is removed — is that path reachable without the break)?
- **The list:** whole, newest saved first; a listed space's card equal to the directory's card (the same
  mapper, its live status), no capacity, no count, no owner data; one that left (hidden, deleted, inactive
  area, unverified?) with `listed: false` and its name via `spaces.namesWithDeleted`; by distance: listed nearest
  first, those that left last (`favoritesOrder`).
- **The point's privacy (security › Location):** `no-store` on every answer to a request carrying
  `Masaha-Near` — 200, 401, 422; the header without `sort=distance` → 422 `invalid_choice` on `near`; the point
  never logged (`requestLogging`'s redaction still covers it on the new route) and never answered back beyond
  `distanceMeters` (rounded as the directory rounds it).
- **The extraction:** `checkNear` / `parseWithNear` — `GET /spaces` keeps the same rules, messages and
  `no-store`; one function used by both routes, no copy.
- **`FAVORITES_LIMIT_REACHED`:** 409, in the shared codes, both catalogues, contract §6 — **quote the Arabic line
  exactly in your report** (the owner approved «امتلأت مفضّلتك؛ أزل مساحة أولًا.» in Q1).
- **Carried from #120:** item 1's rename complete (file, factory, `index.ts`, `app.ts`, conventions §7 and §9,
  `data-reports.md`), no behaviour change; items 2–3 true to the code (the decision race: 403 while the owner is
  linked, 409 once unverified; the admin first → the owner's 409); finding 150's file and index line say
  *Accepted* with the option not taken.
- **Tests:** a behaviour the plan names with no test, or a test that would pass with the bug (T2 and T5's races,
  T4's ceiling, T9's `no-store`, T10's other user).
- **The documents:** the contract's *Favourites* section and §4's exception, `conventions.md` (§7, §9),
  `security.md` (*Location*), `favorites.md` (new, the capability template), `directory.md`, `data-reports.md`,
  `v1-mvp.md`, `overview.md`, `docs/README.md` — true to the code, one home per fact, `#121` where the number
  goes.
- **Scope:** `apps/api`, `packages/shared`, `docs`, and the web's two `errors.ts` only; 35 files; no migration,
  no dependency. Commit subjects ≤ 50, each with a body.

## Your output

One file: the head, CI's state and whether the head moved; **a one-line verdict** (mergeable / mergeable after
a fix round / not mergeable); the findings, most severe first, each with **where its fix belongs** under the
owner's rule — **a serious or large fix: a fix round on this PR; a small one: worker B's next PR's first commit
(ANNOUNCEMENTS PR 4, `feat/closure-extension`, through `0_CARRIED_FROM_121.md`); or a finding to record (151 and
on)**; `FAVORITES_LIMIT_REACHED`'s Arabic line quoted; the departures, each judged; a short "Checked and fine"
list. Then stop.
