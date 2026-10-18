# Review report — PR #49 (S2a-3: the admin's amenities tab)

**Head reviewed:** `eaf8f4d3f08eb0ba9b8bc4db6d9536e9e26e3b17`; base `a1f5aba`. Read only from git objects; neither repository was modified, no test or build was run.

## Verdict

**Sound in hooks, design system and accessibility; one deviation from the copied failure pattern, three small clean-ups. Approve once the failure finding is settled.**

## Findings

### 1. should-fix — one row's failure is hidden by a *failed* action on another row, and the alert never names its amenity

- **Where:** `apps/web/src/features/lookups/hooks/list/useAmenityFailure.ts:39-42` (per-target filter, then `.at(-1)` across all targets), rendered once for the whole list at `apps/web/src/features/lookups/components/list/AmenitiesSection.tsx:67`.
- **Scenario:** the admin retires amenity A → 404. She then toggles a switch on amenity B → 404. `targetOf` differs (`row 4` vs `row 5`), so both survive the per-target filter and `.at(-1)` returns B's: **A's failure disappears although nothing was done on A's row again** — the governorates scope the failure to the card (`useGovernorateCard.ts:58`), and the hook's own comment states it (`useAmenityFailure.ts:16`: "an action elsewhere leaves it standing"). The same substitution breaks the 429 hold: `blocked` comes from that same `refusal` and is passed to **every** row (`useAmenitiesSection.ts:57` → `AmenitiesSection.tsx:71`), so it is released as soon as another row fails otherwise. Amenities have no row card, so the standing failure is also **unattributed** — the alert never names its amenity.
- **Docs:** `docs/features/lookups.md:46` ("A row's failure shows in its card until the next action on that row or list") and its decision at `:66` (dated `#49`) do not describe the amenities' section-level alert or this substitution.
- **Fix:** in `useAmenityRow`, show a row-target failure scoped to that amenity (as `useGovernorateCard` does), keeping only `amenityOrder` failures at the section level; then say in `lookups.md` where an amenity's failure shows. The existing test only has another row's action *succeed* (`useAmenityRow.component.test.tsx:252`); add the case where it *fails*.

### 2. nit — a commit subject is 52 characters

- **Where:** `fix(design-system): dim controls while aria-disabled` (52; workflow §3 formats: ≤ 50, Conventional Commits).
- **Scenario:** the only subject over the limit (the others: 44/47/42/29).
- **Fix:** reword before merge, e.g. `fix(design-system): dim aria-disabled controls` (45).

### 3. nit — `SwitchControl.disabled` is written by both rows and read by nothing

- **Where:** `apps/web/src/features/lookups/types/RowControlsView.ts:6` (`type Control = { label, disabled, waiting }`, extended by `SwitchControl` at `:9`); set at `hooks/list/useRowViews.ts:32` and `hooks/list/useAmenityRow.ts:77` (`disabled: false`); `components/list/RowSwitch.tsx` reads only `label`, `text`, `checked`, `waiting` — `RowControls` reads `disabled` only for the two arrows.
- **Scenario:** a required property no code path consumes; the project bans such options.
- **Fix:** give `SwitchControl` only `label`, `text`, `checked`, `waiting`, `toggle` (or read it in `RowSwitch` and pass it to the `Switch`).

### 4. nit — every edit-path icon fixture is `wifi`, the *first* key, so "editing starts from the amenity's own icon" has no failing test

- **Where:** `hooks/edit/useEditAmenityForm.component.test.tsx:17` (`icon: 'wifi'`, asserted at `:38`) and `components/sheet/AmenitySheet.component.test.tsx:16` — `wifi` is `AMENITY_ICON_KEYS[0]`.
- **Scenario:** the code is right (`defaultValues.icon = amenity.icon` → `useController`; RHF's controller `ref` stores only `focus`/`select`, so it never reads a radio's value), but the edit assertions would still pass if the form resolved the icon to the first option. Proven already: the chosen value is the one sent on edit (`:93-96`, body `icon: 'coffee'`), an unknown key is rejected (`:117-120`), and the add path (error, zero POSTs).
- **Fix:** give the edit fixture a non-first icon (e.g. `sun` or `presentation`) so the initial value must come from the amenity.

## Verified OK

- **T1:** `GlyphIcon` exports a closed `GlyphName` over `iconSet.tsx`, knows nothing of amenities, renders through the layer's `Icon` (no mirroring — the test asserts it under RTL); `AmenityIcon({ icon: AmenityIconKey })` → `GlyphIcon name={icon}` is the compile-time key check; finding 10 marked *Resolved*, pointing at `lookups.md`.
- **Hooks:** amenity keys under `['admin','lookups','amenity', …]`, prefix-matched by TanStack, never the governorates' `…'row'`; add/edit carry no key, so they stay out of the row failure; query key `['admin','lookups','amenities']`; `onSuccess: () => refetch()` returns the awaited `invalidateQueries`, so writes stay pending until the list is refetched; `gcTime: 0` on all three row actions; each switch waits on its own mutation, arrows on any pending order but not a switch (the rule `useAmenityRow.ts:20-22` states), everything on `blocked`; 409 refetches and says the order changed; no optimistic update. Failure lifetime and `blocked`: see finding 1.
- **Icon field:** `useController` + `icon.value ?? ''` means a new amenity can be submitted with no icon (`createAmenitySchema` → `invalid_value` → `invalid_choice` → "Choose an icon"), editing starts from `defaultValues.icon`, the choice is validated against `AMENITY_ICON_KEYS`, and focus moves to the first radio on a client-side error (`shouldFocusError` default).
- **Tab:** `?tab=amenities`, unknown/missing → first, `replace: true`, first tab takes no parameter, inactive panel unmounted; asserted in `routes.component.test.tsx`.
- **Design system (D1):** `aria-disabled:opacity-50` added to `Button` and `Switch` beside the existing `disabled:` rules; `disabled` still blocks pointer events and cursor, focus rings and keyboard untouched; `Pagination` already used the utility; `RowControls`' local copies of it are gone.
- **Accessibility:** switches and Edit carry names containing their visible words (`heard(...)`), the radio group is named and described by its `Field` with the error tied to it, each option by its own `Field` label, arrow keys follow the direction (proven once, layer lane: `RadioGroup.component.test.tsx` RTL/LTR pair), sheet focus, two `axe` runs (section, sheet).
- **Tests:** no `vi.mock`, seams are `fakeTransport`/`fakeAdapter`; behaviour split by layer, as the governorates are; titles match assertions; ordering and 429 are the waiting-matrix assertions.
- **Documents:** `lookups.md` carries T1–T6, D1–D5, the T5 difference and *why* ("an order sends ids alone"), the tab and key-prefix decisions, the code map and `#49` in the history; `foundation.md` §3's `GlyphIcon` line (`:59`) and §12's Button/Switch `aria-disabled` rows (`:360`, `:370`); `overview.md` (date only); one home per fact.
- **Scope and commits:** five atomic commits, no tool attribution, nothing outside the item (the `fixtures.json` reword follows `checkBuild.ts`'s instruction — radix's `createContextScope('Tabs')` now reaches the bundle); no API change.

## Run by

Tool: **opencode** · model: **big-pickle** (`opencode/big-pickle`). No token or cost counter was reported by the tool.
