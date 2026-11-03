p = r"C:\dev\masaha\app-b-lane-l\apps\api\src\modules\auth\idle.api.test.ts"
s = open(p, encoding="utf-8", newline="").read()
s = s.replace("""import request from 'supertest';
""", """import { createHash, randomBytes } from 'node:crypto';

import request from 'supertest';
""", 1)
s = s.replace("""import { createSpace } from '../../../test/factories.ts';
""", """import { createSpace } from '../../../test/factories.ts';
import { whileHeld } from '../../../test/locks.ts';
""", 1)
anchor = """  it('refuses a reception token whose session was signed out', async () => {"""
new = """  it("a request's renewal racing a rotation leaves the new session active", async () => {
    await account('nour@example.com', [['RECEPTION', spaceId]]);
    const desk = await signIn('nour@example.com');
    const nextToken = randomBytes(32).toString('base64url');
    const used = at(10 * MINUTE);

    // A refresh's transaction (finding 170): the new row inserted with the presented row's last
    // use, the presented row marked rotated, so locked. The request's renewal waits on that row,
    // cannot see the new one, and renews the presented row alone once the refresh commits.
    const renewed = await whileHeld(
      async (tx) => {
        const presented = await tx.refreshToken.findFirstOrThrow({
          where: { familyId: desk.sessionId },
        });
        const next = await tx.refreshToken.create({
          data: {
            userId: desk.userId,
            familyId: desk.sessionId,
            tokenHash: createHash('sha256').update(nextToken).digest('hex'),
            expiresAt: presented.expiresAt,
            sessionEndsAt: presented.sessionEndsAt,
            lastActivityAt: presented.lastActivityAt,
          },
        });
        await tx.refreshToken.update({
          where: { id: presented.id },
          data: { rotatedAt: used, replacedById: next.id },
        });
      },
      () => me(desk, used),
      async () => undefined,
    );
    expect(renewed.status).toBe(200);
    expect((await lastActivityOf(desk)).sort()).toEqual(
      [SIGNED_IN.toISOString(), used.toISOString()].sort(),
    );

    const later = at(20 * MINUTE);
    expect((await me(desk, later)).status).toBe(200);
    const rotated = await refresh({ ...desk, refreshToken: nextToken }, later);
    expect(rotated.status).toBe(200);
    const newest = await prisma.refreshToken.findFirstOrThrow({
      where: { familyId: desk.sessionId },
      orderBy: { id: 'desc' },
      select: { lastActivityAt: true },
    });
    expect(newest.lastActivityAt.toISOString()).toBe(later.toISOString());
  });

"""
assert s.count(anchor) == 1
s = s.replace(anchor, new + anchor, 1)
open(p, "w", encoding="utf-8", newline="").write(s)
