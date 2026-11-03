def edit(p, pairs):
    s = open(p, encoding='utf8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)
M = r'C:\dev\masaha\app-lane-a1\apps\api\src\modules'
edit(M + r'\users\users.service.ts', [
("""    /** The names of these users, in one query, for a list that names them (the spaces' owners). */
    namesFor(ids: readonly number[], tx?: Tx): Promise<UserName[]> {""",
"""    /**
     * The names of these users, in one query, for a list that names them (the spaces' owners). Each
     * caller says which transaction it reads in, `undefined` for none, so a read under a lock never
     * takes the names on another connection by omission (finding 79).
     */
    namesFor(ids: readonly number[], tx: Tx | undefined): Promise<UserName[]> {"""),
])
edit(M + r'\users\users.repository.ts', [
("""    /** The names of these users, in one query. */
    findNames(ids: readonly number[], tx: Tx = db): Promise<UserName[]> {
      return tx.user.findMany({""",
"""    /** The names of these users, in one query, in the transaction named, or none (`undefined`). */
    findNames(ids: readonly number[], tx: Tx | undefined): Promise<UserName[]> {
      return (tx ?? db).user.findMany({"""),
])
edit(M + r'\data-reports\data-reports.service.ts', [("      users.namesFor(people),", "      users.namesFor(people, undefined),")])
edit(M + r'\finance\finance.service.ts', [("(await users.namesFor(collections.map(({ recordedById }) => recordedById))).map(",
 "(await users.namesFor(\n          collections.map(({ recordedById }) => recordedById),\n          undefined,\n        )).map(")])
edit(M + r'\space-links\admin-spaces\adminSpaces.service.ts', [("          : await users.namesFor([...new Set(links.map(({ userId }) => userId))]);",
 "          : await users.namesFor([...new Set(links.map(({ userId }) => userId))], undefined);")])
edit(M + r'\subscriptions\closures\closures.service.ts', [
("      const appliers = await users.namesFor([...new Set(extensions.map((row) => row.appliedById))]);",
 "      const appliers = await users.namesFor(\n        [...new Set(extensions.map((row) => row.appliedById))],\n        undefined,\n      );"),
("      const [applier] = await users.namesFor([extension.appliedById]);",
 "      const [applier] = await users.namesFor([extension.appliedById], undefined);"),
])
