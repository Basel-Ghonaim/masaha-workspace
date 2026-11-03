// B71: the CHECK dropped from the lane's own test database, the test run, the CHECK restored.
process.loadEnvFile('.env');
const url = process.env.TEST_DATABASE_URL;
if (!/masaha_a_lane_a2_test/.test(url)) throw new Error('not the lane test db');
const { execSync, spawnSync } = await import('node:child_process');
const exec = (sql) => execSync('npx prisma db execute --stdin', { input: sql, env: { ...process.env, DATABASE_URL: url }, stdio: ['pipe', 'inherit', 'inherit'] });
exec('ALTER TABLE subscriptions DROP CONSTRAINT subscriptions_published_period_check;');
try {
  const r = spawnSync('npx vitest run --project api src/db/subscriptions.api.test.ts -t "published price"', { shell: true, encoding: 'utf8' });
  console.log((r.stdout + r.stderr).split('\n').filter((l) => /×|✓|Tests |Error/.test(l)).join('\n'));
} finally {
  exec(`ALTER TABLE "subscriptions" ADD CONSTRAINT "subscriptions_published_period_check" CHECK ("published_period" IS NULL OR ("published_period" IN ('WEEK', 'MONTH') AND "package_id" IS NULL));`);
}
