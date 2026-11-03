import os, re
os.chdir(r'C:\dev\masaha\app-lane-w2\docs')
p='features/space-links.md'
s=open(p,encoding='utf8').read()
a="either way nothing can be sent until the email changes or the read finds the account."
assert s.count(a)==1
s=s.replace(a,a+" An email already an owner's (`ALREADY_OWNER`, which names them in `details.userId`) reads «هذا البريد لمالك مسبقًا.» under the email, with «اربطه بالمساحة»: the owner read by that exact email, the sheet closes and the link dialog opens for them with the space the sheet chose already chosen (D6.5, [finding 83](../architecture/findings/83-already-owner-names-no-account.md), 2026-10-29, #PRNUM).")
a="- [83](../architecture/findings/83-already-owner-names-no-account.md): `ALREADY_OWNER` names no account, so the add form cannot open the link dialog for that owner.\n"
assert s.count(a)==1; s=s.replace(a,"")
s=s.rstrip('\n')+"\n- #PRNUM — `ALREADY_OWNER` in the add sheet links that owner: the link dialog opens for them and the chosen space (finding 83).\n"
open(p,'w',encoding='utf8',newline='').write(s)
p='architecture/findings/83-already-owner-names-no-account.md'
s=open(p,encoding='utf8').read()
m=re.search(r"\*\*Status:\*\* Open · \*\*Date:\*\* ([0-9-]+)", s)
s=s.replace(m.group(0), f"**Status:** Resolved · **Date:** {m.group(1)} · **Resolved:** 2026-10-29")
s=s.rstrip('\n')+"\n\n**Resolution (#PRNUM):** `ALREADY_OWNER` carries `details.userId`, and the add sheet links that owner (D0.1, D1.7, D6.5): «هذا البريد لمالك مسبقًا.» under the email, and «اربطه بالمساحة», which opens the link dialog for that owner and the chosen space.\n"
open(p,'w',encoding='utf8',newline='').write(s)
