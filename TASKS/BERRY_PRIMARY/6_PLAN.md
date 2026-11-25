# WI-B — the berry on the main action: the plan

> Prompt: `5_PLAN_AND_EXEC_PROMPT.md`. Read on `main` = `c3968a74` (checked against `origin/main` on 2026-11-25; open PRs: none
> yet, C2's #157 expected). Status: **approved by the owner, 2026-11-25: D1–D7 as recommended (the desk's «تحصيل» rows stay filled ink); the WhatsApp assertion goes in `ContactBar`'s own test (C2 edits `SpacePage.component.test.tsx`).**

## 1. Summary

The design system gets a role of its own for the main action, `main-action`. In light it is `spark-600` with white text
and hovers to `spark-700`. In dark it keeps today's ink button (`n-50`, `n-950` text, today's hover), as B1 decides.
`Button` gets a new **opt-in** variant, `main`, that draws it. `primary` (the ink) stays the default and keeps
everything it draws today. Each screen's one main action, and each overlay's confirming action, opts in, screen by
screen (§4.3). The token test makes B1's measures permanent: contrast, shape, and distance from `destructive` with and
without simulated protanopia and deuteranopia, in both themes. It also pins the dark theme to the ink, so the dark
button cannot drift. ADR 0022 gains its *Revised* line as a commit of its own. Foundation §4, §5, §11 and §12 and the
showcase describe what is built.

## 2. Contract

**Scope**
- The `main-action`, `main-action-foreground` and `main-action-hover` roles in both themes, and their utilities.
- `Button`'s `main` variant.
- The call sites in §4.3 opt in. The two tests that assert today's look on a changed button follow it.
- The token tests and the `Button` tests in §9.
- ADR 0022's *Revised* line; foundation §4, §5, §11, §12; the showcase's Button section.

**Acceptance criteria**
- [ ] In light, a `main` Button is `spark-600` with white text and hovers to `spark-700`. In dark it is `n-50` with
      `n-950` text and hovers like today's `primary` Button. Every other variant, and every control that draws `primary`,
      is unchanged in both themes.
- [ ] Each screen in §4.3 shows at most one `main` button at a time. Each overlay's confirming action is `main`.
- [ ] `semantic.unit.test.ts` holds these, in both themes:
  - text ≥ 4.5 : 1 on the fill and on its hover;
  - the fill and its hover ≥ 3 : 1 on `background`, `card` and `popover`;
  - ΔE ≥ 0.10 from `destructive` with normal vision, and ≥ 0.08 under protan and deutan simulation, for the fill and its hover;
  - dark's main action painted as the ink.
- [ ] The main action has fill utilities only: no `text-main-action` and no `border-main-action`.
- [ ] `Button`'s default stays `primary`. The focus ring is the one `ring` style.
- [ ] ADR 0022's *Revised* line, word for word, in its own commit.
- [ ] Foundation and the showcase describe only what is built.
- [ ] Every lane, the build and its check pass locally and in CI. The PR is `CLEAN`.
- [ ] The Chrome pass has a before / after pair for each screen in `C:\Users\basel\Downloads\berry-shots\`, with axe clean.

**Out of scope**
- The berry-to-plum brand surfaces (ADR 0022 point 4), the logo, the icons and the e-mails.
- The status colours, the charts, the sidebar's count (§13, D5) and every `primary` control: Checkbox, RadioGroup,
  Switch, Tabs' pill, Calendar's days, Meter, Heatmap, Badge `primary`, the Toast's action, the link variant and the
  links.
- Anything in C2's files before C2 merges (§7).
- API code, schema, migrations, dependencies, database writes.

## 3. Reading done

- **Always:** CLAUDE.md; workflow §2, §4, §6, §9; the map; the open findings' titles (§6).
- **Skills:** `start-work-item` and `write-plan`. `open-pr` and `final-report` are left for phase 2.
- **ADRs and decisions:**
  - ADR 0022 and ADR 0019, with 0019's *Revised* line;
  - `BERRY_PRIMARY\0_OWNER_DECISIONS.md` (every entry, B1 included);
  - A18 in `DESIGN\AUTH\0_OWNER_DECISIONS.md`.
- **Foundation:** §4 and §5 in full; §11's adaptation rules; §12 in full; §15.
- **The layer:**
  - `primitives.css` (the ramps), `semantic.css`, `semantic.unit.test.ts` (all of it, with its maths), `themes.ts`,
    `tailwind.css`;
  - `Button.tsx` and its test, and `AlertDialog.tsx`'s two answers;
  - the components that draw `primary`: Checkbox, RadioGroup, Switch, Tabs, Calendar, Meter, Heatmap, Toast;
  - the spark's users.
- **The inventory:** every Button-like JSX element in `apps/web/src`, parsed with the TypeScript compiler (427
  elements; 81 `Button`s with no variant, about a dozen with a computed one), and the tests that assert `bg-primary`.
- **Pictures:**
  - the prototype's `Space details/inplace.css` (`.inplace-primary`: `spark-600` + white, hover `spark-700`; its dark
    `spark-400` is superseded by B1);
  - the P2 captures' list;
  - the berry trial's desk and home captures (light, after).
- **C2:** `AUTH_IN_PLACE\WI-C2\2_PLAN.md` §7 (its files).
- **Capability documents:** `desk.md` DI-4 and DI-20 (the filled «تحصيل» and the search's check-in), `directory.md`
  and `space-links.md` (the filter sheets' "primary" button). They describe a filled button in general terms, so none
  of them changes (§7).
- **Measured again** with the test file's own maths, in a scratch script:

  | Measure | Light: `s-600` / hover `s-700` | Dark: `n-50` / hover |
  |---|---|---|
  | Label on the fill | 5.91 / 7.94 : 1 | 18.10 / 11.54 : 1 |
  | Shape on `background` | 5.69 / 7.63 | 18.10 / 11.54 |
  | Shape on `card` | 5.91 / 7.94 | 15.95 / 10.17 |
  | ΔE from `destructive`, normal / protan / deutan | 0.163 / 0.161 / 0.160 and 0.174 / 0.131 / 0.172 | 0.329 / 0.365 / 0.278 and 0.222 / 0.223 / 0.150 |

  This matches the supervisor's numbers. Dark's hover is new here, and it passes too.

## 4. The settled decisions, as they will be built

### 4.1 The role

| Role | Light | Dark |
|---|---|---|
| `main-action` / `main-action-foreground` | `spark-600` / `white` | `neutral-50` / `neutral-950` |
| `main-action-hover` | `spark-700` | `color-mix(in oklab, var(--neutral-50), var(--neutral-950) 18%)` |

- The values are written from the primitives, never as `var(--primary)`. Dark equals the ink by decision, not by
  reference (foundation §4, *coincidence is not identity*), so a later change to the ink does not move the main
  action without a decision of its own.
- **Its focus ring is the system's one `ring`.** The 2 px outline sits 2 px outside the fill, on the page, where
  `ring` is already verified at 3 : 1. No role of its own.
- **A state takes its surface's text:** `main-action-hover` has no foreground. Its label is
  `main-action-foreground`, verified on it.
- **`tailwind.css`:** `--color-main-action-foreground` joins the theme colours, so `text-main-action-foreground`
  exists. The fill is offered only as two utilities, `bg-main-action` and `bg-main-action-hover`, as the spark's are
  (§5, S1).

### 4.2 `Button`

- **A new variant, `main`:** `bg-main-action text-main-action-foreground hover:bg-main-action-hover`.
- **`defaultVariants.variant` stays `primary` (the ink).** The inventory decides it:
  - **Too many to flip.** 81 buttons have no variant today. About 45 of them are a screen's or an overlay's main
    action. The rest are secondary or repeated actions, and settings cards that each save on their own. Flipping the
    default would turn all of them berry. Each extra one would then need a demotion, and every future default button
    would be berry too, which breaks ADR 0022 point 1 quietly.
  - **Opting in fails safe.** A main action someone forgets stays ink, which is today's look.
  - **ADR 0022 point 2 keeps the ink for secondary actions.** So a filled ink button stays a correct secondary.
- **`AlertDialogAction`'s default stays `primary`.** Its one non-destructive caller (`HoursSheet`) passes `main`.
- The `null` variants (`SiteMenu`, `AccountLayout`, `SectionIndex`, `Calendar`, `NearMeButton`) take no variant
  classes in `cva`, so the change does not touch them.

### 4.3 The main action, screen by screen

**The rule:**
- A screen's main action is the action the screen exists for.
- An overlay (Dialog, AlertDialog, Sheet, AdaptiveDialog) is a screen of its own while it is open. Its confirming
  action is its main action, as in the approved P2 picture.
- A page of independent cards that each save on their own has no single main action, so its saves keep the ink.
- So do error, empty, forbidden and not-found states, whose action is a recovery and not the screen's purpose.
- Where the same action shows twice, the toolbar's copy is the main one and the empty state's copy keeps the ink.
- Destructive stays red.

**Screens that show more than one default button today:**

| Screen | Today's default buttons | Main action (`main`) | The others |
|---|---|---|---|
| Desk (screen 12), from 768 px | Top bar «تسجيل زيارة»; each uncollected row's «تحصيل»; the search's «تسجيل زيارة باسم…» when nothing matched; a result card's check-in | The top bar's «تسجيل زيارة» | Stay ink: DI-4 and DI-20 chose them filled. Outline is the alternative (§8, issue 3) |
| Desk, below 768 px | The action bar's «تسجيل زيارة» and the same rows | The action bar's «تسجيل زيارة» | As above |
| Customer file (header) | The state's buttons, the first filled | The first state action (`StateButtons`, index 0) | Outline, as today |
| Customers (screen 14) | Toolbar «إضافة زبون»; the empty state's copy | The toolbar's | The empty state's copy stays ink |
| Staff | Toolbar add; the empty state's copy | The toolbar's | The empty state's copy stays ink |
| Announcements | Header «إعلان جديد»; the empty state's copy | The header's (`AnnouncementsList.tsx:137`) | The empty state's copy (`:81`) stays ink |
| Owners (admin) | `AddOwner`'s trigger; the list's empty copy | `AddOwner`'s trigger | The empty state's copy stays ink |
| About | «تصفّح المساحات»; `PlatformContact`'s first channel, twice | «تصفّح المساحات» | The channels stay ink (first) and outline (others) |
| Account settings | Profile «حفظ»; password «حفظ» | None (independent cards) | Both stay ink |
| Space settings (owner) and platform settings (admin) | One «حفظ» per card | None | All stay ink |
| Space profile editor | Empty sections' actions; photos' upload | None on the page | Stay ink. Its edit sheets' saves are `main` |
| Lookups (admin) | The amenities' add (explicit `primary`) | None (cards) | Stays ink. Its sheets' saves are `main` |
| Directory map, from 768 px | The selected space's «التفاصيل»; the pick card's confirm | None: the directory leads with live status (ADR 0022, *Context*) | Stay ink. The phone filter sheet's «عرض…» is `main` |

**Screens with one main action, opting in:**
- Home: the search's «بحث».
- Space page below 768 px: `ContactBar`'s «واتساب». For from 768 px, see §8, issue 1.
- The forced password change: its submit.
- Admin «المساحات»: «إضافة مساحة».
- Add space: its submit.
- Packages: `PackagesSection`'s add.

**Overlays, whose confirming action becomes `main`:**
- **Desk:**
  - the visit, check-out, collect, debt, pay, price, usage-out and edit-customer dialogs;
  - the correct and subscription sheets;
  - the pre-check-in dialog's main path (which of its buttons is checked when built).
- **Space and admin:**
  - the announcement, package, `AddStaff`, `AddOwner` and link-owner forms;
  - the reissue, issue-password and temporary-password dialogs;
  - the editor's `EditSheet`;
  - `HoursSheet`'s unify confirmation;
  - the amenity and lookup forms;
  - the data reports' `DecideSheet`.
- **Public:** the report dialog.
- **Every phone filter sheet's «عرض…»:** the directory, customers, ledger, audit, admin reports and admin spaces.

**Stay ink** (states and repeats): `RetryState`, `ForbiddenState`, not found, a space not found, the favourites' empty
«تصفّح», the report notice's «حلّ», `SectionEmpty`, the photos' upload, `UncollectedRow`, `CustomerCard`, `DeskSearch`,
and the map's cards.

**C2's screens, which wait (§7):**
- sign-in, register, forgot and reset forms (`features/auth/**`);
- the reset and forgot pages' link buttons (`pages/site/auth/**`);
- `SignInPrompt`.

They follow the same rule: the form's submit, or the done state's one link, is `main`.

About 45 call sites, each a one-word change. The exact list is pinned when built and reported.

### 4.4 The dashboard is quieter (point 5)

With the opt-in, the dashboard's berry is its selected item (the sidebar's current tint and `spark` bar, the tabs'
line, a chip that is on) and its main action. Nothing else on its buttons is berry. The sidebar's count badge and
`chart-1` also draw the spark today. They are left as they are, and this is put to the owner (§13, D5).

### 4.5 ADR 0022's *Revised* line

Under its status line, word for word, dated the commit's date:

`> **Revised:** <date> — the berry main action is the light theme's; in the dark theme the main action keeps the ink's
light step with dark text, as before (the owner, after seeing both on the real screens). The body below is left as
first written.`

It goes in commit 1, `docs(adr): keep dark main action in the ink`, with a body.

## 5. Stronger decisions

- **S1. The main action offers fills only.**
  - **What:** no `--color-main-action` theme colour, so `text-`, `border-`, `ring-` and `outline-main-action` do not
    exist. `bg-main-action` and `bg-main-action-hover` are `@utility`s, as the spark's four are, and a test holds the
    list.
  - **Why:** ADR 0022 rejects a berry link beside a berry button, and links stay ink. Without this, `text-main-action`
    would exist and pass contrast in light (5.91 : 1), and nothing would stop it.
  - **Cost:** two utilities and one test. It departs from shadcn's naming in the same way the spark already does.
  - **Recommended.**
- **S2. Dark is pinned to the ink.**
  - **What:** a unit test holds dark's `main-action`, its foreground and its hover to the ink's painted colours
    (`#f7fbff`, `#0d1217`, and today's hover hex), written by hand.
  - **Why:** B1's "the dark theme's buttons do not change at all" becomes a test, not a memory. The superseded P2 dark
    (`spark-400`) fails it.
  - **Cost:** one test.
  - **Recommended.**
- **S3. The hover is measured as fully as the fill.** The hover gets text, shape and the three distance measures too.
  B1's protan hover distance, 0.131, is the slimmest margin. Cost: a few more cases. Recommended.
- **S4. The shape is also measured on `popover`.** The overlays (Sheet, Dialog, AdaptiveDialog) draw on `popover`,
  where most `main` buttons will sit. Light `popover` is white and dark is `n-900`, which today equal `card`, but the
  roles are separate. Cost: two cases. Recommended.
- **A rule this item weakens: foundation §5's usage rule, "the spark is never … on an action".** It still holds for
  the `spark` role (`s-500` / `s-400`). The main action is a separate role, at a step darker. The rule is rewritten to
  say so, and to point to ADR 0022. `Button`'s test "draws the %s variant without the spark" keeps its meaning for
  every variant, `main` included: no `spark` utility on an action. Nothing else is contradicted.

## 6. Related findings

The open findings are 23, 65, 152, 215 and 221.
- **215** (the prototype's home disagrees with production) and **221** (the README's screenshots show *Sea*) touch the
  identity's pictures, not tokens or Button. **Not folded:** the README's shots are better retaken once the brand
  surfaces exist, and 215 is about content.
- **23, 65 and 152** are API.

No new finding is expected. If one is needed, I'll ask for a number range, since the prompt gives none.

## 7. Files

**Edited:**
- **The layer:** `tokens/semantic.css`, `tokens/tailwind.css`, `tokens/semantic.unit.test.ts`,
  `components/actions/Button/Button.tsx`, `Button.component.test.tsx`.
- **The showcase:** `pages/showcase/sections/actions/ButtonSection.tsx` and `pages/showcase/fixtures.json` (the
  variant's sample words).
- **The call sites in §4.3,** in `features/{desk,announcements,packages,staff,space-links,spaces,lookups,data-reports,
  users,directory,payments,audit}`, `pages/dashboard/admin/SpacesPage.tsx`, `pages/dashboard/space/desk/DeskPage.tsx`
  and `pages/site/public/{home/HomeSearch,about/AboutPage}.tsx`.
- **Their tests where they assert the look:** `StateActions.component.test.tsx` and `AboutPage.component.test.tsx`
  (`bg-primary` becomes `bg-main-action`). `UncollectedCard` and `FavoritesView` keep `bg-primary`, since they stay ink.
- **Documents:**
  - ADR 0022 (the *Revised* line);
  - foundation:
    - §4: the brand's intro names the main action's step;
    - §5: the *Actions* row, *Values*, *Verified*, *Usage rules*, and the "a state takes its surface's text" line;
    - §11: *A hover never fades a fill*;
    - §12: the Button row.

**Shared with C2.** C2 touches no design-system file and not `foundation.md`.
- **C2's files I would otherwise edit:**
  - `features/auth/components/{sign-in/SignInForm,register/RegisterForm,forgot-password/ForgotPasswordForm,reset-password/ResetPasswordForm}.tsx`;
  - `pages/site/auth/{ForgotPasswordPage,ResetPasswordPage}.tsx`;
  - `pages/site/public/SignInPrompt.tsx`.

  **This part waits.** If #157 has merged before my push, I rebase and add it as its own commit, on C2's code and by
  the same rule. If not, the PR goes without it, and the report lists the edits for a follow-up (§13, D4).
- **`features/users/.../ForcedPasswordChangeForm.tsx`** is mine. C2 edits only that form's *tests*, so there is no
  shared file.
- **`ReportDialog.tsx`** is mine. C2 edits `ReportAction.tsx` beside it.
- **Checked again at the report** with `git merge-tree` against C2's head.

**Size:** about 55–60 files. That passes the workflow's review threshold of about 25. It touches no security,
transaction, schema, dependency or CI, so the threshold alone calls for a separate review.

**No other layer, no licence.**

## 8. Design issues (built only once approved)

1. **The space page has no main action from 768 px.** `ContactBar`'s «واتساب» shows below 768 px only. From there,
   the contacts are a list of links. The prototype's space page is where the berry was first approved, and on a
   laptop it has none.
   - **Proposal:** make the first contact channel in the side panel a `main` Button (WhatsApp, as on phones). That is
     the same pattern `PlatformContact` already uses: first channel filled, the others outline.
   - **Not built** unless approved, since it changes the page's layout.
2. **Overlays over a page.** With an overlay open, two berry buttons are in view: the overlay's, and the page's under
   the scrim.
   - **Proposal:** accept it. The scrim dims the page (50 % in light, 70 % in dark), and the overlay is the screen
     while it is open.
   - The alternative is to keep overlay submits ink. That gives up the approved P2 picture.
3. **The desk's uncollected rows** stack several filled ink «تحصيل» buttons under the berry check-in.
   - **Proposal:** keep them ink (DI-4).
   - **The alternative** is outline, which is quieter beside the berry, but undoes an owner decision. Put to the owner.
4. **An empty state that repeats the toolbar's action** (customers, staff, announcements, owners) would show the same
   action twice, once berry and once ink.
   - **Proposal:** the toolbar's copy is `main`, and the empty state's stays ink, as today.
   - **The alternative** is to drop the empty state's button where the toolbar's is in view. That changes behaviour,
     so it is not proposed here.

## 9. Tests: lane, test, and the break each catches

Every new test is seen failing first. For token and variant tests, that means adding the test before the role or
variant, then making the break below once.

**Unit — `semantic.unit.test.ts`** (the same file, the same maths as 0019's criteria):

| Test | Break that fails it |
|---|---|
| `ROLES` gains `main-action`, `-foreground` and `-hover`: key parity, and "resolves every role" in both themes | Leaving `main-action-hover` out of the dark rule |
| `main-action-foreground` on `main-action` ≥ 4.5 (the `-foreground` rule already generates it) | Light fill `spark-500`, 4.11 : 1 (ADR 0022's rejected option) |
| `main-action-foreground` on `main-action-hover` ≥ 4.5 | Light hover `spark-400` |
| `main-action` and `main-action-hover` on `background`, `card` and `popover` ≥ 3 (S3, S4) | Dark fill `spark-600` + white: 2.80 : 1 on `card` (B1's rejected option) |
| "The brand never reads as an error": `main-action` and `main-action-hover` join `primary` and `spark`, three visions, both themes (S3) | A main-action fill of `red-600`. Plus one closer break made and reported: light hover `spark-800` under protan |
| "The main action offers only fills": its `@utility`s are exactly the two, and `tailwind.css` has no `--color-main-action` or `--color-main-action-hover` (S1) | Adding `--color-main-action` to `@theme` |
| "Dark: the main action keeps the ink": painted `#f7fbff`, label `#0d1217`, and hover today's painted hex, all written by hand (S2) | Dark `main-action: var(--spark-400)` (the superseded P2 dark) |

**Component — `Button.component.test.tsx`:**

| Test | Break that fails it |
|---|---|
| "draws the main variant with the main action's fill, label and hover" | `main` mapped to `bg-primary` |
| "stays in the ink unless asked: no variant is `primary`, never the main action" | `defaultVariants.variant: 'main'` |
| The existing `it.each` cases (no table-row hover, no spark, axe) gain `main` | `main` given `hover:bg-spark`, or a table-row rule |

**Component — the screens:** updated assertions in `StateActions` (the first state button is `bg-main-action`, the
second is not) and `AboutPage` («تصفّح» is `bg-main-action`). New one-line assertions go in the screens' existing
tests for Home's «بحث», the desk's top-bar check-in, and `ContactBar`'s «واتساب»: those three must not drop back to
the ink quietly. Break for each: its `variant="main"` removed.

**Not tested in a lane:** the colour as painted, the hover in a real browser, and the dark theme's sameness on screen.
The Chrome pass covers these (§12).

## 10. Review focus (inputs no planned test exercises)

- The about 40 overlay and list call sites with no assertion of their own: a `variant="main"` missed or misplaced
  there shows only in the Chrome pass and the diff.
- The pre-check-in dialog: which of its paths is the main one.
- Every place `cn` merges a caller's `className` over `main`. `twMerge` must still treat `bg-main-action`, an
  `@utility`, as a background colour, so that `className="w-full"` and similar keep the fill. To check in the browser.
- High-contrast and forced-colours modes: the fill becomes the system button colour, as `primary` does today.

## 11. Commits

All Conventional, each subject ≤ 50 characters, each with a body, no tool attribution.

1. `docs(adr): keep dark main action in the ink`: ADR 0022's *Revised* line only.
2. `feat(design-system): add the main action role`: `semantic.css`, `tailwind.css`, the token tests, and foundation
   §4, §5 and §11.
3. `feat(design-system): add Button's main variant`: `Button` and its test, the showcase, and foundation §12.
4. `feat(web): mark each screen's main action`: the call sites in §4.3 and the two updated tests, with the three new
   assertions.
5. *(Only if #157 has merged before the push.)* `feat(auth): mark the auth forms' main action`.

`#PRNUM` in documents is replaced just before the push: expect #158, or the next free number after checking the PR and
Issue lists.

## 12. Verification (phase 4)

- **"Before" shots first.** Servers on 3320 / 5320 on `origin/main`, before any edit lands.
- **On the head, one at a time** through `heavy.mjs b …`: `format:check`, `lint`, `typecheck`, `check:classes`,
  `check:links`, `check:conflicts`, `test:unit`, `test:component`, the production build (`NODE_ENV=production`), then
  `check:build`. `test:api` is left to CI, since no API code changes. If a run is killed for memory, it is retried
  once, then left to CI, and that is said.
- **Chrome,** with the browser pane shown before any layout or axe check:
  - the screens: home, a space page, the directory, sign-in, the desk (owner), and admin «المساحات»;
  - at 390 and 1440, in Arabic and English, in light and dark;
  - on each: the main action's colour and its hover, the focus ring on it, every other control unchanged, and axe;
  - plus one overlay, the visit dialog, in light;
  - a before / after pair per screen, curated, in `C:\Users\basel\Downloads\berry-shots\`, never in the repository;
  - servers stopped by PID afterwards and the ports checked free;
  - if the memory guard stops them, they are restarted once at ≥ 4 GB free; if that fails, the pass is skipped and
    that is said.
- **Then** push, open the PR with `open-pr`, wait for `gh pr checks` green on the pushed head and `CLEAN`, then
  `7_REPORT.md` with `final-report`. **Never merge.**

## 13. Decisions needed from the owner

- **D1. Opt-in `main` variant; the default stays the ink.** The other choice is to flip the default to berry and
  demote the extras. **Recommended: opt-in** (§4.2).
- **D2. An overlay's confirming action is its main action, so it is berry.** That covers about 30 dialogs and sheets,
  the desk's included. **Recommended: yes** (the P2 picture; §8, issue 2).
- **D3. The table in §4.3:**
  - the main action on each screen;
  - "the others stay ink" on the desk (DI-4, DI-20), with outline as the alternative (§8, issue 3);
  - no berry on settings pages, error, empty and not-found states, or the directory.
- **D4. C2's auth forms:** they go in this PR if #157 merges before my push, otherwise in a follow-up. That follow-up
  could be my small PR after both merge, or a fix in C2's conversation once `main` exists. **Recommended: mine,
  after both merge.**
- **D5. The dashboard's other berry:** the sidebar's count badge (`sidebar-primary`) and `chart-1`. A strict reading
  of point 5 would turn them ink. **Recommended: keep both.**
  - The count is ADR 0019's "what matters now" mark, which point 6 keeps.
  - `chart-1` is a data series, not a mark.
  - Changing either reopens the palette's distance checks, outside this item.
- **D6. Design issue 1** (a `main` contact on the space page from 768 px): build it here, or leave it for the space
  page's design. **Recommended: here,** since it is one variant on the first channel.
- **D7. The stronger decisions S1–S4.** **Recommended: all four.**

## Proposed alternatives

None against ADR 0022 or B1. ADR 0022's *Consequences* says "every screen's main action changes colour at once, in
both themes". After B1, that holds in light only, and the *Revised* line says so. The opt-in in D1 changes how the
change is built, not what the ADR decides.
