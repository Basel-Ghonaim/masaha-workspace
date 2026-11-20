# SPACE_PROFILE — Phase 1 report: PR-A (#140) and PR-B (#141)

> Executor: Claude Code (Opus 5.5), 2026-11-10. Plan: `2_PLAN_PROD.md` (approved 2026-11-10). Both PRs from
> `origin/main` at `7fb73c3c` (main did not move during the phase). **Never merged; no branch deleted.**

## 1. The pull requests and their heads

| PR | Branch | Head (full SHA) | CI | GitHub |
|---|---|---|---|---|
| **#140** `feat(spaces): contacts of any kind` | `feat/contact-types` | `29bcf80ae2b4441478abc7ecbf81f42fb500849c` | 10 pass, CodeRabbit skipped | `CLEAN` |
| **#141** `feat(design-system): add a sortable list` | `feat/sortable-list` | `4109534ca08cd31e7e693f5f6fdd96991dfaa4f9` | 10 pass, CodeRabbit skipped | `CLEAN` |

Both assigned to the owner. Labels: #140 `feat`, `area:api`, `area:web`, `area:docs`; #141 `feat`, `area:web`,
`area:design-system`, `area:docs`. `#PRNUM` replaced per commit tree (filter-branch) just before each push; none left.

## 2. The commits

- **#140** (37 files): `4622a003` `refactor(lib): share the contact and map links` (A1) · `29bcf80a`
  `feat(spaces): contacts of any kind` (A2: shared + the migration + API + the web's minimum + docs + tests).
- **#141** (14 files): `4109534c` `feat(design-system): add a sortable list` (B1: dependency, component, keyboard
  step, entry, lint, showcase, foundation).

## 3. What was run

Lint and typecheck on each commit (one at a time). Before each push, on the head, one lane at a time (5.3 GB free):

| Check | #140 | #141 |
|---|---|---|
| `lint`, `typecheck` | clean | clean |
| `format:check` | clean ¹ | clean ¹ |
| `check:classes` / `check:links` / `check:conflicts` | clean / 3260 links / clean | clean / 3260 links / clean |
| `NODE_ENV=production npm run build` + `check:build` | clean | clean (dnd-kit absent from `dist`) |
| `test:unit` (shared / API / web) | 320 / 921 / 1204 | 304 / 921 / 1211 |
| `test:component` | 342 files, 2089 tests | 343 files, 2094 tests |
| `test:api` | 125 files, 1431 tests | 125 files, 1427 tests |

¹ Only a local, git-ignored `.claude/launch.json` is flagged on this machine; not in the repository.

No lane was killed for memory. **Not run:** E2E (end of project); a real phone and a real screen reader (Review Focus).

**Real runs.**
- **#140:** a throwaway database `masaha_wi140_dev` (created, migrated, seeded with the demo set — never
  `masaha_dev`), API on 3340, web on 5340. The demo owner's `PUT /manage/spaces/1/contacts` with WhatsApp, Telegram, X,
  LinkedIn, YouTube and `OTHER` «ديسكورد» → 200, each in its stored form, the name trimmed; `OTHER` without a name →
  422 `contacts.0.label: required`; reception → 403; `GET /spaces/masaha-demo` answers every label. The public page in
  headless Chrome (1440 / 390, ar / en, light / dark): Telegram → `t.me` in a new tab, «ديسكورد» and «سيجنال» named by
  their own names with `dir="auto"`, «سيجنال»'s number a `tel:` link. Screenshots: `Downloads\wi140-shots` (4).
- **#141:** the showcase preview in headless Chrome at 1280 / 768 / 360, ar / en, light / dark: no overflow; real key
  events (RTL left arrow forward, focus kept, Escape restores, Tab drops and moves on, the cover follows the first
  place); a mouse drag in RTL; touch: a 400 ms press-and-drag moves a tile, a quick swipe moves nothing.
  Screenshots: `Downloads\wi141-shots` (15).
- Servers stopped by PID; ports 3340 and 5340 checked free.

## 4. Executor checks

- **EC1:** `SELECT count(*) FROM space_prices WHERE label_ar IS NOT NULL OR label_en IS NOT NULL` on `masaha_dev`: **0**.
- **EC2:** `@dnd-kit/core` 6.3.1 (2024-12-05), `@dnd-kit/sortable` 10.0.0 (2024-12-04), `@dnd-kit/utilities` 3.2.2
  (2023-11-06), plus core's `@dnd-kit/accessibility` 3.1.1 (2024-11-23); peers `react >=16.8.0`. Size: the four
  packages' unminified ESM files are **28.3 KB gzipped** together (core 22.1, sortable 4.7, utilities 2.4,
  accessibility 0.6), an upper bound. **The built chunk's size is measured in PR-C** (see Deviations: no chunk exists
  before a page draws the list).
- **EC3:** dnd-kit's live region stays empty; its described-by text is the caller's instructions; `aria-roledescription`
  the caller's word (jsdom test and Chrome).
- **EC4:** touch press-and-hold drags, a swipe does not (Chrome emulation); "a delete tap stays a click" needs PR-C's
  photo tiles.
- **EC5:** `migrate dev --create-only` once (`20261110085157_contact_types_and_other`); generated SQL = §7's statements;
  the `CHECK` appended by hand; applied to `masaha_dev`. Before and after, `SELECT type, count(*), count(label) FROM
  space_contacts GROUP BY type`: WHATSAPP 30, PHONE 16, EMAIL 3, INSTAGRAM 7, FACEBOOK 1, WEBSITE 1 — **58 rows, equal,
  zero labels** (before the migration the column did not exist).
- **EC6:** a blank label is `too_short` (T7; the contract says it).
- **EC7:** deferred to PR-C (the icons).
- **EC8:** PR-C (T16–T20 are its checks).
- **EC9:** the glossary gained «وسيلة تواصل» with the twelve types and «وسيلة أخرى»; «الأسعار المعلنة» and «سعر» come
  with the prices section in PR-C.
- **EC10:** #140's description says the merge applies one migration online.

## 5. Breaks made and tests seen failing first

- **Shared:** 16 tests red before `contacts.ts`/`requests.ts`; then the label rule dropped once (2 red), restored.
- **API:** 6 red before the repository and service; the service comparing values only (T11 red);
  `space_contacts_label_check` dropped from `masaha_test` once (T12 red), added back identical to `masaha_dev`'s.
- **Web (#140):** `contactLinkOf`'s new cases (5 red); the public page's isolation (1 red); the editor hook's three new
  tests (3 red); `mapsLink` with latitude and longitude swapped (red).
- **#141:** `sortableKeys` by a break (direction ignored: 2 red); `Sortable`'s nine tests passed at once, so each was
  proven by a break restored from a `cp` backup — Escape's `stopPropagation`, `onMove` on an unchanged drop, dnd-kit's
  default words, Tab keeping the lift, `disabled` ignored (1 red each); the entry test red before `sortable.ts` joined
  `LAYER_ENTRIES`; the `@dnd-kit/*` restriction removed once (3 red).

## 6. Problems met and how they were solved

- **`check:build` and a library no page uses.** It fails for any `LIBRARY_CHUNKS` group without a chunk in the build,
  and #141 draws the list on no production page, so the build holds no dnd-kit. The `sortable` group and its test rows
  move to PR-C (patch kept for it); #141 shows the build free of dnd-kit instead.
- **Docker stopped** between the two PRs (the session restarted); `test:api` could not reach the database. Docker
  Desktop and `db:up` started again; the lane re-run green.
- **Encoding while scripting:** curl on Windows sent «ديسكورد» as `???????` from a command-line argument (the API was
  right: the same body from a UTF-8 file stored the Arabic name); a Python edit turned `\r` in a Windows path into a
  carriage return; both caught and fixed before commit.
- **A pattern-based process kill was refused** by the tool's guard; the dev server was stopped by its own PID instead.

## 7. Anything unexpected

- **Contacts do not read Arabic-Indic digits.** The plan's T5 expected `٠٥٩٩١٢٣٤٥٦` → `+970599123456` and C2 says "as
  today (Arabic-Indic digits…)", but `normalisePhone` reads Western digits only, for WhatsApp and phone today too. Not
  asserted; not changed (it is the platform's phone rule). **Outside scope — for the owner:** a finding or a small item.
- `masaha_test` holds PR-A's migration while other branches run without it; `migrate deploy` tolerated it (#141's lane
  green).
- The throwaway `masaha_wi140_dev` is left in the container for inspection; drop it when no longer wanted.

## 8. The early conflict check

Open PRs: #140 and #141 only. `git merge-tree --write-tree`: **#140 × #141 clean; each × `origin/main` clean**; they
share no file. The palette lab's branch (`design/palette-lab`, `2ad55945`, not a PR): clean against both.

## 9. Departures from the plan or the prompt

1. **#141: the `sortable` library chunk moves to PR-C** (§6 problem above).
2. **#141: `renderItem` gets `handleProps` only; the layer draws each item's `<li>`** (instead of `itemProps` +
   `handleProps`): a feature spreads `handleProps` on the whole tile or on a grip, no two refs on one element.
3. **#141: `words.roleDescription` added**, so `aria-roledescription` is the caller's word (EC3).
4. **#141: `MouseSensor` + `TouchSensor`**, not `PointerSensor`: a pointer sensor also takes touch and would start a
   drag on a swipe.
5. **#141: the showcase's handle uses the layer's `EllipsisVerticalIcon`**; GripVertical comes with PR-C as planned.
6. **#140: T5's Arabic-Indic case not asserted** (§7).
7. **#140: T7 sits in `contacts.unit.test.ts`** beside the existing `updateSpaceContactsSchema` tests.
8. **#140: the editor offers `OTHER` on a row already of that kind** (a saved one), so a save never drops its name.
9. **#140: the audit records a name only where one is held**, so the existing types' entries keep their shape.
10. **#140: T14 extends the managed route's existing contacts row with an `OTHER` body** (owner 200, reception 403).
11. **#140's real run used a throwaway database**, not `masaha_dev`, to keep the presentation's data unwritten.

## 10. Findings recorded

None in Phase 1 (finding 216 is PR-C's). The Arabic-Indic digits (§7) is offered to the owner, not recorded.

## Next

Phase 2 (PR-C, `feat/space-profile`) waits for the owner's word that #140 and #141 are merged.


---

## Fix round (2026-11-10 → 11, `7_FIX_ROUND_AB.md`)

Reviews: `6_REVIEW_PR-A.md` (#140 at `29bcf80a`) and `6_REVIEW_PR-B.md` (#141 at `4109534c`), both "mergeable after a
fix round". `main` did not move (`7fb73c3c`). Backups: `backup/contact-types-1`, `backup/sortable-list-1`.

### 1. The pull requests and their new heads

| PR | New head (full SHA) | Commits | Files | CI | GitHub |
|---|---|---|---|---|---|
| **#140** | `357c4b923595d1f047cdc2efc32f59f8b34e11b0` | 3 | 41 | 10 pass, CodeRabbit skipped | `CLEAN` |
| **#141** | `14cfd5df486e91ef3cebfa023cc0e5bc2b2dce2f` | 1 | 16 | 10 pass, CodeRabbit skipped | `CLEAN` |

Each description gained a "Review fixes" section (and its evidence line).

### 2. The commits

- **#140:** `4622a003` A1 (unchanged) · `19c03996` `feat(spaces): contacts of any kind` (F1, F2, F6, findings 217
  and 218 folded) · `357c4b92` `test(spaces): refuse removing a package's shift` (F3, its own commit, as the prompt
  asks).
- **#141:** `14cfd5df` `feat(design-system): add a sortable list` (F1–F11 folded). No `fixup!` left on either branch.

### 3. #140 — what was done

- **F1** a YouTube link that names no channel is refused (`/watch`, `/shorts/…`, `/playlist`, `/results`, `/live/…`);
  `/@h`, `/channel/`, `/c/`, `/user/` kept — a per-network `paths` rule. T4 cases seen failing first.
- **F2** «وسيلة أخرى»: a value written as a number takes the phone rule only (`599123456`, `1800`, `+44.20.7946.0000`
  refused, no longer stored as an IP link). T5 cases seen failing first.
- **F3 / EC8** T16–T18 and T20 named in the PR by their existing tests (hours, profile, confirm, photos, the
  directory's covers); T19's package case added (owner's `PUT …/hours` leaving a package's shift out → 409, nothing
  written, no audit), proven by a break restored from a `cp` backup (`remove` detaching packages first → 200).
  A first break run was invalid (a Prisma client generated on #141's branch, without `label`, answered 500); the
  client was regenerated and the break repeated.
- **F4** finding **217** (Open): contacts and every phone refuse Arabic-Indic digits. Nothing converted; T5 unchanged.
- **Finding 218** (Open): a website's bare number is stored as an IP address; a Facebook video link loses its id.
  Both indexed and listed under spaces.md's open findings.
- **F5** nothing in #140 (PR-C's contacts Sheet clears or keeps the name when a row leaves `OTHER`; T41).
- **F6** LinkedIn from a country's two-letter subdomain stored on `www.linkedin.com`; another subdomain refused (T3).
- `data-model.md`'s contacts rule updated for F1, F2 and F6.
- **Verification on `357c4b92`:** lint and typecheck on each new commit; `format:check`, `check:classes`,
  `check:links` (3264), `check:conflicts`; build + `check:build`; `test:unit` 323 / 921 / 1204; `test:api` 125 files,
  1432 tests; `test:component` 342 files, 2089 tests. (A first API run was cut off when the session ended; re-run whole.)

### 4. #141 — what was done

- **F1** Escape heard on the window in the capture phase while lifted or dragging, its default prevented, so Radix's
  `DismissableLayer` keeps the Sheet open; `stopPropagation` gone. Test inside the layer's real open `Sheet`.
- **F2** a blur to another element drops the lift (as Tab); the refocus runs only after the list's own steps.
- **F3** Space/Enter lift only from the handle itself; a control inside keeps its keys.
- **F4** a cancel gives the focus back. **Not provable in jsdom** (its test passes at the old head: jsdom keeps the
  focus of a moved node); proven in headless Chrome (Arabic 1280, English 768).
- **F5** `touch-none` removed from the showcase; EC4 re-run: a quick swipe on a tile scrolls the page 225 px and moves
  nothing; a 400 ms press then a move still drags.
- **F6** the slide on `--easing-standard` and `--duration-medium` (reduced motion → 0) through `lib/sortableMotion.ts`,
  since jsdom has no `matchMedia` for a media-query read. Unit test.
- **F7** the first `dragOver` (the item over itself) skipped, so the lift is said. Not lane-provable (R-2).
- **F8** T28's list backward arrow in both directions. **F9** foundation §3's `check:build` sentence corrected.
- **F10** `aria-pressed` only while lifted or dragged. **F11** the caller's `items` passed as is when nothing is lifted.
- foundation.md: the Sortable row (Escape and overlays, the blur, controls beside the handle, no `touch-action: none`,
  the motion tokens) and the tree (`lib/sortableMotion.ts`).
- **Seen failing:** at the old head the new F1, F2, F3 and F10 tests failed; breaks restored from `cp` backups: F1
  (no window `preventDefault`), F2 (no blur drop), F3 (no target check), F6 (no swap), F8 (a list taking the backward
  arrow) — each red; F4's break stayed green in jsdom (above).
- **Verification on `14cfd5df`:** lint and typecheck; `format:check`; `check:classes`, `check:links` (3261),
  `check:conflicts`; build + `check:build` (dnd-kit absent from `dist`); `test:unit` 304 / 921 / 1213;
  `test:component` 343 files, 2097 tests. `test:api` left to CI (no API code changed), as the prompt allows.
- A lint rule (refs written during render) refused the first version of the "latest cancel" ref; it is set in a
  layout effect instead.

### 5. Not taken

- **#141 F12** (a repeated `held` unsaid; a stale lift returning when the item set changes back): a nit outside the
  prompt's F1–F11; unchanged.

### 6. Early conflict check (new heads)

Open PRs: #140 and #141. `git merge-tree --write-tree`: **#140 × #141 clean; each × `origin/main` clean.**

### 7. Anything unexpected

- The session ended twice mid-run (lanes cut off, a background watch stopped); each lane affected was re-run whole.
- jsdom does not lose the focus of a moved node, so F4's component test cannot fail on its break; Chrome carries it.

Then stop: never merged; no branch deleted (the `backup/*` branches are kept).
