\echo '=== customerBalances (a page of 20)'
EXPLAIN (ANALYZE, BUFFERS, COSTS OFF, TIMING OFF, SUMMARY ON)
WITH balances AS (
    SELECT 'SUBSCRIPTION' AS kind, u.subscription_id AS id, u.customer_id, u.due_agorot AS due,
           u.usage_based, s.created_at, coalesce(p.paid, 0) AS paid
    FROM subscription_usage(:sid, NULL::integer, :today::date, :week::date) u
    JOIN subscriptions s ON s.id = u.subscription_id
    LEFT JOIN LATERAL (
      SELECT sum(amount_agorot)::integer AS paid FROM payments
      WHERE subscription_id = u.subscription_id AND voided_at IS NULL
    ) p ON true
    WHERE u.customer_id = ANY(:'page'::integer[])
    UNION ALL
    SELECT 'VISIT', v.id, v.customer_id, v.charge_agorot, false, v.created_at, coalesce(p.paid, 0)
    FROM visits v
    LEFT JOIN LATERAL (
      SELECT sum(amount_agorot)::integer AS paid FROM payments
      WHERE visit_id = v.id AND voided_at IS NULL
    ) p ON true
    WHERE v.space_id = :sid AND v.customer_id IS NOT NULL AND v.checked_out_at IS NOT NULL
      AND v.written_off_at IS NULL
      AND v.customer_id IN (SELECT unnest(:'page'::integer[])))
SELECT customer_id, coalesce(sum(greatest(due - paid, 0)), 0)::integer AS debt,
       coalesce(sum(greatest(paid - due, 0)) FILTER (WHERE usage_based), 0)::integer AS credit
FROM balances GROUP BY customer_id;
\echo '=== itemBalances (one customer)'
EXPLAIN (ANALYZE, BUFFERS, COSTS OFF, TIMING OFF, SUMMARY ON)
WITH balances AS (
    SELECT 'SUBSCRIPTION' AS kind, u.subscription_id AS id, u.customer_id, u.due_agorot AS due,
           u.usage_based, s.created_at, coalesce(p.paid, 0) AS paid
    FROM subscription_usage(:sid, NULL::integer, :today::date, :week::date) u
    JOIN subscriptions s ON s.id = u.subscription_id
    LEFT JOIN LATERAL (
      SELECT sum(amount_agorot)::integer AS paid FROM payments
      WHERE subscription_id = u.subscription_id AND voided_at IS NULL
    ) p ON true
    WHERE u.customer_id = ANY(ARRAY[:one]::integer[])
    UNION ALL
    SELECT 'VISIT', v.id, v.customer_id, v.charge_agorot, false, v.created_at, coalesce(p.paid, 0)
    FROM visits v
    LEFT JOIN LATERAL (
      SELECT sum(amount_agorot)::integer AS paid FROM payments
      WHERE visit_id = v.id AND voided_at IS NULL
    ) p ON true
    WHERE v.space_id = :sid AND v.customer_id IS NOT NULL AND v.checked_out_at IS NOT NULL
      AND v.written_off_at IS NULL
      AND v.customer_id IN (SELECT unnest(ARRAY[:one]::integer[])))
SELECT kind, id, due, paid, created_at FROM balances ORDER BY created_at, kind <> 'VISIT', id;
