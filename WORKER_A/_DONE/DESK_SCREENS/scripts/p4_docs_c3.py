"""Commit 3's documents: desk.md, customers.md, finding 125 resolved."""
D = 'C:/dev/masaha/app/docs/'


def edit(path, pairs):
    p = D + path
    s = open(p, encoding='utf-8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old[:80], s.count(old))
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)


WEB = """- **The subscription sheet** (screen 16, K3): one end sheet, full width on a phone, opened from every entry with what it knows — «زبون جديد» in the desk's and the customers' top bars, the search's «زبون جديد باسم «X»» (a link, never a second primary: DI-20) or «زبون جديد بهذا الرقم», a customer's «⋯» «اشتراك جديد». The page passes `packages`' offered packages and `spaces`' shifts (S1); each opening mounts a new sheet, so its keys are that opening's. 2026-10-26, #PRNUM.
- **No preview of the allocation** (decision 3, [finding 125](../architecture/findings/125-the-allocations-order-is-not-exposed-to-the-client.md)): the sheet lists what the customer owes from before, each item and the total from their file, and says «يُطبَّق المستلم على المستحق من قبل أولًا، ثم على الاشتراك الجديد.»; «المستلم الآن» starts at that debt plus the new price; the toast lists each part the answer's `payments` allocated, the price the server charged and the debt left, and `CUSTOMER_HAS_DEBT`'s line. *Why:* one owner of the rule, the server; the default amount pays every part. 2026-10-26, #PRNUM.
- **A new customer is two intents, two keys** (S4, DI-37): the customer is created, then subscribed; a subscribe refused after the customer was saved says «أُضيف {name} إلى الزبائن؛ لم يُحفظ الاشتراك.» with the reason, keeps every field, and «حفظ الاشتراك» sends the subscribe alone with its key; closing then says «{name} في الزبائن بدون اشتراك.». 2026-10-26, #PRNUM.
- **A package's terms are copied, never edited** (DI-50): a package is one line (DK-007) — its name, its price or rate, its validity and terms in a plain caption, no warning icon for no limit (DI-45); another price is «مخصّص». **«مخصّص» is offered only to whoever may type a price** (`visit-terms`' `mayTypePrice`, S5) and asks what the contract does (DI-52): a name prefilled «مخصّص», «لمن», the billing, the price or the rate, four optional limits, the shift where the space has any, an optional end, and «سبب السعر», required. 2026-10-26, #PRNUM.
- **The phone is asked only of a new customer** (DI-53), required while anything stays owed; a known customer with none gets a line, never a block. The start is typed, today by default; a package's end is said from its validity, both days counted, and never sent: the server sets it. 2026-10-26, #PRNUM.
"""

edit('features/desk.md', [
    ("**Last Updated:** 2026-10-25", "**Last Updated:** 2026-10-26"),
    ("""- **Reception's unpriced close says so** (DI-28): «لا سعر لهذه الزيارة. تُغلق بدون سعر، ويحدّده المالك لاحقًا.», and asks the phone the whole is left to. 2026-10-24, #116.
""", """- **Reception's unpriced close says so** (DI-28): «لا سعر لهذه الزيارة. تُغلق بدون سعر، ويحدّده المالك لاحقًا.», and asks the phone the whole is left to. 2026-10-24, #116.
""" + WEB),
    ("`PayDialog`, `useOpenCheckIns`,", "`PayDialog`, `SubscriptionSheet`, `useOpenCheckIns`,"),
    ("`useFileTitle`, `DeskAbilities`)", "`useFileTitle`, `DeskAbilities`, `SheetEntry`, `SheetChoices`)"),
])

# The web history line: after #122's.
p = D + 'features/desk.md'
s = open(p, encoding='utf-8').read()
marker = '### Web history\n'
i = s.index(marker)
j = s.find('\n## ', i)
end = len(s) if j == -1 else j
block = s[i:end].rstrip('\n')
block += ("\n- #PRNUM — the subscription sheet: a new customer then their subscription, or a known "
          "customer's new one, from an offered package or «مخصّص», over their earlier debts, the parts "
          "said from the answer (finding 125). Carried from #122: the focus back on «⋯» after the edit "
          "and the archive's question; an unchanged phone typed locally not sent.\n")
s = s[:i] + block + ('\n' + s[end:] if j != -1 else '')
open(p, 'w', encoding='utf-8', newline='').write(s)

edit('features/customers.md', [
    ("**Last Updated:** 2026-10-25", "**Last Updated:** 2026-10-26"),
    ("and a customer's file edits, archives and restores them — [desk](desk.md), 2026-10-25, #122.",
     "and a customer's file edits, archives and restores them — [desk](desk.md), 2026-10-25, #122; "
     "the subscription sheet creates a new customer before their subscription (`POST …/customers`, "
     "its own key) — [desk](desk.md), 2026-10-26, #PRNUM."),
])

edit('architecture/findings/125-the-allocations-order-is-not-exposed-to-the-client.md', [
    ("**Status:** Open · **Date:** 2026-10-22", "**Status:** Resolved · **Date:** 2026-10-22"),
])
p = D + 'architecture/findings/125-the-allocations-order-is-not-exposed-to-the-client.md'
s = open(p, encoding='utf-8').read().rstrip('\n')
s += ("\n\n**Resolution (2026-10-26, #PRNUM):** the first. The sheet shows the prior debts and their "
      "total, and the allocation after the request, from the answer: the toast lists each part "
      "`NewSubscription.payments` allocated ([desk › Web decisions](../../features/desk.md#web-decisions)).\n")
open(p, 'w', encoding='utf-8', newline='').write(s)

p = D + 'architecture/findings/README.md'
s = open(p, encoding='utf-8').read()
line = "- [125. The allocation's order is not exposed to the client](125-the-allocations-order-is-not-exposed-to-the-client.md)\n"
assert s.count(line) == 1
s = s.replace(line, '', 1)
resolved = s.index('## Resolved')
after = "- [124. A statement's sums and its payments come from different snapshots](124-a-statements-sums-and-its-payments-come-from-different-snapshots.md)\n"
k = s.index(after, resolved) + len(after)
s = s[:k] + line + s[k:]
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
