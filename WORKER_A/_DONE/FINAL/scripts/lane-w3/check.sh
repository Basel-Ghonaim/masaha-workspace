#!/bin/sh
# usage: check.sh <label> <files...>  (run from the worktree root)
label=$1; shift
D=/c/dev/masaha/workspace/WORKER_A/FINAL/scripts/lane-w3
cd /c/dev/masaha/app-lane-w3
npx prettier --check "$@" > $D/prettier-$label.txt 2>&1; echo "prettier exit $?"
code=""; for f in "$@"; do case $f in *.ts|*.tsx) code="$code $f";; esac; done
if [ -n "$code" ]; then node C:/dev/masaha/workspace/WORKER_A/FINAL/scripts/heavy.mjs lane-w3 npx eslint $code > $D/eslint-$label.txt 2>&1; echo "eslint exit $?"; tail -5 $D/eslint-$label.txt; fi
node C:/dev/masaha/workspace/WORKER_A/FINAL/scripts/heavy.mjs lane-w3 npm run typecheck > $D/tsc-$label.txt 2>&1; echo "typecheck exit $?"; grep -E "error TS" $D/tsc-$label.txt | head -20
