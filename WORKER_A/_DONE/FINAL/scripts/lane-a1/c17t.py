p = r'C:\dev\masaha\app-lane-a1\apps\api\src\modules\space-links\admin-owners\adminOwners.api.test.ts'
s = open(p, encoding='utf8').read()
old = """  it('asks for the upgrade of the space’s reception before it refuses the link', async () => {"""
new = """  it('ALREADY_OWNER carries the owner’s id', async () => {
    const owner = await prisma.user.create({
      data: { email: 'nour@example.com', name: 'Nour', passwordHash: 'x', role: 'OWNER' },
    });

    const response = await add({ ...NEW, upgradeExisting: true });

    expect(response.status).toBe(409);
    expect(errorOf(response)).toMatchObject({
      code: 'ALREADY_OWNER',
      details: { userId: owner.id },
    });
  });

""" + old
assert s.count(old) == 1
s = s.replace(old, new)
open(p, 'w', encoding='utf8', newline='').write(s)
