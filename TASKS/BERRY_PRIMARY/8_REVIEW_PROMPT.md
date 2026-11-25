# WI-B — the targeted review of PR #158 (read-only)

You are a **read-only reviewer** of PR **#158** in Masaha (bilingual Arabic RTL / English, React 19 + Vite web), branch
`feat/berry-main-action`, head `071e9214fb15438e20fa9103e148a50559cb89cd`, base `main`. Read it with `git`
(`git fetch origin`, `git diff origin/main...071e9214`, `git show <sha>`, `git show 071e9214:<path>`), `gh pr view 158`,
Read, Grep and Glob, from `C:\dev\masaha\app`. **Edit nothing in the repository; check out nothing; run no build, test
or server.** Write only your review file.

## Read first
- ADR 0022 with its *Revised* line (at the head), ADR 0019;
- `C:\dev\masaha\workspace\TASKS\BERRY_PRIMARY\0_OWNER_DECISIONS.md` (A18, B1), `6_PLAN.md` (approved, D1–D7: the desk's
  «تحصيل» rows stay filled ink), `6b_SUPERVISOR_REVIEW.md`, and `7_REPORT.md` (verify its claims, do not trust them).

## Requirements — PASS / WEAK / FAIL each, with `file:line`
- **B1** The role's values are exactly B1: light `spark-600` / white, hover `spark-700`; dark the ink's light step with
  dark text and today's hover — and a test pins dark to the ink's painted values.
- **B2** The criteria are tests in `semantic.unit.test.ts` with 0019's method: text ≥ 4.5 on the fill and on the hover;
  the shape ≥ 3 on `background`, `card` and `popover`; the distance from `destructive` with and without protan and
  deutan, fill and hover, both themes. Each can fail (its named break).
- **B3** Fills only: no `text-`/`border-`/`ring-`/`outline-main-action`; a test holds it. No link or control takes the
  berry; `primary` still draws links, checked controls, Meter, Heatmap, Toast as before.
- **B4** `Button`'s `main` is opt-in; the default stays the ink; `AlertDialogAction` stays ink except its one
  non-destructive caller.
- **B5** **One main action per screen:** walk the plan's §4.3 table and list against the call sites in the diff —
  every screen named has exactly one `main`, the overlays' confirms are `main`, the states / repeats / settings
  cards / directory are not, the desk's «تحصيل» rows stay filled ink. List any call site that differs from the plan,
  any screen left with two `main`s, and any main action the plan named but the diff missed.
- **B6** Nothing in C2's files (PR #157: `features/auth/**`, `pages/site/auth/**`, `SignInPrompt*`,
  `shared/routing/guest/**`, `SpacePage.component.test.tsx`) is touched.
- **B7** ADR 0022's *Revised* line is the approved text word for word, in its own commit; foundation §4, §5, §11, §12
  and the showcase are true of the code; §5's "the spark is never on an action" rewritten as the plan said.
- **B8** Commits: Conventional, subject ≤ 50, a body, no attribution, no `fixup!`, no `#PRNUM`; scope = the plan's files.
- **B9** The report's claims (before / after shots in `C:\Users\basel\Downloads\berry-shots\`, runs, sizes) match the
  code and the CI. Look at four after-shots yourself: the desk 1440 light, the desk dialog, the home 390, the space
  page 1440 light.

## Output
`C:\dev\masaha\workspace\TASKS\BERRY_PRIMARY\9_REVIEW.md`: a one-line verdict (*mergeable*, *after a fix round*, *not
mergeable*); each requirement with its verdict and evidence; findings ranked blocker / should-fix / nit, each with the
smallest fix. Be precise and brief. Then stop.
