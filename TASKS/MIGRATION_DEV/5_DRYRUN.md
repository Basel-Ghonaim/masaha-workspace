# Path rewrite — DRY RUN

Root: `C:\dev\masaha\workspace`

Rules (longest first, separator kept as written: `\`, `/` or `\\`; a path followed by a letter, digit, `_` or `-` is not touched):

- `(?P<d>[Cc]):(?P<s>\\\\|\\|/)Users(?P=s)basel(?P=s)masaha-design-b(?![\w-])` → `C:<s>dev<s>masaha<s>design-b`
- `(?P<d>[Cc]):(?P<s>\\\\|\\|/)Users(?P=s)basel(?P=s)masaha-design(?![\w-])` → `C:<s>dev<s>masaha<s>design`
- `(?P<d>[Cc]):(?P<s>\\\\|\\|/)Users(?P=s)basel(?P=s)masaha-b(?![\w-])` → `C:<s>dev<s>masaha<s>app-b`
- `(?P<d>[Cc]):(?P<s>\\\\|\\|/)Users(?P=s)basel(?P=s)masaha(?![\w-])` → `C:<s>dev<s>masaha<s>app`
- `(?P<d>[Dd]):(?P<s>\\\\|\\|/)masahaWorkspace(?![\w-])` → `C:<s>dev<s>masaha<s>workspace`

Skipped: dirs named .git, LOGS, REPORT, _DONE, _aborted, _superseded, shots; _SHARED\HANDOFFS, _SHARED\MIGRATION, TASKS\MIGRATION_DEV, _SHARED\ARCHIVE_*; _SHARED\snapshot.log

## Summary

files changed: 73 ; replacements: 439

- design-b: 1
- design: 101
- app-b: 7
- app: 14
- workspace: 316

encodings / line endings of changed files: utf-8/CRLF=1, utf-8/LF=72

old paths left untouched in skipped records (by area): DESIGN=212, TASKS=71, WORKER_A=44, WORKER_B=112, _SHARED\ARCHIVE_2026-10-08=75, _SHARED\HANDOFFS=19, _SHARED\MIGRATION=2166

files mentioning masaha that are not UTF-8 text (not touched): DESIGN\ROUND2\shots\_aborted\OW-DF\chrome-profile\Default\Favicons (binary), DESIGN\ROUND2\shots\_aborted\OW-DF\chrome-profile\Default\Cache\Cache_Data\data_1 (binary), DESIGN\ROUND2\shots\_aborted\OW-DF\chrome-profile\Default\Cache\Cache_Data\data_3 (binary), DESIGN\ROUND2\shots\_aborted\OW-DF\chrome-profile\Default\Code Cache\js\4f345a5f17a0e721_0 (binary), DESIGN\ROUND2\shots\_aborted\OW-DF\chrome-profile\Default\Code Cache\js\61f2f31c3d18a5b1_0 (binary), DESIGN\ROUND2\shots\_aborted\OW-DF\chrome-profile\Default\Code Cache\js\73cc5957306a7c0a_0 (binary), DESIGN\ROUND2\shots\_aborted\OW-DF\chrome-profile\Default\Code Cache\js\a72759c72674460e_0 (binary), DESIGN\ROUND2\shots\_aborted\OW-DF\chrome-profile\Default\Code Cache\js\cab630d2aec65e73_0 (binary), DESIGN\ROUND2\shots\_aborted\OW-DF\chrome-profile\Default\Code Cache\js\e1c14c7c8ef7a4bb_0 (binary), WORKER_B\_DONE\MANAGE\MANAGE_REPORT.md (not-utf8)

## Other spellings found in active files (NOT changed — for the owner)

none

## Every changed file

### `DESIGN\ROUND2\HANDOFF_DESIGN_81.md` — design=2, app=1, workspace=7 (utf-8, LF)
- L5: `supervisor (the project's analyst, reading `D:\masahaWorkspace\HANDOFF.md`) reads this file's *Status log*;`
  → `supervisor (the project's analyst, reading `C:\dev\masaha\workspace\HANDOFF.md`) reads this file's *Status log*;`
- L7: `below reads `C:\dev\masaha\…`: `masaha-design` → `C:\dev\masaha\design`, `D:\masahaWorkspace` →`
  → `below reads `C:\dev\masaha\…`: `masaha-design` → `C:\dev\masaha\design`, `C:\dev\masaha\workspace` →`
- L19: `- You **never edit the repository** (`C:\Users\basel\masaha*`). You write only in`
  → `- You **never edit the repository** (`C:\dev\masaha\app*`). You write only in`
- L20: ``D:\masahaWorkspace\DESIGN\` and to Issue #81 (its body), and only with the owner's word for #81.`
  → ``C:\dev\masaha\workspace\DESIGN\` and to Issue #81 (its body), and only with the owner's word for #81.`
- L25: `- Prompts: `D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-<PART>-<AXIS>.md` (40) and `R2-<PART>-SUMMARY.md`,`
  → `- Prompts: `C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-<PART>-<AXIS>.md` (40) and `R2-<PART>-SUMMARY.md`,`
- L30: `- Settled decisions, which reviews must not report again: `D:\masahaWorkspace\DESIGN\DECISIONS\` (`DECISIONS_*.md`,`
  → `- Settled decisions, which reviews must not report again: `C:\dev\masaha\workspace\DESIGN\DECISIONS\` (`DECISIONS_*.md`,`
- L31: ``REVIEW_LENS.md`). Pending desk decisions (not this round's): `D:\masahaWorkspace\_SHARED\OPEN_DECISIONS.md`.`
  → ``REVIEW_LENS.md`). Pending desk decisions (not this round's): `C:\dev\masaha\workspace\_SHARED\OPEN_DECISIONS.md`.`
- L32: `- The worktree the reviews read: `C:\Users\basel\masaha-design` (detached; keep it on `origin/main`:`
  → `- The worktree the reviews read: `C:\dev\masaha\design` (detached; keep it on `origin/main`:`
- L48: ``D:\masahaWorkspace\DESIGN\DECISIONS_ROUND2.md`; then the fix batch(es) of `docs/design/` (Claude plans,`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS_ROUND2.md`; then the fix batch(es) of `docs/design/` (Claude plans,`
- L58: `- One review per **new session**, opened in `C:\Users\basel\masaha-design`, three at a time at most; paste the`
  → `- One review per **new session**, opened in `C:\dev\masaha\design`, three at a time at most; paste the`
### `DESIGN\ROUND2\MAP_AR.md` — design=1, workspace=3 (utf-8, LF)
- L3: `كل الملفات في: `D:\masahaWorkspace\DESIGN\ROUND2\``
  → `كل الملفات في: `C:\dev\masaha\workspace\DESIGN\ROUND2\``
- L13: `- **باليد (الأضمن الآن):** افتح OpenCode من `C:\Users\basel\masaha-design`، واختر نموذجًا يعمل، والصق:`
  → `- **باليد (الأضمن الآن):** افتح OpenCode من `C:\dev\masaha\design`، واختر نموذجًا يعمل، والصق:`
- L14: ``Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\<ID>.md whole and follow it.``
  → ``Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\<ID>.md whole and follow it.``
- L17: ``& "D:\masahaWorkspace\DESIGN\ROUND2\run-queue.ps1"``
  → ``& "C:\dev\masaha\workspace\DESIGN\ROUND2\run-queue.ps1"``
### `DESIGN\ROUND2\MONITOR_PROMPT.md` — app=1, workspace=3 (utf-8, LF)
- L9: `- 40 review prompts and 7 summary prompts in `D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\`.`
  → `- 40 review prompts and 7 summary prompts in `C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\`.`
- L25: ``Start-Process powershell -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','D:\masahaWorkspace\DESIGN\ROUND2\run-queue.ps1'``
  → ``Start-Process powershell -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','C:\dev\masaha\workspace\DESIGN\ROUND2\run-queue.ps1'``
- L52: `scripts, or anything in `C:\Users\basel\masaha*` (the project's folders). Never run git, npm, tests,`
  → `scripts, or anything in `C:\dev\masaha\app*` (the project's folders). Never run git, npm, tests,`
- L59: `Append to `D:\masahaWorkspace\DESIGN\ROUND2\MONITOR_LOG.md` (create it): at every check, one`
  → `Append to `C:\dev\masaha\workspace\DESIGN\ROUND2\MONITOR_LOG.md` (create it): at every check, one`
### `DESIGN\ROUND2\PROMPT\R2-AD-AX.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L24: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L29: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\AD-AX\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\AD-AX\` (create it if missing).`
- L73: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L74: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes — P7 states,`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes — P7 states,`
- L75: `P8 feedback/429) and `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md` (with all`
  → `P8 feedback/429) and `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md` (with all`
- L91: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-AD-AX_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-AD-AX_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-AD-CP.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L25: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L31: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\AD-CP\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\AD-CP\` (create it if missing).`
- L81: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L82: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes, including the`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes, including the`
- L84: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md` (with all amendments).`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md` (with all amendments).`
- L98: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-AD-CP_REPORT.md`. English, concise`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-AD-CP_REPORT.md`. English, concise`
### `DESIGN\ROUND2\PROMPT\R2-AD-DF.md` — design=2, workspace=5 (utf-8, LF)
- L13: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L23: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L28: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\AD-DF\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\AD-DF\` (create it if missing).`
- L73: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L74: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
- L75: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md` (with all amendments).`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md` (with all amendments).`
- L89: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-AD-DF_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-AD-DF_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-AD-EX.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L24: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L28: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\AD-EX\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\AD-EX\` (create it if missing).`
- L68: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L69: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
- L70: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md` (with all amendments).`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md` (with all amendments).`
- L84: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-AD-EX_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-AD-EX_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-AD-SUMMARY.md` — design=1, workspace=2 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` only to consult the documents named below (lens,`
  → `- Read from `C:\dev\masaha\design` only to consult the documents named below (lens,`
- L19: ``D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-AD-UX_REPORT.md`,`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-AD-UX_REPORT.md`,`
- L37: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\SUMMARY\R2-AD_SUMMARY.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\SUMMARY\R2-AD_SUMMARY.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-AD-TR.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L24: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L28: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\AD-TR\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\AD-TR\` (create it if missing).`
- L76: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L77: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
- L78: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md` (with all amendments, including role-`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md` (with all amendments, including role-`
- L94: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-AD-TR_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-AD-TR_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-AD-UX.md` — design=2, workspace=5 (utf-8, LF)
- L13: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L23: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L27: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\AD-UX\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\AD-UX\` (create it if missing).`
- L83: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L84: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes: P1–P10 as`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes: P1–P10 as`
- L85: `they touch the admin) and `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md` (A1–A8, G1–G4`
  → `they touch the admin) and `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md` (A1–A8, G1–G4`
- L105: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-AD-UX_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-AD-UX_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-AD-VD.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L24: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L28: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\AD-VD\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\AD-VD\` (create it if missing).`
- L72: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L73: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
- L74: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md` (with all amendments).`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md` (with all amendments).`
- L90: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-AD-VD_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-AD-VD_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-ALL-SUMMARY.md` — design=1, workspace=2 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` only to consult the documents named below. `git fetch`
  → `- Read from `C:\dev\masaha\design` only to consult the documents named below. `git fetch`
- L18: ``D:\masahaWorkspace\DESIGN\ROUND2\SUMMARY\R2-AU_SUMMARY.md`,`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\SUMMARY\R2-AU_SUMMARY.md`,`
- L35: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\SUMMARY\R2-ALL_SUMMARY.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\SUMMARY\R2-ALL_SUMMARY.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-AU-AX.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L24: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L29: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\AU-AX\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\AU-AX\` (create it if missing).`
- L72: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L73: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes — P7 states,`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes — P7 states,`
- L75: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_ACCOUNT.md` (C1–C8, especially AC-022's 429`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ACCOUNT.md` (C1–C8, especially AC-022's 429`
- L91: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-AU-AX_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-AU-AX_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-AU-CP.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L25: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L30: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\AU-CP\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\AU-CP\` (create it if missing).`
- L78: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L79: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes, including the`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes, including the`
- L81: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_ACCOUNT.md` (C1–C8 and the 2026-10-13 amendment to`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ACCOUNT.md` (C1–C8 and the 2026-10-13 amendment to`
- L97: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-AU-CP_REPORT.md`. English, concise`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-AU-CP_REPORT.md`. English, concise`
### `DESIGN\ROUND2\PROMPT\R2-AU-DF.md` — design=2, workspace=5 (utf-8, LF)
- L13: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L23: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L28: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\AU-DF\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\AU-DF\` (create it if missing).`
- L76: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L77: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
- L78: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_ACCOUNT.md` (C1–C8 and the 2026-10-13 amendment).`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ACCOUNT.md` (C1–C8 and the 2026-10-13 amendment).`
- L94: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-AU-DF_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-AU-DF_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-AU-EX.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L24: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L28: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\AU-EX\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\AU-EX\` (create it if missing).`
- L70: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L71: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
- L72: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_ACCOUNT.md` (C1–C8 and the 2026-10-13 amendment).`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ACCOUNT.md` (C1–C8 and the 2026-10-13 amendment).`
- L89: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-AU-EX_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-AU-EX_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-AU-SUMMARY.md` — design=1, workspace=2 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` only to consult the documents named below (lens,`
  → `- Read from `C:\dev\masaha\design` only to consult the documents named below (lens,`
- L19: ``D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-AU-UX_REPORT.md`,`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-AU-UX_REPORT.md`,`
- L37: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\SUMMARY\R2-AU_SUMMARY.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\SUMMARY\R2-AU_SUMMARY.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-AU-TR.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L24: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L28: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\AU-TR\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\AU-TR\` (create it if missing).`
- L77: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L78: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
- L79: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_ACCOUNT.md` (C1–C8 and the 2026-10-13 amendment;`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ACCOUNT.md` (C1–C8 and the 2026-10-13 amendment;`
- L95: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-AU-TR_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-AU-TR_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-AU-UX.md` — design=2, workspace=5 (utf-8, LF)
- L13: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L23: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L27: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\AU-UX\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\AU-UX\` (create it if missing).`
- L87: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L88: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes: P1, P4–P9 as`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes: P1, P4–P9 as`
- L89: `they touch the account) and `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_ACCOUNT.md` (C1–C8 and`
  → `they touch the account) and `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ACCOUNT.md` (C1–C8 and`
- L110: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-AU-UX_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-AU-UX_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-AU-VD.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L24: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L28: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\AU-VD\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\AU-VD\` (create it if missing).`
- L75: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L76: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
- L77: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_ACCOUNT.md` (C1–C8 and the 2026-10-13 amendment).`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ACCOUNT.md` (C1–C8 and the 2026-10-13 amendment).`
- L95: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-AU-VD_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-AU-VD_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-BROWSER-PASS.md` — design=2, workspace=2 (utf-8, LF)
- L16: `- Read from `C:\Users\basel\masaha-design` (a detached worktree). First `git fetch origin`; check`
  → `- Read from `C:\dev\masaha\design` (a detached worktree). First `git fetch origin`; check`
- L21: ``C:\Users\basel\masaha-design`, in the background. Pages: `http://127.0.0.1:5490/<Prototype URL>`, with`
  → ``C:\dev\masaha\design`, in the background. Pages: `http://127.0.0.1:5490/<Prototype URL>`, with`
- L29: `| # | Report (in `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\`) | Its prompt (scope, axis, widths) |`
  → `| # | Report (in `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\`) | Its prompt (scope, axis, widths) |`
- L47: `widths and modes) and §5 (its axis). Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b`
  → `widths and modes) and §5 (its axis). Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b`
### `DESIGN\ROUND2\PROMPT\R2-DK-AX.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L26: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L37: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\DK-AX\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\DK-AX\` (create it if missing).`
- L88: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L89: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes — P7 states,`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes — P7 states,`
- L91: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_DESK.md` (K1–K8, DK-003–DK-023, DK-018's retry`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_DESK.md` (K1–K8, DK-003–DK-023, DK-018's retry`
- L107: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-DK-AX_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-DK-AX_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-DK-CP.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L27: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L37: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\DK-CP\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\DK-CP\` (create it if missing).`
- L96: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L97: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes, including the`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes, including the`
- L98: `P9 verb discipline) and `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_DESK.md` (K1–K8,`
  → `P9 verb discipline) and `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_DESK.md` (K1–K8,`
- L113: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-DK-CP_REPORT.md`. English, concise`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-DK-CP_REPORT.md`. English, concise`
### `DESIGN\ROUND2\PROMPT\R2-DK-DF.md` — design=2, workspace=5 (utf-8, LF)
- L13: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L25: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L35: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\DK-DF\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\DK-DF\` (create it if missing).`
- L96: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L97: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
- L98: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_DESK.md` (K1–K8, DK-003–DK-023).`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_DESK.md` (K1–K8, DK-003–DK-023).`
- L112: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-DK-DF_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-DK-DF_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-DK-EX.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L26: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L35: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\DK-EX\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\DK-EX\` (create it if missing).`
- L84: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L85: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
- L86: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_DESK.md` (K1–K8, DK-003–DK-023).`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_DESK.md` (K1–K8, DK-003–DK-023).`
- L100: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-DK-EX_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-DK-EX_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-DK-SUMMARY.md` — design=1, workspace=2 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` only to consult the documents named below (lens,`
  → `- Read from `C:\dev\masaha\design` only to consult the documents named below (lens,`
- L20: ``D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-DK-UX_REPORT.md`,`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-DK-UX_REPORT.md`,`
- L39: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\SUMMARY\R2-DK_SUMMARY.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\SUMMARY\R2-DK_SUMMARY.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-DK-TR.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L26: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L34: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\DK-TR\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\DK-TR\` (create it if missing).`
- L98: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L99: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
- L100: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_DESK.md` (K1–K8, DK-003–DK-023, with the API/docs`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_DESK.md` (K1–K8, DK-003–DK-023, with the API/docs`
- L117: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-DK-TR_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-DK-TR_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-DK-UX.md` — design=2, workspace=5 (utf-8, LF)
- L13: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L25: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L34: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\DK-UX\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\DK-UX\` (create it if missing).`
- L110: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L111: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes: P1's desk`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes: P1's desk`
- L113: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_DESK.md` (K1–K8 and the smaller items DK-003–`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_DESK.md` (K1–K8 and the smaller items DK-003–`
- L131: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-DK-UX_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-DK-UX_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-DK-VD.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L26: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L35: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\DK-VD\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\DK-VD\` (create it if missing).`
- L90: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L91: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
- L92: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_DESK.md` (K1–K8, DK-003–DK-023).`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_DESK.md` (K1–K8, DK-003–DK-023).`
- L107: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-DK-VD_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-DK-VD_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-OW-AX.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L24: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L29: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\` (create it if missing).`
- L71: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L72: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes — P7 states,`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes — P7 states,`
- L73: `P8 feedback/429) and `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (O1–O13 with all`
  → `P8 feedback/429) and `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (O1–O13 with all`
- L89: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-OW-AX_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-OW-AX_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-OW-CP.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L25: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L31: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\OW-CP\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-CP\` (create it if missing).`
- L82: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L83: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes, including the`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes, including the`
- L84: `P9 verb discipline) and `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (O1–O13 with all`
  → `P9 verb discipline) and `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (O1–O13 with all`
- L99: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-OW-CP_REPORT.md`. English, concise`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-OW-CP_REPORT.md`. English, concise`
### `DESIGN\ROUND2\PROMPT\R2-OW-DF.md` — design=2, workspace=5 (utf-8, LF)
- L13: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L23: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L28: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\OW-DF\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-DF\` (create it if missing).`
- L74: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L75: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
- L76: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (O1–O13 with all notes).`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (O1–O13 with all notes).`
- L90: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-OW-DF_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-OW-DF_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-OW-EX.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L24: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L28: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\OW-EX\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-EX\` (create it if missing).`
- L71: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L72: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
- L73: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (O1–O13 with all notes).`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (O1–O13 with all notes).`
- L88: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-OW-EX_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-OW-EX_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-OW-SUMMARY.md` — design=1, workspace=2 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` only to consult the documents named below (lens,`
  → `- Read from `C:\dev\masaha\design` only to consult the documents named below (lens,`
- L19: ``D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-OW-UX_REPORT.md`,`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-OW-UX_REPORT.md`,`
- L37: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\SUMMARY\R2-OW_SUMMARY.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\SUMMARY\R2-OW_SUMMARY.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-OW-TR.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L24: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L28: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\OW-TR\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-TR\` (create it if missing).`
- L79: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L80: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
- L81: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (O1–O13 with all notes, including the`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (O1–O13 with all notes, including the`
- L97: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-OW-TR_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-OW-TR_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-OW-UX.md` — design=2, workspace=5 (utf-8, LF)
- L13: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L23: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L27: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\OW-UX\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-UX\` (create it if missing).`
- L90: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L91: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes: P1 no bottom`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes: P1 no bottom`
- L93: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (O1–O13, the 2026-10-11 DI-10 drawer`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (O1–O13, the 2026-10-11 DI-10 drawer`
- L112: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-OW-UX_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-OW-UX_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-OW-VD.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L24: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L28: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\OW-VD\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-VD\` (create it if missing).`
- L73: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L74: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
- L75: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (O1–O13 with all notes).`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (O1–O13 with all notes).`
- L90: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-OW-VD_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-OW-VD_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-PU-AX.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L24: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L29: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\PU-AX\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\PU-AX\` (create it if missing).`
- L72: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L73: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes — P7 states,`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes — P7 states,`
- L74: `P8 feedback) and `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_PUBLIC.md` (U6–U7, U12, PU-013,`
  → `P8 feedback) and `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_PUBLIC.md` (U6–U7, U12, PU-013,`
- L90: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-PU-AX_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-PU-AX_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-PU-CP.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L25: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L30: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\PU-CP\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\PU-CP\` (create it if missing).`
- L82: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L83: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes, including the`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes, including the`
- L84: `P9 verb discipline) and `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_PUBLIC.md` (U3–U4, U9–U11,`
  → `P9 verb discipline) and `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_PUBLIC.md` (U3–U4, U9–U11,`
- L100: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-PU-CP_REPORT.md`. English, concise`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-PU-CP_REPORT.md`. English, concise`
### `DESIGN\ROUND2\PROMPT\R2-PU-DF.md` — design=2, workspace=5 (utf-8, LF)
- L13: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L23: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L28: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\PU-DF\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\PU-DF\` (create it if missing).`
- L74: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L75: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
- L76: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_PUBLIC.md` (with the 2026-10-12 amendments and the`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_PUBLIC.md` (with the 2026-10-12 amendments and the`
- L92: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-PU-DF_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-PU-DF_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-PU-EX.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L24: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L28: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\PU-EX\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\PU-EX\` (create it if missing).`
- L71: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L72: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
- L73: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_PUBLIC.md` (with the 2026-10-12 amendments and the`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_PUBLIC.md` (with the 2026-10-12 amendments and the`
- L88: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-PU-EX_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-PU-EX_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-PU-SUMMARY.md` — design=1, workspace=2 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` only to consult the documents named below (lens,`
  → `- Read from `C:\dev\masaha\design` only to consult the documents named below (lens,`
- L19: ``D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-PU-UX_REPORT.md`,`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-PU-UX_REPORT.md`,`
- L38: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\SUMMARY\R2-PU_SUMMARY.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\SUMMARY\R2-PU_SUMMARY.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-PU-TR.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L24: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L28: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\PU-TR\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\PU-TR\` (create it if missing).`
- L76: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L77: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
- L78: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_PUBLIC.md` (U1–U12, H2–H5, the 2026-10-12`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_PUBLIC.md` (U1–U12, H2–H5, the 2026-10-12`
- L94: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-PU-TR_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-PU-TR_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-PU-UX.md` — design=2, workspace=5 (utf-8, LF)
- L13: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L23: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L27: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\PU-UX\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\PU-UX\` (create it if missing).`
- L83: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L84: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes: P1, P4–P9 as`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes: P1, P4–P9 as`
- L85: `they touch the site) and `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_PUBLIC.md` (U1–U12, H2–H5,`
  → `they touch the site) and `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_PUBLIC.md` (U1–U12, H2–H5,`
- L106: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-PU-UX_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-PU-UX_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-PU-VD.md` — design=2, workspace=5 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L24: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L28: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\PU-VD\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\PU-VD\` (create it if missing).`
- L77: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L78: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and`
- L79: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_PUBLIC.md` (U1–U12, H2–H5, the 2026-10-12`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_PUBLIC.md` (U1–U12, H2–H5, the 2026-10-12`
- L97: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-PU-VD_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-PU-VD_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-SH-AX.md` — design=2, workspace=4 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L24: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L31: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\SH-AX\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\SH-AX\` (create it if missing).`
- L77: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L78: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` in full (P7 states, P8 feedback/429,`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` in full (P7 states, P8 feedback/429,`
- L95: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-SH-AX_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-SH-AX_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-SH-CP.md` — design=2, workspace=4 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L25: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L33: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\SH-CP\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\SH-CP\` (create it if missing).`
- L80: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L81: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` in full (especially the P9 verb`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` in full (especially the P9 verb`
- L96: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-SH-CP_REPORT.md`. English, concise`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-SH-CP_REPORT.md`. English, concise`
### `DESIGN\ROUND2\PROMPT\R2-SH-DF.md` — design=2, workspace=4 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L24: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L31: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\SH-DF\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\SH-DF\` (create it if missing).`
- L75: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L76: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` in full (P1–P10 with all Amended`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` in full (P1–P10 with all Amended`
- L91: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-SH-DF_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-SH-DF_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-SH-SUMMARY.md` — design=1, workspace=2 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` only to consult the documents named below. `git fetch`
  → `- Read from `C:\dev\masaha\design` only to consult the documents named below. `git fetch`
- L19: ``D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-SH-UX_REPORT.md`,`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-SH-UX_REPORT.md`,`
- L36: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\SUMMARY\R2-SH_SUMMARY.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\SUMMARY\R2-SH_SUMMARY.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-SH-UX.md` — design=2, workspace=4 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L24: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L30: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\SH-UX\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\SH-UX\` (create it if missing).`
- L85: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L86: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` in full (P1–P10 with all Amended notes`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` in full (P1–P10 with all Amended notes`
- L104: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-SH-UX_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-SH-UX_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\PROMPT\R2-SH-VD.md` — design=2, workspace=4 (utf-8, LF)
- L14: `- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).`
  → `- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).`
- L24: `run with `C:\Users\basel\masaha-design` as the working directory.`
  → `run with `C:\dev\masaha\design` as the working directory.`
- L30: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\SH-VD\` (create it if missing).`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\SH-VD\` (create it if missing).`
- L71: `- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
  → `- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then`
- L72: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` in full (P1–P10 with all Amended`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` in full (P1–P10 with all Amended`
- L89: `Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-SH-VD_REPORT.md`. English, concise.`
  → `Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-SH-VD_REPORT.md`. English, concise.`
### `DESIGN\ROUND2\REMAINING_AR.md` — design=1, workspace=32 (utf-8, CRLF)
- L3: `افتح كل جلسة OpenCode من `C:\Users\basel\masaha-design`. ثلاث جلسات معًا على الأكثر. أرسل الأمر ثم سطر الكتابة على أجزاء.`
  → `افتح كل جلسة OpenCode من `C:\dev\masaha\design`. ثلاث جلسات معًا على الأكثر. أرسل الأمر ثم سطر الكتابة على أجزاء.`
- L12: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-AD-EX.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-AD-EX.md whole and follow it.`
- L15: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-AD-TR.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-AD-TR.md whole and follow it.`
- L18: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-AU-AX.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-AU-AX.md whole and follow it.`
- L22: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-AU-CP.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-AU-CP.md whole and follow it.`
- L25: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-AU-DF.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-AU-DF.md whole and follow it.`
- L28: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-AU-EX.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-AU-EX.md whole and follow it.`
- L32: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-AU-TR.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-AU-TR.md whole and follow it.`
- L35: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-DK-CP.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-DK-CP.md whole and follow it.`
- L38: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-DK-DF.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-DK-DF.md whole and follow it.`
- L42: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-DK-EX.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-DK-EX.md whole and follow it.`
- L45: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-DK-TR.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-DK-TR.md whole and follow it.`
- L48: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-OW-AX.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-OW-AX.md whole and follow it.`
- L52: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-OW-CP.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-OW-CP.md whole and follow it.`
- L55: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-OW-DF.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-OW-DF.md whole and follow it.`
- L58: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-OW-EX.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-OW-EX.md whole and follow it.`
- L62: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-OW-TR.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-OW-TR.md whole and follow it.`
- L65: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-PU-AX.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-PU-AX.md whole and follow it.`
- L68: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-PU-CP.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-PU-CP.md whole and follow it.`
- L72: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-PU-DF.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-PU-DF.md whole and follow it.`
- L75: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-PU-EX.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-PU-EX.md whole and follow it.`
- L78: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-PU-TR.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-PU-TR.md whole and follow it.`
- L82: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-SH-AX.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-SH-AX.md whole and follow it.`
- L85: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-SH-CP.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-SH-CP.md whole and follow it.`
- L88: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-SH-DF.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-SH-DF.md whole and follow it.`
- L92: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-SH-VD.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-SH-VD.md whole and follow it.`
- L97: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-AU-SUMMARY.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-AU-SUMMARY.md whole and follow it.`
- L100: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-PU-SUMMARY.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-PU-SUMMARY.md whole and follow it.`
- L103: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-AD-SUMMARY.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-AD-SUMMARY.md whole and follow it.`
- L106: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-OW-SUMMARY.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-OW-SUMMARY.md whole and follow it.`
- L109: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-DK-SUMMARY.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-DK-SUMMARY.md whole and follow it.`
- L112: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-SH-SUMMARY.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-SH-SUMMARY.md whole and follow it.`
- L117: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-ALL-SUMMARY.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-ALL-SUMMARY.md whole and follow it.`
### `DESIGN\ROUND2\REMAINING_KILO_AR.md` — design=2, workspace=17 (utf-8, LF)
- L3: `ستة عشر تقريرًا. كل تقرير في **جلسة Kilo جديدة** مفتوحة في `C:\Users\basel\masaha-design` (على آخر `main`).`
  → `ستة عشر تقريرًا. كل تقرير في **جلسة Kilo جديدة** مفتوحة في `C:\dev\masaha\design` (على آخر `main`).`
- L9: `Use ONLY the playwright MCP tools to see pages (browser_navigate, browser_resize, browser_take_screenshot, browser_press_key, browser_evaluate, browser_snapshot`
  → `Use ONLY the playwright MCP tools to see pages (browser_navigate, browser_resize, browser_take_screenshot, browser_press_key, browser_evaluate, browser_snapshot`
- L18: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-PU-AX.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-PU-AX.md whole and follow it.`
- L23: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-AU-DF.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-AU-DF.md whole and follow it.`
- L26: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-DK-DF.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-DK-DF.md whole and follow it.`
- L29: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-OW-AX.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-OW-AX.md whole and follow it.`
- L32: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-OW-CP.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-OW-CP.md whole and follow it.`
- L35: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-OW-DF.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-OW-DF.md whole and follow it.`
- L38: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-OW-EX.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-OW-EX.md whole and follow it.`
- L41: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-OW-TR.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-OW-TR.md whole and follow it.`
- L44: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-PU-CP.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-PU-CP.md whole and follow it.`
- L47: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-PU-DF.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-PU-DF.md whole and follow it.`
- L50: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-PU-EX.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-PU-EX.md whole and follow it.`
- L53: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-PU-TR.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-PU-TR.md whole and follow it.`
- L56: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-SH-AX.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-SH-AX.md whole and follow it.`
- L59: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-SH-CP.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-SH-CP.md whole and follow it.`
- L62: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-SH-DF.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-SH-DF.md whole and follow it.`
- L65: `Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\R2-SH-VD.md whole and follow it.`
  → `Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-SH-VD.md whole and follow it.`
### `DESIGN\ROUND2\ROUND2_GENERATOR_PROMPT.md` — design=2, workspace=6 (utf-8, LF)
- L10: `- **Read from** `C:\Users\basel\masaha-design` (a git worktree of the repository, detached at`
  → `- **Read from** `C:\dev\masaha\design` (a git worktree of the repository, detached at`
- L12: `- **Write only into** `D:\masahaWorkspace\DESIGN\ROUND2\`:`
  → `- **Write only into** `C:\dev\masaha\workspace\DESIGN\ROUND2\`:`
- L19: `1. `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` — the lens every reviewer follows: what the`
  → `1. `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` — the lens every reviewer follows: what the`
- L22: `2. `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_*.md` (shared, public, account, admin, owner,`
  → `2. `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_*.md` (shared, public, account, admin, owner,`
- L89: `- **Where:** read from `C:\Users\basel\masaha-design` at `origin/main` (check `git rev-parse HEAD``
  → `- **Where:** read from `C:\dev\masaha\design` at `origin/main` (check `git rev-parse HEAD``
- L95: ``D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\<PART>-<AXIS>\`.`
  → ``C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\<PART>-<AXIS>\`.`
- L106: `- **The report:** `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-<PART>-<AXIS>_REPORT.md`:`
  → `- **The report:** `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-<PART>-<AXIS>_REPORT.md`:`
- L129: ``Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\<file> whole and follow it.``
  → ``Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\<file> whole and follow it.``
### `DESIGN\ROUND2\RUN_SHEET.md` — workspace=1 (utf-8, LF)
- L11: ``Read D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\<file> whole and follow it.``
  → ``Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\<file> whole and follow it.``
### `DESIGN\ROUND2\run-chain.ps1` — workspace=2 (utf-8, LF)
- L2: `# Usage (PowerShell):  & "D:\masahaWorkspace\DESIGN\ROUND2\run-chain.ps1" -After 2 -Until 4`
  → `# Usage (PowerShell):  & "C:\dev\masaha\workspace\DESIGN\ROUND2\run-chain.ps1" -After 2 -Until 4`
- L11: `$root  = 'D:\masahaWorkspace\DESIGN\ROUND2'`
  → `$root  = 'C:\dev\masaha\workspace\DESIGN\ROUND2'`
### `DESIGN\ROUND2\run-queue.ps1` — design=1, workspace=2 (utf-8, LF)
- L5: `# Usage:  & "D:\masahaWorkspace\DESIGN\ROUND2\run-queue.ps1" -Models opencode/big-pickle,opencode/step-5-preview-free`
  → `# Usage:  & "C:\dev\masaha\workspace\DESIGN\ROUND2\run-queue.ps1" -Models opencode/big-pickle,opencode/step-5-preview-free`
- L14: `$root = 'D:\masahaWorkspace\DESIGN\ROUND2'`
  → `$root = 'C:\dev\masaha\workspace\DESIGN\ROUND2'`
- L15: `$repo = 'C:\Users\basel\masaha-design'`
  → `$repo = 'C:\dev\masaha\design'`
### `DESIGN\ROUND2\run-summaries.ps1` — design=1, workspace=2 (utf-8, LF)
- L3: `# Usage:  & "D:\masahaWorkspace\DESIGN\ROUND2\run-summaries.ps1"`
  → `# Usage:  & "C:\dev\masaha\workspace\DESIGN\ROUND2\run-summaries.ps1"`
- L7: `$root  = 'D:\masahaWorkspace\DESIGN\ROUND2'`
  → `$root  = 'C:\dev\masaha\workspace\DESIGN\ROUND2'`
- L8: `$repo  = 'C:\Users\basel\masaha-design'`
  → `$repo  = 'C:\dev\masaha\design'`
### `DESIGN\ROUND2\run-watchdog.ps1` — workspace=2 (utf-8, LF)
- L6: `# Usage:  & "D:\masahaWorkspace\DESIGN\ROUND2\run-watchdog.ps1"`
  → `# Usage:  & "C:\dev\masaha\workspace\DESIGN\ROUND2\run-watchdog.ps1"`
- L13: `$root  = 'D:\masahaWorkspace\DESIGN\ROUND2'`
  → `$root  = 'C:\dev\masaha\workspace\DESIGN\ROUND2'`
### `DESIGN\ROUND2\run-wave.ps1` — design=1, workspace=2 (utf-8, LF)
- L2: `# Usage (PowerShell):  & "D:\masahaWorkspace\DESIGN\ROUND2\run-wave.ps1" -Wave 2`
  → `# Usage (PowerShell):  & "C:\dev\masaha\workspace\DESIGN\ROUND2\run-wave.ps1" -Wave 2`
- L9: `$root    = 'D:\masahaWorkspace\DESIGN\ROUND2'`
  → `$root    = 'C:\dev\masaha\workspace\DESIGN\ROUND2'`
- L10: `$repo    = 'C:\Users\basel\masaha-design'`
  → `$repo    = 'C:\dev\masaha\design'`
### `HANDOFF.md` — app-b=1, app=1, workspace=1 (utf-8, LF)
- L44: `**PR 2 executing** (OpenCode; `feat/admin-add-owner` in `C:\Users\basel\masaha`): the `Combobox` search (its own`
  → `**PR 2 executing** (OpenCode; `feat/admin-add-owner` in `C:\dev\masaha\app`): the `Combobox` search (its own`
- L51: ``C:\Users\basel\masaha-b`), one PR, seven commits, **a migration** (temporary password expiry). Part A protects`
  → ``C:\dev\masaha\app-b`), one PR, seven commits, **a migration** (temporary password expiry). Part A protects`
- L87: ``D:\masahaWorkspace\` (soon `C:\dev\masaha\workspace\`): `WORKER_A\`, `WORKER_B\`, `DESIGN\`, `TASKS\`, `_SHARED\`;`
  → ``C:\dev\masaha\workspace\` (soon `C:\dev\masaha\workspace\`): `WORKER_A\`, `WORKER_B\`, `DESIGN\`, `TASKS\`, `_SHARED\`;`
### `WORKER_A\OWNERS\1_PLAN_PROMPT.md` — app-b=1, app=2, workspace=4 (utf-8, LF)
- L12: `**The task's folder:** `D:\masahaWorkspace\WORKER_A\OWNERS\`. This prompt is `1_PLAN_PROMPT.md`; **save`
  → `**The task's folder:** `C:\dev\masaha\workspace\WORKER_A\OWNERS\`. This prompt is `1_PLAN_PROMPT.md`; **save`
- L17: `**Where you read.** `C:\Users\basel\masaha` (worker A's folder, on `main`, idle): `git fetch origin`, then`
  → `**Where you read.** `C:\dev\masaha\app` (worker A's folder, on `main`, idle): `git fetch origin`, then`
- L19: `check anything out. Worker B is planning PACKAGES in `C:\Users\basel\masaha-b` — never work there.`
  → `check anything out. Worker B is planning PACKAGES in `C:\dev\masaha\app-b` — never work there.`
- L44: `latest `origin/main` in `C:\Users\basel\masaha`; `docker start masaha-postgres-1`, never `db:up`; never`
  → `latest `origin/main` in `C:\dev\masaha\app`; `docker start masaha-postgres-1`, never `db:up`; never`
- L53: ``git merge-tree --write-tree` against any open PR; the report to `D:\masahaWorkspace\WORKER_A\OWNERS\4_REPORT.md`,`
  → ``git merge-tree --write-tree` against any open PR; the report to `C:\dev\masaha\workspace\WORKER_A\OWNERS\4_REPORT.md`,`
- L96: `- **D4 — commit 0, #85's leftovers** (`D:\masahaWorkspace\WORKER_A\_DONE\GALLERY\GALLERY_REPORT.md`,`
  → `- **D4 — commit 0, #85's leftovers** (`C:\dev\masaha\workspace\WORKER_A\_DONE\GALLERY\GALLERY_REPORT.md`,`
- L115: ``D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md` (A4, A5, A6, AD-021, and every amendment at its`
  → ``C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md` (A4, A5, A6, AD-021, and every amendment at its`
### `WORKER_A\OWNERS\2_PLAN.md` — app=2, workspace=3 (utf-8, LF)
- L101: ``masaha/admin.jsx` (`TempPassDialog`, `LinkOwnerDialog`, `unlinkLine`); `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md``
  → ``masaha/admin.jsx` (`TempPassDialog`, `LinkOwnerDialog`, `unlinkLine`); `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md``
- L517: `1. In `C:\Users\basel\masaha`: `git status` clean, on `main`; `git fetch origin`; `git switch main && git pull --ff-only`.`
  → `1. In `C:\dev\masaha\app`: `git status` clean, on `main`; `git fetch origin`; `git switch main && git pull --ff-only`.`
- L543: `- Screenshots to `D:\masahaWorkspace\WORKER_A\OWNERS\shots\pr1\`, `…\shots\pr2\`, `…\shots\pr3\` (the tool saves a relative name in the session's folder: move t`
  → `- Screenshots to `C:\dev\masaha\workspace\WORKER_A\OWNERS\shots\pr1\`, `…\shots\pr2\`, `…\shots\pr3\` (the tool saves a relative name in the session's folder: m`
- L544: `- Stop the servers by PID (`Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine -match 'C:\\Users\\basel\\masaha' }`, `Stop-`
  → `- Stop the servers by PID (`Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine -match 'C:\\dev\\masaha\\app' }`, `Stop-Proc`
- L552: `6. The report, written in parts, UTF-8: PR 1 → `D:\masahaWorkspace\WORKER_A\OWNERS\4_REPORT.md`; PR 2 → `…\OWNERS\4_REPORT_ADD.md`; PR 3 → `…\OWNERS\4_REPORT_LI`
  → `6. The report, written in parts, UTF-8: PR 1 → `C:\dev\masaha\workspace\WORKER_A\OWNERS\4_REPORT.md`; PR 2 → `…\OWNERS\4_REPORT_ADD.md`; PR 3 → `…\OWNERS\4_REPO`
### `WORKER_A\OWNERS\3_EXEC_PROMPT_PR1.md` — app-b=2, app=1, workspace=3 (utf-8, LF)
- L8: `1. Work in `C:\Users\basel\masaha` only — never in `C:\Users\basel\masaha-b` (worker B builds PACKAGES`
  → `1. Work in `C:\dev\masaha\app` only — never in `C:\dev\masaha\app-b` (worker B builds PACKAGES`
- L10: `2. Read the plan **whole**: `D:\masahaWorkspace\WORKER_A\OWNERS\2_PLAN.md` — **the owner's approval at its`
  → `2. Read the plan **whole**: `C:\dev\masaha\workspace\WORKER_A\OWNERS\2_PLAN.md` — **the owner's approval at its`
- L47: ``C:\Users\basel\masaha-b\`; if one does, wait. Focused runs of one or two files are fine.`
  → ``C:\dev\masaha\app-b\`; if one does, wait. Focused runs of one or two files are fine.`
- L55: `on another PR. The real run's screenshots go to `D:\masahaWorkspace\WORKER_A\OWNERS\shots\pr1\` (moved`
  → `on another PR. The real run's screenshots go to `C:\dev\masaha\workspace\WORKER_A\OWNERS\shots\pr1\` (moved`
- L73: `Report: D:\masahaWorkspace\WORKER_A\OWNERS\4_REPORT_PR1.md`
  → `Report: C:\dev\masaha\workspace\WORKER_A\OWNERS\4_REPORT_PR1.md`
### `WORKER_A\OWNERS\3_EXEC_PROMPT_PR2.md` — app-b=2, app=1, workspace=3 (utf-8, LF)
- L8: `1. Work in `C:\Users\basel\masaha` only — never in `C:\Users\basel\masaha-b` (worker B builds PACKAGES`
  → `1. Work in `C:\dev\masaha\app` only — never in `C:\dev\masaha\app-b` (worker B builds PACKAGES`
- L10: `2. Read the plan **whole**: `D:\masahaWorkspace\WORKER_A\OWNERS\2_PLAN.md` — **the owner's approval at its`
  → `2. Read the plan **whole**: `C:\dev\masaha\workspace\WORKER_A\OWNERS\2_PLAN.md` — **the owner's approval at its`
- L60: ``C:\Users\basel\masaha-b\`; if one does, wait. Focused runs of one or two files are fine.`
  → ``C:\dev\masaha\app-b\`; if one does, wait. Focused runs of one or two files are fine.`
- L68: `on another PR. The real run's screenshots go to `D:\masahaWorkspace\WORKER_A\OWNERS\shots\pr2\` (moved`
  → `on another PR. The real run's screenshots go to `C:\dev\masaha\workspace\WORKER_A\OWNERS\shots\pr2\` (moved`
- L86: `Report: D:\masahaWorkspace\WORKER_A\OWNERS\4_REPORT_PR2.md`
  → `Report: C:\dev\masaha\workspace\WORKER_A\OWNERS\4_REPORT_PR2.md`
### `WORKER_A\OWNERS\3b_FIX_PROMPT_PR2.md` — app=1, workspace=1 (utf-8, LF)
- L3: `You are the executor of PR **#89** (`feat/admin-add-owner`, head `8548308e`) in `C:\Users\basel\masaha`.`
  → `You are the executor of PR **#89** (`feat/admin-add-owner`, head `8548308e`) in `C:\dev\masaha\app`.`
- L5: `review waits for this round. Read first: `D:\masahaWorkspace\WORKER_A\OWNERS\2_PLAN.md` (the approval note`
  → `review waits for this round. Read first: `C:\dev\masaha\workspace\WORKER_A\OWNERS\2_PLAN.md` (the approval note`
### `WORKER_A\OWNERS\4_REPORT_PR1.md` — workspace=1 (utf-8, LF)
- L78: `- Cases and what was seen (shots in `D:\masahaWorkspace\WORKER_A\OWNERS\shots\pr1\`):`
  → `- Cases and what was seen (shots in `C:\dev\masaha\workspace\WORKER_A\OWNERS\shots\pr1\`):`
### `WORKER_A\OWNERS\4_REPORT_PR2.md` — app=2, workspace=2 (utf-8, LF)
- L11: `| Working folder | `C:\Users\basel\masaha` only. `git status --short --branch` → `## main...origin/main`, no changes. |`
  → `| Working folder | `C:\dev\masaha\app` only. `git status --short --branch` → `## main...origin/main`, no changes. |`
- L118: `Screenshots moved to `D:\masahaWorkspace\WORKER_A\OWNERS\shots\pr2\` (never committed).`
  → `Screenshots moved to `C:\dev\masaha\workspace\WORKER_A\OWNERS\shots\pr2\` (never committed).`
- L146: `Report: D:\masahaWorkspace\WORKER_A\OWNERS\4_REPORT_PR2.md`
  → `Report: C:\dev\masaha\workspace\WORKER_A\OWNERS\4_REPORT_PR2.md`
- L151: `> Executor: Claude Code, in `C:\Users\basel\masaha`. Appended; the sections above are kept as written,`
  → `> Executor: Claude Code, in `C:\dev\masaha\app`. Appended; the sections above are kept as written,`
### `WORKER_A\OWNERS\5_REVIEW_PROMPT_PR1.md` — design-b=1, workspace=3 (utf-8, LF)
- L5: `another tool. Write your report to `D:\masahaWorkspace\WORKER_A\OWNERS\6_REVIEW_PR1_<YOU>.md``
  → `another tool. Write your report to `C:\dev\masaha\workspace\WORKER_A\OWNERS\6_REVIEW_PR1_<YOU>.md``
- L9: `- **Run from `C:\Users\basel\masaha-design-b`, read only commit objects:** `git fetch origin` and`
  → `- **Run from `C:\dev\masaha\design-b`, read only commit objects:** `git fetch origin` and`
- L19: `The plan `D:\masahaWorkspace\WORKER_A\OWNERS\2_PLAN.md` — the owner's approval at its top, and **PR 1 only**`
  → `The plan `C:\dev\masaha\workspace\WORKER_A\OWNERS\2_PLAN.md` — the owner's approval at its top, and **PR 1 only**`
- L21: ``D:\masahaWorkspace\WORKER_A\OWNERS\4_REPORT_PR1.md`: judge its five departures. Scope: `apps/web`, `docs`.`
  → ``C:\dev\masaha\workspace\WORKER_A\OWNERS\4_REPORT_PR1.md`: judge its five departures. Scope: `apps/web`, `docs`.`
### `WORKER_A\OWNERS\5_REVIEW_PROMPT_PR2.md` — design=1, workspace=2 (utf-8, LF)
- L7: ``D:\masahaWorkspace\WORKER_A\OWNERS\6_REVIEW_PR2_CLAUDE_CODE.md`, in parts: first the verdict and the five`
  → ``C:\dev\masaha\workspace\WORKER_A\OWNERS\6_REVIEW_PR2_CLAUDE_CODE.md`, in parts: first the verdict and the five`
- L11: `- **Run from `C:\Users\basel\masaha-design`, read only commit objects:** `git fetch origin` and`
  → `- **Run from `C:\dev\masaha\design`, read only commit objects:** `git fetch origin` and`
- L23: `The plan `D:\masahaWorkspace\WORKER_A\OWNERS\2_PLAN.md` — the owner's approval note at its top (the`
  → `The plan `C:\dev\masaha\workspace\WORKER_A\OWNERS\2_PLAN.md` — the owner's approval note at its top (the`
### `WORKER_A\OWNERS\7_FIXES_PROMPT_PR2.md` — app=1, workspace=1 (utf-8, LF)
- L3: `To the executor of fix round 1 on PR #89 (`feat/admin-add-owner`, head `a074e6d2`, `C:\Users\basel\masaha`).`
  → `To the executor of fix round 1 on PR #89 (`feat/admin-add-owner`, head `a074e6d2`, `C:\dev\masaha\app`).`
- L4: `The review is `D:\masahaWorkspace\WORKER_A\OWNERS\6_REVIEW_PR2_CLAUDE_CODE.md` — read it whole. The owner`
  → `The review is `C:\dev\masaha\workspace\WORKER_A\OWNERS\6_REVIEW_PR2_CLAUDE_CODE.md` — read it whole. The owner`
### `_SHARED\MAP_AR.md` — app-b=1, app=1 (utf-8, LF)
- L4: `- `A_ADMINLIST` — العامل A (الويب): قائمة مساحات الأدمن، «محذوفة» و«استرجاع». يعمل في `C:\Users\basel\masaha`.`
  → `- `A_ADMINLIST` — العامل A (الويب): قائمة مساحات الأدمن، «محذوفة» و«استرجاع». يعمل في `C:\dev\masaha\app`.`
- L5: `- `B_OWNERSREAD` — العامل B (الواجهة البرمجية): أسماء المالكين في قراءة المساحة. يعمل في `C:\Users\basel\masaha-b`.`
  → `- `B_OWNERSREAD` — العامل B (الواجهة البرمجية): أسماء المالكين في قراءة المساحة. يعمل في `C:\dev\masaha\app-b`.`
### `_SHARED\snapshot.ps1` — workspace=2 (utf-8, LF)
- L1: `# Commits and pushes the day's changes of D:\masahaWorkspace to its private GitHub repository.`
  → `# Commits and pushes the day's changes of C:\dev\masaha\workspace to its private GitHub repository.`
- L5: `Set-Location 'D:\masahaWorkspace'`
  → `Set-Location 'C:\dev\masaha\workspace'`
