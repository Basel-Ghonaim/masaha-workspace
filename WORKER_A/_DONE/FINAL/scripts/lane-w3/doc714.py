p=r'C:\dev\masaha\app-lane-w3\docs\features\visits.md'
s=open(p,encoding='utf8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,a
    s=s.replace(a,b)
rep("The API is built; no web screen yet.","The API is built; on the web, the desk's screen («مكتب الاستقبال», [desk](desk.md)) checks visits in and out, collects, writes off and prices them, and lists a day's in «السجل»: the web feature `features/desk` calls these routes, since `visits` has no web feature of its own.")
rep("**Last Updated:** 2026-10-29 ·","**Last Updated:** 2026-10-29 ·")
rep("- #131 — a space's visits by the Gaza day of their check-in (`GET …/visits`).\n","- #131 — a space's visits by the Gaza day of their check-in (`GET …/visits`).\n\n### Web history\n\n- #PRNUM — the *Authority* names the desk's screen, which `features/desk` builds on these routes (G13.24).\n")
open(p,'w',encoding='utf8',newline='').write(s)
