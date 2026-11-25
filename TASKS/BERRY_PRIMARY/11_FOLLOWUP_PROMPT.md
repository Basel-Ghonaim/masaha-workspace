# WI-B2 — the auth forms' main action, and an audit of every screen's main action

You are a **Claude Code worker** on **Masaha**, a bilingual Arabic RTL / English platform for coworking spaces in Gaza.
A fresh session, **Opus 5.5, effort medium**, in **`C:\dev\masaha\app`** (on `main` = `95c33fe9` (#157 and #158 merged), clean; API 3320 on
`masaha_dev`, tests on `masaha_test`, web 5320). `main` is **live in production**: every merge deploys. No other worker
runs in `app`.

This is a **small, decided task**: write a short plan to `C:\dev\masaha\workspace\TASKS\BERRY_PRIMARY\12_PLAN.md` and
**do not stop after it** — build, verify, open the PR, report to `13_REPORT.md`. Never merge.
**You run headless** (launched by the supervisor): run every heavy command in the foreground and wait for it; never end
your turn while a run is pending or before the report is written — a headless session ends when you do. Follow the skills
`start-work-item`, `write-plan`, `open-pr`, `final-report`, with that exception.

## Read first — binding
- ADR 0022 and its *Revised* line; `TASKS\BERRY_PRIMARY\0_OWNER_DECISIONS.md` (A18, B1, WI-B's D1–D7);
- WI-B's `6_PLAN.md` §4.3 (the rule and the table) and `7_REPORT.md` (its list of the auth edits left for this
  follow-up);
- foundation §5 (the main action's rule) and §12 (`Button`'s `main`);
- WI-C2's merged code (PR #157): the in-place sign-in, the reset page's sign-in.

## The work
1. **The auth forms' main action** (WI-B's D4): by the same rule — a form's submit, or a done state's one link, is
   `variant="main"`: sign in, register, the reset link's request, the reset form, the reset page's sign-in (C2's new
   one), the overlay's views (they reuse these forms), and any done state with one link. Nothing else in auth changes.
   One assertion per form that it draws the main action.
2. **The audit — every screen, every overlay.** Walk the route tables (`pages/site/routes.tsx`,
   `pages/dashboard/routes.tsx`) and every Dialog / AlertDialog / Sheet / AdaptiveDialog in `features/**` and `pages/**`:
   - by the code: list each screen and overlay with its `variant="main"` call sites (expect exactly one per screen
     where the table names one, one per overlay's confirm, none on settings cards, states, the directory; the desk's
     «تحصيل» rows ink);
   - in Chrome, **light theme**, as a guest, the demo owner and the admin, at 1440 and 390: count the painted
     `[data-slot="button"].bg-main-action` in view on each route and in each overlay you can open without writing
     data, with a short script; and check **dark** on five screens shows no berry button at all (B1).
   - **Deviations:** fix any that clearly breaks the rule (two main actions in one view, a main action missing where
     the table names one, a berry button in dark) as its own commit; **list for the owner, without changing**, any that
     needs a judgement (a screen the table does not name).
   - The report holds the full table: screen / overlay, role, width, expected, found, verdict.
3. **Tests:** the assertions of item 1; one per fixed deviation, seen failing first.
4. **Documents:** only if a fix changes what they say; WI-B's follow-up note closed in `directory.md` / foundation if it
   points to this work.

## Hard limits
- Web and docs only; no API, schema, migration, dependency or database write. No secret printed.
- Touch only what this task needs; stage by path; no drive-by refactoring; record anything else as a finding.
- Never weaken a test; no production code only a test uses.
- Commits: Conventional, subject ≤ 50, with a body, no attribution, no `fixup!`; `#PRNUM` replaced before the push
  (expect **#159**, check the PR and Issue lists).
- Heavy commands in the foreground through `node C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs b2 <command…>`;
  a run killed for memory: retry once, then CI judges. Servers on 3320 / 5320, stopped by PID after, ports checked.

## Verification
On the head: `format:check`, `lint`, `typecheck`, `check:classes`, `check:links`, `check:conflicts`, `test:unit`,
`test:component`, the production build (`NODE_ENV=production`), `check:build`. Chrome as in item 2, axe on the auth
views. Shots to `C:\Users\basel\Downloads\berry-audit-shots\`, curated. Push, `open-pr`, green CI and `CLEAN`, then the
report with `final-report`. **Then stop. Never merge.**
