# WORKSPACE — copy the Masaha working files into `D:\masahaWorkspace`, arranged by task

You are a careful file clerk for the owner of the Masaha project. You **copy** working files (prompts,
plans, reports, reviews, screenshots) from where they are scattered today into one new tree arranged by
task. **Nothing is moved, renamed in place, edited or deleted at the source** — two workers are still
using the sources; the new tree is adopted only after they finish.

**Two phases. Phase 1 writes a plan of every copy and STOPS for the owner's approval. Phase 2 copies and
verifies.** Never start Phase 2 without the owner's explicit "approved" in this conversation.

## 0. Hard rules

- **Sources are read-only.** No `mv`, `rm`, `Move-Item`, `Remove-Item`, rename or write under any source.
- **Write only under `D:\masahaWorkspace`.** It is empty now; if it is not empty when you start, stop and
  say what is there.
- **Never touch a repository folder** (`C:\Users\basel\masaha`, `masaha-b`, `masaha-design`,
  `masaha-design-b`): not a read, not a write. Nothing from them is copied.
- **Never overwrite** a file in the target: a name collision is an error to resolve in Phase 1.
- **Never open a file to print it.** You need names, sizes and hashes; read a file's text only to find a
  PR number (§3, rule R4), and print no more than the matching line.
- **Do the copying with one script** (Python, `-I`, saved under `D:\masahaWorkspace\_SHARED\MIGRATION\`),
  driven by the manifest — not by many hand-typed commands. `shutil.copy2` (keeps timestamps).
- No git, no GitHub writes. `gh pr view <n> --json number,title,headRefName` (read) is allowed for R4.
- Paths contain spaces and may contain Arabic; quote every path; write files as UTF-8.

## 1. The sources (and only these)

| Key | Source | What it holds |
|---|---|---|
| S1 | `C:\Users\basel\.prompt\` | `HANDOFF.md`; `MASAHA_WORKER_A\`, `MASAHA_WORKER_B\` (`PLAN\`, `PROMPT\`, `REPORT\`, B's `files\`); `MASAHA_AMENITIES\`, `MASAHA_MEDIA\` (one-off tasks); `MASAHA_DESIGN\` (`DECISIONS_*.md`, `REVIEW_LENS.md`, `PLAN\`, `PROMPT\`, `REPORT\`, `ROUND2\`) — about 308 files |
| S2 | `C:\Users\basel\Downloads\masaha-next\` | the per-task prompt kits: `A_ADMINLIST`, `A_GALLERY`, `B_OWNERSREAD`, `B_MANAGE`, `B_HARDEN`, `WORKSPACE` (this prompt), and `MAP_AR.md` |
| S3 | `C:\Users\basel\Downloads\masaha-handoffs\` | older handoffs |
| S4 | `C:\Users\basel\Downloads\masaha-prompts-archive-2026-10-08\` | an older archive, kept as it is |
| S5 | `C:\Users\basel\Downloads\*-shots\` (every folder whose name ends in `-shots`) | screenshots, about 128 MB in all |

Nothing else (no other Downloads file, no `.zip`, `.csv` or `.png` loose in Downloads).

## 2. The target layout

```
D:\masahaWorkspace\
  README.md            the layout and its rules (§4) — you write it
  BOARD.md             one line per task: group, task, status, PR(s), sources — you write it
  HANDOFF.md           copy of S1's HANDOFF.md
  _SHARED\
    HANDOFFS\          S3, as it is
    ARCHIVE_2026-10-08\  S4, as it is (its inner tree kept)
    MAP_AR.md          S2's MAP_AR.md
    MIGRATION\         manifest.csv, MAPPING.md, copy.py, VERIFY.md
    UNSORTED\          anything no rule places, under its source key and relative path
  WORKER_A\
    GALLERY\           active
    _DONE\<TASK>\      finished tasks
  WORKER_B\
    HARDEN\            active
    _DONE\<TASK>\
  DESIGN\
    DECISIONS\         DECISIONS_*.md and REVIEW_LENS.md (reference, not a task)
    ROUND2\            active — S1's MASAHA_DESIGN\ROUND2 whole, its inner tree kept
    _DONE\<TASK>\      the design fix batches and their reviews
  TASKS\
    _DONE\AMENITIES\   S1's MASAHA_AMENITIES
    _DONE\MEDIA\       S1's MASAHA_MEDIA
```

Inside a task folder: the task's files **with their original names**, flat; S2's kit for the task in
`kit\`; its screenshots in `shots\<the shots folder's name>\`. **Active tasks:** `WORKER_A\GALLERY`,
`WORKER_B\HARDEN`, `DESIGN\ROUND2`. Every other task goes under its group's `_DONE`.

## 3. The rules that place a file (apply in order; record the rule used for every file)

- **R1 — task by name.** A file in a `PLAN\`, `PROMPT\`, `REPORT\` or `files\` folder of
  `MASAHA_WORKER_A`, `MASAHA_WORKER_B` or `MASAHA_DESIGN` — **except a name starting with `REVIEW`,
  which R4 places** — belongs to the task named by its file name's
  stem: the name minus a known suffix — `_PROMPT`, `_PLAN`, `_PLAN_REPLY`, `_REPORT`, `_FIXES`,
  `_FIXES2`, `_EXEC`, `_ADDITION`, `_ADDITION2`, `_BUILD`, `_SHOTS_REPLY`, `_BROWSER_REPORT`,
  `_BROWSER_ROUND2_REPORT`, `_PR_BODY`, `_REPORT_PART1`, `_FIXES_REPORT`, `-copilot-draft` (and its
  extension). Example: `ADMINLIST_BROWSER_ROUND2_REPORT.md` → task `ADMINLIST`;
  `MANAGE-copilot-draft.patch` → `MANAGE`. The group is the source folder's worker (A → `WORKER_A`,
  B → `WORKER_B`, DESIGN → `DESIGN`).
- **R2 — design reference.** `MASAHA_DESIGN\DECISIONS_*.md` and `REVIEW_LENS.md` → `DESIGN\DECISIONS\`.
  `MASAHA_DESIGN\ROUND2\**` → `DESIGN\ROUND2\` with its inner paths.
- **R3 — one-off tasks.** `MASAHA_AMENITIES\**` → `TASKS\_DONE\AMENITIES\` and `MASAHA_MEDIA\**` →
  `TASKS\_DONE\MEDIA\`, **flat** (their `PLAN\`, `PROMPT\`, `REPORT\` files side by side; a name collision
  stops you).
- **R4 — reviews by PR number.** A file named `REVIEW<n>…` (e.g. `REVIEW57_CODEX_REPORT.md`,
  `REVIEW74_FIXES.md`, `REVIEW64B_PROMPT.md`) belongs to the task whose **PR is #n**. Find it: the
  task's own report names its PR (`grep` for `#<n>` or `pull/<n>` in that worker's or that folder's
  `*_REPORT.md`), or `gh pr view <n> --json title,headRefName` matched to a task. Known:
  **#82 → OWNERSREAD, #83 → MANAGE, #84 → ADMINLIST.** `REVIEW_MANAGE_*` → MANAGE.
  `REVIEW82-83_*` → **MANAGE** (the later of the two; BOARD notes it covers #82 too).
  `REVIEW_ACCOUNT_*`, `REVIEW_ADMIN_*`, `REVIEW_DESK_*` and the like in `MASAHA_DESIGN` → the matching
  `FIX_…` task if its name says so, else a task named after them under `DESIGN\_DONE\`. If R4 cannot
  decide with evidence, the file goes to `_SHARED\UNSORTED\` — never a guess.
- **R5 — kits.** `S2\A_<TASK>\**` → `WORKER_A\<TASK>\kit\` (or `WORKER_A\_DONE\<TASK>\kit\` when the task
  is done); `S2\B_<TASK>\**` → the same under `WORKER_B`. `S2\WORKSPACE\**` → `_SHARED\MIGRATION\kit\`.
- **R6 — screenshots.** An `S5` folder goes whole to `<task>\shots\<folder name>\` **only** when its name
  names a task in an evidence-backed way: `adminlist-shots` → ADMINLIST, `gallery-shots` → GALLERY,
  `media-shots` → MEDIA, `amenities-shots` → AMENITIES, `r2-shots` → `DESIGN\ROUND2`, `s2b4a-shots` →
  the task whose plan is `S2B4A_PLAN.md`, and so on for `s2b3a`, `s2b3b`, `s2b4b`, `webbase`; `pr<n>-shots`
  by R4's PR rule; `review-desk-shots` → the desk review's task. **Any other** (`wi7-shots`, `f10-shots`,
  `ds1-shots`, `f5b…`, `s2a…`, …) → `_SHARED\UNSORTED\S5\<folder name>\` unless a report names that folder
  (grep the reports for the folder name; that report's task wins).
- **R7 — everything else** → `_SHARED\UNSORTED\<source key>\<relative path>`.

## 4. Phase 1 — the plan of every copy (then STOP)

1. Check `D:\masahaWorkspace` is empty. Create only `D:\masahaWorkspace\_SHARED\MIGRATION\`.
2. List every file under S1–S5 (recursively), with size and SHA-256.
3. Apply §3 to each. Write `manifest.csv` (UTF-8): `source,size,sha256,target,rule,evidence` — one row per
   file; `evidence` is the line or PR lookup that decided R4 or R6, else empty.
4. Check: every source file has exactly one row; no two rows share a target; no target is outside
   `D:\masahaWorkspace`; every target path is under 240 characters.
5. Write `MAPPING.md`: the counts per source key and per target folder; **the task list** (group, task,
   active/done, PR(s) where known); every `UNSORTED` row and why; every R4/R6 decision with its evidence;
   anything you were unsure of.
6. **Stop.** Reply with: the total files and bytes, the task list, the count in `UNSORTED`, and the
   questions you have. Wait for the owner's "approved" (or corrections — then redo steps 3–6).

## 5. Phase 2 — copy and verify (only after "approved")

1. `copy.py` reads `manifest.csv`, creates folders, copies each row with `shutil.copy2`, and **fails on
   any existing target** (no overwrite).
2. Verify, in the same script or a second one: every target exists, its size and SHA-256 equal the
   manifest's; the number of files under `D:\masahaWorkspace` (minus `_SHARED\MIGRATION\`) equals the
   manifest's rows.
3. Re-hash every source. For a **done** task's source, any change is an error: report it. For an
   **active** task's source (GALLERY, HARDEN, ROUND2), a change is expected (the workers are writing):
   list each changed file — its copy is a snapshot of before.
4. Write `VERIFY.md` (counts, mismatches — expected zero — and the active files that changed).
5. Write `README.md` (§2's layout; the rules: one folder per task; active tasks beside `_DONE`; a
   finished task's folder is moved into `_DONE`; **new tasks name their files by the cycle** —
   `1_PLAN_PROMPT.md`, `2_PLAN.md`, `3_EXEC_PROMPT.md`, `4_REPORT.md`, `5_REVIEW_PROMPT.md`,
   `6_REVIEW_<TOOL>.md`, `7_FIXES_PROMPT.md`, `8_MERGE.md`, `shots\`; **old tasks keep their original
   names**; **the sources stay authoritative until the owner adopts this tree**).
6. Write `BOARD.md` from `MAPPING.md`'s task list: `group · task · active|done · PR(s) · where it came from`.
7. Reply: the counts, zero mismatches (or each one), the active files that changed, and that no source
   was touched.

## 6. Stop and ask

- `D:\masahaWorkspace` not empty at the start; a source missing; any name collision; a file R1–R6 places
  in two tasks; more than 20 files in `UNSORTED`; any copy or hash mismatch; any change to a done task's
  source. Never "fix" these by guessing.
