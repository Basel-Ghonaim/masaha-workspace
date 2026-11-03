process.loadEnvFile('.env');
const url = process.env.TEST_DATABASE_URL;
if (!/masaha_a_lane_a2_test/.test(url)) throw new Error('not the lane test db');
const { execSync } = await import('node:child_process');
execSync('npx prisma db execute --stdin', { input: `DELETE FROM subscriptions WHERE NOT ("published_period" IS NULL OR ("published_period" IN ('WEEK', 'MONTH') AND "package_id" IS NULL));
ALTER TABLE "subscriptions" ADD CONSTRAINT "subscriptions_published_period_check" CHECK ("published_period" IS NULL OR ("published_period" IN ('WEEK', 'MONTH') AND "package_id" IS NULL));`, env: { ...process.env, DATABASE_URL: url }, stdio: ['pipe', 'inherit', 'inherit'] });
