import sys, re
p = sys.argv[1]
with open(p, encoding='utf-8', newline='') as f:
    s = f.read()
start = s.index("const HOVER_OR_HIGHLIGHT = new Set([")
end = s.index("]);", start) + 3
s = s[:start] + "const HOVER_OR_HIGHLIGHT = new Set(['hover']);" + s[end:]
with open(p, 'w', encoding='utf-8', newline='') as f:
    f.write(s)
