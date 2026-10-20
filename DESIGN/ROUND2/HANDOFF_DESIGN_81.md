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
- 2026-10-19 — after the move: #81 body paths updated (49 workspace, 1 worktree; read back, no bad characters); DK-DF and OW-AX handed to Kilo afresh.
- 2026-10-19 — OW-AX try2 (OpenCode, Nemotron 3 Ultra Free) rejected: no capture written at all (browser session lost); 002–009 count visible-text buttons as nameless (aria-label null is not a missing name); 44px targets measured without a touch pointer (foundation: 40px, 44px on pointer coarse). Set aside. Stray app-design/r2-shots-tmp/ (5 desk PNGs) left for the running DK-DF session.
- 2026-10-19 — OW-AX try3 rejected: the same text as try2 (one space differs), 2 captures for 20 issues. Set aside. Desk PNGs (_deskdark, _desken, _mypay, _search390) misfiled in shots/r2-shots/OW-AX and R2-DK-DF-test*.png in app-design: left for the running DK-DF session.
- 2026-10-19 — PU-CP (Claude Code; headless Chrome over CDP, the extension's browser is a Mac that cannot reach this PC) checked: six sections, 24 issues with 24 distinct checked captures, widths as the prompt names; 001 and 004 re-checked in source (PRIVACY_LINE in the denied alert, location.jsx:46; fixed resultsLabel, shared.jsx:621). Accepted; #81 tick awaits the owner.
- 2026-10-19 — #81 ticked with the owner's word: PU-CP done (27 done, 13 to do); the AU-CP line now says its corrupted lines were removed. Read back, no bad characters.
- 2026-10-20 — OW-AX, OW-DF, OW-EX (one Claude Code dispatcher, three parallel subagents, headless Chrome over CDP) checked: six sections each; 15/15, 15/16 (007 has two), 18/18 issues/captures, no duplicate captures, ports free; source re-checks: OW-AX 001 (no Skeleton on Finance/Settings, DataTable pages have it) and 002 (<title> Arabic only); OW-DF 011 capture shows «ممتلئ» checked under «متاح»; OW-EX 010 capture shows "shown once" twice. Accepted; #81 tick awaits the owner.
- 2026-10-20 — #81 ticked with the owner's word: OW-AX, OW-DF, OW-EX (30 done, 10 to do); read back, no bad characters. The stalled DK-DF session closed by the owner's word: its 6 stray PNGs (4 in shots/r2-shots/OW-AX, 2 in app-design) moved to shots/_aborted/DK-DF-try2; app-design clean. The owner declined a 5-subagent batch (token cost); next: a split method for cheaper workers.
- 2026-10-20 — split method built: tools/r2-pack.mjs (headless Chrome over CDP; per frame a viewport PNG, a full PNG and measured facts), SLICE.md, MERGE.md, r2-finalize.mjs. PU-DF pack: 55 URLs x 3 widths x ar/en x light/dark = 660 frames, 0 failed, 84 MB; lang/theme checked on all; its probe repeats PU-CP 024 (Sort label clipped). Slices S1-S5 handed to the owner.
- 2026-10-20 — PU-DF S1, S2 try1 rejected (text-only model: no image viewed; S1 judged from source, S2 restated the script's one lead). SLICE.md now gates on viewing an image and forbids source. Set aside in slices/_rejected.
- 2026-10-20 — SLICE.md and MERGE.md open with "This is not a Work Item": no project skills, no branch, plan, commit, PR or issue.
- 2026-10-20 — PU-DF S2 try2 checked: gate true (header matches B09-390-ar-light), one finding (Sort label clipped), true; thin but kept. S1 try2 not written yet. Pack gap found by the supervisor: the inverted price range only shows inside the filters; B56 (sheet=filters, priceMin 30 > priceMax 10) rendered (12 frames) and appended to index/summary; it goes to S3.
- 2026-10-20 — a slice worker ran start-work-item (session opened where the repo's CLAUDE.md applies) and stopped on HEAD != origin/main without judging. app-design moved to origin/main 7d48c9c3 (docs/design unchanged since 18ab170, so the PU-DF pack stands). Slice commands now carry the not-a-Work-Item line themselves.
- 2026-10-20 — PU-DF S3 try1 rejected: viewed only the gate image, restated the script's two leads, B56's inverted-range state not judged. Cause: ~190 images per slice is too many for a worker; contact sheets next.
- 2026-10-20 — contact sheets added (tools/r2-sheets.mjs: per base and width, the 4 frames side by side, first screen and whole page; 6 sheets per base). SLICE.md: open all six sheets per base, list them under "Sheets opened". PU-DF re-cut into 10 slices of 3-7 bases (S1-S10); old S2 (thin, old slicing) set aside.
- 2026-10-20 — PU-DF S1 try2 (old instructions) set aside: one finding (a bottom toast over a card at 390 — the usual transient toast, weak for DF), "Not judged: none" over 96 frames with no list of what was opened. Redone in the new 10-slice cut.
- 2026-10-20 — PU-DF sheets complete: 336 (6 per base for B01-B56), 40 MB, B56-768 checked readable. 10 slice commands handed to the owner.
