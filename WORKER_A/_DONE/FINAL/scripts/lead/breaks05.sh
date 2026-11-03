#!/bin/bash
L=/c/dev/masaha/workspace/WORKER_A/FINAL/scripts/lead
B=/c/dev/masaha/workspace/WORKER_A/FINAL/scripts/brk.py
R=/c/dev/masaha/app
W=apps/web/src
RT="cd apps/web && npx vitest run --project component src/pages/dashboard/routes.component.test.tsx -t 'phone'"
UT="cd apps/web && npx vitest run --project component src/features/users/components/CompactAccountMenu.component.test.tsx"
ST="cd apps/web && npx vitest run --project component src/pages/site/shell/SiteLayout.component.test.tsx -t 'every width'"
cd $L
printf '<div className="hidden items-center gap-1 md:flex">' > o14; printf '<div className="flex items-center gap-1">' > n14
python $B $R B14 $W/pages/dashboard/shell/TopBar.tsx o14 n14 -- "$RT" | head -4
printf '            <DashboardLanguageToggle />\n            <DashboardThemeToggle />' > o15; printf '            <DashboardLanguageToggle />' > n15
python $B $R B15 $W/pages/dashboard/shell/DashboardLayout.tsx o15 n15 -- "$RT" | head -4
printf "place={{ in: 'dashboard' }}" > o16; printf "place={{ in: 'site', dashboardPath: '/dashboard' }}" > n16
python $B $R B16 $W/features/users/components/CompactAccountMenu.tsx o16 n16 -- "$UT" | head -4
printf 'role === undefined ? name : copy.users.nameWithRole({ name, role })' > o17; printf 'name' > n17
python $B $R B17 $W/features/users/hooks/useAccount.ts o17 n17 -- "$UT" | head -4
printf '<SiteThemeToggle className="hidden md:inline-flex" />' > o18; printf '<SiteThemeToggle />' > n18
python $B $R B18 $W/pages/site/shell/SiteHeader.tsx o18 n18 -- "$ST" | head -4
cd $R && git status --short | head -30
