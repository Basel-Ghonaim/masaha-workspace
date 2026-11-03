p = 'apps/api/src/modules/payments/payments.service.ts'
s = open(p, encoding='utf-8', newline='').read()

old_import = '''import {
  createPaymentsRepository,
  type ItemBalanceRow,'''
new_import = '''import {
  createPaymentsRepository,
  type BalancePageRow,
  type BalanceTotals,
  type ItemBalanceRow,'''
assert s.count(old_import) == 1
s = s.replace(old_import, new_import)
old_import2 = '''  type NewPayment,
  type VisitPaymentRow,
} from './payments.repository.ts';'''
assert s.count(old_import2) == 1
s = s.replace(old_import2, '''  type NewPayment,
  type UncollectedTotals,
  type VisitPaymentRow,
} from './payments.repository.ts';''')

anchor = '''    /**
     * Every item of one customer of the space at `at` — subscriptions and closed visits not written'''
new = '''    /**
     * A page of the space's customers who owe, or who are in credit, at `at`, by the one balance
     * rule (an archived customer's kept): the largest first, then by customer id; who owes with the
     * item still owing made first. In the caller's snapshot when given.
     */
    balancesPage(
      spaceId: number,
      state: 'OWES' | 'CREDIT',
      at: Date,
      { page, limit }: PaginationQuery,
      tx?: Tx,
    ): Promise<{ rows: BalancePageRow[]; total: number }> {
      return repository.balancesPage(
        spaceId,
        state,
        calendarOf(at),
        { skip: toSkip({ page, limit }), take: limit },
        tx,
      );
    },

    /**
     * The space's balances totalled at `at`: what is owed and by how many customers, what is held
     * in credit and by how many (Finance's totals; the owner's overview counts who owe).
     */
    balanceTotals(spaceId: number, at: Date, tx?: Tx): Promise<BalanceTotals> {
      return repository.balanceTotals(spaceId, calendarOf(at), tx);
    },

    /** The space's uncollected visits counted: all, what the priced ones owe, the unpriced apart. */
    uncollectedTotals(spaceId: number, tx?: Tx): Promise<UncollectedTotals> {
      return repository.uncollectedTotals(spaceId, tx);
    },

'''
assert s.count(anchor) == 1
s = s.replace(anchor, new + anchor)
open(p, 'w', encoding='utf-8', newline='').write(s)

p = 'apps/api/src/modules/payments/index.ts'
s = open(p, encoding='utf-8', newline='').read()
old = "export type { NewPayment } from './payments.repository.ts';"
assert s.count(old) == 1
s = s.replace(old, "export type {\n  BalancePageRow,\n  BalanceTotals,\n  NewPayment,\n  UncollectedTotals,\n} from './payments.repository.ts';")
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
