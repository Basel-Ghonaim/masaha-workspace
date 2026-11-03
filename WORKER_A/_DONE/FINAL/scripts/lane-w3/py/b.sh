#!/bin/sh
# b.sh <label> <file-rel-to-repo> <test-path> ; reads old/new from b-old.txt / b-new.txt
D=/c/dev/masaha/workspace/WORKER_A/FINAL/scripts/lane-w3/py
python $D/brk.py /c/dev/masaha/app-lane-w3 "$1" "$2" $D/b-old.txt $D/b-new.txt -- npm run test:component -w @masaha/web -- $3
