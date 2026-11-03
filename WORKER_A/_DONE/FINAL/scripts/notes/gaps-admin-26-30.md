# Gaps 26–30 (agent report)

## 26 Spaces — partial (add page complete)
1. Verified row menu says «تعديل»; design «عرض (يعدّلها المالك)» for verified. SpaceActionsMenu.tsx:74; Admin spaces.html:59. S: label by isVerified, add menu.view ar+en.
2. Hide/Show toast no «تراجع» (P9). useSetSpaceHidden.ts:31; Admin spaces.html:43. S.
3. Delete dialog dismiss «إلغاء»/"Cancel" → «رجوع»/"Back". copy arabic spaces.ts:326, english :398. S.
4. Phone filters sheet lacks primary «عرض N نتيجة»; clear is outline not ghost, never disabled. space-links/components/admin-list/FiltersSheet.tsx:49; shared.jsx:613-614 (P5). S (reports sheet already does it).
5. Missing badge «غير مُدخلة:» vs chip «قديمة أو ناقصة» → «ناقصة: …». spaceLinks.ts:41. S.
6. ?status=editable&stale=true falls back to all → 158.
7. Editor has no report notice (?report=<id>#report): «بلاغ مفتوح على {field}», quote, reporter+date, «تم التصحيح», «فتح البلاغ للرد». Admin space edit.html:67-90. M. Admin: GET /admin/data-reports?spaceId=&field=&status=OPEN (no single read); sheet's «تعديل الحقل» adds ?report=<id>.
8. Verified notice lacks «بلاغات {space}» link (→ reports ?space=<id>) and «لتصحيح معلومة:». editor/VerifiedNotice.tsx:14-30; Admin space edit.html:146. S.

## 27 Owners — partial
9. «إجراءات» column header visible (should be sr-only): OwnersList.tsx:79; UsersList.tsx:111. S.
10. Empty state lacks «إضافة مالك». ListState.tsx:36; Admin owners.html:152. S.
11. Add sheet ACCOUNT_SUSPENDED no way out: «الحساب موقوف — استرجعه أولًا» linking users ?q=<email>. spaceLinks.ts:214. S.
12. «مالك جديد بلا حساب؟» lands on owners page without opening add sheet: owners page opens sheet on ?sheet=add. SpaceEditPage.tsx:42. S.
13. ALREADY_OWNER no «اربطه بالمساحة» → ?link=<owner>&space=<id> → 83.

## 28 Admin data reports — partial
14. Sheet title doesn't name the space: admin title «{space} · {field}». useDecideSheet.ts:110; Admin reports.html:86. S.
15. No ?open=<reportId> deep link. adminReportsQueryOf.ts. S.
16. Sidebar badge of reports waiting for the admin («بلاغات بانتظار الإدارة») missing. S–M: from ?status=OPEN&handledBy=ADMIN total.
- «يعالجه» filter: not offered; DI-39 decided no filter and prototype has none → not a gap (owner's call). NOTE: prompt says finding 167's filter on screen 28 is a gap the API now closes → OD/DI.

## 29 Users — partial (minor)
17. «انضم» drops the year when this year; design always with year. userRowView.ts:48. S.

## 30 Lookups — partial
18. Edit sheets still hold Active switch (AD-025 switches in row only). LookupForm.tsx:16, AmenityForm.tsx:18. S.
19. No «الترتيب» position field for list > 10 rows (AD-026). M: position 1–n via order endpoint.
20. Arrows' names lack position «… — {i} من {n}», no polite live region «{name}: {j} من {n}». lookups.ts:40. S.
21. Amenities tab shows governorates' hint; own line «غير النشط لا يظهر في النماذج، وتحتفظ به المساحات التي لديها. الترتيب هنا هو ترتيب الظهور.» LookupsPage.tsx:24. S.

Decided deviations: no owner items in spaces row menu (L7 — reason lapsed, owner may reopen); cards until 1024; deleted muted; verified notice owner names not link (DI 9); owners state chips; users role/state chips, spaces column, «ربط بمساحة»; role change destructive; unlink no prediction; upgrade only once shown; own row «أنت»; governorates English first; reports chips DI-31, no current value DI-33, «ردّ فريقنا» DI-56, no «يعالجه» DI-39, cards until 1024 DI-43; «صاحب المساحة».
UNVERIFIED: widths and dark from class names only.
Total 21.
