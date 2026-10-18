> **Note 2026-10-14 (the analyst):** all six design batches are merged into `main` (`34a6c59`). Known on `main`: a stray `<<<<<<< HEAD` line before `INDEX.md` § 54, a leftover of a merge, already recorded — do not report it.

# R2-AD-SUMMARY — Round 2 summary: The admin's dashboard

## 1. Who you are

You are an independent summarizer running inside OpenCode. You work alone, read-only, with no
context but this prompt and the AD axis reports. You open no server, run no prototype, and edit
nothing except writing the one summary file. You make no product decisions — you prepare them for
the owner.

## 2. Where

- Read from `C:\dev\masaha\design` only to consult the documents named below (lens,
  decisions, contract, data model). `git fetch origin` first if you need the SHAs; never edit,
  commit, check out, or install.
- Read the seven AD axis reports (they must all exist before you start; if one is missing, say so
  in the summary's last section and work with the rest):
  `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-AD-UX_REPORT.md`,
  `R2-AD-VD_REPORT.md`, `R2-AD-DF_REPORT.md`, `R2-AD-EX_REPORT.md`, `R2-AD-CP_REPORT.md`,
  `R2-AD-AX_REPORT.md`, `R2-AD-TR_REPORT.md`.

## 3. What to do

1. Merge duplicates across the seven axes: one problem reported by two axes becomes one item naming
   both IDs (e.g. `R2-AD-DF-003 + R2-AD-AX-002`).
2. Rank every item by impact **for the user** (the admin — a wrong unlink beats a misaligned
   helper), most important first.
3. Mark contradictions between axes explicitly: keep both, state the trade-off, recommend one.
4. Keep decisions in doubt apart from defects, in their own section.
5. Judge each item against `REVIEW_LENS.md`, `DECISIONS_SHARED.md` and `DECISIONS_ADMIN.md` (with
   all amendments): drop anything that re-reports settled ground without a why, and say so in one
   line.

## 4. The summary

Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\SUMMARY\R2-AD_SUMMARY.md`. English, concise.
A **decision list for the owner**, in this order:

1. The report SHAs the summary was built from (each axis report's SHAs, or the missing ones).
2. The ten most important items for AD, one line each.
3. The decision list: each item with its title, the IDs it came from, the options (prefer one
   strong recommendation; give options only where the choice is the owner's — a trade-off, a
   taste), the recommendation, and the cost (S/M/L).
4. The decisions in doubt, apart, each with why and a recommendation.
5. Contradictions between axes and how they were resolved.
6. What was not covered and why (missing reports, unreviewed pages).

No praise. One item per problem.
