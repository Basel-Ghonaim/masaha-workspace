#!/bin/bash
# The rebase todo: drop the two finding records whose defects this PR fixed (LEAD-D7, LEAD-D10).
sed -i -E 's/^pick ([0-9a-f]+) docs: record finding 20(6|10)$/drop \1 docs: record finding 20\2/; s/^pick ([0-9a-f]+) docs: record finding 210$/drop \1 docs: record finding 210/' "$1"
grep -n "^drop\|^fixup" "$1" >&2
