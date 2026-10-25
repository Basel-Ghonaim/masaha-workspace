# DESK PR 2 — resume after the memory stop (2026-10-20)

You stopped at 12.4: `npm run test:api` on `36fa5d29` was killed for low system memory. The owner's answer:
resume now, in this order. Everything else in `3_EXEC_PROMPT_PR2.md` still binds (the stop rule, the report
as you go, the final reply's shape).

1. **Memory first.** Before any full lane: no `vitest`, `tsc`, `tsx watch` or dev server of another worktree
   runs (`Get-CimInstance Win32_Process -Filter "Name='node.exe'"`, by command line — `C:\dev\masaha\app\`
   is worker A's; never stop its processes: if one runs, wait). Write the free memory into the report before
   each full lane (`Get-CimInstance Win32_OperatingSystem` → `FreePhysicalMemory`). One full lane at a time;
   the next starts only after the previous one's `node` processes have ended.
2. **Rebase on #93** — `3b_REBASE_ON_93.md`, now: the tree is clean. `git fetch origin`, `git rebase
   origin/main`; then `npm run build -w @masaha/shared`, `npm run lint`, `npm run typecheck`. Report it as
   that file says.
3. **Finding 98 — the capability documents outgrow their size guide.** Documentation §5 says a capability
   document is "about 1,200 words at most"; `occupancy.md` was ≈ 1,480 words on `main` and this PR brings it
   to ≈ 1,700 — and it is not alone (on `main`, by `wc -w`: `spaces.md` ≈ 11,000, `space-links.md` ≈ 9,000,
   `users.md` ≈ 3,600, `lookups.md` ≈ 2,900). **Do not trim `occupancy.md` in this PR.** Record
   **finding 98** (the number is reserved for you; worker A starts at 99): the guide and the measured sizes,
   why it matters (a document read whole before a change), and that a later documentation item, or a
   revision of the guide, is the owner's to decide — no fix proposed as decided. File
   `docs/architecture/findings/98-the-capability-documents-outgrow-their-size-guide.md` and its index line,
   folded (`--fixup` + autosquash) into the commit of this PR that grows `occupancy.md` most.
4. **Then 12.4 whole, on the rebased head** (the head changed, so each lane runs once more on it): every
   command 12.4 lists, `test:api` included — then 12.5's breaks still owed (B3–B39 and A1's three) — 12.6's
   real run — `#PRNUM`, push, the PR (12.7, its description naming "Carried from #94" with both carried
   commits) — CI green and `CLEAN` — the conflict check (12.8) — the report.
5. **Your scratchpad files** (`breaks.txt`, `brks.py`, `realrun.mjs`): if this conversation can still read
   them, use them; if not, rebuild them from the plan's 12.5 and 12.6 — never skip a break or a case for
   their loss.
6. **If a lane is killed for memory again:** stop at once (no retry, no narrower run), write the free memory
   before and the exact error into the report, and reply `Status: STOPPED`.
