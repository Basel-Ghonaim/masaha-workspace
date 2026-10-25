## What

Fixes #109's review finding 1 (**critical**: wrong stored attendance and money). A subscriber's check-out closed the check-in at *now*, while a visit's check-out stops at the stay's due time and the data model (*Auto check-out*) says no path charges a stay into the next day. An overnight `PER_HOUR` check-in, closed by the desk the next morning because the auto check-out had not run, stored every hour up to then in the subscription's minutes and due, with no route to correct it.

The subscriber's check-out now closes at the earlier of now and the stay's due time, from the space's week and settings read under its lock. The cap is one helper, `spaces.stayEnd`, which the visit's check-out now uses too, so the two stays share one rule. The audit keeps the request's own time (`requestedAt`), as the visit's does.

Check-ins already stored past their due time are not corrected here (out of scope; checked separately).

## Carried from #109

- **The open check-in index answers its code, not a 500** (review 2): `createCheckIn` maps the violation of `check_ins_customer_id_key` to a refusal, as `create` does for its foreign key; the service answers `MEMBER_ALREADY_CHECKED_IN`.
- **The contract's *Front desk* introduction** (review 3): the check-ins, a visit's check-out and the payment send an `Idempotency-Key`; a subscriber's check-out sends none.
- **Findings 126 and 127** (reviews 4 and 5): a whole phone finds the other country code one way only; the dated check-in list filters on an expression its index cannot serve (to decide with finding 120).

## Tests and breaks

- `subscriberCheckOut.api.test.ts`: a check-in from Tuesday 20:00, closing 22:00, checked out on Wednesday morning → `checkedOutAt` 22:00, 120 minutes, due and balance ₪12; with `maxStayMinutes` 90 → 21:30, 90 minutes, ₪9; one before its due time closes at now. Red first (840 minutes, ₪84). Breaks: the request's time passed back in → red; the cap without `maxStayMinutes` → red.
- `subscriberCheckIn.api.test.ts`: a test transaction writes an open check-in for the customer without the space's lock while the desk's check-in waits on the index → 409 `MEMBER_ALREADY_CHECKED_IN`. Red first (500). Break: the mapping removed → 500 → red.
- Locally: lint, typecheck, `test:unit`, the full `test:api`, `format:check`, `check:links`. CI judges `test:component`, the web build, `check:build` and `check:classes`.
- No real run: the API test proves the time; the demo data holds no overdue check-in.

No migration, no new dependency.
