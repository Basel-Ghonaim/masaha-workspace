#!/bin/bash
# Make a lane's worktree: mklane.sh <x> <base-sha> [test-db] [dev-db]
set -e
x=$1; base=$2; tdb=$3; ddb=$4
wt=/c/dev/masaha/app-lane-$x
cd /c/dev/masaha/app
git worktree add -q -b lane/$x $wt $base
cp apps/web/.env $wt/apps/web/.env
cp apps/api/.env $wt/apps/api/.env
if [ -n "$tdb" ]; then
  python - "$wt/apps/api/.env" "$tdb" "$ddb" <<'PY'
import sys,re
p,t,d=sys.argv[1],sys.argv[2],sys.argv[3] if len(sys.argv)>3 else ''
s=open(p,encoding='utf8').read()
s=re.sub(r'^(TEST_DATABASE_URL=.*?/)masaha_test', lambda m: m.group(1)+t, s, flags=re.M)
if d: s=re.sub(r'^(DATABASE_URL=.*?/)masaha_dev', lambda m: m.group(1)+d, s, flags=re.M)
open(p,'w',encoding='utf8',newline='').write(s)
PY
fi
cd $wt
npm ci > /c/dev/masaha/workspace/WORKER_A/FINAL/scripts/npmci-$x.txt 2>&1
npm run build -w @masaha/shared > /dev/null 2>&1
echo "lane $x ready at $(git rev-parse --short HEAD)"
