-- EC15: what the demo data of masaha_b_dev holds for the real run (read only). No phone, no email printed.
\pset footer off
SELECT s.id, s.slug FROM spaces s WHERE s.slug IN ('masaha-demo', 'demo-space') OR s.id IN (
  SELECT space_id FROM space_managers WHERE user_id = (SELECT id FROM users WHERE email = 'demo-owner@example.com'));
WITH sp AS (SELECT space_id AS id FROM space_managers WHERE user_id = (SELECT id FROM users WHERE email = 'demo-owner@example.com') LIMIT 1)
SELECT
 (SELECT count(*) FROM payments WHERE space_id = (SELECT id FROM sp) AND voided_at IS NULL
    AND received_at >= date_trunc('month', now() AT TIME ZONE 'Asia/Gaza') AT TIME ZONE 'Asia/Gaza') AS payments_this_month,
 (SELECT count(*) FROM payments WHERE space_id = (SELECT id FROM sp)) AS payments_all,
 (SELECT count(*) FROM visits WHERE space_id = (SELECT id FROM sp) AND checked_out_at IS NOT NULL
    AND checked_in_at >= now() - interval '14 days') AS closed_visits_14d,
 (SELECT count(*) FROM check_ins WHERE space_id = (SELECT id FROM sp) AND checked_out_at IS NOT NULL
    AND checked_in_at >= now() - interval '14 days') AS closed_checkins_14d,
 (SELECT count(*) FROM data_reports WHERE space_id = (SELECT id FROM sp) AND status = 'OPEN') AS open_reports,
 (SELECT count(*) FROM announcements WHERE space_id = (SELECT id FROM sp) AND deleted_at IS NULL
    AND starts_at <= now() AND (ends_at IS NULL OR ends_at > now())) AS running_announcements,
 (SELECT count(*) FROM customers WHERE space_id = (SELECT id FROM sp)) AS customers,
 (SELECT count(*) FROM customers WHERE space_id = (SELECT id FROM sp) AND archived_at IS NOT NULL) AS archived_customers,
 (SELECT count(*) FROM subscriptions WHERE space_id = (SELECT id FROM sp)) AS subscriptions,
 (SELECT count(*) FROM spaces WHERE deleted_at IS NULL) AS spaces_live,
 (SELECT count(*) FROM data_reports WHERE status = 'OPEN') AS open_reports_all,
 (SELECT count(*) FROM users WHERE created_at >= now() - interval '30 days') AS users_30d;
