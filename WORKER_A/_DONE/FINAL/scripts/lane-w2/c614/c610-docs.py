import glob, os
os.chdir('C:/dev/masaha/app-lane-w2')


def edit(p, pairs):
    s = open(p, encoding='utf8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)


def append_history(p, heading, line):
    s = open(p, encoding='utf8', newline='').read()
    i = s.index(heading)
    j = s.find('\n### ', i + 5)
    j2 = s.find('\n## ', i + 5)
    ends = [k for k in (j, j2) if k != -1]
    j = min(ends) if ends else len(s)
    section = s[i:j].rstrip('\n') + '\n' + line + '\n'
    rest = s[j:]
    s = s[:i] + section + (('\n' + rest.lstrip('\n')) if rest else '')
    open(p, 'w', encoding='utf8', newline='').write(s)


P = 'docs/features/data-reports.md'
s = open(P, encoding='utf8').read()
anchor = "**The user's reports on the web**"
assert s.count(anchor) == 1
notice = """**The report notice on the web** (`ReportNotice` and `useReportNotice`, set by the owner's space profile and Packages & prices and by the admin's space editor). A report the address names (`?report={id}`) is read by its id (`GET …/data-reports/:reportId`, S5), never searched for in a page of the list. Open, its notice draws above the section its field is edited in — the place and «أخرى» above the profile's «المساحة», each other field above its own section, the prices above Packages & prices' prices — through the editor's `noticeFor` slot ([spaces](spaces.md)): an info alert, `#report`, titled «بلاغ مفتوح على {field}», the report's words quoted with who and when («“…” — زائر، 21 أكتوبر» to the owner, never naming the reporter; the reporter's name to the admin), then `primary` «تم التصحيح», which marks it corrected in place (`RESOLVED`, no reply) and says «عُلّم «تم التصحيح»» with «العودة إلى البلاغات», and «فتح البلاغ للرد», the reports list with `?open={id}`. A report decided already, not found, of another space, or — for the admin — a verified space's draws nothing. Each sheet's «تعديل الحقل» carries its report (`?report={id}#{section}`, «أخرى» landing on `#report`), and both lists open the report `?open={id}` names, read by its id when the page does not show it; closing the sheet takes `?open` off the address (D6.8, 2026-10-29, #PRNUM).

"""
s = s.replace(anchor, notice + anchor, 1)
open(P, 'w', encoding='utf8', newline='').write(s)

s = open(P, encoding='utf8').read()
i = s.index('### Web decisions')
j = s.index('\n## ', i)
block = s[i:j].rstrip('\n')
block += """
- **One report is read by its id where the address names it** (the notice's `?report=`, the lists' `?open=`), never found in a page of the list (S5). *Why:* a report on page three, or under another chip, would be missed. Its key sits under its audience's reports, so a decision reads it again. 2026-10-29, #PRNUM.
- **The notice marks a report corrected in place, with no reply; a reply is the sheet's.** *Why:* the owner fixed the field where the notice stands; «فتح البلاغ للرد» leads to the sheet for anything more. The notice keeps saying it was marked once its read answers it decided. 2026-10-29, #PRNUM.
- **The admin's notice draws nothing for a verified space's report.** *Why:* its owner decides it, and the admin's editor of a verified space is read-only. 2026-10-29, #PRNUM.
"""
s = s[:i] + block + '\n' + s[j:]
open(P, 'w', encoding='utf8', newline='').write(s)
append_history(P, '### Web history', "- #PRNUM — the report notice above its field's section (`?report=`), «تعديل الحقل» carrying the report, and both lists opening `?open=` (D6.8).")

S = 'docs/features/spaces.md'
s = open(S, encoding='utf8').read()
i = s.index('### Web decisions')
j = s.index('\n## ', i)
block = s[i:j].rstrip('\n')
block += """
- **The editor lands on the section its address's hash names, once its cards have drawn** (`useHashLanding`, finding 184): it scrolls there and focuses the section's heading, which carries `tabIndex={-1}`; once per opening, a later hash change being the shell's. *Why:* the cards draw only after the space's read, so the browser's own jump found nothing. 2026-10-29, #PRNUM.
- **A page may set a notice above a section of the editable editor** (`noticeFor`, by fact group), such as `data-reports`' report notice. *Why:* the editor knows its sections, the page what stands above them; no feature imports another. 2026-10-29, #PRNUM.
"""
s = s[:i] + block + '\n' + s[j:]
open(S, 'w', encoding='utf8', newline='').write(s)
append_history(S, '### Web history', "- #PRNUM — the editor lands on the section its hash names once drawn (finding 184), and a page's notice above a section (`noticeFor`).")

f = glob.glob('docs/architecture/findings/184-*.md')[0]
s = open(f, encoding='utf8', newline='').read()
s = s.replace('**Status:** Open · **Date:** 2026-10-28', '**Status:** Resolved · **Date:** 2026-10-28 · **Resolved:** 2026-10-29', 1)
s = s.rstrip('\n') + "\n\n**Resolution (#PRNUM):** The editor scrolls to and focuses the card its address's hash names once its cards have drawn (`useHashLanding`, run when the read has answered; the cards' headings `tabIndex={-1}`) (D6.8); «تعديل الحقل» lands on its section with the report's notice above it.\n"
open(f, 'w', encoding='utf8', newline='').write(s)
print('ok')
