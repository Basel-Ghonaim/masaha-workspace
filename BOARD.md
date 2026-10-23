# BOARD

`group · task · active|done · PR(s) · where it came from`

PRs come from the reports and from `gh pr list --state merged` (branch match). "open" = not merged yet. A blank PR means no evidence.

## WORKER_A

- WORKER_A · USERS · done · #93 (merged 2026-10-20 at 7d48c9c3) · one PR, eight commits after its fix round · _DONE
- WORKER_A · OWNER_SETUP · done · #96, #98, #99 (merged 2026-10-21; #99 at 2c4d78f9 after its fix round) · plan approved 2026-10-20 (three PRs: profile, packages, staff & settings); PR 1 = #96 merged 2026-10-20 at c91f5b42 (finding 99; small fixes in 0_CARRIED_FROM_96.md); PR 2 = #98 merged 2026-10-20 at cf3190a4 (small fixes in 0_CARRIED_FROM_98.md); PR 3 next: 3_EXEC_PROMPT_PR3.md
- WORKER_A · PUBLIC · executing (PR 3b next: commits 5-6, its prompt opens with 0_CARRIED_FROM_107.md; then PR 4; the owner reviews the whole public site after PR 4) · #101 (befd96f9), #103 (c3391d0e), #105 (a3828e09), #107 (merged 2026-10-22 at 5e8379af; 100 files accepted by the owner; review: no blocker, all carried) · step 3 web; plan approved 2026-10-21; PR 3 split by the owner into 3a and 3b
- WORKER_A · OWNERS · done · #88, #89, #91 (merged 2026-10-19) · one plan, three PRs
- WORKER_A · GALLERY · done · #85 (merged 2026-10-17; synced at adoption: REVIEW85, the report's fixes section, 5_FIXES_PROMPT) · S1 MASAHA_WORKER_A, S2 A_GALLERY, S5 gallery-shots
- WORKER_A · ADMINLIST · done · #84 · S1 MASAHA_WORKER_A, S2 A_ADMINLIST, S5 adminlist-shots
- WORKER_A · S2B3A · done · #50 · S1 MASAHA_WORKER_A, S5 s2b3a-shots
- WORKER_A · S2B3B · done · #57 · S1 MASAHA_WORKER_A, S5 s2b3b-shots
- WORKER_A · S2B4A · done · #74 · S1 MASAHA_WORKER_A, S5 s2b4a-shots
- WORKER_A · S2B4B · done · #79 · S1 MASAHA_WORKER_A, S5 s2b4b-shots
- WORKER_A · WEBBASE · done · #68 · S1 MASAHA_WORKER_A, S5 webbase-shots

## WORKER_B

- WORKER_B · DESK · done · #94, #95, #97, #100 (merged 2026-10-20/21) · step 7 API, four PRs; folder stays while active prompts cite its 3_EXEC_PROMPT_PR3.md
- WORKER_B · DEMO_SEED · done · #104 (merged 2026-10-21 at 5a0cda1a; no separate review: dev-only, 6 files) · the directory demo set (24 spaces); masaha_dev seeded by the supervisor from app-b's code, its 30 photo files copied into app's .storage; FULL and closed-today hold on 2026-10-21 only
- WORKER_B · SUBSCRIPTIONS · executing (PR 3 next, the check-ins: its prompt opens with 0_CARRIED_FROM_106.md) · #102 (43b34cd3), #106 (merged 2026-10-22 at ab0dadbd; built by Claude Code, phase 2 by OpenCode; review: no blocker, all carried, findings 124-125 to record) · step 8 API, three PRs; plan approved 2026-10-20
- WORKER_B · ANNOUNCEMENTS · planned (2_PLAN.md, approved 2026-10-21, note at its top: Q1–Q10) · — · step 10 API, four PRs (announcements; data reports; favourites; closure extension); owner's decisions 2026-10-21; findings 150+; executes after SUBSCRIPTIONS PR 3 and DEMO_SEED
- WORKER_B · SETTINGS · done · #92 (merged 2026-10-19; migration reception_typed_prices; findings 96–97) · _DONE
- WORKER_B · STAFF · done · #90 (merged 2026-10-18; migration temporary_password_expiry; findings 90–93) · _DONE
- WORKER_B · PACKAGES · done · #87 (merged 2026-10-18) · _DONE
- WORKER_B · HARDEN · done · #86 (merged 2026-10-17) · S1 MASAHA_WORKER_B, S2 B_HARDEN
- WORKER_B · DELETED · done · #67 · S1 MASAHA_WORKER_B
- WORKER_B · DIRECTORY · done · #73 · S1 MASAHA_WORKER_B
- WORKER_B · MANAGE · done · #83 (its folder also holds REVIEW82-83, which covers #82 too) · S1 MASAHA_WORKER_B, S2 B_MANAGE
- WORKER_B · OWNERS · done · #60 · S1 MASAHA_WORKER_B
- WORKER_B · OWNERSREAD · done · #82 · S1 MASAHA_WORKER_B, S2 B_OWNERSREAD
- WORKER_B · SESSIONS · done · #78 · S1 MASAHA_WORKER_B
- WORKER_B · USERS · done · #62 · S1 MASAHA_WORKER_B

## DESIGN

- DESIGN · ROUND2 · active · supervisor: «مشرف مراجعة التصميم #81» (HANDOFF_DESIGN_81.md) · 30 of 40 reviews (2026-10-20); PU-DF in 10 slices with the owner
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

- TASKS · CONFLICT_GUARD_BASEL · ready (2026-10-22; the owner runs and reviews it; worktree app-design, first) · — · check:conflicts in CI, the INDEX.md stray marker, issue #71; plan then build; 0_OWNER_CHECKLIST.md
- TASKS · DEMO_DAILY_BASEL · ready (2026-10-22; after CONFLICT_GUARD's PR is open; worktree app-design, DBs masaha_design_dev/_test, API port 3323) · — · the demo set renews FULL and closed-today on every seed run; plan then build; 0_OWNER_CHECKLIST.md

- TASKS · MIGRATION_DEV · done · — · TASKS\_DONE\MIGRATION_DEV (4_REPORT.md); Masaha now under C:\dev\masaha (2026-10-18)
- TASKS · AMENITIES · done · #64 · S1 MASAHA_AMENITIES, S5 amenities-shots
- TASKS · MEDIA · done · #77 · S1 MASAHA_MEDIA, S5 media-shots

## Not tasks

- 14 older shots folders (ds1, f10, f5b2, f5b3a, f5b3b, f5b3c2, f6b, f6c2, s2a2, s2a3, wi-f5b3c1, wi7, wi8, wi9): `_SHARED\ARCHIVE_2026-10-08\shots\`
