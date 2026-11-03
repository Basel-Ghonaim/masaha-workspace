import os
os.chdir(r'C:\dev\masaha\app-lane-w2\apps\web\src')
def edit(p,pairs):
    s=open(p,encoding='utf8').read()
    for a,b in pairs:
        assert s.count(a)==1,(p,a[:70]); s=s.replace(a,b)
    open(p,'w',encoding='utf8',newline='').write(s)

edit('features/space-links/components/owners-list/OwnersList.tsx',[
("import { Badge } from '@shared/design-system';","import { Badge, Button } from '@shared/design-system';"),
("import { useMemo } from 'react';","import { useMemo } from 'react';\nimport { Link } from 'react-router';"),
])
edit('features/space-links/components/users-list/UsersList.tsx',[
("""          id: 'actions',
          header: headers.actions,""","""          id: 'actions',
          header: () => <span className="sr-only">{headers.actions}</span>,"""),
])
edit('features/space-links/hooks/owners-list/useOwnersList.ts',[
("""    intro: lines.intro,
    columns: lines.columns,""","""    intro: lines.intro,
    columns: lines.columns,
    /** The empty list's way on: «إضافة مالك», the add sheet's own words (D6.11). */
    addOwner: copy.spaceLinks.addOwner.open,"""),
])
s=open('features/space-links/hooks/owners-list/useOwnersList.ts',encoding='utf8').read()
if 'const copy' not in s:
    print('NO COPY VAR'); print(s[:800])
edit('features/space-links/components/ListState.tsx',[
("""import { Button, EmptyState, SearchXIcon } from '@shared/design-system';
import type { ListStateView } from '../types/ListStateView';""","""import { Button, EmptyState, SearchXIcon } from '@shared/design-system';
import type { ReactNode } from 'react';
import type { ListStateView } from '../types/ListStateView';"""),
(""" * and Try again; no rows yet; or none matching the filters, with a button that clears them.
 */
export function ListState({ list }: { list: ListStateView }) {""",""" * and Try again; no rows yet, with the list's way on (`emptyAction`) when it has one; or none
 * matching the filters, with a button that clears them.
 */
export function ListState({ list, emptyAction }: { list: ListStateView; emptyAction?: ReactNode }) {"""),
("""  return <EmptyState title={list.empty.title} description={list.empty.description} />;""","""  return (
    <EmptyState title={list.empty.title} description={list.empty.description}>
      {emptyAction}
    </EmptyState>
  );"""),
])
# joined with its year
open('features/space-links/services/joinedOn.ts','w',encoding='utf8',newline='').write("""import type { Language } from '@shared/copy';

// Western digits and the Gregorian calendar in both languages (docs/frontend/localisation.md ›
// Formatting); dates fall on Gaza's day.
const LOCALES: Record<Language, string> = { ar: 'ar-u-nu-latn', en: 'en-GB' };

/**
 * When an account joined, as the users lists say it: the day, the month and the year, always —
 * «انضم» is a date to tell accounts apart by, this year's too (G29.1) — on Gaza's calendar.
 */
export function joinedOn(iso: string, language: Language): string {
  return new Intl.DateTimeFormat(LOCALES[language], {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    timeZone: 'Asia/Gaza',
  }).format(new Date(iso));
}
""")
edit('features/space-links/services/userRowView.ts',[
("import { updatedOn } from './updatedOn';","import { joinedOn } from './joinedOn';"),
("    joined: updatedOn(row.joinedAt, english ? 'en' : 'ar', now),","    joined: joinedOn(row.joinedAt, english ? 'en' : 'ar'),"),
])
