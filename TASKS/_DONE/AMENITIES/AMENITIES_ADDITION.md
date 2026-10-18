# AMENITIES — the independent review, and one more commit

**The review** (OpenCode, on `b7397dc`, `REPORT\REVIEW64_OPENCODE_REPORT.md`) found **no problem**:
the migrations match the schema, the save path holds under the lock, the flag is gone everywhere,
the documents state the code. Nothing to fix.

**One addition, the owner's decision (2026-10-12), in a fourth commit of its own:** no free price.
Every price of a space is **above zero**; a free event belongs in the space's announcements. It is
yours because the rule lives in `packages/shared/src/spaces/requests.ts`, which this PR already edits
(no other open item may touch it).

- **The rule:** `amountAgorot` an integer from **1** to `PRICE_MAX_AGOROT` (today `min(0)`, line 196);
  0 is refused on its field (`too_small`, the shared vocabulary).
- **The tests:** the shared unit test (0 refused at `prices.<i>.amountAgorot`, 1 accepted) and the API
  prices test (a body with a price of 0 → 422 on that field, nothing written), each seen failing
  first. Check the seed and every test fixture for a price of 0 (`grep`), and fix any.
- **The documents:** the contract's prices body line ("an integer from 1 to 10,000,000"); `spaces.md`
  › *API decisions*, one line: "every price is above zero; a free event goes in the announcements",
  dated 2026-10-12, the owner's decision; the API history line for #64 if it needs a word.
- **Commit:** `feat(spaces): refuse a price of zero` (≤ 50), alone, after the three; mention it in the
  PR description as the owner's addition.
- **Checks:** rebuild the shared `dist`; `test:unit`, `test:api`, `lint`, `typecheck`,
  `format:check`, `check:links`, once each on the new head (no web code changes: say why the component
  lane and the build are not rerun; CI runs them). Push (a new commit: a plain push, no force), wait
  for CI green and `CLEAN`, add a section to `REPORT\AMENITIES_REPORT.md`, `git merge-tree` against
  every open PR. The analyst reviews this commit. Don't merge. Stop every background shell you start;
  `jq` is not installed — use `gh … --jq`.
