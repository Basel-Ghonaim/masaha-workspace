import sys
p = sys.argv[1]
with open(p, encoding='utf-8', newline='') as f:
    s = f.read()
old = "    return SELECTED_TINT.has(utilityName(utility)) && variants.some(hoversOrHighlights);"
assert s.count(old) == 1
s = s.replace(old, "    return false && SELECTED_TINT.has(utilityName(utility)) && variants.some(hoversOrHighlights);")
with open(p, 'w', encoding='utf-8', newline='') as f:
    f.write(s)
