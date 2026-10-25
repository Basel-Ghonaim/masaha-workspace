\set today '\'2026-10-21\''
\set week '\'2026-10-17\''
SELECT array_agg(id ORDER BY id) AS page FROM (SELECT id FROM customers WHERE space_id = :sid ORDER BY name LIMIT 20) x \gset
SELECT min(id) AS one FROM customers WHERE space_id = :sid \gset
