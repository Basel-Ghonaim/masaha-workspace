#!/usr/bin/env bash
# Watches the workers' PRs every 10 minutes until one is ready for review, or the deadline passes.
# Ready = an open PR on the branch, every check passed (none pending), CLEAN, and the worker's report naming the
# PR and unchanged for one whole interval (the worker finished writing it).
# Usage: watch_ready.sh <deadline epoch seconds> <name>=<branch>=<report path> ...
# Prints "READY <name> #<n> <sha>" and exits 0 at the first ready one; "TIMEOUT" and each one's state, exit 3.
deadline=$1; shift
declare -A last
while :; do
  for spec in "$@"; do
    IFS='=' read -r name branch report <<< "$spec"
    pr=$(gh pr list --repo Basel-Ghonaim/masaha --head "$branch" --state open --json number,headRefOid,mergeStateStatus \
      --jq '.[0] | "\(.number) \(.headRefOid) \(.mergeStateStatus)"' 2>/dev/null)
    if [ -z "$pr" ] || [ "$pr" = "null null null" ]; then state="$name: no PR yet"; last[$name]=""; echo "$(date +%H:%M) $state"; continue; fi
    read -r n sha merge <<< "$pr"
    checks=$(gh pr checks "$n" --repo Basel-Ghonaim/masaha --json bucket --jq '[.[].bucket] | "\(length) \(map(select(. == "pending")) | length) \(map(select(. == "fail" or . == "cancel")) | length)"' 2>/dev/null)
    read -r total pending failed <<< "$checks"
    stamp=""
    if [ -f "$report" ] && grep -q "#$n" "$report"; then stamp=$(stat -c %Y "$report"); fi
    echo "$(date +%H:%M) $name: #$n ${sha:0:8} $merge checks=$total pending=$pending failed=$failed report=${stamp:-not naming the PR}"
    if [ -n "$total" ] && [ "$total" -gt 0 ] && [ "$pending" = 0 ] && [ "$failed" = 0 ] && [ "$merge" = CLEAN ] \
       && [ -n "$stamp" ] && [ "${last[$name]}" = "$sha $stamp" ]; then
      echo "READY $name #$n $sha"; exit 0
    fi
    last[$name]="$sha $stamp"
  done
  [ "$(date +%s)" -ge "$deadline" ] && { echo "TIMEOUT"; exit 3; }
  sleep 600
done
