import os
os.chdir(r'C:\dev\masaha\app-lane-w2\docs')
for p, line, hist in [
 ('features/spaces.md', """- **The spaces list and the editor finish their screens** (D6.10, G26.1–G26.3, G26.8, G20.2): a verified row's menu reads «عرض (يعدّلها المالك)» (its owner edits it; an unverified row's «تعديل»); hiding and showing toast «تراجع», which sends the opposite (P9: reversible, no one else affected; the undo's own toast offers none); the delete dialog's dismiss is «رجوع» (P9); a verified space's notice adds «لتصحيح معلومة:» and «بلاغات {space}», a link to the admin's reports of the space (`AdminPlace.reportsLink`); below 768 px a section's header action («نسخ إلى كل الأيام») leads its content instead of sitting beside the title. 2026-10-29, #PRNUM.
""", "- #PRNUM — the spaces list and the editor: «عرض (يعدّلها المالك)», «تراجع» after hiding or showing, «رجوع» in the delete dialog, the verified notice's way to the space's reports, a section's action leading its content on a phone.\n"),
 ('features/space-links.md', """- **The spaces list's phone sheet and missing badge** (D6.10, G26.4, G26.5): the sheet's primary, full-width «عرض {n} نتيجة» closes it on the list, and «مسح الفلاتر» is a `ghost` button, unavailable with no filter on (P5); the missing badge reads «ناقصة: {groups}». 2026-10-29, #PRNUM.
""", "- #PRNUM — the spaces list's phone sheet closes on «عرض {n} نتيجة», its clear unavailable with none; the missing badge «ناقصة: …».\n"),
]:
    s=open(p,encoding='utf8').read()
    a="### Web decisions\n\n"
    assert s.count(a)==1,p
    s=s.replace(a,a+line,1)
    s=s.rstrip('\n')+"\n"+hist
    open(p,'w',encoding='utf8',newline='').write(s)
