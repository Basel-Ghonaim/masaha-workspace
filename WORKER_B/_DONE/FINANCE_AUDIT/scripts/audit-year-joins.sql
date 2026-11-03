-- FINANCE_AUDIT PR 1, §12.2 check 4: the audit reader's statements on a generated year.
-- masaha_b_test only (the API lane empties it before each file); truncated again at the end.
\set ON_ERROR_STOP on
\timing off
TRUNCATE TABLE audit_logs, space_managers, visits, customers, spaces, areas, governorates, users RESTART IDENTITY CASCADE;

INSERT INTO governorates (name_ar, name_en, updated_at) VALUES ('غزة', 'Gaza City', now());
INSERT INTO areas (governorate_id, name_ar, name_en, updated_at) VALUES (1, 'النصر', 'An-Nasr', now());
-- Space 1 is the busy one; 2..11 the others.
INSERT INTO spaces (slug, name_en, name_ar, address_ar, area_id, lat, lng, updated_at)
SELECT 'space-' || g, CASE WHEN g = 1 THEN 'Focus Hub' ELSE 'Hub ' || g END,
       CASE WHEN g = 1 THEN 'فوكس هاب' ELSE NULL END, 'غزة', 1, 31.5, 34.46, now()
FROM generate_series(1, 11) g;
-- Users 1 (owner), 2..4 (reception), 5 (admin), 6..15 (the other spaces' owners).
INSERT INTO users (email, name, role, password_hash, updated_at)
SELECT 'u' || g || '@example.com',
       CASE WHEN g = 1 THEN 'أحمد سالم' WHEN g = 5 THEN 'Rami' ELSE 'User ' || g END,
       CASE WHEN g = 5 THEN 'ADMIN'::"Role" WHEN g = 1 OR g > 5 THEN 'OWNER'::"Role" ELSE 'USER'::"Role" END, 'x',
       now()
FROM generate_series(1, 15) g;
INSERT INTO space_managers (space_id, user_id, role, updated_at) VALUES
  (1, 1, 'OWNER', now()), (1, 2, 'RECEPTION', now()), (1, 3, 'RECEPTION', now()), (1, 4, 'RECEPTION', now());
INSERT INTO space_managers (space_id, user_id, role, updated_at)
SELECT g, g + 4, 'OWNER', now() FROM generate_series(2, 11) g;
INSERT INTO customers (space_id, name, updated_at)
SELECT 1, 'زبون ' || g, now() FROM generate_series(1, 500) g;
INSERT INTO visits (space_id, request_id, visitor_name, updated_at)
SELECT 1, gen_random_uuid(), 'زائر ' || g, now() FROM generate_series(1, 3000) g;

-- A desk's mix: 95 % visit, check-in and payment actions, 5 % platform ones.
CREATE TEMP TABLE mix (n integer, action text, entity_type text);
INSERT INTO mix VALUES
  (0, 'visit.checkedIn', 'visit'), (1, 'visit.checkedOut', 'visit'), (2, 'checkIn.checkedIn', 'checkIn'),
  (3, 'checkIn.checkedOut', 'checkIn'), (4, 'payment.recorded', 'payment'), (5, 'customer.created', 'customer'),
  (6, 'visit.checkedIn', 'visit'), (7, 'payment.recorded', 'payment'), (8, 'checkIn.checkedIn', 'checkIn'),
  (9, 'visit.checkedOut', 'visit'), (10, 'payment.recorded', 'payment'), (11, 'visit.checkedIn', 'visit'),
  (12, 'checkIn.checkedOut', 'checkIn'), (13, 'visit.checkedOut', 'visit'), (14, 'payment.recorded', 'payment'),
  (15, 'customer.edited', 'customer'), (16, 'visit.checkedIn', 'visit'), (17, 'visit.checkedOut', 'visit'),
  (18, 'checkIn.checkedIn', 'checkIn'), (19, 'space.profileEdited', 'space');

INSERT INTO audit_logs (actor_id, action, entity_type, entity_id, space_id, after, created_at)
SELECT CASE WHEN g % 50 = 0 THEN NULL WHEN m.action LIKE 'space.%' THEN 5 ELSE 1 + g % 4 END,
       m.action, m.entity_type,
       CASE m.entity_type WHEN 'visit' THEN 1 + g % 3000 WHEN 'customer' THEN 1 + g % 500
         WHEN 'space' THEN 1 ELSE g END,
       1, jsonb_build_object('amountAgorot', g % 9000),
       now() - (random() * interval '365 days')
FROM generate_series(1, 36000) g JOIN mix m ON m.n = g % 20;

INSERT INTO audit_logs (actor_id, action, entity_type, entity_id, space_id, after, created_at)
SELECT CASE WHEN m.action LIKE 'space.%' THEN 5 ELSE 6 + g % 10 END,
       m.action, m.entity_type, CASE WHEN m.entity_type = 'space' THEN 2 + g % 10 ELSE g END,
       2 + g % 10, jsonb_build_object('amountAgorot', g % 9000),
       now() - (random() * interval '365 days')
FROM generate_series(1, 300000) g JOIN mix m ON m.n = g % 20;

-- The platform's own: accounts and lookups, naming no space.
INSERT INTO audit_logs (actor_id, action, entity_type, entity_id, space_id, created_at)
SELECT 5, CASE WHEN g % 2 = 0 THEN 'user.created' ELSE 'area.edited' END,
       CASE WHEN g % 2 = 0 THEN 'user' ELSE 'area' END, CASE WHEN g % 2 = 0 THEN 1 + g % 15 ELSE 1 END,
       NULL, now() - (random() * interval '365 days')
FROM generate_series(1, 1000) g;

ANALYZE audit_logs; ANALYZE users; ANALYZE spaces; ANALYZE space_managers; ANALYZE customers; ANALYZE visits;
SELECT count(*) AS entries, pg_size_pretty(pg_total_relation_size('audit_logs')) AS size FROM audit_logs;

\set since '(((date_trunc(''day'', now() AT TIME ZONE ''Asia/Gaza'') - interval ''29 days'') AT TIME ZONE ''Asia/Gaza''))'
\set actor_joins 'LEFT JOIN "space_managers" sm ON sm."space_id" = a."space_id" AND sm."user_id" = a."actor_id" LEFT JOIN "users" au ON au."id" = a."actor_id"'
\set target_join 'LEFT JOIN LATERAL (SELECT s."name_en" AS name, s."name_ar" AS name_ar, s."deleted_at" IS NOT NULL AS deleted FROM "spaces" s WHERE a."entity_type" = ''space'' AND s."id" = a."entity_id" UNION ALL SELECT u."name", NULL, false FROM "users" u WHERE a."entity_type" = ''user'' AND u."id" = a."entity_id" UNION ALL SELECT g."name_en", g."name_ar", false FROM "governorates" g WHERE a."entity_type" = ''governorate'' AND g."id" = a."entity_id" UNION ALL SELECT ar."name_en", ar."name_ar", false FROM "areas" ar WHERE a."entity_type" = ''area'' AND ar."id" = a."entity_id" UNION ALL SELECT am."name_en", am."name_ar", false FROM "amenities" am WHERE a."entity_type" = ''amenity'' AND am."id" = a."entity_id" UNION ALL SELECT c."name", NULL, false FROM "customers" c WHERE a."entity_type" = ''customer'' AND c."id" = a."entity_id" UNION ALL SELECT su."name", NULL, false FROM "subscriptions" su WHERE a."entity_type" = ''subscription'' AND su."id" = a."entity_id" UNION ALL SELECT p."name", NULL, false FROM "packages" p WHERE a."entity_type" = ''package'' AND p."id" = a."entity_id" UNION ALL SELECT coalesce(v."visitor_name", vc."name"), NULL, false FROM "visits" v LEFT JOIN "customers" vc ON vc."id" = v."customer_id" WHERE a."entity_type" = ''visit'' AND v."id" = a."entity_id" UNION ALL SELECT cc."name", NULL, false FROM "check_ins" ci JOIN "customers" cc ON cc."id" = ci."customer_id" WHERE a."entity_type" = ''checkIn'' AND ci."id" = a."entity_id" UNION ALL SELECT NULL, NULL, an."deleted_at" IS NOT NULL FROM "announcements" an WHERE a."entity_type" = ''announcement'' AND an."id" = a."entity_id") t ON true'
\set cols 'a."id", a."created_at", a."action", a."entity_type", a."entity_id", a."before", a."after", a."actor_id", t.name, t.name_ar, t.deleted'
\set q 'strpos(masaha_search_text(concat_ws('' '', t.name, t.name_ar)), masaha_search_text(''زبون 42'')) > 0'
\set qa 'strpos(masaha_search_text(concat_ws('' '', t.name, t.name_ar, es."name_en", es."name_ar")), masaha_search_text(''hub 7'')) > 0'
\set platform '(a."action" = ANY(ARRAY[''space.created'',''space.profileEdited'',''space.hoursEdited'',''space.pricesEdited'',''space.amenitiesEdited'',''space.contactsEdited'',''space.profileConfirmed'',''space.hoursConfirmed'',''space.pricesConfirmed'',''space.amenitiesConfirmed'',''space.contactsConfirmed'',''space.photoAdded'',''space.photoRemoved'',''space.photosReordered'',''space.hidden'',''space.unhidden'',''space.deleted'',''space.restored'',''space.ownerLinked'',''space.ownerUnlinked'',''governorate.added'',''governorate.edited'',''governorate.hidden'',''governorate.restored'',''area.added'',''area.edited'',''area.hidden'',''area.restored'',''amenity.added'',''amenity.edited'',''amenity.hidden'',''amenity.restored'',''dataReport.resolved'',''dataReport.dismissed'']::text[]) OR (a."action" = ANY(ARRAY[''user.created'',''user.roleChanged'',''user.suspended'',''user.unsuspended'',''user.temporaryPasswordIssued'',''user.temporaryPasswordHandedOver'',''user.emailChanged'']::text[]) AND a."space_id" IS NULL))'


\set ON_ERROR_STOP on
\set since '(((date_trunc(''day'', now() AT TIME ZONE ''Asia/Gaza'') - interval ''29 days'') AT TIME ZONE ''Asia/Gaza''))'
\set actor_joins 'LEFT JOIN "space_managers" sm ON sm."space_id" = a."space_id" AND sm."user_id" = a."actor_id" LEFT JOIN "users" au ON au."id" = a."actor_id"'
\set target_join 'LEFT JOIN LATERAL (SELECT s."name_en" AS name, s."name_ar" AS name_ar, s."deleted_at" IS NOT NULL AS deleted FROM "spaces" s WHERE a."entity_type" = ''space'' AND s."id" = a."entity_id" UNION ALL SELECT u."name", NULL, false FROM "users" u WHERE a."entity_type" = ''user'' AND u."id" = a."entity_id" UNION ALL SELECT g."name_en", g."name_ar", false FROM "governorates" g WHERE a."entity_type" = ''governorate'' AND g."id" = a."entity_id" UNION ALL SELECT ar."name_en", ar."name_ar", false FROM "areas" ar WHERE a."entity_type" = ''area'' AND ar."id" = a."entity_id" UNION ALL SELECT am."name_en", am."name_ar", false FROM "amenities" am WHERE a."entity_type" = ''amenity'' AND am."id" = a."entity_id" UNION ALL SELECT c."name", NULL, false FROM "customers" c WHERE a."entity_type" = ''customer'' AND c."id" = a."entity_id" UNION ALL SELECT su."name", NULL, false FROM "subscriptions" su WHERE a."entity_type" = ''subscription'' AND su."id" = a."entity_id" UNION ALL SELECT p."name", NULL, false FROM "packages" p WHERE a."entity_type" = ''package'' AND p."id" = a."entity_id" UNION ALL SELECT coalesce(v."visitor_name", vc."name"), NULL, false FROM "visits" v LEFT JOIN "customers" vc ON vc."id" = v."customer_id" WHERE a."entity_type" = ''visit'' AND v."id" = a."entity_id" UNION ALL SELECT cc."name", NULL, false FROM "check_ins" ci JOIN "customers" cc ON cc."id" = ci."customer_id" WHERE a."entity_type" = ''checkIn'' AND ci."id" = a."entity_id" UNION ALL SELECT NULL, NULL, an."deleted_at" IS NOT NULL FROM "announcements" an WHERE a."entity_type" = ''announcement'' AND an."id" = a."entity_id") t ON true'
\set cols 'a."id", a."created_at", a."action", a."entity_type", a."entity_id", a."before", a."after", a."actor_id", t.name, t.name_ar, t.deleted'
\set q 'strpos(masaha_search_text(concat_ws('' '', t.name, t.name_ar)), masaha_search_text(''زبون 42'')) > 0'
\set qa 'strpos(masaha_search_text(concat_ws('' '', t.name, t.name_ar, es."name_en", es."name_ar")), masaha_search_text(''hub 7'')) > 0'
\set platform '(a."action" = ANY(ARRAY[''space.created'',''space.profileEdited'',''space.hoursEdited'',''space.pricesEdited'',''space.amenitiesEdited'',''space.contactsEdited'',''space.profileConfirmed'',''space.hoursConfirmed'',''space.pricesConfirmed'',''space.amenitiesConfirmed'',''space.contactsConfirmed'',''space.photoAdded'',''space.photoRemoved'',''space.photosReordered'',''space.hidden'',''space.unhidden'',''space.deleted'',''space.restored'',''space.ownerLinked'',''space.ownerUnlinked'',''governorate.added'',''governorate.edited'',''governorate.hidden'',''governorate.restored'',''area.added'',''area.edited'',''area.hidden'',''area.restored'',''amenity.added'',''amenity.edited'',''amenity.hidden'',''amenity.restored'',''dataReport.resolved'',''dataReport.dismissed'']::text[]) OR (a."action" = ANY(ARRAY[''user.created'',''user.roleChanged'',''user.suspended'',''user.unsuspended'',''user.temporaryPasswordIssued'',''user.temporaryPasswordHandedOver'',''user.emailChanged'']::text[]) AND a."space_id" IS NULL))'
\set tj 'LEFT JOIN "spaces" ts ON a."entity_type" = ''space'' AND ts."id" = a."entity_id" LEFT JOIN "users" tu ON a."entity_type" = ''user'' AND tu."id" = a."entity_id" LEFT JOIN "governorates" tg ON a."entity_type" = ''governorate'' AND tg."id" = a."entity_id" LEFT JOIN "areas" tar ON a."entity_type" = ''area'' AND tar."id" = a."entity_id" LEFT JOIN "amenities" tam ON a."entity_type" = ''amenity'' AND tam."id" = a."entity_id" LEFT JOIN "customers" tc ON a."entity_type" = ''customer'' AND tc."id" = a."entity_id" LEFT JOIN "subscriptions" tsu ON a."entity_type" = ''subscription'' AND tsu."id" = a."entity_id" LEFT JOIN "packages" tp ON a."entity_type" = ''package'' AND tp."id" = a."entity_id" LEFT JOIN "visits" tv ON a."entity_type" = ''visit'' AND tv."id" = a."entity_id" LEFT JOIN "customers" tvc ON tvc."id" = tv."customer_id" LEFT JOIN "check_ins" tci ON a."entity_type" = ''checkIn'' AND tci."id" = a."entity_id" LEFT JOIN "customers" tcc ON tcc."id" = tci."customer_id" LEFT JOIN "announcements" tan ON a."entity_type" = ''announcement'' AND tan."id" = a."entity_id"'
\set qj 'strpos(masaha_search_text(concat_ws('' '', coalesce(ts."name_en", tu."name", tg."name_en", tar."name_en", tam."name_en", tc."name", tsu."name", tp."name", tv."visitor_name", tvc."name", tcc."name"), coalesce(ts."name_ar", tg."name_ar", tar."name_ar", tam."name_ar"))), masaha_search_text(''زبون 42'')) > 0'
\set qja 'strpos(masaha_search_text(concat_ws('' '', coalesce(ts."name_en", tu."name", tg."name_en", tar."name_en", tam."name_en", tc."name", tsu."name", tp."name", tv."visitor_name", tvc."name", tcc."name"), coalesce(ts."name_ar", tg."name_ar", tar."name_ar", tam."name_ar"), es."name_en", es."name_ar")), masaha_search_text(''hub 7'')) > 0'
\set cj 'a."id", a."created_at", a."action", a."entity_type", a."entity_id", a."before", a."after", a."actor_id", coalesce(ts."name_en", tu."name", tg."name_en", tar."name_en", tam."name_en", tc."name", tsu."name", tp."name", tv."visitor_name", tvc."name", tcc."name") AS name, coalesce(ts."name_ar", tg."name_ar", tar."name_ar", tam."name_ar") AS name_ar, coalesce(ts."deleted_at", tan."deleted_at") IS NOT NULL AS deleted'
\echo '### J7 owner page ALL with q'
EXPLAIN (ANALYZE, BUFFERS) SELECT :cj, sm."user_id" IS NOT NULL FROM "audit_logs" a :actor_joins :tj WHERE a."space_id" = 1 AND :qj ORDER BY a."created_at" DESC, a."id" DESC LIMIT 20 OFFSET 0;
\echo '### J8 owner count ALL with q'
EXPLAIN (ANALYZE, BUFFERS) SELECT count(*)::integer FROM "audit_logs" a :actor_joins :tj WHERE a."space_id" = 1 AND :qj;
\echo '### J9 owner actors ALL with q'
EXPLAIN (ANALYZE, BUFFERS) SELECT kind, id, name FROM (SELECT DISTINCT CASE WHEN a."actor_id" IS NULL THEN 'SYSTEM' WHEN sm."user_id" IS NULL THEN 'MASAHA' ELSE 'PERSON' END AS kind, CASE WHEN sm."user_id" IS NOT NULL THEN a."actor_id" END AS id, CASE WHEN sm."user_id" IS NOT NULL THEN au."name" END AS name FROM "audit_logs" a :actor_joins :tj WHERE a."space_id" = 1 AND :qj) actors ORDER BY 1, 3, 2 LIMIT 50;
\echo '### J1 owner page LAST_30_DAYS'
EXPLAIN (ANALYZE, BUFFERS) SELECT :cj, sm."user_id" IS NOT NULL FROM "audit_logs" a :actor_joins :tj WHERE a."space_id" = 1 AND a."created_at" >= :since ORDER BY a."created_at" DESC, a."id" DESC LIMIT 20 OFFSET 0;
\echo '### J4 owner page ALL'
EXPLAIN (ANALYZE, BUFFERS) SELECT :cj, sm."user_id" IS NOT NULL FROM "audit_logs" a :actor_joins :tj WHERE a."space_id" = 1 ORDER BY a."created_at" DESC, a."id" DESC LIMIT 20 OFFSET 0;
\echo '### J4b owner page ALL, page 500'
EXPLAIN (ANALYZE, BUFFERS) SELECT :cj, sm."user_id" IS NOT NULL FROM "audit_logs" a :actor_joins :tj WHERE a."space_id" = 1 ORDER BY a."created_at" DESC, a."id" DESC LIMIT 20 OFFSET 9980;
\echo '### JA1 admin page ALL'
EXPLAIN (ANALYZE, BUFFERS) SELECT :cj, au."name", es."id", es."name_en" FROM "audit_logs" a LEFT JOIN "users" au ON au."id" = a."actor_id" LEFT JOIN "spaces" es ON es."id" = a."space_id" :tj WHERE :platform ORDER BY a."created_at" DESC, a."id" DESC LIMIT 20 OFFSET 0;
\echo '### JA4 admin page ALL with q'
EXPLAIN (ANALYZE, BUFFERS) SELECT :cj, au."name", es."id", es."name_en" FROM "audit_logs" a LEFT JOIN "users" au ON au."id" = a."actor_id" LEFT JOIN "spaces" es ON es."id" = a."space_id" :tj WHERE :platform AND :qja ORDER BY a."created_at" DESC, a."id" DESC LIMIT 20 OFFSET 0;
\echo '### JA5 admin count ALL with q'
EXPLAIN (ANALYZE, BUFFERS) SELECT count(*)::integer FROM "audit_logs" a LEFT JOIN "spaces" es ON es."id" = a."space_id" :tj WHERE :platform AND :qja;
TRUNCATE TABLE audit_logs, space_managers, visits, customers, spaces, areas, governorates, users RESTART IDENTITY CASCADE;
