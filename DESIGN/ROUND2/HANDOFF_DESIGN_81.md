# Handoff — the design-review supervisor for Issue #81 («مشرف مراجعة التصميم #81»)

**Temporary.** It lives until round 2 is closed (the 40 reviews, the 6 summaries, the summary across all,
`DECISIONS_ROUND2.md` with the owner), then it moves to `_DONE`. You are **one of three supervisors**. The main
supervisor (the project's analyst, reading `C:\dev\masaha\workspace\HANDOFF.md`) reads this file's *Status log*;
the organisation-and-migration supervisor moved these folders on 2026-10-18 (every path below reads
`C:\dev\masaha\…`; the design worktree is `C:\dev\masaha\app-design`, re-created 2026-10-18 detached at
`origin/main`, with no `node_modules` and no `.env`).

## 1. Your task

Run, check and close **design review round 2** for the living prototype in `docs/design/` (read-only reviews
of the designs, not of the app's code). Issue **#81** on GitHub is the owner's checklist: keep it true.

## 2. How you work with the owner

- Reply in **Arabic**, short; no line starts with an English word or a code token; decisions as items with
  options and a recommendation, never tables.
- You **never edit the repository** (`C:\dev\masaha\app*`). You write only in
  `C:\dev\masaha\workspace\DESIGN\` and to Issue #81 (its body), and only with the owner's word for #81.
- **Verify every report yourself before it counts.** Never tick #81 for a report you did not check.

## 3. Where things are

- Prompts: `C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-<PART>-<AXIS>.md` (40) and `R2-<PART>-SUMMARY.md`,
  `R2-ALL-SUMMARY.md`; the browser-pass prompt `R2-BROWSER-PASS.md` (done).
- Reports: `…\ROUND2\REPORT\R2-<PART>-<AXIS>_REPORT.md`; set aside: `REPORT\_superseded\`.
- Captures: `…\ROUND2\shots\r2-shots\<PART>-<AXIS>\<ID>.png`; aborted runs: `shots\_aborted\`.
- The run sheet: `…\ROUND2\REMAINING_KILO_AR.md` — the commands **and the line pasted after each** (its rules).
- Settled decisions, which reviews must not report again: `C:\dev\masaha\workspace\DESIGN\DECISIONS\` (`DECISIONS_*.md`,
  `REVIEW_LENS.md`). Pending desk decisions (not this round's): `C:\dev\masaha\workspace\_SHARED\OPEN_DECISIONS.md`.
- The worktree the reviews read: `C:\dev\masaha\app-design` (detached; keep it on `origin/main`:
  `git fetch origin; git switch --detach origin/main`; first check `git diff --stat <old> origin/main --
  docs/design` — if the design changed, the finished reports may be stale: tell the owner).
- Parts: AD admin · AU sign-in and account · DK desk · OW owner · PU public · SH shared. Axes: AX accessibility ·
  CP content/Arabic copy · DF defects · EX excess · TR truth to product/data/API · UX the way through · VD visual.
  SH has five axes (no EX, TR): **40 reviews**.

## 4. State on 2026-10-18 (Issue #81: 26 done, 14 to do)

- **Done (26):** AD-AX, AD-CP, AD-DF¹, AD-EX², AD-TR, AD-UX¹, AD-VD¹, AU-AX¹, AU-CP³, AU-DF, AU-EX, AU-TR, AU-UX,
  AU-VD, DK-AX¹, DK-CP², DK-EX, DK-TR, DK-UX, DK-VD¹, OW-UX¹, OW-VD¹, PU-AX, PU-UX¹, PU-VD, SH-UX.
  ¹ written from source, then a browser pass appended (2026-10-17). ² source only, accepted for its axis.
  ³ two corrupted lines at its end (model tokens and a stray command) — **removing them needs the owner's word**.
- **To do (14):** DK-DF, OW-AX, OW-CP, OW-DF, OW-EX, OW-TR, PU-CP, PU-DF, PU-EX, PU-TR, SH-AX, SH-CP, SH-DF, SH-VD
  (some may already be running in Kilo sessions the owner opened — ask).
- Then: the six part summaries, then `R2-ALL-SUMMARY`; then the owner and you write
  `C:\dev\masaha\workspace\DESIGN\DECISIONS_ROUND2.md`; then the fix batch(es) of `docs/design/` (Claude plans,
  OpenCode builds, another tool reviews), **the first one fixing the stray `<<<<<<< HEAD` line before § 54 in
  `docs/design/INDEX.md`**; then `docs/design/screens/` regenerated once and the owner reviews every screen.

## 5. The tool and the method that work (learned 2026-10-17/18)

- **Kilo CLI** (`kilo`), with the Playwright MCP server in `C:\Users\basel\.config\kilo\kilo.jsonc`
  (`kilo mcp list` → connected). **Pick a strong model by name, never "Auto"**: the first PU-AX try on Auto
  was rejected; the second, with a named model and the strict line, passed. OpenCode has the same Playwright
  config (`C:\Users\basel\.config\opencode\opencode.json`); free small models there do not call tools.
- One review per **new session**, opened in `C:\dev\masaha\app-design`, three at a time at most; paste the
  command and the line from `REMAINING_KILO_AR.md` in the same message.
- `main` moves with every merge of workers A and B: the line tells the reviewer to continue when
  `git diff --quiet HEAD origin/main -- docs/design` exits 0. Still move the worktree to `origin/main` between
  batches.

## 6. How to check a report (every one, before #81)

1. The six sections: SHAs, verdict, five points, issues, decisions in doubt, what was not reviewed.
2. No "no browser", "not performed", "unverified", "ensure", "must be" as an issue — each issue states an
   **observed** fact with its measured value.
3. **Each issue has its own capture** of its own frame (open one or two PNGs to see they are real and
   distinct; check sizes); evidence paths exist.
4. **Re-check at least one defect in the prototype's source** (`docs/design/prototype/*.html`, `masaha/*.jsx`) —
   e.g. PU-AX's skip link to `#main` that no public page defines was confirmed this way.
5. Clean the worktree: reviewers sometimes save captures or notes inside `masaha-design`. Compare with the
   workspace copies (`cmp`); move uniques to the review's `shots` folder; remove only verified duplicates;
   `git status --short` empty.
6. A weak report: move it to `REPORT\_superseded\` (and its captures to `shots\_aborted\<id>-tryN\`), never
   delete; rerun with a stronger model.
7. Tick #81: fetch the body (`gh issue view 81 --json body --jq .body > file`), change the line and the count
   with a **Python script file** (never inline shell with Arabic or em dashes — they get mangled), `gh issue
   edit 81 --body-file file`, then read the line back and check no `�`.

## 7. Done means

40 reviews checked and ticked, the summaries written and checked, `DECISIONS_ROUND2.md` agreed with the owner,
#81 updated at each step; then the fix batches belong to the main supervisor's planning (you hand over the
decisions file). Then this file moves to `_DONE` and `HANDOFF.md` gets one line.

## Status log (append one dated line per step; newest last)

- 2026-10-18 — created by the analyst; 26 of 40 done; Kilo + Playwright proven on PU-AX (2nd try) and AU-DF.
- 2026-10-18 — AU-CP: the two corrupted end lines removed with the owner's word (backup in the session scratchpad); DK-DF and OW-AX handed to Kilo.
- 2026-10-18 — OW-CP handed to Kilo (third parallel session).
- 2026-10-18 — DK-DF try1 rejected (scope half-covered: no English, dark, fail/state matrix or My payments; 002 and 003 share one capture; 002 false — submit at the sheet's bottom with a plan chosen; 004 tabs not cramped and its quoted labels invented; 005 not an issue); set aside, to rerun with a stronger model.
- 2026-10-18 — OW-AX try1 rejected (1440 only, 390/768 left out; 001 and 003 share one capture, 11 of 13 captures unused; 004 and 005 are not issues; garbled heading text); set aside, to rerun with a stronger model.
- 2026-10-18 — OW-CP try1 rejected: 001 false (a6 carries no `extended` in owner-data.js, only a4 does; by source the dialog opens), 002 false (مدّد is also the imperative, same spelling); the extension dialog copy left unreviewed. Set aside, to rerun with a stronger model.
- 2026-10-18 — OW-CP try2 rejected: 25 issues, 15 captures (10 issues cite "captured in review"); captures show other frames (009 settings issue shows Announcements, 003 void issue shows Overview); 017 and 022 not issues. Its 009 capture shows a6 with «تمديد الاشتراكات», confirming try1 001 false. Set aside.
