#!/bin/sh
cd /c/dev/masaha/workspace/WORKER_A/FINAL/scripts/lane-a1
R=/c/dev/masaha/app-lane-a1
AUTH=apps/api/src/modules/auth/auth.service.ts
USERS=apps/api/src/modules/users/users.service.ts
T="npm run test:api -w @masaha/api -- src/modules/auth/replacement.api.test.ts"
python mk.py b27.old "users.register(request, freeAddress)"
python mk.py b27.new "users.register(request)"
python brk.py $R B27 $AUTH b27.old b27.new -- $T
python mk.py b28.old "if (spaceId !== null) await spaceLinks.endReceptionBySystem(spaceId, holderId, tx);"
python mk.py b28.new ""
python brk.py $R B28 $AUTH b28.old b28.new -- $T
python mk.py b29.old "if ((await spaceLinks.ownsASpace(holderId, tx)) || (await hasActed(holderId, tx))) {"
python mk.py b29.new "if (holderId < 0) {"
python brk.py $R B29 $AUTH b29.old b29.new -- $T
python mk.py b30.old "temporaryPasswordExpired(holder.account, now)"
python mk.py b30.new "holder.account.mustChangePassword"
python brk.py $R B30 $USERS b30.old b30.new -- $T
python mk.py b31.old "          freeAddress,\n        );"
python mk.py b31.new "        );"
python brk.py $R B31 $AUTH b31.old b31.new -- $T
python mk.py b32.old "        if (replaced) await recordReplaced(replaced, created.account.id, tx);"
python mk.py b32.new ""
python brk.py $R B32 $USERS b32.old b32.new -- $T
cd $R && git status --short
