# PR #57 — review fixes (one list)

Three independent reviewers read PR #57 on `3650759`; their findings were merged and each one was
verified against the code at that head. The merged report, with the evidence and line numbers, is
`C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\REVIEW57_MERGED_REPORT.md` — read its §3 for each item.
No blocker. Fold each fix into the commit it corrects (fixup + autosquash, `--force-with-lease`);
ONE "Review fixes" comment; the PR description updated. No subagents. Check each item against the
code first, and push back with reasons where one is wrong.

## Must fix
1. **After a creation, wait for the list itself** (R1). On `/new` no admin query is active, so
   `refresh()` resolves at once and the toast and the navigation come before the list is fetched (the
   list catches up on mount, briefly showing old rows). **Fix:** in the creation, refresh the admin
   scope with `refetchType: 'all'`, so the cached list is fetched and awaited before the toast and
   `onCreated`; keep the other writes as they are. **Test:** no list mounted beside the form — seed the
   list's cache with `setQueryData`, submit, and assert its GET happens before `onCreated`. Make the
   break (`'active'` again) once. Correct the JSDoc in `useCreateSpace.ts` and `useAddSpaceForm.ts` to
   say what now holds.
2. **A tile failure is shown whatever loaded before** (R2). **Fix:** judge each load cycle with
   Leaflet's own events: on `loading` reset a failure count; count each `tileerror`; on `load` set the
   status to failed if any tile of that cycle failed. Drop the `loaded` ref and the clear on every
   `tileload`; the status starts fresh with each layer (the language remount included). **Test:** the
   pure part (the cycle's verdict) in the unit lane; the events by hand in the browser, said in the
   report. Make the break (the old `loaded` guard) once if the test can see it.
3. **The first commit's subject is 52 characters** (R3): reword `df998c9` to
   `fix(design-system): keep the table off the site` (47).
4. **`libraryChunkOf` exists only for its test** (R4) — the owner's rule: remove it, and have
   `libraryChunks.unit.test.ts` test the `LIBRARY_CHUNKS` patterns directly (which entry's `test`
   matches each module id).

## Documents
5. **Dates** (R6): `Last Updated: 2026-10-10` on `docs/frontend/architecture.md`,
   `docs/frontend/design-system/foundation.md` and `docs/project/overview.md`, each in the commit that
   edits it.
6. **Finding 46's home** (R7): link it from architecture §6, in the map's "when it cannot load" part;
   and from `spaces.md`'s *Open findings*, since the add page is what exposes it.
7. **The findings index's numbering sentence** (R8): `docs/architecture/findings/README.md`, "A new
   finding takes the next number", contradicts the ranges each prompt gives (workflow §9
   *Conflicts*). Reword it: a new finding takes the next free number in the range its Work Item's
   prompt gives, linking workflow §9. **46 stays.** (The owner approved this one-sentence rule change.)

## No change
8. **The lock file's five `dev` → `devOptional` flips** (R5) stay: npm recalculated the flags of
   `@hookform/resolvers`' optional peer `ajv`; nothing runs `--omit=dev`, nothing imports them, and
   the lock is never edited by hand. Say so in one line in the PR description.

## The owner's answers to your report
- **The map at 400 px instead of 250:** accepted — at 250 the Strip was too thin to place a pin.
- **The table's chunk holding TanStack's store and a React helper:** accepted.
- **The Leaflet chunk check in commit 5:** accepted.
- **The new Arabic lines** (the PR's list): approved as written.

## Rebase, in the same push
PR #58 (the link check, worker B) merges before you push. It edits the *Commands* line of
`check:build` in `CLAUDE.md` and `docs/development/setup.md`, as you do: after the autosquash, rebase
on `origin/main` and take the **fast path** (workflow §9 *Conflicts*): keep both sides — your
library check and its new `npm run check:links` line. Then run `npm run check:links` once, which now
exists on `main`.

## Checks — only what the fixes touch
- Lint and typecheck on each rewritten commit.
- On the head, once: `test:unit` and `test:component` (items 1, 2 and 4 change tests); then
  `NODE_ENV=production npm run build` and `check:build` (item 4 touches the build script's module).
  **Not** `test:api`: nothing on the API changes; CI runs it.
- A real run for items 1 and 2: add a space and see the new row already in the list on arrival; block
  the tile server after the first tiles have loaded, pan, and see the line.
- Then `final-report`'s "Review fixes" section, with the merge-tree check against any other open PR.
  Don't merge.
