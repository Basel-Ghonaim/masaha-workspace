#!/bin/bash
# The complete local verification (3_EXEC_PROMPT_LEAD.md §5), on feat/final in C:\dev\masaha\app.
# Every heavy step through the grant; each output to scripts/lead/final/<step>.txt; a summary line each.
H=/c/dev/masaha/workspace/WORKER_A/FINAL/scripts
O=$H/lead/final
mkdir -p $O
cd /c/dev/masaha/app
echo "head $(git rev-parse --short HEAD)" > $O/summary.txt
step() { # step <name> <heavy?> <command...>
  local name=$1 heavy=$2; shift 2
  if [ "$heavy" = 1 ]; then node $H/heavy.mjs lead "$@" > $O/$name.txt 2>&1; else "$@" > $O/$name.txt 2>&1; fi
  local code=$?
  local line=$(grep -E "Test Files|Tests  |All matched|No physical|links in|No conflict|conflict|resolve|exit|error" $O/$name.txt | tail -2 | tr '\n' ' ')
  echo "$name exit=$code :: $line" >> $O/summary.txt
}
step npm-ci 0 npm ci
step shared-build 0 npm run build -w @masaha/shared
(cd apps/api && npx prisma generate > $O/prisma-generate.txt 2>&1)
TEST_URL=$(node -e "const t=require('fs').readFileSync('apps/api/.env','utf8');console.log(t.match(/^TEST_DATABASE_URL=\"?([^\"\r\n]+)/m)[1])")
(cd apps/api && DATABASE_URL=$TEST_URL npx prisma migrate deploy > $O/migrate-test.txt 2>&1); echo "migrate-test :: $(tail -1 $O/migrate-test.txt)" >> $O/summary.txt
step format-check 1 npm run format:check
step lint 1 npm run lint
step typecheck 1 npm run typecheck
step check-classes 0 npm run check:classes
step check-links 0 npm run check:links
step check-conflicts 0 npm run check:conflicts
step unit-shared 1 npm run test:unit -w @masaha/shared
step unit-api 1 npm run test:unit -w @masaha/api
step unit-web 1 npm run test:unit -w @masaha/web
step component 1 npm run test:component -w @masaha/web
step api 1 npm run test:api -w @masaha/api
NODE_ENV=production step build 1 npm run build
step check-build 0 npm run check:build
step design-parse 0 node docs/design/scripts/check-parse.mjs
step design-classes 0 node docs/design/scripts/check-classes.mjs
git grep -l '#PRNUM' > $O/prnum-files.txt; echo "prnum files: $(wc -l < $O/prnum-files.txt), non-doc: $(grep -vcE '\.md$' $O/prnum-files.txt)" >> $O/summary.txt
echo DONE >> $O/summary.txt
