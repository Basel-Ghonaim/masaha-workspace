#!/usr/bin/env bash
# PR 3's head-wide checks, once each; each output in h3-<name>.txt, each exit in h3-exits.txt.
cd /c/dev/masaha/app || exit 1
S=/c/dev/masaha/workspace/WORKER_A/DESK_SCREENS/scripts
: > "$S/h3-exits.txt"
mem() {
  powershell -NoProfile -Command "\"free KB \" + (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory + \"; app-b vitest \" + (Get-CimInstance Win32_Process -Filter \"Name='node.exe'\" | Where-Object { \$_.CommandLine -match 'app-b' -and \$_.CommandLine -match 'vitest' } | Measure-Object).Count" >> "$S/h3-exits.txt"
}
run() {
  local name=$1; shift
  local start=$(date +%s)
  "$@" > "$S/h3-$name.txt" 2>&1
  echo "$name exit $? ($(( $(date +%s) - start )) s)" >> "$S/h3-exits.txt"
}
mem; run unit npm run test:unit -w @masaha/web
mem; run comp npm run test:component -w @masaha/web -- src/features/desk src/features/occupancy src/pages/dashboard src/pages/site/auth src/shared/session src/shared/copy src/shared/lists
run build env NODE_ENV=production npm run build
run checkbuild npm run check:build
run classes npm run check:classes
run format npm run format:check
run links npm run check:links
run conflicts npm run check:conflicts
