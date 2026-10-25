"""Commit 3: the desk's index and the three pages open the subscription sheet."""
W = 'C:/dev/masaha/app/apps/web/src/'


def edit(path, pairs):
    p = W + path
    s = open(p, encoding='utf-8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old[:80], s.count(old))
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)


edit('features/desk/index.ts', [
    ("export { PayDialog } from './components/pay/PayDialog';\n",
     "export { PayDialog } from './components/pay/PayDialog';\n"
     "export { SubscriptionSheet } from './components/sheet/SubscriptionSheet';\n"),
    ("export type { DeskAbilities } from './types/DeskAbilities';\n",
     "export type { DeskAbilities } from './types/DeskAbilities';\n"
     "export type { SheetChoices } from './types/SheetChoices';\n"
     "export type { SheetEntry } from './types/SheetEntry';\n"),
])

edit('pages/dashboard/space/desk/DeskPage.tsx', [
    ("""import { PageHeader } from '../../shell/PageHeader';
import { SwitchStaffButton, SwitchStaffItem } from './SwitchStaffButton';""",
     """import { PageHeader } from '../../shell/PageHeader';
import { SubscriptionSheetSlot } from '../SubscriptionSheetSlot';
import { useSheetOpener } from '../useSheetOpener';
import { SwitchStaffButton, SwitchStaffItem } from './SwitchStaffButton';"""),
    (""" * present, `occupancy`'s, with `desk`'s check-out in each row,""",
     """ * present, `occupancy`'s, with `desk`'s check-out in each row; «زبون جديد» in the top bar (its «⋯» on
 * a phone), the search's «زبون جديد باسم «X»» and a card's «اشتراك جديد» open the one subscription
 * sheet, with `packages`' offered packages;"""),
    ("""  // The search's cards' «⋯»: the owner's archive, and the way to a customer's file.
  const menu = useMemo(
    () => ({
      owner,
      fileLink: (customerId: number) => spaceCustomerPath(spaceId, customerId),
    }),
    [owner, spaceId],
  );""", """  // «زبون جديد», «اشتراك جديد»: one subscription sheet, opened from the page, the search or a card.
  const sheet = useSheetOpener();
  const subscribe = sheet.open;
  // The search's cards' «⋯»: the owner's archive, the way to a customer's file, the sheet.
  const menu = useMemo(
    () => ({
      owner,
      fileLink: (customerId: number) => spaceCustomerPath(spaceId, customerId),
      subscribe,
    }),
    [owner, spaceId, subscribe],
  );"""),
    ("""              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  receive({});
                }}
              >
                {words.pay.title}
              </Button>""", """              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  receive({});
                }}
              >
                {words.pay.title}
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  subscribe({ mode: 'new' });
                }}
              >
                {words.sheet.entry.new}
              </Button>"""),
    ("""                  {words.pay.title}
                </DropdownMenuItem>
                <SwitchStaffItem spaceId={spaceId} />""", """                  {words.pay.title}
                </DropdownMenuItem>
                <DropdownMenuItem
                  onSelect={() => {
                    subscribe({ mode: 'new' });
                  }}
                >
                  {words.sheet.entry.new}
                </DropdownMenuItem>
                <SwitchStaffItem spaceId={spaceId} />"""),
    ("""          onClose={() => {
            setPay(null);
          }}
        />
      )}
    </>""", """          onClose={() => {
            setPay(null);
          }}
        />
      )}
      {sheet.entry !== null && (
        <SubscriptionSheetSlot
          key={sheet.opening}
          spaceId={spaceId}
          entry={sheet.entry}
          onClose={sheet.close}
        />
      )}
    </>"""),
])

edit('pages/dashboard/space/customers/CustomersPage.tsx', [
    ("""import { CustomersList } from '@features/desk';""", """import { CustomersList } from '@features/desk';
import { useCopy } from '@shared/copy';
import { Button } from '@shared/design-system';"""),
    ("""import { PageHeader } from '../../shell/PageHeader';""", """import { PageHeader } from '../../shell/PageHeader';
import { SubscriptionSheetSlot } from '../SubscriptionSheetSlot';
import { useSheetOpener } from '../useSheetOpener';"""),
    (""" * customer's file below this page. Whether""",
     """ * customer's file below this page; «زبون جديد» in the top bar and a row's «اشتراك جديد» open `desk`'s
 * subscription sheet. Whether"""),
    ("""  return (
    <>
      <PageHeader />
      {spaceId === undefined ? (
        <NotFoundState />
      ) : (
        // Another space is another list: nothing typed for one carries over to the next.
        <CustomersList key={spaceId} spaceId={spaceId} owner={owner} fileLink={fileLink} />
      )}
    </>
  );""", """  const words = useCopy().desk.sheet;
  const sheet = useSheetOpener();

  return (
    <>
      <PageHeader>
        {spaceId !== undefined && (
          <Button
            size="sm"
            className="ms-auto"
            onClick={() => {
              sheet.open({ mode: 'new' });
            }}
          >
            {words.entry.new}
          </Button>
        )}
      </PageHeader>
      {spaceId === undefined ? (
        <NotFoundState />
      ) : (
        <>
          {/* Another space is another list: nothing typed for one carries over to the next. */}
          <CustomersList
            key={spaceId}
            spaceId={spaceId}
            owner={owner}
            fileLink={fileLink}
            subscribe={sheet.open}
          />
          {sheet.entry !== null && (
            <SubscriptionSheetSlot
              key={`sheet-${String(sheet.opening)}`}
              spaceId={spaceId}
              entry={sheet.entry}
              onClose={sheet.close}
            />
          )}
        </>
      )}
    </>
  );"""),
])

edit('pages/dashboard/space/customers/CustomerPage.tsx', [
    ("""import { PageHeader } from '../../shell/PageHeader';""", """import { PageHeader } from '../../shell/PageHeader';
import { SubscriptionSheetSlot } from '../SubscriptionSheetSlot';
import { useSheetOpener } from '../useSheetOpener';"""),
    (""" * owner's, as the session's link at the space says (S5).""",
     """ * owner's, as the session's link at the space says (S5); the header's «اشتراك جديد» opens `desk`'s
 * subscription sheet."""),
    ("""  const owner = useSession(
    (session) => session.user?.spaces.find((link) => link.spaceId === spaceId)?.role === 'OWNER',
  );

  return (""", """  const owner = useSession(
    (session) => session.user?.spaces.find((link) => link.spaceId === spaceId)?.role === 'OWNER',
  );
  const sheet = useSheetOpener();

  return ("""),
    ("""        <CustomerFile spaceId={spaceId} customerId={customerId} owner={owner} />
      </div>
    </>""", """        <CustomerFile
          spaceId={spaceId}
          customerId={customerId}
          owner={owner}
          subscribe={sheet.open}
        />
      </div>
      {sheet.entry !== null && (
        <SubscriptionSheetSlot
          key={sheet.opening}
          spaceId={spaceId}
          entry={sheet.entry}
          onClose={sheet.close}
        />
      )}
    </>"""),
])
print('ok')
