p = 'C:/dev/masaha/app/apps/web/src/shared/copy/arabic/desk.ts'
s = open(p, encoding='utf-8').read()
BS = chr(92)
old = ' 2066+970 59 000 00002069`'
new = ' ' + BS + 'u2066+970 59 000 0000' + BS + 'u2069`'
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new)
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
