import os
os.chdir(r'C:\dev\masaha\app-lane-w3\apps\web\src')
def edit(p, pairs):
    s=open(p,encoding='utf8').read()
    for a,b in pairs:
        assert s.count(a)==1,(p,a)
        s=s.replace(a,b)
    open(p,'w',encoding='utf8',newline='').write(s)
edit('features/desk/components/check-out/CheckOutAction.tsx',[
("""  receive,
}: {
  spaceId: number;
  person: PresentPerson;
  terms: VisitTerms | undefined;
  after?: After;
  /** Opens the payment on what a subscriber's check-out leaves owed. */
  receive?: (target: PayTarget) => void;
}) {""","""  receive,
  usageOut,
}: {
  spaceId: number;
  person: PresentPerson;
  terms: VisitTerms | undefined;
  after?: After;
  /** Opens the payment on what a subscriber's check-out leaves owed. */
  receive?: (target: PayTarget) => void;
  /** Opens the page's due dialog after a usage-based subscriber's check-out (D7.12). */
  usageOut?: UsageOut;
}) {"""),
("""    <SubscriberCheckOutAction spaceId={spaceId} person={person} after={after} receive={receive} />""","""    <SubscriberCheckOutAction
      spaceId={spaceId}
      person={person}
      after={after}
      receive={receive}
      usageOut={usageOut}
    />"""),
("""  after,
  receive,
}: {
  spaceId: number;
  person: Extract<PresentPerson, { kind: 'CHECK_IN' }>;
  after?: After;
  receive?: (target: PayTarget) => void;
}) {
  const checkOut = useCheckOutSubscriber(spaceId, person, { done: after?.done, receive });""","""  after,
  receive,
  usageOut,
}: {
  spaceId: number;
  person: Extract<PresentPerson, { kind: 'CHECK_IN' }>;
  after?: After;
  receive?: (target: PayTarget) => void;
  usageOut?: UsageOut;
}) {
  const checkOut = useCheckOutSubscriber(spaceId, person, {
    done: after?.done,
    receive,
    usageOut,
  });"""),
("import { useCheckOutSubscriber } from '../../hooks/subscriber/useCheckOutSubscriber';","import {\n  useCheckOutSubscriber,\n  type UsageOut,\n} from '../../hooks/subscriber/useCheckOutSubscriber';"),
])
edit('features/desk/hooks/subscriber/useCheckOutSubscriber.ts',[
("""const repository = createDeskRepository();
""","""const repository = createDeskRepository();

/** Opens the page's due dialog for a usage-based subscriber's check-out, from its answer. */
export type UsageOut = (name: string, answer: CheckInCheckOut) => void;
"""),
("""  { done, receive }: { done?: () => void; receive?: (target: PayTarget) => void } = {},""","""  {
    done,
    receive,
    usageOut,
  }: { done?: () => void; receive?: (target: PayTarget) => void; usageOut?: UsageOut } = {},"""),
("""      onSuccess: (answer) => {
        toastSubscriberOut(""","""      onSuccess: (answer) => {
        // A usage-based subscription's due is said in a dialog, from the answer (D7.12, DI10);
        // a fixed one stays one tap with its toast.
        if (answer.subscription.billing !== 'FIXED' && usageOut !== undefined) {
          usageOut(person.name, answer);
          done?.();
          return;
        }
        toastSubscriberOut("""),
(""" * says how long they stayed""",""" * says how long they stayed — for a usage-based subscription, `usageOut` opens the page's dialog
 * of what is due instead (D7.12) — and"""),
])
edit('pages/dashboard/space/desk/DeskPage.tsx',[
("""  UnpricedCard,
  useOpenCheckIns,""","""  UnpricedCard,
  UsageOutDialog,
  useOpenCheckIns,"""),
("""  const [payOpening, setPayOpening] = useState(0);""","""  const [payOpening, setPayOpening] = useState(0);
  // A usage-based subscriber's check-out: its due, said in a dialog from the answer (D7.12).
  const [usage, setUsage] = useState<{ name: string; checkOut: CheckInCheckOut } | null>(null);
  const usageOut = useCallback((name: string, checkOut: CheckInCheckOut) => {
    setUsage({ name, checkOut });
  }, []);
  const presentRegion = useRef<HTMLDivElement | null>(null);"""),
("""      <CheckOutAction spaceId={spaceId} person={person} terms={termsData} receive={receive} />
    ),
    [spaceId, termsData, receive],""","""      <CheckOutAction
        spaceId={spaceId}
        person={person}
        terms={termsData}
        receive={receive}
        usageOut={usageOut}
      />
    ),
    [spaceId, termsData, receive, usageOut],"""),
("""                  after={after}
                  receive={receive}
                />""","""                  after={after}
                  receive={receive}
                  usageOut={usageOut}
                />"""),
("""        <div className="xl:col-span-8">""","""        <div ref={presentRegion} className="xl:col-span-8">"""),
("""      {sheet.entry !== null && (""","""      {usage !== null && (
        <UsageOutDialog
          spaceId={spaceId}
          name={usage.name}
          checkOut={usage.checkOut}
          onClose={() => {
            setUsage(null);
          }}
          // Their row has left: the focus goes to who is present's heading.
          returnFocus={() => {
            presentRegion.current?.querySelector<HTMLElement>('h2')?.focus();
          }}
        />
      )}
      {sheet.entry !== null && ("""),
("import type { PresentPerson } from '@masaha/shared/occupancy';","import type { CheckInCheckOut } from '@masaha/shared/desk';\nimport type { PresentPerson } from '@masaha/shared/occupancy';"),
])
edit('features/desk/index.ts',[("export { UnpricedCard } from './components/unpriced/UnpricedCard';\n","export { UnpricedCard } from './components/unpriced/UnpricedCard';\nexport { UsageOutDialog } from './components/usage-out/UsageOutDialog';\n")])
ar = """  /** A usage-based subscriber's check-out: what is due, from the answer (D7.12). */
  usageOut: {
    title: ({ name }: { name: string }) => `خرج ${name}`,
    today: ({ time, paid }: { time: string; paid: string }) => `اليوم ${time} · المدفوع ${paid}`,
    left: ({ subscription, balance }: { subscription: string; balance: string }) =>
      `يبقى على اشتراك ${subscription}: ${balance}`,
    receive: ({ amount }: { amount: string }) => `استلام ${amount}`,
    later: 'لاحقًا',
    failed: 'تعذّر تسجيل الدفعة',
  },
"""
en = ar.replace("`خرج ${name}`","`${name} checked out`").replace("`اليوم ${time} · المدفوع ${paid}`","`Today ${time} · paid ${paid}`").replace("`يبقى على اشتراك ${subscription}: ${balance}`","`Left on ${subscription}: ${balance}`").replace("`استلام ${amount}`","`Receive ${amount}`").replace("'لاحقًا'","'Later'").replace("'تعذّر تسجيل الدفعة'","'We couldn’t record the payment'")
for p,end,block in [('shared/copy/arabic/desk.ts',"  log: {\n",ar.replace("  /** A usage-based subscriber's check-out: what is due, from the answer (D7.12). */\n","")),('shared/copy/english/desk.ts',"  /** «السجل»: the day's log beside who is here (K8). */\n",en)]:
    s=open(p,encoding='utf8').read()
    assert s.count(end)==1,(p,end)
    s=s.replace(end,block+end)
    open(p,'w',encoding='utf8',newline='').write(s)
