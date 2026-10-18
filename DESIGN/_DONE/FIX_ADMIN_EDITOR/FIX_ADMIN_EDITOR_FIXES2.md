# FIX ADMIN EDITOR — review fixes, round 2 (the owner's look at PR #61)

The owner looked at the editor on head `1a08fcf`. Three small changes, decided by the owner; build
nothing else. Same method as round 1: fold each into the commit of its decision (fixup + autosquash),
`git push --force-with-lease`, ONE "Review fixes" comment, a new section in
`REPORT\FIX_ADMIN_EDITOR_REPORT.md`. Checks: your two scripts at every commit, `format:check`,
`check:links`, and a look at the hours and amenities sections at 390 and 1440, on both
`Admin space edit.html?id=golden` and `Owner space profile.html`. Stop every background shell you
start; `jq` is not installed — use `gh … --jq`.

## O1 — No «24 ساعة» switch (AD-009 amended by the owner)

No coworking space in Gaza opens around the clock, so the switch is one more decision nobody takes.
Remove it from every day row, and every trace of it in the prototype (`allDay`, `rangeText`'s
«24 ساعة», «نسخ إلى كل الأيام»'s copying of it, the verified page's read-only hours, `CHANGES.md`'s
E4 line, any `INDEX.md` row or frame that shows it). A day that closes at midnight is still entered
as «إلى» 24:00 (DI-15); keep that. The API is unchanged.

## O2 — Each day says whether it is open

Only Friday says «مغلقة»; an open day's switch has no visible word. Beside each day's switch show
its state, «مفتوحة» or «مغلقة», the same way on every day (the switch keeps its accessible name).

## O3 — «إدارة قائمة المرافق» on the admin's editor

Under the admin's amenities list, a link «إدارة قائمة المرافق» to `Admin lookups.html?tab=amenities`,
for an amenity the list lacks. **The admin's editor only**: the owner's page keeps its amenities as
they are (a larger decision on amenities is pending with the owner; do not anticipate it).
