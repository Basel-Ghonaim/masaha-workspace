import os
os.chdir('C:/dev/masaha/app-lane-w2/apps/web/src')


def edit(p, pairs):
    s = open(p, encoding='utf8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)


def write(p, text):
    open(p, 'w', encoding='utf8', newline='').write(text)


# The link builders, pure, in fieldSections.ts.
edit('pages/dashboard/fieldSections.ts', [
("""import type { DataReportField } from '@masaha/shared/data-reports';
""", """import type { DataReportField } from '@masaha/shared/data-reports';
import { adminSpacePath, spacePagePath } from './navigation';
"""),
])
s = open('pages/dashboard/fieldSections.ts', encoding='utf8', newline='').read()
s += """
/** The hash a report's link lands on: its field's section, or the report's notice for «أخرى». */
const landingOf = (field: DataReportField) => `#${FIELD_SECTIONS[field] ?? 'report'}`;

/**
 * The owner's «تعديل الحقل»: where the report's field is edited — the prices on Packages & prices,
 * the other groups in the space profile — carrying the report, so its notice shows there (D6.8).
 */
export function ownerFieldLink(spaceId: number, field: DataReportField, reportId: number): string {
  const page = spacePagePath(spaceId, field === 'PRICES' ? 'packages' : 'profile');
  return `${page}?report=${String(reportId)}${landingOf(field)}`;
}

/**
 * The admin's link to a space's editor; with a report, its «تعديل الحقل», landing on its field's
 * section and carrying the report (D6.8).
 */
export function adminEditorLink(
  spaceId: number,
  field?: DataReportField,
  reportId?: number,
): string {
  const editor = adminSpacePath(spaceId);
  if (field === undefined || reportId === undefined) return editor;
  return `${editor}?report=${String(reportId)}${landingOf(field)}`;
}
"""
write('pages/dashboard/fieldSections.ts', s)

edit('pages/dashboard/admin/DataReportsPage.tsx', [
("""import type { DataReportField } from '@masaha/shared/data-reports';
""", ""),
("""import { FIELD_SECTIONS } from '../fieldSections';
import { adminSpacePath } from '../navigation';
""", """import { adminEditorLink } from '../fieldSections';
"""),
("""/**
 * A space's editor; for a report, the section where its field is edited (DI-33), carrying the report
 * so its notice shows there (`?report={id}`, D6.8).
 */
const editorLink = (spaceId: number, field?: DataReportField, reportId?: number) => {
  const editor = adminSpacePath(spaceId);
  if (field === undefined || reportId === undefined) return editor;
  return `${editor}?report=${String(reportId)}#${FIELD_SECTIONS[field] ?? 'report'}`;
};
""", ""),
("""<AdminReportsList spaceFilter={spaceFilter} editorLink={editorLink} />""",
 """<AdminReportsList spaceFilter={spaceFilter} editorLink={adminEditorLink} />"""),
])

edit('pages/dashboard/space/reports/DataReportsPage.tsx', [
("""import { FIELD_SECTIONS } from '../../fieldSections';
import { spacePagePath } from '../../navigation';
""", """import { ownerFieldLink } from '../../fieldSections';
"""),
("""  // Each carries the report, so its notice shows where the field is edited (`?report={id}`, D6.8).
  const fieldLink = useCallback(
    (field: DataReportField, reportId: number) => {
      const report = `?report=${String(reportId)}`;
      if (field === 'PRICES') return `${spacePagePath(spaceId, 'packages')}${report}#prices`;
      return `${spacePagePath(spaceId, 'profile')}${report}#${FIELD_SECTIONS[field] ?? 'report'}`;
    },
    [spaceId],
  );""", """  const fieldLink = useCallback(
    (field: DataReportField, reportId: number) => ownerFieldLink(spaceId, field, reportId),
    [spaceId],
  );"""),
])

write('pages/dashboard/fieldSections.unit.test.ts', """import { describe, expect, it } from 'vitest';
import { adminEditorLink, ownerFieldLink } from './fieldSections';

describe('«تعديل الحقل» carries ?report=', () => {
  it('leads the owner to the field’s section, the prices to Packages & prices, «أخرى» to the notice', () => {
    expect(ownerFieldLink(7, 'HOURS', 41)).toBe('/dashboard/spaces/7/profile?report=41#hours');
    expect(ownerFieldLink(7, 'LOCATION', 41)).toBe(
      '/dashboard/spaces/7/profile?report=41#location',
    );
    expect(ownerFieldLink(7, 'PRICES', 41)).toBe('/dashboard/spaces/7/packages?report=41#prices');
    expect(ownerFieldLink(7, 'OTHER', 41)).toBe('/dashboard/spaces/7/profile?report=41#report');
  });

  it('leads the admin to the editor’s section with the report, and a space alone to its editor', () => {
    expect(adminEditorLink(7, 'AMENITIES', 41)).toBe(
      '/dashboard/admin/spaces/7?report=41#amenities',
    );
    expect(adminEditorLink(7, 'OTHER', 41)).toBe('/dashboard/admin/spaces/7?report=41#report');
    expect(adminEditorLink(7)).toBe('/dashboard/admin/spaces/7');
  });
});
""")
print('ok')
