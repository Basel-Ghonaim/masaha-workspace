p='docs/architecture/data-model.md'
s=open(p,encoding='utf8',newline='').read()
a="computed by one database function, `subscription_usage`, which every read uses (2026-10-21, #102)."
b=a+" The function answers the due as a `bigint`, so a usage-based subscription with no end never overflows it; the API maps it to a number, exact within the price's bound (10,000,000 agorot), as it does the sums of debt and credit (2026-10-29, #PRNUM)."
assert s.count(a)==1; s=s.replace(a,b)
open(p,'w',encoding='utf8',newline='').write(s)
