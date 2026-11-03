# FINANCE_AUDIT — the audit log, the platform settings and the space's finance, on the API (build map step 11) — PLAN ONLY

**No branch, no checkout, no file edit in the repository, no commit, no install, no test run, no server, no
database command.** You write one file — the plan — then stop.
**No trial build anywhere either:** no temporary copy of the repository, no `git worktree add`, no `git stash`, no
scratch or temp folder holding code, no `node` / `tsx` / `tsc` / `vitest` / `psql` / `npm` run — not in the
repository, not in a scratchpad, not in a temp directory. The only commands are `git fetch`, `git show`, `git log`,
`git ls-tree`, `git grep`, `git diff` between commits, read-only `gh`, and reading files. Where you are unsure that
something works, write it in the plan as **a check the executor makes first, with what to do if it fails** — never
try it yourself. Read only the files the plan needs, each once.

**This is a planning task, not a Work Item's start:** do not run `start-work-item` (it cuts a branch) and do not stop
on the worktree being detached. If you are Claude Code: use `write-plan` for its discipline only (save the file; no
plan-mode step is needed).

**The task's folder:** `C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT\`. This prompt is `1_PLAN_PROMPT.md`; **save
the plan as `2_PLAN.md` here**; reports `4_REPORT_PR<n>.md`.

**Where you read.** `C:\dev\masaha\app-design` — commit objects only: `git fetch origin`, then `git show
origin/main:<path>`, `git ls-tree`, `git grep origin/main`. Never check anything out, switch or reset it (its working
tree is old; reviewers read there too). If a `git` command fails on a `.lock` file, wait 30 s and retry once. Worker
A's `C:\dev\masaha\app` and worker B's `C:\dev\masaha\app-b` — never work there.

## 0. The base and what runs beside it

Plan from today's `origin/main` (write its sha in the plan's header). **#123** (ANNOUNCEMENTS PR 4, the closure
extension) merges on the owner's word: if it is not on `origin/main` when you start, read its head
`origin/feat/closure-extension` (`ff8743c8`) as merged — it only adds — and say so in the header. **Beside it:**
- **Worker A** finishes DESK_SCREENS PR 4 (#124's fix round: `apps/web`, `docs`), then its next web items (the public
  site's fix PR; later the screens of steps 9–11). Name every file this item shares with web work as a likely text
  conflict — at least the web's two `errors.ts` catalogues and the shared documents.
- **Finding numbers:** worker B's range — **151** is the carried file's (resolved by PR 1); this item's own start at
  **152**.

## 1. The plan must stand alone

Fresh Claude Code conversations execute each PR, and another Claude Code conversation reviews each (one reviewer, no
subagents). Every decision with its one-line reason; the files; each route, query, schema, service function,
transaction and type with its interface; each new error code (through the `add-error-code` skill's steps, written so
an executor without that skill follows them); each test with its lane, title and the break that must make it fail
(`docs/development/testing.md` §3 — **every break run and its red output recorded**); **each permission (owner,
reception, admin, another space's staff, a stranger), each money figure, each privacy rule (the admin never sees a
space's customers, visits, subscriptions or payments) and each race gets a deliberate break**; the commits, subjects
counted (≤ 50); fixes before the push folded (`--fixup` + autosquash, `GIT_SEQUENCE_EDITOR=:`); every new decision
and history line ends with its date and `#PRNUM`; the procedure with its commands — as
`WORKER_B\ANNOUNCEMENTS\2_PLAN.md` §12 has them (branches from the latest `origin/main` in `C:\dev\masaha\app-b`,
`--no-track`; `masaha_b_dev` / `masaha_b_test`; `docker start masaha-postgres-1`, never `db:up`, never `npm ci`;
**memory: one full test run at a time on this machine, none while a `vitest` of `C:\dev\masaha\app\` runs, the free
memory recorded before each full lane; a full lane killed for low memory is re-run once when quieter, killed again →
CI's run on the pushed head judges**; per commit `lint` + `typecheck` and the touched test files; on the head once
`test:unit`, `test:api` (no command timeout: ≈ 10 minutes), `format:check`, `check:links`, `check:conflicts`, and
`npm run build -w @masaha/shared` if the shared package changes; **fix rounds run only the touched test files, never
a full lane — CI judges** (the owner's rule, 2026-10-26); **each schema change** (an index for the aggregates
included): a migration by `migrate dev --create-only` run **once** — then the executor checks the folder;
non-interactive or on data loss: `migrate diff --script` — **no PR number in a migration's SQL**, and both B
databases migrated; a real run on 3321 with the demo data, a self-judging script (`PASS|FAIL`, `ALL PASS`) that
**never keeps an `/auth/` request's body** (a demo account or data that does not hold what a case needs → **not
performed, with why and its test** — never change data through the app to get past it; the run's own writes named);
`#PRNUM` replaced per commit tree by a self-checking script (the ANNOUNCEMENTS folder's `scripts\` holds the model)
and **checked against the number `gh pr create` answers** (worker A may open a PR meanwhile); push; `gh pr create
--assignee @me --label feat --label area:api --label area:docs` (`area:web` if the catalogues change); `gh pr
checks` and `CLEAN`; the conflict check); the executor's rule: **a test it cannot run is recorded with its exact
error, the rest continues, CI judges** — never skipped, `.skip`ped or weakened; **never leave silently** (a carried
item or a review nit undone is said); **no stop for the file count** — the count is reported (the owner's rule,
2026-10-26); the executor's scripts in this folder's `scripts\`, never committed; an appendix mapping steps to
Claude's skills, "only a map". Never merge; no tool attribution; stage by path.

**Carried items — PR 1 opens with them:** `C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT\0_CARRIED_FROM_123.md`
(items 1–4, decided by the owner — item 1 is **finding 151, the owner's option A: the extension moves a covered
subscription's not-yet-started renewal chain too**). Plan them as PR 1's first commits (files, tests, breaks, the
locks for item 1), before the plan's own, named in the description under "Carried from #123"; do not re-decide them.

## 2. The owner's decisions (2026-10-26) — binding

**The goal (build map step 11, the API only; the screens 19, 24's rest, 31 and 32 are worker A's later items):**
the owner reads the space's money and occupancy; the owner and the admin read their audit logs; the platform's
settings are edited by the admin. **Read what is built first:** the audit writer and its table (conventions §6), the
`platform-settings` module (minimal: the new-space defaults and the staleness thresholds), `can()`'s
`finance.read`, `space.auditLog.read`, `platform.auditLog.read`, `platform.settings.manage`, the payments list
(#114), the desk's reads.

1. **Three PRs, in this order:** PR 1 the audit reader (the owner's and the admin's), opening with the carried items;
   PR 2 the platform settings; PR 3 the finance read model. Each cut from `main` once the one before merged.
2. **Income is cash collected:** payments received, **voided ones excluded**; a written-off visit is not income; the
   debts are their own figures. (Finance.html says it: «الدخل = المبالغ المقبوضة فعليًا، بدون الدفعات الملغاة».)
3. **Periods as the design settled (OW-015):** one month chosen (Gaza's calendar month), and fixed windows for the
   charts — the last 12 months, the last 30 days, the last 14 days, the last 4 weeks — all on Gaza time. **No free
   date range.**
4. **The server aggregates:** each chart's series and each figure computed by the API (a read model, conventions R7),
   never raw rows for the web to sum; answers bounded (ADR 0014's response size).
5. **CSV export is the web's:** built in the browser from the JSON the API answers; **no export route**. (The debts'
   CSV holds phones: the owner's alone, as the finance route is.)
6. **Finance is the owner's alone** (`finance.read`); reception reads nothing of it (it keeps «دفعاتي اليوم», #114).
7. **Occupancy statistics from closed stays**, those closed by the auto check-out included; open ones excluded.
8. **The owner's audit log** shows every entry of the space — the staff's and the admin's actions on it — with the
   admin's actor shown as **Masaha** (not the admin's name, as the data reports' `repliedBy: MASAHA`); the owner never
   sees another space's entries.
9. **The admin's audit log** as the design settled (AD-028, A7): the platform event types only (conventions §6's
   default-deny allowlist — never an entry about a space's customers, visits, subscriptions or payments), a search
   by target, an actor filter, the default range «آخر 30 يومًا» with «كل الفترة», paged as every list (§5); each
   target linkable to its page.
10. **Audit entries are kept for ever in v1** (no retention job).
11. **The platform settings the admin edits:** the new-space defaults, the staleness thresholds, **and the platform's
    contact details, brought into the typed key catalogue** — resolving **finding 40** (the contact keys the seed
    writes outside it). AD-029's one page, each card its own save and error.
12. **Finding 151 — option A** (the carried file's item 1).

**For you to decide, with a recommendation each (the owner approves):**
13. **The finance figures and their shapes, tab by tab, from `Finance.html` / `masaha/finance.jsx`** — income (the
    month's total, by subscriptions and visits, against the month before; the last 12 months; visit income per day;
    collections per staff member by method), debts (who owes, largest first, since when and the oldest item; who is
    in credit; the totals; what the WhatsApp reminder needs — the phone and the space's reminder text from its
    settings), occupancy (visits and members per day; the average present per hour over 4 weeks; the average stay,
    members and visits): which route(s), each field, each derivation from the ledger and the stays, and what is
    **excluded** (voided, written off, archived customers?). Say which figures the overview (step 12) will reuse, so
    its later item composes them rather than recomputes.
14. **Cost and indexes:** each aggregate's query, its plan on a year of one space's data, and any index (a migration,
    no PR number in its SQL); the response bounds.
15. **The audit entry as answered:** the shape (action, actor, target, when, `before`/`after` as stored or summarised),
    the event types' allowlist for the admin (list them), the owner's filters, paging, and how a target links (an id
    and a kind the web maps to a page).
16. **The platform settings' contract:** the routes (read, one save per card), the keys and their validation, the
    public read of the contact details (who reads them today, and the migration of the seed's keys into the
    catalogue), and audit lines (§6 already lists settings changes).
17. **Each PR's size**, and any document this proves wrong — as a proposal, never applied silently.

**The decisions are proposals you may challenge** (the owner's rule): where you see a better way, argue it with
evidence from the code or the documents in *Proposed alternatives*, with its cost — never apply it.

## 3. Read first

`CLAUDE.md`; `docs/development/workflow.md`; `testing.md`; `docs/backend/conventions.md` (§4–§9 — §6 *Audit*, R7,
§9 *Settings: three screens, three owners* and *New-space defaults* —, §11, §13); `security.md` (authorization,
privacy); ADR 0002, 0009, 0010, 0014; `docs/architecture/data-model.md` (the audit table, *Front desk and money*, the
derived values, the settings); `docs/api/api-contract.md` (§1–6, *Front desk (managed)* — the payments list —,
*Settings (managed)*, the platform-settings and public lookups parts, the error codes); `docs/features/payments.md`,
`desk.md`, `visits.md`, `subscriptions.md`, `space-settings.md`, `announcements.md`, and any `platform-settings` or
`audit` document; `docs/project/overview.md` (*Dashboard*, *Admin*, what drops first); `docs/plans/v1-mvp.md` step 11
and the route table; findings 14 and 40 (and the findings index); `C:\dev\masaha\workspace\DESIGN\DECISIONS\
DECISIONS_OWNER.md` (the money note at its top, O13, OW-015, OW-016), `DECISIONS_ADMIN.md` (A7, AD-028, AD-029),
`DECISIONS_SHARED.md` (P3); the prototypes `docs/design/prototype/Finance.html` (and `masaha/finance.jsx`),
`Owner audit.html`, `Admin audit.html`, `Admin settings.html` — only where the API's shape depends on them;
`_SHARED\OPEN_DECISIONS.md`; the carried file and, for its items, `WORKER_B\ANNOUNCEMENTS\6_REVIEW_PR4_CLAUDE_CODE.md`;
the code of `shared/audit`, `platform-settings`, `payments`, `visits`, `subscriptions`, `occupancy`, `desk`,
`space-settings` and `shared/auth` (`can()`) on `origin/main`; `schema.prisma` (the audit, settings, payments, visits
and check-ins tables and their indexes); the demo seed (what a real run can read); `WORKER_B\ANNOUNCEMENTS\2_PLAN.md`
as the model of the plan.

## 4. The plan's shape

As `WORKER_B\ANNOUNCEMENTS\2_PLAN.md`: a header (base sha, worker, folder, the PRs with their branch, size and
title); summary; the contract per PR (scope, acceptance criteria, out of scope); the reading done and what it
changed; the decisions as built; stronger decisions (S…) and **Proposed alternatives**; related findings (folded or
not, why); the files; the interfaces; the tests with their breaks; the commits (the carried ones first); the
procedure and the executor's rules; the decisions needed from the owner (each with options and a recommendation).
Stop after saving it, and reply only `PLAN READY: C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT\2_PLAN.md` with the
PR count and the number of decisions for the owner.
