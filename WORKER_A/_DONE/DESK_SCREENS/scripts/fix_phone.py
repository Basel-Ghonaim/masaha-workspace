import sys
b=chr(92)
p=sys.argv[1]
s=open(p,encoding="utf-8",newline="").read()
old=b+"2066+970 59 000 00002069"
new=b+"u2066+970 59 000 0000"+b+"u2069"
assert s.count(old)==1
s=s.replace(old,new)
open(p,"w",encoding="utf-8",newline="").write(s)
