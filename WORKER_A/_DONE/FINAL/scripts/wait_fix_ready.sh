#!/usr/bin/env bash
# Waits for the supervisor's FIX_READY flag beside the fix-round prompt; prints READY and exits 0, or TIMEOUT and exits 3.
# Usage: wait_fix_ready.sh <hours>
dir=/c/dev/masaha/workspace/WORKER_A/FINAL
deadline=$(( $(date +%s) + ${1:-6} * 3600 ))
while :; do
  if [ -f "$dir/FIX_READY" ] && [ -f "$dir/7_FIX_ROUND.md" ]; then echo "READY $(date +%H:%M)"; exit 0; fi
  [ "$(date +%s)" -ge "$deadline" ] && { echo "TIMEOUT $(date +%H:%M)"; exit 3; }
  echo "$(date +%H:%M) waiting"
  sleep 120
done
