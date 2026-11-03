def edit(p, pairs):
    s = open(p, encoding='utf8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)
R = r'C:\dev\masaha\app-lane-a1\apps\api\src\modules'
edit(R + r'\space-links\staff\staff.api.test.ts', [
("""  it('an owner cannot deactivate a co-owner, or anyone without a reception link here', async () => {""",
"""  it('a re-activation refuses an admin: ACCOUNT_IS_ADMIN', async () => {
    await staff(owner, 'patch', `/${String(reception.id)}`, { isActive: false });
    await prisma.user.update({ where: { id: reception.id }, data: { role: 'ADMIN' } });

    const response = await staff(owner, 'patch', `/${String(reception.id)}`, { isActive: true });

    expect(response.status).toBe(409);
    expect(errorOf(response).code).toBe('ACCOUNT_IS_ADMIN');
    expect(
      await prisma.spaceManager.findUniqueOrThrow({
        where: { spaceId_userId: { spaceId, userId: reception.id } },
      }),
    ).toMatchObject({ deactivatedAt: expect.any(Date) as unknown });
  });

  it('an owner cannot deactivate a co-owner, or anyone without a reception link here', async () => {"""),
("""  it('refuses a re-issue for an account that holds anything else', async () => {""",
"""  it('the re-issue refuses an OWNER-role account with no link here: ACCOUNT_HAS_LINKS', async () => {
    const added = await addedReceptionist();
    // No other link: its role alone refuses it.
    await prisma.user.update({ where: { id: added.userId }, data: { role: 'OWNER' } });
    const before = await prisma.user.findUniqueOrThrow({ where: { id: added.userId } });

    const response = await staff(owner, 'post', `/${String(added.userId)}/temporary-password`);

    expect(response.status).toBe(409);
    expect(errorOf(response).code).toBe('ACCOUNT_HAS_LINKS');
    expect(
      (await prisma.user.findUniqueOrThrow({ where: { id: added.userId } })).passwordHash,
    ).toBe(before.passwordHash);
  });

  it('the re-issue and the handover answer 404 for a deactivated reception link', async () => {
    const added = await addedReceptionist();
    await staff(owner, 'patch', `/${String(added.userId)}`, { isActive: false });
    const before = await prisma.user.findUniqueOrThrow({ where: { id: added.userId } });
    const entries = (await auditEntries()).length;

    const reissue = await staff(owner, 'post', `/${String(added.userId)}/temporary-password`);
    const handover = await staff(
      owner,
      'post',
      `/${String(added.userId)}/temporary-password/handover`,
      { channel: 'WHATSAPP' },
    );

    expect(reissue.status).toBe(404);
    expect(handover.status).toBe(404);
    expect(
      (await prisma.user.findUniqueOrThrow({ where: { id: added.userId } })).passwordHash,
    ).toBe(before.passwordHash);
    expect(await auditEntries()).toHaveLength(entries);
  });

  it('refuses a re-issue for an account that holds anything else', async () => {"""),
])
edit(R + r'\auth\sessionLock.api.test.ts', [
("""  it('keeps a refresh waiting on a revocation from renewing the session', async () => {""",
"""  it('a temporary password that expires between the check and the lock is refused at confirm', async () => {
    const { id } = await createAccount({ mustChangePassword: true });

    // The password matched while it was live; it expires before the lock is granted.
    const response = await whileLocked(id, login, (tx) =>
      tx.user.update({
        where: { id },
        data: { temporaryPasswordExpiresAt: new Date(Date.now() - 1_000) },
      }),
    );

    expect(response.status).toBe(403);
    expect(response.body).toMatchObject({ error: { code: 'TEMPORARY_PASSWORD_EXPIRED' } });
    expect(await prisma.refreshToken.count({ where: { userId: id } })).toBe(0);
  });

  it('keeps a refresh waiting on a revocation from renewing the session', async () => {"""),
])
