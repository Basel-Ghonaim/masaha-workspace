import io
import os

os.chdir(r'C:\dev\masaha\app-b\apps\api\src\modules\subscriptions\closures')


def edit(path, reps):
    s = io.open(path, encoding='utf-8', newline='').read()
    for a, b in reps:
        assert s.count(a) == 1, (path, a[:80])
        s = s.replace(a, b)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)


edit('closures.service.ts', [
('''import {
  EXTENSION_MAX_DAYS,''', '''import {
  EXTENSION_MAX_DAYS,'''),
('''} from '@masaha/shared/announcements';
''', '''} from '@masaha/shared/announcements';
import { gazaClockOf } from '@masaha/shared/core';
'''),
('''     * moved; one not started yet → `ANNOUNCEMENT_NOT_STARTED`; else the Gaza days it covered to now,
     * the days proposed (at most `EXTENSION_MAX_DAYS`) and how many subscriptions it covered.''',
 '''     * moved; one not started yet → `ANNOUNCEMENT_NOT_STARTED`; else the Gaza days it covered to now,
     * the days proposed (at most `EXTENSION_MAX_DAYS`) and how many subscriptions it would move: those
     * it covered and their renewals not started (finding 151).'''),
('''        const count = await repository.coveredCount(spaceId, span);''',
 '''        const count = await repository.movedCount(spaceId, span, gazaClockOf(at).date);'''),
('''     * `ANNOUNCEMENT_NOT_STARTED`; its span at now; the covered subscriptions locked, their ends moved
     * in one statement; the extension and its links; its audit entry.''',
 '''     * `ANNOUNCEMENT_NOT_STARTED`; its span at now; the covered subscriptions and their renewals not
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
