p = r'C:\dev\masaha\app-lane-a1\apps\api\src\modules\auth\auth.api.test.ts'
s = open(p, encoding='utf8').read()
old = """  it('ends only that session when a token is reused after the grace window', async () => {"""
new = """  it('a token presented twice within the grace gets one successor, the same token', async () => {
    await createAccount();
    const token = refreshTokenOf(await login());

    const first = await refresh(token);
    const second = await refresh(token);

    expect(first.status).toBe(200);
    expect(second.status).toBe(200);
    expect(refreshTokenOf(second)).toBe(refreshTokenOf(first));
    expect(await prisma.refreshToken.count({ where: { familyId: await familyOf(token) } })).toBe(
      2,
    );
  });

""" + old
assert s.count(old) == 1
s = s.replace(old, new)
open(p, 'w', encoding='utf8', newline='').write(s)
