# masahaWorkspace

The Masaha working files, arranged by task. **Adopted on 2026-10-17: this tree is authoritative.**

It was copied from the old places (SHA-256 verified), then synced once at adoption. The old places —
`C:\Users\basel\.prompt\` and `C:\Users\basel\Downloads\masaha-next\` — are **frozen** (each holds a
`FROZEN.md`) and are never written again. ROUND2's prompts and scripts were rewritten to point here;
its reports and logs keep their old paths as records.

```
README.md            this file
BOARD.md             one line per task: group, task, status, PR(s), sources
HANDOFF.md           copy of the latest handoff
_SHARED\
  HANDOFFS\          older handoffs
  ARCHIVE_2026-10-08\  the older archive, its inner tree kept
    shots\           14 older shots folders (ds1, f10, f5b2, f5b3a, f5b3b, f5b3c2, f6b, f6c2,
                     s2a2, s2a3, wi-f5b3c1, wi7, wi8, wi9), dated 2026-09-28 to 2026-10-07,
                     before the archive date, so they went here whole
  MAP_AR.md
  MIGRATION\         manifest.csv, MAPPING.md, VERIFY.md, plan.py, copy.py, kit\
  UNSORTED\          nothing placed here in this copy
WORKER_A\            GALLERY (active), _DONE\<TASK>\
WORKER_B\            HARDEN (active), _DONE\<TASK>\
DESIGN\              DECISIONS\ (reference), ROUND2\ (active), _DONE\<TASK>\
TASKS\_DONE\         AMENITIES, MEDIA
```

## Rules

- One folder per task. A task folder holds its files flat, its prompt kit in `kit\`, and its screenshots in `shots\<folder name>\`.
- Active tasks sit beside `_DONE`. When a task finishes, move its folder into its group's `_DONE`.
- **New tasks name their files by the cycle:** `1_PLAN_PROMPT.md`, `2_PLAN.md`, `3_EXEC_PROMPT.md`, `4_REPORT.md`, `5_REVIEW_PROMPT.md`, `6_REVIEW_<TOOL>.md`, `7_FIXES_PROMPT.md`, `8_MERGE.md`, `shots\`.
- **Old tasks keep their original names.**
- Reviews sit in the folder of the task whose PR they review. `REVIEW82-83_*` is in MANAGE (it covers #82 too).
- `REVIEW_ADMIN` is its own folder under `DESIGN\_DONE`: it is the review behind FIX_ADMIN_EDITOR and FIX_ADMIN_REST.
- Rule used for each copied file: see `_SHARED\MIGRATION\manifest.csv` (`rule`, `evidence`).
