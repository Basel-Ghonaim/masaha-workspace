-- CONTACT_RULES: the stored contacts the new rules (C3) would refuse. Read-only: it counts, it changes nothing.
SET default_transaction_read_only = on;
WITH input AS (
  SELECT 'data'::text AS source, sc.type::text AS type, sc.value,
         s.deleted_at IS NOT NULL AS space_deleted, NULL::boolean AS expected
  FROM space_contacts sc JOIN spaces s ON s.id = sc.space_id
  UNION ALL
  SELECT 'self-test', t.type, t.value, false, t.expected
  FROM (VALUES
    ('WEBSITE', 'https://masaha.ps', false),
    ('WEBSITE', 'https://masaha.ps/about?lang=ar', false),
    ('WEBSITE', 'https://0.0.0.123', true),
    ('WEBSITE', 'https://35.181.230.0', true),
    ('WEBSITE', 'https://localhost:5173/x', true),
    ('WEBSITE', 'https://example', true),
    ('OTHER', 'https://discord.gg/focushub', false),
    ('OTHER', '+970599123456', false),
    ('OTHER', 'https://10.0.0.1', true),
    ('FACEBOOK', 'https://www.facebook.com/masaha.gaza', false),
    ('FACEBOOK', 'https://www.facebook.com/profile.php?id=100012345', false),
    ('FACEBOOK', 'https://www.facebook.com/people/Masaha-Hub/100012345678', false),
    ('FACEBOOK', 'https://www.facebook.com/watch', true),
    ('FACEBOOK', 'https://www.facebook.com/masaha/videos/123', true),
    ('FACEBOOK', 'https://www.facebook.com/photo.php', true),
    ('FACEBOOK', 'https://www.facebook.com/groups/gazafreelancers', true)
  ) AS t(type, value, expected)
), parsed AS (
  SELECT input.*,
    lower(substring(value FROM '^https?://([^/?#:]+)')) AS host,
    coalesce(rtrim(substring(value FROM '^https?://[^/?#]+(/[^?#]*)'), '/'), '') AS path
  FROM input
), judged AS (
  SELECT parsed.*,
    CASE
      WHEN type = 'WEBSITE' OR (type = 'OTHER' AND value NOT LIKE '+%') THEN
        host IS NULL
        OR host !~* '^([a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?\.)+([a-z]{2,63}|xn--[a-z0-9-]{1,59})$'
      WHEN type = 'FACEBOOK' THEN NOT (
        value ~ '^https://www\.facebook\.com/profile\.php\?id=[0-9]+$'
        OR path ~* '^/people/[^/]+/[0-9]+$'
        OR (path ~* '^/[a-z0-9_.-]+$'
            AND lower(path) NOT IN ('/watch', '/reel', '/reels', '/video', '/videos', '/post', '/posts',
              '/groups', '/events', '/photo', '/photos', '/share', '/sharer', '/search', '/stories',
              '/story', '/hashtag', '/live', '/gaming', '/marketplace', '/pages', '/people', '/permalink')
            AND path !~* '\.php$')
      )
      ELSE false
    END AS refused
  FROM parsed
)
SELECT source, type,
  count(*) AS total,
  count(*) FILTER (WHERE refused) AS refused,
  count(*) FILTER (WHERE refused AND space_deleted) AS refused_on_deleted_spaces,
  count(*) FILTER (WHERE source = 'self-test' AND refused IS DISTINCT FROM expected) AS self_test_mismatches,
  string_agg(value, ' | ' ORDER BY value) FILTER (WHERE refused AND source = 'data') AS refused_values
FROM judged
WHERE type IN ('WEBSITE', 'FACEBOOK', 'OTHER')
GROUP BY source, type
ORDER BY source, type;