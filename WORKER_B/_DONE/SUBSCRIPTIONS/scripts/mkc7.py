"""Builds c7.json, the fix round's breaks, from the files as they are now."""
import io, json
REPO = 'C:/dev/masaha/app-b/'
R = 'apps/api/src/modules/payments/payments.repository.ts'
s = io.open(REPO + R, encoding='utf-8', newline='').read()
a = s.index('  return Prisma.sql`\n    SELECT \'SUBSCRIPTION\' AS kind')
b = s.index('}\n', s.index("${asked ? Prisma.sql`AND v.customer_id IN ${asked}` : Prisma.empty}`;", a))
current = s[a:b]
or_join = """  return Prisma.sql`
    WITH items AS (
      SELECT 'SUBSCRIPTION' AS kind, u.subscription_id AS id, u.customer_id, u.due_agorot AS due,
             u.usage_based, s.created_at
      FROM subscription_usage(${spaceId}, NULL::integer, ${today}::date, ${weekStart}::date) u
      JOIN subscriptions s ON s.id = u.subscription_id
      ${customerIds ? Prisma.sql`WHERE u.customer_id = ANY(${[...customerIds]}::integer[])` : Prisma.empty}
      UNION ALL
      SELECT 'VISIT', v.id, v.customer_id, v.charge_agorot, false, v.created_at
      FROM visits v
      WHERE v.space_id = ${spaceId} AND v.customer_id IS NOT NULL AND v.checked_out_at IS NOT NULL
        AND v.written_off_at IS NULL
        ${asked ? Prisma.sql`AND v.customer_id IN ${asked}` : Prisma.empty}
    ), paid AS (
      SELECT visit_id, subscription_id, sum(amount_agorot)::integer AS paid
      FROM payments WHERE space_id = ${spaceId} AND voided_at IS NULL
      GROUP BY visit_id, subscription_id
    )
    SELECT i.kind, i.id, i.customer_id, i.due, i.usage_based, i.created_at,
           coalesce(p.paid, 0) AS paid
    FROM items i
    LEFT JOIN paid p ON (i.kind = 'VISIT' AND p.visit_id = i.id)
                     OR (i.kind = 'SUBSCRIPTION' AND p.subscription_id = i.id)`;
"""
BT = 'src/modules/payments/balances.api.test.ts'
entries = [
 {"id": "F1-or", "file": R, "old": current, "new": or_join, "lane": "api",
  "test": "src/modules/desk/customers.api.test.ts", "name": "a payment on every item"},
 {"id": "F1-whole", "file": R, "old": "    ${customerIds ? Prisma.sql`WHERE u.customer_id = ANY(${[...customerIds]}::integer[])` : Prisma.empty}\n",
  "new": "", "lane": "api", "test": BT},
 {"id": "B32", "file": R, "old": "const DEBT = Prisma.sql`coalesce(sum(greatest(due - paid, 0)), 0)::integer`;",
  "new": "const DEBT = Prisma.sql`coalesce(sum(due - paid), 0)::integer`;", "lane": "api", "test": BT,
  "name": "a debt is the sum of positive balances"},
 {"id": "B33", "file": R, "old": "sum(greatest(paid - due, 0)) FILTER (WHERE usage_based), 0)",
  "new": "sum(greatest(paid - due, 0)), 0)", "lane": "api", "test": BT, "name": "credit is only"},
 {"id": "B34", "file": R, "old": "      WHERE visit_id = v.id AND voided_at IS NULL\n", "new": "      WHERE visit_id = v.id\n",
  "lane": "api", "test": BT, "name": "a voided payment counts for nothing"},
 {"id": "B34s", "file": R, "old": "      WHERE subscription_id = u.subscription_id AND voided_at IS NULL\n",
  "new": "      WHERE subscription_id = u.subscription_id\n", "lane": "api",
  "test": "src/modules/desk/customerFile.api.test.ts", "name": "answers the customer"},
 {"id": "B35", "file": R, "old": "      AND v.written_off_at IS NULL\n      ${asked", "new": "      ${asked",
  "lane": "api", "test": BT, "name": "a voided payment counts for nothing"},
 {"id": "B36b", "file": R, "old": "    WHERE v.space_id = ${spaceId} AND v.customer_id IS NOT NULL",
  "new": "    WHERE ${spaceId} > 0 AND v.customer_id IS NOT NULL", "lane": "api", "test": BT, "name": "the payment filter"},
 {"id": "B37", "file": R, "old": "ORDER BY created_at, kind <> 'VISIT', id`;", "new": "ORDER BY id`;",
  "lane": "api", "test": BT, "name": "itemBalances lists"},
 {"id": "B43", "file": "apps/api/src/modules/customers/customers.repository.ts",
  "old": "Prisma.sql`id IN (SELECT unnest(${[...ids]}::integer[]))`", "new": "Prisma.sql`id IN (${Prisma.join([...ids])})`",
  "lane": "api", "test": "src/modules/customers/customers.api.test.ts", "name": "70,000 ids"},
 {"id": "F2-any", "file": "apps/api/src/modules/customers/customers.repository.ts",
  "old": "Prisma.sql`id IN (SELECT unnest(${[...ids]}::integer[]))`", "new": "Prisma.sql`id = ANY(${[...ids]}::integer[])`",
  "lane": "api", "test": "src/modules/desk/customers.api.test.ts", "name": "20,000 ids is read as a set"},
]
json.dump(entries, open('C:/dev/masaha/workspace/WORKER_B/SUBSCRIPTIONS/scripts/c7.json', 'w', encoding='utf-8'), indent=1)
print('ok', len(entries))
