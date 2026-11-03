import sys

p = sys.argv[1]
s = open(p, encoding='utf8').read()
s = s.replace(chr(8), chr(92) + 'b').replace(chr(7), chr(92) + 'a')
open(p, 'w', encoding='utf8', newline='').write(s)
print(sum(1 for c in s if ord(c) < 9))
