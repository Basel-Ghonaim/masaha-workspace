p = 'src/modules/payments/payments.repository.ts'
s = open(p, encoding='utf-8', newline='').read()

# 1. the uncollected fragment, one function, before the repository
anchor = "/**\n * The `payments` table, the ledger of ADR 0010."
frag = '''/**
 * The space's uncollected visits (data model › Uncollected visits), as a `FROM`: closed by the auto
 * check-out, or closed by hand, priced, with no customer (only a void leaves one owing), not written
 * off, not settled (balance > 0, or no charge yet); each joined to what was paid on it, voided
 * payments left out (`p.paid`). The one rule the desk's list and its totals both read.
 */
function uncollectedOf(spaceId: number) {
  return Prisma.sql`
    FROM visits v
    LEFT JOIN (
      SELECT visit_id, sum(amount_agorot)::integer AS paid FROM payments
      WHERE space_id = ${spaceId} AND visit_id IS NOT NULL AND voided_at IS NULL
      GROUP BY visit_id
    ) p ON p.visit_id = v.id
    WHERE v.space_id = ${spaceId} AND v.checked_out_at IS NOT NULL
      AND (v.checkout_method = 'AUTO' OR (v.customer_id IS NULL AND v.charge_agorot IS NOT NULL))
      AND v.written_off_at IS NULL
      AND (v.charge_agorot IS NULL OR v.charge_agorot - coalesce(p.paid, 0) > 0)`;
}

/** A customer's balance on a page of who owes or is in credit, and the oldest item still owing. */
export interface BalancePageRow {
  customerId: number;
  amountAgorot: number;
  /** Who owes only: the item still owing made first, a visit before a subscription, then by id. */
  oldest: { kind: 'VISIT' | 'SUBSCRIPTION'; id: number; createdAt: Date } | null;
}

/** A space's balances totalled: what is owed and by how many customers, and the same of credit. */
export interface BalanceTotals {
  owed: { agorot: number; customers: number };
  credit: { agorot: number; customers: number };
}

/** A space's uncollected visits counted: all, what the priced ones still owe, the unpriced apart. */
export interface UncollectedTotals {
  visits: number;
  owedAgorot: number;
  unpriced: number;
}

'''
assert s.count(anchor) == 1
s = s.replace(anchor, frag + anchor)

# 2. uncollectedPage reads the fragment
start_marker = "      const uncollected = Prisma.sql`\n        FROM visits v"
end_marker = "(v.charge_agorot IS NULL OR v.charge_agorot - coalesce(p.paid, 0) > 0)`;\n"
old_start = s.index(start_marker)
old_end = s.index(end_marker, old_start) + len(end_marker)
s = s[:old_start] + "      const uncollected = uncollectedOf(spaceId);\n" + s[old_end:]
old_doc = '''    /**
     * A page of the space's uncollected visits (data model › Uncollected visits): closed by the auto
     * check-out, or closed by hand, priced, with no customer (only a void leaves one owing), not
     * written off, not settled (balance > 0, or no charge yet), the latest closed first, then by id;
     * each with what was paid, voided payments left out; and how many there are.'''
assert s.count(old_doc) == 1
s = s.replace(old_doc, '''    /**
     * A page of the space's uncollected visits (`uncollectedOf`), the latest closed first, then by
     * id; each with what was paid, voided payments left out; and how many there are.''')

# 3. the new functions, after customerIdsByPayment
anchor2 = "    /**\n     * Every item of one customer of the space, with its due and what was paid, on these days: the"
new = '''    /**
     * A page of the space's customers who owe, or who are in credit, on these days, by the one
     * balance rule (`balancesOf`, every customer, an archived one's kept): the largest first, then by
     * customer id; who owes with the item still owing made first; and how many there are, counted
     * over the same balances (`count(*) OVER ()`; counted apart only past the last page).
     */
    async balancesPage(
      spaceId: number,
      state: 'OWES' | 'CREDIT',
      now: Now,
      { skip, take }: { skip: number; take: number },
      tx: Tx = prisma,
    ): Promise<{ rows: BalancePageRow[]; total: number }> {
      const amount = state === 'OWES' ? DEBT : CREDIT;
      const rows = await tx.$queryRaw<
        {
          customer_id: number;
          amount: number;
          total: number;
          kind: 'VISIT' | 'SUBSCRIPTION' | null;
          item_id: number | null;
          created_at: Date | null;
        }[]
      >`
        WITH balances AS (${balancesOf(spaceId, null, now)}),
        page AS (
          SELECT customer_id, ${amount} AS amount, count(*) OVER ()::integer AS total
          FROM balances GROUP BY customer_id HAVING ${amount} > 0
          ORDER BY amount DESC, customer_id LIMIT ${take} OFFSET ${skip}
        ),
        oldest AS (
          SELECT DISTINCT ON (b.customer_id) b.customer_id, b.kind, b.id, b.created_at
          FROM balances b JOIN page ON page.customer_id = b.customer_id
          WHERE ${state === 'OWES'} AND b.due - b.paid > 0
          ORDER BY b.customer_id, b.created_at, b.kind <> 'VISIT', b.id
        )
        SELECT page.customer_id, page.amount, page.total, o.kind, o.id AS item_id, o.created_at
        FROM page LEFT JOIN oldest o ON o.customer_id = page.customer_id
        ORDER BY page.amount DESC, page.customer_id`;
      const total =
        rows[0]?.total ??
        (skip === 0 ? 0 : await countOwing(tx, spaceId, amount, now));
      return {
        rows: rows.map(({ customer_id, amount: amountAgorot, kind, item_id, created_at }) => ({
          customerId: customer_id,
          amountAgorot,
          oldest:
            kind && item_id !== null && created_at
              ? { kind, id: item_id, createdAt: created_at }
              : null,
        })),
        total,
      };
    },

    /**
     * The space's balances totalled on these days, by the one balance rule, per customer then
     * summed: what is owed and how many owe; what is held in credit and how many hold it. A
     * customer may be in both.
     */
    async balanceTotals(spaceId: number, now: Now, tx: Tx = prisma): Promise<BalanceTotals> {
      const [row] = await tx.$queryRaw<
        { owed: number; owing: number; credit: number; crediting: number }[]
      >`
        WITH balances AS (${balancesOf(spaceId, null, now)}),
        customers AS (
          SELECT ${DEBT} AS debt, ${CREDIT} AS credit FROM balances GROUP BY customer_id
        )
        SELECT coalesce(sum(debt), 0)::integer AS owed,
               count(*) FILTER (WHERE debt > 0)::integer AS owing,
               coalesce(sum(credit), 0)::integer AS credit,
               count(*) FILTER (WHERE credit > 0)::integer AS crediting
        FROM customers`;
      return {
        owed: { agorot: row?.owed ?? 0, customers: row?.owing ?? 0 },
        credit: { agorot: row?.credit ?? 0, customers: row?.crediting ?? 0 },
      };
    },

    /**
     * The space's uncollected visits counted (`uncollectedOf`): how many, what the priced ones still
     * owe, and how many have no charge yet. One statement.
     */
    async uncollectedTotals(spaceId: number, tx: Tx = prisma): Promise<UncollectedTotals> {
      const [row] = await tx.$queryRaw<UncollectedTotals[]>`
        SELECT count(*)::integer AS visits,
               coalesce(sum(v.charge_agorot - coalesce(p.paid, 0)), 0)::integer AS "owedAgorot",
               count(*) FILTER (WHERE v.charge_agorot IS NULL)::integer AS unpriced
        ${uncollectedOf(spaceId)}`;
      return row ?? { visits: 0, owedAgorot: 0, unpriced: 0 };
    },

'''
assert s.count(anchor2) == 1
s = s.replace(anchor2, new + anchor2)

# 4. the count past the last page, beside the balance sums
anchor3 = "/**\n * The `payments` table, the ledger of ADR 0010."
helper = '''/** How many of the space's customers hold a positive `amount` (`DEBT` or `CREDIT`) on these days. */
async function countOwing(tx: Tx, spaceId: number, amount: Prisma.Sql, now: Now): Promise<number> {
  const [row] = await tx.$queryRaw<{ total: number }[]>`
    WITH balances AS (${balancesOf(spaceId, null, now)})
    SELECT count(*)::integer AS total FROM (
      SELECT customer_id FROM balances GROUP BY customer_id HAVING ${amount} > 0
    ) holding`;
  return row?.total ?? 0;
}

'''
s = s.replace(anchor3, helper + anchor3)
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
