# WOMEN_EVENING — the approved texts, then the PR (the message to paste to the worker)

Resume the worker's conversation from `C:\dev\masaha\app` (see `5_RESUME_MESSAGE.md` for the command), then paste:

```
Supervisor's message (relayed by the owner).
1. The owner approved new wordings for the three texts of X6 (recorded in 0_OWNER_DECISIONS.md › The Arabic texts). Replace them, folded into the commits that introduced them (a backup/* first; --fixup + autosquash):
   - copy.spaces … evening.help (ar): «يظهر للزوار «دوام مسائي»، وساعات العمل أعلاه تحدّد حتى متى تبقى المساحة مفتوحة.» — en: "Visitors see “Evening hours”; the opening hours above set until when the space stays open."
   - copy.spaces … evening.early (ar): «شغّلت الدوام المسائي، لكن ساعات العمل لا تمتد بعد 18:00 في أي يوم.» — en: "Evening hours are on, but the opening hours don’t go past 18:00 on any day."
   - errors AMENITY_IN_FILTER (ar): «لا يمكن إيقاف هذا المرفق، فدليل المساحات يعتمد عليه في فلتر «قاعة للنساء». يمكنك تغيير اسمه وأيقونته وترتيبه.» — en: "This amenity can’t be retired: the directory relies on it for the “Women’s hall” filter. You can still rename it, change its icon or move it."
   Update any test or document that quotes the old words. The owner waived commit 6f6a59ab's 51-character subject: leave it.
2. The owner's word: run no tests and no local checks for this text change — CI on the pushed head checks it (phase 2 was fully verified locally; say this exception in the PR's Evidence and in the report).
3. The owner's word is given: push and open the PR with the open-pr skill — #PRNUM replaced with the real number just before the push (expected #145; check), the description's "Review fixes carried from #144" (R2-F4's corrected figure included), the X decisions, the migration, the merge-day effect (E8's switch-on, the women's hall row). Then wait for CI green on the pushed head and CLEAN, write a "PR" section in 4_REPORT.md with the full head sha, and stop. Never merge.
```

**The owner gave the push word on 2026-11-14 ("OK — but no tests; leave the checking to CI"):** paste all three items.
After the PR is green: the supervisor launches the review (`6_REVIEW_PROMPT.md`).
