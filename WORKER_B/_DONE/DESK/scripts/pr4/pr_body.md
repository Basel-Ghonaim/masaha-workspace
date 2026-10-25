## Summary
The desk finishes a closed visit's money. It can now take a payment after the check-out (`POST …/payments`) and record «تسجيل دينًا», which leaves the debt to the phone's customer (`PUT …/visits/:visitId/customer`). The owner can write a visit off («لن يُحصَّل»), and undo it (`POST` / `DELETE …/visits/:visitId/write-off`). A written-off visit takes no payment and leaves the uncollected visits. Finding 100 is resolved: a visit's customer is kept.

### Carried from #97
Its review was small enough for this PR's first two commits:
1. **The auto check-out keeps closing stays past a failing one** (`fix(jobs): …`). Each stay is caught on its own, logged as `stay not closed` with its id, and counted; the job then fails, so the cron sees a 500.
   - A space with no settings row fails only its own stays: `settingsFor` leaves it out.
   - Test: two stays, the first failing. Two breaks, both red.
2. **Every stay closes by its day's end** (`fix(visits): …`, the owner's choice (b), widened). A stay is due at the earliest of: the closing (when on), the stay limit (when set), and 23:59 of its check-in's Gaza day (always).
   - Unit tests for all three branches, a break each, all red.
   - This also resolves #95's nit 9: a charge is now bounded by one day.
3. `visits.md`'s boundary (*Leaves*, *How it composes*).
4. The scheduler's local timing has one home (conventions §12), and the `.env.example` comment is reworded.
5. The runbook names the jobs' header exactly.
6. `v1-mvp.md` step 7's *Built* line is reworded (in C4).
7. Findings recorded: 111 (#95's nit 7), 112 (#95's nit 8) and 113 (#97's growing uncollected read).

## Scope
- Migration `visit_write_off`: `written_off_at`, `written_off_by_id` and `write_off_reason`, with a `CHECK` (set together, never blank, only on a closed, priced visit). `payments_guard_insert` gains a fourth rule: `payments_visit_written_off`.
- `DeskVisit.writeOff` on every visit answered.
- The four routes, in `desk`, described in the summary.
- `can()`'s `visits.writeOff`, for the owner only.
- The uncollected visits leave written-off visits out.
- One unpaid-part rule (`customerFor`) for the check-out, the payment and «تسجيل دينًا» (finding 100).
- Error codes `VISIT_ALREADY_PAID`, `VISIT_WRITTEN_OFF` and `VISIT_HAS_CUSTOMER`. `VISIT_NOT_PRICED` is reused for the write-off, with both of its lines made general.
- Documents: the contract, the data model, conventions, security, ADR 0009 (a row and a *Revised* line), `desk.md`, `payments.md`, `visits.md`, `space-settings.md`, `v1-mvp.md`, `overview.md`, `docs/README.md`, finding 100 (resolved), and the new findings 110–113.

## Acceptance criteria
- [x] A payment on a closed, priced visit is recorded with who took it and answered 201 with what remains. Each refusal writes nothing and comes before any phone is asked for:
  - above the balance: `PAYMENT_EXCEEDS_DUE`;
  - an unpriced visit: `VISIT_NOT_PRICED`;
  - a written-off visit: `VISIT_WRITTEN_OFF`;
  - an open visit: 409, no code.
- [x] Part left unpaid on a visit with no customer needs a phone (422); the phone finds or creates the customer. A visit with a customer keeps it, and another phone is refused (`VISIT_HAS_CUSTOMER`). The check-out follows the same rule.
- [x] A retry with the same key answers 201 with the first payment. Two requests with one key at once record one payment. A key that paid another item is a conflict.
- [x] «تسجيل دينًا» attaches the customer, with no payment, and is audited. The same phone again changes nothing. It is refused on a written-off visit, a paid one, an open one, and one that is another customer's.
- [x] The owner writes off the balance of a closed, priced visit with a reason, audited; payments stay. Refused for an unpriced visit, a settled one, an open one, and for reception (403). A second write-off answers the visit as it is.
- [x] The undo clears the write-off and is audited with what it was. Undoing a visit not written off writes nothing.
- [x] A written-off visit is not among the uncollected visits.
- [x] Every write takes the space's lock first and decides `can()` on the links read under it. Each race has its test and its break.

## Out of scope
- The desk's screen and dialogs (worker A's later item), and the shared desk device.
- Voids, the payments list, collections per staff member and finance: step 9.
- A subscription's payment and customer debt as a read: step 8.
- Finding 17's sweep.

## Change type
feat: API code, the shared contract, tests and documents. One migration (three columns, a `CHECK`, the payments trigger's fourth rule). The new codes' catalogue lines in `apps/web`, under worker B's licence.

## New error codes (the Arabic needs the owner's approval)
| Code | Answer | English | Arabic |
|---|---|---|---|
| `VISIT_WRITTEN_OFF` | 409 | This visit was written off; the owner must undo the write-off before it takes a payment. | سُجّلت هذه الزيارة «لن يُحصَّل»؛ يتراجع المالك عن ذلك أولًا قبل استلام أي دفعة لها. |
| `VISIT_ALREADY_PAID` | 409 | This visit is already paid in full. | دُفع مبلغ هذه الزيارة كاملًا. |
| `VISIT_HAS_CUSTOMER` | 409 | This visit is already another customer's debt. | هذه الزيارة دينٌ على زبون آخر بالفعل. |
| `VISIT_NOT_PRICED` (revised) | 409 | This visit has no price yet; price it first. | لم تُسعَّر هذه الزيارة بعد؛ سعّرها أولًا. |

## Evidence
- **`lint` and `typecheck`:** run on each commit after the rebase on #98 (`git rebase -x`), all OK.
- **On the head:**
  - `test:unit`: exit 0 (233, 797 and 858 tests, all passed);
  - `test:api`: exit 0, `Tests 998 passed (998)`;
  - `format:check`: exit 0;
  - `check:links`: exit 0, `2455 links … all resolve`;
  - `build -w @masaha/shared`: exit 0.
  - The first `test:api` run was killed for memory. The re-run passed, and it covers the code as it stands: the rebase brought in only web and docs changes.
- **Seen failing first:** every new test, in its lane:
  - U1–U4;
  - D1 and D2, through breaks B5 and B6;
  - T1–T34;
  - the two carried tests.
- **Deliberate breaks, each red then restored** (SHA-256 checked):
  - the carried ones: C0a-1 and C0a-2, C0b-1 to C0b-3;
  - B1–B39 (B12 has no break of its own; B1 covers it);
  - B5 and B6 on the test database, with B6 also run on T22.
- **Real run on 3321** (`masaha_b_dev`), every case answered as planned:
  1. listed;
  2. no phone: 422;
  3. with a phone: 201, balance 1500, the customer created;
  4. the same key: 201, the same payment;
  5. above the balance: 409 `PAYMENT_EXCEEDS_DUE`;
  6. «تسجيل دينًا»: 200, and again 200 with nothing written;
  7. write-off as reception: 403;
  8. write-off as the owner: 200;
  9. the visit gone from the uncollected list;
  10. a payment on it: 409 `VISIT_WRITTEN_OFF`;
  11. undo: 200, listed again;
  12. the rest paid: 201, balance 0.
- **Not run:** `test:component`, the web's `build`, `check:build` and `check:classes`. The web change is two catalogues of strings, and CI runs them.

## Departures from the plan
- The plan's `balancesOf` (a list) is `balanceOfVisit` (one visit). Each caller has one visit, and lint forbids the `!` needed to read one entry back from a map.
- `customerFor` compares the phone with the visit's customer's stored phone; there is no new lookup in `customers`. The answer differs only for an archived customer whose number was reused: this keeps the visit's own customer, where the plan's lookup would refuse.
- `v1-mvp.md` and `overview.md` are edited once, in the last commit.

## Screenshots
None: API and documents only.

## Definition of Done checklist
- [x] Acceptance criteria met, scope kept.
- [x] Lint and typecheck clean; `packages/shared` builds.
- [x] Tests added in the owning lanes, each seen failing.
- [x] No hardcoded user-facing text (codes only; both catalogues).
- [x] Authorization on the server (the boundary, `requireCan`, `can()` under the space's lock).
- [x] Triggered documentation updated in this PR.
- [x] One home per fact; nothing claimed that is not built.
- [x] Every claim names its test or command.
- [x] Atomic history, pushed.
