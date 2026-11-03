#!/usr/bin/env bash
# Waits for the supervisor's READY flag beside the execution prompt; prints READY and exits 0, or TIMEOUT and exits 3.
# Usage: wait_ready.sh <hours>
dir=/c/dev/masaha/workspace/WORKER_A/FINAL
deadline=$(( $(date +%s) + ${1:-8} * 3600 ))
while :; do
  if [ -f "$dir/READY" ] && [ -f "$dir/3_EXEC_PROMPT_LEAD.md" ]; then echo "READY $(date +%H:%M)"; exit 0; fi
  [ "$(date +%s)" -ge "$deadline" ] && { echo "TIMEOUT $(date +%H:%M)"; exit 3; }
  echo "$(date +%H:%M) waiting"
  sleep 120
done
