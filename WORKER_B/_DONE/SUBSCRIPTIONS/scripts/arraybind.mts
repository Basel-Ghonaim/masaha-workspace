// Times one $queryRaw whose only parameter is an integer array, at several sizes (scratch; not committed).
import { prisma } from '../../../../app-b/apps/api/src/db/index.ts';

for (const size of [10_000, 30_000, 50_000, 70_000]) {
  const ids = Array.from({ length: size }, (_, i) => i + 1);
  const started = performance.now();
  const rows = await prisma.$queryRaw<{ n: number }[]>`SELECT count(*)::integer AS n FROM unnest(${ids}::integer[])`;
  console.log(size, rows[0]?.n, `${Math.round(performance.now() - started)} ms`);
}
await prisma.$disconnect();
