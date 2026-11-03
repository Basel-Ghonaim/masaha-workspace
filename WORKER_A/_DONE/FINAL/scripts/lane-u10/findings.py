import glob, re, sys
base = r'C:\dev\masaha\app-lane-u10\docs\architecture\findings'
accepted = {
 22: "(OD1) The reset email's words stay in `resetEmail.copy.ts`, held to one shape in both languages by its test; `localisation.md` names this second home.",
 84: "v1 needs no linking of an existing account to a second front desk (close to in-app claiming, *Not in v1*).",
 112: "(OD2) The web holds one key per intent and never reuses one across two visits, so the case does not arise from the desk; the rule stays.",
 115: "(OD3) The desk never retries the write-off or its undo by itself (test 41 of #117, and D7.2's undo), the condition the owner set.",
 187: "No undo after «إزالة» of a space that left the directory (the owner's DI-58 (a), 2026-10-28).",
 193: "Finance's «غير محصّلة» stays the desk's list (equal to what the overview's tile links to); owed and uncollected are never added.",
}
f1 = [23, 33, 46, 64, 65, 152]
def path(n):
    m = glob.glob(base + '\%d-*.md' % n)
    assert len(m) == 1, n
    return m[0]
for n, line in accepted.items():
    p = path(n)
    s = open(p, encoding='utf8', newline='').read()
    m = re.search(r'^\*\*Status:\*\* Open( · \*\*Date:\*\* \d{4}-\d{2}-\d{2})\n', s, re.M)
    assert m, n
    s = s[:m.start()] + '**Status:** Accepted' + m.group(1) + ' · **Accepted:** 2026-10-29\n' + s[m.end():]
    s = s.rstrip('\n') + '\n\n**Accepted (the owner, 2026-10-29, #PRNUM):** ' + line + '\n'
    open(p, 'w', encoding='utf8', newline='').write(s)
for n in f1:
    p = path(n)
    s = open(p, encoding='utf8', newline='').read()
    assert '**Status:** Open' in s, n
    s = s.rstrip('\n') + '\n\n**To the deployment item** (the owner\'s F1, 2026-10-29).\n'
    open(p, 'w', encoding='utf8', newline='').write(s)
print('ok')
