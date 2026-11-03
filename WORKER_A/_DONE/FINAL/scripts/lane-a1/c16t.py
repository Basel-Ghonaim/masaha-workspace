p = r'C:\dev\masaha\app-lane-a1\apps\api\src\modules\users\me.api.test.ts'
s = open(p, encoding='utf8').read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (old, s.count(old))
    s = s.replace(old, new)
rep("""        language: 'ar',
        role: 'USER',
      });
    }""", """        language: 'ar',
        role: 'USER',
        hasPassword: true,
        hasGoogle: false,
      });
    }""")
rep("""      language: 'en',
      role: 'OWNER',
    });
  });
});""", """      language: 'en',
      role: 'OWNER',
      hasPassword: true,
      hasGoogle: false,
    });
  });

  it('GET /me answers hasPassword and hasGoogle', async () => {
    const sara = await signIn('USER');
    const read = async () =>
      dataOf(await readMe(sara.authorization)) as { hasPassword: boolean; hasGoogle: boolean };

    await prisma.user.update({
      where: { id: sara.id },
      data: { googleSubject: 'google-sara', passwordHash: null },
    });
    expect(await read()).toMatchObject({ hasPassword: false, hasGoogle: true });

    await prisma.user.update({ where: { id: sara.id }, data: { passwordHash: 'x' } });
    expect(await read()).toMatchObject({ hasPassword: true, hasGoogle: true });
  });
});""")
rep("""      name: 'سارة أحمد',
      email: 'user@example.com',
      language: 'ar',
      role: 'USER',
    });""", """      name: 'سارة أحمد',
      email: 'user@example.com',
      language: 'ar',
      role: 'USER',
      hasPassword: true,
      hasGoogle: false,
    });""")
open(p, 'w', encoding='utf8', newline='').write(s)
