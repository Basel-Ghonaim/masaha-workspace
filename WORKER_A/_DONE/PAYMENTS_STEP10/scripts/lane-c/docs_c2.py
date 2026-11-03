"""Commit 2's documents: data-reports.md, directory.md, finding 168 and its index line."""
import sys

ROOT = r'C:\dev\masaha\app-lane-c\docs'


def edit(path, old, new):
    full = ROOT + '\\' + path
    with open(full, encoding='utf8', newline='') as f:
        text = f.read()
    if text.count(old) != 1:
        sys.exit(f'{path}: anchor found {text.count(old)} times: {old[:70]}')
    text = text.replace(old, new, 1)
    with open(full, 'w', encoding='utf8', newline='') as f:
        f.write(text)


D = 'features\\data-reports.md'
edit(D, "The API is built; on the web, the owner's «بلاغات البيانات» and a signed-in user's «بلاغاتي».",
     "The API is built; on the web, the owner's «بلاغات البيانات», a signed-in user's «بلاغاتي» and the report from a space's page.")
edit(D, "the decision sheet; the user's own reports.",
     "the decision sheet; the user's own reports, and the report's button and dialog a space's page sets.")
edit(D, "On the site, the user reads «بلاغاتي» (`/me/reports`) and the replies, linked from the account menu (2026-10-28, #PRNUM). The space page's report button is not built.",
     "On the site, the user reads «بلاغاتي» (`/me/reports`) and the replies, linked from the account menu, and reports from a space's page; a guest's press asks them to sign in first (2026-10-28, #PRNUM).")
edit(D, """Its states: three skeleton cards while loading, a failure with its reference and a retry, a failed refresh over the cards shown, «لم ترسل أي بلاغ بعد» with «تصفّح المساحات», and «لا توجد بلاغات هنا» under a chip.
""", """Its states: three skeleton cards while loading, a failure with its reference and a retry, a failed refresh over the cards shown, «لم ترسل أي بلاغ بعد» with «تصفّح المساحات», and «لا توجد بلاغات هنا» under a chip.

**The report on the web** (`ReportAction`, set by `pages/site/public/space/SpacePage.tsx` in the directory's `report` slot, at the end of the page's main column). «الإبلاغ عن معلومة غير صحيحة» opens a dialog: who reads it, by the space's verification — «بلاغك عن {name} يصل إلى إدارة المساحة، وتجد ردّها في «بلاغاتي».» for a verified space, «…يراجعه فريقنا، وتجد الردّ في «بلاغاتي».» otherwise; «ما المعلومة غير الصحيحة؟», focused first, with the six field groups; «التفاصيل», said optional except for «أخرى», whose missing details say «اكتب ما الخطأ في «أخرى».»; «رجوع» and «إرسال». It is sent once, with no key. A refusal keeps it open with every value, the failure an alert above the footer: a space gone says «لم تعد هذه المساحة في الدليل.», a 429 counts down with the send blocked, and no answer says «لم يصل الرد. أعد المحاولة — لن يُرسَل البلاغ مرتين.» with a retry. Done, it closes, the user's reports are read again, and the toast says where the reply lands — «أرسلنا بلاغك إلى إدارة المساحة. ستجد ردّها في «بلاغاتي».» or «…إلى فريقنا. ستجد الردّ في «بلاغاتي».» — or, when the server answered with the open report (200), «أرسلت بلاغًا عن هذا من قبل، وما زال قيد المراجعة.», each with «عرض بلاغاتي». Closed, the focus returns to the button. A guest's press holds the report in memory and the page asks them to sign in, «سجّل الدخول للإبلاغ عن معلومة», with «إنشاء حساب» and «تسجيل الدخول», each carrying the page as the one to return to; back on the page signed in, the dialog opens, once. Closing the sign-in lets the held report go.
""")
edit(D, """- **The reply is labelled by who replied** (DI-56):""", """- **The details are required for «أخرى» only, said optional otherwise** (DI-44, not A11): the contract requires them there alone, and one rule has one owner. 2026-10-28, #PRNUM.
- **The dialog says who reads the report, by the space's verification** (DI-45, U10): the space's management for a verified space, «فريقنا» otherwise, and where the reply will be found. 2026-10-28, #PRNUM.
- **A refusal keeps the dialog open with every value** (DI-46): the failure is an alert above the footer; a 429 counts down; no answer says a retry is safe, since a repeat answers the open report. 2026-10-28, #PRNUM.
- **The toast says where the reply lands, or that one is already open** (DI-47, DI-48), with «عرض بلاغاتي». *Why:* the repository reads the answer's status — 201 a new report, 200 the open one (S15) — so the user is never told a second report was filed. 2026-10-28, #PRNUM.
- **A report is sent once, with no key** (S4): a repeat answers the open report, so a lost answer is retried from the dialog. 2026-10-28, #PRNUM.
- **A guest's report waits in memory, never in the address** (S14, DI-60, DI-61): the press holds the space's slug and the page asks them to sign in with the reason; the held report opens the dialog once they are back signed in, and is let go if they close the sign-in. *Why:* a link carrying the intent would let a crafted link act for a signed-in user. *Cost:* a reload, or a recovery by email, loses it ([finding 168](../architecture/findings/168-a-guests-intent-does-not-survive-a-password-recovery.md)). 2026-10-28, #PRNUM.
- **The reply is labelled by who replied** (DI-56):""")
edit(D, "(`SpaceReportsList`, `MyReportsList`), read by",
     "(`SpaceReportsList`, `MyReportsList`, `ReportAction`), read by")
edit(D, "and `pages/site/account/MyReportsPage.tsx`, which gives the spaces' and the directory's links:",
     "`pages/site/account/MyReportsPage.tsx`, which gives the spaces' and the directory's links, and `pages/site/public/space/SpacePage.tsx`, which sets the report in the directory's slot with the site's sign-in:")
edit(D, "the card's type in `types/MyReportCardView.ts`.",
     "the card's type in `types/MyReportCardView.ts`; the report, its write and its dialog's view in `hooks/report/`, a guest's held report in `hooks/intent/reportIntent.ts`, its button and dialog in `components/report/`, its toast in `components/toast/`.")
edit(D, """## Open findings

None.""", """## Open findings

- [168. A guest's intent does not survive a password recovery](../architecture/findings/168-a-guests-intent-does-not-survive-a-password-recovery.md) — the report held for a guest is lost by a reload or a recovery by email.""")
edit(D, """- 2026-10-28, #PRNUM — «بلاغاتي»: a signed-in user's own reports, the replies labelled by who replied, a space that left named as text; linked from the account menu.
""", """- 2026-10-28, #PRNUM — «بلاغاتي»: a signed-in user's own reports, the replies labelled by who replied, a space that left named as text; linked from the account menu.
- 2026-10-28, #PRNUM — the report from a space's page: who reads it by the space's verification, the details required for «أخرى» only, the toast by the answer's status; a guest asked to sign in first, the report held in memory.
""")

R = 'features\\directory.md'
edit(R, "- **The page draws no report button and no favourite heart, and no closure's notice yet** (decision 4; design issues 23, 34; [finding 131](../architecture/findings/131-the-space-page-cannot-show-a-closures-notice.md)). *Why:* v1's step 10 builds them. 2026-10-22, #107.",
     "- **The page draws no report button and no favourite heart, and no closure's notice yet** (decision 4; design issues 23, 34; [finding 131](../architecture/findings/131-the-space-page-cannot-show-a-closures-notice.md)). *Why:* v1's step 10 builds them. 2026-10-22, #107. The page's report button is `data-reports`', set by the page in the details' `report` slot, which hands it the space's slug, name and verification, at the end of the main column (2026-10-28, #PRNUM).")

with open(ROOT + '\\architecture\\findings\\168-a-guests-intent-does-not-survive-a-password-recovery.md', 'w', encoding='utf8', newline='') as f:
    f.write("""# 168. A guest's intent does not survive a password recovery

**Status:** Open · **Date:** 2026-10-28

**Evidence:** a guest who presses an action that needs an account — the report of wrong information on a space's page (#PRNUM) — is asked to sign in, and the action is held in memory only, never in the address (PAYMENTS_STEP10 S14): a link carrying it would let a crafted link act for a signed-in user. The site's sign-in, register and Google keep the page alive, so the held action runs once the session is established. A reload, or a password recovered by email (whose link opens a new page), loses it (AU-UX-001): back signed in, the user presses again.

**Resolves when:** the held action survives a new page without travelling in the address (a short-lived, same-origin store the session confirms), or the owner accepts pressing again as enough.
""")

I = 'architecture\\findings\\README.md'
edit(I, """- [166. The ledger's staff filter cannot name a space's other owners](166-the-ledgers-staff-filter-cannot-name-a-spaces-other-owners.md)
""", """- [166. The ledger's staff filter cannot name a space's other owners](166-the-ledgers-staff-filter-cannot-name-a-spaces-other-owners.md)
- [168. A guest's intent does not survive a password recovery](168-a-guests-intent-does-not-survive-a-password-recovery.md)
""")
print('ok')
