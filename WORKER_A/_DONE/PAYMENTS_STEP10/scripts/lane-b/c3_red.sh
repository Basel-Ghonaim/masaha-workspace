#!/usr/bin/env bash
# Commit 3's red step: its new code moved aside and its changed code set back to commit 2's, the
# admin's tests run, then everything restored from the backup copies and checked with cmp.
set -u
cd /c/dev/masaha/app-lane-b
L=/c/dev/masaha/workspace/WORKER_A/PAYMENTS_STEP10/scripts/lane-b
B=$L/bak-c3-red
rm -rf "$B" && mkdir -p "$B"
W=apps/web/src
NEW="$W/features/data-reports/services/adminReportsQueryOf.ts
$W/features/data-reports/hooks/admin/useAdminReports.ts
$W/features/data-reports/hooks/admin/useAdminReportsFilters.ts
$W/features/data-reports/components/admin/AdminReportsList.tsx
$W/features/data-reports/components/admin/AdminReportFilters.tsx
$W/features/data-reports/components/admin/FilterTags.tsx
$W/features/data-reports/types/AdminReportRowView.ts
$W/features/data-reports/types/AdminSpaceFilterSlot.ts
$W/features/space-links/components/admin-filter/AdminSpaceFilter.tsx
$W/pages/dashboard/admin/DataReportsPage.tsx"
CHANGED="$W/features/data-reports/repository/dataReportsRepository.ts
$W/features/data-reports/hooks/decide/useDecideReport.ts
$W/features/data-reports/hooks/decide/useDecideSheet.ts
$W/features/data-reports/components/decide/DecideSheet.tsx
$W/features/data-reports/types/DecideTarget.ts
$W/features/data-reports/hooks/queryKeys.ts
$W/features/data-reports/index.ts
$W/pages/dashboard/routes.tsx"
for f in $NEW $CHANGED; do mkdir -p "$B/$(dirname "$f")"; cp "$f" "$B/$f"; done
for f in $NEW; do rm "$f"; done
for f in $CHANGED; do git show "HEAD:$f" > "$f"; done

npm run test:unit -w @masaha/web -- src/features/data-reports > "$L/c3-red-unit.txt" 2>&1; echo "unit $?"
npm run test:component -w @masaha/web -- src/features/data-reports/hooks/admin src/features/data-reports/components/admin src/features/data-reports/hooks/decide src/features/space-links/components/admin-filter > "$L/c3-red-comp.txt" 2>&1; echo "comp $?"
npm run test:component -w @masaha/web -- src/pages/dashboard/routes.component.test.tsx -t "admin's data reports" > "$L/c3-red-routes.txt" 2>&1; echo "routes $?"

for f in $NEW $CHANGED; do mkdir -p "$(dirname "$f")"; cp "$B/$f" "$f"; done
for f in $NEW $CHANGED; do cmp -s "$f" "$B/$f" && echo "same $f" || echo "DIFF $f"; done
