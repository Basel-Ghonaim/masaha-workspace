# FIX ADMIN EDITOR — review fixes for PR #61

From the analyst's conformance review of head `7aa5087` against the prompt, the approved plan, the
reply and the decision files (two read-only reviewers, findings checked in the code). The owner's own
visual review may add items below, under *From the owner*.

**How:** each fix folds into the commit of its decision (fixup + autosquash), then
`git push --force-with-lease`; ONE "Review fixes" comment; a "Review fixes" section in
`REPORT\FIX_ADMIN_EDITOR_REPORT.md`. Checks: your two scripts, `format:check`, `check:links`, and a
look with your own eyes at each fixed part at 390 and 1440 (and 768 where it is a table). Stop every
background shell you start; `jq` is not installed — use `gh … --jq`.

## Against the plan or the reply

### R1 — A price of 0 is accepted (DI-16 built against the reply)
`profile-b.jsx:31` now takes `Number(r.amount) >= 0`; the reply kept DI-16 out of this item. Keep
your new refusal of an empty amount, and refuse 0 again (an amount above zero), with the base's
wording. Not stated in the report: add it to its departures, then the fix.

### R2 — DI-13 protects only the sample shifts
A shift added in the session keeps `id: null` in the section's state while Save publishes a random
id (`profile-a.jsx:359`, `:416`), so `inUse` (`:396`) is never true for it, and a second hours save
gives it another id, leaving the saved price pointing at nothing. **Fix:** a saved shift keeps the id
it was given, in the section's state too (the contract's "a saved shift keeps its id"), so a price
naming it protects it and survives the next save.

### R3 — A day's «إلى» error does not block Save
`profile-a.jsx:380` shows «بعد البداية» when to ≤ from, but the section's check (`:348-358`) never
reads the days, so Save succeeds with the error on screen, and the focus can land on that day while a
shift blocked the save. **Fix:** the days' errors are part of the section's check, the focus goes to
the first error in order.

### R4 — The default editor frame shows no photo tiles
`?id=golden` opens on «لا صور بعد.» because `Admin space edit.html:130` ties the gallery's emptiness
to `missing: ['photos']`; reorder, «اجعلها الغلاف» and the delete dialog appear only on other ids.
The report says this was approved in the plan; it was not (the plan says "no sample data changes").
**Fix:** the gallery is empty only for a new space (`?id=new`); `?id=golden` shows its tiles again.
Correct the report's line.

### R5 — The verified page's hours have no shifts
Plan §4 E5: "the hours with the shifts". `ReadOnlyView` (`Admin space edit.html:84`) lists the day
ranges only. **Fix:** list the shifts under the hours, as the editor does.

## Correctness

### R6 — The gallery's counting
In `profile-b.jsx`: rejected or failed tiles count toward the 10-photo limit (`:234`, `:250`); files
past the remaining room are dropped silently (`:235`); the tile counter starts at 6 on an empty
gallery (`:219`); a rejected tile first in the list takes the cover badge from the first real photo
(`:265`). **Fix:** only uploaded photos count and take the cover; files past the room are refused
with a line that says how many were left out; the counter follows the photos.

### R7 — A half-typed time can be saved
`ClockInput` (`profile-a.jsx:313`) passes a value such as `12:75`, or `24:30` in an end field, up
before blur, and Enter submits without a blur. **Fix:** an invalid time is not passed up (or is
refused on its field at save).

### R8 — «فك ربط ؟» for a space with no owner
`Admin spaces.html:33` takes `owners[0]`; for `?unlink=golden` the dialog reads «فك ربط ؟». **Fix:**
no dialog when the space has no owner.

## The check scripts and the archive's documents

### R9 — The README says more than the scripts check
`check-classes.mjs:41-42` reads only literal `class=`/`className=` values: not a conditional
(`profile-a.jsx:278`), `cn(…)`, other props (`contentClassName`) or object keys
(`Admin spaces.html:62`). `KNOWN` is a global allow-list by name, so a new use of a known dead class
in another file passes. **Fix:** the README paragraph names these limits, as the script's header
does; the baseline is per file and class, so a new use elsewhere fails. In `check-parse.mjs:18`, the
comment ("registers itself on `self`") says how it really loads (the root `"type": "module"` and
`globalThis.Babel`).

### R10 — The baseline changed in the gallery's commit
`KNOWN` holds five DI-9 classes plus `wm-a` and `wm-word`, and `h-28` was dropped in `e6e22ce`, not
in E8's commit. Fold the baseline into E8's commit and say in the report why it is these seven.

### R11 — Small leftovers
- `docs/design/README.md:25` says 39 pages; there are 40.
- Dead code: `savedOnce`/`setSavedOnce` (`profile-a.jsx:341`, `:359`) and the unreachable
  `out.limit` (`:356`).
- The report's departures also name: the duplicate-price wording («سعر مكرّر: غيّر هذا الحقل», not
  the plan's) and DI-12's English label appearing only once the Arabic is typed — both accepted as
  built.

## Seen and accepted (no change)

- A never-saved hours group opens on the Saturday–Thursday template: that is the API's D9 ("the form's
  starting point, not data", `spaces.md`).
- The owner's page does not mount the checklist: batch 5 (O1).
- `?id=palm` borrows Golden Hub's content under its own name: sample data, 2b's.

## From the owner

_(to be added after the owner's visual review)_
