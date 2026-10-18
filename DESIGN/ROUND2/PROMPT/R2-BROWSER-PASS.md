# R2-BROWSER-PASS — Round 2: the browser half of the reports written without a browser

## 1. Who you are and what you do

You are an independent design reviewer running inside OpenCode, read-only. Nine Round 2 reports were
written from the prototype's **source**, because their runner had no browser. You now have one: the MCP
server **`playwright`** (`browser_navigate`, `browser_resize`, `browser_take_screenshot`,
`browser_press_key`, `browser_evaluate`, `browser_snapshot`). **Use only those tools to see pages.** No
Python or npm package, no install, no curl, no reading HTML instead of looking.

You do **not** rewrite a report. For each one you **add a browser pass**: you check its existing issues on
the rendered page, you check what it said it could not check, and you append one section to it.

## 2. Where

- Read from `C:\Users\basel\masaha-design` (a detached worktree). First `git fetch origin`; check
  `git rev-parse HEAD` equals `git rev-parse origin/main`. If not, stop and say so. Never edit, commit,
  check out, install or move anything there.
- Serve the prototype on port **5490** (no other review uses it):
  `python -m http.server 5490 --bind 127.0.0.1 --directory docs/design/prototype`, run from
  `C:\Users\basel\masaha-design`, in the background. Pages: `http://127.0.0.1:5490/<Prototype URL>`, with
  the parameters exactly as `docs/design/INDEX.md` lists them.
- Screenshots: `browser_take_screenshot` with a **relative** filename `r2-shots/<PART-AXIS>/<ID>.png`
  (the server saves under `C:\Users\basel\Downloads`), e.g. `r2-shots/AD-VD/R2-AD-VD-003.png`.
- At the end: stop the server by its PID; check port 5490 answers nothing.

## 3. The reports, in this order (most visual first)

| # | Report (in `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\`) | Its prompt (scope, axis, widths) |
|---|---|---|
| 1 | `R2-AU-AX_REPORT.md` | `PROMPT\R2-AU-AX.md` |
| 2 | `R2-DK-AX_REPORT.md` | `PROMPT\R2-DK-AX.md` |
| 3 | `R2-AD-VD_REPORT.md` | `PROMPT\R2-AD-VD.md` |
| 4 | `R2-DK-VD_REPORT.md` | `PROMPT\R2-DK-VD.md` |
| 5 | `R2-OW-VD_REPORT.md` | `PROMPT\R2-OW-VD.md` |
| 6 | `R2-AD-DF_REPORT.md` | `PROMPT\R2-AD-DF.md` |
| 7 | `R2-AD-UX_REPORT.md` | `PROMPT\R2-AD-UX.md` |
| 8 | `R2-OW-UX_REPORT.md` | `PROMPT\R2-OW-UX.md` |
| 9 | `R2-PU-UX_REPORT.md` | `PROMPT\R2-PU-UX.md` |

**Resumable:** a report that already ends with a `## Browser pass` section is done — skip it. If this
conversation stops, the next one starts at the first report without that section.

## 4. For each report, in turn

1. Read the report whole, and from its prompt only §3 (how to open), §4 (scope: pages, INDEX sections,
   widths and modes) and §5 (its axis). Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b
   once, for the whole run.
2. **Each existing issue:** open its frame (the report's «where», or INDEX.md's URL) at its width and
   mode; look; take its screenshot as `<ID>.png`. Verdict: **confirmed** / **refuted** (the page does
   not show it) / **changed** (real, but not as written — say how).
3. **What the report said it could not check** (its "What was not reviewed" and every "not captured" /
   "no browser" line): check it now within the axis — the widths its prompt names (390, 768, 1440),
   English/LTR and dark where its prompt asks, and for AX the keyboard (`browser_press_key Tab`, then
   `browser_evaluate "() => document.activeElement.outerHTML.slice(0,200)"`) and contrast
   (`browser_evaluate` with `getComputedStyle`).
4. **New issues** only if real and inside the axis, at most **6** per report, in the report's own block
   format (§8 of its prompt), IDs continuing its numbering, each with its screenshot. Nothing already
   settled (the prompt's §6 decisions) and nothing another axis owns.
5. **Append**, at the end of the report file, one section — never edit what is above it:

   ```
   ## Browser pass (2026-10-17)
   Server: http://127.0.0.1:5490 · masaha-design at <sha> · tool: playwright MCP
   ### Existing issues
   - R2-XX-YY-001 — confirmed | refuted | changed: <one line> — r2-shots/XX-YY/R2-XX-YY-001.png
   ...
   ### Checked now
   - <width/mode/keyboard/contrast item>: <what was seen, one line>
   ### New issues
   <blocks, or "None.">
   ### Still not checked
   - <item>: <why>, or "Nothing."
   ```

6. Write the section **as soon as that report is done**, before opening the next one.

## 5. Keep the conversation small

- Prefer `browser_take_screenshot` (saved to a file) and a targeted `browser_evaluate` over
  `browser_snapshot`; take a snapshot only when a keyboard or an accessible name needs it, and never of a
  whole long page twice.
- Do not re-read a file you already read. One report at a time.

## 6. At the end

Stop the server; check the port. Reply with one line per report: done / skipped (already done) /
stopped (why), and the count of confirmed, refuted, changed and new issues.
