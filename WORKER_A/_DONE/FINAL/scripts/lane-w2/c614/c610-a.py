import os
os.chdir('C:/dev/masaha/app-lane-w2/apps/web/src')


def edit(p, pairs):
    s = open(p, encoding='utf8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)


def write(p, text):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf8', newline='').write(text)


D = 'features/data-reports/'
edit(D + 'repository/dataReportsRepository.ts', [
("""  /** The owner's decision of one of the space's reports, with its reply or none. */""",
 """  /** One of the space's reports, by its id (S5): never who reported it. */
  spaceReport(spaceId: number, reportId: number): Promise<SpaceReport>;
  /** The owner's decision of one of the space's reports, with its reply or none. */"""),
("""  /** The admin's decision of an unverified space's report, with its reply or none. */""",
 """  /** Any space's report, by its id (S5), with who reported it. */
  adminReport(reportId: number): Promise<AdminReport>;
  /** The admin's decision of an unverified space's report, with its reply or none. */"""),
("""    decideSpace: (spaceId, reportId, body) =>""",
 """    spaceReport: (spaceId, reportId) =>
      api.get<SpaceReport>(`${spaceReportsPath(spaceId)}/${String(reportId)}`),
    decideSpace: (spaceId, reportId, body) =>"""),
("""    decideAdmin: (reportId, body) =>""",
 """    adminReport: (reportId) => api.get<AdminReport>(`${ADMIN_REPORTS_PATH}/${String(reportId)}`),
    decideAdmin: (reportId, body) =>"""),
])

edit(D + 'hooks/queryKeys.ts', [
("""  /** Every read of the admin's reports: the admin's decision reads them again. */""",
 """  /** One of the space's reports, by its id: under the space's reports, so a decision reads it again. */
  spaceOne: (spaceId: number, reportId: number) =>
    ['space', spaceId, 'dataReports', 'one', reportId] as const,
  /** Every read of the admin's reports: the admin's decision reads them again. */"""),
("""  /** One page of every space's reports, by its whole query. */""",
 """  /** One report, by its id, under the admin's reports. */
  adminOne: (reportId: number) => ['admin', 'dataReports', 'one', reportId] as const,
  /** One page of every space's reports, by its whole query. */"""),
])

write(D + 'services/reportIdOf.ts', """/**
 * A report's id as an address names it (`?report=`, `?open=`): a positive whole number, or none for
 * anything else.
 */
export function reportIdOf(text: string | null): number | undefined {
  if (text === null || !/^[1-9]\\d*$/.test(text)) return undefined;
  const id = Number(text);
  return Number.isSafeInteger(id) ? id : undefined;
}
""")

write(D + 'services/reportIdOf.unit.test.ts', """import { describe, expect, it } from 'vitest';
import { reportIdOf } from './reportIdOf';

describe('reportIdOf', () => {
  it('reads a positive whole number', () => {
    expect(reportIdOf('42')).toBe(42);
  });

  it('reads nothing else', () => {
    for (const text of [null, '', '0', '-3', '4.5', '12a', '007', '99999999999999999999']) {
      expect(reportIdOf(text)).toBeUndefined();
    }
  });
});
""")

write(D + 'services/noticeGroup.ts', """import type { DataReportField } from '@masaha/shared/data-reports';

/** A section of the space's editor that a report notice can sit above. */
export type NoticeGroup = 'profile' | 'hours' | 'prices' | 'amenities' | 'contacts';

/**
 * The section a report's field is edited in: the place and «أخرى» in the profile's «المساحة», each
 * other field its own group's section.
 */
export const NOTICE_GROUPS: Record<DataReportField, NoticeGroup> = {
  LOCATION: 'profile',
  OTHER: 'profile',
  HOURS: 'hours',
  PRICES: 'prices',
  AMENITIES: 'amenities',
  CONTACT: 'contacts',
};
""")
print('ok')
