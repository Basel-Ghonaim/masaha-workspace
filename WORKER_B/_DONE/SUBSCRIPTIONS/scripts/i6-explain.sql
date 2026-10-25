BEGIN;
-- The review's scale (finding 1), in one transaction on masaha_b_test, rolled back by the caller's script:
-- 2,000 customers, each with a fixed subscription paid in part; 40,000 walk-in visits paid in full.
\timing on
INSERT INTO users (email, name, password_hash, updated_at) VALUES ('scale@example.com', 'S', 'x', now()) RETURNING id AS uid \gset
INSERT INTO governorates (name_ar, name_en, updated_at) VALUES ('غزة-س', 'Scale', now()) RETURNING id AS gid \gset
INSERT INTO areas (governorate_id, name_ar, name_en, updated_at) VALUES (:gid, 'س', 'S', now()) RETURNING id AS aid \gset
INSERT INTO spaces (slug, name_en, name_ar, address_ar, area_id, lat, lng, updated_at)
  VALUES ('scale-space', 'S', 'S', 'S', :aid, 31.5, 34.4, now()) RETURNING id AS sid \gset
INSERT INTO customers (space_id, name, updated_at)
  SELECT :sid, 'Customer ' || lpad(n::text, 5, '0'), now() FROM generate_series(1, 2000) n;
ANALYZE customers;
INSERT INTO subscriptions (space_id, customer_id, name, billing, price_agorot, updated_at)
  SELECT space_id, id, 'Monthly', 'FIXED', 30000, now() FROM customers WHERE space_id = :sid;
ANALYZE subscriptions;
INSERT INTO payments (space_id, subscription_id, request_id, amount_agorot, method, recorded_by_id)
  SELECT space_id, id, gen_random_uuid(), 10000, 'CASH', :uid FROM subscriptions WHERE space_id = :sid;
INSERT INTO visits (space_id, request_id, visitor_name, checked_in_at, checked_out_at, checkout_method, charge_agorot, updated_at)
  SELECT :sid, gen_random_uuid(), 'Walk-in', now() - interval '3 hours', now() - interval '1 hour', 'MANUAL', 1500, now()
  FROM generate_series(1, 30000);
ANALYZE visits;
ANALYZE payments;
INSERT INTO visits (space_id, request_id, visitor_name, customer_id, checked_in_at, checked_out_at, checkout_method, charge_agorot, updated_at)
  SELECT c.space_id, gen_random_uuid(), c.name, c.id, now() - (k || ' days')::interval - interval '3 hours',
         now() - (k || ' days')::interval - interval '1 hour', 'MANUAL', 1500, now()
  FROM customers c CROSS JOIN generate_series(1, 5) k WHERE c.space_id = :sid;
ANALYZE visits;
INSERT INTO payments (space_id, visit_id, request_id, amount_agorot, method, recorded_by_id)
  SELECT space_id, id, gen_random_uuid(), 500, 'CASH', :uid FROM visits WHERE space_id = :sid AND customer_id IS NOT NULL;
ANALYZE payments;
\set today '\'2026-10-21\''
\set week '\'2026-10-17\''
SELECT array_agg(id ORDER BY id) AS page FROM (SELECT id FROM customers WHERE space_id = :sid ORDER BY name LIMIT 20) x \gset
SELECT min(id) AS one FROM customers WHERE space_id = :sid \gset
\echo '##### BEFORE'
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
\echo '##### THE INDEX'
CREATE INDEX "visits_customer_id_closed_idx" ON "visits" ("customer_id") WHERE "checked_out_at" IS NOT NULL;
ANALYZE visits;
\echo '##### AFTER'
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
ROLLBACK;
