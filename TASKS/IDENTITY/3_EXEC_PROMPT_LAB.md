# IDENTITY — the palette lab (OpenCode worker, prototype only, new files only)

You are a worker on **Masaha**, a bilingual (Arabic RTL / English) directory of coworking spaces in Gaza. The owner
wants to choose a new colour identity by eye, on real screens, with one click per palette, in light and dark at once.
You build a **palette lab** page inside the design prototype. Everything you need is in this prompt; read it whole.

## 0. Where and how

- Worktree: `C:\dev\masaha\app-b` (detached at `origin/main`). `git fetch origin && git switch --detach origin/main`,
  then `git switch -c design/palette-lab`.
- **New files only.** You create exactly these, and edit **no existing file** (another worker is editing the
  prototype at the same time in another worktree):
  - `docs/design/prototype/Palette lab.html`
  - `docs/design/prototype/masaha/palette-lab.js` (plain JavaScript, no JSX, no React needed)
- **Hard limits:** no PR, **no push**, no merge, nothing on `main`, no test lane, no build, no lint, no `npm ci`, no
  file outside the two above. No tool attribution anywhere (no `Co-Authored-By`, no "generated with").
- Commits: Conventional Commits, subject ≤ 50 characters, a body saying what and why, staged by explicit path. For
  example `feat(design): add a palette lab to the prototype`, then one commit per later step if useful.
- Checks before every commit, from the worktree root: `node docs/design/scripts/check-parse.mjs` and
  `node docs/design/scripts/check-classes.mjs`. Both must pass. Read `docs/design/README.md` first (the prototype's
  rules: shared global scope per page, no object rest, the prebuilt CSS bundle).
- Serve on its own port, so it never clashes with the other worker: `cd docs/design/prototype && npx serve -l 5401 .`

## 1. How the colours work (facts — rely on them)

- The design-system bundle `docs/design/prototype/_ds/masaha-design-system-*/_ds_bundle.css` defines primitive ramps
  as CSS variables: `--brand-50` … `--brand-950` and `--neutral-50` … `--neutral-950` (steps 50, 100, 200 … 900, 950),
  plus `--green-*`, `--amber-*`, `--red-*`, `--blue-*` (status ramps, **not changed** by the lab), and `white`.
- The semantic tokens reference the ramps, e.g. `--background: var(--neutral-50)`, `--primary: var(--brand-600)` in
  light and `--background: var(--neutral-950)`, `--primary: var(--brand-400)` under dark. So setting the 22 ramp
  variables as **inline style on a page's `<html>` element** restyles that page in either theme.
- A prototype page takes its theme and language from the URL: `?theme=dark`, `?lang=en`
  (`masaha/i18n.js` sets `document.documentElement.dataset.theme`). Pages must be served over HTTP (not `file://`).
- The current palette, *Sea* (foundation §4, locked today):

  | Ramp | 50 | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900 | 950 |
  |---|---|---|---|---|---|---|---|---|---|---|---|
  | brand | #EAFBFC | #D5F4F5 | #B3E6E8 | #85D0D4 | #50B3B8 | #15959B | #02787D | #096165 | #05494C | #023235 | #001D1F |
  | neutral | #F4FCFE | #EAF5F7 | #DBE6E9 | #C7D1D4 | #9DA7A9 | #747E80 | #5C6567 | #464F51 | #2A3234 | #182022 | #0C1315 |
  | green | #ECFCEF | #D9F5DF | #BAE8C5 | #90D3A2 | #63B77C | #39995B | #137D41 | #026732 | #034D25 | #013517 | #001F0A |
  | amber | #FFF5EA | #FFE9CF | #FBD3A2 | #EEB56C | #D6912B | #B27406 | #905C01 | #754B04 | #593700 | #3E2500 | #261400 |
  | red | #FEF4F3 | #FDE7E4 | #FFCDC8 | #FEA69E | #FC6E68 | #DE4544 | #BE222A | #A20419 | #7C0110 | #580007 | #370003 |
  | blue | #F1F8FE | #E0EFFF | #C0DEFF | #90C6FE | #64A6E9 | #3E87CE | #1F6CB0 | #075796 | #004174 | #002C52 | #001934 |

- The semantic mapping (foundation §5; `b` brand, `n` neutral, `g` green, `a` amber, `r` red, `i` blue), light / dark:

  | Role | Light | Dark |
  |---|---|---|
  | background / foreground | n-50 / n-900 | n-950 / n-50 |
  | card / card-foreground | white / n-900 | n-900 / n-50 |
  | muted / muted-foreground | n-100 / n-600 | n-800 / n-400 |
  | border | n-200 | n-800 |
  | input | n-500 | n-500 |
  | ring | b-500 | b-400 |
  | primary / primary-foreground | b-600 / white | b-400 / b-950 |
  | secondary / secondary-foreground | n-100 / n-900 | n-800 / n-100 |
  | accent / accent-foreground | b-50 / b-800 | b-900 / b-100 |
  | destructive / -foreground | r-600 / white | r-400 / r-950 |
  | success / -foreground | g-600 / white | g-400 / g-950 |
  | warning / -foreground | a-500 / a-950 | a-400 / a-950 |
  | info / -foreground | i-600 / white | i-400 / i-950 |
  | destructive-subtle / -fg | r-50 / r-800 | r-950 / r-200 |
  | success-subtle / -fg | g-50 / g-800 | g-950 / g-200 |
  | warning-subtle / -fg | a-50 / a-800 | a-950 / a-200 |
  | info-subtle / -fg | i-50 / i-800 | i-950 / i-200 |
  | sidebar / sidebar-foreground | white / n-700 | n-900 / n-300 |
  | sidebar-accent / -fg | b-50 / b-800 | n-800 / n-50 |
  | chart-1 … chart-5 | b-600 · i-600 · a-500 · g-500 · n-500 | b-400 · i-400 · a-400 · g-400 · n-500 |

- **The contrast rule** (foundation §5, "Verified"): every `-foreground` on its surface; `muted-foreground`, `primary`,
  `destructive`, `success` and `info` as text on `background`, `card` and `muted`; `foreground` and
  `muted-foreground` on `accent` — all **≥ 4.5:1** in both themes. `input`, `ring`, every `chart-*` and the status fills
  (`destructive`, `success`, `warning`, `info`) **≥ 3:1** against `background` and `card`. WCAG 2 relative-luminance
  contrast.

## 2. What to build

### 2.1 The palettes

A palette is a `brand` ramp and a `neutral` ramp (11 steps each). Build them in **OKLCH** (write the sRGB ↔ OKLCH
conversion yourself, a few dozen lines; no library):

- **Lightness follows Sea:** for each step, take the OKLCH lightness of Sea's same step (brand from Sea's brand,
  neutral from Sea's neutral). This keeps the contrast close to today's verified values.
- **Hue and chroma come from the palette's seed**, with chroma following the shape of Sea's ramp (highest around
  500–700, low at the ends), and clamped into the sRGB gamut (reduce chroma until the colour fits).
- Neutrals are low-chroma (a cast, not a colour): a hue and a peak chroma of about 0.005–0.02.

Palettes (brand seed / neutral hue + feel):

1. **Sea (current)** — the exact table above, not generated. The baseline.
2. **Clay & stone (recommended)** — brand seed `#B4532A` (terracotta); neutrals warm sand/stone (hue ≈ 70, chroma
   ≈ 0.012); dark theme reads charcoal-brown.
3. **Olive & ink** — brand seed `#5F6F2A` (olive); neutrals ink (hue ≈ 260, chroma ≈ 0.012).
4. **Sea sunset** — brand seed `#C2492F` (sunset coral); neutrals blue-grey (hue ≈ 230, chroma ≈ 0.012).
5. **Indigo & sand** — brand seed `#3D4FA8`; neutrals warm sand (hue ≈ 75, chroma ≈ 0.01).
6. **Sage & clay** — brand seed `#3F6B57` (deep sage); neutrals warm (hue ≈ 60, chroma ≈ 0.01).
7. **Free colour** — a colour input for the brand seed and a hue slider + chroma slider for the neutrals; the ramps
   build live from them.

Keep the palette list as one data array at the top of `palette-lab.js`, so the main supervisor can add or tune one
without reading the rest.

### 2.2 The page

`Palette lab.html`: Arabic RTL by default, lab chrome in Arabic with English in parentheses where useful. The chrome may
use classes already in the bundle and a small `<style>` block in this page **for the lab's own chrome only**, written
with the semantic variables (no raw colours in the chrome). Layout:

- **Top bar:** one button per palette (its name and a small swatch strip of brand 600 + neutral 50/900), the active
  one marked; a theme switch with three states: **light**, **dark**, **both side by side** (default); a screen picker.
- **Screens:** real prototype pages in `<iframe>`s (same origin, so the lab can reach `contentDocument`):
  `Home.html`, `Directory.html`, `Space details.html` (its default space), `Desk.html?role=reception`,
  `Owner overview.html`. Show one screen at a time at 1440 wide scaled to fit (CSS `transform: scale`), or a "phone"
  toggle at 390. In "both", the same screen twice: `?theme=light`-less URL and `?theme=dark`.
- **Applying a palette:** set the 22 ramp variables as inline style on each iframe's `document.documentElement`
  (`style.setProperty('--brand-600', …)`), on the iframe's `load` event too, so navigating inside an iframe keeps the
  palette. Sea clears them (back to the bundle's own values).
- **Ramps panel:** the two ramps of the active palette as 11 swatches each with their hex.
- **Contrast panel:** every pair of §1's rule, computed for the active palette in both themes, with its ratio and
  ✓/✗; a summary at the top («كل الشروط متحققة» or the number failing). Status ramps stay Sea's, but their pairs are
  re-checked on the new neutrals.
- **Hue-clash warning:** when the brand-600's OKLCH hue is within 25° of green-600, amber-500, red-600 or blue-600,
  say which status it may be confused with (a warning, not a block).
- **Copy values:** a button that copies the active palette's two ramps as a Markdown table row in the format of the
  Sea table above (brand row, neutral row) — the record the owner's choice will go into.
- **URL state:** `?palette=clay&theme=both&screen=home&device=desktop` (and the free colour's values), so a link
  reopens the same view.

## 3. Run, stop once

1. Write a short plan (≤ 30 lines) to `C:\dev\masaha\workspace\TASKS\IDENTITY\2_PLAN_LAB.md`; do not wait for approval.
2. Build, run both checks, open the lab in a browser and click through every palette, theme and screen. Fix what
   breaks. Commit.
3. Screenshots into `C:\Users\basel\Downloads\palette-lab-shots\` (never into the repository): each palette on Home in
   "both", and the contrast panel for Clay & stone.
4. **Stop once.** Print for the owner: the branch and `git log --oneline origin/main..HEAD`, the serve command, the lab
   URL (`http://localhost:5401/Palette%20lab.html`), and a ready URL per palette. Then wait.
5. The owner's notes come in this same session (new palettes, tuned seeds, layout). For each round:
   `git branch backup/palette-lab-<n>` first, fix, `git commit --fixup=<the commit it belongs to>`, then
   `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main`; both checks; print the URLs again; wait.
6. When the owner says it is done: write `C:\dev\masaha\workspace\TASKS\IDENTITY\4_REPORT_LAB.md` — head sha, commits,
   `git diff --stat origin/main`, the checks' output, each palette's contrast summary (pass / which pairs fail), and
   the "copy values" output for every palette.
