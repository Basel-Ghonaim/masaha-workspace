-- EC4: a generated year on masaha_b_test ONLY (the plan's §13 EC4). 300 spaces; 11 of them busy, each with
-- 2 000 customers, 500 fixed subscriptions, 9 000 visits, 3 000 check-ins and ≈ 10 000 payments over 365 days
-- (5 % voided, 2 % of the visits written off); 5 000 users; open data reports. Truncated after (ec4-truncate.sql).
\set ON_ERROR_STOP on
BEGIN;
INSERT INTO governorates (name_ar, name_en, updated_at) VALUES ('غزة', 'Gaza City', now()) ON CONFLICT DO NOTHING;
INSERT INTO areas (governorate_id, name_ar, name_en, updated_at)
  SELECT id, 'النصر', 'An-Nasr', now() FROM governorates WHERE name_ar = 'غزة' ON CONFLICT DO NOTHING;

INSERT INTO users (email, name, role, password_hash, created_at, updated_at)
  SELECT 'user' || g || '@example.com', 'User ' || g, 'USER', 'x', now() - (g % 365) * interval '1 day', now()
  FROM generate_series(1, 5000) g;

INSERT INTO spaces (slug, name_en, name_ar, address_ar, area_id, lat, lng, is_hidden, profile_updated_at, created_at, updated_at)
  SELECT 'space-' || g, 'Space ' || lpad(g::text, 3, '0'), 'مساحة ' || g, 'غزة',
         (SELECT id FROM areas WHERE name_ar = 'النصر' LIMIT 1), 31.5, 34.46, g % 17 = 0,
         now() - (g % 120) * interval '1 day', now(), now()
  FROM generate_series(1, 300) g;

-- An owner for the first 150 spaces (verified), the other 150 unverified.
INSERT INTO space_managers (space_id, user_id, role, created_at, updated_at)
  SELECT s.id, u.id, 'OWNER', now(), now()
  FROM spaces s JOIN users u ON u.email = 'user' || (s.id % 5000 + 1) || '@example.com'
  WHERE s.slug ~ '^space-' AND substring(s.slug FROM 7)::int <= 150;

INSERT INTO data_reports (space_id, user_id, field, status, created_at, updated_at)
  SELECT s.id, (SELECT min(id) FROM users), 'PRICES', 'OPEN',
         now() - g * interval '1 hour', now()
  FROM spaces s CROSS JOIN generate_series(1, 2) g WHERE s.slug ~ '^space-' AND (s.id + g) % 3 = 0;

CREATE TEMP TABLE busy AS
  SELECT id AS space_id, row_number() OVER (ORDER BY id) AS n FROM spaces WHERE slug ~ '^space-([1-9]|10|11)$';

INSERT INTO customers (space_id, name, created_at, updated_at)
  SELECT b.space_id, 'Customer ' || g, now() - (g % 365) * interval '1 day', now()
  FROM busy b CROSS JOIN generate_series(1, 2000) g;

INSERT INTO subscriptions (space_id, request_id, customer_id, name, billing, price_agorot, created_at, updated_at)
  SELECT c.space_id, gen_random_uuid(), c.id, 'Monthly', 'FIXED', 30000, now() - (c.id % 365) * interval '1 day', now()
  FROM (SELECT c.*, row_number() OVER (PARTITION BY space_id ORDER BY id) AS k FROM customers c
        WHERE space_id IN (SELECT space_id FROM busy)) c
  WHERE c.k <= 500;

CREATE TEMP TABLE cust AS
  SELECT id, space_id, row_number() OVER (PARTITION BY space_id ORDER BY id) AS k FROM customers;
CREATE INDEX ON cust (space_id, k);

-- 9 000 visits per busy space: 60 % of a customer, 40 % walk-ins; closed the same day; 1 % auto-closed unpaid.
INSERT INTO visits (space_id, request_id, customer_id, visitor_name, checked_in_at, checked_out_at, checkout_method,
                    charge_agorot, created_at, updated_at)
  SELECT b.space_id, gen_random_uuid(),
         CASE WHEN g % 5 < 3 THEN (SELECT id FROM cust WHERE cust.space_id = b.space_id AND cust.k = g % 2000 + 1) END,
         CASE WHEN g % 5 >= 3 THEN 'Walk-in ' || g END,
         d + interval '8 hours' + (g % 8) * interval '1 hour',
         d + interval '10 hours' + (g % 8) * interval '1 hour',
         CASE WHEN g % 100 = 0 THEN 'AUTO' ELSE 'MANUAL' END::"CheckOutMethod",
         CASE WHEN g % 100 = 0 AND g % 200 = 0 THEN NULL ELSE 1500 END,
         d + interval '8 hours', now()
  FROM busy b CROSS JOIN generate_series(1, 9000) g
  CROSS JOIN LATERAL (SELECT (date_trunc('day', now() AT TIME ZONE 'Asia/Gaza') - (g % 365) * interval '1 day') AT TIME ZONE 'Asia/Gaza' AS d) day;

-- 3 000 closed check-ins per busy space, on its subscriptions.
INSERT INTO check_ins (space_id, request_id, customer_id, subscription_id, checked_in_at, checked_out_at, checkout_method, created_at, updated_at)
  SELECT s.space_id, gen_random_uuid(), s.customer_id, s.id,
         d + interval '9 hours' + (g % 6) * interval '1 hour', d + interval '12 hours' + (g % 6) * interval '1 hour',
         'MANUAL', d + interval '9 hours', now()
  FROM (SELECT s.*, row_number() OVER (PARTITION BY space_id ORDER BY id) AS k FROM subscriptions s
        WHERE space_id IN (SELECT space_id FROM busy)) s
  CROSS JOIN generate_series(1, 6) g
  CROSS JOIN LATERAL (SELECT (date_trunc('day', now() AT TIME ZONE 'Asia/Gaza') - ((s.k * 7 + g) % 365) * interval '1 day') AT TIME ZONE 'Asia/Gaza' AS d) day;

-- Payments: each manual priced visit paid in full, except 2 % (written off below) and the auto-closed ones.
INSERT INTO payments (space_id, request_id, visit_id, amount_agorot, method, recorded_by_id, received_at, created_at)
  SELECT v.space_id, gen_random_uuid(), v.id, v.charge_agorot,
         CASE WHEN v.id % 4 = 0 THEN 'TRANSFER' ELSE 'CASH' END::"PaymentMethod",
         (SELECT min(id) FROM users) + (v.id % 3), v.checked_out_at, v.checked_out_at
  FROM visits v
  WHERE v.space_id IN (SELECT space_id FROM busy) AND v.checkout_method = 'MANUAL' AND v.charge_agorot IS NOT NULL
    AND v.id % 50 <> 0;
UPDATE visits SET written_off_at = checked_out_at, written_off_by_id = (SELECT min(id) FROM users), write_off_reason = 'Gone'
  WHERE space_id IN (SELECT space_id FROM busy) AND checkout_method = 'MANUAL' AND id % 50 = 0;
-- Two partial payments on each subscription.
INSERT INTO payments (space_id, request_id, subscription_id, amount_agorot, method, recorded_by_id, received_at, created_at)
  SELECT s.space_id, gen_random_uuid(), s.id, 10000, 'CASH', (SELECT min(id) FROM users), s.created_at + g * interval '3 days', now()
  FROM subscriptions s CROSS JOIN generate_series(1, 2) g WHERE s.space_id IN (SELECT space_id FROM busy);
-- 5 % voided.
UPDATE payments SET voided_at = received_at + interval '1 hour', voided_by_id = (SELECT min(id) FROM users), void_reason = 'Counted twice'
  WHERE id % 20 = 0;
COMMIT;
ANALYZE;
SELECT (SELECT count(*) FROM spaces) AS spaces, (SELECT count(*) FROM users) AS users,
       (SELECT count(*) FROM customers) AS customers, (SELECT count(*) FROM subscriptions) AS subscriptions,
       (SELECT count(*) FROM visits) AS visits, (SELECT count(*) FROM check_ins) AS check_ins,
       (SELECT count(*) FROM payments) AS payments, (SELECT count(*) FROM payments WHERE voided_at IS NOT NULL) AS voided;
