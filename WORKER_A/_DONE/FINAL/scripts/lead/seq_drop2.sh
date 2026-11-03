#!/bin/bash
# The rebase todo: drop the records of findings 206 and 210, fixed in this PR (LEAD-D7, LEAD-D10).
sed -i -E 's/^pick ([0-9a-f]+)( #)? docs: record finding (206|210)$/drop \1\2 docs: record finding \3/' "$1"
grep -n "^drop" "$1" >&2
