# WI-C1 — an overlay that is a dialog on wide screens and a full-screen panel on a phone

You are a **Claude Code worker** on **Masaha**, a bilingual Arabic RTL / English platform for coworking spaces in Gaza.
This is a fresh session, **Opus 5.5, effort high**, started in **`C:\dev\masaha\app`**. `main` is at `e0f9f66a` (ADR 0021 merged, #154), clean and
**live in production**: every merge deploys. No other worker is running in `app`.

**Read first, they are binding:**
- `C:\dev\masaha\workspace\TASKS\AUTH_IN_PLACE\0_OWNER_DECISIONS.md` — the owner's decisions;
- `C:\dev\masaha\workspace\TASKS\AUTH_IN_PLACE\1_ANALYSIS.md` — §0, §1, **I7, I9, I15** (this Work Item), and I2 / I4 for
  context (the rest is WI-C2's);
- ADR 0021 in the repository (`docs/architecture/decisions/0021-sign-in-where-the-action-is.md`).

**The picture to build is approved:** masaha-prototype's `Space details.html?v=inplace`
(`https://github.com/Basel-Ghonaim/masaha-prototype`, `prototype/variants/Space details/inplace.jsx` + `.css`,
described in `decisions/Space details.md`), captures in `C:\dev\masaha\workspace\DESIGN\AUTH\inplace-P1\`. Its form is
WI-C2's; **this Work Item takes only its shell**: the dialog from 768 px, the full-screen panel below it with its top
bar and close button, the slide, Back closing it. Its berry button is WI-B's: **not here**.

Follow the project's skills `start-work-item`, `write-plan`, `open-pr` and `final-report`. **Plan, save it to
`TASKS\AUTH_IN_PLACE\WI-C1\2_PLAN.md`, and stop for the owner's approval.** The supervisor launched you while the owner
is away: do not wait inside plan mode for an answer — write the plan file, say in the conversation that it is saved,
and stop. The approval comes later as a message in this same session. After the approval, work to the end without
stopping. Report: `4_REPORT.md` beside it.

## Hard limits

- Web and docs only: no API code, schema, migration, new dependency or database write. No secret printed.
- Touch only what this Work Item needs. Stage by path, never `git add -A` or `git add .`. No drive-by refactoring;
  record anything else you find as a finding or in the report.
- The design system's rules hold: the new component lives in `apps/web/src/shared/design-system/`, semantic tokens
  only, logical classes only, every user-facing string through the copy catalogue in both languages.
- Never weaken a test. No production code only a test uses. Break the code each new or changed test guards once, see
  it fail, restore.
- Commits: Conventional, **subject ≤ 50 characters, with a body**; no tool attribution; no `fixup!` left. `#PRNUM` in
  documents, replaced just before the push (expect **#155**; Issues share the numbers, so check both lists).
- Never push to `main`, never merge, never force-push a branch that is not yours.
- Heavy commands (lint, typecheck, build, a test lane, headless Chrome) through the grant script from the repository
  root: `node C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs c1 <command…>`. **A run killed for memory:
  retry once, then CI judges,** and say so. If the memory guard stops your servers, restart them once at ≥ 4 GB free;
  if that fails, skip the Chrome pass and say so in the report and the PR's Evidence.

## 1. Read

- `CLAUDE.md`, `docs/development/workflow.md`, `docs/development/testing.md`, `docs/architecture/documentation.md`.
- `docs/frontend/design-system/foundation.md`: §3 (the layer's structure), §9 (breakpoints), the motion tokens, and
  §12's rows for `Dialog`, `Sheet`, `AlertDialog`.
- `docs/frontend/architecture.md` §2 (routing, landing and guards) and its focus rules (`useMainFocus`).
- The layer's `components/overlays/Dialog/` and `Sheet/` with their tests; the showcase's overlay section.
- `apps/web/src/pages/site/public/SignInPrompt.tsx`, `useSignInPrompt.tsx`, `SignInPrompt.component.test.tsx`;
  `features/favorites/hooks/useFavoriteToggle.ts`; `features/data-reports/…/useReportAction.ts`;
  `shared/routing/guest/heldIntent.ts` and `guestLeaving.ts` (what counts as leaving a page).
- `docs/features/favorites.md` and `data-reports.md` where they describe a guest's press.

## 2. The work

1. **The component** (its name is yours to propose in the plan, saying what it is; one component, built on the
   layer's Radix primitives, not a second dialog system):
   - **From 768 px:** the layer's dialog, centred, its width a prop or a size step (the sign-in will need more than
     today's `sm:max-w-md`), the close button in its corner as today.
   - **Below 768 px:** a full-screen panel (`100dvh`, no radius, no border), a **top bar** that stays while the body
     scrolls, holding the close button (a 44 px target, at the bar's inline start — the prototype's place), the
     body scrolling under it; safe-area insets top and bottom; it slides up with `--duration-medium` and
     `--easing-standard`, and appears at once under reduced motion.
   - **Back closes it** (I15): opening adds **one history entry at the same address** (no new URL, ADR 0021 point 3);
     the browser's or the phone's Back closes it and the page stays mounted, scrolled where it was; closing it any
     other way (its button, Escape, the scrim, a done action) removes that entry, so Back afterwards leaves the page
     as it would have; **following a link inside it replaces that entry**, so no dead Back press is left behind; a
     reload while it is open shows the page with it closed. Work out with the data router (`react-router` 8) whether
     this is the router's own navigation with state or the history API beside it, and say why in the plan.
   - **Focus:** trapped while open; on a phone it goes to the title (so the keyboard does not open at once), from
     768 px the caller may choose (default: the layer's dialog behaviour); **on every way of closing, Back
     included, it returns to the trigger** (the prototype loses it after Back: do not copy that).
   - A caller may block closing while it is busy (as `ReportDialog` does today).
   - In the showcase, both widths, light and dark, Arabic and English.
2. **`SignInPrompt` moves onto it,** its content unchanged (the reason's title and line, «إنشاء حساب», «تسجيل
   الدخول»). This is the component's first real use: on a phone the guest's prompt becomes the full-screen panel.
   Its two links leave through the "replace" rule above; the held favourite / report keeps working exactly as today
   (the round trip through the pages is WI-C2's to remove, not yours).
3. **Tests** (component lane): the dialog from 768 and the panel below it (the width stubbed); Back closes it and
   leaves the page; closing by the button removes the history entry; a link inside replaces it; focus returns to
   the trigger on each way of closing; reduced motion; blocked while busy. `SignInPrompt`'s tests stay green and
   gain the phone case.
4. **Documents:** foundation §12 (the new component's row, and `Dialog`'s / `Sheet`'s rows if they now point to it);
   `docs/frontend/architecture.md` where an overlay's history entry belongs (one home); `favorites.md` /
   `data-reports.md` only if what they say of the guest's prompt is now wrong. Keep one home per fact; claim only
   what is built.

## 3. Verify, open the PR, report

1. **Branch:** after `git fetch`, with a clean status: `git switch --no-track -c feat/adaptive-overlay origin/main`
   (rename it if your component's name suggests a better one).
2. **Local verification on the head:** `npm run format:check`, `lint`, `typecheck`, `check:classes`, `check:links`,
   `check:conflicts`, `test:unit`, `test:component`, a production build (`NODE_ENV=production`, since `apps/web/.env`
   sets development), then `check:build`. `test:api` is left to CI (no API code changes).
3. **Chrome, real behaviour:** with the API (3320) and web (5320) on `masaha_dev`, as a guest on a space page: press
   the heart at 390 and 1440, Arabic and English, light and dark; check the panel / dialog, Back, the close button,
   Escape, the focus back on the heart, a link inside then Back; run axe on each (expect no violation). Show the
   browser pane before any layout or axe check (a hidden pane runs no frames). Stop your servers by PID and check
   the ports are free. Shots to `C:\Users\basel\Downloads\c1-shots\`, curated, never in the repository.
4. **Push and open the PR** with `open-pr`. Wait until `gh pr checks <n>` is all green on the pushed head and GitHub
   says `CLEAN`.
5. **Report** with `final-report` to `4_REPORT.md`: PR number and full head sha, the commits, each requirement above
   with its test and the break you saw fail, the Chrome results, what ran locally and what CI judged, your decisions,
   anything left for WI-C2.

**Then stop. Never merge.**

## Proposed alternatives

If you think a decision here is wrong (the breakpoint, the bar's close position, the history entry, the scope), say
so in the plan's "Proposed alternatives" section, with the reason. Do not build an alternative before the owner's
answer.
