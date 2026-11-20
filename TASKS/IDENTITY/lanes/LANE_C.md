# IDENTITY — lane C: outside the web's source (C8, C9, C10, C11)

You are **lane C**, a sub-agent of the IDENTITY item's lead, on **Masaha** (a bilingual Arabic RTL / English web
platform for coworking spaces in Gaza; a monorepo: `apps/web` React + Vite, `apps/api` Express + Prisma, a design
archive in `docs/design/`). The lead built the shared layer: the ink + berry tokens (ADR 0019) and the `Logo`. You
build four commits that live outside `apps/web/src`, in your own worktree, and **return your report as your final
message**. You run in the background: you cannot ask the lead a question and wait. **Decide and record:** a choice
the plan does not settle — take the safest option, build it, record it (what, why, undo).

## 1. Where you work

- **Folder:** `C:\dev\masaha\app-design-lane-c` (a git worktree). **Branch:** `lane/c`, cut by the lead at the shared
  layer's head `22ddac1c`. Every command starts with `cd /c/dev/masaha/app-design-lane-c && …` (Bash) and every file
  tool takes an absolute path inside this folder (or your scratch folder). Never touch any other folder: not
  `C:\dev\masaha\app-design` (the lead's), `app-design-lane-a` / `-b`, `C:\dev\masaha\app` or
  `C:\dev\masaha\app-pr143`.
- The worktree is installed (`npm ci`, `packages/shared` built) and has its `.env` files. Never print them. **Never**
  run `npm ci` / `npm install`, `git clean`, or delete `node_modules`.
- **No server, no `test:api`, no database, no build.** No push, no merge, no branch but `lane/c`.
- **Your scratch folder:** `C:\dev\masaha\workspace\TASKS\IDENTITY\lanes\scratch-c\` — your render and pack scripts,
  your Chrome profile, the rasters before they are copied in. Write long edits as Python scripts there (heredocs with
  quotes fail to parse; tools turn `\u` escapes into literal characters). Open files with `newline=''`.

## 2. Read first

1. `CLAUDE.md` (in your folder), `docs/development/workflow.md` §3 (*Commits*) and §8, `docs/development/testing.md`
   §3 (rules 5–7).
2. **The plan:** `C:\dev\masaha\workspace\TASKS\IDENTITY\2_PLAN_PROD.md` — §1, §2, §4 (the logo's rules), §5.2's
   resolved hexes, §6 (*Rules of the documents this item bends*), **§7.5 (the icons), §7.6 (the e-mail), §7.7 (the
   prototype)**, §8 (the README's finding — its number is **221** now, see commit 4), §9 D2, D3, D4, §10 T13–T15, T22, T24, §12 EC8,
   EC9, §15 commits 8–11, §16 (Google's steps, for the 120 px PNG).
3. The logo files (the owner's, read only): `docs/design/prototype/masaha/logo/masaha-mark-berry.svg` (the mark),
   `masaha-app-icon-berry.svg` (the mark on a white `rx 170` tile), `masaha-logo-berry.svg`.
4. `apps/web/index.html`, `apps/web/scripts/contentSecurityPolicy.unit.test.ts`, `vercel.json` (read: the CSP and
   the SPA rewrite), `apps/api/src/modules/auth/email/resetEmail.ts` and its test, the findings index
   `docs/architecture/findings/README.md` and one recent finding as a model (e.g. 218), `docs/design/README.md`
   (*Rules for implementing*), `docs/design/CHANGES.md`, `INDEX.md`, `SCREENS.md`, `docs/design/prototype/masaha/i18n.js`
   and `identity-ink-spark.css`.

## 3. Your commits (on `lane/c`, in this order)

Subjects exactly as below (≤ 50 characters), each with a body that says **why**:

1. **`feat(web): add the favicon and home-screen icon`** — `apps/web/public/` (new; Vite copies it to `dist/` as is):
   - `favicon.svg` — the berry mark (the words path defined once in `<defs>`, two `<use>`; the clip rectangles and
     transforms of `masaha-mark-berry.svg`), classes `.ink` / `.spark` filled `#1a1f25` / `#b55bb3`, and
     `@media (prefers-color-scheme: dark)` `#f7fbff` / `#d27ed0`. No background (the owner's "no background").
   - `favicon.ico` — 16, 32 and 48 px PNG entries of the app-icon art (the mark on its white rounded tile, transparent
     outside the tile; D3).
   - `apple-touch-icon.png` — 180 × 180, the mark on white, **full bleed** (the tile squared; D2).
   - `apps/web/index.html`, after the stylesheet link: `<link rel="icon" href="/favicon.ico" sizes="16x16 32x32
     48x48" />`, `<link rel="icon" href="/favicon.svg" type="image/svg+xml" />`, `<link rel="apple-touch-icon"
     href="/apple-touch-icon.png" />`, `<meta name="theme-color" content="#f7fbff" media="(prefers-color-scheme:
     light)" />`, `<meta name="theme-color" content="#0d1217" media="(prefers-color-scheme: dark)" />`. The inline
     scripts are untouched, so their CSP hashes hold (`contentSecurityPolicy.unit.test.ts` stays green: run it).
   - T13–T15 in `apps/web/scripts/browserIcons.unit.test.ts` (new). *Body:* none before; how they were made; why the
     hexes live there (images the browser draws outside the page cannot read a token).
2. **`feat(auth): draw the reset email in ink`** — `resetEmail.ts`'s `COLOR` (§7.6): `page` `#f7fbff`, `card`
   `#ffffff`, `border` `#dde5ed`, `ink` `#1a1f25` (the brand line «مساحة», the button's fill, the links), `onInk`
   `#ffffff`, `text` `#1a1f25` (kept apart from `ink`: same value, another meaning), `muted` `#5e646a`; the English
   inline link gets `text-decoration:underline`; the link written as text is ink. The comment names ADR 0019's
   values and finding 19. No spark, no image. T22. *Body:* finding 19's "carried by hand".
3. **`docs(design): make berry the prototype's default`** — §7.7 (OD5 (a)): `masaha/i18n.js` (no `?identity=` gives
   `slate-berry`; `?identity=sea` gives today's bundle, no `data-identity`; `slate-coral` unchanged; links carry
   `identity` only when it is not the default; the tab's icon follows as now), `identity-ink-spark.css`'s header
   comment (production now takes berry, ADR 0019; Sea is `?identity=sea`), `Reset email.html`'s inline hexes to
   §7.6's, `CHANGES.md` (a section «Berry, the default (2026-11-12)»), `INDEX.md`'s `?identity=` row, `SCREENS.md`'s
   line on `Wordmark.html` (option A superseded by the logo, foundation §16). Checks: `node
   docs/design/scripts/check-parse.mjs` and `node docs/design/scripts/check-classes.mjs` (T24). *Body:* the design
   source matches production; Sea and coral stay to compare.
4. **`docs(findings): record the 404 bar and sea shots`** — **two** findings, the next two free numbers (the lead
   checked on `main` `f58c12a8`: 219 is the last, so **220** and **221**), each a file in
   `docs/architecture/findings/` in the model's format and a line in the index (append-only, in order):
   - **220 — first:** #143's fix-round offer: "On the admin's 404 page the top bar still offers «إخفاء عن الزوار»
     and «حذف المساحة» for the space just found deleted". The cause as #143's report gives it: `SpaceEditorActions`
     reads the space query, whose earlier data stays after the 404 (source:
     `C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\4_REPORT_C.md` › *Fix round* §6). Read
     `apps/web/src/features/spaces/components/editor/SpaceEditorActions.tsx` and its hook (read only, never edit)
     so the finding names the files and the mechanism exactly; say what is seen, why, and the direction of a fix,
     not the fix itself. Status *Open*.
   - **221 — second:** the README's screenshots (`docs/assets/readme/*.webp`, `masaha.gif`) show Sea; resolved when
     they are re-shot under ink + berry, in a README task. Status *Open*.
   *Body:* the two observations recorded, not fixed (workflow §4).

**Rules:** the prototype's CSS is a specification, never copied into `apps/web/src`; you do not touch `apps/web/src`
at all, nor `foundation.md`, `setup.md`, `CLAUDE.md` (§5); public text never names hosting providers, free plans or
session durations; no drive-by changes — anything else wrong you notice: record it in your report.

## 4. The rasters (OD4 (a); EC9) — rendered in headless Chrome, packed by a script

- A Node script in your scratch folder drives `C:\Program Files\Google\Chrome\Application\chrome.exe --headless=new
  --remote-debugging-port=<a random free port> --user-data-dir=<scratch-c>\cdp-profile` over CDP with Node 24's
  built-in `WebSocket` (no dependency). **Run it through the grant** (a Chrome batch is heavy):
  `node C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs lane-c node <your script>`. At its end, stop the
  Chrome it started **by its PID** (never another Chrome), and say in the report that none is left.
- Each image: the SVG drawn at its pixel size (an `<img>` of the file at `width`/`height` in a page whose viewport is
  exactly that size, `Emulation.setDeviceMetricsOverride` at device scale 1), the background set with
  `Emulation.setDefaultBackgroundColorOverride` — transparent (`a: 0`) for the `.ico` art, white for 180 and 120 —
  and `Page.captureScreenshot` (PNG).
  - `.ico` art: `masaha-app-icon-berry.svg` at 16, 32, 48.
  - 180: the mark on white, full bleed (`masaha-mark-berry.svg` on white, or the app icon with its tile's `rx` 0).
  - **120 for Google** (D4): the mark on white **with clear space all round**, so a round crop never cuts the dots;
    to `C:\dev\masaha\workspace\TASKS\IDENTITY\google\masaha-logo-120.png` — **never committed**.
- The `.ico` packed by a ~30-line Node script in your scratch folder: ICONDIR (reserved 0, type 1, count 3), three
  16-byte ICONDIRENTRYs (width, height, 0 colours, 0, planes 1, 32 bits, the PNG's size, its offset), then the three
  PNGs.
- **Look at each** (the Read tool shows an image): the 16 px still reads as the mark, the 180 is square and full, the
  120 has its margin. Say what you saw.
- Only the three files enter the repository; the scripts and intermediate PNGs stay in your scratch folder.

## 5. Tests — each seen failing first, each break made

| Test | File · lane | Proves | Seen failing |
|---|---|---|---|
| T13 | `apps/web/scripts/browserIcons.unit.test.ts` · unit | `index.html` links `/favicon.ico`, `/favicon.svg` (`image/svg+xml`), `/apple-touch-icon.png`, each present in `public/`; `theme-color` `#f7fbff` light, `#0d1217` dark | before `public/` exists |
| T14 | same | `favicon.svg` fills ink `#1a1f25` / spark `#b55bb3`, and `#f7fbff` / `#d27ed0` under `prefers-color-scheme: dark` | same |
| T15 | same | `apple-touch-icon.png` is 180 × 180 (its PNG header); `favicon.ico` holds 16, 32 and 48 entries (its directory) | same |
| T22 | `apps/api/src/modules/auth/email/resetEmail.unit.test.ts` · unit (api) | the HTML's colours are exactly {`#f7fbff`, `#ffffff`, `#dde5ed`, `#1a1f25`, `#5e646a`}; the button cell `background:#1a1f25` with a `#ffffff` label; the English link underlined | before C9's change |
| T24 | the prototype's `check-parse.mjs`, `check-classes.mjs` | the prototype's pages still parse and pass | n/a |

- Expectations by hand (the hexes written in the test, never read from the tokens); each title says what it proves.
- **Breaks**, each from a backup copy, restored by copy, the red line copied into the report: T13 — a link dropped
  from `index.html`; T14 — the dark rule removed from `favicon.svg`; T15 — a 32-only `.ico` (or a 192 px touch icon);
  T22 — a Sea hex left (`#02787d`); the underline removed.
- Also run `apps/web/scripts/contentSecurityPolicy.unit.test.ts` after the `index.html` change (green).

## 6. Documents — what is yours, what is the lead's

- Yours, in your commits: the prototype's documents (`CHANGES.md`, `INDEX.md`, `SCREENS.md`) and finding 220 with
  its index line.
- **The lead's** (write the exact text in your report, with its section): foundation §16's lines on the browser's
  icons (C8: the three files, how they were made, `theme-color`; the stated exception — images outside the page
  carry the identity's hexes, held by T13–T15) and on the e-mail (C9: the stated exception, finding 19, held by T22).

## 7. Commands — every heavy one through the grant script

The grant: `node C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs lane-c <command…>` (it waits for a slot
and ≥ 4 GB free; it may wait minutes — let it; never bypass it). Heavy = lint, typecheck, any test run, a Chrome
batch.
- Typecheck: `node …/heavy.mjs lane-c npm run typecheck`
- Lint, **your files only:** `node …/heavy.mjs lane-c npx eslint <your files…>`
- Web unit tests, your files: `node …/heavy.mjs lane-c npx vitest run --project unit <files…> --root apps/web`;
  the API's: `node …/heavy.mjs lane-c npx vitest run --project unit <file> --root apps/api`.
- The prototype's checks: `node …/heavy.mjs lane-c node docs/design/scripts/check-parse.mjs` (and `check-classes`).
- Light, no grant: `npx prettier --check <your files>` (and `--write` on them only; Markdown is excluded by the
  project's Prettier config — keep its line style by hand); `npm run check:links` after the documents.
- **A run killed for memory** (exit 137, a signal, "JavaScript heap out of memory"): retry once; killed again — record
  it and carry on; the lead's full run and CI judge.
- **Every commit lints and typechecks on its own.**

## 8. Committing

- `git status` before each commit; stage **by path** (never `git add -A` / `git add .`); binary files staged by path
  too; no tool attribution, no `Co-Authored-By`, no "generated with" anywhere.
- A fix to an earlier commit folds into it (`git commit --fixup <sha>`, then
  `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash 22ddac1c`), after `git branch backup/lane-c-<n>` first.
- At the end: `git log --oneline 22ddac1c..lane/c` shows exactly your four commits, the tree clean.

## 9. Limits

No merge; no push; no migration; no dependency; no database; never `db:seed`; never weaken, skip or delete a test,
a check or a lane to pass; no production code only a test uses; never stop on file count — report it; nothing
outside your folder but your scratch folder and the Google PNG's path.

## 10. Your report = your final message

The harness refuses a sub-agent's report file: return it as text; the lead saves it as `lanes\REPORT_C.md`.
- `lane/c`'s head (full sha) and each commit: sha, subject (length), files (binary sizes too).
- Per test: the red line (copied) before its code, the green line after; per break: the red line and "restored".
- The rasters: how made, the sizes, what you saw (EC9); the Chrome stopped by PID.
- The commands run and their results, any wait or kill.
- **The lead's document lines** of §6, ready to paste.
- Every decision you took without the lead (what, why, undo), and anything that behaved unexpectedly.
