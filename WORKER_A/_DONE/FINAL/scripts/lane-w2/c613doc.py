import os
os.chdir(r'C:\dev\masaha\app-lane-w2\docs')
p='features/space-links.md'
s=open(p,encoding='utf8').read()
a="### Web decisions\n\n"
assert s.count(a)==1
s=s.replace(a,a+"""- **The owners and users lists finish their screens** (D6.11, G27.1–G27.4, G29.1): the «إجراءات» header read only by assistive technology; the owners' empty state offers «إضافة مالك»; the add sheet opens on `?sheet=add` (taken off the address once it closes), which the empty state and a space editor's «مالك جديد بلا حساب؟» use; `ACCOUNT_SUSPENDED` in the sheet reads «الحساب موقوف — استرجعه أولًا.», «استرجعه أولًا» a link to the users list searched by the email; «انضم» says its year always. 2026-10-29, #PRNUM.
""")
s=s.rstrip('\n')+"\n- #PRNUM — the owners and users lists: the actions' header read only, «إضافة مالك» on the empty owners list, the add sheet on `?sheet=add`, a suspended account led to the users list, the join date with its year.\n"
open(p,'w',encoding='utf8',newline='').write(s)
