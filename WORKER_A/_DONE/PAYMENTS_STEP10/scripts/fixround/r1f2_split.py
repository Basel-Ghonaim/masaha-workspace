"""R1-F2's split: save the final files, then write the delete-only state (the extension's parts as at HEAD).
Usage: python r1f2_split.py save | delete-only | restore"""
import io, os, re, shutil, subprocess, sys

APP = 'C:/dev/masaha/app/'
A = 'apps/web/src/features/announcements/'
FILES = [A + f for f in [
    'types/CardDialog.ts', 'components/extension/ExtensionAction.tsx', 'components/list/ClosureLine.tsx',
    'components/actions/AnnouncementMenu.tsx', 'components/list/AnnouncementCard.tsx',
    'components/list/AnnouncementsList.tsx', 'hooks/list/useCardFocus.ts',
    'components/list/AnnouncementsList.component.test.tsx']]
SAVE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'r1f2-final')


def read(f):
    return io.open(APP + f, encoding='utf8', newline='').read()


def write(f, s):
    io.open(APP + f, 'w', encoding='utf8', newline='').write(s)


def sub1(s, a, b):
    assert s.count(a) == 1, a[:60]
    return s.replace(a, b)


how = sys.argv[1]
if how == 'save':
    os.makedirs(SAVE, exist_ok=True)
    for f in FILES:
        shutil.copyfile(APP + f, os.path.join(SAVE, f.replace('/', '_')))
    print('saved')
elif how == 'restore':
    for f in FILES:
        shutil.copyfile(os.path.join(SAVE, f.replace('/', '_')), APP + f)
    print('restored')
else:
    for f in [A + 'components/extension/ExtensionAction.tsx', A + 'components/list/ClosureLine.tsx']:
        io.open(APP + f, 'wb').write(subprocess.run(['git', 'show', f'HEAD:{f}'], cwd=APP, capture_output=True).stdout)
    write(A + 'types/CardDialog.ts', """import type { AnnouncementCardView } from './AnnouncementCardView';

/** A card's dialog, as the list holds it: an announcement's delete. */
export type CardDialog = { kind: 'delete'; card: AnnouncementCardView };

/** Opens a card's dialog, held by the list: the card's key and the control that opened it. */
export type OpenCardDialog = (dialog: CardDialog, key: string, trigger: HTMLElement) => void;
""")
    s = read(A + 'components/list/AnnouncementCard.tsx')
    s = sub1(s, '        <ClosureLine card={card} openDialog={openDialog} />', '        <ClosureLine spaceId={spaceId} card={card} />')
    s = sub1(s, " The extension's\n * and the delete's dialogs are the list's (`openDialog`).", " The delete's\n * dialog is the list's (`openDialog`).")
    write(A + 'components/list/AnnouncementCard.tsx', s)
    s = read(A + 'components/list/AnnouncementsList.tsx')
    s = sub1(s, "import { ExtensionDialog } from '../extension/ExtensionDialog';\n", '')
    s = sub1(s, " * A card's extension and delete dialogs are held here too,", " * A card's delete dialog is held here too,")
    s = re.sub(r"      \{dialog\?\.kind === 'extension' && \(\n.*?\n      \)\}\n", '', s, count=1, flags=re.S)
    assert "ExtensionDialog" not in s
    write(A + 'components/list/AnnouncementsList.tsx', s)
    t = read(A + 'components/list/AnnouncementsList.component.test.tsx')
    t2 = re.sub(r"    it\('keeps the extension’s CLOSURE_ALREADY_EXTENDED.*?\n    \}\);\n\n", '', t, count=1, flags=re.S)
    assert t2 != t
    write(A + 'components/list/AnnouncementsList.component.test.tsx', t2)
    print('delete-only written')
