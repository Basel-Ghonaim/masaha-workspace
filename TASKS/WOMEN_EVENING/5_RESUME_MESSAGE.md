# WOMEN_EVENING — the message to paste when resuming the worker (written 2026-11-14)

Resume the worker's own conversation from `C:\dev\masaha\app`:

    claude --resume 0eeaa45f-873d-4ef9-977c-77d839495d90 --model claude-opus-5-5 --effort high --add-dir 'C:\dev\masaha\workspace' --strict-mcp-config --no-chrome --settings 'C:\dev\masaha\workspace\_SHARED\worker-settings.json'

Before it: Docker Desktop running and `masaha-postgres-1` up; no stale `heavy-slot-*` in
`TASKS\IDENTITY\scripts\`. Then paste:

```
Supervisor's message (relayed by the owner). Docker and the database are up; masaha_we_* are intact; no grant slot is held.
1. Finish the current phase: retake shot 04, then complete 4_REPORT.md (the verification you ran on 11-13: build, test:unit, test:component in two shards with the load timeouts that passed alone, test:api 1,446, the real run).
2. The identity PR #144 has merged (main = 88c5eb3f), so the no-conflict rule is over. Rebase feat/women-evening on origin/main (a backup/* first). Make the first commit on the rebased branch the carried review fixes: C:\dev\masaha\workspace\TASKS\WOMEN_EVENING\0_CARRIED_FROM_144.md (read it whole; tests seen failing first). Then build the items "Waiting for the identity merge" from your report: the card's two marks, VenusIcon in the layer's index and the showcase, foundation if needed.
3. Re-run the complete verification through the grant script, then add a "Phase 2" section to 4_REPORT.md with the new head (full sha).
Still no push and no PR: the owner gives that word after the report.
```
