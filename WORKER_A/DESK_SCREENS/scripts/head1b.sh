#!/usr/bin/env bash
# The head's checks, one at a time; each output in scripts/h-<name>.txt, each exit code in h-exits.txt.
cd /c/dev/masaha/app
S=/c/dev/masaha/workspace/WORKER_A/DESK_SCREENS/scripts
: > $S/h-exits.txt
waitb() { for i in $(seq 1 60); do n=$(powershell -NoProfile -c "@(Get-CimInstance Win32_Process -Filter \"Name='node.exe'\" | Where-Object { \$_.CommandLine -match 'app-b.*vitest' }).Count"); [ "$n" = "0" ] && break; sleep 10; done; echo "app-b vitest $n; free $(powershell -NoProfile -c '(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory')" >> $S/h-exits.txt; }
run() { name=$1; shift; "$@" > $S/h-$name.txt 2>&1; echo "$name $?" >> $S/h-exits.txt; }
waitb; run unit npm run test:unit -w @masaha/web
waitb; run comp npm run test:component -w @masaha/web -- src/features/desk src/features/occupancy src/pages/dashboard src/shared/copy
NODE_ENV=production run build npm run build
run checkbuild npm run check:build
run classes npm run check:classes
run format npm run format:check
run links npm run check:links
run conflicts npm run check:conflicts
echo done >> $S/h-exits.txt
