#!/bin/sh
cd /c/dev/masaha/workspace/WORKER_A/FINAL/scripts/lane-a1
R=/c/dev/masaha/app-lane-a1
STAFF=apps/api/src/modules/space-links/staff/staff.service.ts
T="npm run test:api -w @masaha/api -- src/modules/space-links/staff/staff.api.test.ts"
python mk.py b41.old "          account.role !== 'USER' ||"
python mk.py b41.new "          false ||"
python brk.py $R B41 $STAFF b41.old b41.new -- $T -t "\"OWNER-role account\""
python mk.py b42.old "if (!account || !link || link.deactivatedAt !== null) {"
python mk.py b42.new "if (!account || !link) {"
python brk.py $R B42 $STAFF b42.old b42.new -- $T -t "\"deactivated reception link\""
python mk.py b43.old "          if (account.role === 'ADMIN') throw AppError.conflict('ACCOUNT_IS_ADMIN', 'An admin');"
python mk.py b43.new ""
python brk.py $R B43 $STAFF b43.old b43.new -- $T -t "\"re-activation refuses an admin\""
python mk.py b44.old "          assertTemporaryPasswordLive(locked);\n"
python mk.py b44.new ""
python brk.py $R B44 apps/api/src/modules/users/users.service.ts b44.old b44.new -- npm run test:api -w @masaha/api -- src/modules/auth/sessionLock.api.test.ts -t "\"expires between the check\""
cd $R && git status --short
