# S2b-4b — The admin's space editor: opening hours with shifts, and prices (web) — PLAN

> **For the executor.** This plan stands alone. It is written for any capable coding agent (Claude Code,
> Copilot, Codex) that has **not** seen the planning conversation. Read `CLAUDE.md`, then this plan, then
> only the documents and files it names. **Do not re-decide anything written here**: every decision has
> its reason so you can tell a slip from a choice. When something is not covered, follow §16 *Stop and
> ask*. The owner approved this plan on 2026-10-13, with the four design answers in §4 (D2, D3, D4, D6) and §9 (A–D).
>
> Repository: `C:\Users\basel\masaha` (worker A's main folder), Windows 11, Git Bash and PowerShell, Node 24.
> Databases `masaha_dev` / `masaha_test` (already migrated); API port 3320; web port 5320.
> Branch: `feat/space-hours-prices`, cut from the **latest** `origin/main` (main moved on 2026-10-13: #77,
> the photos API, merged; nothing in it changes `AdminSpace`, the hours or the prices schemas).
> Report: `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\S2B4B_REPORT.md`. Screenshots:
> `C:\Users\basel\Downloads\s2b4b-shots\` (never committed).

---

## 1. Summary

The admin's space editor (`apps/web/src/features/spaces/`, built by PR #74) draws three of the five fact
groups: «المساحة», «المرافق», «التواصل». This item adds the other two, as sections built exactly like
those three (each saves alone, is dated, confirmed, guarded on leaving, and read-only on a verified space):

- **«ساعات العمل» / "Opening hours"**: the week (Saturday first), each day open or closed with «من» and
  «إلى», «نسخ إلى كل الأيام» in the header, and the shifts (up to 10), saved together in one
  `PUT /admin/spaces/:id/hours`.
- **«الأسعار» / "Prices"**: up to 40 prices, a small table from `md` and one card per price below it,
  saved whole in one `PUT /admin/spaces/:id/prices`.

It also folds **finding 60**: the area field shows a space's own area that was hidden since, marked
«(مخفية)», instead of an empty field.

Web and documents only. No change in `apps/api` or `packages/shared`; no new dependency; no new error code.

## 2. The contract (it goes into the PR description)

**Scope**
- «ساعات العمل»: the week and the shifts in the editor, saved, dated and confirmed as one group.
- «الأسعار»: the space's prices in the editor, saved, dated and confirmed as one group.
- Both in the editor's navigation, the «ما زال ناقصًا» checklist, the leave guard, and a verified space's
  read-only page.
- Finding 60: a space's own hidden area shows in its area field, marked hidden.

**Acceptance criteria**
- [ ] A space whose hours were never saved shows the template: Saturday to Thursday 08:00–18:00, Friday
      closed, no shifts; «لم تُضف بعد» and Save only; its first save sends the template and dates it.
- [ ] Each day is «مفتوحة» or «مغلقة» by its switch; «إلى» takes 24:00 as a day's end (sent as 1440);
      times are 24-hour, Western digits, left to right in Arabic too; Arabic digits typed are read.
- [ ] «نسخ إلى كل الأيام» copies the first open day's range (Saturday first) to every open day; closed
      days stay closed; disabled while no day is open, the line under it saying why.
- [ ] A shift outside every open day is refused on the shift before anything is sent; a shift that fits
      some open days only names the days it does not apply on, as a helper.
- [ ] A shift that a saved price uses cannot be removed: its remove button is disabled with the reason
      beside it; the server's 409 on a removed shift in use says so and fetches the space again.
- [ ] Shifts keep their ids; the English name is optional; at ten, «إضافة وردية» is disabled with why.
- [ ] Prices: period «الفترة», audience «لمن» (الجميع · الطلاب), shift, custom label (Arabic, then
      English), amount in shekels (₪, up to two decimals, above zero); the labels once in the table's
      header from `md`, one card per price below; at forty «إضافة سعر» is disabled with why.
- [ ] A repeated price is refused on the field that would tell it apart; an amount empty, zero or not an
      amount is refused on its field; all before anything is sent.
- [ ] «الوردية» lists the space's saved shifts only; with none, it is disabled and a line says
      «أضف ورديات أولًا»; while «ساعات العمل» has unsaved changes, a line says to save them first.
- [ ] Both sections: «تغييرات غير محفوظة», discard, «المعلومات ما زالت صحيحة», «قديمة», the date,
      a save that changes nothing sends nothing, a 429 holds Save and the confirmation with its wait,
      403 turns the page read-only, 404 shows the 404 — as the first three sections do.
- [ ] The navigation lists the five sections; every checklist line links to its section; the leave
      guard names «ساعات العمل» and «الأسعار».
- [ ] A verified space shows its hours (each day, its shifts) and its prices (each price, its amount in
      ₪) to read.
- [ ] Finding 60: a space whose area was hidden since shows that area in the area field, marked
      «(مخفية)», and the area is offered to no other space.

**Out of scope**
- The gallery («الصور», S2b-4c); the owner's editor (O1/O6: the owner's page shows prices as a link to
  Packages); `apps/api`, `packages/shared`; the prototype in `docs/design/` (its «المدة»/«الفئة» words
  catch up later — recorded in the report, not touched).

## 3. The reading done (and what the executor reads)

Planning read: `CLAUDE.md`; `docs/development/workflow.md`; `docs/README.md`; the findings index and
findings 27, 55, 59, 60; `docs/features/spaces.md` (whole, as on `main` after #77);
`docs/api/api-contract.md` › *Spaces (the admin)* (`PUT …/hours`, `PUT …/prices`, the confirms);
`packages/shared/src/spaces/requests.ts` and `responses.ts`; `packages/shared/src/core/fieldErrors.ts`;
the editor's code (`components/editor/*`, `hooks/editor/*`, the three sections' hooks, components and
tests, `repository/spacesRepository.ts`, `services/amenitiesForm.ts`, `services/profileChanges.ts`);
`apps/web/src/shared/forms/` (`useServerForm`, `schemaResolver`, `applyServerError`, `fieldMessage`);
the design system's `Field`; `features/lookups` (`AreaSelect`, `useAreaOptions`, `useAreaName`,
`useGovernoratesQuery`); `docs/frontend/architecture.md` §3, *Forms*, §7;
`docs/frontend/design-system/foundation.md` §5, §8, §9, §10, §12; `docs/frontend/localisation.md`;
`docs/development/testing.md` §1–§4; the prototype (`docs/design/prototype/masaha/profile-a.jsx` hours,
`profile-b.jsx` prices); the frames in `C:\Users\basel\Downloads\a-edit-space-screens\`; the design
decisions (`DECISIONS_ADMIN.md` › *Hours*, *Prices*, *Amended 2026-10-12*; `DECISIONS_OWNER.md` › O1, O6;
the review's AD-007, AD-008, AD-009); PR #74's description and its "Review fixes" comment.

**The executor reads, before building:** `CLAUDE.md`; `docs/development/workflow.md` §3–§5, §9;
`docs/development/testing.md` §1–§3; `docs/frontend/architecture.md` §3 and *Forms*;
`docs/features/spaces.md` › *The space editor on the web* and *Web decisions*; the files named in §9;
and the existing code it copies (named in §9 per file).

## 4. The settled decisions, as they will be built

- **D1 — Scope:** hours with shifts, and prices. No gallery (its own item, S2b-4c).
- **D2 — Midnight:** no «24 ساعة» switch. «إلى» accepts `24:00` as a day's end (sent as `1440`); «من»
  does not (00:00–23:59). Each day reads «مفتوحة» or «مغلقة». A range 0–1440 is the contract's
  open-all-day and needs nothing special. **Layout (owner's answer):** a **day's** «من»/«إلى» sit side by
  side at every width (two narrow fields); a **shift's** «من»/«إلى» sit side by side from `md` and stack
  below it (AD-007). Both are labelled `Field`s.
- **D3 — «نسخ إلى كل الأيام»** in the section's header. **(owner's answer)** It copies the first open
  day's range, in the shown order (Saturday first), to **every open day**; closed days stay closed. While
  no day is open it stays visible, **disabled**, and the line under the header says
  «افتح يومًا واحدًا على الأقل.» (foundation §10: a disabled control shows its reason beside it).
- **D4 — A shift lies inside the range of at least one open day** (the shared rule, `updateSpaceHoursSchema`).
  **(owner's answer)** A shift outside every open day is refused with «خارج ساعات كل يوم مفتوح»
  («لا يوم مفتوح بعد» when no day is open). A shift inside some open days but not all gets a **helper,
  not an error**, naming the open days it does not apply on: «لا تنطبق يوم الخميس». The shift's English
  name is marked optional.
- **D5 — The price table's words are O6's:** «الفترة» / "Period"; «لمن» / "For" with «الجميع» /
  "Everyone" and «الطلاب» / "Students". A small table from `md`, the labels once in its header; one card
  per price below `md`; every amount above zero; «إضافة سعر» disabled at 40 with its reason; a repeated
  row refused on the field that tells it apart. (The prototype still says «المدة»/«الفئة»: say so in the
  report; do not touch `docs/design/`.)
- **D6 — «الوردية» lists the space's saved shifts only** (`space.hours.shifts`). None → every row's
  shift field is disabled. **(owner's answer)** The two lines are said **once, above the price rows**,
  not under each row: «لا ورديات محفوظة — أضف ورديات أولًا.» while there are none, and
  «احفظ ساعات العمل لتظهر الوردية الجديدة هنا.» while «ساعات العمل» has unsaved changes. Each section
  still saves alone.
- **D7 — A shift a saved price uses cannot be removed:** its remove button is disabled and
  «يستعملها سعر — احذف السعر أولًا» shows beside it, read from `space.prices` (the saved prices). The
  server's 409 on the hours save stays handled (a price saved meanwhile elsewhere): see S1.
- **D8 — Finding 60 folded:** a space whose area was hidden since shows that area in the area field,
  marked «(مخفية)», instead of an empty field; the finding is resolved in this PR.
- **D9 — #74's patterns, as its review corrected them:** each section saves alone through its own hook
  (`useSaveGroup`); a save's "nothing changed" is judged **against the group as the form was last filled
  from** (kept in a ref, renewed at each fill), never against a newer server answer; «لم تُضف بعد» with
  Save only while missing; its date, «قديمة», the confirmation; «تغييرات غير محفوظة»; the leave guard;
  403 → read-only, 404 → the 404; a 429 holds Save and the confirmation with its reason (all through
  `useSectionFrame`, unchanged); hooks' logic proven in `renderHook` tests, components' tests for what
  renders, the repository's for paths and bodies.

**Decisions of this plan (each with its reason):**
- **P1 — The week is shown Saturday first, in both languages.** *Why:* it is the space's week in Gaza
  (data model: template Saturday–Thursday; conventions: the week runs Saturday to Friday), not a
  calendar; foundation §12's "Sunday in English" is the date picker's rule.
- **P2 — Day names come from the catalogue**, not `Intl`. *Why:* they compose the switch's name
  («مفتوحة يوم السبت») and the helper; catalogue parity tests them; engines differ in `Intl`'s output.
- **P3 — A time is typed as text** (`Input`, `inputMode="numeric"`, `dir="ltr"`, placeholder `08:00`,
  `maxLength={5}`), not `<input type="time">`. *Why:* the native field cannot hold 24:00 and shows a
  12-hour clock in some locales. It accepts `8`, `08`, `830`, `0830`, `8:30`, `08:30` and Arabic-Indic
  digits; **once the field is left (blur), a time it can read is rewritten as `HH:MM`** (no colon is
  inserted while typing: rewriting under the caret fights the keyboard). A text it cannot read stays as
  typed and is refused on submit.
- **P4 — An amount is typed in shekels** (`Input`, `inputMode="decimal"`, `dir="ltr"`), with at most two
  decimals (agorot), Arabic-Indic digits and the Arabic decimal separator `٫` or `,` read as `.`; it is
  sent as whole agorot (`Math.round(value * 100)`). More than two decimals is refused (`invalid_format`,
  the contract's "not an integer"). A saved amount is shown in the form as shekels: `1500` → `15`,
  `1250` → `12.50`.
- **P5 — The form's field names are the request's paths** (`days.0.opensMinute`, `shifts.2.nameAr`,
  `prices.3.amountAgorot`), holding text that `prepare` converts. *Why:* `useServerForm` reads each
  error's code from the schema's input by path, and places the server's 422 by path; the same names make
  both land on the right field.
- **P6 — A new shift** starts with empty names and the first open day's range (08:00–18:00 when no day
  is open). *Why:* it then lies inside an open day from the start (the prototype's fixed 08:00–13:00
  could fall outside).
- **P7 — A new price** starts as «يوم» / «الجميع» / no shift / no label / empty amount (the prototype's).
- **P8 — The custom label's English field is always shown** (see design issue E). The Arabic and the
  English are stacked in one cell from `md`.
- **P9 — The prices section takes `hoursUnsaved: boolean`** from the editor (`useSpaceEditor` already
  knows which groups are dirty). *Why:* D6's line; the sections stay independent otherwise.
- **P10 — The editor draws all five groups,** so `useSpaceEditor`'s `SECTIONS` becomes `FACT_GROUPS`
  and every checklist line is a link.
- **P11 — A price's amount is shown read-only with `Intl.NumberFormat(locale, { style: 'currency',
  currency: 'ILS' })`**, locale `ar-u-nu-latn` or `en`, no decimals for a whole amount and two otherwise,
  inside `dir="ltr"`. *Why:* localisation › Formatting ("Prices with currency ILS, LTR inside RTL",
  Western digits). It is a service of this feature (`services/priceText.ts`), as `updatedAgo` is; no
  shared formatter exists yet.
- **P12 — Days are joined with `Intl.ListFormat(locale, { type: 'conjunction' })`** in D4's helper
  («الخميس والجمعة», "Thursday and Friday").

## 5. Stronger decisions

Each is something the prompt or the documents leave open or weaker; the recommendation is built.

- **S1 — The hours save's 409 fetches the space again, and says what to do.** *What:* on 409 (a removed
  shift still used by a price, a package, a subscription or a visit), the section shows
  «وردية حذفتها ما زالت مستعملة في سعر أو باقة أو اشتراك، فلم يُحفظ شيء. غيّر ما يستعملها أولًا.» and
  invalidates the space's query, so a price saved meanwhile elsewhere reaches `space.prices` and D7
  marks the shift once the admin discards. *Why:* D7 said "handled"; without the fetch, D7's reason could
  never appear. *Cost:* one `invalidateQueries` in the hook, one test. **Built.**
- **S2 — A 422 on a shift's id (another admin removed it meanwhile) is said, and the space fetched
  again.** *What:* the contract answers `invalid_choice` on `shifts.<i>.id`, a path no field shows; the
  section shows «تغيّرت ورديات هذه المساحة منذ فُتحت الصفحة. تجاهل تغييراتك لتراها كما حُفظت.» and
  invalidates the space. *Why:* otherwise the general "check the fields" line points at no field.
  *Cost:* a `failureLines.validation` line and the invalidation. **Built.**
- **S3 — A price's shift removed meanwhile lands on its field, and the space is fetched again.**
  *What:* `invalid_choice` on `prices.<i>.shiftId` shows «لم تعد هذه الوردية من ورديات المساحة» on that
  row's shift field, and the space's query is invalidated so the options are the shifts as they are.
  *Cost:* a field line and the invalidation. **Built.**
- **S4 — "Nothing changed" is judged against the group as filled** (D9's profile rule) for both new
  sections, though the contacts and the amenities compare with the current space. *Why:* the prompt asks
  for the profile's lesson; for a whole group the two give the same answer, so the older sections are
  left as they are (no drive-by change). **Built for the new sections only.**
- **No document rule is contradicted or weakened.** P1 does not contradict foundation §12 (a calendar
  rule, not a space's week).

## 6. Related findings

- **60 — the area field shows no area for a space whose area was hidden since: folded** (D8). *Cost:*
  `lookups`' `useAreaOptions` reads the admin's governorates (with hidden areas) only when the field's
  value is not in the public catalogue, and adds that one area, marked hidden, at the top of the list;
  one copy line; two tests; the finding resolved. **Note for later, not built:** the owner's editor
  (O1) cannot read the admin's lists; its page will set its own area field.
- **59 — the verified editor cannot name its owner:** not folded (needs the owners' read; out of scope).
- **27 — two dashboard chunks import each other:** not folded; this item adds **no module-level**
  `queryOptions(…)` or `useQuery` call, so it cannot trigger it.
- **55 — a lazy shell's first wait on a busy machine:** not folded; the reason the lanes run alone (§13).
- **44, 46, 63, 64:** do not touch the editor; not folded.
- **New findings:** none planned. Anything the executor observes and does not fix takes number **67**,
  then **68** (one file each in `docs/architecture/findings/`, and a line in the index's *Open* group).

## 7. Files (and the other open items)

All in `apps/web` and `docs`. `apps/api` and `packages/shared` are **not touched**. Open items:
**#78** (`feat/session-ends`, `apps/api` and docs: contract, data model, ADRs 0003/0017, conventions,
security, `auth.md`, `users.md`, findings 16/20/39/51/65 and the index) and **#76** (`design/owner`,
`docs/design/` only). Shared documents with #78: **the findings index** (append-only; this item moves
60 to *Resolved*). No code file is shared. A conflict in a document takes the fast path (§14.9).

### Commit 1 — finding 60 (`features/lookups`)
- `apps/web/src/features/lookups/hooks/list/useGovernoratesQuery.ts` — takes `{ enabled = true }:
  { enabled?: boolean } = {}`, passed to `useQuery`. Same key `lookupsKeys.governorates`.
- `apps/web/src/features/lookups/hooks/area/useAreaOptions.ts` — also returns
  `kept: { value: string; label: string } | null`: when `value !== null`, the catalogue has loaded, and
  no catalogue area has that id, it reads `useGovernoratesQuery({ enabled: <that condition> })`, finds
  the area and its governorate, and returns `{ value: String(id), label: copy.lookups.areaSelect.hidden({
  name: copy.lookups.areaName({ area, governorate }) }) }` (names in the interface's language);
  `null` otherwise, and while that list loads or fails. The doc comment says it.
- `apps/web/src/features/lookups/components/area/AreaSelect.tsx` — renders `kept` as the first
  `SelectItem`, before the groups, when present.
- `apps/web/src/shared/copy/english/lookups.ts`, `…/arabic/lookups.ts` — `areaSelect.hidden`.
- Tests: `hooks/area/useAreaOptions.component.test.tsx`, `components/area/AreaSelect.component.test.tsx`.
- Docs: `docs/features/lookups.md` (*Behaviour and flows*: the area field; *Web decisions*; *Web
  history*), `docs/features/spaces.md` (*Open findings*: remove 60),
  `docs/architecture/findings/60-…md` (status `Resolved`, a resolution line),
  `docs/architecture/findings/README.md` (60 moves from *Open* to *Resolved*, in number order).

### Commit 2 — «ساعات العمل»
- **New** `features/spaces/services/clockTime.ts` (+ `clockTime.unit.test.ts`):
  - `clockOf(minute: number): string` — `0` → `"00:00"`, `510` → `"08:30"`, `1440` → `"24:00"`.
  - `minuteOf(text: string, { end }: { end: boolean }): number | string | undefined` — blank (after
    trim) → `undefined`; a readable time → its minute (`24:00` → `1440` only when `end`); anything else
    → the text as typed (so the schema says `invalid_format`). Arabic-Indic digits `٠–٩` read as `0–9`.
  - `settledClock(text, { end }): string` — what blur writes: `clockOf(minuteOf(...))` when it reads,
    else the text unchanged.
- **New** `features/spaces/services/hoursForm.ts` (+ `hoursForm.unit.test.ts`):
  - `type HoursValues = { days: { open: boolean; opensMinute: string; closesMinute: string }[];
    shifts: { id: number | null; nameAr: string; nameEn: string; startsMinute: string; endsMinute: string }[] }`
    — `days` indexed as the contract (0 = Sunday … 6 = Saturday), always 7.
  - `SHOWN_DAYS = [6, 0, 1, 2, 3, 4, 5] as const` (Saturday first); `DAY_KEYS = ['sunday', 'monday',
    'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'] as const` (catalogue keys by index).
  - `hoursValues(hours: SpaceHours | null): HoursValues` — `null` → the template: every day open
    08:00–18:00 but Friday (index 5) closed, no shifts; a saved closed day → `{ open: false,
    opensMinute: '08:00', closesMinute: '18:00' }` (what opening it starts from); a shift's missing
    English name → `''`.
  - `hoursInput(values): Record<string, unknown>` — `prepare` for the schema: `days[i]` →
    `open ? { opensMinute: minuteOf(o, { end: false }), closesMinute: minuteOf(c, { end: true }) } : null`;
    each shift → `{ ...(id === null ? {} : { id }), nameAr, nameEn: blank ? null : nameEn, startsMinute:
    minuteOf(s, { end: false }), endsMinute: minuteOf(e, { end: true }) }`.
  - `sameHours(request: UpdateSpaceHoursRequest, hours: SpaceHours | null): boolean` — the same week
    (each day `null` or the same two minutes) and the same shifts in the same order (id, Arabic name,
    English name or `null`, both minutes). `hours === null` → `false`.
  - `firstOpenDay(values): number | null` — the first open day in `SHOWN_DAYS` order (contract index).
  - `daysNotCovering(values, shiftIndex): number[]` — the open days (shown order) whose readable range
    does not hold the shift's readable range; `[]` when the shift's times cannot be read, or it fits no
    open day (then it is the error, not the helper).
- `features/spaces/repository/spacesRepository.ts` — `updateHours(spaceId, request:
  UpdateSpaceHoursRequest): Promise<AdminSpace>`: `PUT /admin/spaces/:id/hours`. Its unit test gains a
  case; the confirm `it.each` gains `'hours'`.
- **New** `features/spaces/hooks/hours/useHoursSection.ts` (+ `useHoursSection.component.test.tsx`).
  Copy `useContactsSection.ts` and `useProfileSection.ts` (the `filledFrom` ref).
  - **Input:** `{ space: AdminSpace; onDirtyChange: (group: FactGroup, dirty: boolean) => void }`.
  - **Uses:** `useSaveGroup(space.id, 'hours', (r) => repository.updateHours(space.id, r))`;
    `useServerForm<HoursValues, UpdateSpaceHoursRequest>({ schema: updateSpaceHoursSchema,
    defaultValues: hoursValues(space.hours), fields: FIELDS, prepare: hoursInput, submit, failureTitle:
    section.failureTitle({ section: sections.hours }), fieldLines, failureLines: { forbidden:
    section.verifiedMeanwhile, not_found: section.deletedMeanwhile, conflict: hours.inUse409,
    validation: hours.shiftsChanged } })`; `useFieldArray` on `shifts`; `useWatch` on `days` and
    `shifts`; `useSectionFrame({ space, group: 'hours', form, onDirtyChange })`; `useQueryClient` for
    the invalidations.
  - **FIELDS** (shown order, so a refusal focuses the first): for each day in `SHOWN_DAYS`:
    `days.<i>.opensMinute`, `days.<i>.closesMinute`; then for each shift index 0–9: `shifts.<i>.nameAr`,
    `shifts.<i>.nameEn`, `shifts.<i>.startsMinute`, `shifts.<i>.endsMinute`, `shifts.<i>` (the
    item-level `out_of_range` of D4).
  - **submit:** missing (`space.updatedAt.hours === null`) → always send; else `sameHours(request,
    filledFrom.current)` → `setUnchanged(true)`, reset to the filled values, send nothing. Sending: the
    answer resets the form (`hoursValues(answer.hours)`) and renews `filledFrom`. A refusal with status
    409, or with a 422 key starting `shifts.` and ending `.id`, invalidates `spacesKeys.space(space.id)`
    (S1, S2), then rethrows.
  - **An unchanged section follows the space** (the effect `useContactsSection` has), renewing `filledFrom`.
  - **Returns** (what `HoursSection` renders):
    - `frame: SectionFrameView`;
    - `copyAll: { label; disabled; run }` — `disabled` while no day is open or the form is pending;
      `run` sets every **open** day's two texts to the first open day's, `shouldDirty: true`;
    - `hint: string` — `hours.copyHint({ day })` naming the first open day, or `hours.noOpenDay`;
    - `days: { key: number; name: string; state: string; toggle: { label: string; checked: boolean;
      disabled: boolean; run: (checked: boolean) => void }; opens: TimeField | null; closes: TimeField
      | null }[]` in `SHOWN_DAYS` order, the fields `null` while the day is closed;
    - `shifts: { title; hint; rows: { key; label; nameAr: TextField; nameEn: TextField & { optional:
      string }; starts: TimeField; ends: TimeField; remove: { label; disabled; reason: string | null;
      run } }[]; add: { label; disabled; reason: string | null; run } }`;
    - `TimeField = { label; placeholder; binding; error?: string; helper?: string }` where `binding` is
      `form.field(path)` with its `onBlur` also writing `settledClock(...)` through `setValue(path, …,
      { shouldDirty: true })`; `TextField = { label; binding; error?: string }`.
  - **Rules in the returned values:** a shift's `ends.error` is its own error, else the item-level one
    (`codes['shifts.<i>'] === 'out_of_range'` → `hours.fieldErrors.outside`, or `hours.fieldErrors.noneOpen`
    when no day is open); `ends.helper` is `hours.notOn({ days })` when `daysNotCovering` is not empty;
    a shift's `remove.disabled` is `form.isPending ||` (its `id` is a saved shift's and
    `space.prices.some(p => p.shiftId === id)`), `reason` `hours.inUse` in that second case; `add` is
    disabled at `MAX_SHIFTS` (reason `hours.shiftLimit`) or while pending; a day's toggle is disabled
    while pending; toggling sets `days.<i>.open` with `shouldDirty: true`.
- **New** `features/spaces/hooks/hours/useReadOnlyHours.ts` — `useReadOnlyHours(space)` →
  `{ title, none: string | null /* hours.none when space.hours is null */, days: { key; name; value:
  string /* "08:00–18:00" through hours.range({ from, to }) or hours.closed */ }[], shiftsTitle,
  shifts: { key; name; lang?: 'ar'|'en'; value: string }[] }` (English interface: `nameEn ?? nameAr`,
  `lang: 'ar'` when it falls back; Arabic: `nameAr`).
- **New** `features/spaces/components/hours/HoursSection.tsx` and `ReadOnlyHours.tsx` (design in §8).
- `features/spaces/components/editor/SectionCard.tsx` — an optional `action?: ReactNode`, rendered in
  `CardAction` with the unsaved badge (`className="flex flex-wrap items-center justify-end gap-2"`);
  `CardAction` renders when either is present.
- `features/spaces/hooks/editor/useSpaceEditor.ts` — `SECTIONS` gains `'hours'` (in `FACT_GROUPS`
  order: profile, hours, amenities, contacts).
- `features/spaces/components/editor/SpaceEditor.tsx` — renders `HoursSection` after `ProfileSection`,
  and `ReadOnlyHours` after `ReadOnlyProfile`.
- `features/spaces/components/editor/SpaceEditor.component.test.tsx` — updated and extended (§10).
- `apps/web/src/shared/copy/english/spaces.ts`, `…/arabic/spaces.ts` — `editor.hours` (§11).
- `docs/features/spaces.md` — *What it does* (web line), *The space editor on the web* («ساعات العمل»
  bullet; the checklist bullet), *Web decisions*, *Code map* (§12).

### Commit 3 — «الأسعار»
- **New** `features/spaces/services/pricesForm.ts` (+ `pricesForm.unit.test.ts`):
  - `type PricesValues = { prices: { period: PricePeriod; audience: PriceAudience; shiftId: string /*
    '' = none */; labelAr: string; labelEn: string; amountAgorot: string /* shekels, as typed */ }[] }`.
  - `pricesValues(prices: Price[]): PricesValues` (amount via `shekelsOf`).
  - `shekelsOf(agorot: number): string` — `1500` → `"15"`, `1250` → `"12.50"`, `5` → `"0.05"`.
  - `agorotOf(text: string): number | string | undefined` — blank → `undefined`; digits (Arabic-Indic
    read), one optional separator (`.`, `,` or `٫`), then → `Math.round(n * 100)` when it has at most
    two decimals, else `n * 100` unrounded (a non-integer: `invalid_format`); not a number → the text.
  - `pricesInput(values)` — `prepare`: `shiftId: '' → null, else Number`; a blank label → `null`;
    `amountAgorot: agorotOf(...)`.
  - `samePrices(request, prices: Price[]): boolean` — same rows, same order, every field (`null` for none).
  - `NEW_PRICE` (P7).
- **New** `features/spaces/services/priceText.ts` (+ `priceText.unit.test.ts`): `priceText(agorot,
  language: 'ar' | 'en'): string` (P11).
- `repository/spacesRepository.ts` — `updatePrices(spaceId, request: UpdateSpacePricesRequest)`:
  `PUT /admin/spaces/:id/prices`; unit test case; confirm `it.each` gains `'prices'`.
- **New** `features/spaces/hooks/prices/usePricesSection.ts` (+ `usePricesSection.component.test.tsx`):
  - **Input:** `{ space: AdminSpace; hoursUnsaved: boolean; onDirtyChange }`.
  - **Uses:** as the hours hook, with `updateSpacePricesSchema`, `pricesValues(space.prices)`,
    `prepare: pricesInput`, `failureLines: { forbidden, not_found }`, `fieldLines` per row (§11), and
    `useFieldArray` on `prices`.
  - **FIELDS:** for each index 0–39: `prices.<i>.period`, `.audience`, `.shiftId`, `.labelAr`,
    `.labelEn`, `.amountAgorot`.
  - **submit:** as the hours (missing → send; `samePrices` against `filledFrom` → nothing). A 422 with
    a key ending `.shiftId` invalidates the space (S3), then rethrows.
  - **Returns:** `frame`; `intro: string`; `notes: string[]` (D6: `prices.noShifts` when the space has
    no saved shift, `prices.hoursUnsaved` when `hoursUnsaved`); `columns: { period; audience; shift;
    label; labelEn; amount; optional }`; `rows: { key; label /* prices.row({ position }) */; period:
    SelectField; audience: SelectField; shift: SelectField; labelAr: TextField; labelEn: TextField;
    amount: TextField; remove: { label; disabled; run } }[]`; `add: { label; disabled; reason; run }`.
    `SelectField = { label; value: string; options: { value: string; label: string; lang?: 'ar' | 'en'
    }[]; disabled: boolean; choose: (value: string) => void; error?: string; ref: RefCallBack }` — `ref`
    is `form.form.register(path).ref`, set on the `SelectTrigger`, so a refusal focuses it; `choose`
    is `setValue(path, value, { shouldDirty: true })`, and once the form was submitted it re-checks the
    row (`trigger` on the row's `period`, `shiftId` and `labelAr`), as the contacts re-check a type.
    The shift field's options: «بدون وردية» (`''`) then each saved shift (Arabic name; in English
    `nameEn ?? nameAr`, `lang: 'ar'` on the fallback); `disabled` while there are no saved shifts or
    pending. Remove is disabled while pending; add at `MAX_PRICES` (reason `prices.limit`) or pending.
- **New** `features/spaces/hooks/prices/useReadOnlyPrices.ts` — `{ title, none: string | null /*
  prices.none when there are none */, prices: { key; label: string; value: string }[] }`; `label`
  `prices.summary({ period, audience })`, then `prices.withPart({ line, part })` for a shift's name and
  for the label (in the interface's language, Arabic when the English is missing); `value`
  `priceText(amountAgorot, language)`.
- **New** `features/spaces/components/prices/PricesSection.tsx`, `ReadOnlyPrices.tsx` (§8).
- `hooks/editor/useSpaceEditor.ts` — `SECTIONS = FACT_GROUPS` (P10); the checklist's `href` is always
  `#<group>`; it returns `hoursUnsaved: dirty.includes('hours')` in the ready state. Its test
  `hooks/editor/useSpaceEditor.component.test.tsx` gains one case (§10).
- `components/editor/SpaceEditor.tsx` — renders `PricesSection` (with `hoursUnsaved`) after
  `HoursSection`, `ReadOnlyPrices` after `ReadOnlyHours`; its test extended (§10).
- Copy: `editor.prices` (§11).
- Docs: `docs/features/spaces.md` («الأسعار» bullet, verified bullet, *Web decisions*, *Code map*,
  *What it does*, the "not built" sentence, *Web history*), `docs/project/overview.md` (*Built*, §12).

**Nothing else.** In particular: no change to `useSectionFrame`, `useSaveGroup`, `useLeaveGuard`,
`MissingChecklist`, `SectionNav`, the three existing sections, `apps/api`, `packages/shared`,
`docs/design/`, `package.json`.

## 8. The design of each section (components and states)

Frames to match: `C:\Users\basel\Downloads\a-edit-space-screens\01_EDIT_UNVERIFIED_{1SM,2MD,3LG}.png`
(both sections saved), `03_EDIT_AFTER_CREATE_{1SM,2MD,3LG}.png` (both missing),
`04_EDIT_VERIFIED_READONLY_*.png` (read-only), `02_EDIT_MISSING_CHECKLIST_*.png` (the checklist). Where
this plan and a frame differ, **this plan wins** (the frames predate D2–D7 and O6).

Only design-system components (`@shared/design-system`) and semantic tokens; no colour or arbitrary
value (`npm run check:classes`); logical classes only (`ms-`, `pe-`, `text-start`, never `ml-`/`left`).

### «ساعات العمل» (`HoursSection`)
- **Frame:** `SectionCard` with `action` = `Button variant="outline" size="sm"` «نسخ إلى كل الأيام»
  (`disabled` per D3). The header holds it at **every** width (design issue F).
- **Content, top to bottom:**
  1. `p.text-caption.text-muted-foreground`: `hint` (copy line or «افتح يومًا واحدًا على الأقل.»).
  2. The days: `ul` with `divide-y divide-border rounded-lg border`; each `li`
     `flex flex-col gap-3 p-3 md:flex-row md:items-end md:gap-6`:
     - a row `flex items-center justify-between gap-3 md:w-44 md:self-center`: the day name
       (`text-label`), then `span.flex.items-center.gap-2`: the state word (`text-caption
       text-muted-foreground`, `aria-hidden`) and `Switch` (`aria-label` = «مفتوحة يوم {day}»,
       `checked`, `onCheckedChange`, `disabled`);
     - when open: `div.grid.grid-cols-2.gap-3` with two `Field`s «من» and «إلى», each an `Input`
       (P3; `className="md:w-28"`), «إلى»'s `error` shown under it. Side by side at every width (D2).
  3. `Separator`.
  4. The shifts: `h3.text-title-sm` «الورديات», `p.text-caption.text-muted-foreground` the hint; a `ul`
     `flex flex-col gap-4`; each `li` `role="group"` `aria-label` «الوردية {n}», `rounded-lg border p-4`
     `flex flex-col gap-4`:
     - `div.grid.gap-4.md:grid-cols-2`: `Field` «الاسم بالعربية» (`Input dir="rtl"`), `Field`
       «الاسم بالإنجليزية» with `labelEnd={<OptionalMark label="اختياري" />}` (`Input dir="ltr"`);
     - `div.grid.gap-4.md:grid-cols-2` (stacked below `md`, D2): `Field` «من», `Field` «إلى» (its
       `error` and `helper` per §7);
     - `div.flex.flex-wrap.items-center.gap-2`: `Button variant="ghost" size="sm"` with `XIcon` and the
       visible text «حذف الوردية» (`aria-label` «حذف الوردية {n}»), then, when disabled for a price,
       `span.text-caption.text-muted-foreground` «يستعملها سعر — احذف السعر أولًا».
  5. `div.flex.flex-wrap.items-center.gap-3`: `Button variant="outline"` «إضافة وردية» and, at ten, its
     reason (`text-caption text-muted-foreground`), as `ContactsSection` does.
- Use the exact Tailwind text-style names the existing sections use; if `text-title-sm` does not exist,
  use the class `AmenitiesSection` uses for «مرافق إضافية»'s heading (check it, do not invent one).

### «الأسعار» (`PricesSection`)
- **Frame:** `SectionCard`, no header action.
- **Content:**
  1. `p.text-caption.text-muted-foreground`: `intro`.
  2. Each of `notes`: `p.text-caption.text-muted-foreground`, once, above the rows (D6).
  3. When there are rows: from `md`, a header row `div` `hidden md:grid md:grid-cols-12 md:gap-3`
     `aria-hidden="true"`, `text-label text-muted-foreground`: «الفترة» (`col-span-2`), «لمن» (2),
     «الوردية» (2), «وصف مخصّص» with «اختياري» under it (3), «المبلغ (₪)» (2), an empty cell (1).
  4. `ul.flex.flex-col.gap-4.md:gap-2`; each `li` `role="group"` `aria-label` «السعر {n}», classes
     `grid gap-3 rounded-lg border p-4 md:grid-cols-12 md:items-start md:gap-3 md:rounded-none
     md:border-0 md:p-0`. Each control is in a `Field` whose `label` is
     `<span className="md:sr-only">{label}</span>` (seen on a phone card, read by a screen reader at
     every width, the header saying it once from `md`):
     - `Field` «الفترة» `md:col-span-2`: `Select` (`SelectTrigger ref`), options ساعة/يوم/أسبوع/شهر;
     - `Field` «لمن» `md:col-span-2`: `Select`, الجميع/الطلاب;
     - `Field` «الوردية» `md:col-span-2`: `Select`, «بدون وردية» + saved shifts, `disabled` per D6;
     - `div.flex.flex-col.gap-2.md:col-span-3`: `Field` «وصف مخصّص» (`labelEnd` «اختياري» shown below
       `md` only: `<OptionalMark>` inside `span.md:hidden`), `Input dir="rtl"`; `Field` «الوصف
       بالإنجليزية» (same optional mark), `Input dir="ltr"` with `placeholder` «بالإنجليزية (اختياري)»;
     - `Field` «المبلغ (₪)» `md:col-span-2`: `Input` (P4);
     - `div.flex.justify-end.md:col-span-1`: `Button variant="ghost" size="icon"` `XIcon`,
       `aria-label` «حذف السعر {n}».
  5. «إضافة سعر» `Button variant="outline"` and, at forty, «الحد 40 سعرًا» beside it.
- On a phone, a card's fields stack in one column (`grid` with no columns).

### The states (both sections)
| State | What shows | Owned by |
|---|---|---|
| Loading / failure / 404 | the editor's `EditorLoading`, `EditorFailure` (Try again), `NotFoundState` | `SpaceEditor` (unchanged) |
| Missing | date line «لم تُضف بعد», Save only; hours show the template, prices no rows | `useSectionFrame` |
| Saved, unchanged | «آخر تحديث قبل …», «قديمة» `Badge warning` when stale, «المعلومات ما زالت صحيحة» | `useSectionFrame` |
| Dirty | «تغييرات غير محفوظة» `Badge warning` in the header; «تجاهل التغييرات» | `useSectionFrame` |
| Pending | Save `loading`; every field, switch, select, add and remove disabled | the hooks |
| Saved | toast «حُفظ قسم «ساعات العمل»» / «حُفظ قسم «الأسعار»»; the answer's date | `useSaveGroup` |
| Nothing changed | the `p role="status"` line under the fields | `useSectionFrame` |
| Refused on a field | `Field` `error` text; the first refused field focused | `useServerForm` |
| 409 (hours) | `FormFailure` with S1's line; the space fetched again | hours hook |
| 422 on a shift id | `FormFailure` with S2's line | hours hook |
| 403 / 404 | `FormFailure` line; the space fetched again → read-only / the 404 | `useSaveGroup` + frame |
| 429 | `FormFailure` countdown; Save and the confirmation disabled | `useServerForm` + frame |
| Read-only (verified) | `ReadOnlyHours`, `ReadOnlyPrices`, no section list below `lg` | `SpaceEditor` |

### Read-only
- `ReadOnlyHours`: `ReadOnlyCard id="hours"`; when `none`, `p.text-body-sm.text-muted-foreground`;
  else a `dl.flex.flex-col.divide-y.divide-border` of `ReadOnlyItem` per day (label the day; value
  `span dir="ltr"` for a range, plain for «مغلقة»), then when there are shifts an `h3` «الورديات» and a
  `dl` of `ReadOnlyItem` (label the shift's name with its `lang`, value `span dir="ltr"`).
- `ReadOnlyPrices`: `ReadOnlyCard id="prices"`; `none` as above; else a `dl` of `ReadOnlyItem` (label the
  summary, value `span dir="ltr"` the amount). Copy `ReadOnlyContacts.tsx`.

## 9. Design issues (approved with the plan)

- **A — A shift's error cannot name one day** (D4 vs the rule "at least one open day"): the error says
  «خارج ساعات كل يوم مفتوح»; a helper names the open days a fitting shift skips. *Owner's answer.*
- **B — «نسخ إلى كل الأيام» copies to open days only, and is disabled with its reason while none is
  open** (the prototype hides it). *Owner's answer.*
- **C — D6's two lines are said once, above the price rows,** not under up to 40 fields. *Owner's answer.*
- **D — A day's «من»/«إلى» stay side by side on a phone** (7 rows stay short); a shift's stack (AD-007).
  *Owner's answer.*
- **E — The custom label's English field is always shown** (the prototype shows it only once the
  Arabic has text, DI-12). *Why:* a hidden field keeps its value, and a refusal on it («الوصف بالعربية
  أولًا») would point at a field the admin cannot see.
- **F — «نسخ إلى كل الأيام» stays in the header at every width** (the prototype moves it into the
  content on a phone). *Why:* one control in one place; two copies hidden by CSS would both exist for
  a screen reader and for the tests.
- **G — The prices' «للعرض فقط · الدفع في المساحة» moves from the date line to the intro line** under
  the header. *Why:* every section's date line holds the date alone (#74).
- **H — A verified space reads a closed day as «مغلقة»** (the editor's word; the prototype's verified
  page says «مغلق»), and shows **every** price with its shift and label (the prototype shows one per
  period). *Why:* one word for one state; a price with a shift or label would otherwise vanish.

## 10. Tests — each with its lane, title and the break that must make it fail

Rules (testing §3): every new test is **seen failing first** in its own lane — written before the code,
or, where the code exists, by breaking the code once (copy the file aside first, make the break, run,
copy back, run green; **never** `git checkout <file>`, which wipes uncommitted work). Expectations are
written by hand. No `vi.mock`: the network is faked with `src/test/fakeTransport.ts` (`fakeTransport`,
`ok`, `refused`, `bodyOf`, `restoreTransport`). Each hook test file builds its own space constant, as
`useContactsSection.component.test.tsx` does (copy its `renderSection`, `save`, `writes()` helpers;
`startPreferences('en')` in `beforeEach`).

Run one file: `npm run test:unit -w @masaha/web -- <path>` or `npm run test:component -w @masaha/web -- <path>`.

### Unit
`features/spaces/services/clockTime.unit.test.ts`
1. "writes a minute of the day as a 24-hour time, the day's end as 24:00" — break: `clockOf(1440)`
   returns `"00:00"`.
2. "reads a time typed with or without its colon, in Western or Arabic digits" — break: drop the
   Arabic-Indic digit mapping.
3. "reads 24:00 only as a day's end" — break: accept 24:00 when `end` is false.
4. "leaves what is no time as typed, and a blank as no value" — break: return `0` for a blank.

`features/spaces/services/hoursForm.unit.test.ts`
5. "fills a space with no hours from the template: Saturday to Thursday 08:00–18:00, Friday closed" —
   break: leave Friday open.
6. "builds the contract's week, Sunday first, a closed day as null" — break: index `days` in shown order.
7. "sends a saved shift with its id, a new one without, a blank English name as none" — break: send
   `id: null` for a new shift.
8. "tells the hours as filled from apart from changed ones, the shifts' order counting" — break: compare
   the shifts sorted.
9. "names the open days a shift does not fit, none when it fits no open day" — break: return the closed
   days too.

`features/spaces/services/pricesForm.unit.test.ts`
10. "reads an amount in shekels as whole agorot, Arabic digits and separators included" — break: drop the
    `× 100`.
11. "leaves an amount with more than two decimals as no whole number of agorot" — break: round it.
12. "writes agorot as shekels, with no decimals for a whole amount" — break: always two decimals.
13. "builds the contract's prices, no shift and a blank label as none" — break: send `shiftId: ''`.
14. "tells the prices as filled from apart from changed ones, their order counting" — break: compare
    sorted.

`features/spaces/services/priceText.unit.test.ts`
15. "writes an amount in shekels with Western digits in both languages" — break: use the locale `ar`.
    (Assert English exactly — `"₪15"`, `"₪12.50"`; for Arabic assert the digits `15` and `12.50` and `₪`
    appear and no Arabic-Indic digit does: the exact Arabic string depends on the engine's ICU.)

`features/spaces/repository/spacesRepository.unit.test.ts`
16. "PUTs the hours with the shifts whole" — break: the path `/hour`.
17. "PUTs the prices whole" — break: send `{ prices }` as `prices` only.
18. The existing "POSTs the %s group's confirmation, with no body" gains `'hours'` and `'prices'` —
    break: the confirm path written `/confirm/${group}` once, so the new rows fail.

### Component — hooks (`renderHook`)
`features/spaces/hooks/hours/useHoursSection.component.test.tsx`
19. "fills a space with no hours from the template, Saturday first" — break: show Sunday first.
20. "saves hours never saved, the template as it is, which dates them" — break: treat a missing group
    as unchanged.
21. "sends the week Sunday first and the shifts with their ids, a day to 24:00 as 1440" — break: drop the
    shift's id in `hoursInput`.
22. "writes a time it can read as HH:MM once its field is left" — break: remove the blur rewrite.
23. "copies the first open day's hours to every open day, leaving closed days closed" — break: copy to
    every day.
24. "holds the copy while no day is open, saying why" — break: never disable it.
25. "refuses a shift outside every open day on the shift, sending nothing" — break: drop the item-level
    field `shifts.<i>` from `FIELDS`.
26. "names the open days a shift does not apply on" — break: never set the helper.
27. "refuses a day that closes before it opens, and a time it cannot read, on their fields" — break:
    `fieldLines` for `closesMinute` removed (the generic line shows instead).
28. "holds a shift's Remove while a saved price uses it, saying why" — break: read the prices from
    nothing (`[]`).
29. "says a removed shift is still in use when the server refuses it, and fetches the space again" (409)
    — break: drop the invalidation.
30. "says the shifts changed meanwhile when the server refuses a shift's id, and fetches the space
    again" (422 on `shifts.0.id`) — break: drop the invalidation.
31. "sends nothing for saved hours as they are, and says how to renew their date" — break: never set
    `unchanged` (always send).
32. "stops adding shifts at ten, saying why" — break: `MAX_SHIFTS + 1`.
33. "keeps its unsaved changes when the space arrives again with its hours changed elsewhere" — break:
    reset on every new space.
34. "confirms its own group, and names it" — break: confirm `'profile'`.
35. "holds each Remove, switch and Add while a save is pending" — break: drop `form.isPending` from
    remove's `disabled`.

`features/spaces/hooks/prices/usePricesSection.component.test.tsx`
36. "sends the prices in their order, an amount in shekels as agorot, no shift and a blank label as none"
    — break: send the amount as typed.
37. "saves prices never saved even empty, which dates them" — break: treat a missing group as unchanged.
38. "sends nothing for saved prices as they are, and says how to renew their date" — break: never
    `unchanged`.
39. "offers the space's saved shifts only, and holds the field while there are none, saying why" —
    break: offer a fixed list / never disable.
40. "says to save the opening hours while they have unsaved changes" — break: ignore `hoursUnsaved`.
41. `it.each` "refuses a repeated price on its %s, sending nothing" (`period`, `shiftId`, `labelAr`) —
    break: drop `.shiftId` from `FIELDS`.
42. "refuses an amount empty, zero or not an amount, on its field" — break: drop the amount's
    `fieldLines`.
43. "refuses an English label without its Arabic one, on the Arabic" — break: drop `labelAr`'s
    `required` line.
44. "puts a shift removed meanwhile on its field, and fetches the space again" — break: drop the
    invalidation.
45. "stops adding prices at forty, saying why" — break: `MAX_PRICES + 1`.
46. "keeps its unsaved changes when the space arrives again with its prices changed elsewhere" — break:
    reset on every new space.
47. "confirms its own group, and names it" — break: confirm `'hours'`.
48. "holds each Remove and Add while a save is pending" — break: drop `form.isPending` from remove.

`features/spaces/hooks/editor/useSpaceEditor.component.test.tsx`
49. "says whether the hours have unsaved changes, for the prices" — break: return `false`.

`features/lookups/hooks/area/useAreaOptions.component.test.tsx`
50. "keeps a space's own area the catalogue no longer offers, marked hidden" — break: never set `kept`.
51. "reads no admin list while the catalogue offers the area" — break: `enabled: true` always (assert
    no `GET /admin/governorates`).

### Component — rendering
`features/lookups/components/area/AreaSelect.component.test.tsx`
52. "shows a space's own hidden area in its trigger, marked hidden" — break: do not render `kept`.

`features/spaces/components/editor/SpaceEditor.component.test.tsx` (update, then add)
- **Update** "heads a space with missing groups with the five, a drawn section's line a link to it" →
  title "heads a space with missing groups with the five, each line a link to its section"; it asserts
  the 'Opening hours' and 'Prices' links (`#hours`, `#prices`) instead of no link. Break: `href: null`
  for hours.
- **Update** "lists its sections in a navigation, the one in view marked": the five links, in order.
  Break: drop `'prices'` from `SECTIONS`.
- **Update** "a verified space": also 'Saturday' with `08:00–18:00` (`dir="ltr"`), 'Closed', a shift's
  name, and a price's summary with `₪15`. Break: leave `ReadOnlyPrices` out.
53. (new, describe "the opening hours section") "shows each day with its state and switch, its two
    times when open, and the copy in its header" — break: render the times of a closed day.
54. (new) "shows why a shift cannot be removed beside its Remove" — break: do not render `reason`.
55. (new, describe "the prices section") "names each price's controls by its row, and says once why no
    shift can be chosen" — break: render the note per row.
(No test for the leave guard naming «ساعات العمل»: `useSectionFrame` reports any group, and the
guard's naming is proven by "asks first while a section has unsaved changes, naming it".)

Not tested by a new test (proven elsewhere): the frame's states (`useSectionFrame`'s tests), the 429
(the frame's and the form's tests), the leave guard, the toast wording (`useSaveGroup`), catalogue
parity (the existing `catalogues.unit.test.ts` covers the new lines automatically).

## 11. The copy — every new line, with its key (English is the source shape)

`apps/web/src/shared/copy/english/spaces.ts` and `…/arabic/spaces.ts`, under `editor`. A function line
takes named parameters (localisation › Writing a line). `{…}` below is a parameter.

**`editor.hours`**
| Key | English | Arabic |
|---|---|---|
| `days.saturday` … `days.friday` | Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday | السبت، الأحد، الاثنين، الثلاثاء، الأربعاء، الخميس، الجمعة |
| `open` | Open | مفتوحة |
| `closed` | Closed | مغلقة |
| `openOn({ day })` | Open on {day} | مفتوحة يوم {day} |
| `from` | From | من |
| `to` | To | إلى |
| `timeExample` | 08:00 | 08:00 |
| `copyAll` | Copy to all days | نسخ إلى كل الأيام |
| `copyHint({ day })` | “Copy to all days” copies {day}’s hours to every open day. | «نسخ إلى كل الأيام» ينسخ ساعات {day} إلى كل يوم مفتوح. |
| `noOpenDay` | Open at least one day. | افتح يومًا واحدًا على الأقل. |
| `shifts` | Shifts | الورديات |
| `shiftsHint` | Optional. Each shift lies inside the hours of at least one open day. | اختيارية. تقع كل وردية داخل ساعات يوم مفتوح واحد على الأقل. |
| `shift({ position })` | Shift {position} | الوردية {position} |
| `nameAr` | Name in Arabic | الاسم بالعربية |
| `nameEn` | Name in English | الاسم بالإنجليزية |
| `addShift` | Add shift | إضافة وردية |
| `shiftLimit` | Up to 10 shifts | الحد 10 ورديات |
| `removeShift` | Remove shift | حذف الوردية |
| `removeShiftNamed({ position })` | Remove shift {position} | حذف الوردية {position} |
| `inUse` | A price uses it — remove that price first | يستعملها سعر — احذف السعر أولًا |
| `notOn({ days })` | Doesn’t apply on {days} | لا تنطبق يوم {days} |
| `range({ from, to })` | {from}–{to} | {from}–{to} |
| `none` | No opening hours yet | لا ساعات عمل بعد |
| `inUse409` | A shift you removed is still used by a price, a package or a subscription, so nothing was saved. Change what uses it first. | وردية حذفتها ما زالت مستعملة في سعر أو باقة أو اشتراك، فلم يُحفظ شيء. غيّر ما يستعملها أولًا. |
| `shiftsChanged` | This space’s shifts changed since the page was opened. Discard your changes to see them as saved. | تغيّرت ورديات هذه المساحة منذ فُتحت الصفحة. تجاهل تغييراتك لتراها كما حُفظت. |
| `fieldErrors.opens.required` | Enter a time | أدخل الوقت |
| `fieldErrors.opens.invalid_format` | A time from 00:00 to 23:59 | وقت من 00:00 إلى 23:59 |
| `fieldErrors.closes.required` | Enter a time | أدخل الوقت |
| `fieldErrors.closes.invalid_format` | A time up to 24:00, such as 18:30 | وقت حتى 24:00، مثل 18:30 |
| `fieldErrors.closes.out_of_range` | Must be after the start | يجب أن يكون بعد البداية |
| `fieldErrors.nameAr.too_short` | Enter the shift’s Arabic name | أدخل اسم الوردية بالعربية |
| `fieldErrors.nameAr.too_long` | 40 characters at most | 40 حرفًا على الأكثر |
| `fieldErrors.nameAr.not_unique` | A repeated shift name | اسم وردية مكرّر |
| `fieldErrors.nameEn.too_long` | 40 characters at most | 40 حرفًا على الأكثر |
| `fieldErrors.outside` | Outside the hours of every open day | خارج ساعات كل يوم مفتوح |
| `fieldErrors.noneOpen` | No day is open yet | لا يوم مفتوح بعد |

Field lines map: `days.<i>.opensMinute` → `fieldErrors.opens`; `days.<i>.closesMinute` and
`shifts.<i>.endsMinute` → `fieldErrors.closes`; `shifts.<i>.startsMinute` → `fieldErrors.opens`;
`shifts.<i>.nameAr` → `fieldErrors.nameAr`; `shifts.<i>.nameEn` → `fieldErrors.nameEn`. The shift's
English name's optional mark reuses `copy.spaces.add.optional` («اختياري» / "Optional").

**`editor.prices`**
| Key | English | Arabic |
|---|---|---|
| `intro` | For display only: payment is at the space. Leave out the periods it doesn’t offer. | للعرض فقط، والدفع في المساحة. اترك الفترة غير المتوفرة بلا سعر. |
| `noShifts` | No saved shifts — add shifts first. | لا ورديات محفوظة — أضف ورديات أولًا. |
| `hoursUnsaved` | Save the opening hours for a new shift to show here. | احفظ ساعات العمل لتظهر الوردية الجديدة هنا. |
| `period` | Period | الفترة |
| `audience` | For | لمن |
| `shift` | Shift | الوردية |
| `label` | Custom label | وصف مخصّص |
| `labelEn` | Label in English | الوصف بالإنجليزية |
| `labelEnPlaceholder` | In English (optional) | بالإنجليزية (اختياري) |
| `amount` | Amount (₪) | المبلغ (₪) |
| `periods.HOUR` / `DAY` / `WEEK` / `MONTH` | Hour / Day / Week / Month | ساعة / يوم / أسبوع / شهر |
| `audiences.GENERAL` / `STUDENT` | Everyone / Students | الجميع / الطلاب |
| `noShift` | No shift | بدون وردية |
| `row({ position })` | Price {position} | السعر {position} |
| `add` | Add price | إضافة سعر |
| `limit` | Up to 40 prices | الحد 40 سعرًا |
| `remove({ position })` | Remove price {position} | حذف السعر {position} |
| `summary({ period, audience })` | {period} · {audience} | {period} · {audience} |
| `withPart({ line, part })` | {line} · {part} | {line} · {part} |
| `none` | No prices yet | لا أسعار بعد |
| `fieldErrors.amount.required` | Enter the amount | أدخل المبلغ |
| `fieldErrors.amount.invalid_format` | An amount in shekels, such as 15 or 12.50 | مبلغ بالشيكل، مثل 15 أو 12.50 |
| `fieldErrors.amount.out_of_range` | Above zero, up to ₪100,000 | أكبر من صفر، حتى 100,000 ₪ |
| `fieldErrors.repeated` | A repeated price: change this field | سعر مكرّر: غيّر هذا الحقل |
| `fieldErrors.labelAr.required` | The Arabic label first | الوصف بالعربية أولًا |
| `fieldErrors.label.too_long` | 60 characters at most | 60 حرفًا على الأكثر |
| `fieldErrors.shiftGone` | This shift is no longer the space’s | لم تعد هذه الوردية من ورديات المساحة |

Field lines map per row: `period` → `{ not_unique: repeated }`; `shiftId` → `{ not_unique: repeated,
invalid_choice: shiftGone }`; `labelAr` → `{ not_unique: repeated, required: labelAr.required,
too_long: label.too_long }`; `labelEn` → `{ too_long: label.too_long }`; `amountAgorot` →
`fieldErrors.amount`. Day names in `copyHint` and `notOn` need no isolate (catalogue words in the
sentence's language). In `withPart`, the `part` (a shift's name or a price's label, typed by the admin)
is always passed through `isolated()` from `@shared/forms`, as the contacts insert their values.

**`lookups.areaSelect.hidden({ name })`**: "{name} (hidden)" / «{name} (مخفية)».

**New Arabic lines need the owner's approval:** list every Arabic line above in the PR description's
"New Arabic lines" section (as #74 did).

## 11b. Documents (the exact edits)

Decision and history lines cite the PR as `#PRNUM` while committing; replace it just before the push
(§14.7). No D-labels on this item's decisions (#74's review). Present tense, only what is built.

- `docs/features/spaces.md`
  - *Authority*/*What it does*: the web bullet reads "…edits a space on a page of its own, its profile,
    its hours with the shifts, its prices, its amenities and its contacts each saved, dated and
    confirmed as a section…"; the sentence "The owner's side is not built, and the photos are the API's
    only; on the web, neither are the hours with the shifts, nor the prices." becomes "The owner's side
    is not built, and the photos are the API's only."
  - *The space editor on the web*: a bullet «ساعات العمل» (the week Saturday first, «مفتوحة»/«مغلقة»,
    «من»/«إلى», 24:00, the copy to the open days, the shifts with their ids, the error and the helper,
    a shift in use not removable, the 409 and the shift id refused); a bullet «الأسعار» (the columns,
    the table and the cards, the amount in shekels, the saved shifts only, the two lines, the repeat,
    the limit, the shift gone); the checklist bullet: every line a link; the verified bullet: its hours
    and prices.
  - *Web decisions*: P1, P2, P3, P4, D3 (open days), D4 (error and helper), D6 (saved shifts, lines
    once), D7 (in use, from the saved prices), S1–S3, design issues E and G, each "*Why:* …
    2026-10-13, #PRNUM." Mark #74's «The checklist lists the five groups; a line leads to its section
    only once the editor draws it» as `*Superseded 2026-10-13 by #PRNUM's «Every checklist line leads
    to its section», below.*` and add that line.
  - *Code map* › Web: `hours/` and `prices/` in `hooks/` and `components/`; in `services/` "the hours
    and the prices as their forms hold them, a time of day, an amount in shekels".
  - *Open findings*: remove 60 (commit 1).
  - *Web history*: "- #PRNUM — the editor's «ساعات العمل» with the shifts and «الأسعار», each saved,
    dated and confirmed, and read-only on a verified space; finding 60 resolved."
- `docs/features/lookups.md`: the area field keeps a space's own area hidden since, marked hidden, read
  from the admin's lists only then (behaviour + web decision + web history), linking finding 60.
- `docs/architecture/findings/60-…md`: `**Status:** Resolved · **Date:** 2026-10-13`, then
  `**Resolution:** the area field keeps a space's own area the catalogue no longer offers, named from the
  admin's lists and marked hidden, and offers it to no other space (#PRNUM).`
- `docs/architecture/findings/README.md`: 60 moves to *Resolved*.
- `docs/project/overview.md` › *Built* › Spaces: "edit its profile, its amenities and its contacts on
  its own page" → "edit its profile, its hours with the shifts, its prices, its amenities and its
  contacts on its own page".

## 12. Review Focus (inputs no planned test exercises)

- The `md:sr-only` labels and the header row's alignment at 768 (CSS; checked in the real run only).
- A time typed as `24:00` in «من» (refused `invalid_format`) and `23:60` (refused).
- A shift whose times cannot be read while other shifts are fine: the helper must not show.
- The kept hidden area's label while the admin's list is still loading (empty for a moment).
- The focus target of the item-level `shifts.<i>` error: no field is registered under it, so nothing is
  focused for it; the error shows on «إلى».
- `useServerForm.errors['shifts.<i>']` holds a generic line whenever a child field of that shift has
  an error (`get` returns the nested object): the hook must read the item-level error from
  `codes['shifts.<i>']` only, never from `errors`.
- A price row whose saved shift's English name is missing, in English.
- An amount `٫٥` (Arabic separator, no integer part) → `0.50`.
- Copy-to-all while the first open day's times cannot be read: the texts are copied as typed.

## 13. Commits

| # | Subject (≤ 50) | Chars | Holds |
|---|---|---|---|
| 1 | `fix(lookups): show a space's own hidden area` | 44 | §7 commit 1; tests 50–52 |
| 2 | `feat(spaces): the editor's opening hours` | 40 | §7 commit 2; tests 1–9, 16, 18 (hours), 19–35, 53–54, editor test updates for hours |
| 3 | `feat(spaces): the editor's prices` | 33 | §7 commit 3; tests 10–15, 17, 18 (prices), 36–49, 55, editor test updates for prices; overview |

Each body explains why (2–4 lines). No `Co-Authored-By`, no "generated with" line. Stage by path
(`git add <path> …`), never `git add -A` / `git add .`; `git status` before each commit. After each
commit: `npm run lint` and `npm run typecheck`, both clean (fix and amend that commit if not).

## 14. The executor's procedure

1. **Start.** `cd C:\Users\basel\masaha`; `git status` must be clean, on `main`. Then
   `git fetch --prune origin` and `git switch -c feat/space-hours-prices origin/main`.
   `npm ci` if `package-lock.json` changed since the last install (it did with #77: run it).
2. **Read** what §3 names for the executor.
3. **Build in commit order** (§13). Within each commit: services and their unit tests first (seen
   failing, then green), the repository, the hooks with their tests, the components, the editor wiring,
   the copy (English then Arabic), the editor's component test, the documents. Run each new test file
   alone as you go (§10's command).
4. **Commit** each unit (§13), checks after each.
5. **Local verification, once, on the head, one lane at a time** (workflow phase 4):
   - First check no other folder runs a lane (the machine runs one at a time):
     PowerShell `Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine
     -match 'vitest' } | Select-Object ProcessId, CommandLine`. If a command line names `masaha-b` or
     `masaha-media` (or any other folder), wait and check again; never run beside it.
   - `npm run test:unit`; `npm run test:component` (record each count).
   - `NODE_ENV=production npm run build` (Git Bash; the folder's `apps/web/.env` sets
     `NODE_ENV=development`, which would ship the showcase), then `npm run check:build`.
   - `npm run lint`, `npm run typecheck`, `npm run check:classes`, `npm run format:check`,
     `npm run check:links`.
   - **Not run:** `npm run test:api` — no API change (say so in Evidence).
   - A failure: find the root cause before changing code; after three failed fixes, stop (§16).
6. **The real run** (web on 5320, API on 3320, both from this folder):
   - `npm run db:up` only if the container is down (`docker ps` shows `masaha-postgres-1`); start the
     API `npm run dev -w @masaha/api` and the web `npm run dev`, each in the background; note their PIDs.
   - Browse `http://localhost:5320` (not `[::1]`: CORS). Sign in as the seeded admin (`SEED_ADMIN_EMAIL`
     / `SEED_ADMIN_PASSWORD` in `apps/api/.env`). Keep reloads few (the refresh is limited to 30 per
     15 minutes).
   - Steps: add a space (Spaces › Add space) → its editor opens with «ما زال ناقصًا» and both new
     sections «لم تُضف بعد»; in «ساعات العمل» set Saturday 09:00–24:00, close Wednesday, use «نسخ إلى
     كل الأيام», add a shift 20:00–23:30 (fits Saturday only: the helper names the others), add one
     06:00–07:00 (refused «خارج ساعات كل يوم مفتوح»), fix it, save; confirm. In «الأسعار» add a day
     price, a month price for students, a price for the shift; add a repeat (refused on its field);
     add rows to 40 (the reason shows); remove extras; save; confirm. Back in «ساعات العمل», the shift a
     price uses cannot be removed (reason beside it). With an unsaved change in hours, the prices show
     the save-the-hours line. The checklist empties once all five are saved (the profile is saved at
     creation; save «المرافق» and «التواصل» empty). Leave with unsaved hours: the dialog names
     «ساعات العمل». Finding 60: hide the space's area in Lookups, reopen its editor: the area field
     shows «… (مخفية)». A verified space: the seed's demo space `masaha-demo` exists only when
     `SEED_DEMO=true` was seeded; if it is there, open it from the list: hours and prices read-only.
     If it is not, say so in the report (do not seed demo data into `masaha_dev` without asking).
   - **Screenshots** to `C:\Users\basel\Downloads\s2b4b-shots\` (create it; never commit): with any
     browser automation the executor has, or Chrome's device toolbar by hand (Chrome headless over its
     DevTools protocol with Node 24's built-in `WebSocket` needs no dependency). A curated set, numbered
     `01-…`, `02-…` (not the whole grid): hours and prices saved at 1440 ar light, 1440 en dark, 768 ar
     light, 768 en dark, 390 ar light, 390 en dark; the missing state at 1440 ar;
     the shift error and helper; a shift in use; a repeated price; the limit; the 409 if reproducible;
     the area «(مخفية)»; the verified read-only at 1440 and 390. In RTL, capture the viewport only
     (full-page capture shifts RTL pages sideways in headless Chrome).
   - **Stop the servers** by PID — on Windows, stopping `npm run dev -w @masaha/api` leaves `tsx watch`,
     the server and `pino-pretty` running: list `node.exe` processes whose command line names
     `C:\Users\basel\masaha` and stop them by PID — then check the ports are free: PowerShell
     `Get-NetTCPConnection -LocalPort 3320,5320 -State Listen` returns nothing.
7. **The PR number in the documents.** Just before the push: `gh api
   "repos/{owner}/{repo}/issues?state=all&per_page=1&sort=created&direction=desc" --jq '.[0].number'`
   gives the latest number n (78 on 2026-10-13); the PR will be n+1. Replace `#PRNUM` in **every
   commit's own tree**: `git filter-branch -f --tree-filter "grep -rl '#PRNUM' docs | xargs -r sed -i
   's/#PRNUM/#<n+1>/g'" origin/main..HEAD`, then `git update-ref -d refs/original/refs/heads/feat/space-hours-prices`.
   `git grep '#PRNUM'` must find nothing. Push and create the PR at once; confirm it got n+1 (if not,
   repeat with the right number and `git push --force-with-lease`).
8. **Push and open the PR:**
   `git push -u origin feat/space-hours-prices`, then
   `gh pr create --assignee @me --label feat --label area:web --label area:docs --title "feat(spaces):
   the editor's hours and prices" --body-file <file>` with the description of §15 (Evidence, counts and
   screenshots filled in). No tool attribution anywhere.
9. **CI and CLEAN.** `gh pr checks <n> --watch --interval 30` (bounded: give up after 30 minutes and
   report); then `gh pr view <n> --json headRefOid,mergeStateStatus` — the head must be the branch's
   (`git rev-parse HEAD`) and the state `CLEAN`. If GitHub shows a conflict (`DIRTY`): `git fetch origin`,
   `git rebase origin/main`, keep both sides; a conflict only in documents is resolved, `npm run
   format:check` alone, and pushed with `git push --force-with-lease` (CI runs the lanes); a conflict in
   code adds `npm run lint` and `npm run typecheck`. Never rebase when GitHub shows no conflict.
10. **The early conflict check.** For each other open PR (`gh pr list --state open`): `git fetch origin
    pull/<m>/head:pr-<m>`, then `git merge-tree --write-tree HEAD pr-<m>`; note "clean" or the files in
    conflict.
11. **The report** to `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\S2B4B_REPORT.md`, in this order:
    (1) the PR and its head SHA; (2) the commits; (3) what was run, with counts per lane, and what was
    not, with why; (4) the breaks made and the tests seen failing first; (5) the problems met and how
    each was solved; (6) **anything that behaved unexpectedly, even unsolved**; (7) the early conflict
    check, per open PR; (8) each departure from this plan or the prompt, with its reason — and the note
    that the prototype still says «المدة»/«الفئة» (D5). Summarise it in the conversation.
12. **Stop.** Never merge, never delete a branch, never create an Issue.
13. **Review fixes** (they come back to the executor): verify each item against the code (push back with
    reasons when one is wrong); fold each fix into the commit it corrects — `git commit --fixup=<sha>`
    then `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main` (non-interactive) — no fix
    commits; lint and typecheck each commit; repeat step 5; `git push --force-with-lease`; step 9;
    update the PR description to the final state; post ONE comment "Review fixes" listing each fix and
    what changed (no replies in threads); add a section to the report for that round.

**No error code is added** by this item. (Were one ever needed: follow `docs/backend/conventions.md` §4
*Adding a domain error code* in its order — its third step adds the code's line to api-contract §6 —
and list each new code with its English and Arabic text in the PR description, the Arabic marked for
the owner's approval. Here it would be an API change, so: stop and ask.)

## 15. The PR description (fill in the bracketed parts)

```
## Summary
The admin's space editor gains its last two fact groups: «ساعات العمل» (the week with its shifts) and
«الأسعار» (the prices), each saved, dated and confirmed alone, in the navigation, the checklist, the
leave guard, and read-only on a verified space. Finding 60 is resolved: a space's own hidden area shows
in its area field, marked hidden.

## Scope
[§2 Scope]
## Acceptance criteria
[§2's list, each ticked and ending "— <test file › title>" or "— real run"]
## Out of scope
[§2 Out of scope]

## Change type
`feat` · web (`features/spaces`: `hooks/hours`, `hooks/prices`, `components/hours`, `components/prices`,
`services`, `repository`, `editor`; `features/lookups`: area field; `shared/copy`) · docs (`spaces.md`,
`lookups.md`, finding 60 and the index, `overview.md`)

## Evidence
Head `<sha>`. Lanes one at a time, after checking no other folder ran one: `test:unit` [n],
`test:component` [n]; `NODE_ENV=production npm run build` + `check:build`; `lint`, `typecheck` (also per
commit), `check:classes`, `format:check`, `check:links`.
**Not run:** `test:api` — no API change.
**Seen failing first:** every new test, in its own lane [list the breaks].
**Real run:** [ports, steps and what was seen]. Servers stopped by PID, ports free.

## Screenshots
Not committed; in `Downloads\s2b4b-shots\`: [numbered list].

## New Arabic lines, for the owner's approval
[every Arabic line of §11]

## Definition of Done
- [x] Acceptance criteria met, scope kept.
- [x] Lint and typecheck clean; build passes.
- [x] Tests added in the owning lanes and passing.
- [x] No hardcoded user-facing text; both catalogues updated.
- [x] UI checked in RTL and LTR, light and dark, phone and desktop.
- [x] Authorization enforced on the server (no new protected action; the server's 403 handled).
- [x] Documentation updated: `spaces.md`, `lookups.md`, finding 60 and the index, `overview.md`.
- [x] One home per fact; nothing claimed that is not built.
- [x] Every claim names its test or command.
- [x] Atomic history (3 commits), pushed, description complete.

An independent review follows.
```

## 16. Stop and ask (do not improvise)

Stop, write what you found in the report's §6, and ask the owner when:
- a change is needed in a file **not listed in §7** (any `apps/api` or `packages/shared` file, any
  design-system component, `useSectionFrame`, `useSaveGroup`, the three existing sections, a
  `package.json`);
- the API answers differently from the contract this plan relies on (the hours' and prices' bodies,
  `invalid_choice` on `shifts.<i>.id` or `prices.<i>.shiftId`, the 409 with no code) — record a finding
  (67) and stop;
- the shared schema refuses or accepts something this plan says otherwise (for example 24:00 in «من»);
- a decision this plan did not take (a new string, a different layout, a new state);
- a test cannot be made to fail by its break, or a lane fails for a cause not found after three fixes;
- a document conflict that is not a plain both-sides merge;
- another folder keeps a lane running for more than 30 minutes.

## 17. Decisions needed from the owner

None open: the four design questions were answered on 2026-10-13 (§4 D2, D3, D4, D6; §9 A–D).
Approving this plan approves design issues E–H and the stronger decisions S1–S4.

---

## Appendix — If the executor is Claude Code

Only a map; the steps above are complete without it.
- §14.1–14.2 (start, read): the `start-work-item` skill (its step 5 cuts the branch).
- §14.5–14.9 (verify, screenshots, push, PR, CI, CLEAN): the `open-pr` skill; §14.13 is its step 8.
- §14.10–14.11 (conflict check, report): the `final-report` skill.
- No `add-error-code` (no new code).
