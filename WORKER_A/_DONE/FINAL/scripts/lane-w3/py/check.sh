#!/bin/sh
# Per-commit checks: prettier, eslint (changed web files, through the grant), typecheck (through the grant).
cd /c/dev/masaha/app-lane-w3 || exit 1
D=/c/dev/masaha/workspace/WORKER_A/FINAL/scripts/lane-w3
FILES=$( (git diff --name-only; git ls-files --others --exclude-standard) | sort -u)
npx prettier --check $(echo "$FILES" | grep -v '\.md$') > $D/prettier.txt 2>&1; echo "prettier exit $?"; tail -3 $D/prettier.txt
TS=$(echo "$FILES" | grep -E '^apps/web/.*\.(ts|tsx)$' | sed 's|^apps/web/||')
(cd apps/web && node C:/dev/masaha/workspace/WORKER_A/FINAL/scripts/heavy.mjs lane-w3 npx eslint $TS) > $D/eslint.txt 2>&1; echo "eslint exit $?"; grep -E 'error|warning|problem' $D/eslint.txt | head -15
node C:/dev/masaha/workspace/WORKER_A/FINAL/scripts/heavy.mjs lane-w3 npm run typecheck > $D/typecheck.txt 2>&1; echo "typecheck exit $?"; grep -E 'error TS' $D/typecheck.txt | head -15
