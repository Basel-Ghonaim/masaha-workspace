"""Commit 3: the admin's parts added beside the owner's in the repository, the keys and the target."""
BASE = 'C:/dev/masaha/app-lane-b/apps/web/src/features/data-reports/'


def edit(rel, pairs):
    path = BASE + rel
    with open(path, encoding='utf8', newline='') as handle:
        text = handle.read()
    for old, new in pairs:
        assert text.count(old) == 1, (rel, old[:60], text.count(old))
        text = text.replace(old, new)
    with open(path, 'w', encoding='utf8', newline='') as handle:
        handle.write(text)


edit('repository/dataReportsRepository.ts', [
    ("""import type {
  DecideReportRequest,
  SpaceReport,
  SpaceReportsQuery,
} from '@masaha/shared/data-reports';""", """import type {
  AdminReport,
  AdminReportsQuery,
  DecideReportRequest,
  SpaceReport,
  SpaceReportsQuery,
} from '@masaha/shared/data-reports';"""),
("""const spaceReportsPath = (spaceId: number) => `/manage/spaces/${String(spaceId)}/data-reports`;
""", """const spaceReportsPath = (spaceId: number) => `/manage/spaces/${String(spaceId)}/data-reports`;
/** Every space's reports, below the admin's path. */
const ADMIN_REPORTS_PATH = '/admin/data-reports';
"""),
(""" * space's reports and the owner's decision. Each audience's calls are its own, side by side.""",
 """ * space's reports and the owner's decision; the admin's list of every space's and the admin's
 * decision. Each audience's calls are its own, side by side."""),
("""  decideSpace(spaceId: number, reportId: number, body: DecideReportRequest): Promise<SpaceReport>;
}""", """  decideSpace(spaceId: number, reportId: number, body: DecideReportRequest): Promise<SpaceReport>;
  /** A page of every space's reports the query finds, newest first, with who reported each. */
  adminReports(query: AdminReportsQuery): Promise<Page<AdminReport[]>>;
  /** The admin's decision of an unverified space's report, with its reply or none. */
  decideAdmin(reportId: number, body: DecideReportRequest): Promise<AdminReport>;
}"""),
("""      api.patch<SpaceReport>(`${spaceReportsPath(spaceId)}/${String(reportId)}`, body),
""", """      api.patch<SpaceReport>(`${spaceReportsPath(spaceId)}/${String(reportId)}`, body),
    adminReports: (query) => api.getPage<AdminReport[]>(ADMIN_REPORTS_PATH, { params: query }),
    decideAdmin: (reportId, body) =>
      api.patch<AdminReport>(`${ADMIN_REPORTS_PATH}/${String(reportId)}`, body),
"""),
])

edit('hooks/queryKeys.ts', [
    ("import type { SpaceReportsQuery } from '@masaha/shared/data-reports';",
     "import type { AdminReportsQuery, SpaceReportsQuery } from '@masaha/shared/data-reports';"),
    (" * reports under the space's.", " * reports under the space's, every space's under the admin's."),
    ("""    ['space', spaceId, 'dataReports', query] as const,
""", """    ['space', spaceId, 'dataReports', query] as const,
  /** Every read of the admin's reports: the admin's decision reads them again. */
  adminAll: () => ['admin', 'dataReports'] as const,
  /** One page of every space's reports, by its whole query. */
  admin: (query: AdminReportsQuery) => ['admin', 'dataReports', query] as const,
"""),
])

edit('types/DecideTarget.ts', [
    ("""import type { SpaceReport } from '@masaha/shared/data-reports';

/** The report the decision sheet shows, and whose decision it sends: the owner's, of a space's. */
export type DecideTarget = { audience: 'owner'; spaceId: number; report: SpaceReport };""",
     """import type { AdminReport, SpaceReport } from '@masaha/shared/data-reports';

/**
 * The report the decision sheet shows, and whose decision it sends: the owner's, of a space's, or
 * the admin's, of any space's.
 */
export type DecideTarget =
  | { audience: 'owner'; spaceId: number; report: SpaceReport }
  | { audience: 'admin'; report: AdminReport };"""),
])
print('ok')
