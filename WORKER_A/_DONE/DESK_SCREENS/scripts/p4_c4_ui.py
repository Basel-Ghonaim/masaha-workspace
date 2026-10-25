"""Commit 4: the renewal's one line, the renewed-meanwhile line, «تجديد» on the file's card, prices."""
W = 'C:/dev/masaha/app/apps/web/src/'


def edit(path, pairs):
    p = W + path
    s = open(p, encoding='utf-8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old[:80], s.count(old))
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)


edit('features/desk/components/sheet/PackageOptions.tsx', [
    (""" * and «مخصّص» last. While the packages load, three skeletons; failed, the line and «إعادة المحاولة».
 */""", """ * and «مخصّص» last; a renewal's package alone, as one line with «تغيير الباقة», until it is changed.
 * While the choices load, three skeletons; failed, the line and «إعادة المحاولة».
 */"""),
    ("""  const baseId = useId();
""", """  const baseId = useId();
  const { current } = view;
"""),
    ("""      {view.empty !== null && <p""", """      {current !== null && (
        <div className="flex min-w-0 flex-col gap-2">
          <p className="text-label">{view.legend}</p>
          <div className="flex min-w-0 items-start justify-between gap-3 rounded-lg border border-primary p-3">
            <span className="flex min-w-0 flex-col gap-0.5">
              <span className="flex flex-wrap items-baseline gap-2">
                <span dir="auto" className="text-label">
                  {current.line.title}
                </span>
                {current.line.amount !== null && (
                  <span dir="ltr" className="text-label">
                    {current.line.amount}
                  </span>
                )}
              </span>
              <span className="text-caption text-muted-foreground">{current.line.terms}</span>
            </span>
            <Button variant="outline" size="sm" disabled={disabled} onClick={current.change.run}>
              {current.change.label}
            </Button>
          </div>
        </div>
      )}
      {view.empty !== null && <p"""),
    ("""      {view.groups.length > 0 && (""", """      {current === null && view.groups.length > 0 && ("""),
])

edit('features/desk/components/sheet/SubscriptionSheet.tsx', [
    ("""            {view.prior !== null && <PriorDebts prior={view.prior} />}""",
     """            {view.renewedAlready !== null && (
              <Alert variant="info">
                <AlertDescription>{view.renewedAlready}</AlertDescription>
              </Alert>
            )}
            {view.prior !== null && <PriorDebts prior={view.prior} />}"""),
    ("""/**
 * «زبون جديد» / «اشتراك جديد» (screen 16), the end sheet, titled by its mode:""",
     """/**
 * «زبون جديد» / «اشتراك جديد» / «تجديد الاشتراك» (screen 16), the end sheet, titled by its mode:"""),
])

edit('features/desk/components/file/SubscriptionCard.tsx', [
    (""" * الاشتراك» ends it early, asking first. `opened` hears which control opened the payment.
 */""", """ * الاشتراك» ends it early, asking first; «تجديد» (`renew`, the latest's) opens the page's sheet for
 * its renewal. `opened` hears which control opened the payment.
 */"""),
    ("""  card,
  opened,
}: {
  spaceId: number;
  card: SubscriptionCardView;
  opened: (trigger: HTMLElement) => void;
}) {""", """  card,
  opened,
  renew,
}: {
  spaceId: number;
  card: SubscriptionCardView;
  opened: (trigger: HTMLElement) => void;
  /** «تجديد», offered on the latest subscription. */
  renew: { label: string; run: () => void } | null;
}) {"""),
    ("""        <Button
          variant="ghost"
          aria-expanded={statement.toggle.expanded}""", """        {renew !== null && (
          <Button variant="secondary" onClick={renew.run}>
            {renew.label}
          </Button>
        )}
        <Button
          variant="ghost"
          aria-expanded={statement.toggle.expanded}"""),
])

edit('features/desk/components/file/CustomerFile.tsx', [
    ("""import { CustomerActions } from '../menu/CustomerActions';""", """import { useCopy } from '@shared/copy';
import { CustomerActions } from '../menu/CustomerActions';"""),
    ("""  const file = useCustomerFile(spaceId, customerId);
""", """  const file = useCustomerFile(spaceId, customerId);
  const words = useCopy().desk.sheet;
"""),
    ("""  const { subscriptions } = file;""", """  const { subscriptions, header } = file;
  // The latest subscription, the file's first, is the one a renewal renews (DK-007).
  const renew = (index: number, subscription: (typeof subscriptions.cards)[number]['subscription']) =>
    index === 0 && header.customer.archivedAt === null
      ? {
          label: words.entry.renew,
          run: () => {
            subscribe({
              mode: 'renew',
              customer: { ...header.customer, debtAgorot: header.debtAgorot },
              renews: subscription,
            });
          },
        }
      : null;"""),
    ("""            {subscriptions.cards.map((card) => (
              <SubscriptionCard key={card.key} spaceId={spaceId} card={card} opened={opened} />
            ))}""", """            {subscriptions.cards.map((card, index) => (
              <SubscriptionCard
                key={card.key}
                spaceId={spaceId}
                card={card}
                opened={opened}
                renew={renew(index, card.subscription)}
              />
            ))}"""),
])

edit('pages/dashboard/space/SubscriptionSheetSlot.tsx', [
    ("""import { useSpaceShifts } from '@features/spaces';""", """import { useSpacePrices, useSpaceShifts } from '@features/spaces';"""),
    (""" * `desk`'s subscription sheet with what other capabilities hold for it (S1): the space's offered
 * packages, as `packages` reads them, and its shifts, as `spaces` reads them. It is mounted only
 * while the sheet is open, so those are read when it opens.
 */""", """ * `desk`'s subscription sheet with what other capabilities hold for it (S1): the space's offered
 * packages, as `packages` reads them, and its published prices and shifts, as `spaces` reads them.
 * It is mounted only while the sheet is open; the prices are read again each time it opens (finding
 * 171), so the sheet never sells from an older read.
 */"""),
    ("""  const shifts = useSpaceShifts('owner', spaceId);
""", """  const shifts = useSpaceShifts('owner', spaceId);
  const prices = useSpacePrices('owner', spaceId);
"""),
    ("""      choices={{ ...offered, shifts }}""", """      choices={{
        ...offered,
        prices: { state: prices.state, list: prices.prices, refresh: prices.refresh },
        shifts,
      }}"""),
])
print('ok')
