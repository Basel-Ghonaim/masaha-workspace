#!/usr/bin/env bash
# The verification on the head, one command at a time; each's exit and its result lines into head-<name>.txt.
cd /c/dev/masaha/app-b || exit 9
S=/c/dev/masaha/workspace/WORKER_B/FINANCE_AUDIT/scripts
mem() { powershell -NoProfile -Command "(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory" | tr -d '\r'; }
waitmem() { for i in $(seq 1 45); do m=$(mem); [ "$m" -ge 4000000 ] && { echo "mem $1 $m"; return; }; echo "mem $1 $m wait"; sleep 120; done; echo "mem $1 $(mem) ran anyway"; }
step() { name=$1; shift; waitmem $name; "$@" > $S/head2-$name.txt 2>&1; echo "== $name exit $?"; }
echo "head $(git rev-parse HEAD)"
step build npm run build -w @masaha/shared
step lint npm run lint
step typecheck npm run typecheck
step unit npm run test:unit
step format npm run format:check
step links npm run check:links
step conflicts npm run check:conflicts
step api npm run test:api
step component npm run test:component
git grep -l '#PRNUM' > $S/head2-prnum.txt; echo "== prnum files: $(tr '\n' ' ' < $S/head2-prnum.txt)"
echo "== web/package diff: $(git diff --stat origin/main -- apps/web package.json package-lock.json | wc -l)"
echo DONE
