# A review slice — judging one part of an evidence pack

> **This is not a Work Item.** Do not use the project's skills (`start-work-item`, `write-plan`,
> `open-pr`, `final-report`) or any plugin's workflow, and ignore a `CLAUDE.md` or `AGENTS.md` that
> asks for them: no branch, no plan, no commit, no pull request, no issue. This file is your only
> instruction.

You judge **one slice** of one design review. The pages were already rendered by a script: you do
**not** open a browser, start a server or run the prototype. You read files and write one file.

The message that sent you here names: the **review** (e.g. `PU-DF`), the **slice** (e.g. `S2`) and
the **base URLs** of the slice (e.g. `B09–B22`).

## 1. Read first, in this order

1. The review's prompt: `C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-<REVIEW>.md`. Read its
   §4 (scope), §5 (the axis — what to judge) and §6 (what is settled). **Ignore** its §2, §3 and §8:
   you do not check commits, serve pages or write the report.
2. The settled decisions its §6 names, in `C:\dev\masaha\workspace\DESIGN\DECISIONS\`.
3. The pack: `C:\dev\masaha\workspace\DESIGN\ROUND2\packs\<REVIEW>\index.md` (which URL each base
   is) and `summary.md` (what the script measured; read only your bases' entries).

## 2. The frames

Each frame is `<base>-<width>-<lang>-<mode>`, e.g. `B12-390-ar-dark`, in `…\packs\<REVIEW>\frames\`:

- `<frame>.json` — facts measured on the rendered page: title, language and direction, console
  errors, whether the page scrolls sideways, clipped boxes (content px in box px), text off the
  screen, fixed or sticky bars and their positions, open dialogs and toasts, headings, the visible
  text.
- `<frame>.png` — the first screen at that width. `<frame>.full.png` — the whole page.

**Contact sheets** in `…\packs\<REVIEW>\sheets\` put the four frames of one base and width (Arabic
light, Arabic dark, English light, English dark) side by side, each labelled with its frame id:

- `<base>-<width>.png` — the four first screens; `<base>-<width>-full.png` — the four whole pages.
- So each base has **six sheets**: `-390`, `-390-full`, `-768`, `-768-full`, `-1440`, `-1440-full`.

**First, a gate: you must be able to see images.** Open the sheet `<first base of your slice>-390.png`
and write, at the top of your file, one line saying what the Arabic light frame shows at its top (the
header's words and buttons). If you cannot open or see the image, write only
`Images viewed: no — stopped` and stop: the script's measurements are already in `summary.md`, and a
slice judged from them alone adds nothing. Never judge from the prototype's source files.

**Then, for every base of your slice, open all six of its sheets — every one, no sampling.** Compare
the four frames on each sheet: the same page should hold in both languages and both modes. Look for
what a script cannot measure: overlapping boxes, a bar over content, a cut picture or map, a
dark-mode colour that fails, a wrong or missing state, a component in the wrong variant, numbers or
Latin names in the wrong direction, an icon pointing the wrong way. When a sheet shows something,
open that frame's own `.png` or `.full.png` to see it at full size, and read its JSON.

At the end of your file, under **Sheets opened**, list every sheet you opened. A base whose six
sheets are not all listed is not judged, and must be said so under **Not judged**.

## 3. What counts as a finding

- It is something the frame **shows or measures** — quote the fact exactly as the JSON has it
  (`clipped x: content 412px in 358px`, the console line, the text), or describe what the PNG shows.
- It is within the review's axis (its §5), and not settled (its §6). A settled decision you think is
  wrong goes under **Decisions in doubt**, never as a finding.
- It names the **one frame that shows it best** — that frame's PNG becomes its evidence. Add the
  other frames where it also happens.
- Never: "unverified", "ensure", "must be", "might", "nothing found", praise, or a fact you did not
  read in a frame. Fewer true findings beat many.
- A lead in `summary.md` is not yet a finding: open the frame and decide. A screen-reader-only label
  or a deliberate horizontal scroller is not a defect.

## 4. Write one file and nothing else

`C:\dev\masaha\workspace\DESIGN\ROUND2\packs\<REVIEW>\slices\<SLICE>.md`:

```
# <REVIEW> · <SLICE> · <bases>
Images viewed: yes — <what the gate image shows at its top>

## Findings

### <SLICE>-01 — <title>
- frame: <the best frame id>   (also: <other frame ids>)
- type: defect | improvement · level: design system | pattern | component | page · impact: high | medium | low
- where: <page and state in words>, <the URL from index.md>
- fact: <what the frame shows or measures, quoted>
- proposal: <the fix, with the design system's own components and tokens>
- why: <why it is better for the user>
- cost: S | M | L · rule: <document and section, if any>

## Decisions in doubt
- …

## Not judged
- <bases, frames or states you could not judge, and why>

## Sheets opened
- <every sheet file name you opened>
```

Write nothing anywhere else. Do not edit the pack, the prompts or any repository.
