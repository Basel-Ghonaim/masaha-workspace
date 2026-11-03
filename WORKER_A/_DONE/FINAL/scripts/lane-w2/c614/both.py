import sys, re
# Keeps both sides of every conflict in the files given: HEAD's lines, then ours.
for p in sys.argv[1:]:
    s = open(p, encoding='utf8', newline='').read()
    pat = re.compile(r'<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n', re.S)
    n = len(pat.findall(s))
    s = pat.sub(lambda m: m.group(1) + m.group(2), s)
    open(p, 'w', encoding='utf8', newline='').write(s)
    print(p, n, 'conflicts kept both')
