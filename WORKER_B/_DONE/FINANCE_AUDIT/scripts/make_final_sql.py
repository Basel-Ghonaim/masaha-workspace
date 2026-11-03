import io
import os

os.chdir(r'C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT\scripts')
BS = chr(92)
s = io.open('audit-year.sql', encoding='utf-8').read()
j = io.open('audit-year-joins.sql', encoding='utf-8').read()
names = ('tj', 'qj', 'qja', 'cj')
extra = '\n'.join(l for l in j.splitlines() if any(l.startswith(BS + 'set ' + n + ' ') for n in names))
marker = BS + "echo '### O1"
head, rest = s.split(marker, 1)
rest = marker + rest
for a, b in [(':target_join', ':tj'), (':cols', ':cj'), (':qa;', ':qja;'), (':q;', ':qj;'),
             (':qa ', ':qja '), (':q ', ':qj ')]:
    rest = rest.replace(a, b)
io.open('audit-year-final.sql', 'w', encoding='utf-8', newline='\n').write(head + extra + '\n' + rest)
print(len(extra.splitlines()), 'sets added')
