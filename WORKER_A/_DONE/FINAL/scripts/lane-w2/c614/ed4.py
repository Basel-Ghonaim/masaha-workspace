import re
p = r'C:\dev\masaha\app-lane-w2\apps\web\src\features\lookups\hooks\list\useAmenityRow.component.test.tsx'
s = open(p, encoding='utf8', newline='').read()
old = "toMatch(/^تحريك لأعلى: ⁨إنترنت⁩ — \d+ من \d+$/)"
assert s.count(old) == 1
s = s.replace(old, "toBe('تحريك لأعلى: ⁨إنترنت⁩ — 1 من 3')")
open(p, 'w', encoding='utf8', newline='').write(s)
p = r'C:\dev\masaha\app-lane-w2\apps\web\src\features\lookups\hooks\list\useGovernorateCard.component.test.tsx'
s = open(p, encoding='utf8', newline='').read()
for old, new in [("toBe('تحريك لأعلى: ⁨الرمال⁩')", "toBe('تحريك لأعلى: ⁨الرمال⁩ — 1 من 3')"),
                 ("toBe('تحريك لأسفل: ⁨محافظة غزة⁩')", "toBe('تحريك لأسفل: ⁨محافظة غزة⁩ — 1 من 2')")]:
    assert s.count(old) == 1, old
    s = s.replace(old, new)
open(p, 'w', encoding='utf8', newline='').write(s)
