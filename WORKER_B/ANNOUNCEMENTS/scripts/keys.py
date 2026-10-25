import re,sys
R='C:/dev/masaha/app-b/'
def ed(p, pairs):
    s=open(R+p,encoding='utf-8',newline='').read()
    for a,b,n in pairs:
        assert s.count(a)==n,(p,a,s.count(a))
        s=s.replace(a,b)
    if 'randomUUID' in s and "import { randomUUID } from 'node:crypto';" not in s:
        s="import { randomUUID } from 'node:crypto';\n\n"+s
    open(R+p,'w',encoding='utf-8',newline='').write(s)
K="idempotencyKey: randomUUID(), "
ed('apps/api/src/db/schema.api.test.ts',[
 ("data: { spaceId: space.id, type: 'CLOSURE', textAr: 'مغلق', startsAt, endsAt: startsAt },",
  "data: {\n          spaceId: space.id,\n          type: 'CLOSURE',\n          textAr: 'مغلق',\n          startsAt,\n          endsAt: startsAt,\n          idempotencyKey: randomUUID(),\n        },",1),
 ("        endsAt: new Date('2026-10-03T05:00:00Z'),\n      },\n    });\n    return { space, owner, announcement };",
  "        endsAt: new Date('2026-10-03T05:00:00Z'),\n        idempotencyKey: randomUUID(),\n      },\n    });\n    return { space, owner, announcement };",1)])
ed('apps/api/src/db/seed/demoDirectory.ts',[
 ("            startsAt: daysAgo(1),\n          },","            startsAt: daysAgo(1),\n            idempotencyKey: randomUUID(),\n          },",1)])
ed('apps/api/src/modules/directory/liveStatus.api.test.ts',[
 ("data: { spaceId: closed.id, type: 'CLOSURE', textAr: 'مغلق', startsAt: sunday('08:00') },",
  "data: {\n        spaceId: closed.id,\n        type: 'CLOSURE',\n        textAr: 'مغلق',\n        startsAt: sunday('08:00'),\n        "+K.strip()+"\n      },",1)])
ed('apps/api/src/modules/occupancy/override.api.test.ts',[
 ("data: { spaceId, type: 'CLOSURE', textAr: 'مغلق', startsAt: sunday('08:00') },",
  "data: {\n        spaceId,\n        type: 'CLOSURE',\n        textAr: 'مغلق',\n        startsAt: sunday('08:00'),\n        "+K.strip()+"\n      },",1)])
ed('apps/api/src/modules/occupancy/present.api.test.ts',[
 ("data: { spaceId, type: 'CLOSURE', textAr: 'مغلق', startsAt: sunday('09:30') },",
  "data: {\n        spaceId,\n        type: 'CLOSURE',\n        textAr: 'مغلق',\n        startsAt: sunday('09:30'),\n        "+K.strip()+"\n      },",1),
 ("data: { spaceId, type: 'CLOSURE', textAr: 'مغلق', startsAt: sunday('08:00'), ...data },",
  "data: {\n          spaceId,\n          type: 'CLOSURE',\n          textAr: 'مغلق',\n          startsAt: sunday('08:00'),\n          "+K.strip()+"\n          ...data,\n        },",1),
 ("data: { spaceId: otherSpaceId, type: 'CLOSURE', textAr: 'مغلق', startsAt: sunday('08:00') },",
  "data: {\n        spaceId: otherSpaceId,\n        type: 'CLOSURE',\n        textAr: 'مغلق',\n        startsAt: sunday('08:00'),\n        "+K.strip()+"\n      },",1)])
