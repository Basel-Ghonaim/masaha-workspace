import { startEvery } from '../../../../app-b/apps/api/src/shared/jobs/timer.ts';

const started = Date.now();
startEvery(5 * 60_000, () => Promise.resolve(), { error() {} } as never);
process.on('exit', () => console.log(`exited after ${String(Date.now() - started)} ms`));
console.log('timer started');
