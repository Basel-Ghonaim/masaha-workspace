# MAPPING — Phase 1 plan

Total files: **2148**, bytes: **137,673,126**.

## Per source key

| key | files | bytes |
|---|---|---|
| S1 | 309 | 4,427,520 |
| S2 | 33 | 100,710 |
| S3 | 3 | 42,733 |
| S4 | 124 | 1,662,113 |
| S5 | 1679 | 131,440,050 |

## Per target folder

| folder | files |
|---|---|
| `DESIGN\DECISIONS` | 7 |
| `DESIGN\ROUND2` | 690 |
| `DESIGN\_DONE\FIX_ACCOUNT` | 8 |
| `DESIGN\_DONE\FIX_ADMIN_EDITOR` | 6 |
| `DESIGN\_DONE\FIX_ADMIN_REST` | 5 |
| `DESIGN\_DONE\FIX_DESK` | 30 |
| `DESIGN\_DONE\FIX_OWNER` | 9 |
| `DESIGN\_DONE\FIX_PUBLIC` | 7 |
| `DESIGN\_DONE\FIX_SHARED` | 115 |
| `DESIGN\_DONE\REVIEW_ADMIN` | 2 |
| `HANDOFF.md` | 1 |
| `TASKS\_DONE\AMENITIES` | 18 |
| `TASKS\_DONE\MEDIA` | 14 |
| `WORKER_A\GALLERY` | 18 |
| `WORKER_A\_DONE\ADMINLIST` | 36 |
| `WORKER_A\_DONE\S2B3A` | 40 |
| `WORKER_A\_DONE\S2B3B` | 43 |
| `WORKER_A\_DONE\S2B4A` | 41 |
| `WORKER_A\_DONE\S2B4B` | 34 |
| `WORKER_A\_DONE\WEBBASE` | 13 |
| `WORKER_B\HARDEN` | 6 |
| `WORKER_B\_DONE\DELETED` | 6 |
| `WORKER_B\_DONE\DIRECTORY` | 7 |
| `WORKER_B\_DONE\MANAGE` | 13 |
| `WORKER_B\_DONE\OWNERS` | 7 |
| `WORKER_B\_DONE\OWNERSREAD` | 11 |
| `WORKER_B\_DONE\SESSIONS` | 7 |
| `WORKER_B\_DONE\USERS` | 8 |
| `_SHARED` | 1 |
| `_SHARED\ARCHIVE_2026-10-08` | 941 |
| `_SHARED\HANDOFFS` | 3 |
| `_SHARED\MIGRATION` | 1 |

## Task list

| group | task | state | PR(s) | files |
|---|---|---|---|---|
| DESIGN | FIX_ACCOUNT | done | #75 | 8 |
| DESIGN | FIX_ADMIN_EDITOR | done | #61 | 6 |
| DESIGN | FIX_ADMIN_REST | done | #66 | 5 |
| DESIGN | FIX_DESK | done | #80 | 30 |
| DESIGN | FIX_OWNER | done | #76 | 9 |
| DESIGN | FIX_PUBLIC | done | #65 | 7 |
| DESIGN | FIX_SHARED | done | #59 | 115 |
| DESIGN | REVIEW_ADMIN | done | unknown | 2 |
| DESIGN | ROUND2 | active | unknown | 690 |
| TASKS | AMENITIES | done | #64 | 18 |
| TASKS | MEDIA | done | #77 | 14 |
| WORKER_A | ADMINLIST | done | #84 | 36 |
| WORKER_A | GALLERY | active | unknown | 18 |
| WORKER_A | S2B3A | done | #50 | 40 |
| WORKER_A | S2B3B | done | #57 | 43 |
| WORKER_A | S2B4A | done | #74 | 41 |
| WORKER_A | S2B4B | done | #79 | 34 |
| WORKER_A | WEBBASE | done | #68 | 13 |
| WORKER_B | DELETED | done | #67 | 6 |
| WORKER_B | DIRECTORY | done | #73 | 7 |
| WORKER_B | HARDEN | active | #86 | 6 |
| WORKER_B | MANAGE | done | #83 | 13 |
| WORKER_B | OWNERS | done | #60 | 7 |
| WORKER_B | OWNERSREAD | done | #82 | 11 |
| WORKER_B | SESSIONS | done | #78 | 7 |
| WORKER_B | USERS | done | #62 | 8 |

PRs for AMENITIES (#64) and MEDIA (#77) come from their folders' REVIEW64/REVIEW77 files and reports. HARDEN's #86 (`fix/space-api-hardening`, still open) is named by REVIEW86_OPENCODE_REPORT.md and confirmed with `gh pr view 86`. GALLERY and ROUND2 have no merged PR yet.


## UNSORTED — 0 files


S1/S2 files in UNSORTED, and why:


## R4 decisions (evidence)

- `REVIEW75_PROMPT.md` -> `DESIGN\_DONE\FIX_ACCOUNT\REVIEW75_PROMPT.md` — PR #75 -> FIX_ACCOUNT; MASAHA_DESIGN\REPORT\FIX_ACCOUNT_REPORT.md: - PR **#75** — `design: the account and signing in`: https://github.com/Basel-Ghonaim/masaha/pull/75
- `REVIEW76_PROMPT.md` -> `DESIGN\_DONE\FIX_OWNER\REVIEW76_PROMPT.md` — PR #76 -> FIX_OWNER; MASAHA_DESIGN\REPORT\FIX_OWNER_REPORT.md: - **PR:** #76 — https://github.com/Basel-Ghonaim/masaha/pull/76
- `REVIEW_ACCOUNT_PROMPT.md` -> `DESIGN\_DONE\FIX_ACCOUNT\REVIEW_ACCOUNT_PROMPT.md` — MASAHA_DESIGN\PROMPT\FIX_ACCOUNT_PROMPT.md: 3. **The review behind them:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_ACCOUNT_REPORT.md`.
- `REVIEW_DESK_BUILD_PROMPT.md` -> `DESIGN\_DONE\FIX_DESK\REVIEW_DESK_BUILD_PROMPT.md` — MASAHA_DESIGN\PROMPT\FIX_DESK_PROMPT.md: 4. **The review behind them:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_DESK_REPORT.md`.
- `REVIEW_DESK_PROMPT.md` -> `DESIGN\_DONE\FIX_DESK\REVIEW_DESK_PROMPT.md` — MASAHA_DESIGN\PROMPT\FIX_DESK_PROMPT.md: 4. **The review behind them:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_DESK_REPORT.md`.
- `REVIEW_OWNER_PROMPT.md` -> `DESIGN\_DONE\FIX_OWNER\REVIEW_OWNER_PROMPT.md` — MASAHA_DESIGN\PROMPT\FIX_OWNER_PROMPT.md: 3. **The review behind them:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_OWNER_REPORT.md`.
- `REVIEW_PUBLIC_PROMPT.md` -> `DESIGN\_DONE\FIX_PUBLIC\REVIEW_PUBLIC_PROMPT.md` — MASAHA_DESIGN\PROMPT\FIX_PUBLIC_PROMPT.md: 3. **The review behind them:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_PUBLIC_REPORT.md`
- `REVIEW_SHARED_PROMPT.md` -> `DESIGN\_DONE\FIX_SHARED\REVIEW_SHARED_PROMPT.md` — MASAHA_DESIGN\PROMPT\FIX_SHARED_PROMPT.md: 2. **The review behind them:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_SHARED_REPORT.md`
- `REVIEW75_OPENCODE_REPORT.md` -> `DESIGN\_DONE\FIX_ACCOUNT\REVIEW75_OPENCODE_REPORT.md` — PR #75 -> FIX_ACCOUNT; MASAHA_DESIGN\REPORT\FIX_ACCOUNT_REPORT.md: - PR **#75** — `design: the account and signing in`: https://github.com/Basel-Ghonaim/masaha/pull/75
- `REVIEW76_OPENCODE_REPORT.md` -> `DESIGN\_DONE\FIX_OWNER\REVIEW76_OPENCODE_REPORT.md` — PR #76 -> FIX_OWNER; MASAHA_DESIGN\REPORT\FIX_OWNER_REPORT.md: - **PR:** #76 — https://github.com/Basel-Ghonaim/masaha/pull/76
- `REVIEW_ACCOUNT_REPORT.md` -> `DESIGN\_DONE\FIX_ACCOUNT\REVIEW_ACCOUNT_REPORT.md` — MASAHA_DESIGN\PROMPT\FIX_ACCOUNT_PROMPT.md: 3. **The review behind them:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_ACCOUNT_REPORT.md`.
- `REVIEW_DESK_OPENCODE_REPORT.md` -> `DESIGN\_DONE\FIX_DESK\REVIEW_DESK_OPENCODE_REPORT.md` — MASAHA_DESIGN\PROMPT\FIX_DESK_PROMPT.md: 4. **The review behind them:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_DESK_REPORT.md`.
- `REVIEW_DESK_REPORT.md` -> `DESIGN\_DONE\FIX_DESK\REVIEW_DESK_REPORT.md` — MASAHA_DESIGN\PROMPT\FIX_DESK_PROMPT.md: 4. **The review behind them:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_DESK_REPORT.md`.
- `REVIEW_OWNER_REPORT.md` -> `DESIGN\_DONE\FIX_OWNER\REVIEW_OWNER_REPORT.md` — MASAHA_DESIGN\PROMPT\FIX_OWNER_PROMPT.md: 3. **The review behind them:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_OWNER_REPORT.md`.
- `REVIEW_PUBLIC_REPORT.md` -> `DESIGN\_DONE\FIX_PUBLIC\REVIEW_PUBLIC_REPORT.md` — MASAHA_DESIGN\PROMPT\FIX_PUBLIC_PROMPT.md: 3. **The review behind them:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_PUBLIC_REPORT.md`
- `REVIEW_SHARED_REPORT.md` -> `DESIGN\_DONE\FIX_SHARED\REVIEW_SHARED_REPORT.md` — MASAHA_DESIGN\PROMPT\FIX_SHARED_PROMPT.md: 2. **The review behind them:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_SHARED_REPORT.md`
- `REVIEW50_PROMPT.md` -> `WORKER_A\_DONE\S2B3A\REVIEW50_PROMPT.md` — PR #50 -> S2B3A; MASAHA_WORKER_A\REPORT\S2B3A_FIXES_REPORT.md: # S2b-3a — review fixes report (PR #50)
- `REVIEW57_PROMPT.md` -> `WORKER_A\_DONE\S2B3B\REVIEW57_PROMPT.md` — PR #57 -> S2B3B; MASAHA_WORKER_A\REPORT\S2B3B_REPORT.md: - **PR #57:** https://github.com/Basel-Ghonaim/masaha/pull/57, `feat(spaces): add a space with its map pin`.
- `REVIEW68_PROMPT.md` -> `WORKER_A\_DONE\WEBBASE\REVIEW68_PROMPT.md` — PR #68 -> WEBBASE; MASAHA_WORKER_A\REPORT\WEBBASE_REPORT.md: [#68 `refactor(web): storage layer and page titles`](https://github.com/Basel-Ghonaim/masaha/pull/68):
- `REVIEW74_FIXES.md` -> `WORKER_A\_DONE\S2B4A\REVIEW74_FIXES.md` — PR #74 -> S2B4A; MASAHA_WORKER_A\REPORT\S2B4A_REPORT.md: **#74** `feat(spaces): the admin's space editor` — https://github.com/Basel-Ghonaim/masaha/pull/74
- `REVIEW74_PROMPT.md` -> `WORKER_A\_DONE\S2B4A\REVIEW74_PROMPT.md` — PR #74 -> S2B4A; MASAHA_WORKER_A\REPORT\S2B4A_REPORT.md: **#74** `feat(spaces): the admin's space editor` — https://github.com/Basel-Ghonaim/masaha/pull/74
- `REVIEW79_FIXES.md` -> `WORKER_A\_DONE\S2B4B\REVIEW79_FIXES.md` — PR #79 -> S2B4B; MASAHA_WORKER_A\REPORT\S2B4B_REPORT.md: - **#79** — `feat(spaces): the editor's hours and prices` — https://github.com/Basel-Ghonaim/masaha/pull/79
- `REVIEW79_PROMPT.md` -> `WORKER_A\_DONE\S2B4B\REVIEW79_PROMPT.md` — PR #79 -> S2B4B; MASAHA_WORKER_A\REPORT\S2B4B_REPORT.md: - **#79** — `feat(spaces): the editor's hours and prices` — https://github.com/Basel-Ghonaim/masaha/pull/79
- `REVIEW50_REPORT.md` -> `WORKER_A\_DONE\S2B3A\REVIEW50_REPORT.md` — PR #50 -> S2B3A; MASAHA_WORKER_A\REPORT\S2B3A_FIXES_REPORT.md: # S2b-3a — review fixes report (PR #50)
- `REVIEW57_CODEX_REPORT.md` -> `WORKER_A\_DONE\S2B3B\REVIEW57_CODEX_REPORT.md` — PR #57 -> S2B3B; MASAHA_WORKER_A\REPORT\S2B3B_REPORT.md: - **PR #57:** https://github.com/Basel-Ghonaim/masaha/pull/57, `feat(spaces): add a space with its map pin`.
- `REVIEW57_COPILOT_REPORT.md` -> `WORKER_A\_DONE\S2B3B\REVIEW57_COPILOT_REPORT.md` — PR #57 -> S2B3B; MASAHA_WORKER_A\REPORT\S2B3B_REPORT.md: - **PR #57:** https://github.com/Basel-Ghonaim/masaha/pull/57, `feat(spaces): add a space with its map pin`.
- `REVIEW57_MERGED_REPORT.md` -> `WORKER_A\_DONE\S2B3B\REVIEW57_MERGED_REPORT.md` — PR #57 -> S2B3B; MASAHA_WORKER_A\REPORT\S2B3B_REPORT.md: - **PR #57:** https://github.com/Basel-Ghonaim/masaha/pull/57, `feat(spaces): add a space with its map pin`.
- `REVIEW57_OPENCODE_REPORT.md` -> `WORKER_A\_DONE\S2B3B\REVIEW57_OPENCODE_REPORT.md` — PR #57 -> S2B3B; MASAHA_WORKER_A\REPORT\S2B3B_REPORT.md: - **PR #57:** https://github.com/Basel-Ghonaim/masaha/pull/57, `feat(spaces): add a space with its map pin`.
- `REVIEW68_OPENCODE_REPORT.md` -> `WORKER_A\_DONE\WEBBASE\REVIEW68_OPENCODE_REPORT.md` — PR #68 -> WEBBASE; MASAHA_WORKER_A\REPORT\WEBBASE_REPORT.md: [#68 `refactor(web): storage layer and page titles`](https://github.com/Basel-Ghonaim/masaha/pull/68):
- `REVIEW74_CLAUDE_REPORT.md` -> `WORKER_A\_DONE\S2B4A\REVIEW74_CLAUDE_REPORT.md` — PR #74 -> S2B4A; MASAHA_WORKER_A\REPORT\S2B4A_REPORT.md: **#74** `feat(spaces): the admin's space editor` — https://github.com/Basel-Ghonaim/masaha/pull/74
- `REVIEW79_OPENCODE_REPORT.md` -> `WORKER_A\_DONE\S2B4B\REVIEW79_OPENCODE_REPORT.md` — PR #79 -> S2B4B; MASAHA_WORKER_A\REPORT\S2B4B_REPORT.md: - **#79** — `feat(spaces): the editor's hours and prices` — https://github.com/Basel-Ghonaim/masaha/pull/79
- `REVIEW84_OPENCODE_REPORT.md` -> `WORKER_A\_DONE\ADMINLIST\REVIEW84_OPENCODE_REPORT.md` — PR #84 -> ADMINLIST; MASAHA_WORKER_A\REPORT\ADMINLIST_REPORT.md: **PR:** [#84](https://github.com/Basel-Ghonaim/masaha/pull/84) — `feat(space-links): show deleted space facts`.
- `REVIEW60_PROMPT.md` -> `WORKER_B\_DONE\OWNERS\REVIEW60_PROMPT.md` — PR #60 -> OWNERS; MASAHA_WORKER_B\REPORT\OWNERS_REPORT.md: - **PR:** [#60](https://github.com/Basel-Ghonaim/masaha/pull/60), `feat(space-links): add the admin's owners`.
- `REVIEW62_PROMPT.md` -> `WORKER_B\_DONE\USERS\REVIEW62_PROMPT.md` — PR #62 -> USERS; MASAHA_WORKER_B\REPORT\USERS_REPORT.md: - **#62** `feat(users): suspend, role and temporary password` — https://github.com/Basel-Ghonaim/masaha/pull/62
- `REVIEW67_PROMPT.md` -> `WORKER_B\_DONE\DELETED\REVIEW67_PROMPT.md` — PR #67 -> DELETED; MASAHA_WORKER_B\REPORT\DELETED_REPORT.md: **#67** — `feat(space-links): list the deleted spaces` — https://github.com/Basel-Ghonaim/masaha/pull/67
- `REVIEW73_PROMPT.md` -> `WORKER_B\_DONE\DIRECTORY\REVIEW73_PROMPT.md` — PR #73 -> DIRECTORY; MASAHA_WORKER_B\REPORT\DIRECTORY_REPORT.md: **PR:** [#73](https://github.com/Basel-Ghonaim/masaha/pull/73), `feat(directory): the public directory's API`.
- `REVIEW78_PROMPT.md` -> `WORKER_B\_DONE\SESSIONS\REVIEW78_PROMPT.md` — PR #78 -> SESSIONS; MASAHA_WORKER_B\REPORT\SESSIONS_REPORT.md: - **PR #78**, `feat(sessions): end a session when it should`: https://github.com/Basel-Ghonaim/masaha/pull/78
- `REVIEW60_CLAUDE_REPORT.md` -> `WORKER_B\_DONE\OWNERS\REVIEW60_CLAUDE_REPORT.md` — PR #60 -> OWNERS; MASAHA_WORKER_B\REPORT\OWNERS_REPORT.md: - **PR:** [#60](https://github.com/Basel-Ghonaim/masaha/pull/60), `feat(space-links): add the admin's owners`.
- `REVIEW62_CLAUDE_REPORT.md` -> `WORKER_B\_DONE\USERS\REVIEW62_CLAUDE_REPORT.md` — PR #62 -> USERS; MASAHA_WORKER_B\REPORT\USERS_REPORT.md: - **#62** `feat(users): suspend, role and temporary password` — https://github.com/Basel-Ghonaim/masaha/pull/62
- `REVIEW62_OPENCODE_REPORT.md` -> `WORKER_B\_DONE\USERS\REVIEW62_OPENCODE_REPORT.md` — PR #62 -> USERS; MASAHA_WORKER_B\REPORT\USERS_REPORT.md: - **#62** `feat(users): suspend, role and temporary password` — https://github.com/Basel-Ghonaim/masaha/pull/62
- `REVIEW67_OPENCODE_REPORT.md` -> `WORKER_B\_DONE\DELETED\REVIEW67_OPENCODE_REPORT.md` — PR #67 -> DELETED; MASAHA_WORKER_B\REPORT\DELETED_REPORT.md: **#67** — `feat(space-links): list the deleted spaces` — https://github.com/Basel-Ghonaim/masaha/pull/67
- `REVIEW73_COPILOT_REPORT.md` -> `WORKER_B\_DONE\DIRECTORY\REVIEW73_COPILOT_REPORT.md` — PR #73 -> DIRECTORY; MASAHA_WORKER_B\REPORT\DIRECTORY_REPORT.md: **PR:** [#73](https://github.com/Basel-Ghonaim/masaha/pull/73), `feat(directory): the public directory's API`.
- `REVIEW73_OPENCODE_REPORT.md` -> `WORKER_B\_DONE\DIRECTORY\REVIEW73_OPENCODE_REPORT.md` — PR #73 -> DIRECTORY; MASAHA_WORKER_B\REPORT\DIRECTORY_REPORT.md: **PR:** [#73](https://github.com/Basel-Ghonaim/masaha/pull/73), `feat(directory): the public directory's API`.
- `REVIEW78_OPENCODE_REPORT.md` -> `WORKER_B\_DONE\SESSIONS\REVIEW78_OPENCODE_REPORT.md` — PR #78 -> SESSIONS; MASAHA_WORKER_B\REPORT\SESSIONS_REPORT.md: - **PR #78**, `feat(sessions): end a session when it should`: https://github.com/Basel-Ghonaim/masaha/pull/78
- `REVIEW82-83_OPENCODE_REPORT.md` -> `WORKER_B\_DONE\MANAGE\REVIEW82-83_OPENCODE_REPORT.md` — covers #82 and #83; later of the two -> MANAGE; MASAHA_WORKER_B\REPORT\REVIEW_MANAGE_CODEX_REPORT.md: ﻿PR #83 — head `d5726ddfa3057e8c368dd58d995e82dde526dd59`
- `REVIEW86_OPENCODE_REPORT.md` -> `WORKER_B\HARDEN\REVIEW86_OPENCODE_REPORT.md` — PR #86 -> HARDEN; MASAHA_WORKER_B\REPORT\REVIEW86_OPENCODE_REPORT.md: # Review — PR #86, HARDEN (independent reviewer)
- `REVIEW_MANAGE_CODEX_REPORT.md` -> `WORKER_B\_DONE\MANAGE\REVIEW_MANAGE_CODEX_REPORT.md` — REVIEW_MANAGE_* -> MANAGE (PR #83): MASAHA_WORKER_B\REPORT\REVIEW_MANAGE_CODEX_REPORT.md: ﻿PR #83 — head `d5726ddfa3057e8c368dd58d995e82dde526dd59`
- `REVIEW_MANAGE_COPILOT_REPORT.md` -> `WORKER_B\_DONE\MANAGE\REVIEW_MANAGE_COPILOT_REPORT.md` — REVIEW_MANAGE_* -> MANAGE (PR #83): MASAHA_WORKER_B\REPORT\REVIEW_MANAGE_CODEX_REPORT.md: ﻿PR #83 — head `d5726ddfa3057e8c368dd58d995e82dde526dd59`

## R6 decisions

- `adminlist-shots` -> `WORKER_A\_DONE\ADMINLIST\shots\adminlist-shots` — ADMINLIST_PLAN/PROMPT/REPORT name it
- `amenities-shots` -> `TASKS\_DONE\AMENITIES\shots\amenities-shots` — AMENITIES_PLAN/PROMPT/REPORT name it
- `ds1-shots` -> `_SHARED\UNSORTED\S5\ds1-shots` — owner ruling 1: folder dated 2026-09-28..2026-10-07, before the 2026-10-08 archive
- `f10-shots` -> `_SHARED\UNSORTED\S5\f10-shots` — owner ruling 1: folder dated 2026-09-28..2026-10-07, before the 2026-10-08 archive
- `f5b2-shots` -> `_SHARED\UNSORTED\S5\f5b2-shots` — owner ruling 1: folder dated 2026-09-28..2026-10-07, before the 2026-10-08 archive
- `f5b3a-shots` -> `_SHARED\UNSORTED\S5\f5b3a-shots` — owner ruling 1: folder dated 2026-09-28..2026-10-07, before the 2026-10-08 archive
- `f5b3b-shots` -> `_SHARED\UNSORTED\S5\f5b3b-shots` — owner ruling 1: folder dated 2026-09-28..2026-10-07, before the 2026-10-08 archive
- `f5b3c2-shots` -> `_SHARED\UNSORTED\S5\f5b3c2-shots` — owner ruling 1: folder dated 2026-09-28..2026-10-07, before the 2026-10-08 archive
- `f6b-shots` -> `_SHARED\UNSORTED\S5\f6b-shots` — owner ruling 1: folder dated 2026-09-28..2026-10-07, before the 2026-10-08 archive
- `f6c2-shots` -> `_SHARED\UNSORTED\S5\f6c2-shots` — owner ruling 1: folder dated 2026-09-28..2026-10-07, before the 2026-10-08 archive
- `gallery-shots` -> `WORKER_A\GALLERY\shots\gallery-shots` — GALLERY_PLAN/REPORT name it
- `media-shots` -> `TASKS\_DONE\MEDIA\shots\media-shots` — MEDIA_REPORT names it
- `pr59-shots` -> `DESIGN\_DONE\FIX_SHARED\shots\pr59-shots` — SHOTS59_PROMPT names it; FIX_SHARED_REPORT names design/shared and #59 (owner ruling 5)
- `r2-shots` -> `DESIGN\ROUND2\shots\r2-shots` — ROUND2 prompts/reports and ROUND2_GENERATOR_PROMPT name it
- `review-desk-shots` -> `DESIGN\_DONE\FIX_DESK\shots\review-desk-shots` — REVIEW_DESK_BUILD_PROMPT / REVIEW_DESK_OPENCODE_REPORT name it; REVIEW_DESK -> FIX_DESK
- `s2a2-shots` -> `_SHARED\UNSORTED\S5\s2a2-shots` — owner ruling 1: folder dated 2026-09-28..2026-10-07, before the 2026-10-08 archive
- `s2a3-shots` -> `_SHARED\UNSORTED\S5\s2a3-shots` — owner ruling 1: folder dated 2026-09-28..2026-10-07, before the 2026-10-08 archive
- `s2b3a-shots` -> `WORKER_A\_DONE\S2B3A\shots\s2b3a-shots` — S2B3A_PROMPT names it
- `s2b3b-shots` -> `WORKER_A\_DONE\S2B3B\shots\s2b3b-shots` — S2B3B_PLAN/PROMPT/REPORT name it
- `s2b4a-shots` -> `WORKER_A\_DONE\S2B4A\shots\s2b4a-shots` — S2B4A_PLAN/PROMPT/REPORT name it
- `s2b4b-shots` -> `WORKER_A\_DONE\S2B4B\shots\s2b4b-shots` — S2B4B_PLAN/PROMPT/REPORT name it
- `webbase-shots` -> `WORKER_A\_DONE\WEBBASE\shots\webbase-shots` — WEBBASE_PLAN/PROMPT/REPORT name it
- `wi-f5b3c1-shots` -> `_SHARED\UNSORTED\S5\wi-f5b3c1-shots` — owner ruling 1: folder dated 2026-09-28..2026-10-07, before the 2026-10-08 archive
- `wi7-shots` -> `_SHARED\UNSORTED\S5\wi7-shots` — owner ruling 1: folder dated 2026-09-28..2026-10-07, before the 2026-10-08 archive
- `wi8-shots` -> `_SHARED\UNSORTED\S5\wi8-shots` — owner ruling 1: folder dated 2026-09-28..2026-10-07, before the 2026-10-08 archive
- `wi9-shots` -> `_SHARED\UNSORTED\S5\wi9-shots` — owner ruling 1: folder dated 2026-09-28..2026-10-07, before the 2026-10-08 archive

## PR evidence for the FIX_* tasks (gh pr list --state merged --limit 100, branch design/<part>)

- FIX_SHARED: #59 `design/shared` "design: apply the shared layer's decisions"
- FIX_ADMIN_EDITOR: #61 `design/admin-editor` "design: the admin's space editor"
- FIX_ADMIN_REST: #66 `design/admin-rest` "design: the rest of the admin's dashboard"
- FIX_PUBLIC: #65 `design/public` "design: the public site"
- FIX_ACCOUNT: #75 `design/account` "design: the account and signing in"
- FIX_OWNER: #76 `design/owner` "design: the owner's management"
- FIX_DESK: #80 `design/desk` "design: the front desk"
- GALLERY (feat/space-gallery) and ROUND2: no merged PR matches; PR left blank. HARDEN: #86 is open, not merged. REVIEW_ADMIN has no PR of its own (the review behind FIX_ADMIN_EDITOR #61 and FIX_ADMIN_REST #66).
- `pr59-shots` and `SHOTS59_PROMPT.md` joined FIX_SHARED: FIX_SHARED_PLAN/REPORT name `design/shared`; the report names PR #59.
- The 14 shots folders no report names (ds1, f10, f5b2, f5b3a, f5b3b, f5b3c2, f6b, f6c2, s2a2, s2a3, wi-f5b3c1, wi7, wi8, wi9) go whole to `_SHARED\ARCHIVE_2026-10-08\shots\<folder>\`: owner ruling, they are dated 2026-09-28 to 2026-10-07, before the archive. README.md will say so.

## Unsure

- FIX_ADMIN_EDITOR (#61) and FIX_ADMIN_REST (#66) are matched by branch name only; their reports were not checked for the PR.
- AMENITIES (#64) and MEDIA (#77): numbers come from the REVIEW64/REVIEW77 file names; the gh list agrees (feat/space-own-amenities, feat/space-photos).

## Check results

- every source file has exactly one row; no shared targets; no target outside `D:\masahaWorkspace`; all target paths < 240 chars
- longest target path: 152 chars
