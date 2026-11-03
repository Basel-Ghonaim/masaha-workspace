p = r'C:\dev\masaha\app-lane-a1\apps\api\src\modules\space-links\staff\staff.api.test.ts'
s = open(p, encoding='utf8').read()
old = """  it('refuses a re-issue for an account that holds anything else', async () => {"""
new = """  it('the re-issue refuses an admin’s account with ACCOUNT_IS_ADMIN', async () => {
    const added = await addedReceptionist();
    await prisma.user.update({ where: { id: added.userId }, data: { role: 'ADMIN' } });
    const before = await prisma.user.findUniqueOrThrow({ where: { id: added.userId } });

    const response = await staff(owner, 'post', `/${String(added.userId)}/temporary-password`);

    expect(response.status).toBe(409);
    expect(errorOf(response).code).toBe('ACCOUNT_IS_ADMIN');
    expect(
      (await prisma.user.findUniqueOrThrow({ where: { id: added.userId } })).passwordHash,
    ).toBe(before.passwordHash);
  });

""" + old
assert s.count(old) == 1
s = s.replace(old, new)
open(p, 'w', encoding='utf8', newline='').write(s)
