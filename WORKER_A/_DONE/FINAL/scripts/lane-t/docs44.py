root = 'C:/dev/masaha/app-lane-t/'
def rep(rel, old, new):
    p = root + rel; s = open(p, encoding='utf8').read()
    assert s.count(old) == 1, (rel, old[:60])
    open(p, 'w', encoding='utf8', newline='').write(s.replace(old, new))
S = 'docs/development/setup.md'
rep(S, "- `masaha_test` is created by [`docker/postgres/create-test-database.sql`](../../docker/postgres/create-test-database.sql) when the volume is first created.",
 "- `masaha_test` is created when the volume is first created, by an init script the Compose file holds inline (its `configs`), so the container depends on no folder (2026-10-29, #PRNUM). This needs Docker Compose 2.23.1 or later.")
rep(S, "The database container is shared by every folder: in a second folder, never run `npm run db:up` (it recreates the container bound to that folder, [finding 48](../architecture/findings/48-db-up-from-another-folder-recreates-the-shared-container.md)); run `docker start masaha-postgres-1`.",
 "The database container is shared by every folder. Every folder now gives Compose the same configuration, so a second folder's `npm run db:up` leaves the running container as it is ([finding 48](../architecture/findings/48-db-up-from-another-folder-recreates-the-shared-container.md)). **Once,** on a machine whose container was created before the init script moved inline (it binds a folder's `docker/postgres/create-test-database.sql`), the first `npm run db:up` recreates the container with the new configuration; the data stays in the volume (2026-10-29, #PRNUM).")
p = root + 'docs/architecture/findings/48-db-up-from-another-folder-recreates-the-shared-container.md'
s = open(p, encoding='utf8').read()
import re
m = re.search(r"\*\*Status:\*\* Open · \*\*Date:\*\* (\S+)", s)
s = s.replace(m.group(0), "**Status:** Resolved · **Date:** " + m.group(1), 1)
s = s.rstrip('\n') + "\n\n**Resolution (2026-10-29, #PRNUM):** the init script is an inline Compose config, so the container binds no folder and `docker compose config` gives one configuration from any folder; the existing container is recreated once, its volume kept ([setup › Running a second folder](../../development/setup.md#running-a-second-folder)).\n"
open(p, 'w', encoding='utf8', newline='').write(s)
