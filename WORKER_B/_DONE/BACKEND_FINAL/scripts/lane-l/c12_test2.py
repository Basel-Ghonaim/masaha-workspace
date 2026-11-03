p = r"C:\dev\masaha\app-b-lane-l\apps\api\src\modules\auth\idle.api.test.ts"
s = open(p, encoding="utf-8", newline="").read()
old = """    const later = at(20 * MINUTE);
    expect((await me(desk, later)).status).toBe(200);
    const rotated = await refresh({ ...desk, refreshToken: nextToken }, later);
    expect(rotated.status).toBe(200);
    const newest = await prisma.refreshToken.findFirstOrThrow({
      where: { familyId: desk.sessionId },
      orderBy: { id: 'desc' },
      select: { lastActivityAt: true },
    });
    expect(newest.lastActivityAt.toISOString()).toBe(later.toISOString());
"""
new = """    // Twenty minutes in: ten since the renewal, so neither the refresh nor a request is idle, and
    // the refresh copies the renewal into the token it issues.
    const later = at(20 * MINUTE);
    expect((await refresh({ ...desk, refreshToken: nextToken }, later)).status).toBe(200);
    const newest = await prisma.refreshToken.findFirstOrThrow({
      where: { familyId: desk.sessionId },
      orderBy: { id: 'desc' },
      select: { lastActivityAt: true },
    });
    expect(newest.lastActivityAt.toISOString()).toBe(used.toISOString());
    expect((await me(desk, later)).status).toBe(200);
"""
assert s.count(old) == 1
s = s.replace(old, new, 1)
open(p, "w", encoding="utf-8", newline="").write(s)
