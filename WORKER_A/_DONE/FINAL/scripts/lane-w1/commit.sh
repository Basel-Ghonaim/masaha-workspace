#!/usr/bin/env bash
# commit.sh <variant.py> <msg-file> [ENV=..] : stages the variant, shows the staged stat, commits.
set -e
cd /c/dev/masaha/app-lane-w1
S=/c/dev/masaha/workspace/WORKER_A/FINAL/scripts/lane-w1
python $S/stage_variant.py "$S/$1" > /dev/null
git diff --cached --stat | tail -40
git commit -q -F "$S/$2"
git log --oneline -1
