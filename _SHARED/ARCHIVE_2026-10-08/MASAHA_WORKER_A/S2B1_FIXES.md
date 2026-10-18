# PR #44 — review fixes (one list)

The review gate ran on `92d04ba` (no blockers, five should-fix); the analyst verified items 1 and 2
in the code. Fold each fix into the commit it corrects (fixup + autosquash onto the PR's own base,
`--force-with-lease`; GitHub shows the PR `CLEAN`, so don't rebase on `main`); no "fix" commits.
Then post ONE "Review fixes" comment and update the PR description. No subagents.

**Keep this round tight:** only these items, the smallest change that closes each; add only the tests
an item names. If an item turns out bigger than described, stop and report.

**Superpowers, selectively** (the owner adopted part of it): use `receiving-code-review` to check
each item against the code before fixing it, and push back with reasons where an item is wrong
(still ONE "Review fixes" comment, no thread replies); use `verification-before-completion` for
every claim in the comment and the description. For items 3 and 4, **make the break once**: remove
the retry (item 3) or make the delete deactivate the links (item 4), see the new test fail, restore.
Don't use any other Superpowers skill.

## Must fix

1. **The profile edit takes a second connection inside its transaction**
   (`profile.service.ts:43–67`: `view()` runs inside `runInTransaction`, and `spaceView.ts:20` reads
   the staleness thresholds without `tx`). Under concurrent edits the pool runs out. **Read the
   thresholds before opening the transaction** and pass them in (or build the view after it, as
   `create()` does) — and **use the same order in `create()`** (review nit 6): read the thresholds
   before the transaction, so an unreadable setting fails before anything is written, never as a 500
   for a space that now exists (a retry would create `…-2`). One rule for both paths.
2. **Finding 11's guard can never fail:** pg warns once per process through `util.deprecate`, and the
   listener is attached only in the file's last `describe`, after earlier creations have used the one
   warning. Move the guard to **its own test file** (or attach the listener before any creation in
   the file), so the first creation in the process is the one it watches. Then:
   - correct finding 11's resolution so it claims exactly what the test proves;
   - give the rule a lasting home: one sentence in `docs/backend/conventions.md` §8 › *Transactions*
     — inside an interactive transaction, write one statement at a time (no nested writes), and check
     this guard before upgrading `pg`'s major version.
3. **The slug race retry is untested, and its 409 is undocumented.** Add an API test that sends
   several creations with the same `nameEn` at once (`Promise.all`) and expects distinct slugs, all
   answered 201. Document the `conflict` (409) after three lost races in api-contract.md
   `POST /admin/spaces`.
4. **"Deleting writes nothing in `space_managers`" is unproven:** after `DELETE`, assert the link row
   is unchanged (`deactivatedAt` still null), and that `DELETE` then `restore` through the API gives
   the user their space back.
5. **Invalid new-space defaults are untested:** store a `newSpaceDefaults` value that fails its
   schema, then assert a 500 and nothing written (no space, no settings row, no audit entry).

## Cheap nits — fix
- **The links loader returns a deleted space's links** (`space-links.service.ts:50`): return no links
  for a soft-deleted space, so a future `/manage` guard built on it can't let a deleted space's
  managers through. One test.
- Skip `users.namesFor` when no listed space has an owner (`adminSpaces.service.ts:41`).
- Drop the two cross-lane duplicates (`adminSpaces.api.test.ts:164–177`; `requests.unit.test.ts:69–73`).
- Finding 18's resolution in `8c2ee31` claims restore before it exists: word it for that commit, and
  let the restore commit add the restore sentence.
- The contract's slug length: "the base, at most 60 characters, then the suffix".

## Checks — don't re-run what already passed
- Lint and typecheck on each rewritten commit.
- On the head, once each, one at a time: `test:unit`, `test:api`. Skip `test:component`,
  `check:classes` and `build` locally (no web change in this round); CI runs every lane.
- Report once CI is green and GitHub shows `CLEAN`: the head, what changed per item, which tests you
  saw fail first (items 3–5 and the loader nit), the counts. Don't merge.
