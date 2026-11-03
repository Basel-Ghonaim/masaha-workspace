#!/bin/bash
L=/c/dev/masaha/workspace/WORKER_A/FINAL/scripts/lead
B=/c/dev/masaha/workspace/WORKER_A/FINAL/scripts/brk.py
R=/c/dev/masaha/app
F=apps/web/src/shared/routing/focus
T="cd apps/web && npx vitest run --project component src/shared/routing/focus src/pages/dashboard/shell/DashboardLayout.component.test.tsx"
cd $L
printf '  if (history.left) return false;' > o9; printf '  return false;' > n9
python $B $R B9 $F/firstPage.ts o9 n9 -- "$T" | head -5
printf '  useMainFocus();\n\n  return (\n    <SidebarProvider' > o10; printf '\n  return (\n    <SidebarProvider' > n10
python $B $R B10 apps/web/src/pages/dashboard/shell/DashboardLayout.tsx o10 n10 -- "$T" | head -5
printf '  if (history.left) return false;' > o11; printf '  if (history.left && arrival !== NavigationType.Pop) return false;' > n11
python $B $R B11 $F/firstPage.ts o11 n11 -- "$T" | head -5
printf '  if (hash.length < 2) return null;' > o12; printf '  if (hash.length > 0) return null;' > n12
python $B $R B12 $F/useMainFocus.ts o12 n12 -- "$T" | head -5
printf '      <SkipLink />\n      <Sidebar label={label}>' > o13; printf '      <Sidebar label={label}>' > n13
python $B $R B13 apps/web/src/pages/dashboard/shell/DashboardLayout.tsx o13 n13 -- "$T" | head -5
cd $R && git status --short
