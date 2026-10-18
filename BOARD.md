# BOARD

`group · task · active|done · PR(s) · where it came from`

PRs come from the reports and from `gh pr list --state merged` (branch match). "open" = not merged yet. A blank PR means no evidence.

## WORKER_A

- WORKER_A · OWNERS · active · — · begun in the workspace (`1_PLAN_PROMPT.md`): the owners page, adding and linking an owner, the editor naming its owners (closes finding 59); USERS follows
- WORKER_A · GALLERY · done · #85 (merged 2026-10-17; synced at adoption: REVIEW85, the report's fixes section, 5_FIXES_PROMPT) · S1 MASAHA_WORKER_A, S2 A_GALLERY, S5 gallery-shots
- WORKER_A · ADMINLIST · done · #84 · S1 MASAHA_WORKER_A, S2 A_ADMINLIST, S5 adminlist-shots
- WORKER_A · S2B3A · done · #50 · S1 MASAHA_WORKER_A, S5 s2b3a-shots
- WORKER_A · S2B3B · done · #57 · S1 MASAHA_WORKER_A, S5 s2b3b-shots
- WORKER_A · S2B4A · done · #74 · S1 MASAHA_WORKER_A, S5 s2b4a-shots
- WORKER_A · S2B4B · done · #79 · S1 MASAHA_WORKER_A, S5 s2b4b-shots
- WORKER_A · WEBBASE · done · #68 · S1 MASAHA_WORKER_A, S5 webbase-shots

## WORKER_B

- WORKER_B · PACKAGES · in review · #87 (CI green, CLEAN; review prompt 5_REVIEW_PROMPT.md) · the owner's packages API, step 5b
- WORKER_B · STAFF · approved, waits for #87 · — · 2_PLAN.md approved 2026-10-18 (one PR, a migration: temporary password expiry); 3_EXEC_PROMPT.md starts with the sync to #87's merge
- WORKER_B · HARDEN · done · #86 (merged 2026-10-17) · S1 MASAHA_WORKER_B, S2 B_HARDEN
- WORKER_B · DELETED · done · #67 · S1 MASAHA_WORKER_B
- WORKER_B · DIRECTORY · done · #73 · S1 MASAHA_WORKER_B
- WORKER_B · MANAGE · done · #83 (its folder also holds REVIEW82-83, which covers #82 too) · S1 MASAHA_WORKER_B, S2 B_MANAGE
- WORKER_B · OWNERS · done · #60 · S1 MASAHA_WORKER_B
- WORKER_B · OWNERSREAD · done · #82 · S1 MASAHA_WORKER_B, S2 B_OWNERSREAD
- WORKER_B · SESSIONS · done · #78 · S1 MASAHA_WORKER_B
- WORKER_B · USERS · done · #62 · S1 MASAHA_WORKER_B

## DESIGN

- DESIGN · ROUND2 · active · none yet · prompts and scripts point at this workspace since adoption; 25 of 40 reports (9 with a browser pass), 16 to run, then the summaries · S1 MASAHA_DESIGN\ROUND2, S1 ROUND2_GENERATOR_PROMPT, S5 r2-shots
- DESIGN · FIX_SHARED · done · #59 (`design/shared`) · S1 MASAHA_DESIGN, includes FIX_SHARED_REVIEW_LINKS and the SHOTS59 prompt, S5 pr59-shots
- DESIGN · FIX_ADMIN_EDITOR · done · #61 (`design/admin-editor`, matched by branch only) · S1 MASAHA_DESIGN
- DESIGN · FIX_ADMIN_REST · done · #66 (`design/admin-rest`, matched by branch only) · S1 MASAHA_DESIGN
- DESIGN · REVIEW_ADMIN · done · none · it is the review behind FIX_ADMIN_EDITOR and FIX_ADMIN_REST · S1 MASAHA_DESIGN
- DESIGN · FIX_PUBLIC · done · #65 (`design/public`) · S1 MASAHA_DESIGN
- DESIGN · FIX_ACCOUNT · done · #75 (`design/account`) · S1 MASAHA_DESIGN
- DESIGN · FIX_OWNER · done · #76 (`design/owner`) · S1 MASAHA_DESIGN
- DESIGN · FIX_DESK · done · #80 (`design/desk`) · S1 MASAHA_DESIGN, includes desk-scratch-reference.diff, S5 review-desk-shots
- DESIGN · DECISIONS · reference, not a task · S1 MASAHA_DESIGN

## TASKS (one-off)

- TASKS · AMENITIES · done · #64 · S1 MASAHA_AMENITIES, S5 amenities-shots
- TASKS · MEDIA · done · #77 · S1 MASAHA_MEDIA, S5 media-shots

## Not tasks

- 14 older shots folders (ds1, f10, f5b2, f5b3a, f5b3b, f5b3c2, f6b, f6c2, s2a2, s2a3, wi-f5b3c1, wi7, wi8, wi9): `_SHARED\ARCHIVE_2026-10-08\shots\`
