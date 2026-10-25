import sys
s=open(sys.argv[1],encoding='utf-8').read(); i=s.find(sys.argv[2]); print(ascii(s[i:i+int(sys.argv[3])]))
