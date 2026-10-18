# Review — PR #87, PACKAGES

**Head reviewed:** `9567da9acf7e366a9486c8305ce70b10db1f8526` (`feat/space-packages`), base `5e8c979d`.
At the end, `gh pr view 87 --json headRefOid` gave the same head, `mergeStateStatus` `CLEAN`, and
`origin/main` had not moved from `5e8c979d`.

**Method.** Read only commit objects from `C:\Users\basel\masaha-design-b`: `git diff 5e8c979d...9567da9a`,
`git show <commit>` and `git show 9567da9a:<file>` (and some neighbours on that head: `requireCan.ts`,
`validate.ts`, `uniqueViolation.ts`, `can.ts`, `spaces.service.ts`, `hours.service.ts`,
`shifts.repository.ts`, `test/locks.ts`, the front-desk migration, `schema.prisma`,
`documentation.md`, `workflow.md`). Nothing was run: no test, no npm, no server, no database. **Every
test result below (red runs, the 13 breaks, the lanes, the real run, CI) is the executor's report
(`4_REPORT.md`), not something I checked myself.** What I say about the code and the documents I saw in
the code and the documents.

## Verdict

**No blocker. Approve after one small fix round** (findings 1–3, plus the nits if convenient). The
security boundary, the lock-then-`can()` order, the compound-key scoping and the error mapping are right
as far as I could see in the code. Departure 1's extension to R8 is acceptable (see *Departures*).

## The five most important findings

### 1. should-fix — the edit's own decision under the lock has no test and no break
**Where:** `apps/api/src/modules/packages/packages.service.ts:107` (`update`'s `lockFor`); tests T9/T10
at `packages.api.test.ts:337` and `:354` exercise **POST only**.
**Scenario:** delete line 107, or have `update` call `can(actor, 'packages.manage', space)` on the
loader's links instead. Every test still passes. Reception's PATCH is still refused by `requireCan` at
the route (T16). The foreign id is still refused by `findIn`'s compound key (T14). The owner's edits
(T11–T13, T15) still succeed. So an owner unlinked while their PATCH waits is not refused, and a PATCH
to a space deleted meanwhile writes. B9 and B10 break the shared `lockFor` and only redden the create
tests, so this second call site is not proven. testing §3 rule 7 wants each authorization decision
shown by a break.
**Fix:** add the two races for PATCH, in the same shape as T9/T10. (a) Owner unlinked meanwhile → 403,
row unchanged, no `package.edited` entry. (b) Space soft-deleted meanwhile → 404, row unchanged. Break
each by removing `lockFor` from `update`, or by deciding on `space` instead of `linksUnder(tx)`. Both
inherit finding 77's caveat, like T9/T10.
**Where its fix belongs:** a fix round on this PR.

### 2. should-fix — all four commits have no body
**Where:** `1202d322`, `bfcab517`, `130487fc`, `9567da9a`. For each one, `git log -1 --format=%b`
prints nothing.
**Scenario:** `docs/development/workflow.md:87`: "≤ 50 chars; the body explains *why*". Plan §11:
"Bodies say *why* in one or two lines". Every non-merge commit on `main` I looked at has a body. The
report does not list this as a departure.
**Fix:** reword each commit with a one- or two-line *why*, then push with `--force-with-lease`. This
can ride on the same rewrite as the folded fixes.
**Where its fix belongs:** a fix round on this PR.

### 3. should-fix — an unplanned edit to another capability's line in the documentation map
**Where:** `docs/README.md:18`, in commit `bfcab517`. The `spaces.md` line's em dash `—` became a
hyphen `-`.
**Scenario:** plan A.7 only adds the packages line *after* the spaces line. Now the spaces line is the
only entry in the features list with a hyphen. This is a drive-by change to a line the item does not
own, and the report's "Nothing else departed" misses it.
**Fix:** restore `—` on line 18, folded into `bfcab517`.
**Where its fix belongs:** a fix round on this PR.

### 4. nit — the overview's new line sits before the Spaces line, not after it
**Where:** `docs/project/overview.md:23–24`.
**Scenario:** plan A.8 says "A new line after the Spaces line". As built, *Packages* (23) comes before
*Spaces* (24). The new capability is listed ahead of the one it depends on, and the order differs from
the map (`docs/README.md`, where packages follows spaces).
**Fix:** move line 23 below line 24, folded into `9567da9a`.
**Where its fix belongs:** a fix round on this PR.

### 5. nit — T15 asserts the database's id sequence, not the behaviour
**Where:** `apps/api/src/modules/packages/packages.api.test.ts:495`:
`expect(alpha.id).toBe(beta.id - 1)`.
**Scenario:** the plan does not have this line, and it proves nothing the title claims. It holds only
because two inserts in a row take consecutive sequence values. If a refused insert, or anything else,
used up a value in between, the test would fail with the behaviour still correct. It looks like it was
added only so the `alpha` variable is used.
**Fix:** assert that `Alpha` is unchanged instead (its stored name and `shiftId`). That is what "on
their fields, changing nothing" needs anyway.
**Where its fix belongs:** a fix round on this PR.

## The rest

### 6. nit — the contract's §4 exception list now has a full stop mid-list
**Where:** `docs/api/api-contract.md:64–65`.
**Scenario:** line 64, formerly the last item, still ends with `.`. The new last item, 65, also ends
with `.`. The items before 64 end with `;`.
**Fix:** end line 64 with `;`.
**Where its fix belongs:** a fix round on this PR (C2).

### 7. nit — `written`'s comment names only the unique violation
**Where:** `apps/api/src/modules/packages/packages.repository.ts:31`: "A write, or its unique violation
turned into the field that is refused."
**Scenario:** the function also turns P2003 into `shiftId`, which the next sentence explains. The
opening line undersells it.
**Fix:** "A write, or the key that refused it, turned into its field."
**Where its fix belongs:** a fix round on this PR (C3).

### 8. nit (the report, not the PR) — `4_REPORT.md` contradicts itself
**Where:** `4_REPORT.md`. *The commits* lists C2 as `edcb9dc4`, the pre-rewrite sha. *What is done, and
where it stands*, *Not run, and why* and *The environment* are left over from the stop at R6: they say
C3 is uncommitted and that the breaks, the real run, the push and CI "were never reached". The sections
above them record all of those as done. "Nothing else departed" is also untrue given findings 2 and 3.
**Fix:** delete the three stale sections, correct the C2 sha, and add findings 2 and 3 to *Departures*.
**Where its fix belongs:** the fix round (the report is updated with it).

### 9. nit — a retired package that keeps its shift blocks that shift's removal
**Where:** behaviour of `shifts.repository.ts` `remove` (P2003 → `inUse`) together with
`packages_shift_id_space_id_fkey` (`ON DELETE NO ACTION`). The contract's hours line (`api-contract.md`
§5, `PUT …/hours`) already says a shift "still used by … a package" refuses its removal.
**Scenario:** the owner retires the «evening» package and later removes the evening shift from the
hours. The answer is 409 with no code, because a package that is no longer offered still names the
shift. The only way out is `PATCH { shiftId: null }` on the retired package, and neither the contract's
packages section nor `packages.md` says so. The rule is consistent with the contract; this is about the
owner being able to find the way out.
**Fix:** none in this API. The owner's packages screen should explain it, or offer to clear the shift.
**Where its fix belongs:** the next item that touches the area (the packages web screen).

## Departures (the report's seven), judged

1. **R6 and R8's choice fields answer `invalid_choice`. Accepted, R8's extension included.** In the code,
   `toFieldErrors` maps `invalid_value` to `invalid_choice`, and the owner's amendment explains the
   mapping as "an enum's failure, absent or not". A `null` on a `z.enum` is one more value the enum
   cannot take, so the same sentence covers it. No new code was introduced, and the refusal still
   names the field, which is what R8's title asserts. The contract's packages section does not say
   what `null` on a required term answers, so nothing in it is contradicted. R8 tests exactly this
   (`requests.unit.test.ts`, the last `it`). That it passes is the executor's report and CI. The owner
   should still know the R8 line was extended by the executor's reading rather than named in the
   amendment.
2. **The BOM in the first C1 message:** fine. `1202d322`'s subject is 44 characters, and I saw no BOM.
3. **B11 needed both edits:** consistent with the code. `findIn` alone by `{ id }` leaves `update`
   scoped, which raises P2025, and `written` does not map that. 500 is the expected answer.
4. **B6/B7 redden T15 too:** consistent. T15 reaches the same `written` through PATCH.
5. **T2's own first red:** fine. The committed T2 seeds once, above the loop.
6. **The 41/42 count:** I counted each subject myself: 44, 39, 40, 41. All are ≤ 50.
7. **`prettier --write`:** fine for code. The new Markdown files (`packages.md`, findings 77–80) still
   end without a final newline. Finding 74 on `main` does too and Markdown is outside Prettier, so this
   is not raised.

## Checked and fine

- **Boundary:** the router is mounted only as `manage.use('/packages', …)` inside the
  `/manage/spaces/:spaceId` mount (`app.ts:362`). No other route reads `packages`: `git grep` outside
  the module finds only the seed, `can.ts` and `app.ts`. No public router. The module's `index.ts`
  exports only the factories.
- **Order of checks:** `requireCan('packages.manage')` comes before `validate` on POST and PATCH, and
  `requireCan` throws before any body is read. `'packages.manage'` is `'owner'` in `can.ts:77`.
- **Lock, then decide:** the service's `lockFor` calls `spaces.lock` (FOR NO KEY UPDATE; `false` for a
  soft-deleted space → 404), then `can()` on `space.linksUnder(tx)` (`packages.service.ts:39–44`), in
  both writes.
- **No cross-space path:** `findIn` and `update` both use the `id_spaceId` compound key. `PackageData`
  has no `spaceId`. `validate` replaces the body with the parsed, key-stripped value (`validate.ts`), so
  `packageChange`'s spread cannot carry `spaceId` or `sortOrder`. There is no read by id.
- **Error mapping:** P2002 is matched only on `packages_space_id_name_key`. The other unique key,
  `packages_id_space_id_key`, does not contain that string, and a write cannot violate it. Under the
  lock, P2003 really can only be the composite shift key: the space's FK cannot miss, because a locked
  row is never hard-deleted (soft delete only, and the lock blocks `DELETE`). Anything else is
  rethrown. P2025 cannot be reached, because the row is found under the lock and packages have no
  delete.
- **Concurrency:** `nextPlace` aggregates under the lock in READ COMMITTED, so the second waiter sees
  the first's committed row. Two creates of one name are serialized, and the key decides. A shift
  removal (the hours' `groupEdit`, under the space's lock) and a package write are serialized. Either
  order gives a truthful answer: `invalid_choice` or `inUse`.
- **Schemas:** price `min(1).max(PRICE_MAX_AGOROT)`. The counts go from 1 to the Int max,
  `daysPerWeek` ≤ 7 and `hoursPerDay` ≤ 24, all inside the DB CHECKs (`packages_limits_check`,
  `validity_days > 0`), so validated input cannot hit a CHECK and get a 500. PATCH is `.partial()`
  and only the limits and `shiftId` are nullable. Unknown keys are stripped. An edit that changes
  nothing returns before `update` and audit (`packages.service.ts:110–111`).
- **Audit:** `package.created` with the ten terms, nulls included. `package.edited` with only the
  changed fields, `isActive` included. Both run in the write's transaction, with the space as
  `spaceId`.
- **Tests (read, not run):** the expectations are written by hand; R1–R8, U1–U5 and T1–T16 match §9
  except finding 5; each break in §12.5 would turn its named test red, by my reading of the code.
- **Documents:** `packages.md` follows the template's ten sections in order, about 1,150 words, `#87`
  on every decision line and in the history. Contract §4 exception and §5 *Packages (managed)* (S1's
  409, reception's 403 before the body). `security.md`, `conventions.md` (§6 bullet, §7 row link, date),
  `v1-mvp.md` (A.6 verbatim), `spaces.md` (A.9). The findings index has four lines under *Open*.
  Findings 77–80 are honest: I checked 77's cited lines in `test/locks.ts` (10, 19, 30, 65) and that
  `vitest.config.ts` sets no timeout, 78's lines in `space.service.ts` (97, 99, 101, 102), and 80's
  CHECK at migration lines 226–227. No `#PRNUM` is left. Nothing in `apps/web`, `prisma/` or the
  dependencies changed, and `data-model.md` is untouched, as S1 requires.
- **Commits:** four, each a complete unit: the docs-only findings commit, then read, add, edit, each
  with its code, tests and documents. Subjects are 44/39/40/41 characters (finding 2 aside).
