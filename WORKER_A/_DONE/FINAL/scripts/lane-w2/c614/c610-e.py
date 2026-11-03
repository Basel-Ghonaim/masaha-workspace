import os
os.chdir('C:/dev/masaha/app-lane-w2/apps/web/src')


def edit(p, pairs):
    s = open(p, encoding='utf8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)


D = 'features/data-reports/'
edit(D + 'hooks/space/useSpaceReports.ts', [
("""import { useState } from 'react';""", """import { useState } from 'react';
import { useSearchParams } from 'react-router';"""),
("""import { fieldLabel, messageView, reportDay, statusView } from '../../services/reportView';""",
 """import { reportIdOf } from '../../services/reportIdOf';
import { fieldLabel, messageView, reportDay, statusView } from '../../services/reportView';"""),
(""" * is open — decided elsewhere, met under «جديدة» — it is read from the first page of «الكل».
 */""", """ * is open — decided elsewhere, met under «جديدة» — it is read from the first page of «الكل». A report
 * the address names (`?open=`, the notice's «فتح البلاغ للرد») opens in the sheet, read by its id when
 * the page does not show it; closing the sheet takes `?open` off the address.
 */"""),
("""  const [opened, setOpened] = useState<SpaceReport | null>(null);
  const now = new Date();
  const reports = answer?.data ?? [];""", """  const [clicked, setClicked] = useState<SpaceReport | null>(null);
  const [params, setParams] = useSearchParams();
  const addressed = reportIdOf(params.get('open'));
  const now = new Date();
  const reports = answer?.data ?? [];
  // The report the address names, from the page when it shows it, else read by its id (S5).
  const addressedOnPage = reports.find((report) => report.id === addressed);
  const one = useQuery<SpaceReport, AppError>({
    queryKey: dataReportsKeys.spaceOne(spaceId, addressed ?? 0),
    queryFn: () => repository.spaceReport(spaceId, addressed ?? 0),
    enabled:
      clicked === null &&
      addressed !== undefined &&
      answer !== undefined &&
      addressedOnPage === undefined,
    retry: false,
  });
  const opened =
    clicked ?? (addressed === undefined ? null : (addressedOnPage ?? one.data ?? null));
  const setOpened = setClicked;"""),
("""    close: () => {
      setOpened(null);
    },""", """    close: () => {
      setOpened(null);
      if (addressed !== undefined) {
        setParams(
          (current) => {
            const next = new URLSearchParams(current);
            next.delete('open');
            return next;
          },
          { replace: true },
        );
      }
    },"""),
])

edit(D + 'hooks/admin/useAdminReports.ts', [
("""  /** A space's editor, and the section where a field group is edited in it, as the page routes it. */
  editorLink: (spaceId: number, field?: DataReportField) => string;
}) {""", """  /**
   * A space's editor; with a report's field and id, the section where its field is edited, carrying
   * the report (`?report=`), as the page routes it.
   */
  editorLink: (spaceId: number, field?: DataReportField, reportId?: number) => string;
}) {"""),
("""  const [opened, setOpened] = useState<AdminReport | null>(null);
  const now = new Date();
  const english = language === 'en';
  const reports = answer?.data ?? [];""", """  const [clicked, setClicked] = useState<AdminReport | null>(null);
  const [params, setParams] = useSearchParams();
  const addressed = reportIdOf(params.get('open'));
  const now = new Date();
  const english = language === 'en';
  const reports = answer?.data ?? [];
  // The report the address names, from the page when it shows it, else read by its id (S5).
  const addressedOnPage = reports.find((report) => report.id === addressed);
  const one = useQuery<AdminReport, AppError>({
    queryKey: dataReportsKeys.adminOne(addressed ?? 0),
    queryFn: () => repository.adminReport(addressed ?? 0),
    enabled:
      clicked === null &&
      addressed !== undefined &&
      answer !== undefined &&
      addressedOnPage === undefined,
    retry: false,
  });
  const opened =
    clicked ?? (addressed === undefined ? null : (addressedOnPage ?? one.data ?? null));
  const setOpened = setClicked;"""),
("""        : editorLink(target.space.id, target.field),
    close: () => {
      setOpened(null);
    },""", """        : editorLink(target.space.id, target.field, target.id),
    close: () => {
      setOpened(null);
      if (addressed !== undefined) {
        setParams(
          (current) => {
            const next = new URLSearchParams(current);
            next.delete('open');
            return next;
          },
          { replace: true },
        );
      }
    },"""),
])
s = open(D + 'hooks/admin/useAdminReports.ts', encoding='utf8').read()
print('useSearchParams import present:', "from 'react-router'" in s, 'reportIdOf' in s.split('export function')[0])

edit(D + 'components/space/SpaceReportsList.tsx', [
("""  fieldLink: (field: DataReportField) => string;""", """  /** Where a report's field is edited, carrying the report (`?report=`), as the page routes it. */
  fieldLink: (field: DataReportField, reportId: number) => string;"""),
("""          editLink={fieldLink(list.sheet.report.field)}""", """          editLink={fieldLink(list.sheet.report.field, list.sheet.report.id)}"""),
])
edit(D + 'components/admin/AdminReportsList.tsx', [
("""  /** A space's editor, and the section where a field group is edited in it, as the page routes it. */
  editorLink: (spaceId: number, field?: DataReportField) => string;
}) {""", """  /**
   * A space's editor; with a report's field and id, the section where its field is edited, carrying
   * the report (`?report=`), as the page routes it.
   */
  editorLink: (spaceId: number, field?: DataReportField, reportId?: number) => string;
}) {"""),
])

edit('pages/dashboard/admin/DataReportsPage.tsx', [
("""/** A space's editor, and the section where a field group is edited in it (DI-33). */
const editorLink = (spaceId: number, field?: DataReportField) => {
  const section = field === undefined ? null : FIELD_SECTIONS[field];
  return section === null ? adminSpacePath(spaceId) : `${adminSpacePath(spaceId)}#${section}`;
};""", """/**
 * A space's editor; for a report, the section where its field is edited (DI-33), carrying the report
 * so its notice shows there (`?report={id}`, D6.8).
 */
const editorLink = (spaceId: number, field?: DataReportField, reportId?: number) => {
  const editor = adminSpacePath(spaceId);
  if (field === undefined || reportId === undefined) return editor;
  return `${editor}?report=${String(reportId)}#${FIELD_SECTIONS[field] ?? 'report'}`;
};"""),
])
edit('pages/dashboard/space/reports/DataReportsPage.tsx', [
("""  const fieldLink = useCallback(
    (field: DataReportField) => {
      if (field === 'PRICES') return spacePagePath(spaceId, 'packages');
      const profile = spacePagePath(spaceId, 'profile');
      const section = FIELD_SECTIONS[field];
      return section === null ? profile : `${profile}#${section}`;
    },
    [spaceId],
  );""", """  // Each carries the report, so its notice shows where the field is edited (`?report={id}`, D6.8).
  const fieldLink = useCallback(
    (field: DataReportField, reportId: number) => {
      const report = `?report=${String(reportId)}`;
      if (field === 'PRICES') return `${spacePagePath(spaceId, 'packages')}${report}#prices`;
      return `${spacePagePath(spaceId, 'profile')}${report}#${FIELD_SECTIONS[field] ?? 'report'}`;
    },
    [spaceId],
  );"""),
])
edit('pages/dashboard/fieldSections.ts', [
("""/**
 * The space editor's section where each field group of a data report is edited — its cards'
 * anchors — for «تعديل الحقل» (DI-33); «أخرى» has none, and leads to the editor itself.
 */""", """/**
 * The space editor's section where each field group of a data report is edited — its cards'
 * anchors — for «تعديل الحقل» (DI-33); «أخرى» has none, and lands on the report's notice
 * (`#report`) above the profile.
 */"""),
])
print('ok')
