def sub(p, pairs):
    s = open(p, encoding='utf8', newline='').read()
    for a, b in pairs:
        assert s.count(a) == 1, (p, a)
        s = s.replace(a, b)
    open(p, 'w', encoding='utf8', newline='').write(s)

sub('src/modules/subscriptions/subscriptions.mapper.ts', [
    ("    dueAgorot: row.due_agorot,\n",
     "    // `bigint` in SQL; exact as a number within the price's bound (data model › Derived values).\n    dueAgorot: Number(row.due_agorot),\n"),
])
sub('src/modules/subscriptions/subscriptions.repository.ts', [
    ("  minutes_today: number;\n  due_agorot: number;\n}",
     "  minutes_today: number;\n  /** `bigint`, so no price within its bound overflows it (data model › Derived values). */\n  due_agorot: bigint;\n}"),
])
sub('src/modules/payments/payments.repository.ts', [
    ("""/**
 * Per customer: the debt, the sum of the positive balances (due − paid), an unpriced visit none; and
 * the credit, the sum of what was paid above the due, a usage-based subscription's only.
 */
const DEBT = Prisma.sql`coalesce(sum(greatest(due - paid, 0)), 0)::integer`;
const CREDIT = Prisma.sql`coalesce(sum(greatest(paid - due, 0)) FILTER (WHERE usage_based), 0)::integer`;""",
     """/**
 * Per customer: the debt, the sum of the positive balances (due − paid), an unpriced visit none; and
 * the credit, the sum of what was paid above the due, a usage-based subscription's only. Both
 * `bigint`, as a subscription's due is (data model › Derived values); each reader maps them through
 * `Number()`, exact within the price's bound.
 */
const DEBT = Prisma.sql`coalesce(sum(greatest(due - paid, 0)), 0)::bigint`;
const CREDIT = Prisma.sql`coalesce(sum(greatest(paid - due, 0)) FILTER (WHERE usage_based), 0)::bigint`;"""),
    ("""      const rows = await tx.$queryRaw<{ customer_id: number; debt: number; credit: number }[]>`""",
     """      const rows = await tx.$queryRaw<{ customer_id: number; debt: bigint; credit: bigint }[]>`"""),
    ("""        rows.map(({ customer_id, debt, credit }) => [customer_id, { debt, credit }]),""",
     """        rows.map(({ customer_id, debt, credit }) => [
          customer_id,
          { debt: Number(debt), credit: Number(credit) },
        ]),"""),
    ("""          customer_id: number;
          amount: number;
          total: number;""",
     """          customer_id: number;
          amount: bigint;
          total: number;"""),
    ("""          amountAgorot,
          oldest:""",
     """          amountAgorot: Number(amountAgorot),
          oldest:"""),
    ("""        { owed: number; owing: number; credit: number; crediting: number }[]""",
     """        { owed: bigint; owing: number; credit: bigint; crediting: number }[]"""),
    ("""        SELECT coalesce(sum(debt), 0)::integer AS owed,
               count(*) FILTER (WHERE debt > 0)::integer AS owing,
               coalesce(sum(credit), 0)::integer AS credit,""",
     """        SELECT coalesce(sum(debt), 0)::bigint AS owed,
               count(*) FILTER (WHERE debt > 0)::integer AS owing,
               coalesce(sum(credit), 0)::bigint AS credit,"""),
    ("""        owed: { agorot: row?.owed ?? 0, customers: row?.owing ?? 0 },
        credit: { agorot: row?.credit ?? 0, customers: row?.crediting ?? 0 },""",
     """        owed: { agorot: Number(row?.owed ?? 0), customers: row?.owing ?? 0 },
        credit: { agorot: Number(row?.credit ?? 0), customers: row?.crediting ?? 0 },"""),
    ("""          due: number | null;
          paid: number;
          created_at: Date;""",
     """          /** `bigint` for a subscription, as `subscription_usage` answers it. */
          due: bigint | number | null;
          paid: number;
          created_at: Date;"""),
    ("""        dueAgorot: due,
        paidAgorot: paid,""",
     """        dueAgorot: due === null ? null : Number(due),
        paidAgorot: paid,"""),
])
