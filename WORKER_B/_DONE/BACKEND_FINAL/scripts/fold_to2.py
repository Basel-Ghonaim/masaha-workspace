p = 'apps/api/src/modules/overview/ownerOverview.api.test.ts'
s = open(p, encoding='utf-8', newline='').read()
start = s.index("// The payments service, as the composition root builds it, for the debtors' total it answers.\n")
end = s.index("let spaceId: number;\n")
s = s[:start] + s[end:]
old = """    // The lead adds finance/debts' total at the join.
    const { owed } = await payments.balanceTotals(spaceId, NOW);
    expect(owed.customers).toBe(overview.attention.customersOwing);
"""
new = """    // Finance › debts' total of who owes, an archived debtor included.
    const debts = await request(app)
      .get(spacePath('/finance/debts'))
      .set('Authorization', owner.authorization);
    expect(debts.status).toBe(200);
    expect(
      (debts.body as { meta: { totals: { owed: { customers: number } } } }).meta.totals.owed
        .customers,
    ).toBe(overview.attention.customersOwing);
"""
assert s.count(old) == 1
s = s.replace(old, new)
for line in [
    "import { pino } from 'pino';\n",
    "import { createRunInTransaction, prisma } from '../../db/index.ts';\n",
    "import { writeAudit } from '../../shared/audit/index.ts';\n",
    "import { createCounter, createLimiter } from '../../shared/rate-limit/index.ts';\n",
    "import { createCustomersService } from '../customers/index.ts';\n",
    "import { createPaymentsService } from '../payments/index.ts';\n",
    "import { createSpaceSettingsService } from '../space-settings/index.ts';\n",
    "import { createSpacesService } from '../spaces/index.ts';\n",
    "import { createSubscriptionsService } from '../subscriptions/index.ts';\n",
    "import { createUsersService } from '../users/index.ts';\n",
    "import { createVisitsService } from '../visits/index.ts';\n",
]:
    assert s.count(line) == 1, line
    s = s.replace(line, "import { prisma } from '../../db/index.ts';\n" if 'createRunInTransaction' in line else '')
s = s.replace("import { accessTokens, createTestApp } from '../../../test/app.ts';", "import { createTestApp } from '../../../test/app.ts';")
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
