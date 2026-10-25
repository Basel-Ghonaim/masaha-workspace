"""Commit 4's documents: desk.md, visits.md, architecture §2 and §3, overview.md, docs/README.md, finding 161."""
from pathlib import Path

APP = Path('C:/dev/masaha/app')


def edit(rel: str, pairs: list[tuple[str, str]]) -> None:
    path = APP / rel
    text = path.read_text(encoding='utf-8')
    for old, new in pairs:
        if text.count(old) != 1:
            raise SystemExit(f'{rel}: not once: {old[:70]!r}')
        text = text.replace(old, new)
    path.write_bytes(text.encode('utf-8'))


DATE = '2026-10-24, #PRNUM'

edit('docs/features/desk.md', [
    ('The API is built; no web screen yet.',
     'The API is built; on the web, the desk\'s screen («مكتب الاستقبال»): who is present, a visit\'s check-in and check-out with its payment.'),
    ('> **Scope:** the API module `desk` (L5); `@masaha/shared/desk`. No web feature yet.',
     '> **Scope:** the API module `desk` (L5); `@masaha/shared/desk`; the web feature `features/desk`, dashboard-only: the desk\'s screens.'),
    ('No web screen yet; the shared desk device is not settled (who signs out an idle reception account, and switching staff on one device): the desk\'s screen item.',
     f'On the dashboard, the owner and reception work «مكتب الاستقبال» ({DATE}). On the shared desk device, «تبديل الموظف» signs the person out on the server and opens sign-in with the desk as the page to return to; the server\'s idle sign-out of a reception session is planned (the desk\'s screen item, its spec C).'),
    ('## Decisions\n', f'''**The desk on the web** (`features/desk`, composed by `pages/dashboard/space/desk/`). The page shows [occupancy](occupancy.md)'s people present and live status control, with this feature's «خروج» in each row, and «تسجيل زيارة» in the top bar from 768 px and in the bar at the foot below it.
- **The check-in** asks the visitor's name, «طالب» only where the terms carry student rates for the chosen shift, and «الوردية» only where the space has shifts, the current one on Gaza's clock chosen; it says the rate the visit will copy, from `visit-terms`, and, while the space is full, that it may still be checked in. It is sent at once: the server's warnings (`SPACE_FULL`, `OUTSIDE_OPENING_HOURS`, `CLOSURE_IN_FORCE`) are said after, in the toast, which then stays until it is closed.
- **The check-out** reads the visit's quote on opening and each minute while open, and reads it again before sending when it is older than 4 minutes; a changed due stops the send and says the new one. It sends the quote's time and the amount recorded, never more than the due. The money block fills «المستلم الآن» with the due and follows it until a figure is typed, and says one of four facts under it: paid in full, the change, the credit, or what stays owed and by whom. A remainder on a visit with no customer asks a name and a phone, which stay once shown. A visit with no rate asks a typed price and its reason of whoever may type one (`mayTypePrice`); whoever may not closes it unpriced, with a phone, the whole left owed. The toast says what the answer recorded: the amount and its method, or nothing paid, or unpriced, and what stays owed.
- **One intent, one key:** each opening of the check-in or the check-out holds one `Idempotency-Key`, kept across the transport's re-sends, a second press and «إعادة المحاولة» ([architecture §7](../frontend/architecture.md#7-server-state)). A lost answer says a retry is safe; a refusal says nothing was recorded, before its reason.

## Decisions
'''),
    ('## Code map\n', f'''### Web decisions

- **`desk` on the web holds the desk's screens** (S1): it calls the desk module's routes and those of `visits` the same staff call on the same screens (the terms, the quote); the state now and the override are [occupancy](occupancy.md)'s, and the page sets one in the other's slot. *Why:* a feature per module would put every dialog that reads one module and writes another in the page. {DATE}.
- **The desk sends a write once, beyond the transport's rule** (S3): only a keyed write is re-sent by the transport; the override is sent once, and a lost answer is the user's to retry. {DATE}.
- **One key per intent** (S4): a dialog's opening makes its key; a retry, a second press and an edit of the form keep it; a new opening is a new key. *Why:* ADR 0015 rule 1; a key per press would record twice on a double press over a weak connection. {DATE}.
- **The warnings are the server's, said after** (S6): a check-in is never held for a warning the browser would have to work out a second time. {DATE}.
- **Money is agorot end to end, and the due is the server's** (S7): the web computes only the line under the money block — recorded, change, what stays — never a charge. {DATE}.
- **Every line after a write is worded from the answer** (S8), never from the form. {DATE}.
- **The keyboard at speed** (S10): each dialog's first field takes the focus («المستلم الآن», or the typed price with no rate); Enter submits; when the person whose «خروج» had the focus leaves the list, the focus goes to the next row's «خروج», else to the list's heading. {DATE}.
- **Two failure lines, two facts** (DI-8): no answer — «لم يصل الرد. أعد المحاولة — لن تُسجَّل مرتين.»; a refusal — «لم يُسجَّل شيء.» before its reason. {DATE}.
- **A typed price carries its reason** (DI-10), «سبب السعر», required, as the contract requires. {DATE}.
- **«لم يدفع شيئًا» goes both ways** (DI-12): at nothing received it reads «استلام المبلغ كاملًا» and gives the due back. {DATE}.
- **The debt's fields stay once shown** (DI-13), required only while something stays owed. {DATE}.
- **Row actions are 44 px on touch** (DI-16): «خروج» takes the layer's default size, and the bar's «تسجيل زيارة» `size="lg"`. {DATE}.
- **The due has its own weight** (DI-25), and **one money fact under the block** (DI-26). {DATE}.
- **Reception's unpriced close says so** (DI-28): «لا سعر لهذه الزيارة. تُغلق بدون سعر، ويحدّده المالك لاحقًا.», and asks the phone the whole is left to. {DATE}.

## Code map
'''),
    ('The idempotency key\'s header and schema are in `core`.\n',
     'The idempotency key\'s header and schema are in `core`.\n- **Web:** `apps/web/src/features/desk/`, entry `index.ts` (`CheckOutAction`, `VisitDialog`, `useVisitDialog`, `useVisitTermsQuery`), read by `pages/dashboard/space/desk/`: the repository in `repository/`; the keys, the shared write (`useDeskWrite`: the space read again, a link ended), the terms, the check-in, the check-out and its quote, and the money block in `hooks/`; the rates, the current shift, the money line, the quote\'s age, the warnings\' lines and the dialogs\' failure in `services/`; the dialogs, the money block and the toasts in `components/`. The key per intent is `shared/api`\'s (`useIntentKey`). Words: the catalogue\'s `desk` section.\n'),
])
text = (APP / 'docs/features/desk.md').read_text(encoding='utf-8').rstrip('\n')
text += '\n\n### Web history\n\n- #PRNUM — the desk\'s screen: who is present (from `occupancy`), a visit\'s check-in with its warnings and its check-out with its payment, one key per intent, and «تبديل الموظف».\n'
(APP / 'docs/features/desk.md').write_bytes(text.encode('utf-8'))

edit('docs/features/visits.md', [
    ('they read the quote and the terms through this module\'s own routes.',
     f'they read the quote and the terms through this module\'s own routes; on the web, the desk\'s screen reads both ([desk](desk.md), {DATE}).'),
])

edit('docs/frontend/architecture.md', [
    ('A sub-part with the same audience and the same screens stays inside its module\'s feature. Check-ins stay in `subscriptions`, for example, because a check-in changes the subscription\'s progress: split apart, one feature would have to import the other\'s query keys.',
     f'A sub-part with the same audience and the same screens stays inside its module\'s feature. Check-ins stay in `subscriptions`, for example, because a check-in changes the subscription\'s progress: split apart, one feature would have to import the other\'s query keys. **The exception, `desk`:** `desk` on the web holds the desk\'s screens: it calls the desk module\'s routes and those of `visits`, `payments`, `customers` and `subscriptions` that the same staff call on the same screens; each of those capabilities gets a web feature of its own only with a screen of its own (step 9\'s payments) (S1, {DATE}).'),
    (', each space page with a screen loaded lazily from the routes\' own map.',
     f', and «مكتب الاستقبال», which composes [occupancy](../features/occupancy.md)\'s people present and live status control with [desk](../features/desk.md)\'s check-out in each row and its visit\'s check-in ({DATE}), each space page with a screen loaded lazily from the routes\' own map.'),
])

edit('docs/project/overview.md', [
    ('the unpriced visits the owner prices, and the uncollected visits, collecting a visit\'s debt or the owner\'s write-off ([visits](../features/visits.md), [payments](../features/payments.md)).',
     'the unpriced visits the owner prices, and the uncollected visits, collecting a visit\'s debt or the owner\'s write-off ([visits](../features/visits.md), [payments](../features/payments.md)); on the dashboard, the desk: who is present, the live status and its override, a visit\'s check-in and check-out with its payment.'),
])

edit('docs/README.md', [
    ('the customers list and file, and a customer\'s archive (API only).',
     'the customers list and file, and a customer\'s archive; on the web, the desk\'s screen: who is present, a visit\'s check-in and check-out with its payment.'),
])

(APP / 'docs/architecture/findings/161-no-route-reads-the-visits-of-a-day.md').write_bytes(
    ('# 161. No route reads the visits of a day\n\n'
     '**Status:** Open · **Date:** 2026-10-24\n\n'
     '**Evidence:** The desk\'s design has an attendance log tab («السجل»), the day\'s visits and check-ins. The API answers a space\'s subscriber check-ins by date (`GET …/check-ins?from&to`), but no route reads its visits by date: the open ones come with the state now (`GET …/occupancy`), the uncollected ones from `…/uncollected-visits`, and the plan\'s `GET …/visits` with a date range is not built ([v1 plan](../../plans/v1-mvp.md)). The desk\'s screen (#PRNUM) leaves the tab out.\n\n'
     '**Resolves when:** the planned `GET /manage/spaces/:spaceId/visits` with a date range is built, and the desk\'s log tab reads it.\n').encode('utf-8'))

edit('docs/architecture/findings/README.md', [
    ('- [138. A failed refresh keeps a status that still reads live](138-a-failed-refresh-keeps-a-status-that-still-reads-live.md)\n',
     '- [138. A failed refresh keeps a status that still reads live](138-a-failed-refresh-keeps-a-status-that-still-reads-live.md)\n- [161. No route reads the visits of a day](161-no-route-reads-the-visits-of-a-day.md)\n'),
])
print('docs ok')
