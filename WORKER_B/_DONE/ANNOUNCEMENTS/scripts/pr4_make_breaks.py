import json
SVC = 'apps/api/src/modules/subscriptions/closures/closures.service.ts'
REPO = 'apps/api/src/modules/subscriptions/closures/closures.repository.ts'
EXT = 'src/modules/subscriptions/closures/extension.api.test.ts'
LOCK = "        if (!(await spaces.lock(space.id, tx))) {\n"
b = [
 dict(id='B1', file='packages/shared/src/core/gazaTime.ts', old="getTime()) / 86_400_000;", new="getTime()) / 86_400_000 + 1;", lane='shared', test='src/core/gazaTime.unit.test.ts', name='daysFrom'),
 dict(id='B2', file='apps/api/src/modules/announcements/closureSpan.ts', edits=[["gazaClockOf(startsAt).date", "startsAt.toISOString().slice(0, 10)"], ["gazaClockOf(lastInstant).date", "lastInstant.toISOString().slice(0, 10)"]], lane='unit', test='src/modules/announcements/closureSpan.unit.test.ts'),
 dict(id='B3', file='apps/api/src/modules/announcements/closureSpan.ts', old="new Date(endsAt.getTime() - 1)", new="endsAt", lane='unit', test='src/modules/announcements/closureSpan.unit.test.ts'),
 dict(id='B4', file='packages/shared/src/announcements/requests.ts', old="  days: z.number().int().min(1).max(EXTENSION_MAX_DAYS),", new="  days: z.number().int().min(1),", lane='shared', test='src/announcements/requests.unit.test.ts'),
 dict(id='B7', file=REPO, old='    AND "ends_on" >= ${firstDay}::date\n', new='', lane='api', test=EXT, name='the preview answers'),
 dict(id='B8', file=SVC, old="await repository.moveEnds(ids, days, at, tx);", new="await repository.moveEnds(ids, closureSpan(closure, at).days, at, tx);", lane='api', test=EXT, name='the owner extends'),
 dict(id='B9', file=REPO, old='AND "ended_at" IS NULL ', new='', lane='api', test=EXT, name='which move'),
 dict(id='B10', file=REPO, old='\n    AND ("starts_on" IS NULL OR "starts_on" <= ${lastDay}::date)`;', new=' AND ${lastDay}::date IS NOT NULL`;', lane='api', test=EXT, name='which move'),
 dict(id='B11', file=REPO, old='"space_id" = ${spaceId} AND ', new='${spaceId}::integer IS NOT NULL AND ', lane='api', test=EXT, name='which move'),
 dict(id='B12', file='apps/api/src/modules/subscriptions/closures/closures.manage.routes.ts', old="    requireCan('subscriptions.extendAfterClosure'),\n", new='', lane='api', test=EXT, name='reception is 403'),
 dict(id='B13', file=SVC, old="const recorded = await repository.findByKey(key, tx);", new="const recorded = key === '' ? await repository.findByKey(key, tx) : null;", lane='api', test=EXT, name='a retry with the same key'),
 dict(id='B14', file=SVC, old=LOCK, new="        if (!(await Promise.resolve(space.id > 0))) {\n", lane='api', test=EXT, name='two owners at once'),
 dict(id='B15', file=SVC, old="        if (closure.startsAt.getTime() > at.getTime()) {\n", new="        if (closure.startsAt.getTime() > at.getTime() && at.getTime() < 0) {\n", lane='api', test=EXT, name='an upcoming closure'),
 dict(id='B16', file=SVC, old="const [extension] = await repository.extensionsOf([closure.id]);", new="const [extension] = await repository.extensionsOf([]);", lane='api', test=EXT, name='an applied extension'),
 dict(id='B17', file=SVC, edits=[[LOCK, "        const early = await announcements.closureIn(space.id, announcementId);\n        const earlyIds = await repository.lockCovered(space.id, closureSpan(early, now()), tx);\n" + LOCK], ["const ids = await repository.lockCovered(space.id, closureSpan(closure, at), tx);", "const ids = earlyIds;"]], lane='api', test=EXT, name='read as committed'),
 dict(id='B18', file=SVC, edits=[[LOCK, "        const early = await announcements.closureIn(space.id, announcementId);\n" + LOCK], ["closureSpan(closure, at), tx);", "closureSpan(early, at), tx);"]], lane='api', test=EXT, name='new span'),
 dict(id='B19', file=SVC, old="const links = await space.linksUnder(tx);", new="const links = space.links;", lane='api', test=EXT, name='link ended'),
 dict(id='B20', file='apps/api/src/shared/errors/constraintCodes.ts', old="  announcements_closure_extended: { type: 'conflict', code: 'CLOSURE_EXTENDED' },\n", new='', lane='api', test='src/modules/announcements/extendedClosure.api.test.ts', name='after its extension'),
]
old = json.load(open('pr4-breaks.json', encoding='utf-8'))
json.dump(old + b, open('pr4-breaks.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(old + b))
