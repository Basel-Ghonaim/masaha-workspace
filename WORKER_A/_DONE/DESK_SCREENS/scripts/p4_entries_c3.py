"""Commit 3's entries: every place that opens the subscription sheet."""
W = 'C:/dev/masaha/app/apps/web/src/'


def edit(path, pairs):
    p = W + path
    s = open(p, encoding='utf-8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old[:80], s.count(old))
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)


edit('features/desk/types/SheetEntry.ts', [
    ("import type { CustomerBalance } from '@masaha/shared/payments';\n", ''),
    (""" * Where the subscription sheet opens, with what its entry knows: a new customer (a typed name or
 * phone, from the desk's search), or a known customer's new subscription.
 */""", """ * Where the subscription sheet opens, with what its entry knows: a new customer (a typed name or
 * phone, from the desk's search), or a known customer's new subscription, with what they owe as the
 * entry read it (their file, read when the sheet opens, says it again).
 */"""),
    ("  | { mode: 'subscribe'; customer: Customer & CustomerBalance };",
     "  | { mode: 'subscribe'; customer: Customer & { debtAgorot: number } };"),
])

edit('features/desk/components/menu/CustomerMenu.tsx', [
    ("""  file: { label: string; to: string } | null;
  edit: { label: string; run: () => void };""", """  file: { label: string; to: string } | null;
  /** «اشتراك جديد»: the subscription sheet for this customer. */
  subscribe: { label: string; run: () => void };
  edit: { label: string; run: () => void };"""),
    (""" * A customer's «⋯» (DI-39): a quiet icon trigger and its menu, both named by the customer; «ملف
 * الزبون» where it leads elsewhere, «تعديل البيانات», and the owner's «أرشفة…», destructive (DI-46).""",
     """ * A customer's «⋯» (DI-39): a quiet icon trigger and its menu, both named by the customer; «ملف
 * الزبون» where it leads elsewhere, «اشتراك جديد», «تعديل البيانات», and the owner's «أرشفة…»,
 * destructive (DI-46)."""),
    ("""        <DropdownMenuItem onSelect={menu.edit.run}>{menu.edit.label}</DropdownMenuItem>""",
     """        <DropdownMenuItem onSelect={menu.subscribe.run}>{menu.subscribe.label}</DropdownMenuItem>
        <DropdownMenuItem onSelect={menu.edit.run}>{menu.edit.label}</DropdownMenuItem>"""),
])

edit('features/desk/components/menu/CustomerMenu.component.test.tsx', [
    ("""            file: { label: 'Customer file', to: '/file/4' },
""", """            file: { label: 'Customer file', to: '/file/4' },
            subscribe: { label: 'New subscription', run: vi.fn() },
"""),
])

edit('features/desk/components/menu/CustomerActions.tsx', [
    ("""import { isolate } from '@shared/localisation';""", """import { isolate } from '@shared/localisation';"""),
    ("""import { useArchiveFlow } from '../../hooks/archive/useArchiveFlow';""",
     """import { useArchiveFlow } from '../../hooks/archive/useArchiveFlow';
import type { SheetEntry } from '../../types/SheetEntry';"""),
    (""" * the file's header: their «⋯» («ملف الزبون» where `fileLink` leads, «تعديل البيانات», the owner's
 * «أرشفة…»), with its dialogs;""", """ * the file's header: their «⋯» («ملف الزبون» where `fileLink` leads, «اشتراك جديد» opening the
 * page's subscription sheet, «تعديل البيانات», the owner's «أرشفة…»), with its dialogs;"""),
    ("""  /** The customer's file, where the menu offers it; none in the file itself. */
  fileLink: string | null;
}) {
  const words = useCopy().desk.customer.menu;""", """  /** The customer's file, where the menu offers it; none in the file itself. */
  fileLink: string | null;
  /** Opens the page's subscription sheet. */
  subscribe: (entry: SheetEntry) => void;
}) {
  const copy = useCopy();
  const words = copy.desk.customer.menu;"""),
    ("""  owner,
  fileLink,
}: {""", """  owner,
  fileLink,
  subscribe,
}: {"""),
    ("""          file: fileLink === null ? null : { label: words.file, to: fileLink },
""", """          file: fileLink === null ? null : { label: words.file, to: fileLink },
          subscribe: {
            label: copy.desk.sheet.entry.subscribe,
            run: () => {
              subscribe({ mode: 'subscribe', customer: { ...customer, debtAgorot } });
            },
          },
"""),
])

edit('features/desk/components/menu/CustomerActions.component.test.tsx', [
    ("""import { afterEach, beforeEach, describe, expect, it } from 'vitest';""",
     """import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';"""),
    ("""            fileLink={null}
""", """            fileLink={null}
            subscribe={vi.fn()}
"""),
])

edit('features/desk/components/card/CustomerCard.tsx', [
    ("""import { useSubscriberCheckIn } from '../../hooks/subscriber/useSubscriberCheckIn';""",
     """import { useSubscriberCheckIn } from '../../hooks/subscriber/useSubscriberCheckIn';
import type { SheetEntry } from '../../types/SheetEntry';"""),
    ("""  /** The card's «⋯»: whether the caller is the owner (S5), and where a customer's file is. */
  menu: { owner: boolean; fileLink: (customerId: number) => string };""",
     """  /**
   * The card's «⋯»: whether the caller is the owner (S5), where a customer's file is, and the page's
   * subscription sheet.
   */
  menu: {
    owner: boolean;
    fileLink: (customerId: number) => string;
    subscribe: (entry: SheetEntry) => void;
  };"""),
    ("""            fileLink={menu.fileLink(row.id)}
""", """            fileLink={menu.fileLink(row.id)}
            subscribe={menu.subscribe}
"""),
])

edit('features/desk/components/customers/CustomersList.tsx', [
    ("""import { CustomerActions } from '../menu/CustomerActions';""",
     """import type { SheetEntry } from '../../types/SheetEntry';
import { CustomerActions } from '../menu/CustomerActions';"""),
    ("""  owner,
  fileLink,
}: {
  spaceId: number;
  /** The owner's list offers «مؤرشف»; the server decides (S5). */
  owner: boolean;
  /** A customer's file, by id, as the page routes it. */
  fileLink: (customerId: number) => string;
}) {""", """  owner,
  fileLink,
  subscribe,
}: {
  spaceId: number;
  /** The owner's list offers «مؤرشف»; the server decides (S5). */
  owner: boolean;
  /** A customer's file, by id, as the page routes it. */
  fileLink: (customerId: number) => string;
  /** Opens the page's subscription sheet, from a customer's «⋯». */
  subscribe: (entry: SheetEntry) => void;
}) {"""),
    ("""              owner={owner}
              fileLink={fileLink(info.row.original.id)}
            />""", """              owner={owner}
              fileLink={fileLink(info.row.original.id)}
              subscribe={subscribe}
            />"""),
    ("""    [headers, fileLink, spaceId, owner],""", """    [headers, fileLink, spaceId, owner, subscribe],"""),
    ("""              owner={owner}
              fileLink={fileLink(row.id)}
            />""", """              owner={owner}
              fileLink={fileLink(row.id)}
              subscribe={subscribe}
            />"""),
])

edit('features/desk/components/customers/CustomersList.component.test.tsx', [
    ("""<CustomersList spaceId={7} owner={owner} fileLink={(id) => `/file/${String(id)}`} />""",
     """<CustomersList
            spaceId={7}
            owner={owner}
            fileLink={(id) => `/file/${String(id)}`}
            subscribe={() => undefined}
          />"""),
])

edit('features/desk/components/file/CustomerFile.tsx', [
    ("""import { CustomerActions } from '../menu/CustomerActions';""",
     """import type { SheetEntry } from '../../types/SheetEntry';
import { CustomerActions } from '../menu/CustomerActions';"""),
    ("""  owner,
}: {
  spaceId: number;
  customerId: number;
  /** The owner's header offers the archive and the restore; the server decides (S5). */
  owner: boolean;
}) {""", """  owner,
  subscribe,
}: {
  spaceId: number;
  customerId: number;
  /** The owner's header offers the archive and the restore; the server decides (S5). */
  owner: boolean;
  /** Opens the page's subscription sheet, from the header's «⋯». */
  subscribe: (entry: SheetEntry) => void;
}) {"""),
    ("""            owner={owner}
            fileLink={null}
""", """            owner={owner}
            fileLink={null}
            subscribe={subscribe}
"""),
])

for path in ['features/desk/components/file/CustomerFile.component.test.tsx',
             'features/desk/components/statement/Statement.component.test.tsx']:
    edit(path, [("<CustomerFile spaceId={7} customerId={4} owner />",
                 "<CustomerFile spaceId={7} customerId={4} owner subscribe={() => undefined} />")])

for path in ['features/desk/components/search/DeskSearch.component.test.tsx',
             'features/desk/hooks/subscriber/useSubscriberCheckIn.component.test.tsx']:
    edit(path, [("const MENU = { owner: false, fileLink: (id: number) => `/file/${String(id)}` };",
                 """const MENU = {
  owner: false,
  fileLink: (id: number) => `/file/${String(id)}`,
  subscribe: () => undefined,
};""")])

print('ok')
