# SETTINGS (#92) — fix round 1 (documents and one commit message)

To the executor of PR #92 (`feat/space-settings`, head `af5a05a6`, `C:\dev\masaha\app-b`). The review is
`C:\dev\masaha\workspace\WORKER_B\SETTINGS\6_REVIEW_CLAUDE_CODE.md` — read it. No code changes. Everything
in `3_EXEC_PROMPT.md` still binds (the report as you go, the final-reply template).

Already done by the supervisor: `_SHARED\OPEN_DECISIONS.md` point 1 (review finding 1) — your report's text.

## Fix
1. **ADR 0009 (finding 2, verified):** the row «New customer; subscription from a package or custom» gives
   reception a custom subscription without the condition the next row sets on its hand-typed price. Make the
   two rows agree (e.g. the custom subscription's price typed by hand → the row below), in the commit that
   revised the ADR.
2. **`security.md`'s *Built* summary (finding 3):** list the settings and capacity routes, as its body does.
3. **The last commit's message (finding 4):** "finding 94" → "finding 96" (`git commit --fixup=reword:<sha>`
   or the `amend!` form you used before; subject unchanged).
4. **Finding to record (finding 5):** the visit-rounding rule in two places (the platform's new-space
   defaults and the new settings schema) — the next free number on the latest `origin/main`'s index, for
   step 11.
5. **The four small wording nits** the review lists (DI-41 with no definition in the repository — a short
   in-place gloss; step 5 of the build map still naming capacity; the conventions header and the new
   feature documents overlapping — keep one home; the data-model sentence grouping capacity with the stay
   limit).

## How
Fold each into its commit (`--fixup` + `GIT_SEQUENCE_EDITOR=:` autosquash), bodies kept. Run what the change
touches only: `check:links`, `format:check`. Push with lease; CI green; `CLEAN`; append *Fix round 1* to
`4_REPORT_PR1.md`; final reply in the template.
