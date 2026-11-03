def sub(p, pairs):
    s = open(p, encoding='utf8', newline='').read()
    for a, b in pairs:
        assert s.count(a) == 1, (p, a)
        s = s.replace(a, b)
    open(p, 'w', encoding='utf8', newline='').write(s)

sub('src/shared/jobs/jobs.ts', [
("""/** A module's timed work: what it did, counted, at the run's time. */
export interface Job {
  name: string;
  run(now: Date): Promise<Record<string, number>>;
}

/** One run of every job: each one's counts, `null` for one that failed. */
export interface JobsRun {
  ranAt: string;
  jobs: { name: string; done: Record<string, number> | null }[];
  failed: boolean;
}""",
"""/**
 * What a job did, counted; `stalled: true` when it closed nothing and its failures filled the batch
 * it took, so the next run would only fail the same rows again (finding 121).
 */
export type JobDone = Record<string, number> & { stalled?: true };

/** A module's timed work: what it did, counted, at the run's time. */
export interface Job {
  name: string;
  run(now: Date): Promise<JobDone>;
}

/** One run of every job: each one's counts, `null` for one that failed; whether one stalled. */
export interface JobsRun {
  ranAt: string;
  jobs: { name: string; done: JobDone | null }[];
  failed: boolean;
  stalled: boolean;
}"""),
("""/**
 * The scheduler port (ADR 0014; conventions §12): runs each registered job in turn, at one time
 * read from the clock. A job that throws is logged and the others still run.
 */""",
"""/**
 * The scheduler port (ADR 0014; conventions §12): runs each registered job in turn, at one time
 * read from the clock. A job that throws is logged and the others still run; so does one that
 * stalled, logged `job stalled` with its count of failures.
 */"""),
("""          logger.info({ job: job.name, ...done, ms }, 'job ran');
          ran.push({ name: job.name, done });""",
"""          logger.info({ job: job.name, ...done, ms }, 'job ran');
          if (done.stalled) logger.error({ job: job.name, failed: done.failed }, 'job stalled');
          ran.push({ name: job.name, done });"""),
("""        failed: ran.some(({ done }) => done === null),
      };""",
"""        failed: ran.some(({ done }) => done === null),
        stalled: ran.some(({ done }) => done?.stalled === true),
      };"""),
])

sub('src/shared/jobs/jobs.routes.ts', [
("""`unauthorized` and runs nothing; a run where a job itself threw answers `server`, so the cron
 * service shows it. Stays a job could not close are counted in its `failed`, and answered 200: one
 * bad stay never turns every run red, which a cron service may answer by switching the job off.
 */""",
"""`unauthorized` and runs nothing; a run where a job itself threw answers `server`, so the cron
 * service shows it. Stays a job could not close are counted in its `failed`, and answered 200: one
 * bad stay never turns every run red, which a cron service may answer by switching the job off.
 * But a job that stalled — its failures filled its batch, nothing closed — answers `server` too: no
 * later run can get past those stays by itself (finding 121).
 */"""),
("""    const { ranAt, jobs: ran, failed } = await jobs.run();
    if (failed) throw AppError.server(undefined, 'A timed job failed');""",
"""    const { ranAt, jobs: ran, failed, stalled } = await jobs.run();
    if (failed) throw AppError.server(undefined, 'A timed job failed');
    if (stalled) throw AppError.server(undefined, 'A timed job stalled');"""),
])

sub('src/shared/jobs/index.ts', [
("export { createJobs, type Job, type Jobs, type JobsRun } from './jobs.ts';",
 "export { createJobs, type Job, type JobDone, type Jobs, type JobsRun } from './jobs.ts';"),
])

for p, key, name in [('src/modules/visits/visits.service.ts', 'visits', 'stay'),
                     ('src/modules/subscriptions/subscriptions.service.ts', 'checkIns', 'checkIn')]:
    s = open(p, encoding='utf8', newline='').read()
    old_sig = f"Promise<{{ {key}: number; remaining: number; failed: number }}>"
    assert s.count(old_sig) == 1, (p, 'sig')
    s = s.replace(old_sig, f"Promise<{{\n      {key}: number;\n      remaining: number;\n      failed: number;\n      stalled?: true;\n    }}>")
    loop = f"      let closed = 0;\n      for (const {{ {name}, dueAt"
    assert s.count(loop) == 1, (p, 'loop')
    s = s.replace(loop, f"      const batch = due.slice(0, AUTO_CHECKOUT_BATCH);\n      const failedBefore = failed;\n      let closed = 0;\n      for (const {{ {name}, dueAt")
    s = s.replace(" of due.slice(0, AUTO_CHECKOUT_BATCH)) {", " of batch) {", 1)
    ret = f"""      return {{
        {key}: closed,
        remaining: Math.max(due.length - AUTO_CHECKOUT_BATCH, 0),
        failed,
      }};"""
    assert s.count(ret) == 1, (p, 'ret')
    s = s.replace(ret, f"""      // Stalled: the batch was all failures, so the next run would take and fail the same stays.
      const stalled = batch.length > 0 && closed === 0 && failed - failedBefore === batch.length;
      return {{
        {key}: closed,
        remaining: Math.max(due.length - AUTO_CHECKOUT_BATCH, 0),
        failed,
        ...(stalled && {{ stalled: true as const }}),
      }};""")
    open(p, 'w', encoding='utf8', newline='').write(s)
