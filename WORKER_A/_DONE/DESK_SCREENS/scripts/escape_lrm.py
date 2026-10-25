import sys
p=sys.argv[1]
s=open(p,encoding="utf-8",newline="").read()
s=s.replace(chr(0x200e), chr(92)+"u200e")
open(p,"w",encoding="utf-8",newline="").write(s)
