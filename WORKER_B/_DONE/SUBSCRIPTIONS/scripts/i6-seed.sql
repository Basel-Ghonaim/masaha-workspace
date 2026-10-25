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
