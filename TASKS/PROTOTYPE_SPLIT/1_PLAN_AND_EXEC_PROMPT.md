# PROTOTYPE_SPLIT — move the design archive out of the production repository — PLAN, STOP, then EXECUTE

You are a **Claude Code worker** on **Masaha** (a bilingual Arabic RTL / English platform for coworking spaces in
Gaza), a fresh session, **Opus 5.5, effort high**, started in **`C:\dev\masaha\app`** (on `main` `f073decb`, clean,
**live in production**: every merge to `main` deploys). The owner's decisions are binding:
**`C:\dev\masaha\workspace\TASKS\PROTOTYPE_SPLIT\0_OWNER_DECISIONS.md` (P1–P6) — read it first, whole.**

This item touches the production repository's documents and configuration and creates a **public** repository. Work
slowly and verify every step; when unsure, stop and ask rather than guess.

## Hard limits (the whole item)

- **Phase 1 is read-only:** no branch, no file written outside `C:\dev\masaha\workspace\TASKS\PROTOTYPE_SPLIT\`, no
  `gh repo create`, no push. **It ends with a saved plan and a STOP** — the owner approves it in this conversation.
- Never push to `main`, never merge, never force-push a branch that is not yours, never `git add -A` / `git add .`.
- **Nothing is deleted from `masaha` before the new repository is verified** (its tree identical to the archive's,
  below) **and pushed**.
- No secret printed. Never write the university, the supervisor or the defence anywhere (the project's identity rule).
- No tool attribution in commits, PRs or files. Commits: Conventional, subject ≤ 50 characters, with a body.
- No scratch worktrees or trial copies in Phase 1; the only new folder is `C:\dev\masaha\masaha-prototype` in Phase 2.
- Heavy commands (lint, typecheck, build, a test lane) only through the grant script:
  `node C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs split <command…>`. A run killed for memory: retry
  once, then CI judges.

## Phase 1 — read, inventory, plan (read-only)

**Read:** `CLAUDE.md`; `docs/README.md`; `docs/architecture/documentation.md`; `docs/development/workflow.md`;
`docs/design/README.md`, `INDEX.md`, `SCREENS.md`, `CHANGES.md`; `docs/design/prototype/BRIEF.md`;
`docs/design/scripts/*`; `docs/architecture/decisions/` (the ADR format; the next is **0020**); the findings README.

**Inventory — what the supervisor measured (verify each, find what he missed):**
- `docs/design/`: `prototype/` (117 files, 7.5 MB, 86 commits since 2026-09-30), `screens/` (437 files, 17 MB),
  `scripts/` (`check-parse.mjs`, `check-classes.mjs`), `README.md`, `INDEX.md`, `SCREENS.md`, `CHANGES.md`.
- Pointers into it from outside: `CLAUDE.md:71` (*Design archive*), `docs/README.md:79`, `.prettierignore:8`,
  `eslint.config.js:248`, `apps/api/scripts/checkLinks.ts:175` (`NOT_SCANNED`),
  `apps/web/src/shared/design-system/components/display/Logo/drawing.ts:2` (a comment), and the documents citing
  `design/prototype` or `docs/design/` — at least `foundation.md`, `features/directory.md`, `finance.md`, `visits.md`,
  `payments.md`, `audit.md`, and findings 14, 19, 37, 73, 74, 96, 110, 165, 215 and the findings README. Use
  `git grep -n -i "docs/design\|design/prototype\|design archive\|prototype"` and judge each hit: a pointer to move,
  a word that only means "the design" (leave it), or a test comment (leave it unless it cites a path).

**Decide in the plan (with the owner's P1–P6):**
1. **What moves.** The supervisor's recommendation: **the whole `docs/design/`** (the prototype, the screens it was
   drawn from, its scripts and its four documents) — one home for the design archive. Say if anything must stay, and
   why.
2. **How the history moves:** `git subtree split --prefix=docs/design` (or `git filter-repo --subdirectory-filter` on
   a fresh clone) into `C:\dev\masaha\masaha-prototype`. **The proof:** the new repository's `HEAD^{tree}` equals
   `git rev-parse main:docs/design` — byte-identical. The archive's relative links and the prototype's relative script
   paths keep working at the new root (check `scripts/*.mjs` paths).
3. **The history scan before going public (P2)** — over **every commit** of the split history, not only the tip:
   - secrets: keys, tokens, passwords, connection strings, `.env` content;
   - personal data: real phone numbers and e-mails (the brief says placeholders only — confirm), names of real people;
   - the identity rule: list every hit of `university|جامعة|supervisor|مشرف|defen[cs]e|مناقشة|graduat|تخرج|thesis|
     college|كلية|course|مساق|instructor|دكتور` with its commit and file — **list them for the owner; do not judge them
     away.**
   Note: `masaha` is already public, so this history is public today (P5) — still report.
4. **The new repository's own documents (P4, P6):** `README.md`, `CLAUDE.md`, the updated `BRIEF.md`, `decisions/`
   — draft their outlines in the plan. `CLAUDE.md` says: the original page is never edited; every idea is a variant
   `<Page>.html?v=<name>`; the switcher; the production repository is the one home of product facts, read-only (paths
   to its key documents); the fixed points (ink + berry and the logo — ADR 0019 and foundation §16 in `masaha`;
   Arabic first; v1 scope and *Not in v1*; no fake data — no ratings, no seat counts); what a variant may change
   freely (layout, type scale and typeface as a proposal, spacing, surfaces, imagery, motion), each change stated in
   the page's decision file; how to run it; commits straight to `main` of that repository, Conventional, no
   attribution.
5. **The variant mechanism (P6):** how a page reads `?v=` and how the switcher lists the original and its variants,
   in the prototype's existing style (it already reads `?identity=`, `?demo=`, `?prices=`; Babel globals are shared
   across scripts — never a top-level `name`, see `check-parse`). Mechanism only, no variant designed.
6. **The removal PR in `masaha`** (branch `chore/design-archive-out`, expected **#147** — check): delete
   `docs/design/`; repoint each pointer to the public repository's URL
   (`https://github.com/Basel-Ghonaim/masaha-prototype/blob/main/<path>`) or reword it; drop the exclusions that
   existed only for the archive (`.prettierignore`, `eslint.config.js`, `NOT_SCANNED` — confirm nothing else needs
   them); **ADR 0020** (short, decision-level: why the design archive and prototype live in their own repository,
   what stays the source of truth where, how a chosen design reaches production); `CLAUDE.md`'s *Design archive*
   line and `docs/README.md`'s entry; any *Deferred documents* trigger. The commits (e.g. the ADR first, then the
   move). `#PRNUM` replaced just before the push.
7. **Verification of the PR:** `npm run lint`, `typecheck`, `format:check`, `check:links`, `check:conflicts`,
   `check:classes`, `build` then `check:build` (production build: `NODE_ENV=production`). Test lanes: if no file
   under `apps/` or `packages/` changes beyond comments, they may be left to CI — say so; otherwise run them.
8. **Risks and the rollback** (e.g. the PR reverted while the new repository stays).

**Save the plan** as `C:\dev\masaha\workspace\TASKS\PROTOTYPE_SPLIT\2_PLAN.md` (English): the inventory with every
pointer and its fate, the decisions above, the scan's results, the commit list for both repositories, the
verification, and a *Proposed alternatives* section if you disagree with a decision. **Then STOP** and say in the
chat that the plan is ready. Wait for the owner's word.

## Phase 2 — execute (only after the owner approves the plan)

1. **The new repository, locally:** create `C:\dev\masaha\masaha-prototype` with the split history; prove the tree is
   identical; add the documents of P4 and the variant mechanism of P6 as their own commits; run `check-parse` and
   `check-classes` from their new place; serve it once (`python -m http.server <free port> --directory
   C:\dev\masaha\masaha-prototype` — if your session refuses to start a server, say so and go on) and load a page
   with and without `?v=` to see the switcher; stop the server by PID.
2. **Publish:** `gh repo create Basel-Ghonaim/masaha-prototype --public --source C:\dev\masaha\masaha-prototype
   --push` — **only if the plan's scan was approved**. Confirm with `gh repo view`.
3. **The removal PR** in `C:\dev\masaha\app`: branch from the latest `main`, the commits of the plan, the
   verification of §7, push, open the PR with the `open-pr` skill (Evidence: the tree-hash proof, the scan's summary,
   the new repository's URL). Wait until `gh pr checks <n>` is all green on the pushed head and GitHub says `CLEAN`.
4. **Report** `C:\dev\masaha\workspace\TASKS\PROTOTYPE_SPLIT\4_REPORT.md`: the new repository (URL, head, commits),
   the tree-hash proof, the scan, the PR (number, full head sha, commits, files), what ran and what CI judged, every
   decision you took, anything left. **Stop. Never merge.**
