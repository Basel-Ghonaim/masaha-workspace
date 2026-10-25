#!/usr/bin/env bash
# Sets the PR number in the documents of every commit of feat/data-reports, and in the description.
# Usage (from PowerShell): & "C:\Program Files\Git\bin\bash.exe" C:/dev/masaha/workspace/WORKER_B/ANNOUNCEMENTS/scripts/prnum-pr2.sh <expected number>
# Prints "PRNUM OK #<n> <new head>" and exits 0, or prints "PRNUM STOP: <why>" and exits 1. Changes nothing on a stop.
set -u
stop() { echo "PRNUM STOP: $*"; exit 1; }
expected="${1:-}"
[[ "$expected" =~ ^[0-9]+$ ]] || stop "give the expected PR number as the only argument"
cd /c/dev/masaha/app-b || stop "no app-b"
[ "$(git branch --show-current)" = "feat/data-reports" ] || stop "not on feat/data-reports"
[ -z "$(git status --short)" ] || stop "the working tree is not clean"
git fetch -q origin || stop "fetch failed"
last=$(gh api "repos/{owner}/{repo}/issues?state=all&per_page=1&sort=created&direction=desc" --jq '.[0].number') || stop "gh api failed"
[[ "$last" =~ ^[0-9]+$ ]] || stop "the last number is not a number: $last"
n=$((last + 1))
[ "$n" -eq "$expected" ] || stop "the next number is $n, not $expected"
base=$(git merge-base HEAD origin/main)
old=$(git rev-parse HEAD)
git branch -f backup/data-reports-pre-prnum "$old" || stop "backup branch failed"
FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f --tree-filter "grep -rl '#PRNUM' docs | xargs -r sed -i 's/#PRNUM/#$n/g'" "$base..HEAD" >/dev/null 2>&1 \
  || { git reset -q --hard "$old"; stop "filter-branch failed; head restored to $old"; }
git for-each-ref --format='%(refname)' refs/original/ | xargs -r -n1 git update-ref -d
[ -z "$(git grep -n '#PRNUM')" ] || stop "#PRNUM still in the tree (backup: backup/data-reports-pre-prnum)"
changed=$(git diff "$old" HEAD | grep -E '^[-+][^-+]' | grep -vcE "#PRNUM|#$n")
[ "$changed" -eq 0 ] || stop "the rewrite changed more than the number (backup: backup/data-reports-pre-prnum)"
[ -z "$(git status --short)" ] || stop "the working tree is not clean after the rewrite"
body=/c/dev/masaha/workspace/WORKER_B/ANNOUNCEMENTS/scripts/pr2-body.md
sed -i "s/#PRNUM/#$n/g" "$body"
grep -q '#PRNUM' "$body" && stop "#PRNUM still in the description"
echo "PRNUM OK #$n $(git rev-parse --short HEAD) (was ${old:0:8})"
