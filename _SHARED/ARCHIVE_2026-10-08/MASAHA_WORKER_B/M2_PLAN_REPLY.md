# M2 — reply to your plan

The plan is approved, with the answers below. **First, save it** (as amended here) to
`C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\M2_PLAN.md` — `PLAN\` holds only `M1_PLAN.md` so far.
Then wait: **PR #50 has not merged yet**; the owner will tell you when to cut the branch.

## Stronger decisions
1. **Proof 1 compares links by their resolved target:** approved, as a stated departure from D7.1's
   wording.
2. **The D3/D4 rule as one sentence in documentation §5:** approved (the headings' names; a decision
   on both layers or on `packages/shared` goes to the API part; a PR on both layers in both
   histories).
3. **The wider checker** (the root README, every `docs/` path cited in code): approved.
4. **The index check in proof 2** (each file listed once, under its status's group): approved.
5. **Links into `#decisions` left as they are:** approved.
6. **Finding 38's PR number — changed.** Don't predict it: issues and PRs share one counter, and
   another worker may open a PR first (worker C may open one for the README today). Instead:
   push, `gh pr create`, then fold the real number into commit 1 (`**Resolution (<date>, #N):**`)
   and push again with `--force-with-lease` **before** you wait for CI. One extra CI run on a docs
   PR is the price of certainty.

## The owner's decisions (§12)
1. **The doubtful placements and the three history additions:** approved as you listed them.
2. (Above.)
3. (Above, changed.)
4. **`space-links`' missing #48:** add it, in the **API history**: "#48 — the missing fact groups on
   the admin list's rows." A history that omits a PR states less than is true; list the line among
   proof 3's additions.
5. **The branch:** cut only when the owner says #50 has merged; then `git fetch`, check `HEAD` at the
   new `origin/main`, and re-read #50's final documents (its review fixes change `space-links.md`,
   `lookups.md` and finding 45's wording), so the appendix's allocation and proof 1 run against
   what merged, not against `cfd1a5a`.

Everything else as planned: the three commits, the checker before each commit, the three proofs as
commands with their output, `format:check` + lint + typecheck once, the `git grep` for `findings.md`,
the early conflict check, the report in `REPORT\M2_REPORT.md`.
