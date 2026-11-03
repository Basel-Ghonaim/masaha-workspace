p = r'C:\dev\masaha\app-lane-a1\apps\api\src\modules\space-links\staff\staff.api.test.ts'
s = open(p, encoding='utf8').read()
old = """  it('re-activating restores the link, ends nothing, and the same state writes nothing', async () => {"""
new = """  it('deactivating a link of a person with another active link keeps their sessions', async () => {
    const nour = await signedInReceptionist();
    // An owner elsewhere, who is this space's reception too.
    await prisma.spaceManager.create({
      data: { spaceId: otherSpaceId, userId: nour.id, role: 'OWNER' },
    });
    const { sessionVersion } = await prisma.user.findUniqueOrThrow({ where: { id: nour.id } });

    const response = await staff(owner, 'patch', `/${String(nour.id)}`, { isActive: false });

    expect(response.status).toBe(200);
    expect(dataOf(response)).toMatchObject({ isActive: false });
    // This space is closed to them at once: the boundary reads the links on every request.
    expect((await readSpace(nour)).status).toBe(404);
    expect((await refresh(nour.refreshToken)).status).toBe(200);
    expect(await prisma.user.findUniqueOrThrow({ where: { id: nour.id } })).toMatchObject({
      sessionVersion,
    });
  });

""" + old
assert s.count(old) == 1
s = s.replace(old, new)
open(p, 'w', encoding='utf8', newline='').write(s)
