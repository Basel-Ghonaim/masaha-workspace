def edit(p, pairs):
    s = open(p, encoding='utf8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)
A = r'C:\dev\masaha\app-lane-a1\apps\api\src'
edit(A + r'\shared\jobs\jobs.ts', [("""/** A module's timed work: what it did, counted, at the run's time. */""",
"""/**
 * How many rows a sweep deletes at most a table a run, so a run stays within the function's time
 * (ADR 0014): what is left goes at the next run.
 */
export const SWEEP_BATCH = 5_000;

/** A module's timed work: what it did, counted, at the run's time. */""")])
edit(A + r'\shared\jobs\index.ts', [("export { createJobs, type Job, type Jobs, type JobsRun } from './jobs.ts';",
 "export { createJobs, SWEEP_BATCH, type Job, type Jobs, type JobsRun } from './jobs.ts';")])
edit(A + r'\shared\rate-limit\counter.ts', [
("""/** How many rows a sweep deletes at most a table a run, so a run stays within the function's time. */
export const SWEEP_BATCH = 5_000;

""", ""),
("""import type { PrismaClient } from '../../generated/prisma/client.ts';""", """import type { PrismaClient } from '../../generated/prisma/client.ts';
import { SWEEP_BATCH } from '../jobs/index.ts';"""),
])
edit(A + r'\shared\rate-limit\index.ts', [("export {\n  createCounter,\n  SWEEP_BATCH,\n  sweepEndedWindows,", "export {\n  createCounter,\n  sweepEndedWindows,")])
edit(A + r'\modules\sessions\sessions.service.ts', [
("""
/** How many rows the sweep deletes at most a table a run, so a run stays within the function's time. */
export const SWEEP_BATCH = 5_000;""", ""),
("""import type { Tx } from '../../db/index.ts';""", """import type { Tx } from '../../db/index.ts';
import { SWEEP_BATCH } from '../../shared/jobs/index.ts';"""),
])
edit(A + r'\app.ts', [("""  createCounter,
  FIFTEEN_MINUTES,
  createLimiter,
  limitRequests,
  type RateLimitPolicy,
} from './shared/rate-limit/index.ts';""", """  createCounter,
  FIFTEEN_MINUTES,
  createLimiter,
  limitRequests,
  sweepEndedWindows,
  type RateLimitPolicy,
} from './shared/rate-limit/index.ts';""")])
