# PR #48 — review fixes (one list)

The review gate ran on `c4e993d` (no blockers, six should-fix); the analyst verified items 3, 4 and 6
in the code. Fold each fix into the commit it corrects (fixup + autosquash, `--force-with-lease`;
GitHub shows the PR `CLEAN`, so don't rebase on `main`); no "fix" commits. Then post ONE "Review
fixes" comment and update the PR description. No subagents. Follow workflow §10:
`receiving-code-review` first (check each item, push back with reasons where one is wrong); **make
the break** for every new or strengthened test, and list the breaks in the comment.

The report is `C:\Users\basel\.prompt\MASAHA_WORKER_A\REVIEW48_REPORT.md`.

**Keep this round tight:** only these items, the smallest change that closes each; add only the tests
an item names.

## Must fix

1. **The refused-caller tests prove nothing for prices and amenities:** their request bodies change
   nothing, so an admin's request writes nothing either. Give every refused-caller case a body that
   **would** change the group (and its date and audit) if it got through, so "a refused caller changes
   nothing" can fail. Break: let one refused role through, see the test fail, restore.
2. **Three of the four "missing group" conditions in the list's `stale` filter are untested** (only
   hours is). Add the prices, amenities and contacts cases (table-driven is fine). Break: delete each
   condition once.
3. **A network value with a dot is taken as a handle** (`contacts.ts:20`, `HANDLE` allows `.`): a
   Facebook value `profile.php` is stored as `…/profile.php` with no id, getting around the id rule,
   and `instagram.com` becomes `https://www.instagram.com/instagram.com`. A value that looks like a
   host or a path (contains `/`, or ends in a known domain such as `.com`, or is `profile.php`) is
   **not** a handle: it must parse as a URL on the network's host (and Facebook's `profile.php` must
   carry its numeric `id`), else 422 `invalid_format` on `contacts.<i>.value`. Keep real handles with
   dots working (`my.space_gaza`). One unit case each.
4. **`spaces.md` says every group saves through one path, but the profile's edit has its own copy**
   (`profile.service.ts`: its own `runInTransaction` and `lock`). **The owner's choice: move the
   profile edit onto the shared `groupEdit` path**, so the lock, the deleted and verified refusals,
   the date, the audit and (in step 5) the owner's reuse live in one place. Its behaviour, responses
   and audit entries stay exactly as they are (its existing tests are the proof). If the move turns out
   larger than a refactor of that one service, stop and report instead.
5. **`spaces.md` restates facts other documents own:** the contact storage forms (data-model.md owns
   them) and the size caps (the API contract owns them). Replace each with a link.
6. **Commit subject over 50 characters:** `feat(spaces): confirm fact groups, missing until set` (52).
   Shorten it, for example `feat(spaces): confirm groups; missing until set` or
   `feat(spaces): add confirm and missing fact groups`.

## Nits — fix
- The retired-amenity test asserts the retired link is actually kept after a save that keeps it.
- The contract's audit wording for hours never saved matches what is recorded.
- Accept `+970 (0)59 912 3456`: a `(0)` after the country code is dropped before the phone rule (one
  unit case).
- **Record one finding (number 43)** for the two races the review names, evidence only: an admin's save
  can land on a space that was verified a moment before (the save locks the space's row; creating an
  owner link, in step 4, doesn't take that lock), and an unlocked read during an hours save can show
  the old week with the new shifts. It resolves when step 4's linking takes the space's lock and the
  read is consistent (one statement or one snapshot).

## Checks — don't re-run what already passed
- Lint and typecheck on each rewritten commit.
- On the head, once each: `test:unit`, `test:api`. Skip `test:component`, `check:classes` and
  `build` locally (no web change in this round); CI runs every lane.
- Report once CI is green and GitHub shows `CLEAN`: the head, what changed per item, the breaks made,
  the counts. Don't merge.
