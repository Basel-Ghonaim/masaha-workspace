# FINAL — worker A: wait for the execution prompt, then run it

You are **worker A's lead executor** for the project's last build mission, in `C:\dev\masaha\app`, in a fresh
conversation. The plan is being written by another session; the supervisor will review it, settle its open points on
the owner's behalf, and write your execution prompt. **The owner is away; do not wait for him.**

1. **Do nothing else first:** no reading of the repository, no branch, no install. `git -C C:\dev\masaha\app status
   --short` must be empty and `main` at `origin/main` — if not, say so in your final reply and continue.
2. **Start the waiting script in the background** (it polls every 2 minutes, up to 8 hours):
   `bash /c/dev/masaha/workspace/WORKER_A/FINAL/scripts/wait_ready.sh 8` — with `run_in_background`, so you are woken
   when it exits. Do not poll its output yourself, and do not sleep.
3. **When it prints `READY`:** read
   `C:\dev\masaha\workspace\WORKER_A\FINAL\3_EXEC_PROMPT_LEAD.md` whole and **execute it** — it is your full
   instruction from then on, under its own rules (a lead with sub-agents, no stop until ready for review).
4. **If it prints `TIMEOUT`:** start it once more (another 8 hours); a second `TIMEOUT` → reply "No execution prompt
   arrived" and stop.
