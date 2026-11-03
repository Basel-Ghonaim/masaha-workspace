#!/usr/bin/env bash
# Commits the five stages as fixups of their homes, in order; stops at the first failure.
set -eu
cd /c/dev/masaha/app
S=/c/dev/masaha/workspace/WORKER_A/PAYMENTS_STEP10/scripts/fixround
W=apps/web/src
home() { git log --format=%h -1 --grep="$1" origin/main..HEAD; }
OWNER=$(home "decide a space's reports")
ADMIN=$(home "list every space's reports")
REPORT=$(home "report wrong information")
CARD=$(home "save a space from its card")
LIST=$(home "list a user's favourite spaces")
echo "homes: $OWNER $ADMIN $REPORT $CARD $LIST"

PYTHONIOENCODING=utf8 python $S/stages.py stage 4
git add $W/features/favorites/hooks/intent/favoriteIntent.ts $W/features/favorites/hooks/intent/favoriteIntent.unit.test.ts $W/features/favorites/components/FavoriteButton.component.test.tsx $W/features/favorites/hooks/toggle/useFavoriteToggle.component.test.tsx $W/pages/site/public/space/SpacePage.component.test.tsx $W/features/favorites/hooks/toggle/useFavoriteToggle.ts docs/features/favorites.md
git commit -q --fixup "$CARD"

PYTHONIOENCODING=utf8 python $S/stages.py stage 5
git add $W/features/favorites/hooks/toggle/useFavoriteToggle.ts $W/features/favorites/components/RemoveFavorite.tsx $W/features/favorites/components/RemoveFavorite.component.test.tsx $W/features/favorites/components/toast/favoriteToasts.tsx $W/features/favorites/hooks/favoriteWrite.ts $W/shared/copy/arabic/favorites.ts $W/shared/copy/english/favorites.ts docs/features/favorites.md docs/features/directory.md docs/architecture/findings/187-a-favourite-just-removed-cannot-be-saved-again-for-an-undo.md
git commit -q --fixup "$LIST"

git status --short
git log --format='%h %s' -6
