// Removes the empty M1 record from the lane's own test database, so migrate deploy applies the filled one.
process.loadEnvFile('.env');
const url = process.env.TEST_DATABASE_URL;
if (!/masaha_a_lane_a2_test/.test(url)) throw new Error('not the lane test db');
const { execSync } = await import('node:child_process');
execSync('npx prisma db execute --stdin', { input: `DELETE FROM _prisma_migrations WHERE migration_name = '${process.argv[2]}';`, env: { ...process.env, DATABASE_URL: url }, stdio: ['pipe', 'inherit', 'inherit'] });
execSync('npx prisma migrate deploy', { env: { ...process.env, DATABASE_URL: url }, stdio: 'inherit' });
