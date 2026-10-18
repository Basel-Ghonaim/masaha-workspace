# Masaha — analyst handoff (updated 2026-10-02)

You are taking over as the owner's **analyst and control room** for Masaha. The previous analyst conversation ran out of context. Read this whole file first, then CLAUDE.md, then `docs/development/workflow.md` (especially §9 Parallel work), then `docs/README.md`.

- **Language:** speak **Arabic** with the owner. Write every prompt for workers in **English**.

## 1. Your role

You do NOT build. Workers build. The owner merges. You:

1. **Write each Work Item's prompt** to `C:\Users\basel\Downloads\<ITEM>_PROMPT.md`.
2. **Review each worker's PLAN before the owner approves it.** The owner pastes the plan, or screenshots of plan-mode questions. You explain them in Arabic: what the question means, the options, a clear recommendation with reasons. Then you give a paste-ready English reply for the worker.
3. **Review each PR yourself before merge.** Read the branch with `git show` / `git diff origin/main...origin/<branch>`, `gh pr checks`, and `git merge-tree --write-tree` against `main` and the other open branch. Never trust a worker's report alone; verify the important claims in the code.
4. **Explain code to the owner** when asked, in plain Arabic. The owner is strong in React and TypeScript, newer to backend work and to Zustand.
5. **Hold the blueprint:** the waves, who works on what, what is next. It is NEVER written into the project docs, because it goes stale.
6. **Never edit the project yourself.** Never merge. Never create Issues. Read-only git commands are fine.

## 2. Working method (proven; keep it)

- **Two workers:**
  - **Worker A** works in the main folder `C:\Users\basel\masaha`, with the databases `masaha_dev` and `masaha_test`. It carries the critical path.
  - **Worker B** works in the long-lived worktree `C:\Users\basel\masaha-b`, detached at `origin/main` between items, with its own databases `masaha_b_dev` and `masaha_b_test`. Each item cuts its own branch: `git switch --no-track -c <branch> origin/main`.
  - The stable rules are in workflow §9.
- **One Work Item = one fresh conversation.** Fixes and rebases for the same PR stay in its conversation. The exception: if that conversation's context is too full, a new conversation continues the same PR from a progress note.
- **Every prompt has:**
  - a mandatory "How to work" section: read CLAUDE.md, workflow.md and README; work in PLAN MODE; checks before planning (the folder, a clean tree, HEAD at origin/main);
  - the worker and its folder;
  - a "Parallel work" section: the other worker's files, the shared files and which section each side owns, "rebase before the PR; whoever merges second rebases and keeps both sides", and the lockfile rule (take main's `package-lock.json`, then `npm install`, never hand-edit it);
  - the PR rules: labels, `--assignee @me`, the workflow §3 template, no AI attribution, don't merge.
- **SIZE CONTROL (a hard lesson).** Every prompt states a cap: "use at most 4 subagents; no workflows." A review prompt without a cap, under `ultracode`, fanned out to 9 and then 29 agents and burned about 4.4M tokens. Advise the owner to keep `ultracode` off unless they want maximum fan-out.
- **The review gate** for large or security-sensitive items: two independent reviews (≤ 4 agents each), then ONE merged fixes list that you verify in the code. Fixes go to the item's own conversation.
- **The PR record after fixes:**
  - update the PR description to the final state;
  - add ONE comment, "Review fixes": a table of each item, its severity, and the commit that fixed it, or "not done" with the reason.
- **After every merge:**
  - in the main folder: `git pull`; after a schema change, also `npm exec -w @masaha/api -- prisma generate`, then `prisma migrate deploy` (and `db:seed` if needed);
  - worker B: back to detached `origin/main`, and the owner deletes the merged branch.
- **Screenshots** for UI work go to `C:\Users\basel\Downloads\<item>-shots` and are never committed.

## 3. The owner's standing preferences (also in memory)

- **Screen ≠ capability:** a value belongs to the capability whose rule consumes it.
- **ADRs** are short and decision-level, with no file names.
- **The build map** has no implementation details, targets not dates, and is a direction, not a contract.
- **From Quick Tweets** (`D:\quick-tweets-app`): take the strength and the ideas, rebuilt inside Masaha's rules; never copy-paste.
- **Every decision** is presented with its options and a recommendation. The owner decides architecture and scope.
- **Quality over speed:** engineering quality is part of the graduation deliverable. The defence is by **16 January 2027**, the only fixed date; everything else is a target.

## 4. State on 2026-10-02

**`main` = `5b6302c`.** Merged so far:

| PR | Item | What it did |
|---|---|---|
| #17 | ADR 0011 | One web app |
| #18 | A-1 | ADR 0012 (modular monolith, levels L0–L5), ADR 0013 (sessions / users / auth), conventions rewrite, design archive in `docs/design/` |
| #19 | A-2 | The `space_settings` and `space_occupancy` tables |
| #20 | A-3 | ADR 0014 (Vercel + Neon on free tiers, with a deviations list), ADR 0015 (idempotency and concurrency), ADR 0016 (dashboard URLs) |
| #21 | DS-1 | Design-system category folders (actions, fields, display, data, feedback, overlays, navigation); the showcase's three views |
| #22 | P-1 | The build map in `docs/plans/v1-mvp.md`, steps 1–12 |
| #23 | Finding 9 | The Vitest drive-letter hook |
| #24 | P-2 | Workflow §9 Parallel work |
| #26 | F-6a | `shared/preferences` (Zustand, no persist middleware; plain-string keys `masaha.language` / `masaha.theme`; three theme choices, light, dark and system; cross-tab sync; derived from `CATALOGUES` / `THEMES`) and `app/providers.tsx` (`AppProviders`) |

**Worker A: F-5a, the authentication API.** PR #25, branch `feat/auth-api`, was 10 commits ahead of `main` and 8 behind.
- It went through the review gate: two reviews, plus the analyst's verification.
- The ONE fixes list is `C:\Users\basel\Downloads\F5A_FINAL_FIXES.md`. The owner approved all its decisions, D1–D12.
- The detailed review it refers to is `F5A_REVIEW_2.md`. The superseded list is `F5A_REVIEW_FIXES.md`; don't use it.
- The worker was told:
  - rebase on `main` first;
  - fix the blockers first (B2 needs S5 first);
  - if its context passes 75%, stop at a commit boundary, push, and write `C:\Users\basel\Downloads\F5A_PROGRESS.md`;
  - when done, update the PR description, add the "Review fixes" comment, and stop.
- **Your next action on F-5a:**
  - when the worker reports (or `F5A_PROGRESS.md` appears), re-check the fixes against `F5A_FINAL_FIXES.md` in the code;
  - check CI;
  - advise the merge.
  - **The Arabic copy for any new error codes** (from D1 or D3) needs the owner's approval in that PR.
- **After F-5a merges,** the owner must add `JWT_SECRET` (≥ 32 characters) to their `apps/api/.env`, or the API won't start.
- `F5A_WALKTHROUGH.md` (in Downloads) is an Arabic explanation of what F-5a built, written for the owner. It describes the state before the fixes.

- **Progress at handoff:** the worker had rebased locally and committed S5 (`refactor(api): accept tx in every repository call`); the rate-limit fixes (B1) were uncommitted in the tree. Nothing was pushed yet: `origin/feat/auth-api` was still `e56664f`.

**Worker B: free.**
- Its worktree still needs cleaning after F-6a: `git fetch --prune origin`, `git switch --detach origin/main`, and the owner deletes `feat/preferences`.

**Environment:**
- `masaha_dev` was migrated to all 8 migrations on 2026-10-01. F-5a will add one more: `rate_limits`, plus `family_id` on refresh tokens.
- The owner's databases are `masaha_dev`, `masaha_test`, `masaha_b_dev` and `masaha_b_test`.

## 5. Pending — the owner had not answered yet

The analyst proposed the next waves, and these four questions are open:

1. **Finding 10** (the amenity icons in the design system) for worker B now? Recommended: yes.
2. **Split the rest of F-6:**
   - **F-6b**, the public shell: header and footer, with the language and theme toggles on top of F-6a, and the 404 / error / offline pages. It doesn't need the session, so worker B can run it parallel to F-5b.
   - **F-6c**, the dashboard shells: space and admin, the sidebar, the space switcher, the role guards per ADR 0016, and the account settings page with the theme select.

   Recommended: yes.
3. **F-7, the first deployment,** for worker B, parallel to F-6c. It is possible once sign-in works end to end, after F-5b. Recommended: yes.
4. **Discuss and decide, BEFORE the F-5b prompt:**
   - do frontend features export UI, or hooks only, with pages composing? The owner's previous project used hooks only, and a mixed approach is possible;
   - where do components that combine several features live (for example the desk dialogs)?

   F-5b creates the first feature (`features/auth`), and its shape becomes the pattern.

**The proposed sequence:**
- **Now:** A finishes the F-5a fixes; B does finding 10; the owner and you decide item 4.
- **After F-5a merges:**
  - A does **F-5b**, the web auth: the ports 5320/3320 with strictPort, the Vite `/api` proxy, the Axios client with single-flight refresh reading the session store from outside React, `AppError` with `requestId`, `shared/session` (Zustand), the `RequireRole` guards, screens 5, 6, 7 and the forced change, the reset page reading `#token` then clearing it, and the deferred `system-overview.md`. New dependencies for approval: axios, @tanstack/react-query, react-hook-form. Run the review gate.
  - B does **F-6b**.
- **Then:** A does **F-6c**; B does **F-7**.
- **Then:** the build map's step 2 onward (the build steps).

## 6. Decisions already recorded (don't re-open)

- **The backend:**
  - modules by capability in levels L0–L5;
  - imports go only downward and only through `index.ts`, enforced by ESLint;
  - orchestrators own the transactions (`runInTransaction` in `db/`);
  - ports only for infrastructure;
  - read models read, never write.
- **The frontend:**
  - zones `app → pages → features → shared`;
  - features never import each other;
  - capability names match the backend modules;
  - one web app with two dashboard shells (ADR 0011, 0016).
- **Client state is Zustand** for `preferences` (built) and `session` (F-5b). One mechanism.
- **Deployment (ADR 0014):** Vercel plus Neon, one origin, the deployment adapts to the architecture, and every free-tier difference is listed for a future paid host.
- **Email:** nodemailer plus Gmail SMTP behind a port, using the owner's own Gmail temporarily (a Masaha account later, by configuration only).
- **Library candidates by build step** (each needs approval when its step comes):
  - date-fns and @date-fns/tz (time);
  - sharp, plus storage or multer (photos, step 5);
  - libphonenumber-js (customer phones, steps 7–8);
  - CSV with a UTF-8 BOM (step 11);
  - a map library (step 2);
  - charts (step 11).
- **Open findings:** 8, 10, 11, 14, 15, 16–19, plus those F-5a adds or corrects.
- **Rejected (don't propose again):** NestJS, auth frameworks (Better Auth and the like), CASL, Redis, an event bus, Postman/Newman as a test layer (the API lane covers it; an optional Bruno collection near the defence is fine), and a generic channel-verification layer.

## 6b. Hard rules

- **No AI attribution** anywhere: commits, PRs, docs. Never `git add -A`. No Issues unless the owner asks. Merging and deleting branches are the owner's alone.
- **Reviewers are read-only** and pinned to a commit: no edits, commits, checkouts, installs, database commands, test runs or GitHub comments.
- **Secrets:** never ask for the Gmail app password. It lives only in `apps/api/.env` (and later in Vercel's environment). Never send the owner's email address to any service.
- **Every new dependency** needs the owner's explicit approval.

## 7. Files in Downloads

- Prompts: `A3_PROMPT.md`, `DS1_PROMPT.md`, `F5_PROMPT.md`, `F9_PROMPT.md`, `P1_PROMPT.md`, `P2_PROMPT.md`, `F6A_PROMPT.md`, `F5A_REVIEW2_PROMPT.md` (all done).
- F-5a: `F5A_FINAL_FIXES.md` (active), `F5A_REVIEW_2.md`, `F5A_WALKTHROUGH.md`, and `F5A_REVIEW_FIXES.md` (superseded).
- This handoff.

## 8. First thing to do

1. Confirm to the owner, in Arabic, that you've taken over: summarise the state in a few lines and list the pending decisions from §5.
2. Ask which to start with. The likely order: answer §5 items 1–3, then discuss item 4 while the workers are busy.
