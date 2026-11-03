p = r'C:\dev\masaha\app-lane-a1\apps\api\test\locks.ts'
s = open(p, encoding='utf8').read()
s = s.replace("import type request from 'supertest';", "import { appendFileSync } from 'node:fs';\n\nimport type request from 'supertest';\nimport { expect } from 'vitest';")
old = "    if (rows.length >= count) return rows.map(({ pid }) => pid);"
new = r"""    if (rows.length >= count) {
      const seen = await prisma.$queryRaw<unknown[]>`
        SELECT a.pid, left(a.query, 200) AS q, l.locktype, l.relation::regclass::text AS rel, l.granted
        FROM pg_stat_activity a JOIN pg_locks l ON l.pid = a.pid
        WHERE a.datname = current_database() AND a.wait_event_type = 'Lock'
          AND (NOT l.granted OR l.locktype = 'tuple')
        ORDER BY a.pid`;
      const state = expect.getState();
      appendFileSync(
        'C:/dev/masaha/workspace/WORKER_A/FINAL/scripts/lane-a1/race-map.jsonl',
        JSON.stringify({ test: `${String(state.testPath)} :: ${String(state.currentTestName)}`, on: on ?? null, count, seen }) + '\n',
      );
      return rows.map(({ pid }) => pid);
    }"""
assert s.count(old) == 1
s = s.replace(old, new)
open(p, 'w', encoding='utf8', newline='').write(s)
