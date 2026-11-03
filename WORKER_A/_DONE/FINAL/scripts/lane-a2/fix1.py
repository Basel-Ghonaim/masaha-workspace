import sys
for p in sys.argv[1:]:
    s=open(p,encoding='utf8',newline='').read()
    s=s.replace("checked_out_at, checkout_method)\n      SELECT","checked_out_at, checkout_method, updated_at)\n      SELECT")
    s=s.replace("+ n * interval '1 day', 'MANUAL'\n","+ n * interval '1 day', 'MANUAL', now()\n")
    open(p,'w',encoding='utf8',newline='').write(s)
