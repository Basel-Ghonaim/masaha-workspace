# Lane C report (IDENTITY, C8–C11)

(Saved by the lead from the lane's final message, 2026-11-12.)

## Summary
All four commits are on `lane/c`, in the order the brief gives. `git log --oneline 22ddac1c..lane/c` shows exactly those four and the tree is clean. Nothing was pushed or merged. I made no other branch and did not touch `apps/web/src`, `foundation.md`, `setup.md` or `CLAUDE.md`. No Chrome I started is still running.

**`lane/c` head: `df7c6ffb9c6cb5bab623c36039b215319eabd301`**

| # | sha | subject (length) | files |
|---|---|---|---|
| 1 | `45968c2bde0da51da7268b31ee7aa22570f3e857` | `feat(web): add the favicon and home-screen icon` (47) | `apps/web/index.html` (+7), `apps/web/public/favicon.svg` (new, 14 988 B, text, LF), `apps/web/public/favicon.ico` (new, binary, 2 112 B), `apps/web/public/apple-touch-icon.png` (new, binary, 3 264 B), `apps/web/scripts/browserIcons.unit.test.ts` (new, T13–T15) |
| 2 | `13b3e9b3a13c71f81cae99220a08ceba3383a1b2` | `feat(auth): draw the reset email in ink` (39) | `apps/api/src/modules/auth/email/resetEmail.ts`, `resetEmail.unit.test.ts` (T22) |
| 3 | `5011e7c2d250cbee886442440de097c3c3beef4d` | `docs(design): make berry the prototype's default` (48) | `docs/design/CHANGES.md`, `INDEX.md`, `SCREENS.md`, `prototype/Reset email.html`, `prototype/masaha/i18n.js`, `prototype/masaha/identity-ink-spark.css` |
| 4 | `df7c6ffb9c6cb5bab623c36039b215319eabd301` | `docs(findings): record the 404 bar and sea shots` (48) | `docs/architecture/findings/220-the-admins-top-bar-still-offers-to-hide-and-delete-a-space-found-deleted.md`, `221-the-readmes-screenshots-show-sea.md`, `README.md` (two lines appended under Open, after 219) |

Each commit has a body that says why. There is no `Co-Authored-By` or "generated with" anywhere (grep of the four bodies: 0).

## Tests: seen failing, then green
- **T13–T15** (`apps/web/scripts/browserIcons.unit.test.ts`, unit lane), run before `public/` existed: `Tests  5 failed (5)`. Red lines:
  - `Error: ENOENT: no such file or directory, open 'C:\dev\masaha\app-design-lane-c\apps\web\public\favicon.svg'`
  - the same for `apple-touch-icon.png` and `favicon.ico`
  - theme-color: `expected [] to deeply equal [...]` (`+ []`)
  - **Green after:** with `contentSecurityPolicy.unit.test.ts`, `Test Files  2 passed (2)`, `Tests  8 passed (8)`. The CSP test stays green, so the inline scripts' hashes hold.
- **T22** (`resetEmail.unit.test.ts`, API unit lane), run before the `resetEmail.ts` change: `Tests  3 failed | 6 passed (9)`. Red lines:
  - `AssertionError: expected Set{ '#f4fcfe', '#02787d', …(4) } to deeply equal Set{ '#f7fbff', '#ffffff', …(3) }`
  - `expected 'border-radius:8px;background:#02787d;' to contain 'background:#1a1f25;'`
  - `expected 'color:#02787d;' to contain 'color:#1a1f25;'`
  - **Green after:** `Tests  9 passed (9)`.
- **T24:** `check-parse.mjs` gives `52/52 blocks parsed, from 42 pages and the modules`. `check-classes.mjs` gives `361 classes used, 5 dead uses, 0 new` (exit 0).

## Breaks
Each break was made from a backup copy and restored by copy; each restored file was compared with its backup and was byte-identical. The script is `scratch-c\breaks.py`.
- **T13** (the SVG `<link>` dropped from `index.html`): `FAIL … index.html links the .ico, then the SVG, and the home-screen icon, each a file of public/`, `AssertionError: expected [ { rel: 'icon', …(2) }, …(1) ] to deeply equal [ { rel: 'icon', …(2) }, …(2) ]`. Restored.
- **T14** (the dark `@media` rule removed from `favicon.svg`): `FAIL … the SVG favicon draws ink #1a1f25 and spark #b55bb3, and #f7fbff and #d27ed0 under the browser's dark scheme`, `AssertionError: expected {} to deeply equal { ink: '#f7fbff', spark: '#d27ed0' }`. Restored.
- **T15** (a 32-only `.ico` copied over): `FAIL … the .ico holds 16, 32 and 48 px images in its directory, each a PNG of that size`, `AssertionError: expected [ { width: 32, height: 32, …(1) } ] to deeply equal [ …(3) ]`. Restored.
- **T22 Sea** (`ink: '#02787d'`): 3 failed. One red line: `expected Set{ '#f7fbff', '#02787d', …(4) } to deeply equal …`. Restored.
- **T22 underline removed:** `FAIL … writes its links in #1a1f25 ink, the one in the English text underlined`, `AssertionError: expected 'color:#1a1f25;' to contain 'text-decoration:underline;'`. Restored.

I ran the T13–T15 breaks twice: before and after a lint fix that only added types to the test helpers. All red both times.

## Rasters (EC9)
**How they were made.** `scratch-c\render.mjs` launches `chrome.exe --headless=new` on a random free port with `--user-data-dir=scratch-c\cdp-profile`, and drives it over CDP with Node 24's built-in `WebSocket`. It ran through the grant twice.
- Each image is an `<img>` of the SVG (as a `data:` URL) at its pixel size, in a viewport of exactly that size. The script asserts `innerWidth`, `innerHeight` and `devicePixelRatio === 1`.
- The background is set with `Emulation.setDefaultBackgroundColorOverride`: transparent for the `.ico` art, white for the 180 and the 120. Capture is `Page.captureScreenshot` as PNG.
- `scratch-c\pack.mjs` (about 30 lines) packs the `.ico`: ICONDIR 0/1/3, three entries (w, h, 0, 0, planes 1, 32 bits, size, offset), then the three PNGs.
- `favicon.svg` is written by `scratch-c\make_favicon.py` from `masaha-mark-berry.svg`. The script first checks that the source's structure is exactly the two clips, the two identical ink copies, the dots and the two transforms. The output has the words path once in `<defs>` and two `<use href="#w" class="ink">`.

**The files:**
- `.ico` entries: `masaha-app-icon-berry.svg` at 16, 32 and 48 px, RGBA PNG (463 / 697 / 898 B).
- `apple-touch-icon.png`: 180×180 RGB, the mark on white, full bleed.
  - It is rendered from `masaha-mark-berry.svg` on white.
  - I checked by text that the app icon file is the mark file plus the white `rx 170` rect, so this equals the app icon with `rx` 0.
- Google: `C:\dev\masaha\workspace\TASKS\IDENTITY\google\masaha-logo-120.png`, 120×120 RGB, 1 301 B. Not committed.

**What I saw:**
- **16 px:** still reads as the mark: a dark rounded "room" with two berry dots on its white rounded tile. The corners are transparent, and it is legible on both a light (#f1f3f4) and a dark (#202124) tab strip.
- **32 and 48 px:** crisp.
- **180:** square, full white, the mark centred.
- **120:**
  - Layout: the mark at 96 px, centred at (12, 12).
  - Measured: the mark's farthest drawn pixel is 47.5 px from the centre, and no non-white pixel lies at or beyond 56 px. So a round crop keeps about 12 px clear, dots included. A preview with the 60 px and 48 px circles drawn over it confirms this.
  - My first attempt sized the image by fraction (≈97 px at x 11.5). Chrome resampled it and left a light vertical seam where the mark's two mirrored halves meet. Re-rendered at whole pixels: the seam is gone. At 16, 32, 48, 64 and 180 px the seam falls on a pixel boundary, and none showed one.
- **`favicon.svg` against the owner's files:** at 64 px it renders pixel-identical (0 of 4096 pixels differ) to `masaha-mark-berry.svg`. Under `Emulation.setEmulatedMedia` `prefers-color-scheme: dark` it renders pixel-identical to `masaha-mark-dark-berry.svg`, so the switch works.
- The 32 px mark has two near-invisible anti-alias pixels under the ring. The owner's own file draws them the same.
- **Decoding:** Windows' WIC `IconBitmapDecoder` reads all three `.ico` frames (16, 32, 48; Bgra32; corner alpha 0). .NET Framework's `System.Drawing.Icon.ToBitmap` cannot read PNG frames ("Requested range extends past the end of the array"); that is a limit of that API, not of the file.

**Chrome stopped by PID:** 16576 on the first run and 13308 on the second, each with `taskkill /PID … /T /F`. `taskkill` printed errors for children that had already exited ("no running instance" / "operation not supported"). `tasklist` confirmed each parent was gone, and a final check found no `chrome.exe` with `cdp-profile` on its command line. **None is left.** The owner's own Chrome (27768) was never touched.

## Commands and results
Everything heavy went through `heavy.mjs lane-c`.
- **Grant waits:** memory under 4 GB twice: 11:10–11:14 UTC (two tries) and 11:18–11:22 UTC (two tries). No run was killed for memory and none needed a retry.
- **Lint (my files):** the T13–T15 test first failed `@typescript-eslint/no-unsafe-return` three times (`Object.fromEntries` returning `any`). I typed the helpers' tuples and it is clean. `resetEmail.ts` and its test are clean.
- **Typecheck:** commit 1 green (twice), commit 2 green, head green. Commits 3 and 4 touch no file that eslint or tsc reads (`docs/design/` is eslint-ignored, Markdown is not linted), and the head typecheck covers them.
- **Prettier (`--check` on my four TS/HTML files):** clean after one `--write` on each test file (line wrapping only).
- **`check:links`:** `3285 links in 220 documents and 2684 source files all resolve` after commit 3, and `3288 links in 222 documents …` after commit 4.
- **`check:conflicts`:** no markers.
- **i18n.js probe** (`scratch-c\i18n-probe.mjs`, runs the file in a node:vm stub page; not heavy):

| `?identity=` | `data-identity` | tab icon | carried on a link |
|---|---|---|---|
| none | `slate-berry` | `masaha-mark-berry.svg` / `masaha-mark-dark-berry.svg` | nothing |
| `slate-berry` | `slate-berry` | same as none | nothing |
| `bogus` | `slate-berry` | same as none | nothing |
| `sea` | none | `masaha/favicon.svg` unchanged | `?identity=sea` |
| `slate-coral` | `slate-coral` | `masaha-mark.svg` / `masaha-mark-dark.svg` | `?identity=slate-coral` |

A link that already names an identity keeps it, and `lang` and `theme` are still carried.

## The lead's document lines (foundation §16, after the «The source files» bullet), ready to paste
- **The browser's icons** (`apps/web/public/`, linked from `index.html`):
  - `favicon.svg`: the small mark with no background, in the light theme's ink and spark, and in the dark theme's by the browser's own scheme (the tab is the browser's, not the app's toggle).
  - `favicon.ico`: the app icon (the mark on its white tile) at 16, 32 and 48 px, for a browser that takes no SVG and for a dark tab bar.
  - `apple-touch-icon.png`: the mark on white at 180 px, full bleed, since iOS rounds the corners itself.

  The rasters are drawn from the source files in headless Chrome at device scale 1, and the `.ico` is packed from them. `theme-color` is each scheme's background. **A stated exception** to §2's *one layer, one place*: the browser draws these outside the page, where no token reaches, so they carry the identity's values as hexes. `apps/web/scripts/browserIcons.unit.test.ts` holds the links, the files, their sizes and those hexes by hand.
- **The reset email** draws no logo: its brand line is the word «مساحة» in the ink. **A stated exception** too: a mail client reads no token, so `resetEmail.ts` writes the ink and the neutrals inline, with no spark; its links are ink and the English one is underlined. A change of the brand or the neutrals is carried to it by hand ([finding 19](../../architecture/findings/19-the-reset-emails-colours-fonts-and-styles-are-written-outside-the-design-system.md)), and `resetEmail.unit.test.ts` holds its colour set.

## Decisions I took without the lead (what, why, undo)
1. **The 120 is the mark at 96 px, centred, on white.**
   - Why: whole pixels avoid the resampled seam, and 80 % of the circle keeps the dots clear of a round crop.
   - Undo: change `layout` in `render.mjs` and re-run it.
2. **The 180 comes from the mark file on white**, not from an edited app-icon file. It is the same picture as the app icon squared, and nothing had to be modified. Undo: render the app icon with `rx` 0 instead.
3. **A two-line HTML comment in `index.html`** above the new tags points to foundation §16. This goes beyond the brief's literal list.
   - Why: index.html explains its other blocks the same way, and the hexes there need a reason.
   - It does not touch the script hashes (CSP test green). Undo: delete the comment.
4. **Extra assertions in the tests:**
   - T13 checks the order of the links (`.ico`, then SVG, then touch icon); it matters to browsers that take the last supported icon.
   - T14 also checks that `favicon.svg` holds no colour but the four.
   - T22 also checks that both "link as text" paragraphs are ink.
   - Undo: drop those assertions.
5. **`resetEmail.ts`:**
   - `brand`/`onBrand` are renamed `ink`/`onInk` (plan §7.6).
   - Each `COLOR` entry carries a comment naming its neutral step and role. Undo: remove the comments.
6. **`i18n.js`:** an unknown `?identity=` now gives berry (it gave Sea before). `?identity=slate-berry` is still accepted, as the default, and is never carried.
7. **`INDEX.md`:** I changed only the `?identity=` row and kept the section heading «Identity trial — ink + spark (2026-11-11)». **`CHANGES.md`:** the new section has a «The documents» row naming the INDEX and SCREENS edits.
8. **Finding titles are in English**, so each file name is the heading's anchor. Finding 220 names the full paths of `SpaceEditorActions.tsx` and `useSpaceEditorActions.ts`, and of `useSpaceEditor.ts` and `useSpaceName.ts`, which read the 404 correctly. It describes the mechanism: TanStack Query keeps the last data beside the 404 error, and the actions hook only checks `query.data === undefined`.
9. **`favicon.svg` uses SVG 2's `href` on `<use>`**, not `xlink:href`.

## Behaved unexpectedly, or noticed and not changed (for the lead)
- The first 120 render had the seam described above (fixed). `taskkill /T` reported errors on children that had already exited; the parents were confirmed gone. System.Drawing cannot read the `.ico`'s PNG frames; WIC can.
- **Not changed (outside the brief), prototype tab icons:**
  - `Reset email.html` still links `masaha/favicon.svg`, Sea's «م» tile, because it loads no `i18n.js`, so its tab stays Sea.
  - `Wordmark.html` (historical) also stays Sea.
  - `Flows - states.html` and `Sign in - board.html` embed app pages in iframes, which now default to berry.
- **Not changed, reset email difference:** in the prototype the English part writes the link inline in a `<span>`; production writes it as its own `<p>`. This predates this item.
- **For EC8 / Review Focus:** with `sizes="16x16 32x32 48x48"` on the `.ico` link, whether Chrome picks the SVG over the `.ico` in a real tab is still to be checked against a served page. I ran no server, so I could not check it.

The scratch scripts, logs and previews are in `C:\dev\masaha\workspace\TASKS\IDENTITY\lanes\scratch-c\`: `render.mjs`, `pack.mjs`, `make_favicon.py`, `breaks.py`, `edit_*.py`, `write_findings.py`, `i18n-probe.mjs`, `out\*.png`, `break-*.log`, `render-run*.log`.
