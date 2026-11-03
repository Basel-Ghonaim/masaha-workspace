#!/usr/bin/env bash
# DEPLOY's complete local verification on the branch's head, one command at a time. Each command's
# exit code and last lines go to verify-log.txt.
cd /c/dev/masaha/app-b || exit 1
LOG=/c/dev/masaha/workspace/WORKER_B/DEPLOY/scripts/verify-log.txt
: > "$LOG"
echo "head $(git rev-parse --short HEAD) $(date -Iseconds)" >> "$LOG"
free_gb() { powershell -NoProfile -Command "[math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1MB,1)"; }
step() {
  local name="$1"; shift
  echo "=== $name (free $(free_gb) GB) $(date +%T)" >> "$LOG"
  "$@" > /tmp/verify-step.txt 2>&1
  local code=$?
  tail -6 /tmp/verify-step.txt >> "$LOG"
  echo "--- $name exit $code" >> "$LOG"
}
step "npm ci" npm ci
step "build shared" npm run build -w @masaha/shared
step "format:check" npm run format:check
step "lint" npm run lint
step "typecheck" npm run typecheck
step "check:classes" npm run check:classes
step "check:links" npm run check:links
step "check:conflicts" npm run check:conflicts
step "test:unit" npm run test:unit
step "test:component" npm run test:component
step "test:api" npm run test:api
step "build (production)" env NODE_ENV=production npm run build
step "check:build" npm run check:build
echo "done $(date -Iseconds)" >> "$LOG"
