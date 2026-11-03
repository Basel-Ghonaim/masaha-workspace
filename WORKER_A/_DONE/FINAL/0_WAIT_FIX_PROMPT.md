# FINAL — worker A's fix round on #132: wait for the fix-round prompt, then run it

You are **worker A's fix-round executor** for #132 (`feat/final`), in `C:\dev\masaha\app`, in a fresh conversation.
The last review is still running; the supervisor will gather every review's findings and write your prompt. **The
owner is away; do not wait for him.**

1. **Do nothing else first:** no reading of the repository, no branch change, no install. Note `git -C
   C:\dev\masaha\app status -sb` (expected: `feat/final`, clean, at `origin/feat/final`) for your report.
2. **Start the waiting script in the background** (it polls every 2 minutes, up to 6 hours):
   `bash /c/dev/masaha/workspace/WORKER_A/FINAL/scripts/wait_fix_ready.sh 6` — with `run_in_background`, so you are
   woken when it exits. Do not poll its output yourself, and do not sleep. (The old `READY` file in that folder is the
   first run's; ignore it — yours is `FIX_READY`.)
3. **When it prints `READY`:** read `C:\dev\masaha\workspace\WORKER_A\FINAL\7_FIX_ROUND.md` whole and **execute it** —
   it is your full instruction from then on, under its own rules.
4. **If it prints `TIMEOUT`:** start it once more; a second `TIMEOUT` → reply "No fix-round prompt arrived" and stop.
