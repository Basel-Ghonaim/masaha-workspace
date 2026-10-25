"""Commit 4: the renewal and the published prices (spec D), on the sheet."""
W = 'C:/dev/masaha/app/apps/web/src/'


def edit(path, pairs):
    p = W + path
    s = open(p, encoding='utf-8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old[:80], s.count(old))
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)


# The words.
edit('shared/copy/english/desk.ts', [
    ("""    groups: { packages: 'The space’s packages — not shown to visitors' },""",
     """    groups: {
      published: 'Published',
      packages: 'The space’s packages — not shown to visitors',
    },
    published: {
      WEEK: 'Weekly',
      MONTH: 'Monthly',
      students: '· students',
      gone: 'This published price changed or was removed; the prices were read again. Check the choice, then save.',
    },
    changePackage: 'Change package',"""),
])
edit('shared/copy/arabic/desk.ts', [
    ("""    groups: { packages: 'باقات المساحة — لا تظهر للزوار' },""",
     """    groups: { published: 'منشورة للزوار', packages: 'باقات المساحة — لا تظهر للزوار' },
    published: {
      WEEK: 'أسبوعي',
      MONTH: 'شهري',
      students: '· للطلاب',
      gone: 'تغيّر هذا السعر المنشور أو حُذف؛ قُرئت الأسعار من جديد. راجع الاختيار ثم احفظ.',
    },
    changePackage: 'تغيير الباقة',"""),
])

# What the page gives: the published prices too.
edit('features/desk/types/SheetChoices.ts', [
    ("""import type { Shift } from '@masaha/shared/spaces';""",
     """import type { Price, Shift } from '@masaha/shared/spaces';"""),
    (""" * What the page gives the subscription sheet to choose from, as other capabilities read it: the
 * space's offered packages (`packages`') with their read's state and retry, and the space's shifts
 * (`spaces'`), `null` while they load.
 */""", """ * What the page gives the subscription sheet to choose from, as other capabilities read it: the
 * space's offered packages (`packages`') with their read's state and retry; its published prices
 * (`spaces`'), read again when the sheet opens, with a refresh; and its shifts (`spaces`'), `null`
 * while they load.
 */"""),
    ("""  retry: () => void;
  shifts: Shift[] | null;""", """  retry: () => void;
  prices: { state: 'loading' | 'failed' | 'ready'; list: Price[]; refresh: () => void };
  shifts: Shift[] | null;"""),
])

edit('features/desk/types/SheetEntry.ts', [
    ("""import type { Customer } from '@masaha/shared/customers';""",
     """import type { Customer } from '@masaha/shared/customers';
import type { SubscriptionState } from '@masaha/shared/subscriptions';"""),
    (""" * phone, from the desk's search), or a known customer's new subscription, with what they owe as the
 * entry read it (their file, read when the sheet opens, says it again).
 */""", """ * phone, from the desk's search), a known customer's new subscription, with what they owe as the
 * entry read it (their file, read when the sheet opens, says it again), or the renewal of one of
 * their subscriptions.
 */"""),
    ("""  | { mode: 'subscribe'; customer: Customer & { debtAgorot: number } };""",
     """  | { mode: 'subscribe'; customer: Customer & { debtAgorot: number } }
  | { mode: 'renew'; customer: Customer & { debtAgorot: number }; renews: SubscriptionState };"""),
])

# The request: a published price by its key and its name.
edit('features/desk/services/sheetRequest.ts', [
    (""" * What the subscription sheet holds, by the paths its requests name: a new customer's name and
 * phone; the chosen package (`pkg-{id}`), published price or `custom`;""",
     """ * What the subscription sheet holds, by the paths its requests name: a new customer's name and
 * phone; the chosen package (`pkg-{id}`), published price (`price-…`) or `custom`;"""),
    ("""/** The sheet's two requests: the new customer's, when there is one, and the subscribe. */""",
     """/** A published price as the subscribe names it: its key, and the name the desk gives it. */
export type PublishedChoice = NonNullable<SubscribeRequest['published']>;

/** The sheet's two requests: the new customer's, when there is one, and the subscribe. */"""),
    (""" * (the phone only when typed); exactly one choice — a package's id, or the custom terms, each limit,""",
     """ * (the phone only when typed); exactly one choice — a package's id, a published price by its key
 * and its name (`published`, never a price's id: the server reads its amount), or the custom terms, each limit,"""),
    ("""  { newCustomer, renewalOfId }: { newCustomer: boolean; renewalOfId?: number },
): Record<string, unknown> {
  const { custom, payment } = values;
  const choice = values.choice.startsWith('pkg-')
    ? { packageId: Number(values.choice.slice('pkg-'.length)) }
    : values.choice === 'custom'""", """  {
    newCustomer,
    renewalOfId,
    published,
  }: {
    newCustomer: boolean;
    renewalOfId?: number;
    /** The published prices offered, by their choice's value. */
    published?: ReadonlyMap<string, PublishedChoice>;
  },
): Record<string, unknown> {
  const { custom, payment } = values;
  const price = published?.get(values.choice);
  const choice = values.choice.startsWith('pkg-')
    ? { packageId: Number(values.choice.slice('pkg-'.length)) }
    : price !== undefined
      ? { published: price }
      : values.choice === 'custom'"""),
])
print('ok')
