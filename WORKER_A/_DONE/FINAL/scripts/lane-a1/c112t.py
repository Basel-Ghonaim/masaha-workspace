p = r'C:\dev\masaha\app-lane-a1\apps\api\src\modules\space-links\staff\staff.api.test.ts'
s = open(p, encoding='utf8').read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (old, s.count(old))
    s = s.replace(old, new)
rep("""          isActive: true,
          temporaryPassword: { expiresAt: '2026-10-25T10:00:00.000Z' },
        },""", """          isActive: true,
          addedAt: expect.any(String) as unknown,
          temporaryPassword: { expiresAt: '2026-10-25T10:00:00.000Z' },
        },""")
rep("""          isActive: true,
          temporaryPassword: null,
        },""", """          isActive: true,
          addedAt: expect.any(String) as unknown,
          temporaryPassword: null,
        },""")
rep("""          isActive: false,
          temporaryPassword: null,
        },""", """          isActive: false,
          addedAt: expect.any(String) as unknown,
          temporaryPassword: null,
        },""")
rep("""      isActive: false,
      temporaryPassword: null,
    });""", """      isActive: false,
      addedAt: expect.any(String) as unknown,
      temporaryPassword: null,
    });""")
rep("""/** A receptionist of the space who signs in with a password: their access token and refresh cookie. */""",
"""describe('the date of a reception link', () => {
  it('a staff member is answered with the date their link was made', async () => {
    await prisma.spaceManager.update({
      where: { spaceId_userId: { spaceId, userId: reception.id } },
      data: {
        createdAt: new Date('2026-09-14T08:30:00.000Z'),
        updatedAt: new Date('2026-10-20T12:00:00.000Z'),
      },
    });

    const listed = await staff(owner, 'get');
    const changed = await staff(owner, 'patch', `/${String(reception.id)}`, { isActive: false });

    expect(dataOf(listed)).toEqual([
      expect.objectContaining({ userId: reception.id, addedAt: '2026-09-14T08:30:00.000Z' }),
    ]);
    expect(dataOf(changed)).toMatchObject({ addedAt: '2026-09-14T08:30:00.000Z' });
  });
});

/** A receptionist of the space who signs in with a password: their access token and refresh cookie. */""")
open(p, 'w', encoding='utf8', newline='').write(s)
