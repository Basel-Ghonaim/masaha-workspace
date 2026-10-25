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
("""/** A report as its space's owner may see it: never who reported it. */""", """// Only the reporter's own list and the admin's read who reported and who decided.
const WITH_PEOPLE = { ...REPORT, userId: true, resolvedById: true } as const;

/** A report as its space's owner may see it: never who reported it. */"""),
("""/** A report under its decision's lock""", """/** A report with who reported it and who decided it: the admin's list. */
export interface ReportWithPeople extends ReportRow {
  userId: number;
  resolvedById: number | null;
}

/** A report under its decision's lock"""),
("""    /** The space a report is about, read without a lock; `null` for no such report. */""", """    /**
     * A page of every report, newest first, then id, filtered by status, field and space; and how
     * many pass. A soft-deleted space's reports are left out (ADR 0007).
     */
    async pageAll(
      {
        status,
        field,
        spaceId,
      }: {
        status?: ReportStatusFilter | undefined;
        field?: DataReportField | undefined;
        spaceId?: number | undefined;
      },
      { skip, take }: Page,
    ): Promise<{ rows: ReportWithPeople[]; total: number }> {
      const where = {
        space: { deletedAt: null },
        ...statusWhere(status),
        ...(field ? { field } : {}),
        ...(spaceId === undefined ? {} : { spaceId }),
      };
      const [rows, total] = await Promise.all([
        prisma.dataReport.findMany({
          where,
          orderBy: NEWEST_FIRST,
          skip,
          take,
          select: WITH_PEOPLE,
        }),
        prisma.dataReport.count({ where }),
      ]);
      return { rows, total };
    },

    /** One report with who reported and who decided it, as it is now. */
    findWithPeople(id: number): Promise<ReportWithPeople> {
      return prisma.dataReport.findUniqueOrThrow({ where: { id }, select: WITH_PEOPLE });
    },

    /** The space a report is about, read without a lock; `null` for no such report. */"""),
])

edit(D + 'data-reports.mapper.ts', [
("import type { MyReport, ReportDecision, SpaceReport } from '@masaha/shared/data-reports';", "import type {\n  AdminReport,\n  MyReport,\n  ReportDecision,\n  SpaceReport,\n} from '@masaha/shared/data-reports';"),
("import type { SpaceName } from '../spaces/index.ts';\nimport type { ReportRow } from './data-reports.repository.ts';", "import type { SpaceName } from '../spaces/index.ts';\nimport type { ReportRow, ReportWithPeople } from './data-reports.repository.ts';"),
("""/** A report as its reporter sees it""", """/**
 * A report as the admin sees it: its space with whether it is verified, who reported it and who
 * decided it, by the names given.
 */
export function toAdminReport(
  row: ReportWithPeople,
  space: SpaceName,
  verified: boolean,
  names: ReadonlyMap<number, string>,
): AdminReport {
  return {
    ...toSpaceReport(row),
    space: { id: space.id, slug: space.slug, nameEn: space.nameEn, nameAr: space.nameAr, verified },
    reporter: { id: row.userId, name: names.get(row.userId) ?? '' },
    decidedBy:
      row.resolvedById === null
        ? null
        : { id: row.resolvedById, name: names.get(row.resolvedById) ?? '' },
  };
}

/** A report as its reporter sees it"""),
])

edit(D + 'data-reports.service.ts', [
("""import type {
  CreateReportRequest,""", """import type {
  AdminReport,
  AdminReportsQuery,
  CreateReportRequest,"""),
("import type { LookupsService } from '../lookups/index.ts';", "import type { LookupsService } from '../lookups/index.ts';\nimport type { SpaceLinksService } from '../space-links/index.ts';"),
("import { toMyReport, toSpaceReport } from './data-reports.mapper.ts';\nimport { createDataReportsRepository, type ReportRow } from './data-reports.repository.ts';",
 "import { toAdminReport, toMyReport, toSpaceReport } from './data-reports.mapper.ts';\nimport {\n  createDataReportsRepository,\n  type ReportRow,\n  type ReportWithPeople,\n} from './data-reports.repository.ts';"),
("""  lookups: LookupsService;
  users""", """  lookups: LookupsService;
  spaceLinks: SpaceLinksService;
  users"""),
("""  lookups,
  users,
  now,
}: Dependencies) {""", """  lookups,
  spaceLinks,
  users,
  now,
}: Dependencies) {"""),
("""  /**
   * Decides a report, in one transaction""", """  /**
   * These reports as the admin sees them: their spaces' names and whether each is verified, and
   * the names of who reported and who decided them, one query each.
   */
  async function asAdminReports(rows: readonly ReportWithPeople[]): Promise<AdminReport[]> {
    const spaceIds = [...new Set(rows.map(({ spaceId }) => spaceId))];
    const people = [
      ...new Set(rows.flatMap(({ userId, resolvedById }) => [userId, resolvedById ?? userId])),
    ];
    const [spaceNames, verifiedIds, names] = await Promise.all([
      spaces.namesWithDeleted(spaceIds),
      spaceLinks.verifiedSpaceIds(),
      users.namesFor(people),
    ]);
    const byId = new Map(spaceNames.map((space) => [space.id, space]));
    const verified = new Set(verifiedIds);
    const nameOf = new Map(names.map(({ id, name }) => [id, name]));
    return rows.flatMap((row) => {
      const space = byId.get(row.spaceId);
      return space ? [toAdminReport(row, space, verified.has(row.spaceId), nameOf)] : [];
    });
  }

  /**
   * Decides a report, in one transaction"""),
("""    /**
     * A page of the user's own reports""", """    /**
     * A page of every report, newest first, by status, field and space, as the admin reads them:
     * with who reported and who decided; a soft-deleted space's left out. Read without a lock.
     */
    async all({
      status,
      field,
      spaceId,
      page,
      limit,
    }: AdminReportsQuery): Promise<{ rows: AdminReport[]; total: number }> {
      const { rows, total } = await repository.pageAll(
        { status, field, spaceId },
        { skip: toSkip({ page, limit }), take: limit },
      );
      return { rows: await asAdminReports(rows), total };
    },

    /**
     * The admin decides a report (`decideUnder`), on its space's links read under the lock: an
     * unverified space's only, so an owner linked meanwhile makes it `forbidden`.
     */
    async decideAsAdmin(
      actor: Actor,
      reportId: number,
      request: DecideReportRequest,
    ): Promise<AdminReport> {
      await decideUnder(actor, reportId, request, {
        spaceId: null,
        linksUnder: (spaceId, tx) => spaceLinks.linksAt(spaceId, tx),
        resolvedAs: 'ADMIN',
      });
      const [decided] = await asAdminReports([await repository.findWithPeople(reportId)]);
      if (!decided) throw AppError.notFound(undefined, 'Report not found');
      return decided;
    },

    /**
     * A page of the user's own reports"""),
])

edit(D + 'data-reports.controller.ts', [
("""import type {
  CreateReportRequest,""", """import type {
  AdminReport,
  AdminReportsQuery,
  CreateReportRequest,"""),
("""    /** 200 with the report as decided now, or as it was for the same decision again. */""", """    /** 200 with a page of every report and its `meta`, with who reported and who decided. */
    all: async (req: Request, res: Response) => {
      const query = req.query as unknown as AdminReportsQuery;
      const { rows, total } = await service.all(query);
      sendSuccess(res, rows satisfies AdminReport[], { meta: buildPaginationMeta(query, total) });
    },

    /** 200 with the report as the admin decided it, or as it was for the same decision again. */
    decideAsAdmin: async (req: Request, res: Response) => {
      const { userId, role } = signedIn(req);
      const decided = await service.decideAsAdmin(
        { id: userId, role },
        parseId(req.params.reportId),
        req.body as DecideReportRequest,
      );
      sendSuccess(res, decided satisfies AdminReport);
    },

    /** 200 with the report as decided now, or as it was for the same decision again. */"""),
])

edit(D + 'index.ts', [("export { createDataReportsManageRouter }", "export { createDataReportsAdminRouter } from './data-reports.admin.routes.ts';\nexport { createDataReportsManageRouter }")])

edit('apps/api/src/app.ts', [
("""  createDataReportsController,
  createDataReportsManageRouter,""", """  createDataReportsAdminRouter,
  createDataReportsController,
  createDataReportsManageRouter,"""),
("""    lookups,
    users,
    now: clock,
  });
  const adminUsers""", """    lookups,
    spaceLinks,
    users,
    now: clock,
  });
  const adminUsers"""),
("""  admin.use(createUsersAdminRouter(usersController));""", """  admin.use(createUsersAdminRouter(usersController));
  admin.use('/data-reports', createDataReportsAdminRouter(dataReportsController));"""),
])
print('ok')
