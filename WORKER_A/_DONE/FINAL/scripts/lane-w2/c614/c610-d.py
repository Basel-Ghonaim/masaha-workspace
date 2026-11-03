import os
os.chdir('C:/dev/masaha/app-lane-w2/apps/web/src/pages/dashboard')


def edit(p, pairs):
    s = open(p, encoding='utf8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)


edit('space/ProfilePage.tsx', [
("""import { AmenityChecklist, AreaSelect } from '@features/lookups';
import { SpaceEditor, type AmenitiesField, type AreaField } from '@features/spaces';
import { NotFoundState, parseSpaceId, publicSpacePath } from '@shared/routing';
import { useParams } from 'react-router';""", """import type { FactGroup } from '@masaha/shared/spaces';
import { ReportNotice, reportIdOf, useReportNotice } from '@features/data-reports';
import { AmenityChecklist, AreaSelect } from '@features/lookups';
import { SpaceEditor, type AmenitiesField, type AreaField } from '@features/spaces';
import { NotFoundState, parseSpaceId, publicSpacePath } from '@shared/routing';
import { useParams, useSearchParams } from 'react-router';"""),
(""" * that leads to Packages & prices. The guard has checked the space's id and the owner's role.
 */""", """ * that leads to Packages & prices. A report the address names (`?report=`) shows its notice, from
 * `data-reports`, above the section its field is edited in (D6.8). The guard has checked the space's
 * id and the owner's role.
 */"""),
("""        // Another space is another editor: nothing typed for one carries over to the next.
        <SpaceEditor
          key={spaceId}
          spaceId={spaceId}
          place={{ kind: 'owner', pricesLink: spacePagePath(spaceId, 'packages') }}
          areaField={areaField}
          amenitiesField={amenitiesField}
          publicLink={publicSpacePath}
        />
      )}
    </>
  );
}""", """        // Another space is another editor: nothing typed for one carries over to the next.
        <Profile key={spaceId} spaceId={spaceId} />
      )}
    </>
  );
}

/** One space's editor, with the notice of the report the address names. */
function Profile({ spaceId }: { spaceId: number }) {
  const [params] = useSearchParams();
  const notice = useReportNotice(
    { audience: 'owner', spaceId, reportsPath: spacePagePath(spaceId, 'reports') },
    reportIdOf(params.get('report')),
  );
  const noticeFor = (group: FactGroup) =>
    notice?.group === group ? <ReportNotice view={notice} /> : null;

  return (
    <SpaceEditor
      spaceId={spaceId}
      place={{ kind: 'owner', pricesLink: spacePagePath(spaceId, 'packages') }}
      areaField={areaField}
      amenitiesField={amenitiesField}
      publicLink={publicSpacePath}
      noticeFor={noticeFor}
    />
  );
}"""),
])

edit('space/PackagesPage.tsx', [
("""import { PackagesSection } from '@features/packages';""",
 """import { ReportNotice, reportIdOf, useReportNotice } from '@features/data-reports';
import { PackagesSection } from '@features/packages';"""),
("""import { useParams } from 'react-router';""", """import { useParams, useSearchParams } from 'react-router';"""),
(""" * them. Both lines for a space with no shift lead to the opening hours on the profile. The guard has
 * checked the space's id and the owner's role.""", """ * them. Both lines for a space with no shift lead to the opening hours on the profile. A prices
 * report the address names (`?report=`) shows its notice above the prices (D6.8). The guard has
 * checked the space's id and the owner's role."""),
("""  const copy = useCopy();

  return (
    <div className="flex flex-col gap-8">
      <p className="text-body-sm text-muted-foreground">{copy.packages.pageLine}</p>
      <SpacePricesEditor""", """  const copy = useCopy();
  const [params] = useSearchParams();
  const notice = useReportNotice(
    { audience: 'owner', spaceId, reportsPath: spacePagePath(spaceId, 'reports') },
    reportIdOf(params.get('report')),
  );

  return (
    <div className="flex flex-col gap-8">
      <p className="text-body-sm text-muted-foreground">{copy.packages.pageLine}</p>
      {notice?.group === 'prices' && <ReportNotice view={notice} />}
      <SpacePricesEditor"""),
])

edit('admin/SpaceEditPage.tsx', [
("""import { AmenityChecklist, AmenityNames, AreaName, AreaSelect } from '@features/lookups';""",
 """import type { FactGroup } from '@masaha/shared/spaces';
import { ReportNotice, reportIdOf, useReportNotice } from '@features/data-reports';
import { AmenityChecklist, AmenityNames, AreaName, AreaSelect } from '@features/lookups';"""),
("""import { Link, useParams } from 'react-router';""", """import { Link, useParams, useSearchParams } from 'react-router';"""),
("""  reportsLink: (spaceId) => `${DASHBOARD_PATHS.admin}/reports?space=${String(spaceId)}`,""",
 """  reportsLink: (spaceId) => `${ADMIN_REPORTS_PATH}?space=${String(spaceId)}`,"""),
("""/** The editor's area field, from""", """/** The admin's reports list. */
const ADMIN_REPORTS_PATH = `${DASHBOARD_PATHS.admin}/reports`;

/** The editor's area field, from"""),
(""" * or link one to an unverified space, a new owner being added on the owners page.
 */""", """ * or link one to an unverified space, a new owner being added on the owners page. A report the
 * address names (`?report=`) shows its notice, from `data-reports`, above its field's section (D6.8).
 */"""),
("""  const name = useSpaceName(spaceId);
  useRecordTitle(name);
""", """  const name = useSpaceName(spaceId);
  useRecordTitle(name);
  const [params] = useSearchParams();
  const notice = useReportNotice(
    { audience: 'admin', spaceId, reportsPath: ADMIN_REPORTS_PATH },
    reportIdOf(params.get('report')),
  );
  const noticeFor = (group: FactGroup) =>
    notice?.group === group ? <ReportNotice view={notice} /> : null;
"""),
("""          publicLink={publicSpacePath}
        />
      </div>""", """          publicLink={publicSpacePath}
          noticeFor={noticeFor}
        />
      </div>"""),
])
print('ok')
