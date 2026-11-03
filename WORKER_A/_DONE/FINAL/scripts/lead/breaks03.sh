#!/bin/bash
# C0.3's breaks B4–B8, each from a backup copy (brk.py restores by copy).
L=/c/dev/masaha/workspace/WORKER_A/FINAL/scripts/lead
B=/c/dev/masaha/workspace/WORKER_A/FINAL/scripts/brk.py
R=/c/dev/masaha/app
T="npx vitest run --project component src/pages/dashboard/routes.component.test.tsx -t navigation"
W=apps/web/src
cd $L
printf '  if (!grouped) return' > o4; printf '  if (grouped || !grouped) return' > n4
python $B $R B4 $W/pages/dashboard/shell/DashboardNavigation.tsx o4 n4 -- "cd apps/web && $T" | head -6
printf 'grouped={isOwner}' > o5; printf 'grouped' > n5
python $B $R B5 $W/pages/dashboard/shell/SpaceLayout.tsx o5 n5 -- "cd apps/web && $T" | head -6
printf "        mode === 'tablet' && 'sr-only',\n        className,\n      )}\n      {...props}\n    />\n  );\n}\n\nexport function SidebarMenu" > o6; printf "        className,\n      )}\n      {...props}\n    />\n  );\n}\n\nexport function SidebarMenu" > n6
python $B $R B6 $W/shared/design-system/components/navigation/Sidebar/Sidebar.tsx o6 n6 -- "cd apps/web && $T" | head -6
printf "{ name: 'audit', segment: 'audit', roles: OWNER, group: 'team' }" > o7; printf "{ name: 'audit', segment: 'audit', roles: BOTH, group: 'team' }" > n7
python $B $R B7 $W/pages/dashboard/navigation.ts o7 n7 -- "cd apps/web && $T" | head -6
printf 'badge.count > 0' > o8; printf 'badge.count >= 0' > n8
python $B $R B8 $W/pages/dashboard/shell/NavigationItem.tsx o8 n8 -- "cd apps/web && $T" | head -6
cd $R && git status --short
