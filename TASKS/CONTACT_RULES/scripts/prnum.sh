#!/usr/bin/env bash
# Replaces "#<from>" with "#<to>" in the docs of every commit of the branch, each commit's tree on its
# own, so no commit's patch conflicts with another's (a rebase that amends each one did).
set -euo pipefail
from="$1"
to="$2"
cd /c/dev/masaha/app-cr
export FILTER_BRANCH_SQUELCH_WARNING=1
git filter-branch -f --tree-filter \
  "grep -rlZ -e '#${from}\\b' docs | xargs -0 -r sed -i 's/#${from}\\b/#${to}/g'" \
  origin/main..HEAD
git update-ref -d refs/original/refs/heads/fix/contact-rules
if git grep -n "#${from}\\b" -- docs; then echo "#${from} is left"; exit 1; fi
echo "replaced #${from} with #${to}"
