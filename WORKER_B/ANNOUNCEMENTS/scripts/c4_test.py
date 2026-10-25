p = 'C:/dev/masaha/app-b/apps/api/src/modules/directory/page.api.test.ts'
s = open(p, encoding='utf-8', newline='').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)


rep("import request from 'supertest';", "import { randomUUID } from 'node:crypto';\n\nimport request from 'supertest';")
rep("""          { card: photoUrl('second', 'card'), page: photoUrl('second', 'page') },
        ],
      },
    });""", """          { card: photoUrl('second', 'card'), page: photoUrl('second', 'page') },
        ],
        announcements: [],
      },
    });""")
rep("""  it.each([
    ['an unknown slug', 'nowhere'],""", """  it('the page carries the running and upcoming announcements by start then id, each with its start and end; never an ended or deleted one', async () => {
    const space = await createPublicSpace(areaId, 'Announcing');
    const other = await createPublicSpace(areaId, 'Elsewhere');
    const post = (data: object) =>
      prisma.announcement.create({
        data: {
          spaceId: space.id,
          type: 'GENERAL',
          textAr: 'إعلان',
          startsAt: daysAgo(1),
          idempotencyKey: randomUUID(),
          ...data,
        },
      });
    const upcoming = await post({ type: 'EVENT', startsAt: daysAgo(-2), textEn: 'A talk' });
    const runningB = await post({ type: 'CLOSURE', endsAt: daysAgo(-1) });
    const runningA = await post({ type: 'OFFER', startsAt: daysAgo(3) });
    const runningC = await post({});
    // Never shown: ended (its end now), deleted, and another space's.
    await post({ startsAt: daysAgo(2), endsAt: NOW });
    await post({ deletedAt: daysAgo(0.5) });
    await post({ spaceId: other.id });

    const response = await page('announcing');

    expect(response.status).toBe(200);
    expect((response.body as { data: { announcements: unknown } }).data.announcements).toEqual([
      {
        id: runningA.id,
        type: 'OFFER',
        textAr: 'إعلان',
        textEn: null,
        startsAt: daysAgo(3).toISOString(),
        endsAt: null,
      },
      {
        id: runningB.id,
        type: 'CLOSURE',
        textAr: 'إعلان',
        textEn: null,
        startsAt: daysAgo(1).toISOString(),
        endsAt: daysAgo(-1).toISOString(),
      },
      expect.objectContaining({ id: runningC.id }) as unknown,
      {
        id: upcoming.id,
        type: 'EVENT',
        textAr: 'إعلان',
        textEn: 'A talk',
        startsAt: daysAgo(-2).toISOString(),
        endsAt: null,
      },
    ]);
  });

  it('at most 20', async () => {
    const space = await createPublicSpace(areaId, 'Busy');
    await prisma.announcement.createMany({
      data: Array.from({ length: 21 }, (_, i) => ({
        spaceId: space.id,
        type: 'EVENT' as const,
        textAr: `فعالية ${String(i + 1)}`,
        startsAt: daysAgo(-(i + 1)),
        idempotencyKey: randomUUID(),
      })),
    });

    const response = await page('busy');

    const { announcements } = (response.body as { data: { announcements: { textAr: string }[] } })
      .data;
    expect(announcements).toHaveLength(20);
    expect(announcements.at(-1)?.textAr).toBe('فعالية 20');
  });

  it.each([
    ['an unknown slug', 'nowhere'],""")
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
