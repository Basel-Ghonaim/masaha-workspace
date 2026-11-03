"""Commit 1: the repository's, the keys' and the fixtures' additions (beside lane B's lines)."""
import sys

ROOT = r'C:\dev\masaha\app-lane-c\apps\web\src'


def edit(path, old, new):
    full = ROOT + '\\' + path
    with open(full, encoding='utf8', newline='') as f:
        text = f.read()
    if text.count(old) != 1:
        sys.exit(f'{path}: anchor found {text.count(old)} times')
    text = text.replace(old, new, 1)
    with open(full, 'w', encoding='utf8', newline='') as f:
        f.write(text)


R = 'features\\data-reports\\repository\\dataReportsRepository.ts'
edit(R, """import type {
  DecideReportRequest,
  SpaceReport,
  SpaceReportsQuery,
} from '@masaha/shared/data-reports';""", """import type {
  DecideReportRequest,
  MyReport,
  MyReportsQuery,
  SpaceReport,
  SpaceReportsQuery,
} from '@masaha/shared/data-reports';""")
edit(R, """  decideSpace(spaceId: number, reportId: number, body: DecideReportRequest): Promise<SpaceReport>;
}""", """  decideSpace(spaceId: number, reportId: number, body: DecideReportRequest): Promise<SpaceReport>;
  /** A page of the signed-in user's own reports, newest first, each with its space and its reply. */
  myReports(query: MyReportsQuery): Promise<Page<MyReport[]>>;
}""")
edit(R, """      api.patch<SpaceReport>(`${spaceReportsPath(spaceId)}/${String(reportId)}`, body),
  };""", """      api.patch<SpaceReport>(`${spaceReportsPath(spaceId)}/${String(reportId)}`, body),
    myReports: (query) => api.getPage<MyReport[]>('/me/reports', { params: query }),
  };""")

K = 'features\\data-reports\\hooks\\queryKeys.ts'
edit(K, """import type { SpaceReportsQuery } from '@masaha/shared/data-reports';""",
     """import type { MyReportsQuery, SpaceReportsQuery } from '@masaha/shared/data-reports';""")
edit(K, """    ['space', spaceId, 'dataReports', query] as const,
};""", """    ['space', spaceId, 'dataReports', query] as const,
  /** Every read of the user's own reports, under the session's scope: a new report reads them again. */
  mineAll: ['me', 'reports'] as const,
  /** One page of the user's own reports, by its whole query. */
  mine: (query: MyReportsQuery) => ['me', 'reports', query] as const,
};""")

F = 'test\\dataReport.ts'
edit(F, """import type { SpaceReport } from '@masaha/shared/data-reports';""",
     """import type { MyReport, SpaceReport } from '@masaha/shared/data-reports';""")
edit(F, """/** A page of reports, with its pagination. */""", """/**
 * A report as its reporter reads it: `spaceReport()`'s, about «Masaha Hub» (`masaha-hub`, id 7),
 * a space still listed; `space` overrides the space's fields.
 */
export function myReport(
  change: Partial<MyReport> = {},
  space: Partial<MyReport['space']> = {},
): MyReport {
  return {
    ...spaceReport(),
    space: { id: 7, slug: 'masaha-hub', nameEn: 'Masaha Hub', nameAr: 'مساحة هب', listed: true, ...space },
    ...change,
  };
}

/** A page of reports, with its pagination. */""")
print('ok')
