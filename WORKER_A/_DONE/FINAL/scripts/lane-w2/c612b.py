import os
os.chdir(r'C:\dev\masaha\app-lane-w2\apps\web\src')
def edit(p,pairs):
    s=open(p,encoding='utf8').read()
    for a,b in pairs:
        assert s.count(a)==1,(p,a[:70]); s=s.replace(a,b)
    open(p,'w',encoding='utf8',newline='').write(s)
edit('shared/copy/english/spaces.ts',[("""    /** A hiding's or a showing's toast: the opposite, sent at once (P9). */
    undo: 'Undo',
""",""),("""    /** Restores the space just deleted. */
    undo: 'Undo',""","""    /** Restores the space just deleted; on a hiding's or a showing's toast, the opposite (P9). */
    undo: 'Undo',""")])
s=open('shared/copy/arabic/spaces.ts',encoding='utf8').read()
a="""    shown: ({ name }: { name: string }) => `أصبحت ${name} ظاهرة`,
    undo: 'تراجع',
"""
assert s.count(a)==1
s=s.replace(a,"""    shown: ({ name }: { name: string }) => `أصبحت ${name} ظاهرة`,
""")
open('shared/copy/arabic/spaces.ts','w',encoding='utf8',newline='').write(s)

edit('features/space-links/components/admin-list/FiltersSheet.tsx',[
("""  const { sheet } = filters;

  return (
    <Sheet>""","""  const { sheet } = filters;
  const [open, setOpen] = useState(false);

  return (
    <Sheet open={open} onOpenChange={setOpen}>"""),
("""        <SheetFooter>
          <Button variant="outline" onClick={sheet.clear}>
            {sheet.clearLabel}
          </Button>
        </SheetFooter>""","""        <SheetFooter>
          {sheet.show !== null && (
            <Button
              size="lg"
              className="w-full"
              onClick={() => {
                setOpen(false);
              }}
            >
              {sheet.show}
            </Button>
          )}
          <Button variant="ghost" disabled={sheet.clearDisabled} onClick={sheet.clear}>
            {sheet.clearLabel}
          </Button>
        </SheetFooter>"""),
])
s=open('features/space-links/components/admin-list/FiltersSheet.tsx',encoding='utf8').read()
s="import { useState } from 'react';\n"+s
open('features/space-links/components/admin-list/FiltersSheet.tsx','w',encoding='utf8',newline='').write(s)

edit('features/spaces/types/EditorPlace.ts',[("""  amenitiesListLink: string;
  areaName:""","""  amenitiesListLink: string;
  /** The admin's reports of the space, where a fact its owner keeps is corrected (G26.8). */
  reportsLink: (spaceId: number) => string;
  areaName:""")])
edit('features/spaces/components/editor/VerifiedNotice.tsx',[
("""import type { ReactNode } from 'react';""","""import type { ReactNode } from 'react';
import { Link } from 'react-router';"""),
(""" * with the way to its page on the public site, in a new tab, and the owners' actions under it
 * (`children`).
 */""",""" * with the way to its page on the public site, in a new tab, «لتصحيح معلومة:» with the link to the
 * space's reports (`reports`), and the owners' actions under it (`children`).
 */"""),
("""  publicHref,
  children,
}: {
  words: { title: string; description: string; viewOnSite: string };
  publicHref: string;""","""  publicHref,
  reports,
  children,
}: {
  words: { title: string; description: string; viewOnSite: string; correct: string };
  publicHref: string;
  reports: { label: string; href: string };"""),
("""        </p>
        {children}""","""        </p>
        <p>
          {words.correct}{' '}
          <Link to={reports.href} className="underline underline-offset-4">
            {reports.label}
          </Link>
        </p>
        {children}"""),
])
edit('features/spaces/components/editor/SpaceEditor.tsx',[("""            <VerifiedNotice words={editor.notice.verified} publicHref={publicLink(space.slug)}>""","""            <VerifiedNotice
              words={editor.notice.verified}
              publicHref={publicLink(space.slug)}
              reports={{
                label: editor.notice.verified.reports({
                  space: isolate(spaceNameOf(space, english).text),
                }),
                href: place.reportsLink(space.id),
              }}
            >""")])
edit('pages/dashboard/admin/SpaceEditPage.tsx',[("""  amenitiesListLink: ADMIN_AMENITIES_PATH,""","""  amenitiesListLink: ADMIN_AMENITIES_PATH,
  reportsLink: (spaceId) => `${DASHBOARD_PATHS.admin}/reports?space=${String(spaceId)}`,""")])
