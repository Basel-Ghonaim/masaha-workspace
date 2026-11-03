p='src/db/subscriptions.api.test.ts'
s=open(p,encoding='utf8',newline='').read()
for a,b in [("        due_agorot: 30_000,\n","        due_agorot: 30_000n,\n"),
            ("usage_based: true, due_agorot: 5_000 }","usage_based: true, due_agorot: 5_000n }"),
            ("usage_based: true, due_agorot: 500 }","usage_based: true, due_agorot: 500n }"),
            ("days_used: 0, due_agorot: 0 }","days_used: 0, due_agorot: 0n }")]:
    assert s.count(a)==1,a; s=s.replace(a,b)
open(p,'w',encoding='utf8',newline='').write(s)
