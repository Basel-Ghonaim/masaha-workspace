import os
os.chdir(r'C:\dev\masaha\app-lane-w2\apps\web\src')
def edit(p,pairs):
    s=open(p,encoding='utf8').read()
    for a,b in pairs:
        assert s.count(a)==1,(p,a[:70]); s=s.replace(a,b)
    open(p,'w',encoding='utf8',newline='').write(s)

# --- copy
edit('shared/copy/english/spaces.ts',[
("""    edit: 'Edit',
    hide: 'Hide',""","""    edit: 'Edit',
    /** A verified space's: its owner edits it, the admin views it. */
    view: 'View (its owner edits it)',
    hide: 'Hide',"""),
("""    cancel: 'Cancel',
""","""    cancel: 'Back',
"""),
("""    shown: ({ name }: { name: string }) => `${name} is visible again`,""","""    shown: ({ name }: { name: string }) => `${name} is visible again`,
    /** A hiding's or a showing's toast: the opposite, sent at once (P9). */
    undo: 'Undo',"""),
("""      viewOnSite: 'View on the site',
    },""","""      viewOnSite: 'View on the site',
      /** Before the space's reports, where a fact its owner keeps is corrected. */
      correct: 'To correct a fact:',
      reports: ({ space }: { space: string }) => `${space}’s reports`,
    },"""),
])
edit('shared/copy/arabic/spaces.ts',[
("""    edit: 'تعديل',
""","""    edit: 'تعديل',
    view: 'عرض (يعدّلها المالك)',
"""),
("""    cancel: 'إلغاء',
""","""    cancel: 'رجوع',
"""),
("""    shown: ({ name }: { name: string }) => `أصبحت ${name} ظاهرة`,""","""    shown: ({ name }: { name: string }) => `أصبحت ${name} ظاهرة`,
    undo: 'تراجع',"""),
("""      viewOnSite: 'عرض في الموقع',
    },""","""      viewOnSite: 'عرض في الموقع',
      correct: 'لتصحيح معلومة:',
      reports: ({ space }: { space: string }) => `بلاغات ${space}`,
    },"""),
])
edit('shared/copy/arabic/spaceLinks.ts',[("""    missing: ({ groups }: { groups: string }) => `غير مُدخلة: ${groups}`,""","""    missing: ({ groups }: { groups: string }) => `ناقصة: ${groups}`,""")])
s=open('shared/copy/english/spaceLinks.ts',encoding='utf8').read()
a="    clearFilters: 'Clear filters',\n"
i=s.index(a)  # the admin list's, the first
s=s[:i+len(a)]+"""    /** The phone's sheet's way back to the list, with the count the filters keep. */
    showResults: ({ count }: { count: number }) =>
      englishPlural(count, { one: 'Show 1 result', other: `Show ${String(count)} results` }),
"""+s[i+len(a):]
if "import { englishPlural }" not in s:
    s="import { englishPlural } from '../plural';\n"+s
open('shared/copy/english/spaceLinks.ts','w',encoding='utf8',newline='').write(s)
s=open('shared/copy/arabic/spaceLinks.ts',encoding='utf8').read()
a="    clearFilters: 'مسح الفلاتر',\n"
i=s.index(a)
s=s[:i+len(a)]+"""    showResults: ({ count }: { count: number }) =>
      arabicPlural(count, {
        zero: `عرض ${String(count)} نتيجة`,
        one: 'عرض نتيجة واحدة',
        two: 'عرض نتيجتين',
        few: `عرض ${String(count)} نتائج`,
        many: `عرض ${String(count)} نتيجة`,
        other: `عرض ${String(count)} نتيجة`,
      }),
"""+s[i+len(a):]
if "import { arabicPlural }" not in s:
    s="import { arabicPlural } from '../plural';\n"+s
open('shared/copy/arabic/spaceLinks.ts','w',encoding='utf8',newline='').write(s)

# --- the menu: view for a verified space
edit('features/spaces/types/SpaceRef.ts',[("""export type SpaceRef = Pick<AdminSpaceRow, 'id' | 'nameEn' | 'nameAr' | 'isHidden' | 'deletedAt'>;""","""export type SpaceRef = Pick<
  AdminSpaceRow,
  'id' | 'nameEn' | 'nameAr' | 'isHidden' | 'deletedAt' | 'isVerified'
>;""")])
edit('features/spaces/hooks/menu/useSpaceActionsMenu.ts',[("""    edit: lines.menu.edit,""","""    // A verified space's owner edits it: the admin's editor shows it read-only (G26.1).
    edit: space.isVerified ? lines.menu.view : lines.menu.edit,""")])

# --- hide/show: «تراجع»
edit('features/spaces/hooks/hide/useSetSpaceHidden.ts',[
(""" * Hides a space from the public, or shows it again, pending until the admin's list has arrived
 * again; then a toast says so by its name.""",""" * Hides a space from the public, or shows it again, pending until the admin's list has arrived
 * again; then a toast says so by its name, with «تراجع», which sends the opposite (P9: reversible,
 * no one else affected); an undo's own toast offers none."""),
("""  return useMutation<undefined, AppError, SpaceAction & { isHidden: boolean }>({""","""  const mutation = useMutation<
    undefined,
    AppError,
    SpaceAction & { isHidden: boolean; undoing?: boolean }
  >({"""),
("""    onSuccess: async (_answer, { name, isHidden }) => {
      await refresh();
      // Worded when it lands, in the language the interface speaks then.
      const { toasts } = currentCopy().spaces;
      toastDone(isHidden ? toasts.hidden : toasts.shown, name);
    },""","""    onSuccess: async (_answer, action) => {
      await refresh();
      // Worded when it lands, in the language the interface speaks then.
      const { toasts } = currentCopy().spaces;
      const { name, isHidden, undoing = false } = action;
      toastDone(
        isHidden ? toasts.hidden : toasts.shown,
        name,
        undoing
          ? undefined
          : {
              duration: UNDO_MS,
              action: {
                label: toasts.undo,
                onClick: () => {
                  mutation.mutate({ ...action, isHidden: !isHidden, undoing: true });
                },
              },
            },
      );
    },"""),
])
s=open('features/spaces/hooks/hide/useSetSpaceHidden.ts',encoding='utf8').read()
s=s.replace("""    },
  });
}""","""    },
  });
  return mutation;
}""")
s=s.replace("const repository = createSpacesRepository();","const repository = createSpacesRepository();\n\n/** How long «تراجع» is offered: long enough to read the toast and change one's mind. */\nconst UNDO_MS = 10_000;",1)
open('features/spaces/hooks/hide/useSetSpaceHidden.ts','w',encoding='utf8',newline='').write(s)

# --- the phone's sheet
edit('features/space-links/hooks/admin-list/useAdminSpacesList.ts',[("""        clearLabel: lines.clearFilters,
        clear: filters.clearFilters,
      },""","""        clearLabel: lines.clearFilters,
        clear: filters.clearFilters,
        /** «مسح الفلاتر» is unavailable while none applies. */
        clearDisabled: filters.applied === 0,
        /** «عرض {n} نتيجة», which closes the sheet on the list the filters leave. */
        show:
          answer === undefined ? null : lines.showResults({ count: answer.meta.totalRecords }),
      },""")])
edit('features/space-links/components/admin-list/FiltersSheet.tsx',[
("""import {""","""import { useState } from 'react';
import {"""),
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

# --- the verified notice
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
