#!/bin/sh
cd /c/dev/masaha/app-lane-a1
S=/c/dev/masaha/workspace/WORKER_A/FINAL/scripts/lane-a1
H=C:/dev/masaha/workspace/WORKER_A/FINAL/scripts/heavy.mjs
npm run build -w @masaha/shared > $S/final-shared-build.txt 2>&1; echo "shared build exit $?"
for job in "lint:npm run lint" "typecheck:npm run typecheck" "unit-shared:npm run test:unit -w @masaha/shared" "unit-api:npm run test:unit -w @masaha/api" "unit-web:npm run test:unit -w @masaha/web" "component-web:npm run test:component -w @masaha/web" "api:npm run test:api -w @masaha/api"; do
  name=${job%%:*}; cmd=${job#*:}
  node $H lane-a1 $cmd > $S/final-$name.txt 2>&1
  code=$?
  echo "$name exit $code $(grep -E 'Test Files|Tests  ' $S/final-$name.txt | tr -s ' ' | tr '\n' ' ')"
done
