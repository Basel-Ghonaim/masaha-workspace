import io, os
os.chdir(r'C:\dev\masaha\app-b')

def edit(p, pairs):
    s = io.open(p, encoding='utf-8', newline='').read()
    for o, n in pairs:
        assert s.count(o) == 1, (p, o)
        s = s.replace(o, n)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)

D = 'apps/api/src/modules/data-reports/'

edit(D + 'data-reports.repository.ts', [
("""import type {
  DataReportField,
  DataReportStatus,
  ReportStatusFilter,
} from '@masaha/shared/data-reports';""", """import type {
  DataReportDecision,
  DataReportField,
  DataReportStatus,
  ReportStatusFilter,
} from '@masaha/shared/data-reports';"""),
("""/** A page's bounds. */""", """/** A report under its decision's lock: who decided it, to tell a retry from another decision. */
export interface LockedReport extends ReportRow {
  resolvedById: number | null;
}

/** A page's bounds. */"""),
("""      return { rows, total };
    },
  };""", """      return { rows, total };
    },

    /**
     * A page of the space's reports, newest first, then id, filtered by status and field; and how
     * many pass. Its select has no reporter: the owner's list never holds one.
     */
    async pageOfSpace(
      spaceId: number,
      {
        status,
        field,
      }: { status?: ReportStatusFilter | undefined; field?: DataReportField | undefined },
      { skip, take }: Page,
    ): Promise<{ rows: ReportRow[]; total: number }> {
      const where = { spaceId, ...statusWhere(status), ...(field ? { field } : {}) };
      const [rows, total] = await Promise.all([
        prisma.dataReport.findMany({ where, orderBy: NEWEST_FIRST, skip, take, select: REPORT }),
        prisma.dataReport.count({ where }),
      ]);
      return { rows, total };
    },

    /** The space a report is about, read without a lock; `null` for no such report. */
    async findSpaceOf(id: number): Promise<number | null> {
      const row = await prisma.dataReport.findUnique({ where: { id }, select: { spaceId: true } });
      return row?.spaceId ?? null;
    },

    /** Locks the report's row (`FOR UPDATE`) and answers it with who decided it. */
    async lockIn(id: number, tx: Tx): Promise<LockedReport> {
      await tx.$queryRaw`SELECT id FROM data_reports WHERE id = ${id} FOR UPDATE`;
      return tx.dataReport.findUniqueOrThrow({
        where: { id },
        select: { ...REPORT, resolvedById: true },
      });
    },

    /** Writes a decision's fields together (the CHECKs of `data_report_rules`). */
    decide(
      id: number,
      data: {
        status: DataReportDecision;
        resolvedById: number;
        resolvedAt: Date;
        resolutionNote: string | null;
        resolvedAs: DataReportResolver;
      },
      tx: Tx,
    ): Promise<ReportRow> {
      return tx.dataReport.update({ where: { id }, data, select: REPORT });
    },
  };"""),
])

edit(D + 'data-reports.service.ts', [
("import type { CreateReportRequest, MyReport, MyReportsQuery } from '@masaha/shared/data-reports';", """import type {
  CreateReportRequest,
  DecideReportRequest,
  MyReport,
  MyReportsQuery,
  SpaceReport,
  SpaceReportsQuery,
} from '@masaha/shared/data-reports';"""),
("import type { RunInTransaction } from '../../db/index.ts';\nimport type { Actor } from '../../shared/auth/index.ts';",
 "import type { RunInTransaction, Tx } from '../../db/index.ts';\nimport type { DataReportResolver } from '../../generated/prisma/enums.ts';\nimport type { AuditWriter } from '../../shared/audit/index.ts';\nimport { can, type Actor, type LoadedSpace, type SpaceLink } from '../../shared/auth/index.ts';"),
("import { toMyReport } from './data-reports.mapper.ts';\nimport { createDataReportsRepository } from './data-reports.repository.ts';",
 "import { toMyReport, toSpaceReport } from './data-reports.mapper.ts';\nimport { createDataReportsRepository, type ReportRow } from './data-reports.repository.ts';\nimport { decisionOf } from './decision.ts';"),
("""  runInTransaction: RunInTransaction;
  spaces""", """  runInTransaction: RunInTransaction;
  audit: AuditWriter;
  spaces"""),
("""  runInTransaction,
  spaces,
  publicSpace,""", """  runInTransaction,
  audit,
  spaces,
  publicSpace,"""),
(""" * signed-in user about a listed space, read by the reporter.
 */""", """ * signed-in user about a listed space, read by the reporter, read and decided by the space's owner,
 * or by the admin while the space is unverified.
 */"""),
("""  return {
    /**
     * A page of the user's own reports""", """  /**
   * Decides a report, in one transaction and in this order: the report's space, read without a
   * lock, the expected one when one is (else `not_found`); the space's lock (`not_found` once it is
   * deleted); `can('dataReports.resolve')` on the links read under it, so an owner linked or
   * unlinked meanwhile decides; the report's row, locked; `decisionOf`: a retry answered as it is,
   * writing nothing, another decision of a decided report `REPORT_ALREADY_DECIDED`; else the
   * decision, by `resolvedAs`, audited with its reply.
   */
  async function decideUnder(
    actor: Actor,
    reportId: number,
    request: DecideReportRequest,
    {
      spaceId,
      linksUnder,
      resolvedAs,
    }: {
      spaceId: number | null;
      linksUnder: (spaceId: number, tx: Tx) => Promise<readonly SpaceLink[]>;
      resolvedAs: DataReportResolver;
    },
  ): Promise<ReportRow> {
    const reportSpaceId = await repository.findSpaceOf(reportId);
    if (reportSpaceId === null || (spaceId !== null && reportSpaceId !== spaceId)) {
      throw AppError.notFound(undefined, 'Report not found');
    }
    return runInTransaction(async (tx) => {
      if (!(await spaces.lock(reportSpaceId, tx))) {
        throw AppError.notFound(undefined, 'Report not found');
      }
      if (!can(actor, 'dataReports.resolve', { links: await linksUnder(reportSpaceId, tx) })) {
        throw AppError.forbidden();
      }
      const current = await repository.lockIn(reportId, tx);
      const outcome = decisionOf(current, request, actor.id);
      if (outcome === 'as-is') return current;
      if (outcome === 'conflict') throw AppError.conflict('REPORT_ALREADY_DECIDED');

      const note = request.note ?? null;
      const decided = await repository.decide(
        reportId,
        {
          status: request.status,
          resolvedById: actor.id,
          resolvedAt: now(),
          resolutionNote: note,
          resolvedAs,
        },
        tx,
      );
      await audit(
        {
          actorId: actor.id,
          action: request.status === 'RESOLVED' ? 'dataReport.resolved' : 'dataReport.dismissed',
          entityType: 'dataReport',
          entityId: reportId,
          spaceId: reportSpaceId,
          after: { note },
        },
        tx,
      );
      return decided;
    });
  }

  return {
    /**
     * A page of the space's reports, newest first, by status and field, as its owner reads them:
     * never who reported them; and how many there are. Read without a lock.
     */
    async ofSpace(
      spaceId: number,
      { status, field, page, limit }: SpaceReportsQuery,
    ): Promise<{ rows: SpaceReport[]; total: number }> {
      const { rows, total } = await repository.pageOfSpace(
        spaceId,
        { status, field },
        { skip: toSkip({ page, limit }), take: limit },
      );
      return { rows: rows.map(toSpaceReport), total };
    },

    /** The space's owner decides one of its reports (`decideUnder`), on its links under the lock. */
    async decideAtSpace(
      actor: Actor,
      space: LoadedSpace,
      reportId: number,
      request: DecideReportRequest,
    ): Promise<SpaceReport> {
      const decided = await decideUnder(actor, reportId, request, {
        spaceId: space.id,
        linksUnder: (_spaceId, tx) => space.linksUnder(tx),
        resolvedAs: 'OWNER',
      });
      return toSpaceReport(decided);
    },

    /**
     * A page of the user's own reports"""),
])

edit(D + 'data-reports.controller.ts', [
("import type { CreateReportRequest, MyReport, MyReportsQuery } from '@masaha/shared/data-reports';", """import type {
  CreateReportRequest,
  DecideReportRequest,
  MyReport,
  MyReportsQuery,
  SpaceReport,
  SpaceReportsQuery,
} from '@masaha/shared/data-reports';"""),
("import { signedIn } from '../../shared/auth/index.ts';", "import { signedIn, spaceOf } from '../../shared/auth/index.ts';"),
("import { buildPaginationMeta, sendSuccess } from '../../shared/http/index.ts';", "import { buildPaginationMeta, sendSuccess } from '../../shared/http/index.ts';\nimport { parseId } from '../../shared/validation/index.ts';"),
("""      sendSuccess(res, rows satisfies MyReport[], { meta: buildPaginationMeta(query, total) });
    },
""", """      sendSuccess(res, rows satisfies MyReport[], { meta: buildPaginationMeta(query, total) });
    },

    /** 200 with a page of the space's reports and its `meta`: never who reported them. */
    ofSpace: async (req: Request, res: Response) => {
      const query = req.query as unknown as SpaceReportsQuery;
      const { rows, total } = await service.ofSpace(spaceOf(req).id, query);
      sendSuccess(res, rows satisfies SpaceReport[], { meta: buildPaginationMeta(query, total) });
    },

    /** 200 with the report as decided now, or as it was for the same decision again. */
    decideAtSpace: async (req: Request, res: Response) => {
      const { userId, role } = signedIn(req);
      const decided = await service.decideAtSpace(
        { id: userId, role },
        spaceOf(req),
        parseId(req.params.reportId),
        req.body as DecideReportRequest,
      );
      sendSuccess(res, decided satisfies SpaceReport);
    },
"""),
])

edit(D + 'index.ts', [("export { createDataReportsSiteRouter }", "export { createDataReportsManageRouter } from './data-reports.manage.routes.ts';\nexport { createDataReportsSiteRouter }")])

edit('apps/api/src/app.ts', [
("""  createDataReportsController,
  createDataReportsService,""", """  createDataReportsController,
  createDataReportsManageRouter,
  createDataReportsService,"""),
("""  const dataReports = createDataReportsService({
    runInTransaction,""", """  const dataReports = createDataReportsService({
    runInTransaction,
    audit: writeAudit,"""),
("""  manage.use('/packages',""", """  manage.use('/data-reports', createDataReportsManageRouter(dataReportsController));
  manage.use('/packages',"""),
])
print('ok')
