import os
os.chdir(r'C:\dev\masaha\app-lane-w2\docs')
def edit(p,pairs):
    s=open(p,encoding='utf8').read()
    for a,b in pairs:
        assert s.count(a)==1,(p,a[:60]); s=s.replace(a,b)
    open(p,'w',encoding='utf8',newline='').write(s)
edit('features/space-links.md',[
("the sheet reads the email's account from the users list (`GET /admin/users?q=`)","the sheet reads the email's account from the users list by its exact email (`GET /admin/users?email=`, D6.5, 2026-10-29, #PRNUM)"),
("Only an account with exactly this email counts: with none (the search also finds longer emails that hold it), or a failed read, no upgrade is offered, the sheet says to check the email, and nothing can be sent until the email changes.",
 "With no account of exactly this email, no upgrade is offered and the sheet says so («لا حساب بهذا البريد تمامًا الآن، فلا يُرقّى أحد — تحقّق منه.»); a failed read is said apart, «تعذّر التحقق من هذا البريد الآن.», with «إعادة المحاولة» ([finding 89](../architecture/findings/89-check-the-email-stands-for-three-causes.md)); either way nothing can be sent until the email changes or the read finds the account."),
("- [89](../architecture/findings/89-check-the-email-stands-for-three-causes.md): «تحقّق من البريد» stands for three causes, a right email among them.\n",""),
])
p='features/space-links.md'
s=open(p,encoding='utf8').read().rstrip('\n')+"\n- #PRNUM — the add sheet reads the email's account by its exact email; a failed read is worded apart, with a retry (finding 89).\n"
open(p,'w',encoding='utf8',newline='').write(s)
p='architecture/findings/89-check-the-email-stands-for-three-causes.md'
s=open(p,encoding='utf8').read()
s=s.replace("**Status:** Open · **Date:** 2026-10-18","**Status:** Resolved · **Date:** 2026-10-18 · **Resolved:** 2026-10-29")
s=s.rstrip('\n')+"\n\n**Resolution (#PRNUM):** The add sheet reads the account by its exact email; a failed read is worded apart, with a retry (D1.8, D6.5): `GET /admin/users?email=` finds a right email on any page; none found reads «لا حساب بهذا البريد تمامًا الآن…», a failed read «تعذّر التحقق من هذا البريد الآن.» with «إعادة المحاولة».\n"
open(p,'w',encoding='utf8',newline='').write(s)
