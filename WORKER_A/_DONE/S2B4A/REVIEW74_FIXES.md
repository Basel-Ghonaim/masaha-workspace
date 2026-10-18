# S2b-4a — review fixes for PR #74 (one round)

The independent review is in `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\REVIEW74_CLAUDE_REPORT.md`
(head `b5406c0`). **Read it whole**: each finding below names its file, its scenario and the fix it
proposes; that report is the detail, this list is the decision. The analyst checked findings 1, 2
and 3 in the code: all three hold. **The owner chose one round on this PR, everything in it.**

Follow `receiving-code-review` as workflow §10 adapts it: verify each item against the code before
changing anything, and push back with reasons where one is wrong. Fold each fix into the commit it
corrects (fixup + autosquash), never a fix commit; every subject stays ≤ 50.

## Must fix

1. **The section jumps (finding 1, plausible blocker).** First **reproduce it in a real browser**
   (open the list fresh, open a space's editor, click a chip and a «ما زال ناقصًا» line; at 390 and
   1440). Whatever you see, replace the plain `<a href="#id">` in `SectionNav` and `MissingChecklist`
   with React Router's `<Link to={{ hash: id }}>` through `Button asChild` (the leave guard must still
   let it through, with no dialog; `scroll-mt-*` respected). A test clicks the chip itself and expects
   the hash location with no dialog. Report what the browser showed before and after.
2. **A deleted space stays editable (finding 2).** A 404 shows the 404 state even when old data is
   cached (or the query is removed on a 404); a test: a 404 on a save shows the 404 and the leave
   guard no longer asks.
3. **A dirty profile can undo another admin's change (finding 3).** Diff against the values the form
   was last reset from (or the dirty fields), never against the latest server answer; keep the
   comparison with `space` only for the "nothing changed" note. A test: another admin's change
   arrives while the section is dirty; the save sends only the admin's own fields.
4. **The confirm during a 429 (finding 4).** The confirm is disabled while its wait counts down, with
   its reason; Save too while that wait runs (the limit is the user's).
5. **The hooks' logic in hook tests (finding 5, the owner: now — this editor is the pattern S2b-4b and
   the owner's editor copy).** Move the logic now proven through `SpaceEditor.component.test.tsx`
   (request bodies as the hook prepares them, the "unchanged" rule, dirty tracking, the leave guard,
   the refusals, the section in view) into `renderHook` tests of the hooks that hold it
   (`hooks/editor/*`, `hooks/profile|amenities|contacts|confirm/*`, lookups' `useAmenityChecklist`,
   `useAreaName`, `useAmenityNames`), as testing §3's table says; the component test keeps what
   rendering decides; method and URL checks leave it (the repository's test owns them). Each moved
   test still seen failing by its break.
6. **The six behaviours no test catches (finding 6 (a)–(f)),** each as the report says, written as
   hook tests (5) or a unit test (`services/amenitiesForm.ts`), each break made once and seen failing.
7. **`spaces.md` and `lookups.md` (finding 7 (a)–(c) and finding 21):** no label collision (point to
   #57's superseded decision by its name, or drop #74's labels); #50's "No Edit … yet" and "a write
   fetches the whole admin scope again" restated as they hold today; "items" → "actions"; D5 says the
   sections hold no admin-only interface but call the admin's endpoints until the owner's exist; the
   code map names folders only; no unbuilt intent in a Description; the retired-amenity rule stated
   once and linked.

## Also fix (findings 8–20)

8. A contact's type change revalidates once submitted (`shouldValidate: formState.isSubmitted`).
9. **The owner's choice:** a save that lands while the leave dialog is open **proceeds** with the
   navigation the admin asked for (nothing is left to lose); while a save is pending, the dialog says
   the changes are being saved, not that they will be lost (both languages; list the new lines in
   the PR description for the owner's approval).
10. The section in view follows the scroll after a 403 turns the page read-only.
11. `<SpaceEdit key={spaceId} …>`: a change of space resets the editor.
12. The record title cleared before the next page paints (`useLayoutEffect`), if it holds.
13. "Nothing changed" and a save's section failure cleared on Discard and on a confirm's success.
14. A write does not mark the answer it has just stored as out of date.
15. "Add space" does not wait on refetching every cached editor query.
16. Remove disabled while a save is pending (amenities and contacts).
17. The read-only amenities keyed uniquely (not by an English name that may repeat).
18. A mixed 422 keeps the `amenityIds` refusal, and the amenities list is refetched so the retired
    one shows its badge.
19. `beforeunload` sets `returnValue` as well as `preventDefault()`.
20. The test titles and data the report names (`updatedAgo`'s title, the discard test's missing
    check, the add-flow test asserting no `GET /admin/spaces/7`, the unused `data-testid`).

If a fix turns out larger than the report says, or needs a file outside `apps/web` and the
documents, stop and say so.

## Then

- **Verify again (phase 4), once each on the new head, one at a time:** `test:unit`, `test:component`
  (first check that worker B in `masaha-b` and the media worker in `masaha-media` run no lane), the
  build with `NODE_ENV=production` and `check:build`, `lint`, `typecheck` (on each commit),
  `check:classes`, `format:check`, `check:links`. A real run: the chips and checklist lines in the
  browser (finding 1), a dirty profile meeting another admin's change (finding 3), a deleted space's
  save (finding 2), a confirm under a 429 if you can produce one. Fresh screenshots of anything that
  changed, in `Downloads\s2b4a-shots\`. Stop the servers by PID and check the ports free.
- **Push** with `git push --force-with-lease`; wait for CI on the pushed head and `CLEAN`.
- **One "Review fixes" comment** on #74: each finding's number and what was done (or why not), no
  replies in threads. Update the PR description to the final state.
- **Add a "Review fixes" section to `REPORT\S2B4A_REPORT.md`** in the report's order (`final-report`
  step 5), with the pushed-back items and their reasons.
- No tool attribution anywhere. Don't merge. Stop every background shell you start; `jq` is not
  installed — use `gh … --jq`.
