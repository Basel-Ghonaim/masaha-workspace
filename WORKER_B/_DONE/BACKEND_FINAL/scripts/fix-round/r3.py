import pathlib, sys
root = pathlib.Path(r"C:\dev\masaha\app-b")
def sub(rel, old, new):
    p = root / rel
    t = p.read_bytes().decode("utf-8")
    if t.count(old) != 1:
        sys.exit(f"{rel}: {t.count(old)} matches of {old[:40]!r}")
    p.write_bytes(t.replace(old, new).encode("utf-8"))
sub("docs/features/announcements.md",
    "each once — one `DISTINCT` query on the list's own `RUNNING` condition —",
    "each once — one query of the running ones on the list's own `RUNNING` condition, each type kept once (Prisma's `distinct`, applied in memory, not in SQL) —")
sub("docs/backend/conventions.md",
    "The owner's overview will read `closures.summary`. 2026-10-24, #112.",
    "The owner's overview reads `closures.summary` (2026-10-29, #131). 2026-10-24, #112.")
sub("apps/api/src/modules/occupancy/occupancy.service.ts",
    "async glance(space: LoadedSpace, at: Date = clock()): Promise<Glance> {",
    "async glance(space: LoadedSpace, at: Date): Promise<Glance> {")
sub("apps/api/src/modules/occupancy/glance.api.test.ts",
    "const glance = await occupancy.glance(await loaded());",
    "const glance = await occupancy.glance(await loaded(), NOW);")
