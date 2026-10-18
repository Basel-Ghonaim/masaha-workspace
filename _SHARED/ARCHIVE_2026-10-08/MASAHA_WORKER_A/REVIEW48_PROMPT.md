# Review — PR #48 (S2b-2: the spaces' facts API)

You are the **independent reviewer** of PR #48. Run from `C:\Users\basel\masaha` (the main folder).
You don't build, fix or merge.

## Budget (hard limits — the owner's)

- **At most 2 subagents. Never a third.** No workflows. Use no plugin skill (workflow §10: review
  sessions use none); you may apply testing.md §3's *name the break* and *make the break* as a lens.
- **The whole review stays under 600,000 tokens**, this conversation and both subagents together.
- **Reports:** at most 700 words per subagent, and at most 900 for yours.

## Rules

- **Read-only.** No edits, commits, checkouts, switches, installs, npm or test runs, database or
  migration commands, or GitHub comments. Another worker may be using the main folder's working tree:
  read only from commit objects. `git fetch origin`, then pin to the PR's head:
  `gh pr view 48 --json headRefOid` (it was `c4e993d`); base `a1f5aba`. Use
  `git diff a1f5aba...<head> -- <paths>` and `git show <head>:<file>`. State the head in your report.
- **Read in the order workflow §2 gives:** `docs/features/spaces.md` first (at `<head>`: its decisions
  F1–F7, A1, D1–D9 and their reasons), then only what it links and what your area needs.
- **Report concrete problems only:** file and line, the failing scenario, the severity
  (blocker / should-fix / nit) and the fix. **Verify each in the code before reporting it.**

## What the PR must be (the owner's decisions)

API, `packages/shared` and documents only. The admin edits an **unverified** space's facts one group
at a time — `PUT …/hours` (with the shifts), `…/prices`, `…/amenities`, `…/contacts` — and confirms a
group unchanged (`POST …/<group>/confirm`, profile included). Each save is one transaction: the
thresholds read before it; lock the space, 404 if deleted, `can()` (403 if verified), change, date the
group, audit, all in the same transaction. Decisions:
- **F1** one `PUT` per group replacing it whole, plus confirm; **F2** a never-saved group is *missing*
  (null date; a migration made four dates nullable and cleared them where a space has no rows);
  **F3** shifts saved with the hours, their freshness the hours'; **F4** a day is closed or one range
  in 0–1,440 minutes, no range past midnight; **F5** shift ids kept, a shift in use refused (409, by
  the database's own keys); **F6** contacts validated and normalised per type; **F7** only an active
  amenity can be added, a retired one already linked is kept.
- **A1** duplicates inside a group are 422 `not_unique` on the right row field (the database keys
  stay as a guard); **D1–D9** as `spaces.md` states them (confirm a missing group → 409; a no-op save
  writes nothing except the first save of a missing group; a shift must fit one open day; audit
  payloads hold the whole group; `phoneSchema` in `core` with separators stripped; networks stored as
  `https://` URLs on their own host, a Facebook `profile.php?id=` keeping its id; size caps; no hours
  for a new space).
- **Folded findings:** 31 (the older spaces service no longer takes a repository), 41 (the request
  log names the space), 36 (missing groups). **Finding 42** records a component test that failed once.
- **Project rules:** levels R1–R8; no parameter only tests pass; one statement at a time in a
  transaction (conventions §8, finding 11's guard); every protected endpoint tested as a guest, a
  USER, an OWNER of another space, the OWNER of this space, the ADMIN and an admin with a pending
  change; `docs/features/spaces.md` updated in this PR, one home per fact.

## The split

### Subagent 1 — security, data integrity and correctness (`apps/api`, `packages/shared`, the migration)

**It checks:**
- **Authorization:** every new route behind `/admin`, the links loader and `can()`; a verified space
  refused before anything is written; confirm on the profile uses the profile's rule; nothing reachable
  by an owner through these routes.
- **Transactions and the write order:** every write and its audit inside the one transaction (`tx`
  passed everywhere); the shifts' order (remove → temporary rename → update → create → hours) safe
  under a name swap and a used shift; no nested write; the lock taken before any read used to decide.
- **The migration:** correct on existing rows (the fill), nothing else in the schema changed, the
  seed consistent with it.
- **Validation and normalisation:** the phone rule (every accepted form, the +972→+970 rewrite for
  59/56, separators only), the network URL rules (hosts, the Facebook id), A1's duplicate fields, the
  caps, `closes ≤ opens`, a shift outside every open day; nothing a client could send that reaches a
  500.
- **Freshness:** `missingGroups`, `staleGroups` ignoring nulls, `lastUpdate`, the list's `stale=true`
  including missing groups, consistent between the row and the filter.
- **Findings 31 and 41** truly resolved; the audit value type widening is safe.

### Subagent 2 — the tests, the contract, the documents and the conformance

**It checks:**
- **The caller matrix** on all 4 `PUT`s and 5 confirms; refused callers change nothing.
- **Each decision has a test that would fail with broken code** — check the breaks the PR description
  lists against the tests; titles match assertions; one behaviour in one lane; the concurrent lock
  test truly proves the lock.
- **The contract matches the code** (paths, bodies, statuses, shapes, errors); **`spaces.md`** states
  the code truly and owns only its own facts (no restated mechanism, endpoint shape, security rule);
  data-model.md (freshness, F3), conventions §2 and §10, overview's spaces line, `v1-mvp.md`,
  `lookups.md`'s one clause, findings 31, 36, 41 resolved and 42 accurate.
- **Finding 42:** is it a real flake worth its own finding, or a symptom of finding 28's class?
- **The commits:** seven, Conventional, ≤ 50 characters, each a complete unit.

## Your output

Write **one file**, `C:\Users\basel\.prompt\MASAHA_WORKER_A\REVIEW48_REPORT.md`: a one-line verdict;
the findings, most severe first, deduplicated (severity, file and line, scenario, fix); a short
"Verified OK" list per area; the tokens used. Then stop.
