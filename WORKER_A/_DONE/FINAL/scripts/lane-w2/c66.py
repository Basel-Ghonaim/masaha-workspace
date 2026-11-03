import os
os.chdir(r'C:\dev\masaha\app-lane-w2\apps\web\src')
def edit(p,pairs):
    s=open(p,encoding='utf8').read()
    for a,b in pairs:
        assert s.count(a)==1,(p,a[:70]); s=s.replace(a,b)
    open(p,'w',encoding='utf8',newline='').write(s)

edit('shared/copy/english/spaceLinks.ts',[
("""      ALREADY_OWNER:
        'This email is already an owner’s — link them to the space from their row in the list.',
""",""),
("""    checkFailed: 'Couldn’t check this email right now.',""","""    checkFailed: 'Couldn’t check this email right now.',
    /** `ALREADY_OWNER`, under the email (finding 83), and the way on: the link dialog for them. */
    alreadyOwner: 'This email is already an owner’s.',
    linkThem: 'Link them to the space',"""),
])
edit('shared/copy/arabic/spaceLinks.ts',[
("""      ALREADY_OWNER: 'هذا البريد لمالك مسبقًا — اربطه بالمساحة من صفّه في القائمة.',
""",""),
("""    checkFailed: 'تعذّر التحقق من هذا البريد الآن.',""","""    checkFailed: 'تعذّر التحقق من هذا البريد الآن.',
    alreadyOwner: 'هذا البريد لمالك مسبقًا.',
    linkThem: 'اربطه بالمساحة',"""),
])
edit('features/space-links/types/LinkTarget.ts',[
("""import type { SpaceNameView } from './AdminSpaceRowView';""","""import type { SpaceNameView } from './AdminSpaceRowView';
import type { SpaceChoiceView } from './SpaceChoiceView';"""),
(""" * theirs and the spaces whose front desk they work.
 */""",""" * theirs and the spaces whose front desk they work, and, from the add sheet's `ALREADY_OWNER`, the
 * space chosen there.
 */"""),
("""        deskIds: readonly number[];
      };
    };""","""        deskIds: readonly number[];
      };
      /** The space already chosen, as the add sheet chose it. */
      space?: SpaceChoiceView;
    };"""),
])
edit('features/space-links/hooks/link/useLinkOwnerDialog.ts',[
("""  const [chosenSpace, setSpace] = useState<SpaceChoiceView | null>(null);""","""  const [chosenSpace, setSpace] = useState<SpaceChoiceView | null>(
    target.from === 'person' ? (target.space ?? null) : null,
  );"""),
])
edit('features/space-links/types/EmailAccountView.ts',[
("""import type { SpaceNameView } from './AdminSpaceRowView';""","""import type { AdminUserRow } from '@masaha/shared/space-links';
import type { SpaceNameView } from './AdminSpaceRowView';"""),
("""  | { status: 'found'; account: EmailAccountView }""","""  | { status: 'found'; account: EmailAccountView; row: AdminUserRow }"""),
])
edit('features/space-links/hooks/add-owner/useEmailAccount.ts',[
("""  return {
    status: 'found',
    account: {""","""  return {
    status: 'found',
    row,
    account: {"""),
])
F='features/space-links/hooks/add-owner/useAddOwnerForm.ts'
edit(F,[
("""import type { AddedOwnerView } from '../../types/TemporaryPasswordSlot';""","""import type { AddedOwnerView } from '../../types/TemporaryPasswordSlot';
import type { LinkTarget } from '../../types/LinkTarget';"""),
("""  const [added, setAdded] = useState<AddedOwnerView | null>(null);""","""  const [added, setAdded] = useState<AddedOwnerView | null>(null);
  // An email the server refused as an owner's already (`ALREADY_OWNER`, finding 83), and the link
  // dialog opened for that owner and the chosen space.
  const [ownerEmail, setOwnerEmail] = useState<string | null>(null);
  const [linkTarget, setLinkTarget] = useState<LinkTarget | null>(null);"""),
("""  const account = useEmailAccount(rememberedEmail);""","""  const account = useEmailAccount(rememberedEmail);
  // The owner the refused email is, read by its exact email, for the link dialog.
  const owner = useEmailAccount(ownerEmail);"""),
("""      const refused = toAppError(error);
      if (refused.code === 'EMAIL_HAS_ACCOUNT' && !upgrade) {
        setRememberedEmail(request.email);
        return;
      }""","""      const refused = toAppError(error);
      if (refused.code === 'EMAIL_HAS_ACCOUNT' && !upgrade) {
        setRememberedEmail(request.email);
        return;
      }
      if (refused.code === 'ALREADY_OWNER' && refused.details !== undefined) {
        setOwnerEmail(request.email);
        return;
      }"""),
("""  const notice = noticeOf(hasAccount ? account : { status: 'none' }, lines, copy.status.retry);""","""  const notice = noticeOf(hasAccount ? account : { status: 'none' }, lines, copy.status.retry);
  // The email refused as an owner's, while it is still the one typed.
  const isOwner = ownerEmail !== null && watchedEmail === ownerEmail;
  const ownerRow = owner.status === 'found' ? owner.row : null;"""),
("""    errors: form.errors,""","""    errors: isOwner ? { ...form.errors, email: lines.alreadyOwner } : form.errors,
    /**
     * «اربطه بالمساحة», under the email an owner's already: the link dialog for that owner and the
     * chosen space, once their account is read.
     */
    linkOwner: isOwner
      ? {
          label: lines.linkThem,
          ready: ownerRow !== null,
          run: () => {
            if (ownerRow === null) return;
            setOpen(false);
            setLinkTarget({
              from: 'person',
              person: {
                id: ownerRow.id,
                name: ownerRow.name,
                role: 'OWNER',
                spaceIds: ownerRow.spaces.map((space) => space.id),
                deskIds: ownerRow.receptionSpaces.map((desk) => desk.id),
              },
              ...(chosenSpace !== null && { space: chosenSpace }),
            });
          },
        }
      : null,
    /** The link dialog opened from «اربطه بالمساحة», until it closes. */
    linkTarget,
    closeLink: () => {
      setLinkTarget(null);
      setOwnerEmail(null);
    },"""),
])
C='features/space-links/components/add-owner/AddOwner.tsx'
edit(C,[
("""import { SpaceCombobox } from '../SpaceCombobox';""","""import { SpaceCombobox } from '../SpaceCombobox';
import { LinkOwnerDialog } from '../link/LinkOwnerDialog';"""),
("""              <Field label={form.labels.email} error={form.errors.email}>
                <Input type="email" dir="ltr" {...form.fields.email} />
              </Field>""","""              <div className="flex flex-col gap-1">
                <Field label={form.labels.email} error={form.errors.email}>
                  <Input type="email" dir="ltr" {...form.fields.email} />
                </Field>
                {form.linkOwner !== null && (
                  <Button
                    type="button"
                    variant="link"
                    className="self-start"
                    loading={!form.linkOwner.ready}
                    onClick={form.linkOwner.run}
                  >
                    {form.linkOwner.label}
                  </Button>
                )}
              </div>"""),
("""      {/* Outside the sheet, which closes once the owner is added. */}""","""      {form.linkTarget !== null && (
        <LinkOwnerDialog
          target={form.linkTarget}
          onClose={form.closeLink}
          returnFocus={{ current: trigger }}
        />
      )}
      {/* Outside the sheet, which closes once the owner is added. */}"""),
])
