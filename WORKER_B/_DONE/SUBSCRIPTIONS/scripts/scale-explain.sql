-- After scale-seed.sql, in the same transaction: the three balance queries, today's form (the OR join over the
-- whole space) against the new form (LATERAL per item on the payments' indexes, the customers asked passed in).
\set today '\'2026-10-21\''
\set week '\'2026-10-17\''
SELECT array_agg(id ORDER BY id) AS page FROM (SELECT id FROM customers WHERE space_id = :sid ORDER BY name LIMIT 20) x \gset
SELECT min(id) AS one FROM customers WHERE space_id = :sid \gset

\echo '=== OLD customerBalances (a page of 20)'
EXPLAIN (ANALYZE, BUFFERS, COSTS OFF, TIMING OFF, SUMMARY ON)
WITH balances AS (
  WITH items AS (
    SELECT 'SUBSCRIPTION' AS kind, u.subscription_id AS id, u.customer_id, u.due_agorot AS due, u.usage_based, s.created_at
    FROM subscription_usage(:sid, NULL::integer, :today::date, :week::date) u JOIN subscriptions s ON s.id = u.subscription_id
    UNION ALL
    SELECT 'VISIT', v.id, v.customer_id, v.charge_agorot, false, v.created_at FROM visits v
    WHERE v.space_id = :sid AND v.customer_id IS NOT NULL AND v.checked_out_at IS NOT NULL AND v.written_off_at IS NULL
  ), paid AS (
    SELECT visit_id, subscription_id, sum(amount_agorot)::integer AS paid FROM payments
    WHERE space_id = :sid AND voided_at IS NULL GROUP BY visit_id, subscription_id
  )
  SELECT i.kind, i.id, i.customer_id, i.due, i.usage_based, i.created_at, coalesce(p.paid, 0) AS paid
  FROM items i LEFT JOIN paid p ON (i.kind = 'VISIT' AND p.visit_id = i.id) OR (i.kind = 'SUBSCRIPTION' AND p.subscription_id = i.id)
)
SELECT customer_id, coalesce(sum(greatest(due - paid, 0)), 0)::integer AS debt
FROM balances WHERE customer_id = ANY(:'page'::integer[]) GROUP BY customer_id;

\echo '=== NEW customerBalances (a page of 20)'
EXPLAIN (ANALYZE, BUFFERS, COSTS OFF, TIMING OFF, SUMMARY ON)
WITH asked AS (SELECT unnest(:'page'::integer[]) AS id),
items AS (
  SELECT u.customer_id, u.due_agorot AS due, u.usage_based, coalesce(p.paid, 0) AS paid
  FROM asked c
  CROSS JOIN LATERAL subscription_usage(:sid, c.id, :today::date, :week::date) u
  LEFT JOIN LATERAL (SELECT sum(amount_agorot)::integer AS paid FROM payments
                     WHERE subscription_id = u.subscription_id AND voided_at IS NULL) p ON true
  UNION ALL
  SELECT v.customer_id, v.charge_agorot, false, coalesce(p.paid, 0)
  FROM visits v
  LEFT JOIN LATERAL (SELECT sum(amount_agorot)::integer AS paid FROM payments
                     WHERE visit_id = v.id AND voided_at IS NULL) p ON true
  WHERE v.space_id = :sid AND v.customer_id IN (SELECT id FROM asked)
    AND v.checked_out_at IS NOT NULL AND v.written_off_at IS NULL
)
SELECT customer_id, coalesce(sum(greatest(due - paid, 0)), 0)::integer AS debt FROM items GROUP BY customer_id;

\echo '=== OLD customerIdsByPayment (OWES)'
EXPLAIN (ANALYZE, BUFFERS, COSTS OFF, TIMING OFF, SUMMARY ON)
WITH balances AS (
  WITH items AS (
    SELECT 'SUBSCRIPTION' AS kind, u.subscription_id AS id, u.customer_id, u.due_agorot AS due, u.usage_based, s.created_at
    FROM subscription_usage(:sid, NULL::integer, :today::date, :week::date) u JOIN subscriptions s ON s.id = u.subscription_id
    UNION ALL
    SELECT 'VISIT', v.id, v.customer_id, v.charge_agorot, false, v.created_at FROM visits v
    WHERE v.space_id = :sid AND v.customer_id IS NOT NULL AND v.checked_out_at IS NOT NULL AND v.written_off_at IS NULL
  ), paid AS (
    SELECT visit_id, subscription_id, sum(amount_agorot)::integer AS paid FROM payments
    WHERE space_id = :sid AND voided_at IS NULL GROUP BY visit_id, subscription_id
  )
  SELECT i.kind, i.id, i.customer_id, i.due, i.usage_based, i.created_at, coalesce(p.paid, 0) AS paid
  FROM items i LEFT JOIN paid p ON (i.kind = 'VISIT' AND p.visit_id = i.id) OR (i.kind = 'SUBSCRIPTION' AND p.subscription_id = i.id)
)
SELECT customer_id FROM balances GROUP BY customer_id HAVING coalesce(sum(greatest(due - paid, 0)), 0) > 0;

\echo '=== NEW customerIdsByPayment (OWES)'
EXPLAIN (ANALYZE, BUFFERS, COSTS OFF, TIMING OFF, SUMMARY ON)
WITH items AS (
  SELECT u.customer_id, u.due_agorot AS due, u.usage_based, coalesce(p.paid, 0) AS paid
  FROM subscription_usage(:sid, NULL::integer, :today::date, :week::date) u
  LEFT JOIN LATERAL (SELECT sum(amount_agorot)::integer AS paid FROM payments
                     WHERE subscription_id = u.subscription_id AND voided_at IS NULL) p ON true
  UNION ALL
  SELECT v.customer_id, v.charge_agorot, false, coalesce(p.paid, 0)
  FROM visits v
  LEFT JOIN LATERAL (SELECT sum(amount_agorot)::integer AS paid FROM payments
                     WHERE visit_id = v.id AND voided_at IS NULL) p ON true
  WHERE v.space_id = :sid AND v.customer_id IS NOT NULL AND v.checked_out_at IS NOT NULL AND v.written_off_at IS NULL
)
SELECT customer_id FROM items GROUP BY customer_id HAVING coalesce(sum(greatest(due - paid, 0)), 0) > 0;

\echo '=== subscription_usage(NULL) filtered after the call: is the filter pushed inside?'
EXPLAIN (COSTS OFF)
SELECT * FROM subscription_usage(:sid, NULL::integer, :today::date, :week::date) u WHERE u.customer_id = ANY(:'page'::integer[]);
