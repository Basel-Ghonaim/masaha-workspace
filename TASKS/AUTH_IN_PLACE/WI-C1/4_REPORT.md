# WI-C1 — Report: `AdaptiveDialog`, and `SignInPrompt` on it

> Worker: Claude Code (Opus 5.5), main folder. Plan: `2_PLAN.md`, approved with D1–D4 and the supervisor's three
> notes (`2b_SUPERVISOR_REVIEW.md`). Status: **ready for review, not merged.**

## 1. The pull request and its head

- **PR #155**, `feat/adaptive-dialog` → `main`: https://github.com/Basel-Ghonaim/masaha/pull/155
- **Head:** `f2b8dff6abebb2a7f7bbd24024001e4851d60660`
- **CI** run 45409828163 on that head: all eleven checks pass (typecheck, lint, format:check, test:unit,
  test:component, test:api, check:classes, check:links, check:conflicts, build; CodeRabbit skipping).
- **GitHub:** `CLEAN`, `MERGEABLE`.

## 2. The commits

| SHA | Subject | What |
|---|---|---|
| `19adc7b1` | `feat(design-system): add the adaptive dialog` | The component (both forms, the focus rules, `busy`), `opener.ts` (S1), the reduced-motion token assertion, the showcase section (ar/en samples), foundation §3 and §12 |
| `012239dd` | `feat(design-system): close adaptive dialog on back` | `historyEntry.ts` (the entry, the step back, S2–S4), its tests, architecture §2 *An overlay's history entry*, and foundation's row linking it |
| `f2b8dff6` | `feat(site): show sign-in prompt in adaptive dialog` | `SignInPrompt` on it, both links with `replace`, and its new tests |

Each commit has a subject of 50 characters or fewer and a body. There is no attribution and no `fixup!`. `#PRNUM`
was replaced with `#155` in each commit's tree just before the push (filter-branch, two document lines). PR #155
got the expected number: the PR and Issue lists both ended at 154.

## 3. What was run

Every run was local, on the head before the number rewrite (which changed only two document lines). Heavy runs went
through `heavy.mjs c1`.

| Run | Result |
|---|---|
| `format:check` | ✔ |
| `lint` (whole repository) | ✔ |
| `typecheck` (all workspaces) | ✔ |
| `check:classes` | ✔ (2000 files) |
| `check:links` | ✔ (2801 links, 266 documents, 2701 sources) |
| `check:conflicts` | ✔ |
| `test:unit` | ✔: shared 29 files / 384 tests, API 77 / 924, web 196 / 1404 |
| `test:component` | ✔: 351 files / 2193 tests |
| `NODE_ENV=production npm run build` | ✔ (`apps/web/.env` sets development locally) |
| `check:build` | ✔: no showcase in the build, and nothing heavy or dashboard-only in the site's first download |
| Chrome (§5) | ✔ |

**Not run locally:** `test:api`, since the change touches no API code. CI ran it and it passed.

## 4. The breaks made (each test seen failing, then the code restored)

**`AdaptiveDialog.component.test.tsx`** (22 tests):

| Break | Tests that failed |
|---|---|
| Always the panel | the 1280 form; the 1280 focus / the caller's choice |
| Always the dialog | the 390 form; the slide on the tokens; the title focus; the trap |
| `duration-300` in place of the token | the slide on the tokens |
| No title focus | the title focus; the trap (which starts from the title) |
| The caller's `onOpenAutoFocus` ignored | the 1280 focus / the caller's choice |
| The bar's close rendered outside the Radix content | the 390 form; the trap; closing by its button; busy |
| No focus return (`onCloseAutoFocus`) | closing by Escape, its button, a done action and the scrim; the Safari fallback |
| No pressed-control fallback | the Safari fallback |
| No busy guard at the root | busy |
| No `popstate` listener | Back closes it; one entry; busy (Back); StrictMode |
| No step back on close | closed by its button, Escape or a done action leaves the entry (three cases); busy |
| An unconditional step back on unmount | a link's replaced entry is not gone back from |
| Back ignores busy | busy |
| No stale-entry check | the stale entry after a reload |
| A synchronous step back in the cleanup | StrictMode (after the fix in §6.3) |

**`semantic.unit.test.ts`:** with `--duration-medium: 0ms` removed from the reduced-motion block, "both durations
0 ms" failed.

**`SignInPrompt.component.test.tsx`** (7 tests, of which 4 are new):

| Break | Tests that failed |
|---|---|
| The old `Dialog` version | the phone panel; Back closes it (mounted page, focus) |
| `replace` dropped from «Sign in» | «Sign in» then Back |
| `replace` dropped from «Create account» | «Create account» then Back |

## 5. The Chrome pass

Headless Chrome over CDP, on `masaha_dev`, as a guest on `/spaces/pal-hub`. The run used device-metrics emulation,
so 390 is a true 390, and a foreground target, so frames run. The matrix was 390 and 1440, ar and en, light and dark
(eight combinations). Per combination:

- **Open at 390:** the panel at 390 × 844, radius 0, the bar shown. The 44 × 44 close is at the inline start: x = 338
  (the right) in Arabic, x = 8 in English. The focus is on the title (`H2.adaptive-dialog-title`). One entry is
  added at the same address.
- **Open at 1440:** a 480 px dialog with a 12 px radius, no bar, and the 32 px close in its corner. Radix's default
  focus lands on the close button, because Radix skips links when it chooses the first control (§7.2). One entry is
  added.
- **Closing:** Back, the close button and Escape each close it. No marked entry is left, the address and the scroll
  are unchanged, and the focus is back on the heart.
- **A link then Back:** «تسجيل الدخول» / «Sign in» leads to `/login?next=%2Fspaces%2Fpal-hub`. Back then lands on
  the space page at once, with no marked entry; the focus is on `main`, the page's own rule after a path change.
- **axe:** 0 violations on every open state and every page after it.

Beyond the matrix:

- **Reduced motion:** `animation-duration: 0s` with `prefers-reduced-motion: reduce`, and `0.25s` without.
- **A reload while open:** the page shows closed, the marked entry is stepped back from (no mark afterwards), and
  only one page load happens (§6.4).
- **Scroll kept across Back,** measured with «Report wrong information» lower on the page: at 390, y = 2498 before
  and after; at 1440, y = 1431 before and after. The focus returns to the report link, and the title is «Sign in to
  report information».

The servers were stopped by PID (the API's `tsx watch`, its server and `pino-pretty`, and Vite), and ports 3320 and
5320 were checked free. No headless Chrome was left running.

**Shots:** ten, curated, in `C:\Users\basel\Downloads\c1-shots\` (not in the repository):
- `390|1440 × ar|en × light|dark` with the prompt open;
- `390-en-light-report-open`;
- `1440-en-light-report-open`.

## 6. Problems met, and how each was solved

1. **`history.length` is a poor measure in jsdom.** Earlier tests leave forward entries, and a push prunes them, so
   "length + 1" failed. "Exactly one entry" is now proven by one Back landing on the page's own state.
2. **The busy guard was in two places.** Escape and outside presses were held in the content's handlers and again
   at the root, so a break of either one alone failed nothing. I kept the root guard, which sees every way of
   closing, and removed the duplicate. The break then failed the busy test.
3. **StrictMode.** The first version ran the stale-entry check between StrictMode's cleanup and its re-run. The
   check saw the dialog's own entry as stale and stepped back, closing the dialog. Moving the check after the
   entry's effect fixed it.

   Separately, the test for a synchronous step back passed at first. jsdom's `pushState` cancels a pending traversal
   (a real browser does not), and the stale check then repaired the double entry. The test now counts the moves: one
   Back must reach the page in exactly one move. The break fails it.
4. **The reload cost.** I feared that stepping back after a reload would load the page twice, since the earlier entry
   belongs to the unloaded document. Chrome showed a single load event, and no mark left.
5. **The Chrome script itself:**
   - My first selectors failed on two counts: the directory's card links, and a wait that returned a DOM node by
     value, which CDP refuses, so every check read as false. I fixed both: the slug comes from the API, and the
     waits use `!!(…)`.
   - The first, cold load of the space page also outlasted 15 s, so the wait is now 40 s.
6. **Memory.** The production build waited about 40 minutes for the grant: free memory sat at 3.0–4.1 GB after I
   started Docker Desktop, which had been down, for the database. I asked to stop Docker during the build; the
   permission was refused, so I waited. The grant came at 7 GB and the build passed. No run was killed.

## 7. Anything that behaved unexpectedly

1. **Docker Desktop was down at the start** (the database container had exited). I started it and the container,
   and left both running.
2. **From 768 px, the prompt opens on its close button,** not on «Create account». Radix's first-focus rule skips
   links, and the prompt holds only links. This is the layer's dialog behaviour that the prompt asked to keep as the
   default, and it was the same before this change (the old `Dialog`). WI-C2's form will hold fields, which Radix
   does focus.
3. **jsdom's `pushState` cancels a pending history traversal,** unlike browsers (§6.3). A test of history ordering in
   jsdom can pass for the wrong reason; counting `popstate` moves catches it.
4. **On the capture,** the earlier mismatch between the two Arabic phone shots is void, as the supervisor's note 1
   says. The build puts the close button at the inline start, as in the picture.

## 8. Decisions and departures from the prompt and plan

1. **D1:** one width, 30 rem (`sm:max-w-120`, in effect from 768), with no `size` prop.
2. **D2:** the history API beside the router.
3. **D3, S1–S4:** all built.
4. **D4:** the title on the scale (`heading-1` in the panel, `heading-2` from 768).
5. **The supervisor's notes:**
   - **Note 2:** the `pointerdown` listener is registered when the first `AdaptiveDialog` mounts (`listenForPresses`,
     once, kept), not on import.
   - **Note 3, my call:** I documented the limit rather than mounting a check in the app shell. A page that mounts no
     `AdaptiveDialog` keeps a marked entry after a reload: one Back lands on the same page. This is stated in
     architecture §2. The overlay's only pages (space, home, directory) always mount `SignInPrompt`, closed, so their
     reload is covered. A check in the app shell would add a layer mechanism to `app/` for a case no page has yet.
6. **Plan files:**
   - The plan named `historyEntry.ts` for both the entry and the pressed control. The pressed control went to its
     own `opener.ts`: two concerns, two small modules.
   - The plan listed an `AdaptiveDialogClose` part implicitly. It was not built, since no caller needs it (the
     showcase closes through state).
7. **Escape and outside presses while busy** are held once, at the root (`onOpenChange` ignored), rather than in
   the content's handlers too (§6.2).
8. **`busy` has no production caller yet.** The prompt requires it ("a caller may block closing while it is busy"),
   and WI-C2's sign-in is its first user. It is a requirement of this item, not code only a test uses.

## 9. The early conflict check

`gh pr list --state open` lists only #155, so there is no other open pull request to check against.

## 10. Left for WI-C2

- **The size:** the sign-in form goes inside `AdaptiveDialogContent`, already at the picture's 30 rem.
- **Busy:** pass `busy` while a request is in flight. Back is then held too.
- **Focus from 768:** the form's first field takes the focus by Radix's default. A caller wanting Google's button
  first passes `onOpenAutoFocus`.
- **Links leaving the overlay:** any new link from inside it that leaves the page (privacy is a new tab, per I7) must
  use `replace`, as `SignInPrompt`'s two do (architecture §2).
- **The «رجوع» in the top bar** (I15) for register or forgot is not in the shell. The bar holds only the close
  button today, so WI-C2 decides whether the bar takes a slot (a layer change) or the view puts «رجوع» above its
  title, as P2's captures do.
