#!/usr/bin/env bash
# Finishes PR #108 after Copilot ran out of quota (2026-10-22), written by the supervisor.
# 1. Folds Copilot's test fix (useSpacePage's requests told apart by URL) into the commit whose live-status
#    reads broke it (6ea23650, "refresh a space's live status").
# 2. Folds the separate "style: format directory changes" commit (5c3122ff) back into the one commit each of
#    its files came from (each file was touched by exactly one commit of the branch).
# 3. Checks the final tree equals what was there before plus the test fix, lint and typecheck pass, the fixed
#    test passes; then pushes with a lease on 5c3122ff.
# Usage (PowerShell): & "C:\Program Files\Git\bin\bash.exe" C:/dev/masaha/workspace/WORKER_A/PUBLIC/scripts/finish108.sh
# Prints "FINISH OK <new head>" or "FINISH STOP: <why>" (on a stop the backup branch keeps the old head).
set -u
stop() { echo "FINISH STOP: $*"; exit 1; }
cd /c/dev/masaha/app || stop "no app"
T=apps/web/src/features/directory/hooks/page/useSpacePage.component.test.tsx
[ "$(git branch --show-current)" = "feat/space-photos-status" ] || stop "not on feat/space-photos-status"
[ "$(git rev-parse --short HEAD)" = "5c3122ff" ] || stop "head is not 5c3122ff"
[ "$(git status --short)" = " M $T" ] || stop "the working tree holds more than the test fix: $(git status --short | tr '\n' ' ')"
git fetch -q origin || stop "fetch failed"
[ "$(git rev-parse --short origin/feat/space-photos-status)" = "5c3122ff" ] || stop "the pushed head moved"
base=$(git merge-base HEAD origin/main)

git branch -f backup/space-photos-status-pre-finish 5c3122ff || stop "backup failed"
git add "$T" && git commit -q -m "wip: the expected tree" || stop "could not record the expected tree"
wip=$(git rev-parse HEAD)
expected=$(git rev-parse HEAD^{tree})
# Back to where we started: 5c3122ff with the test fix uncommitted.
restore() { git rebase --abort >/dev/null 2>&1; git reset -q --hard "$wip"; git reset -q --soft HEAD~1; git reset -q; }
git reset -q --soft 5c3122ff~1 || stop "reset failed"
git reset -q || stop "unstage failed"

fix() { # <commit> <file>...
  local c=$1; shift
  git add -- "$@" || stop "add failed: $*"
  git commit -q --fixup "$c" || stop "fixup for $c failed"
}
fix 6ea23650 "$T" apps/web/src/features/directory/hooks/page/useSpacePage.ts
fix 04e25352 apps/web/src/features/directory/components/map/DirectoryMap.tsx
fix 1dc46c18 apps/web/src/features/directory/components/page/Gallery.tsx \
  apps/web/src/features/directory/components/page/SpaceDetails.component.test.tsx \
  apps/web/src/features/directory/hooks/page/useGallery.ts
fix 72ae561d apps/web/src/pages/site/routes.component.test.tsx
fix 01289292 apps/web/src/pages/site/shell/SiteFooter.tsx
[ -z "$(git status --short)" ] || { restore; stop "files left over: restored to 5c3122ff with the test fix uncommitted"; }

GIT_SEQUENCE_EDITOR=: git rebase -q -i --autosquash "$base" >/dev/null 2>&1 \
  || { restore; stop "autosquash failed: restored to 5c3122ff with the test fix uncommitted"; }
[ "$(git rev-parse HEAD^{tree})" = "$expected" ] || { restore; stop "the final tree differs from the expected one: restored"; }
git log --format=%s "$base..HEAD" | grep -qE '^(fixup!|style:|wip:)' && { restore; stop "a fixup, style or wip commit is left: restored"; }
echo "commits:"; git log --format='  %h %s' "$base..HEAD"

npm run lint >/dev/null 2>&1 || stop "lint failed"
npm run typecheck >/dev/null 2>&1 || stop "typecheck failed"
npm run test:component -w @masaha/web -- "$T" >/dev/null 2>&1 || stop "the fixed test failed"

git push -q --force-with-lease=feat/space-photos-status:5c3122ff origin feat/space-photos-status || stop "push failed"
echo "FINISH OK $(git rev-parse --short HEAD) (was 5c3122ff); now: gh pr checks 108 --watch --interval 60"
