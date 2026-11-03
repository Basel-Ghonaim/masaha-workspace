#!/usr/bin/env bash
# Sets the PR number in every commit's tree of feat/step10-screens (the lead's run), and in the description.
# Usage: bash prnum-lead.sh <expected number> [--no-next-check]
# Rewrites a temporary branch, checks it, then moves feat/step10-screens onto it (clean tree only; no reset --hard).
# Prints "PRNUM OK #<n> <new head>" and exits 0, or "PRNUM STOP: <why>" and exits 1, leaving the branch as it was.
set -u
stop() { echo "PRNUM STOP: $*"; git branch -D prnum-tmp >/dev/null 2>&1; exit 1; }
expected="${1:-}"
check_next="${2:-}"
BRANCH=feat/step10-screens
[[ "$expected" =~ ^[0-9]+$ ]] || stop "give the expected PR number as the first argument"
cd /c/dev/masaha/app || stop "no app"
[ "$(git branch --show-current)" = "$BRANCH" ] || stop "not on $BRANCH"
[ -z "$(git status --short)" ] || stop "the working tree is not clean"
git fetch -q origin || stop "fetch failed"
if [ "$check_next" != "--no-next-check" ]; then
  last=$(gh api "repos/Basel-Ghonaim/masaha/issues?state=all&per_page=1" --jq '.[0].number') || stop "gh api failed"
  [[ "$last" =~ ^[0-9]+$ ]] || stop "the last number is not a number: $last"
  n=$((last + 1))
  [ "$n" -eq "$expected" ] || stop "the next number is $n, not $expected"
fi
n=$expected
base=$(git merge-base HEAD origin/main)
old=$(git rev-parse HEAD)
files_before=$(git diff --name-only origin/main HEAD)
git branch -f backup/step10-pre-prnum "$old" || stop "backup branch failed"
git branch -f prnum-tmp "$old" || stop "temp branch failed"
FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f -d /c/dev/masaha/workspace/WORKER_A/PAYMENTS_STEP10/scripts/fb-tmp \
  --tree-filter "git grep -l '#PRNUM' -- docs apps | xargs -r sed -i 's/#PRNUM/#$n/g'" "$base..prnum-tmp" >/dev/null 2>&1 \
  || stop "filter-branch failed; $BRANCH untouched"
git for-each-ref --format='%(refname)' refs/original/ | xargs -r -n1 git update-ref -d
new=$(git rev-parse prnum-tmp)
[ -z "$(git grep -n '#PRNUM' "$new")" ] || stop "#PRNUM still in the new head"
for c in $(git rev-list "$base..$new"); do
  [ -z "$(git grep -n '#PRNUM' "$c")" ] || stop "#PRNUM still in commit $c"
done
changed=$(git diff "$old" "$new" | grep -E '^[-+][^-+]' | grep -vcE "#PRNUM|#$n")
[ "$changed" -eq 0 ] || stop "the rewrite changed more than the number"
[ "$(git diff --name-only origin/main "$new")" = "$files_before" ] || stop "the files changed against main differ"
[ "$(git rev-list --count "$base..$new")" = "$(git rev-list --count "$base..$old")" ] || stop "the commit count differs"
[ "$(git log --format=%s "$base..$new")" = "$(git log --format=%s "$base..$old")" ] || stop "a subject changed"
git switch -q -C "$BRANCH" "$new" || stop "could not move $BRANCH"
git branch -D prnum-tmp >/dev/null
[ -z "$(git status --short)" ] || stop "the working tree is not clean after the move"
body=/c/dev/masaha/workspace/WORKER_A/PAYMENTS_STEP10/scripts/pr-body-lead.md
if [ -f "$body" ]; then
  sed -i "s/#PRNUM/#$n/g" "$body"
  grep -q '#PRNUM' "$body" && stop "#PRNUM still in the description"
fi
echo "PRNUM OK #$n $(git rev-parse --short HEAD) (was ${old:0:8})"
