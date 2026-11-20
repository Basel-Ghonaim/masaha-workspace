# Masaha logo — working notes (with the owner)

Decisions per axis of HANDOFF_LOGO.md §5, as they are settled. The image-tool prompt is assembled from them.

## Axis 1 — the idea (settled 2026-10-25)

**Decision (owner):** one mark fusing three meanings: a **location pin**, the letter **«م»** and a **work desk**.

**Risks raised and accepted, with their mitigations:**
- Three shapes blur at 16 px → the three are fused into **one continuous silhouette**, not placed side by side; a
  **simplified small version** (pin + «م», desk line dropped) is used at 16–32 px.
- A pin looks like the directory map's status-coloured pins → the mark must **not** be a symmetric standard map
  marker: the «م» tail makes it asymmetric, and it is never green, amber or red.

**Prompt text (idea part, draft):**

```text
Concept: a single-line logo mark that fuses three meanings into ONE silhouette:
1) a location pin, 2) the Arabic letter Meem (م), 3) a work desk.
The head of the pin is the head of the Meem: a soft rounded square loop.
The point of the pin is the Meem's descending tail.
The tail lands on a short horizontal line that reads as a desk surface.
It must read as one connected shape, never as three icons placed together.
Not a standard symmetric map marker. No house, no laptop, no Wi-Fi arcs,
no letter inside a filled square tile, no dots.
Also give a simplified version for 16–32 px: pin + Meem only, desk line removed.
```

### Axis 1 reopened (2026-11-02)

The tool results did not satisfy the owner, and the «م» is **no longer required** (it is only the name's initial and
means nothing on its own). The product's meanings to carry: finding the right place, places open now, the place's
location near you, workspaces. The owner chose **idea A, "the room-pin"**: a rounded square (the workspace) with a
pin's point (the location) and a door (open now); search is left to the product itself. Claude now drafts the mark
directly as SVG in `drafts/` (the image-tool prompt in LOGO_PROMPT.md is on hold).

Drafts round 1 (`drafts/preview.html`, `drafts/preview.png`): a1 dropped by Claude's own check (a gap in a square
reads as the letter C); b1 square pin with an outlined door; b2 square pin with a solid door; b3 diamond pin with a
solid door.

## Axis 2 — the form (settled 2026-10-26)

**Decision (owner, 1b 2c 3a 4a):**
- **Lockups:** the mark alone (favicon, collapsed sidebar), a horizontal lockup (mark beside the word) and a
  stacked one (mark above the word: social avatar, door sign, receipt).
- **Drawing style:** a geometric **thick monoline**: one stroke weight, about 1/8 of the mark's width, rounded ends.
- **Geometry:** soft rounded corners on a square grid; the mark fits a square.
- **Two languages:** one mark, two words («مساحة», "Masaha"). The mark sits right of the Arabic word and left of
  the English one; it is **never mirrored** (it is an Arabic letter). A bilingual lockup only if wanted, for print.

The image tool makes **the mark only**; the words and lockups are set later with the real font in a design tool.

**Prompt text (form part, draft):**

```text
Style: geometric monoline mark with ONE thick stroke weight
(about 1/8 of the mark's width), rounded stroke ends, soft rounded corners,
built on a square grid and fitting inside a square.
Calm, practical, trustworthy. Not playful, not decorative, not calligraphic.
The mark alone: no text, no letters other than the Meem shape itself.
```

## Axis 3 — the colour (settled 2026-11-01)

**Decision (owner, 1a 2a 3a):**
- **One colour** for the mark and the word together: `#02787d` (brand-600) on light, `#50b3b8` (brand-400) on dark
  (brand-950), white on a teal background, black for print. Never green, amber or red in any version.
- **The tool draws in solid black on white**; the exact colours are applied afterwards in the design tool.
- **Favicon:** the mark with no background, switching between the two shades with the light/dark scheme. The phone
  home-screen icon needs a background: a teal mark on white — **never** a white mark in a teal tile (it would
  look like the spaces' letter tiles).

**Prompt text (colour part, draft):**

```text
Colour: solid black on a plain white background. Flat. No gradients, no shadows,
no texture, no 3D, no glow, no mock-up scene.
```

## Axis 4 — the wordmark's typography (settled 2026-11-01)

Not part of the image-tool prompt: the words are set with the real font in the design tool.

**Decision (owner, 1b 2a 3a 4a):**
- **Arabic word:** IBM Plex Sans Arabic, converted to outlines, letter spacing adjusted, **no kashida**, every
  letter as the font draws it. The word's «م» stays plain: the mark already is a «م», and echoing it in the word
  would read as «م» twice.
- **Weight:** 600, to match the mark's thick stroke; one step lighter only if, beside the mark, the word looks
  heavier than the stroke.
- **Latin word:** "Masaha" (capital first letter), IBM Plex Sans, same weight.
- **Proportion:** the mark is as tall as the Arabic word (top of the alif to the bottom of the letters); the Latin
  word is matched to look the same size, by eye rather than by number; a fixed gap between mark and word, set in
  the rules of use.

## Axis 5 — the tools and the method (settled 2026-11-01)

**Decision (owner):**
- **Tools:** Recraft first (native vector output); ChatGPT's image tool second, with the **same prompt**, as a check
  that the idea is clear rather than invented by one tool. Midjourney not used.
- **The tool's result is a reference:** the mark is redrawn in Figma on a square grid with one stroke weight, the
  stroke outlined before export. A tool's own SVG is kept only if it is truly clean.
- **Rounds:** round 1 runs the prompt several times (about ten variants) and keeps two or three; round 2 reruns it
  describing what to keep, to refine rather than replace. Every kept variant is checked at 16 and 32 px. The
  "what do you see?" test with 3–5 people from the audience is optional.
- **Clean SVG checklist** (into LOGO_DECISION.md): exported from Figma, passed through SVGOMG; no embedded image; no
  live text (all letters outlined); one fill colour (the code swaps it for a semantic token); a square viewBox for
  the mark; about 1–2 KB for the mark.

**Prompt text (method part, draft):**

```text
Show several distinctly different variations of this same concept in each run.
```

## Axis 6 — the deliverables (settled 2026-11-01)

**Decision (owner):**
- **Source files:** one **black** SVG per element, eight in all: the mark, the small mark, the Arabic word, the
  English word, and a horizontal and a stacked lockup per language. The code colours them with semantic tokens;
  coloured print versions are exported from Figma when needed.
- **Favicon set, made by the owner in Figma:** PNGs at 16, 32 and 48 px joined into one `.ico` with a free
  converter, a 180 px PNG for the phone home screen (teal mark on white), and an SVG favicon that switches with the
  light/dark scheme. The build Work Item stays code-only, with no new dependency.
- **Rules of use:** written by Claude in LOGO_DECISION.md; the owner adjusts them once the real logo exists.
- **Where and names:** `C:\dev\masaha\workspace\TASKS\LOGO\final\`, fixed English names starting with `masaha-`.

All six axes are settled. The full prompt is in LOGO_PROMPT.md; the decision file is LOGO_DECISION.md.

## Round 2 — the mark in ink + spark (2026-11-11)

Plan: `LOGO_PLAN_R2.md` (the owner said "start drawing"; L1 (a) room ink + door spark and L2 b1/b2/b4 taken as the
plan's recommendations, open to change). The name stays **provisional**: «مساحة / Masaha» is a placeholder in the
lockups; the mark does not depend on it. Drafts: `drafts/round2/preview.html` (served on 5403 from the supervisor's
session) and `preview.png` (full page), `preview-top.png`.

- **b1** — the door's outline makes the pin's point (spark outline). Reads as a door; at large sizes it can read as a
  pen nib.
- **b2** — an outlined room-pin with a solid spark door standing on its floor (door widened to 12 of 48 units).
- **b4** — a solid room-pin with the door cut out; in two colours the door is filled with spark.

Measured (WCAG, graphics need 3:1): ink on its grounds 16–18:1 in both identities. Spark door on the ground (b1,
b2): coral 3.91 light / 9.99 dark, berry 3.95 / 6.84 — pass. **b4's spark door on the ink room fails in dark**
(coral 1.81, berry 2.65): in dark the room is near-white and the pale spark disappears; b4 would need a cut-out
door (no spark) in dark, or b4 is dropped.

## The symbol dropped (2026-11-11)

The owner closed the symbol idea (rounds 1–2, the room-pin): the logo becomes the **wordmark "Masaha"**. Plan:
`LOGO_PLAN_WORDMARK.md`. The drafts in `drafts/` stay as history.

## Wordmark round 1 — ten black drafts (2026-11-11)

The owner asked to analyse Oyoun Academy's logo, extract its principles and make **10 different first drafts, no
colour**. Analysis: `wordmark/ANALYSIS_OYOUN.md` (principles only; nothing copied). Sheet: `wordmark/round1.html` and
`round1.png` (each draft large, at 24 px and at 16 px):
1 geometric lowercase (Jost) · 2 wide-tracked capitals (DM Sans) · 3 capitals with open A's, drawn thin · 4
"masaha." heavy lowercase with a full stop (Manrope) · 5 heavy capitals, the M's right stem is the first A's left leg
(drawn) · 6 heavy oblique "Masaha" (Plus Jakarta Sans) · 7 friendly "Masaha" (Sora) · 8 tight rounded lowercase
(Lexend) · 9 heavy capitals cut by one band of negative space (Outfit) · 10 monoline lowercase built from circles
and lines (drawn). Fonts load from Google Fonts by link; nothing downloaded.

## Arabic-first bilingual (2026-11-11)

The owner sent Oyoun Media's official logo (`reference/oyoun-media-logo.png`: the Arabic «عيون» in custom geometric
lettering as the hero, "OYOUN" small beneath) and approved the direction: **«مساحة» is the hero, "MASAHA" small
beneath** — W1 of `LOGO_PLAN_WORDMARK.md` is reversed. Browser-tool prompt: `wordmark/PROMPT_BROWSER_AGENTS.md`
(ChatGPT, Ideogram, Recraft, Gemini); results go to `wordmark/external/`. The Arabic of every kept idea is redrawn
by hand as SVG.

## Browser-tool round A — rejected (2026-11-11)

Four sheets from the browser tools (`wordmark/external/round-a-01…04`): the owner liked none — "a normal word in a
font; where is the creative touch?". Diagnosis: the prompt asked for restraint and geometry only, so the tools set
the word in stock-looking geometric Kufi; nothing tells a story. Oyoun's mark works because it has a **construction
idea**, not a style. Next: **concept first** — an idea tied to «مساحة»'s meaning, chosen with the owner, then drawn.
(Also seen: one result spelled «قساحة» — the tools' Arabic is unreliable, as expected.)

## Round B — the room module (2026-11-11)

The owner's own one-line request to ChatGPT ("redraw Oyoun's logo with مساحة, same creativity") beat every
principle-based prompt: a **construction system** is what the owner calls creativity. Its result was a blind copy
(Oyoun's circles and the four status colours), so the supervisor's prompt gave the same boldness a module of
Masaha's own — **a rounded-square ring (a room)**, ink letters, two coral dots on the ة as two people. ChatGPT's six
(`external/round-b-chatgpt.webp`): the owner likes **#6** (the bracket under MASAHA) but "it needs something more".
Seen in it: the ح closes into a ring (reads as a ه), the س has two teeth, stray outline seams where letters meet.

Redrawn by hand: `wordmark/round2-rooms.html` / `.png` — #6 cleaned (ح open, س three teeth, «مسا» and «حة» joined,
one stroke, no seams) and three additions: (2) the bracket grows into an open-topped room the word sits in, (3) the
م's head is a room with a lit (spark) window — "open now", (4) both. Light and dark, large, 150 px and 96 px.

## Round C — ChatGPT's corrected #6, chosen: draft 1 (2026-11-11)

The owner asked ChatGPT to keep #6 and fix only the spelling (ح open, س with three teeth): four results
(`final-trace/chatgpt-sheet-round-c.webp`); **the owner chose draft 1**. Traced to SVG by the supervisor (potrace
2.1.8, npm, in the scratchpad; an ink mask and a coral mask traced apart), faithful to the drawing:
`final-trace/masaha-logo-traced.svg` (ink `#151F2C` + coral `#D2573D`), `-dark.svg` (`#F7FBFF` + `#FEA793`),
`-mono.svg` (black); previews `preview-sizes.png`, comparison `_compare.png`, large detail `_big.png`.
**Limit:** the source is ChatGPT's ~660 px image, so at large sizes the traced edges wobble, straight lines are not
straight and "MASAHA" is rough. Good enough to review; not yet production-clean.

## The logo traced clean (2026-11-11)

The owner brought ChatGPT's draft 1 at 2000 × 668 (`final-trace/chatgpt-large.webp`); upscaled to 3000 px
(`large-3000.png`) and re-traced (potrace, ink and coral apart), cropped to its content (viewBox `263 45 2473 903`):
**`final-trace/masaha-logo.svg`** (ink `#151F2C` + coral `#D2573D`), **`masaha-logo-dark.svg`** (`#F7FBFF` +
`#FEA793`), **`masaha-logo-mono.svg`** (black); ~14 KB each. Edges and straight lines now clean at large sizes
(`preview-final.png`). The small-traced first attempt was deleted. Still open: the small mark (favicon), "MASAHA"
possibly reset in a real font, the colour identity (coral vs berry) to confirm, `LOGO_DECISION.md`.

## The small mark (2026-11-11)

Cut from the traced logo, not redrawn: the ة's ring (outer x 287–871, y 263–742 in the trace) with its two coral
dots. The ring's left half is mirrored about x 579, because its bottom-right corner is hidden under the ح in the
word; the dots (centred at 590.5) are moved 11.5 units to sit on the ring's centre. Files in `final-trace/`:
`masaha-mark.svg`, `-dark.svg`, `-mono.svg`, and `masaha-app-icon.svg` (on a white rounded tile, for the phone
home screen). Preview at 200 / 64 / 32 / 16 px, in a browser tab and as an app icon: `preview-mark.png`. Reads at
16 px as "a room with two people".
