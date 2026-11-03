"""R1-F2: the cards' dialogs held by the list."""
import io

D = 'C:/dev/masaha/app/apps/web/src/features/announcements/'


def edit(path, pairs):
    p = D + path
    s = io.open(p, encoding='utf8', newline='').read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, a[:70])
        s = s.replace(a, b)
    io.open(p, 'w', encoding='utf8', newline='').write(s)
    print('ok', path)


edit('components/list/ClosureLine.tsx', [
    ("import type { AnnouncementCardView } from '../../types/AnnouncementCardView';\n",
     "import type { AnnouncementCardView } from '../../types/AnnouncementCardView';\nimport type { OpenCardDialog } from '../../types/CardDialog';\n"),
    ("export function ClosureLine({ spaceId, card }: { spaceId: number; card: AnnouncementCardView }) {",
     "export function ClosureLine({\n  card,\n  openDialog,\n}: {\n  card: AnnouncementCardView;\n  openDialog: OpenCardDialog;\n}) {"),
    ("""        <ExtensionAction
          spaceId={spaceId}
          closure={card.announcement}
          label={card.extension.label}
        />""",
     """        <ExtensionAction
          closure={card.announcement}
          cardKey={card.key}
          label={card.extension.label}
          openDialog={openDialog}
        />"""),
])

edit('components/actions/AnnouncementMenu.tsx', [
    ("import { useLayoutEffect, useRef, useState } from 'react';\n", "import { useLayoutEffect, useRef } from 'react';\n"),
    ("import type { AnnouncementCardView } from '../../types/AnnouncementCardView';\nimport { DeleteDialog } from './DeleteDialog';\n",
     "import type { AnnouncementCardView } from '../../types/AnnouncementCardView';\nimport type { OpenCardDialog } from '../../types/CardDialog';\n"),
    (""" * A card's «⋯», named by its announcement («إجراءات أخرى: {type} · {period}»), holding «حذف…»,
 * destructive, which opens its dialog. Closed, the focus goes back to the «⋯»; once the «⋯» is gone
 * with the focus on it — the announcement deleted, its card gone — `onGone` places it.
 */""",
     """ * A card's «⋯», named by its announcement («إجراءات أخرى: {type} · {period}»), holding «حذف…»,
 * destructive, which opens the delete's dialog, held by the list so that it stays open whatever the
 * list's refetch makes of the card (a refusal stays in it). Once the «⋯» is gone with the focus on it
 * — the announcement deleted, its card gone — `onGone` places it.
 */"""),
    ("""export function AnnouncementMenu({
  spaceId,
  card,
  menu,
  onGone,
}: {
  spaceId: number;
  card: AnnouncementCardView;""",
     """export function AnnouncementMenu({
  card,
  menu,
  openDialog,
  onGone,
}: {
  card: AnnouncementCardView;"""),
    ("""    remove: NonNullable<AnnouncementActionsView['menu']['remove']>;
  };
  onGone: () => void;
}) {
  const [open, setOpen] = useState(false);
  const trigger""",
     """    remove: NonNullable<AnnouncementActionsView['menu']['remove']>;
  };
  openDialog: OpenCardDialog;
  onGone: () => void;
}) {
  const trigger"""),
    ("""            onSelect={() => {
              setOpen(true);
            }}""",
     """            onSelect={() => {
              if (trigger.current !== null) {
                openDialog({ kind: 'delete', card }, card.key, trigger.current);
              }
            }}"""),
    ("""      </DropdownMenu>
      {open && (
        <DeleteDialog
          spaceId={spaceId}
          card={card}
          onClose={() => {
            setOpen(false);
          }}
          returnFocus={() => {
            if (trigger.current?.isConnected === true) trigger.current.focus();
            else onGone();
          }}
        />
      )}
    </>""",
     """      </DropdownMenu>
    </>"""),
])

edit('components/list/AnnouncementCard.tsx', [
    ("import type { AnnouncementCardView } from '../../types/AnnouncementCardView';\n",
     "import type { AnnouncementCardView } from '../../types/AnnouncementCardView';\nimport type { OpenCardDialog } from '../../types/CardDialog';\n"),
    (" * sheet (`open`); «إنهاء الآن» or «ابدأ الآن»; then the «⋯» with «حذف…» at the end.",
     " * sheet (`open`); «إنهاء الآن» or «ابدأ الآن»; then the «⋯» with «حذف…» at the end. The extension's\n * and the delete's dialogs are the list's (`openDialog`)."),
    ("""  open,
  showTab,
  onGone,
}: {
  spaceId: number;
  card: AnnouncementCardView;
  open: (entry: SheetEntry, trigger: HTMLElement) => void;""",
     """  open,
  openDialog,
  showTab,
  onGone,
}: {
  spaceId: number;
  card: AnnouncementCardView;
  open: (entry: SheetEntry, trigger: HTMLElement) => void;
  openDialog: OpenCardDialog;"""),
    ("        <ClosureLine spaceId={spaceId} card={card} />",
     "        <ClosureLine card={card} openDialog={openDialog} />"),
    ("""              <AnnouncementMenu
                spaceId={spaceId}
                card={card}
                menu={{ ...actions.menu, remove }}
                onGone={onGone}
              />""",
     """              <AnnouncementMenu
                card={card}
                menu={{ ...actions.menu, remove }}
                openDialog={openDialog}
                onGone={onGone}
              />"""),
])

edit('components/list/AnnouncementsList.tsx', [
    ("import type { SheetEntry } from '../../types/SheetEntry';\nimport { AnnouncementSheet } from '../sheet/AnnouncementSheet';\n",
     "import type { CardDialog, OpenCardDialog } from '../../types/CardDialog';\nimport type { SheetEntry } from '../../types/SheetEntry';\nimport { DeleteDialog } from '../actions/DeleteDialog';\nimport { ExtensionDialog } from '../extension/ExtensionDialog';\nimport { AnnouncementSheet } from '../sheet/AnnouncementSheet';\n"),
    (" * opening (its key is that opening's, S4); closed, the focus goes back to the control that opened it.\n",
     " * opening (its key is that opening's, S4); closed, the focus goes back to the control that opened it.\n"
     " * A card's extension and delete dialogs are held here too, so that they stay open whatever the list's\n"
     " * refetch makes of the card — a 409 or a 404 stays in its dialog until «رجوع»; closed, the focus goes\n"
     " * back to the control that opened it, else to the card's first action, else on as below.\n"),
    ("""  const { listRef, tabsRef, leave } = useCardFocus(list.cards.map((card) => card.key));
""",
     """  const { listRef, tabsRef, leave, settle } = useCardFocus(list.cards.map((card) => card.key));
  const [dialog, setDialog] = useState<
    (CardDialog & { key: string; opening: number }) | null
  >(null);
  const dialogOpener = useRef<HTMLElement | null>(null);
  const openDialog: OpenCardDialog = (entry, key, trigger) => {
    dialogOpener.current = trigger;
    setDialog((before) => ({ ...entry, key, opening: (before?.opening ?? 0) + 1 }));
  };
  const returnDialogFocus = (key: string) => {
    const trigger = dialogOpener.current;
    if (trigger?.isConnected === true) trigger.focus();
    else settle(key);
  };
"""),
    ("""                    open={open}
                    showTab={list.choose}""",
     """                    open={open}
                    openDialog={openDialog}
                    showTab={list.choose}"""),
    ("""      {sheet !== null && (""",
     """      {dialog?.kind === 'extension' && (
        <ExtensionDialog
          key={dialog.opening}
          spaceId={spaceId}
          closure={dialog.closure}
          onClose={() => {
            setDialog(null);
          }}
          returnFocus={() => {
            returnDialogFocus(dialog.key);
          }}
        />
      )}
      {dialog?.kind === 'delete' && (
        <DeleteDialog
          key={dialog.opening}
          spaceId={spaceId}
          card={dialog.card}
          onClose={() => {
            setDialog(null);
          }}
          returnFocus={() => {
            returnDialogFocus(dialog.key);
          }}
        />
      )}
      {sheet !== null && ("""),
])

edit('hooks/list/useCardFocus.ts', [
    (""" * once it leaves under the focus. The refs live here, read only in effects and events, never while
 * drawing (the React compiler's rule).
 */""",
     """ * once it leaves under the focus; `settle` places the focus once a dialog the list held for a card
 * closes and its opener is gone: the card's first action, else on as above. The refs live here, read
 * only in effects and events, never while drawing (the React compiler's rule).
 */"""),
    ("""  return { listRef: list, tabsRef: tabs, leave };""",
     """  /** A card's dialog closed with its opener gone: the card's first action, else the next one's. */
  const settle = useCallback((key: string) => {
    const action = actionOf(keeper.current, key);
    if (action === null) move(keeper.current, key);
    else action.focus();
  }, []);

  return { listRef: list, tabsRef: tabs, leave, settle };"""),
])
