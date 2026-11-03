REPO = r'C:\dev\masaha\app-lane-w1'
T = 'npm run test:component -w @masaha/web -- src/features/staff/components/StaffList'
H = r'apps\web\src\features\staff\hooks\list\useStaffList.ts'
A = r'apps\web\src\features\staff\hooks\access\useStaffActions.ts'
BREAKS = [
    ('B138', H, "    const agorot = collections.of(userId);", "    const agorot = collections.of(16);", T),
    ('B139', H, "agorot === null ? words.noCollections : priceText(agorot, language)", "priceText(agorot ?? 0, language)", T),
    ('B140', A, "    items: [collections, ...(", "    items: [...(", T),
]
