# Watch the round-2 design reviews until they finish (for Copilot, in auto mode)

You are the **monitor** of a batch job the owner left running on this laptop. Your only job: keep it
going until it finishes, fixing what stops it, and write down what you did. **You review nothing and
change nothing in any project.**

## The job

- 40 review prompts and 7 summary prompts in `D:\masahaWorkspace\DESIGN\ROUND2\PROMPT\`.
  Each review writes `ROUND2\REPORT\<ID>_REPORT.md`; the summaries write `ROUND2\SUMMARY\…`. The job is
  **done when `ROUND2\SUMMARY\R2-ALL_SUMMARY.md` exists.**
- They run through **`ROUND2\run-queue.ps1`** (read it first): it starts every missing review with
  `opencode run`, three at a time, then the summaries. When a model answers "Rate limit exceeded" (the
  refusal is written to `%USERPROFILE%\.local\share\opencode\log\opencode.log`, not to the run's log),
  it switches to the next model in its `-Models` list; a run that ends or passes 45 minutes without its
  report is retried. Each run's output is in `ROUND2\LOGS\`. The free OpenCode models have limits:
  **each model has its own**, and one at its limit refuses at once.

## What you do

1. **Start or find the queue.** The owner may already have started it from an open PowerShell window
   (then its command line does not name the script): **if any `opencode` process is running, the
   queue is running — leave it.** Only if no `opencode` process runs and no report has appeared for 10
   minutes, start it in a new window:
   `Start-Process powershell -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','D:\masahaWorkspace\DESIGN\ROUND2\run-queue.ps1'`
2. **Every 10 minutes** (`Start-Sleep -Seconds 600`), check: how many reports and summaries exist; when
   the newest was written; how many `opencode` processes run; the last lines of `opencode.log` with
   "Rate limit" (which models, when).
3. **When to act:**
   - **The queue stopped** (no `run-queue.ps1` process) and the job is not done → test which models
     answer now: for each of `opencode models opencode` (skip any name with `flash` or `lightning`
     unless nothing else works), run `opencode run -m <model> "Reply with the single word OK."` with a
     60-second limit, and check `opencode.log` for a new "Rate limit" on that model. Restart the queue
     with the working ones first:
     `… -File …\run-queue.ps1 -Models <model1>,<model2>,…` (comma-separated, no spaces). If none works,
     wait 30 minutes and test again.
   - **No new report for 60 minutes while the queue runs** → stop the queue's `powershell` process and
     every `opencode` process, then do the same as above.
   - **A run's log shows an error you can fix by running it again** → leave it: the queue retries.
4. **If OpenCode cannot run at all for 90 minutes** (every model refuses or fails, tested twice, 30
   minutes apart): stop the queue and every `opencode` process, and **run the missing reviews
   yourself, one at a time**: for each missing ID, read `ROUND2\PROMPT\<ID>.md` whole and follow it
   exactly as its reviewer would (read-only, its own port, its report at its path), and write
   `Reviewer: Copilot (fallback — OpenCode unavailable)` as the report's first line. Then the part
   summaries, then the summary across all, the same way. Do not hand the work to another tool.
   If OpenCode answers again meanwhile, go back to the queue for what is still missing.
5. **Stop** when `R2-ALL_SUMMARY.md` exists, or after **10 hours**, whichever comes first.

## Never

- Never edit, move or delete any file under `ROUND2\PROMPT\`, `ROUND2\REPORT\`, `ROUND2\SUMMARY\`, the
  scripts, or anything in `C:\Users\basel\masaha*` (the project's folders). Never run git, npm, tests,
  Docker or database commands. Never write a review or a summary yourself, except under step 4.
- Never start more than one queue at a time. Never run more than three `opencode` reviews at once.
- Never print or open a `.env` file or anything holding a secret.

## Your log

Append to `D:\masahaWorkspace\DESIGN\ROUND2\MONITOR_LOG.md` (create it): at every check, one
line — the time, reports and summaries counted, `opencode` processes, the model in use; and every
action you took, with why. At the end, one line saying whether the job finished.
