# Review — FINANCE_AUDIT PR 2 (`feat/platform-settings`), one independent reviewer (Claude Code)

You are the **independent reviewer** of worker B's second FINANCE_AUDIT PR in Basel-Ghonaim/masaha (step 11's API,
PR 2 of 3), **API only** (`apps/api`, `packages/shared`, `docs`; no migration, no `apps/web`): the platform's settings
— the admin's three cards (the new spaces' defaults, the staleness thresholds 1–365, the contact: email and WhatsApp),
each its own resource and save (`GET`/`PUT /admin/settings/{new-space-defaults|staleness|contact}`), audited
`platformSettings.*Edited` with no entity id and only what changed, on the admin's log; the public contact
(`GET /settings/public`, `Cache-Control: public, max-age=300`); finding 40 resolved (the contact keys in the typed
catalogue). **Authorization, the audit, concurrency and validation:** trust nothing you have not seen in the code.
Find the PR: `gh pr list --head feat/platform-settings --state open --json number,headRefOid,mergeStateStatus`
(expected #130, head `299d8abd`). Write the report to
`C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT\6_REVIEW_PR2_CLAUDE_CODE.md`, **as you go**. **Work alone — no
subagents.** This is a review, not a Work Item: run no project skill, no branch.

## Rules

- **Read only, from `C:\dev\masaha\app-design`, commit objects only:** `git fetch origin` and `git fetch origin
  pull/<n>/head`; base = `origin/main`; **pin every read to the head's sha**. No edits, checkout, switch or reset, no
  installs, no npm or test runs, no servers, no database commands, no comments on GitHub. The only file you write is
  the report. A `git` command failing on a `.lock` file: wait 30 s, retry once.
- First `gh pr checks <n>` — red or pending: say so and stop. At the end, `gh pr view <n> --json headRefOid` again.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario (inputs → wrong
  result), severity (**blocker** — a non-admin reading or writing a card, a private value reaching the public read, a
  save lost or doubled under concurrency, an audit entry false or missing, a 500 a client can cause, a test that
  cannot fail · **should-fix** — a real defect, a missing planned test, a false document · **nit**), the fix and
  where it belongs (a fix round on this PR; worker B's next PR's first commit; a finding from **154**). "Plausible"
  when unsure. Say what you saw in the code and what you only read in the report. No praise.

## What to read

1. `git show origin/main:CLAUDE.md`.
2. `C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT\2_PLAN.md`: the owner's approval note at its top (binding); for PR
   2: §2 *Scope* and *Acceptance criteria*; §4 decision 11, D1's PR 2 routes, D3/D4's PR 2 lines, **D7**, D13, D14;
   §5 **S8–S11**; §6 (finding 40); §9 *PR 2* (U1–U2, T1–T11, B1–B12); §11 *PR 2*; §12.6's PR 2 cases.
3. `3_EXEC_PROMPT_PR2.md` and `4_REPORT_PR2.md` (same folder). The executor ran under the owner's **no-stop rule**:
   judge **every decision taken without the owner** (nine) — above all its **SERIOUS** one: the real run's first
   check saved the contact card with the values it read, the seed's `+972…` WhatsApp was normalised to `+970…` and
   audited (entry 56), not put back; finding 153 (the seed accepts any E.164 contact). Is the normalisation right by
   the project's phone rule, is a save of "the same values" that changes the stored form a defect of the API (S10:
   read stored, written normalised — should the no-change check compare the normalised forms?), and is 153 true?
   Also: `features/audit.md` touched beyond the plan's list; every card saved and put back in the run.
4. The contract at the head (*Settings* — the admin's and the public routes), conventions §6, §7, §9 *Settings*, and
   the shared `platform-settings` / `space-settings` schemas.

## Look hardest at

- **Authorization:** the six admin routes behind `/admin` only (a guest 401, a user and an owner 403 — before the
  body is read); the public read exposes the contact only, nothing else of the catalogue.
- **The save (D7):** each card its own resource; `ensure` then `lock` (`FOR UPDATE`) then `write` per changed key,
  reads through `tx`; two saves of one card at once (the second's `before` is the first's `after`); two first saves
  of the contact (one row per key, both 200); the no-change branch (nothing written, nothing audited) — and whether
  "the same values" can still write when the stored form differs from the normalised one (the SERIOUS case above);
  `null` clears an optional key (`Prisma.JsonNull`).
- **The audit:** `entityType: 'platformSettings'`, `entityId: null` (S8 — the writer's type now `number | null`: does
  any existing caller or reader break?), no space, `before`/`after` with only the changed fields, the three actions on
  the admin's allowlist and in `@masaha/shared/audit`; the owner's log never shows them; #128's target joins read a
  null entity id as `name: null`.
- **Validation:** thresholds whole 1–365 (S11); the email lowercased; WhatsApp normalised (Jawwal/Ooredoo to +970),
  another country refused; the defaults' minutes rule; a stored contact failing its schema → 500, never answered.
- **The defaults (T3):** a saved default reaches only spaces created after it; existing spaces keep their own.
- **Tests and breaks:** B1–B12 seen red per the report; B8 red "on the lock wait, not the plan's 500" — does T6 still
  prove one row per key?; T7 passed before its router existed (B9 its proof).
- **Documents:** the contract, conventions, `platform-settings.md` (new), `audit.md`, finding 40 resolved, 153, the
  index, `v1-mvp.md`, `overview.md`, `docs/README.md` — true to the code, `#130` where it goes.
- **Scope:** `apps/api`, `packages/shared`, `docs` only; no migration, no dependency; subjects ≤ 50 with bodies; no
  `fixup!`, no tool attribution.

## Your output

One file: the head, CI's state, whether the head moved; **a one-line verdict** (mergeable / mergeable after a fix
round / not mergeable); the findings, most severe first, each with where its fix belongs; the SERIOUS decision judged
first, then the other eight; the tests and breaks one line each; a short "Checked and fine". Then stop.
