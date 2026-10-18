# R2-AD-EX — Round 2 review: the admin's dashboard · Excess and simplification («الزوائد»)

## 1. Commit SHAs

- `HEAD`: `34a6c59aab049e8f2992b29b88c8a700b926ddba`
- `origin/main`: `a82541b1435366854d253f88cfe9258f87d36b8d`

> **The two SHAs differ.** Per §2 of the prompt, this is recorded in §6 below.

## 2. Verdict

The admin dashboard is lean; the clearest remaining excess is the owner–space relationship listed in full on two pages, plus a few duplicated details in pickers and sheets that a design reviewer would simplify.

## 3. The five most important points

1. The owner–space relationship is listed in full on both the spaces and owners pages.
2. The add-owner sheet's space picker repeats each space's status and owner list.
3. The stale/missing fact appears in four representations across the overview and spaces pages.
4. The unlink action is reachable from both the spaces dropdown and the editor's read-only alert.
5. The reports sheet's current-value box repeats what the linked editor shows.

## 4. Issues

### R2-AD-EX-001 — Owner names duplicated across the spaces and owners pages

- **Type:** improvement
- **Level:** pattern
- **Impact:** medium
- **Where:** `Admin spaces.html` (frame 43, 1440 ar) and `Admin owners.html` (frame 44, 1440 ar)
- **Evidence:** `R2-AD-EX-001.png` (spaces owners column + owners linked-spaces chips)
- **What is wrong:** The spaces table lists every owner name in a row (`owners(s)` joined), and the owners page lists every linked space name as chips per owner. The same relationship is read in full on both pages.
- **Proposal:** On the spaces table, keep the owner names (the space's editors). On the owners page, replace the per-space chip list with a count badge («مساحتان») that links to the spaces page filtered by that owner.
- **Why it is better:** The owner sees one number instead of scanning the same names they already saw on the spaces page; the detail is one click away.
- **Cost:** S
- **Rule:** A6 (owners page stays, with links) — in doubt whether the chips must be the full list.

### R2-AD-EX-002 — «عرض (يعدّلها المالك)» and «تعديل» lead to the same editor URL

- **Type:** defect
- **Level:** component
- **Impact:** low
- **Where:** `Admin spaces.html` row dropdown (frame 43, 1440 ar)
- **Evidence:** `R2-AD-EX-002.png`
- **What is wrong:** For a verified space the dropdown says «عرض (يعدّلها المالك)»; for unverified it says «تعديل». Both hrefs are `Admin space edit.html?id=…`. The label changes, the destination does not.
- **Proposal:** One item, «تعديل» (or «عرض»), regardless of status; the page itself already signals read-only vs edit in its banner.
- **Why it is better:** The admin does not have to parse a status-dependent label to find the editor.
- **Cost:** S
- **Rule:** none; the label is decoration without meaning (axis §4.4).

### R2-AD-EX-003 — Stale/missing badges shown four times

- **Type:** improvement
- **Level:** page
- **Impact:** medium
- **Where:** `Admin overview.html` tile + «اكتمال البيانات» card, `Admin spaces.html` «الحداثة» column, and the «قديمة أو ناقصة» chip (frames 42–43, 1440 ar)
- **Evidence:** `R2-AD-EX-003.png`
- **What is wrong:** The overview tile counts stale/missing, the card lists each with badges, the table repeats the same badges per row, and the chip filters to them. The same fact (which groups are stale) is written four times.
- **Proposal:** Keep the chip (A7) and the table badges (the per-group detail). In the overview card, drop the badges and keep only the space name and its «تعديل» button — the badges are already in the row the card links to.
- **Why it is better:** The card becomes a queue of names, not a second table; the admin reads the detail where they act on it.
- **Cost:** S
- **Rule:** A8 (the tile and card count stale **and** missing) — in doubt whether the card must repeat the per-group badges.

### R2-AD-EX-004 — Add-owner sheet's space picker repeats the spaces list

- **Type:** improvement
- **Level:** component
- **Impact:** low
- **Where:** `Admin owners.html?sheet=add` space combobox (frame 44, 1440 ar)
- **Evidence:** `R2-AD-EX-004.png`
- **What is wrong:** Each option shows the space name, its status badge, and its current owner names. The admin already has the spaces list; the picker asks for one name.
- **Proposal:** Show the space name and its status badge only; drop the owner names.
- **Why it is better:** The picker stops restating the spaces table; the choice is by name, and the badge still warns when a space is already verified.
- **Cost:** S
- **Rule:** none; text that repeats the list (axis §4.4).

### R2-AD-EX-005 — Unlink reachable from two pages

- **Type:** improvement
- **Level:** pattern
- **Impact:** low
- **Where:** `Admin spaces.html` row dropdown (per-owner «فك ربط») and `Admin space edit.html?id=…` read-only alert (per-owner «فك ربط») (frames 43, 1440 ar)
- **Evidence:** `R2-AD-EX-005.png`
- **What is wrong:** The same unlink action is offered in the spaces dropdown and again in the verified-space editor's alert.
- **Proposal:** Keep it in the spaces dropdown (the list that owns the action); in the editor alert, replace the per-owner link with a single «المساحات» breadcrumb back to the filtered list.
- **Why it is better:** One place to unlink; the editor stays a read-only view and does not grow action links.
- **Cost:** S
- **Rule:** A4 (one item per owner in the dropdown) — in doubt whether the editor should repeat it.

## 5. Decisions in doubt

- **A6** — the owners page shows each owner's links as full chip names. The same names appear in the spaces table. A count badge with a filter link would keep A6's intent (the page shows the links) without restating the list.
- **A8** — the overview card repeats the per-group stale/missing badges that the table already shows. The card's job is the queue, not the detail.

## 6. What was not reviewed, and why

- **HEAD ≠ origin/main** (§2): the worktree is at `34a6c59aab049e8f2992b29b88c8a700b926ddba`, origin/main is at `a82541b1435366854d253f88cfe9258f87d36b8d`. The review read the worktree as it stands; the two may differ in content.
- **No server or screenshots:** this environment has no browser or screenshot tool, so the pages were read as source at 1440 Arabic light. Evidence captures (`C:\Users\basel\Downloads\r2-shots\AD-EX\`) are named per issue but not captured; each «where» names the frame, URL and mode to open on port 5418.
- **Other prompts' axes** (UX, VD, DF, CP, AX, TR) and the *Not in v1* list were not reviewed, per §5.
