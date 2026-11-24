# WI-C1 — Plan: `AdaptiveDialog`, a dialog from 768 px and a full-screen panel below it

> Worker: Claude Code (Opus 5.5), main folder `C:\dev\masaha\app`, `main` = `e0f9f66a`, clean.
> Prompt: `1_PLAN_AND_EXEC_PROMPT.md`. Status: **waiting for the owner's approval.** Nothing is built and no branch
> is cut.

## 1. Summary

The design-system layer gains **`AdaptiveDialog`** (category `overlays`): one modal dialog, built on the same Radix
Dialog primitive as `Dialog`, whose form follows the width. From 768 px it is the layer's centred dialog; below it a
full-screen panel with a top bar holding the close button, its body scrolling under the bar, sliding up. Opening it
adds one history entry at the same address, so the browser's or the phone's Back closes it and keeps the page. The
focus returns to whatever opened it, however it closes. `SignInPrompt` moves onto it, its words unchanged: on a phone
the guest's sign-in prompt becomes the full-screen panel, and its two links replace the overlay's history entry.

**The name.** `AdaptiveDialog`: it is a dialog, with a dialog's role and focus rules, whose form adapts to the width.
The name says what it is and keeps it beside `Dialog` in the inventory. The branch is `feat/adaptive-dialog`. I
renamed it from the prompt's `feat/adaptive-overlay` to match the component.

## 2. Contract

**Scope.** The layer component with its parts, its history entry, its focus rules, the busy block, its showcase
section, and its inventory row. `SignInPrompt` on it. A home for the overlay's history entry in
`docs/frontend/architecture.md` §2.

**Acceptance criteria**
- [ ] From 768 px: a centred dialog, 30 rem wide (§4, D1), with the close button in its corner as `Dialog` has it.
- [ ] Below 768 px: a full-screen panel (`100dvh`, no radius, no border). Its top bar stays while the body scrolls
      and holds the close button: 44 px, at the bar's inline start. Safe-area insets apply top and bottom.
- [ ] The panel slides up with `--duration-medium` and `--easing-standard`. Under reduced motion it appears at once
      (the token is 0 ms).
- [ ] Opening adds exactly one history entry at the same address (no URL change), and Back closes it. The page stays
      mounted, scrolled where it was.
- [ ] Closing it any other way (its button, Escape, the scrim, a done action) removes the entry, so Back afterwards
      leaves the page.
- [ ] A link inside it replaces the entry, so no dead Back press is left. A reload while it is open shows the page
      with it closed.
- [ ] Focus: trapped while open. On a phone it goes to the title. From 768 px it follows the layer's dialog
      behaviour, or the caller's choice. On every way of closing, Back included, it returns to the trigger.
- [ ] A caller may block closing while it is busy: Escape, the scrim, the close button and Back.
- [ ] Showcase: a section, seen at both widths, light and dark, Arabic and English (the toolbar's settings).
- [ ] `SignInPrompt` is on it, its content unchanged; its links replace the entry, and the held favourite or report
      works as today.
- [ ] Tests in the component lane (and one unit assertion for the reduced-motion token), each seen failing.
- [ ] foundation §3 (the category's list) and §12 (the new row, `Dialog`'s row pointing to it). architecture §2: the
      overlay's history entry, in one home. `favorites.md` and `data-reports.md` are untouched, since what they say
      of the guest's prompt stays true (checked, §6).

**Out of scope.** The sign-in form, register, the reset request, Google, the lazy chunk and its `check:build` rule,
and removing the round trip are WI-C2's. The berry primary button is WI-B's. `ReportDialog`, the other dialogs and
`Sheet` stay as they are (no migration). There are no API, schema, dependency or catalogue changes: the prompt's
words already exist (`site.signInPrompt`), and the showcase's samples live in `fixtures.json`.

## 3. Reading done

CLAUDE.md; workflow (all); testing (all); documentation rules (all); the map's *read it when* lines and the deferred
table (nothing triggered); the findings index's open titles; ADR 0021; `0_OWNER_DECISIONS.md`; `1_ANALYSIS.md` §0,
§1, I2, I4, I7, I9, I15 (and the rest, for context); foundation §3, §5 (*Other scales*: motion, z-index), §8, §9,
§10, §11, §12; architecture §2 (groups, the shells' focus, `useMainFocus`, landing and guards); the layer's `Dialog`,
`Sheet` and their tests, `useMediaQuery`, the motion tokens (`primitives.css`: reduced motion sets both durations to
0 ms), the touch control height; the showcase's registry, preview and `DialogSection`, plus `fixtures.json`;
`SignInPrompt`, `useSignInPrompt`, their test, and `useHeart`; `useFavoriteToggle` / `FavoriteButton`;
`useReportAction` and `ReportDialog` (its busy pattern); `heldIntent.ts`, `guestLeaving.ts`; `useLeaveGuard` (the
only `useBlocker`); `favorites.md` and `data-reports.md` (a guest's press); react-router 8.4's history and the
router's popstate handling (`lib/router/history.js`, `router.js`); Radix Dialog 1.1.23's focus return
(`onCloseAutoFocus` → `triggerRef`); the prototype's `inplace.jsx` / `.css`, `decisions/Space details.md`, and the
six P1 captures; `src/test/screenWidth.ts`, `startPreferences.ts` (it stubs `matchMedia` to `false`, so every page
test renders the phone form).

## 4. The settled decisions, as they will be built

**Parts** (exported from `@shared/design-system`):
`AdaptiveDialog` (the root: `open`, `onOpenChange`, `busy`), `AdaptiveDialogContent` (`closeLabel`, plus Radix
Content's props), `AdaptiveDialogHeader`, `AdaptiveDialogTitle`, `AdaptiveDialogDescription`, `AdaptiveDialogFooter`.
There is no `Trigger` part, since no caller has one: the prompt opens from a feature's hook, and the focus return
(below) does not need one.

**The form follows `useMediaQuery('(min-width: 768px)')`** (the layer's width hook, as Sidebar and DataTable use it).
The tree stays the same at both widths: the caller's children always sit at the same place inside one body element.
So a rotation or a resized window re-styles the overlay without remounting what the caller put in it (a form keeps
its values).
- **From 768 px:** `Dialog`'s surface and scrim (`modalContentClasses`, `overlayClasses`, reused), 30 rem wide
  (`md:max-w-120`), padding `p-8` as in the picture, and the close button in the corner as `Dialog` draws it.
- **Below 768 px:** `inset-0 h-dvh w-full max-w-none rounded-none border-0`, flex column. The **top bar** is
  `flex-none`, `h-14` plus `pt-[env(safe-area-inset-top)]`, `px-2`, and a `border-b`. It holds the close button,
  `ghost`, `size-11` (44 px), at the inline start (logical classes; it is first in the bar's flex row). The **body**
  is `flex-1 overflow-y-auto`, padded `px-5 pt-6`, with its end padding plus `env(safe-area-inset-bottom)`. The
  **slide**: `data-open:animate-in slide-in-from-bottom-6 fade-in-0`, closing in reverse, with
  `duration-(--duration-medium) ease-(--easing-standard)`. Under reduced motion the token is 0 ms, so it appears at
  once. These are the picture's 24 px rise and fade.
- **Title:** `text-heading-1 md:text-heading-2` (24 px on a phone, 22 px from 768). These are the picture's sizes on
  the scale (§8, design issue 2). It has `tabIndex={-1}` and `outline-none`, since it is the phone's focus target and
  not a control, as `main` is.
- **Footer:** stacked with the main action on top below 768 px, and in a row at the end from 768 px (`Dialog`'s
  footer, keyed on `md` instead of `sm`).

**The history entry: the history API, beside the router, inside the layer.** The prompt asked me to choose between
the router's own navigation with state and the history API beside it, and say why. I chose the history API. The
reasons:
1. **The layer stays closed.** The layer imports nothing app-level and has never needed a router: the showcase and
   the layer's tests render it without one. With the router's `navigate`, the component would need a data router
   around it, and every caller would get router coupling from a visual component.
2. **It is not a navigation.** ADR 0021 point 3 says the overlay has no address. A router push to the same URL is
   still a navigation that every location listener sees twice (on opening and on closing): `useNavigationType`,
   location-keyed effects, a revalidation of loaders if any are added later, and a scroll reset unless
   `preventScrollReset` is passed. With the history API, the router sees only Back, as a POP to the same location.
3. **What that POP touches, checked:**
   - The pushed state copies `history.state` (the router's `key`, `idx`, `usr`) and adds one marker, so the router's
     index arithmetic reads delta 0 and `useLocation().state` is unchanged.
   - `useMainFocus` compares the pathname and the hash, which are unchanged, so it moves nothing.
   - `noteSitePage` compares the pathname, so a guest's held action is not let go.
   - `ScrollRestoration` saves and restores the same key's position, so the page stays where it was.
   - The one `useBlocker` (the space editor's) blocks only a change of pathname, so it never fires.
   - The route element is the same match, so the page stays mounted.

**The mechanics** (one small module in the component's folder, `historyEntry.ts`):
- **Opening:** `history.pushState({...history.state, [MARK]: token}, '')`, with no URL argument (same address). The
  token is unique per opening and per page load. A `popstate` listener runs while it is open.
- **Back:** `popstate` arrives on an entry without its token, so the component calls `onOpenChange(false)`. If the
  caller is `busy`, it pushes the entry again and stays open instead.
- **Closing any other way** (`open` turning false, including a caller's done action): if the current entry still
  carries its token, `history.back()`. The page entry is then current again, and the next Back leaves the page.
- **A link inside** (the caller's `<Link replace>`): the router replaces the marked entry with the new page. The
  component then unmounts with the current entry not its own, so it does not go back.
- **A reload while open:** the state is gone, so the overlay is closed. The marked entry is left over, so a check
  run once on the first mount, and on every `popstate`, goes back from an entry marked by a token that no open
  overlay holds. Back after a reload then leaves the page instead of landing on the same page (§5, S3).
- **StrictMode** (`main.tsx` runs it): going back on close is deferred by a microtask and cancelled if the same
  overlay is still open by then. A double-run effect therefore neither drops nor duplicates the entry.

**Focus.**
- **Trapped:** Radix's modal focus scope, the bar's close button inside it.
- **On opening, below 768 px:** `onOpenAutoFocus` is prevented and the title takes the focus, so the keyboard does
  not open at once.
- **On opening, from 768 px:** the caller's `onOpenAutoFocus` if it gives one, else Radix's default (the first
  focusable control), as `Dialog` does.
- **The trigger:** the element focused when `open` turns true, read in a layout effect before Radix moves the focus.
  When that is `<body>`, it falls back to the control last pressed (a `pointerdown` seen in the capture phase). This
  covers Safari and iOS, where a tap does not focus a button (§5, S1).
- **On closing,** every way including Back: `onCloseAutoFocus` is prevented and the trigger is focused, if it is
  still in the page. After a link inside, the page is gone and nothing is focused by the overlay; the new page's
  `useMainFocus` places it.

**Busy** (`busy` on the root, as `ReportDialog` uses `submit.busy`): Escape and an outside press are prevented, the
close button is disabled, `onOpenChange(false)` from Radix is ignored, and Back re-adds the entry.

**`SignInPrompt`** becomes `AdaptiveDialog` + `AdaptiveDialogContent` with `closeLabel={words.close}`. The title,
line and the two links are unchanged. Each link becomes `<Link replace …>`. `useSignInPrompt` is unchanged. Escape,
the close button, the scrim and Back all call its `onClose`, which lets the held action go, as closing does today.
The links carry `?next=` as today, and `/login` and `/register` lie outside the site shell, so the held action
survives the round trip exactly as before.

**The showcase:** `AdaptiveDialogSection` in `sections/overlays/`, with one registry entry and samples in both
languages in `fixtures.json`. A button opens it, with a title, a line, enough body text to scroll on a phone, and a
two-button footer. The toolbar's width (360, 768 or 1280), theme and language show every combination. The preview's
iframe has its own history, which joins the window's, so Back closes the overlay there too.

## 5. Stronger decisions

- **S1. The focus returns to the trigger even where a tap does not focus it.**
  - What: an `activeElement` fallback to the last pressed control.
  - Why: on iOS Safari a tapped button does not take the focus, so "the element focused at opening" would be
    `<body>`, and VoiceOver users would land at the top of the page.
  - Cost: one capture-phase `pointerdown` listener, registered once by the layer.
  - **Recommended.** Today `SignInPrompt` loses the focus on every close: Radix returns it only to a Radix `Trigger`,
    and the heart is not one. This fixes it for the heart and the report link.
- **S2. Back is blocked while busy too.**
  - What: the prompt lists blocking for Escape, the button and the scrim, as `ReportDialog` does. Back would
    otherwise slip through while a sign-in (WI-C2) is in flight.
  - Cost: re-pushing an entry, which is invisible at the same address.
  - **Recommended.**
- **S3. No dead Back after a reload or a Forward.**
  - What: the prompt asks only that a reload shows the page closed. That alone leaves a marked entry, on which Back
    lands on the same page: the dead press the prompt forbids for links. The check of §4 goes back from a marked
    entry no open overlay holds.
  - Cost: about fifteen lines and one test. Forward into such an entry bounces back, which does no harm.
  - **Recommended.**
- **S4. StrictMode-safe history.**
  - Why: the app runs StrictMode in development, where the prototype's naive effect would push twice or close at
    once.
  - Cost: a microtask.
  - **Recommended.**
- **No rule of the documents is weakened.** The component lives in the layer, uses only semantic tokens and logical
  classes, has no words of its own (`closeLabel` is a prop), and imports nothing outside the layer. Arbitrary values
  (`env(safe-area-inset-*)`) appear only inside the layer, as `Sheet` already has them.

## 6. Related findings

There are no open findings about overlays, focus or history: the five open ones are 23, 65, 152, 215 and 221. None
is folded.
- `favorites.md` and `data-reports.md` were read for the guest's press: "the page asks them to sign in … with
  «إنشاء حساب» and «تسجيل الدخول» … closing the sign-in lets the held favourite go" stays true. They are not edited.
- If something is found during the work, it will be recorded as a finding numbered 230 or next (the prompt gives no
  range) and named in the report.

## 7. Files

New:
- `apps/web/src/shared/design-system/components/overlays/AdaptiveDialog/AdaptiveDialog.tsx`
- `…/AdaptiveDialog/historyEntry.ts`: the entry's push, back and stale check, and the last pressed control.
- `…/AdaptiveDialog/index.ts`
- `…/AdaptiveDialog/AdaptiveDialog.component.test.tsx`
- `apps/web/src/pages/showcase/sections/overlays/AdaptiveDialogSection.tsx`

Edited:
- `apps/web/src/shared/design-system/index.ts`: the export.
- `apps/web/src/shared/design-system/tokens/semantic.unit.test.ts`: one assertion that reduced motion sets both
  durations to 0 ms.
- `apps/web/src/pages/showcase/registry.tsx` and `fixtures.json` (ar and en).
- `apps/web/src/pages/site/public/SignInPrompt.tsx` and `SignInPrompt.component.test.tsx`.
- `docs/frontend/design-system/foundation.md`: §3's overlays row, and §12's `AdaptiveDialog` row, with `Dialog`'s
  row pointing to it for a task a phone gives the whole screen.
- `docs/frontend/architecture.md` §2: one bullet, "An overlay's history entry", beside the focus bullet. It is the
  one home: foundation's row links it.

Shared with another open item: none. WI-B must not run beside this item (both edit `foundation.md`), as the owner's
order already says. WI-C2 starts after this merges. There is no other layer and no licence.

## 8. Design issues

1. **The light Arabic phone capture** (`p1-signin-390-light-ar.png`) shows the close button at the left, the inline
   end in RTL. The dark Arabic capture and the prototype's code (`flex`, first child) put it at the right, the inline
   start, as the prompt says. I will build the inline start. The light capture looks stale.
2. **The picture's title is 26 px on a phone and 22 px wide**, written as raw sizes. On the scale, that becomes
   `heading-1` (24 px on a phone) and `heading-2` (22 px) from 768 px. Today's prompt title is `heading-3` (17 px),
   which reads small as the only heading of a full screen.
3. **The prototype hides the corner close button with CSS on a phone** and draws a second one in the bar: two buttons
   with the same name in the tree. Here exactly one close button is rendered, in the bar or in the corner, by width.
4. **The prototype loses the focus after Back** (its own note). This is fixed (§4, *Focus*).

## 9. Tests

All tests are in the component lane, except one unit assertion. Each is seen failing by the break named.
`stubScreenWidth` sets the width.

**`AdaptiveDialog.component.test.tsx`**

| # | Proves | Break that fails it |
|---|---|---|
| 1 | At 1280: a named, described dialog with no top bar, the close button in the corner (last, `absolute`), `md:max-w-120` | render the phone form at every width |
| 2 | At 390: full screen (`h-dvh`, `rounded-none`, `border-0`); the bar holds the close button first, `size-11`; the body scrolls (`overflow-y-auto`); safe-area classes on bar and body | drop the phone branch |
| 3 | At 390 the title takes the focus on opening. At 1280 the first control does, and a caller's `onOpenAutoFocus` is honoured | remove the title focus / ignore the caller's handler |
| 4 | At 390 the focus is trapped: Tab cycles from the bar's close button through the body and back | render the bar outside the Radix content |
| 5 | `it.each` closing by its button, Escape, the scrim, a done action (`open` false), and Back: it closes and the trigger has the focus | remove the `onCloseAutoFocus` override |
| 6 | Opening adds one entry at the same address (`history.length` + 1, same `location.href`, the earlier state's fields kept), and `history.back()` closes it with `onOpenChange(false)` | remove the `popstate` listener |
| 7 | Closing by its button, Escape or a done action restores the state from before it opened (the entry is gone back from) | remove the `back()` on close |
| 8 | An entry replaced while open (a link's replace), then unmount: the location stays | go back unconditionally on unmount |
| 9 | Busy: Escape and the scrim do nothing, the close button is disabled, and Back re-adds the entry and stays open; no longer busy, it closes | drop the busy guard in the `popstate` handler |
| 10 | A stale marked entry at mount (a reload) is gone back from | remove the stale check |
| 11 | Inside `<StrictMode>`, opening leaves it open with exactly one entry | go back synchronously in the cleanup |
| 12 | Reduced motion: the panel's classes time the slide by `--duration-medium` and `--easing-standard` | a fixed `duration-300` |
| 13 | A trigger that did not take the focus (a tap): the last pressed control gets it back | remove the fallback |
| 14 | axe at both widths | (the rules) |

**`semantic.unit.test.ts`:** reduced motion sets `--duration-short` and `--duration-medium` to 0 ms. Break: delete
the media block in `primitives.css`. This is existing code, reverted once.

**`SignInPrompt.component.test.tsx`:** the existing three tests are pinned to 1280 and stay green unchanged in their
assertions. New tests, with a browser router (`createBrowserRouter`, the window's history):

| # | Proves | Break that fails it |
|---|---|---|
| a | At 390, the prompt is the full-screen panel titled by the reason, the focus is on the title, and axe is clean | keep `Dialog` |
| b | Pressing «تسجيل الدخول» inside it lands on `/login?next=…`, and Back then returns to the space's page with no marked entry left | drop `replace` from the link |
| c | Back closes it, `onClose` is called once, the page component is the same node (still mounted), and the focus is on the trigger | no history entry |

The page tests (Space, Home, Directory, routes) render the phone form, since `startPreferences` answers `false`.
They must stay green unchanged. This is an executor check, run on the head.

**Executor checks** (unproven, by the plan rule):
- jsdom fires `popstate` on `history.back()` between same-document entries. If it does not, I stop and report; I
  will not dispatch it by hand.
- `createBrowserRouter` runs in jsdom for b and c.
- `slide-in-from-bottom-6` resolves on Tailwind's spacing scale in tw-animate-css.

## 10. Review Focus (inputs no planned test exercises)

- Real layout: `100dvh` with the phone's keyboard and address bar, the safe areas on a notched device, scrolling under
  the bar, and the slide itself (the Chrome pass covers 390 and 1440; a real notch and keyboard are not available).
- A width change while open (rotation): the form switches without remounting the children. This is reasoned, not
  tested.
- Two overlays open at once (one over another). No caller does that, and the entries would stack in order.
- A future `useBlocker` that blocks a move to the same pathname would turn the router's POP of delta 0 into
  `history.go(0)`, a reload. Today's only blocker compares pathnames. This is stated in architecture §2's bullet.
- iOS Safari's edge swipe: it is a `popstate` like Back. Untestable here.

## 11. Commits

Each commit has a body, a subject of 50 characters or fewer, and no attribution.
1. `feat(design-system): add the adaptive dialog`: the component (forms, focus, busy), the reduced-motion token
   assertion, the showcase section and samples, foundation §3 and §12, and tests 1–5, 9 (without Back), and 12–14.
2. `feat(design-system): close adaptive dialog on back`: `historyEntry.ts`, tests 5 (Back), 6–11, and architecture
   §2's bullet, with foundation's row linking it.
3. `feat(site): show sign-in prompt in adaptive dialog`: `SignInPrompt` on it with replacing links, and its tests
   a–c.

`#PRNUM` in the documents is replaced with the PR's number (expected #155; both the PR and the Issue lists will be
checked) just before the push.

## 12. Verification

Heavy commands go through `node C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs c1 …`, one at a time.
- On the head: `format:check`, `lint`, `typecheck`, `check:classes`, `check:links`, `check:conflicts`,
  `test:unit`, `test:component`, and `build` with `NODE_ENV=production`, then `check:build`.
- `test:api` is left to CI: there is no API change.
- **Chrome:** the API on 3320 and the web on 5320 against `masaha_dev`, as a guest on a space page. The heart is
  pressed at 390 and 1440, in Arabic and English, light and dark. I check the panel or dialog, Back, the close
  button, Escape, the focus back on the heart, and a link inside followed by Back, and run axe on each. The browser
  pane is shown before each layout or axe check. Shots go to `C:\Users\basel\Downloads\c1-shots\`, curated.
  Servers are stopped by PID and the ports checked free.
- A run killed for memory is retried once, then CI judges, and the report says so.
- Push, open the PR with `open-pr`, then wait for `gh pr checks` to be green on the pushed head and for `CLEAN`.
  Then `4_REPORT.md` with `final-report`.

## 13. Decisions needed from the owner

- **D1 — the width.** The prompt allows "a prop or a size step".
  - I recommend **one step, 30 rem** (the approved picture's), set in the component with no `size` prop yet. A prop
    whose second value no caller passes would be code only the showcase and the tests use (testing §3 rule 2). The
    first caller needing another width adds the prop.
  - The alternative is `size: 'md' | 'lg'` (28 and 30 rem), with `SignInPrompt` on `lg`.
- **D2 — the history API beside the router** (§4), rather than the router's navigation with state. Recommended for
  the three reasons given there.
- **D3 — S1 to S4** (§5): each recommended.
- **D4 — the title's sizes and the panel's paddings** from the picture, on the scale (§8, 2). Recommended.

## Proposed alternatives

None against the prompt's decisions. The breakpoint (768), the close button at the bar's inline start (the phone
conventions: Android's up/close and iOS's leading Cancel sit there), one same-address entry and the scope all hold
as written.
