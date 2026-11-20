# WOMEN_EVENING — #145's fix round (the message to paste to the worker)

The owner's word (2026-11-14): fix F1, F3, F4, F5 and N1 of `7_REVIEW.md` before the merge; F2 → finding 227 and a
rollback step in the PR; **run only the tests the round touches** — CI judges the rest.

Paste into the worker's open conversation (in `C:\dev\masaha\app`). If it was closed, resume it first:

```
claude --resume 0eeaa45f-873d-4ef9-977c-77d839495d90 --model claude-opus-5-5 --effort high --add-dir 'C:\dev\masaha\workspace' --strict-mcp-config --no-chrome --settings 'C:\dev\masaha\workspace\_SHARED\worker-settings.json'
```

```
Supervisor's message (relayed by the owner). #145's review is done: C:\dev\masaha\workspace\TASKS\WOMEN_EVENING\7_REVIEW.md — read it whole. The supervisor verified every finding in the code. The owner's word: a fix round now, then the merge.

Start: a backup/women-evening-pre-fix at 8f511d5a. Each fix folds into the commit named (--fixup + autosquash); no fix commits.

1. F1 → fold into e1beddc1: remove `IF NOT EXISTS` from the migration's ALTER TABLE, and its comment line. The migration test runs only the file's data steps (the UPDATE and the INSERT, exactly as written), the ALTER TABLE filtered out; its header says so. The lane's migrate deploy proves the DDL. If a local database (masaha_we_dev / masaha_we_test) then refuses the edited migration, never reset it: say so and ask the owner.
2. F2 → fold into e1beddc1: record finding 227 (check the index's next free number): the web crashes on an icon key it does not know (GlyphIcon / AmenityIcon), so a migration adding an icon key breaks the code before it; a fallback like iconOf's would make the next key safe. No code change. In the PR description's migration section, a rollback step: before a Vercel rollback past #145, `UPDATE amenities SET icon = 'users' WHERE key = 'womens_hall'`; restore 'venus' once the new code is back.
3. F3 → fold into 8501d64e: split each `not.toHaveClass('bg-secondary', 'hover:bg-hover')` in AccountLayout, SpaceEditor and LocationStatus into two assertions.
4. F4 → fold into 07691835: in apps/api/src/modules/directory/favorites.api.test.ts, a favourite linked to an active womens_hall (not the first amenity id) reads womensHall: true, and one without it reads false.
5. F5 → fold into 2c73d610: one component case — the admin's page of a verified space, the switch on and every day closing by 18:00, shows «دوام مسائي» and no hint.
6. N1 → fold into fae90db1: the public page's evening line rendered in English too, with axe on the hours section.

Each new or changed assertion: make its break once and watch it fail (F3: `variant="ghost"` / `'outline'` as 7_REVIEW.md says; F4: drop womensHallId; F5: drop `host.editable &&`), then restore.

Checks — the owner's word for this round: run ONLY the test files you touched (each alone, through the grant script; a run killed for memory: retry once, then CI judges). No full lanes, no lint, typecheck or check:* locally; Prettier on the touched files. Say this exception in the PR's Evidence and in the report.

Then push (--force-with-lease, your branch only), update the PR description: a "Review fixes (#145's review)" section listing F1, F3, F4, F5, N1 with their commits, F2 → finding 227 with the rollback step. Wait for CI green on the new head and CLEAN, add a "Fix round" section to 4_REPORT.md with the full head sha, and stop. Never merge.
```
