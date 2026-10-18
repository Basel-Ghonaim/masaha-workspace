# H-1 — Housekeeping: resolve five findings (tests, docs, cache, format, dev ports)

**Worker B** · worktree `C:\Users\basel\masaha-b` · branch `chore/resolve-five-findings`, cut with
`git fetch --prune origin` then `git switch --no-track -c chore/resolve-five-findings origin/main`
(the worktree is detached at `origin/main`, clean, after PR #43's merge).

**Size cap:** at most 2 subagents in total, and **no self-review subagent** (an independent review
follows the PR). Do not run any workflow. This is a small item: read only the files and sections
each finding names; don't sweep the repository.

## 1. How to work

- **Start with the `start-work-item` skill.** Plan in plan mode before writing code.
- **Read** `docs/architecture/findings.md` entries **26, 28, 29, 30, 31, 34** in full; they own the
  evidence and the "Resolves when" of each item below. Then only the files and document sections
  those entries and this prompt name.
- **When finished, follow the `open-pr` skill.**
- **The owner's rules:**
  - honest test titles; tests stub the platform's seams, never `vi.mock` of a module;
  - **no parameter, option or callback that only tests pass or that nothing uses**;
  - **checks:** lint and typecheck on each commit; the lanes below once on the head, one at a time;
    don't re-run a lane that already passed on unchanged code;
  - commit subjects of 50 characters or fewer; report only once CI is green on the pushed head;
  - review fixes fold into their commits, with ONE "Review fixes" comment;
  - **rebase only on a real conflict:** if GitHub shows the PR `CLEAN`, don't rebase on `main`;
  - no tool or AI attribution anywhere.

## 2. What this item delivers

One pull request, **five commits, one per finding group**, each resolving its finding(s) in
`findings.md` (status, date, and a line saying how) in the same commit as its change. No production
behaviour changes except item 3's cache hardening; no migration; no new dependency.

## 3. The proposed decisions

These came out of the analysis and the owner approved them, **but they are proposals, not orders.**
If you find a stronger option for any of them, put it in your plan under a dedicated section,
**"Proposed alternatives"**, with its trade-off and your recommendation. The owner and the analyst
weigh it; build an alternative only once it is approved.

1. **Finding 28 — the tests that wait for a lazy page.** The cause: Testing Library waits 1 s by
   default (`asyncUtilTimeout`), and on the owner's machine, under a full run, Vite's first transform
   of a lazily imported page can take longer. **Raise the wait once, for the component lane**, in
   `apps/web/src/test/componentSetup.ts` (5 s is the proposal), with a comment saying why. No
   per-test timeouts, no production change. **Proof:** two consecutive full `test:component` runs on
   this machine with no failure (report both counts), as the finding asks; then resolve it.

2. **Findings 31 and the rebase rule — the documents follow the owner's rules.**
   - `docs/backend/conventions.md` §2 (dependency injection) and R8, and
     `docs/development/testing.md` §3 rule 3: a service creates its own repository; the composition
     root passes only real dependencies (the transaction runner, the audit writer, lower modules'
     services, ports); logic worth unit-testing lives in pure helpers; the API lane proves services
     on the real database. Say the older services still inject a repository and follow in the
     planned refactor. Resolve finding 31.
   - `docs/development/workflow.md` §9 (and any other line that says "rebase before opening a PR"):
     a PR is rebased on `main` only when GitHub shows a conflict; if it is clean and CI ran after
     main's last change, it is left ready for review.
   - **Finding 30 is accepted by the owner** (the lists are small and the admin sees them whole):
     mark it *Accepted* with that reason, in this commit.

3. **Finding 34 — passwords in the mutation cache.** Set `gcTime: 0` on the sign-in, registration and
   password-change mutations (`features/auth` and `features/users`), each with a comment saying why,
   as `useGoogleSignIn` and `useCheckResetLink` already do. Extend each hook's existing test: once the
   mutation is answered and its page has gone, the cache holds no password. Resolve finding 34.

4. **Finding 26 — a format check that doesn't write.** Add `format:check` (Prettier's check mode,
   same file set and ignores as `format`, Markdown still excluded). Point setup.md and CLAUDE.md's
   *Commands* list to it (one line each). **CI is not changed** in this item: if the repository isn't
   clean under `format:check` today, say so in the PR and record it, don't reformat files here.
   Resolve finding 26.

5. **Finding 29 — dev ports from the environment.** The web's dev port and its `/api` proxy target
   are read from the web's own environment file (for example `WEB_PORT` and `API_PROXY_TARGET`, read
   in `vite.config.ts` with `loadEnv`; **not** `VITE_`-prefixed, so they never reach the browser
   bundle), defaulting to today's 5320 and `http://localhost:3320`. Check how the API's port and
   `CORS_ORIGIN` are set and keep them per folder. `apps/web/.env.example` documents the two keys;
   setup.md gains a short "Running a second folder" note (a worktree sets its own ports in its own
   `.env` files). The worktree's own `.env` files are not committed. Resolve finding 29, and say in
   the PR that the scratch Vite configs are no longer needed.

**Not in this item (left open, each for its own item):** findings 8, 10, 11, 14–18, 20–25, 27, 32,
33, 35.

## 4. Your plan decides

- the exact wait (justify the number from what you measure), the env keys' names, the wording of the
  document changes (short; summarise and link, one owner per fact);
- the tests: item 3's three hook tests; for item 5, whether a unit test of a small pure helper that
  reads the env fits, or the config is checked by a manual run only (say which);
- the commit subjects (≤ 50 characters), for example `test(web): wait longer for lazy pages`,
  `docs: align the rules on rebase and injection`, `fix(auth): drop passwords from the cache`,
  `chore: add a format check that doesn't write`, `chore(web): read dev ports from the env`.

## 5. Checks

- Lint and typecheck on each commit.
- On the head, once each, one at a time: `check:classes`, `test:unit`, **`test:component` twice in a
  row** (item 1's proof), `build` + `check:build` (item 5 touches `vite.config.ts`). Skip `test:api`
  locally (no API change); CI runs every lane.
- **Manual for item 5:** start the web from this worktree on its own ports, against this worktree's
  API, with no scratch config, and check one page loads data. Then stop every process you started,
  and confirm the ports are free (a `tsx watch` can survive Ctrl+C on Windows; finding 29).

## 6. Parallel work

Another worker may be working in the main folder at the same time.
- **Declare in your plan every shared file you will edit** (for example `findings.md`, workflow.md,
  conventions.md, testing.md, setup.md, CLAUDE.md, the root `package.json`, `vite.config.ts`,
  `apps/web/.env.example`), and edit each minimally.
- If a conflict appears later, the PR is rebased then, keeping both sides.

## 7. Pull request

- **Title:** `chore: resolve five findings` (or similar).
- **Labels:** `chore`, `area:web`, `area:docs`. Assigned to the owner.
- **The description:** each finding, what changed and its proof; what was not run.
- **Review:** a light independent review, after you report.
- After CI is green on the pushed head, stop and report: the head, the commits, the counts (both
  component runs), your tokens. Don't merge. Don't create an Issue.
