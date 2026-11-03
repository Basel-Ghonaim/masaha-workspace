import os, re
root = r'C:\dev\masaha\app-lane-t\apps\web\src'
NOTE = "// The lazy modules its tests open, loaded once before any test waits (src/test/warmLazy.ts).\n"
def edit(rel, vitest_old, vitest_new, after_import, warm_import, loaders):
    p = os.path.join(root, rel); s = open(p, encoding='utf8').read()
    if vitest_old != vitest_new:
        assert s.count(vitest_old) == 1, (rel, vitest_old); s = s.replace(vitest_old, vitest_new, 1)
    assert s.count(after_import) == 1, (rel, after_import)
    body = ''.join(f"    () => import('{m}'),\n" for m in loaders)
    block = f"{after_import}\n{NOTE}beforeAll(\n  () =>\n    warm(\n{body}    ),\n  60_000,\n);\n"
    s = s.replace(after_import, block, 1)
    # the warm import after the last import from the test folder
    imports = list(re.finditer(r"^import .*? from '(\.\./)+test/[^']+';\n", s, re.M))
    last = imports[-1]
    s = s[:last.end()] + warm_import + s[last.end():]
    open(p, 'w', encoding='utf8', newline='').write(s)

D = ['./shell/SpaceLayout','./shell/AdminLayout','./DashboardLanding','./PlaceholderPage',
     './space/overview/OverviewPage','./space/desk/DeskPage','./space/customers/CustomersPage','./space/customers/CustomerPage',
     './space/payments/PaymentsPage','./space/payments/MyPaymentsPage','./space/StaffPage','./space/SettingsPage',
     './space/ProfilePage','./space/PackagesPage','./space/announcements/AnnouncementsPage','./space/reports/DataReportsPage',
     './space/finance/FinancePage','./space/audit/AuditPage',
     './admin/overview/OverviewPage','./admin/SpacesPage','./admin/AddSpacePage','./admin/SpaceEditPage','./admin/UsersPage',
     './admin/OwnersPage','./admin/DataReportsPage','./admin/LookupsPage','./admin/audit/AuditPage','./admin/settings/SettingsPage']
edit(r'pages\dashboard\routes.component.test.tsx', 'x', 'x', "import { dashboardRoutes } from './routes';\n",
     "import { warm } from '../../test/warmLazy';\n", D)
edit(r'pages\site\routes.component.test.tsx',
     "import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';",
     "import { afterEach, beforeAll, beforeEach, describe, expect, it, vi } from 'vitest';",
     "import { siteRoutes } from './routes';\n", "import { warm } from '../../test/warmLazy';\n",
     ['./shell/SiteLayout','./shell/FocusLayout','./public/home/HomePage','./public/directory/DirectoryPage',
      './public/space/SpacePage','./public/about/AboutPage','./public/not-found/NotFoundPage'])
edit(r'pages\site\shell\SiteLayout.component.test.tsx',
     "import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';",
     "import { afterEach, beforeAll, beforeEach, describe, expect, it, vi } from 'vitest';",
     "import { siteRoutes } from '../routes';\n", "import { warm } from '../../../test/warmLazy';\n",
     ['./SiteLayout','./FocusLayout','../public/home/HomePage','../public/directory/DirectoryPage',
      '../public/about/AboutPage','../auth/SignInPage'])
edit(r'pages\site\auth\authPages.component.test.tsx',
     "import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';",
     "import { afterEach, beforeAll, beforeEach, describe, expect, it, vi } from 'vitest';",
     "import { siteRoutes } from '../routes';\n", "import { warm } from '../../../test/warmLazy';\n",
     ['../shell/FocusLayout','../shell/SiteLayout','./SignInPage','./RegisterPage','./ForgotPasswordPage',
      '@features/users','../public/about/AboutPage','../public/directory/DirectoryPage'])
edit(r'app\App.component.test.tsx', 'x', 'x', "import { bootstrap } from './bootstrap';\n",
     "import { warm } from '../test/warmLazy';\n",
     ['../pages/site/shell/SiteLayout','../pages/site/public/home/HomePage'])
edit(r'app\router.component.test.tsx',
     "import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';",
     "import { afterEach, beforeAll, beforeEach, describe, expect, it, vi } from 'vitest';",
     "import { routes } from './router';\n", "import { warm } from '../test/warmLazy';\n",
     ['../pages/site/shell/SiteLayout','../pages/site/public/home/HomePage'])
