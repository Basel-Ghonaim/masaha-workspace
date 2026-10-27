import io
import os

os.chdir(r'C:\dev\masaha\app-b\apps\api\src\modules\subscriptions\closures')


def edit(path, reps):
    s = io.open(path, encoding='utf-8', newline='').read()
    for a, b in reps:
        assert s.count(a) == 1, (path, a[:80])
        s = s.replace(a, b)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)


edit('closures.repository.ts', [
('''    AND ("starts_on" IS NULL OR "starts_on" <= ${lastDay}::date)`;
}
''', '''    AND ("starts_on" IS NULL OR "starts_on" <= ${lastDay}::date)`;
}

/**
 * The subscriptions an extension moves (finding 151): those the closure covered, and the chain of
 * renewals of each that has not started by `today` (a Gaza date) and was not ended early — the
 * renewal of a renewal too. A renewal started, or with no start, runs on its own days: the covered
 * rule judges it. It names `covered` and `chain` for the statement that follows.
 */
function moved(spaceId: number, span: ClosureSpan, today: string): Prisma.Sql {
  const pending = Prisma.sql`s."space_id" = ${spaceId} AND s."ended_at" IS NULL
    AND s."starts_on" IS NOT NULL AND s."starts_on" > ${today}::date`;
  return Prisma.sql`WITH RECURSIVE covered AS (
      SELECT "id" FROM "subscriptions" WHERE ${covered(spaceId, span)}
    ), chain AS (
      SELECT s."id" FROM "subscriptions" s JOIN covered c ON s."renewal_of_id" = c."id"
      WHERE ${pending}
      UNION
      SELECT s."id" FROM "subscriptions" s JOIN chain c ON s."renewal_of_id" = c."id"
      WHERE ${pending}
    )`;
}
'''),
('''    /** How many of the space's subscriptions the closure's span covered: one query. */
    async coveredCount(spaceId: number, span: ClosureSpan): Promise<number> {
      const [row] = await prisma.$queryRaw<{ count: number }[]>`
        SELECT count(*)::integer AS count FROM "subscriptions" WHERE ${covered(spaceId, span)}`;
      return row?.count ?? 0;
    },

    /** Locks the subscriptions the closure's span covered (`FOR UPDATE`, by id) and answers them. */
    async lockCovered(spaceId: number, span: ClosureSpan, tx: Tx): Promise<number[]> {
      const rows = await tx.$queryRaw<{ id: number }[]>`
        SELECT "id" FROM "subscriptions" WHERE ${covered(spaceId, span)} ORDER BY "id" FOR UPDATE`;
      return rows.map(({ id }) => id);
    },
''', '''    /** How many subscriptions an extension at `today` would move, the renewals included: one query. */
    async movedCount(spaceId: number, span: ClosureSpan, today: string): Promise<number> {
      const [row] = await prisma.$queryRaw<{ count: number }[]>`
        ${moved(spaceId, span, today)}
        SELECT ((SELECT count(*) FROM covered)
          + (SELECT count(*) FROM chain WHERE "id" NOT IN (SELECT "id" FROM covered)))::integer AS count`;
      return row?.count ?? 0;
    },

    /**
     * Locks the subscriptions an extension at `today` moves (`FOR UPDATE`, by id: the renewals with
     * the covered ones, in one statement) and answers them, the covered apart from the renewals.
     */
    async lockMoved(
      spaceId: number,
      span: ClosureSpan,
      today: string,
      tx: Tx,
    ): Promise<{ covered: number[]; renewals: number[] }> {
      const rows = await tx.$queryRaw<{ id: number; renewal: boolean }[]>`
        ${moved(spaceId, span, today)}
        SELECT "id", ("id" IN (SELECT "id" FROM chain) AND "id" NOT IN (SELECT "id" FROM covered)) AS "renewal"
        FROM "subscriptions"
        WHERE "id" IN (SELECT "id" FROM covered UNION SELECT "id" FROM chain)
        ORDER BY "id" FOR UPDATE`;
      return {
        covered: rows.filter(({ renewal }) => !renewal).map(({ id }) => id),
        renewals: rows.filter(({ renewal }) => renewal).map(({ id }) => id),
      };
    },
'''),
('''        WHERE "id" = ANY(${[...ids]}::integer[])`;
    },

    /** The extension this key applied''', '''        WHERE "id" = ANY(${[...ids]}::integer[])`;
    },

    /** Moves these renewals' starts and ends by `days` (an end of `NULL` stays): one statement. */
    async moveRenewals(ids: readonly number[], days: number, at: Date, tx: Tx): Promise<void> {
      if (ids.length === 0) return;
      await tx.$executeRaw`
        UPDATE "subscriptions" SET "starts_on" = "starts_on" + ${days}::integer,
          "ends_on" = "ends_on" + ${days}::integer, "updated_at" = ${at}
        WHERE "id" = ANY(${[...ids]}::integer[])`;
    },

    /** The extension this key applied'''),
('''    /** Records the extension and links it to each subscription it moved: two statements. */''',
 '''    /** Records the extension and links it to each subscription it moved: two statements. */'''),
])

edit('closures.service.ts', [
('''import {
  EXTENSION_MAX_DAYS,''', '''import {
  EXTENSION_MAX_DAYS,'''),
('''} from '@masaha/shared/announcements';
''', '''} from '@masaha/shared/announcements';
import { gazaClockOf } from '@masaha/shared/core';
'''),
('''   * moved; one not started yet → `ANNOUNCEMENT_NOT_STARTED`; else the Gaza days it covered to now,
   * the days proposed (at most `EXTENSION_MAX_DAYS`) and how many subscriptions it covered.''',
 '''   * moved; one not started yet → `ANNOUNCEMENT_NOT_STARTED`; else the Gaza days it covered to now,
   * the days proposed (at most `EXTENSION_MAX_DAYS`) and how many subscriptions it would move: those
   * it covered and their renewals not started (finding 151).'''),
('''        const count = await repository.coveredCount(spaceId, span);''',
 '''        const count = await repository.movedCount(spaceId, span, gazaClockOf(at).date);'''),
('''   * `ANNOUNCEMENT_NOT_STARTED`; its span at now; the covered subscriptions locked, their ends moved
   * in one statement; the extension and its links; its audit entry.''',
 '''   * `ANNOUNCEMENT_NOT_STARTED`; its span at now; the covered subscriptions and their renewals not
   * started by today locked in one statement, the covered ones' ends moved, the renewals' starts and
   * ends (finding 151); the extension and its links to both; its audit entry.'''),
('''        const ids = await repository.lockCovered(space.id, closureSpan(closure, at), tx);
        await repository.moveEnds(ids, days, at, tx);
        await repository.createExtension(
          { announcementId, days, appliedById: actor.id, key, appliedAt: at },
          ids,
          tx,
        );''', '''        const { covered, renewals } = await repository.lockMoved(
          space.id,
          closureSpan(closure, at),
          gazaClockOf(at).date,
          tx,
        );
        await repository.moveEnds(covered, days, at, tx);
        await repository.moveRenewals(renewals, days, at, tx);
        await repository.createExtension(
          { announcementId, days, appliedById: actor.id, key, appliedAt: at },
          [...covered, ...renewals],
          tx,
        );'''),
('''            after: { days, subscriptionIds: ids },''',
 '''            after: { days, subscriptionIds: covered, renewalIds: renewals },'''),
('''          { announcementId, days, subscriptions: ids.length, appliedAt: at, appliedById: actor.id },''',
 '''          {
            announcementId,
            days,
            subscriptions: covered.length + renewals.length,
            appliedAt: at,
            appliedById: actor.id,
          },'''),
])
print('ok')
