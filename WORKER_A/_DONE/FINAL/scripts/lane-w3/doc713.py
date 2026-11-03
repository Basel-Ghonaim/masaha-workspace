p=r'C:\dev\masaha\app-lane-w3\docs\features\desk.md'
s=open(p,encoding='utf8').read()
i=s.index("- **The subscription sheet** (screen 16, K3)")
j=s.index("\n",i)
add=(" Its «من» and «إلى» are the layer's date pickers, «إلى» clearable («بلا تاريخ نهاية»); a package's end is said as text, never a field. A custom end is said by the limits set: no end and no total — «بلا تاريخ نهاية · يبقى نشطًا حتى يُنهى»; a total and no end — «… ينتهي عند استهلاك {limit}»; an end and a total — «ينتهي في {date} أو عند استهلاك {limit}، أيهما أسبق», the limit counted in days, else hours. An earlier debt is a warning; the money block then lists each earlier item and the new subscription («الاشتراك: …» or «التجديد: …»), its due «المجموع». A usage-based custom rate starts from the published hour or day price for whom and the shift («من السعر المنشور»), and the terms say «يُحسب من الحضور: {rate} للساعة» (or «لليوم»). The desk's packages are headed «خاصة بالمكتب — لا تظهر للزوار», each with a «خاصة» badge.")
s=s[:j]+add+s[j:]
a="a usage-based subscriber's due said after the check-out."
assert s.count(a)==1
s=s.replace(a,a[:-1]+"; the subscription sheet's date pickers, end note, earlier-debt warning and total, published rate and private packages.")
open(p,'w',encoding='utf8',newline='').write(s)
