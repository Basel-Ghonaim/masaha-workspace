D = 'C:/dev/masaha/app-b-lane-f/apps/api/src/modules/'


def rw(p, f):
    s = open(D + p, encoding='utf-8', newline='').read()
    s = f(s)
    open(D + p, 'w', encoding='utf-8', newline='').write(s)


def rep(s, old, new):
    assert s.count(old) == 1, old[:80]
    return s.replace(old, new)


def service(s):
    s = rep(s, "import { addMonths, gazaClockOf } from '@masaha/shared/core';\nimport type { FinanceMonthQuery, IncomeReport } from '@masaha/shared/finance';\n",
            """import { addMonths, gazaClockOf, type PaginationMeta } from '@masaha/shared/core';
import type {
  BalanceRow,
  DebtsMeta,
  DebtsQuery,
  FinanceMonthQuery,
  IncomeReport,
  Payer,
  PayersQuery,
} from '@masaha/shared/finance';
""")
    s = rep(s, """import { AppError } from '../../shared/errors/index.ts';
import type { IncomeWindow, PaymentsService } from '../payments/index.ts';
import type { UsersService } from '../users/index.ts';
import { toCollections } from './finance.mapper.ts';
""", """import { AppError } from '../../shared/errors/index.ts';
import { toSkip } from '../../shared/http/index.ts';
import type { CustomersService } from '../customers/index.ts';
import type { IncomeWindow, PaymentsService } from '../payments/index.ts';
import type { SpaceSettingsService } from '../space-settings/index.ts';
import type { SubscriptionsService } from '../subscriptions/index.ts';
import type { UsersService } from '../users/index.ts';
import type { VisitsService } from '../visits/index.ts';
import { toBalanceRow, toCollections } from './finance.mapper.ts';
import { createFinanceRepository } from './finance.repository.ts';
""")
    s = rep(s, """  /** The ledger's aggregates: income, collections. */
  payments: PaymentsService;
  /** The names of who recorded the payments. */
  users: UsersService;
""", """  /** The ledger's aggregates: income, collections, the balances and the uncollected visits. */
  payments: PaymentsService;
  /** The names of who recorded the payments. */
  users: UsersService;
  /** The debtors' names and phones, an archived one marked; the payers' names. */
  customers: CustomersService;
  /** The name of a debtor's oldest subscription still owing. */
  subscriptions: SubscriptionsService;
  /** The name of a debtor's oldest visit still owing. */
  visits: VisitsService;
  /** The space's reminder template. */
  spaceSettings: SpaceSettingsService;
""")
    s = rep(s, "export function createFinanceService({ readSnapshot, payments, users, now }: Dependencies) {\n",
            """export function createFinanceService({
  readSnapshot,
  payments,
  users,
  customers,
  subscriptions,
  visits,
  spaceSettings,
  now,
}: Dependencies) {
  const repository = createFinanceRepository();

""")
    s = rep(s, """      };
    },
  };
}

export type FinanceService""", """      };
    },

    /**
     * Who owes, or who is in credit (`state`), by the ledger's one balance rule — an archived
     * customer's kept and marked — the largest first, paged, each with their phone and, who owes,
     * the item still owing made first; with the space's totals (owed, in credit, the uncollected
     * visits apart) and its reminder template. All of it in one snapshot, so the page agrees with
     * its totals.
     */
    debts(
      spaceId: number,
      query: DebtsQuery,
    ): Promise<{
      rows: BalanceRow[];
      total: number;
      meta: Omit<DebtsMeta, keyof PaginationMeta>;
    }> {
      const at = now();
      return readSnapshot(async (tx) => {
        const [page, balances, uncollected, settings] = await Promise.all([
          payments.balancesPage(spaceId, query.state, at, query, tx),
          payments.balanceTotals(spaceId, at, tx),
          payments.uncollectedTotals(spaceId, tx),
          spaceSettings.read(spaceId, tx),
        ]);
        const oldestOf = (kind: 'VISIT' | 'SUBSCRIPTION') =>
          page.rows.flatMap(({ oldest }) => (oldest?.kind === kind ? [oldest.id] : []));
        const [contacts, subscriptionNames, deskVisits] = await Promise.all([
          customers.contactsOf(
            spaceId,
            page.rows.map(({ customerId }) => customerId),
            tx,
          ),
          subscriptions.namesOf(spaceId, oldestOf('SUBSCRIPTION'), tx),
          visits.deskVisitsOf(spaceId, oldestOf('VISIT'), tx),
        ]);
        /** The oldest item's name: a visit's visitor, else its customer; a subscription's. */
        const nameOf = ({ kind, id }: { kind: 'VISIT' | 'SUBSCRIPTION'; id: number }) => {
          if (kind === 'SUBSCRIPTION') {
            const subscription = subscriptionNames.get(id);
            if (!subscription) throw new Error(`The subscription ${String(id)} is missing.`);
            return subscription.name;
          }
          const visit = deskVisits.get(id);
          if (!visit) throw new Error(`The visit ${String(id)} is missing.`);
          return visit.visitorName ?? visit.customer?.name ?? null;
        };
        return {
          rows: page.rows.map((row) => {
            const contact = contacts.get(row.customerId);
            if (!contact) throw new Error(`The customer ${String(row.customerId)} is missing.`);
            return toBalanceRow(row, contact, row.oldest && nameOf(row.oldest));
          }),
          total: page.total,
          meta: {
            totals: { ...balances, uncollected },
            reminderTemplate: settings.reminderTemplate,
          },
        };
      });
    },

    /**
     * Who paid in the month (the current Gaza month by default): each customer with what they paid
     * then, the latest paid first, paged; named after the page. Read apart, as every list.
     */
    async payers(spaceId: number, query: PayersQuery): Promise<{ rows: Payer[]; total: number }> {
      const month = monthAsked(query.month, now());
      const { rows, total } = await repository.payersIn(spaceId, monthWindow(month), {
        skip: toSkip(query),
        take: query.limit,
      });
      const names = await customers.namesOf(
        spaceId,
        rows.map(({ customerId }) => customerId),
      );
      return {
        rows: rows.map(({ customerId, paidAgorot, lastPaidAt }) => {
          const name = names.get(customerId);
          if (name === undefined) throw new Error(`The customer ${String(customerId)} is missing.`);
          return { customer: { id: customerId, name }, paidAgorot, lastPaidAt: lastPaidAt.toISOString() };
        }),
        total,
      };
    },
  };
}

export type FinanceService""")
    return s


def mapper(s):
    s = rep(s, "import type { Collections } from '@masaha/shared/finance';\n\nimport type { CollectionsRow } from '../payments/index.ts';",
            "import { gazaClockOf } from '@masaha/shared/core';\nimport type { BalanceRow, Collections } from '@masaha/shared/finance';\n\nimport type { CustomerContact } from '../customers/index.ts';\nimport type { BalancePageRow, CollectionsRow } from '../payments/index.ts';")
    return s + """
/**
 * A customer's balance as the debts list shows it: the customer's contact, archived or not; its
 * oldest item still owing, named, with the Gaza day it was made.
 */
export function toBalanceRow(
  { amountAgorot, oldest }: BalancePageRow,
  customer: CustomerContact,
  name: string | null,
): BalanceRow {
  return {
    customer,
    amountAgorot,
    oldestItem: oldest && {
      kind: oldest.kind,
      id: oldest.id,
      name,
      since: gazaClockOf(oldest.createdAt).date,
    },
  };
}
"""


rw('finance/finance.service.ts', service)
rw('finance/finance.mapper.ts', mapper)
rw('customers/index.ts', lambda s: s + "export type { CustomerContact } from './customers.repository.ts';\n")


def controller(s):
    s = rep(s, "import type { FinanceMonthQuery, IncomeReport } from '@masaha/shared/finance';",
            "import type {\n  BalanceRow,\n  DebtsMeta,\n  DebtsQuery,\n  FinanceMonthQuery,\n  IncomeReport,\n  Payer,\n  PayersQuery,\n} from '@masaha/shared/finance';")
    s = rep(s, "import { sendSuccess } from '../../shared/http/index.ts';",
            "import { buildPaginationMeta, sendSuccess } from '../../shared/http/index.ts';")
    s = rep(s, """      sendSuccess(res, (await service.income(spaceOf(req).id, query)) satisfies IncomeReport);
    },
""", """      sendSuccess(res, (await service.income(spaceOf(req).id, query)) satisfies IncomeReport);
    },

    /** 200 with a page of `BalanceRow` and its `DebtsMeta`: the totals and the reminder template. */
    debts: async (req: Request, res: Response) => {
      const query = req.query as unknown as DebtsQuery;
      const { rows, total, meta } = await service.debts(spaceOf(req).id, query);
      const debtsMeta: DebtsMeta = { ...buildPaginationMeta(query, total), ...meta };
      sendSuccess(res, rows satisfies BalanceRow[], { meta: debtsMeta });
    },

    /** 200 with a page of the month's `Payer` and its pagination. */
    payers: async (req: Request, res: Response) => {
      const query = req.query as unknown as PayersQuery;
      const { rows, total } = await service.payers(spaceOf(req).id, query);
      sendSuccess(res, rows satisfies Payer[], { meta: buildPaginationMeta(query, total) });
    },
""")
    return s


def routes(s):
    s = rep(s, "import { financeMonthQuery } from '@masaha/shared/finance';",
            "import { debtsQuerySchema, financeMonthQuery, payersQuerySchema } from '@masaha/shared/finance';")
    s = rep(s, """    controller.income,
  );
""", """    controller.income,
  );
  router.get(
    '/debts',
    requireCan('finance.read'),
    validate(debtsQuerySchema, 'query'),
    controller.debts,
  );
  router.get(
    '/payers',
    requireCan('finance.read'),
    validate(payersQuerySchema, 'query'),
    controller.payers,
  );
""")
    return s


rw('finance/finance.controller.ts', controller)
rw('finance/finance.manage.routes.ts', routes)


def app(s):
    return rep(s, """  const finance = createFinanceService({
    readSnapshot: createReadSnapshot(),
    payments,
    users,
    now: clock,
  });""", """  const finance = createFinanceService({
    readSnapshot: createReadSnapshot(),
    payments,
    users,
    customers,
    subscriptions,
    visits,
    spaceSettings,
    now: clock,
  });""")


s = open('C:/dev/masaha/app-b-lane-f/apps/api/src/app.ts', encoding='utf-8', newline='').read()
open('C:/dev/masaha/app-b-lane-f/apps/api/src/app.ts', 'w', encoding='utf-8', newline='').write(app(s))
print('ok')
