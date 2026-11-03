import io
import os
import re

# C1's version of audit.repository.ts: the lateral replaced by the target's joins, as the head has them.
os.chdir(r'C:\dev\masaha\app-b\apps\api\src\modules\audit')
p = 'audit.repository.ts'
s = io.open(p, encoding='utf-8', newline='').read()

start = s.index('/**\n * The target\'s current name, by its type')
end = s.index('/** The owner\'s actor filter')
final = io.open(r'C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT\scripts\final-audit.repository.ts',
                encoding='utf-8', newline='').read()
f_start = final.index('/**\n * The target, joined by its type')
f_end = final.index('/**\n * `q` against the target')
block = final[f_start:f_end]
block += '''/** `q` against the target's names, as the directory searches (`masaha_search_text`). */
const matches = (q: string) =>
  Prisma.sql`strpos(masaha_search_text(concat_ws(' ', ${TARGET_NAME}, ${TARGET_NAME_AR})),
    masaha_search_text(${q})) > 0`;

'''
s = s[:start] + block + s[end:]
reps = [
('''            t.name AS target_name, t.name_ar AS target_name_ar, t.deleted AS target_deleted''',
 '''            ${TARGET_NAME} AS target_name, ${TARGET_NAME_AR} AS target_name_ar,
            ${TARGET_DELETED} AS target_deleted'''),
('''            target_deleted: boolean | null;''', '''            target_deleted: boolean;'''),
('''          targetDeleted: row.target_deleted ?? false,''', '''          targetDeleted: row.target_deleted,'''),
]
for a, b in reps:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
s = re.sub(r'\bTARGET_JOIN\b', 'TARGET_JOINS', s)
assert 't.name' not in s and 't.deleted' not in s
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
