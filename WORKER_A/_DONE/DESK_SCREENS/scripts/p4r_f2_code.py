W = 'C:/dev/masaha/app/apps/web/src/'


def edit(path, pairs):
    p = W + path
    s = open(p, encoding='utf-8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old[:90], s.count(old))
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)


edit('features/desk/types/SheetEntry.ts', [
    ("""  | { mode: 'renew'; customer: Customer & { debtAgorot: number }; renews: SubscriptionState };""",
     """  | { mode: 'renew'; customer: Customer & { debtAgorot: number }; renews: SubscriptionState };

/**
 * Opens the page's subscription sheet for `entry`; `from` is the control the focus returns to once it
 * closes (a menu's trigger when it opened from one of its items, which leave the page).
 */
export type OpenSheet = (entry: SheetEntry, from: HTMLElement | null) => void;"""),
])

edit('features/desk/index.ts', [
    ("export type { SheetEntry } from './types/SheetEntry';",
     "export type { OpenSheet, SheetEntry } from './types/SheetEntry';"),
])

edit('features/desk/components/menu/CustomerActions.tsx', [
    ("import type { SheetEntry } from '../../types/SheetEntry';",
     "import type { OpenSheet } from '../../types/SheetEntry';"),
    ("""  /** Opens the page's subscription sheet. */
  subscribe: (entry: SheetEntry) => void;""",
     """  /** Opens the page's subscription sheet, the focus coming back to «⋯». */
  subscribe: OpenSheet;"""),
    ("""              subscribe({ mode: 'subscribe', customer: { ...customer, debtAgorot } });""",
     """              subscribe({ mode: 'subscribe', customer: { ...customer, debtAgorot } }, trigger.current);"""),
])

edit('features/desk/components/card/CustomerCard.tsx', [
    ("import type { SheetEntry } from '../../types/SheetEntry';",
     "import type { OpenSheet } from '../../types/SheetEntry';"),
    ("    subscribe: (entry: SheetEntry) => void;", "    subscribe: OpenSheet;"),
])

edit('features/desk/components/search/DeskSearch.tsx', [
    ("import type { SheetEntry } from '../../types/SheetEntry';",
     "import type { OpenSheet } from '../../types/SheetEntry';"),
    ("    subscribe: (entry: SheetEntry) => void;", "    subscribe: OpenSheet;"),
    ("""            onClick={() => {
              menu.subscribe(newCustomer.entry);
            }}""", """            onClick={(event) => {
              menu.subscribe(newCustomer.entry, event.currentTarget);
            }}"""),
])

edit('features/desk/components/customers/CustomersList.tsx', [
    ("import type { SheetEntry } from '../../types/SheetEntry';",
     "import type { OpenSheet } from '../../types/SheetEntry';"),
    ("  subscribe: (entry: SheetEntry) => void;", "  subscribe: OpenSheet;"),
])

edit('features/desk/components/file/CustomerFile.tsx', [
    ("import type { SheetEntry } from '../../types/SheetEntry';",
     "import type { OpenSheet } from '../../types/SheetEntry';"),
    ("  subscribe: (entry: SheetEntry) => void;", "  subscribe: OpenSheet;"),
    ("""          run: () => {
            subscribe({
              mode: 'renew',
              customer: { ...header.customer, debtAgorot: header.debtAgorot },
              renews: subscription,
            });
          },""", """          run: (from: HTMLElement) => {
            subscribe(
              {
                mode: 'renew',
                customer: { ...header.customer, debtAgorot: header.debtAgorot },
                renews: subscription,
              },
              from,
            );
          },"""),
])

edit('features/desk/components/file/SubscriptionCard.tsx', [
    ("""  renew: { label: string; run: () => void } | null;""",
     """  renew: { label: string; run: (from: HTMLElement) => void } | null;"""),
    ("""          <Button variant="secondary" onClick={renew.run}>""",
     """          <Button
            variant="secondary"
            onClick={(event) => {
              renew.run(event.currentTarget);
            }}
          >"""),
])

edit('features/desk/components/sheet/SubscriptionSheet.tsx', [
    (""" * keys are that opening's); while it is sent nothing closes it; a failure shows above the footer,
 * every value kept, and a customer saved with the subscription refused says so (DI-37). Closed, the
 * focus returns to what opened it.
 */""", """ * keys are that opening's); while it is sent nothing closes it; a failure shows above the footer,
 * every value kept, and a customer saved with the subscription refused says so (DI-37). Closed, the
 * focus goes where `returnFocus` says while it is on the page — the control that opened it, or the
 * menu's trigger when a menu item did — else where Radix returns it.
 */"""),
    ("""  choices,
  onClose,
}: {""", """  choices,
  returnFocus,
  onClose,
}: {"""),
    ("""  choices: SheetChoices;
  onClose: () => void;
}) {""", """  choices: SheetChoices;
  returnFocus: () => HTMLElement | null;
  onClose: () => void;
}) {"""),
    ("""        onEscapeKeyDown={(event) => {
          if (busy) event.preventDefault();
        }}
      >""", """        onEscapeKeyDown={(event) => {
          if (busy) event.preventDefault();
        }}
        onCloseAutoFocus={(event) => {
          const target = returnFocus();
          if (target?.isConnected === true) {
            event.preventDefault();
            target.focus();
          }
        }}
      >"""),
])

edit('pages/dashboard/space/useSheetOpener.ts', [
    ("import type { SheetEntry } from '@features/desk';", "import type { OpenSheet, SheetEntry } from '@features/desk';"),
    ("import { useCallback, useState } from 'react';", "import { useCallback, useRef, useState } from 'react';"),
    (""" * The page's one subscription sheet, opened from any of its entries: what the entry knew, and the
 * opening's count, so each opening mounts a new sheet with new keys (S4).
 */""", """ * The page's one subscription sheet, opened from any of its entries: what the entry knew, the
 * opening's count, so each opening mounts a new sheet with new keys (S4), and the control the focus
 * returns to once it closes.
 */"""),
    ("""  const [opening, setOpening] = useState(0);
  const open = useCallback((next: SheetEntry) => {
    setEntry(next);
    setOpening((count) => count + 1);
  }, []);""", """  const [opening, setOpening] = useState(0);
  const from = useRef<HTMLElement | null>(null);
  const open: OpenSheet = useCallback((next, trigger) => {
    from.current = trigger;
    setEntry(next);
    setOpening((count) => count + 1);
  }, []);
  const returnFocus = useCallback(() => from.current, []);"""),
    ("  return { entry, opening, open, close };", "  return { entry, opening, open, close, returnFocus };"),
])

edit('pages/dashboard/space/SubscriptionSheetSlot.tsx', [
    ("""  entry,
  onClose,
}: {
  spaceId: number;
  entry: SheetEntry;
  onClose: () => void;
}) {""", """  entry,
  returnFocus,
  onClose,
}: {
  spaceId: number;
  entry: SheetEntry;
  returnFocus: () => HTMLElement | null;
  onClose: () => void;
}) {"""),
    ("""      onClose={onClose}
    />""", """      returnFocus={returnFocus}
      onClose={onClose}
    />"""),
])

for page in ['pages/dashboard/space/desk/DeskPage.tsx', 'pages/dashboard/space/customers/CustomerPage.tsx']:
    edit(page, [("""          entry={sheet.entry}
          onClose={sheet.close}""", """          entry={sheet.entry}
          returnFocus={sheet.returnFocus}
          onClose={sheet.close}""")])

edit('pages/dashboard/space/customers/CustomersPage.tsx', [
    ("""              entry={sheet.entry}
              onClose={sheet.close}""", """              entry={sheet.entry}
              returnFocus={sheet.returnFocus}
              onClose={sheet.close}"""),
    ("""            onClick={() => {
              sheet.open({ mode: 'new' });
            }}""", """            onClick={(event) => {
              sheet.open({ mode: 'new' }, event.currentTarget);
            }}"""),
])

edit('pages/dashboard/space/desk/DeskPage.tsx', [
    ("import { useCallback, useMemo, useState } from 'react';",
     "import { useCallback, useMemo, useRef, useState } from 'react';"),
    ("""  const sheet = useSheetOpener();
  const subscribe = sheet.open;""", """  const sheet = useSheetOpener();
  const subscribe = sheet.open;
  // The phone's «⋯», where the focus returns once a sheet opened from its item closes.
  const more = useRef<HTMLButtonElement | null>(null);"""),
    ("""                onClick={() => {
                  subscribe({ mode: 'new' });
                }}""", """                onClick={(event) => {
                  subscribe({ mode: 'new' }, event.currentTarget);
                }}"""),
    ("""                <Button variant="ghost" size="icon" aria-label={words.actions.more}>""",
     """                <Button ref={more} variant="ghost" size="icon" aria-label={words.actions.more}>"""),
    ("""                  onSelect={() => {
                    subscribe({ mode: 'new' });
                  }}""", """                  onSelect={() => {
                    subscribe({ mode: 'new' }, more.current);
                  }}"""),
])
print('ok')
