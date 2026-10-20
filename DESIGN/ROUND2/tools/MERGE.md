# Merging the slices into one review report

> **This is not a Work Item.** Do not use the project's skills (`start-work-item`, `write-plan`,
> `open-pr`, `final-report`) or any plugin's workflow, and ignore a `CLAUDE.md` or `AGENTS.md` that
> asks for them: no branch, no plan, no commit, no pull request, no issue. This file is your only
> instruction.

The message that sent you here names the **review** (e.g. `PU-DF`). Its slices were judged from an
evidence pack; you turn them into the review's report. You do not open a browser and you do not
judge pages again.

## 1. Read

1. The review's prompt `C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\R2-<REVIEW>.md`, its §8 (the
   report's shape) and §9 (the cap).
2. `C:\dev\masaha\workspace\DESIGN\ROUND2\packs\<REVIEW>\index.md` (the SHAs and the base URLs).
3. Every file in `…\packs\<REVIEW>\slices\`.

## 2. Write the report

`C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-<REVIEW>_REPORT.md`, in the prompt's §8 order:

1. **Commits:** HEAD and origin/main from `index.md`, and whether the design is identical.
2. **Verdict:** one line.
3. **The five most important points**, one line each.
4. **Issues**, most important first, at most the prompt's cap. Number them `R2-<REVIEW>-001`…
   Merge findings that are the same problem across slices into one issue (keep every frame).
   Each issue keeps the slice's fact, word for word, and its fields, and has this evidence line:
   `- **evidence:** `R2-<REVIEW>-<NNN>.png` (frame <frame id>)`
   — exactly that form: the script that copies the captures reads it.
5. **Decisions in doubt:** from the slices, merged.
6. **What was not reviewed, and why:** the slices' "Not judged", merged; and state that pages were
   rendered by script (`tools\r2-pack.mjs`) and judged from its captures and measured facts.

Do not add a finding that no slice has. Do not drop a slice's finding without saying why under
section 6. Write nothing else.

## 3. Copy the captures

Run, and paste its last line in your reply:

```
node C:\dev\masaha\workspace\DESIGN\ROUND2\tools\r2-finalize.mjs <REVIEW>
```
