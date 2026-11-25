# WI-B — the supervisor's review of `6_PLAN.md` (2026-11-25)

**Verdict: sound; recommend approval with every D as the worker recommends.** The plan answers the question the
trial raised (four default buttons on the desk, almost none on the public pages) with an inventory, not a guess:
81 buttons with no variant, about 45 of them a main action. Opting in (D1) is the safe build — a forgotten main
action stays ink, today's look — and B1 becomes a test (S2), not a memory. Checked: the role's values are B1's exactly
(light `spark-600` / white, hover `spark-700`; dark the ink's painted values); ADR 0022's Revised line is the approved
one, word for word, as its own commit; nothing in the repository was edited.

## On the owner's decisions
- **D1 opt-in `main`, default stays ink:** agree.
- **D2 an overlay's confirming action is main:** agree (it is the approved P2 picture).
- **D3 the table:** agree. **The desk's «تحصيل» rows stay filled ink** (the owner's own DI-4 / DI-20); outline is the
  alternative — it would be quieter beside the berry check-in, but it reverses an owner decision for reception's daily
  screen, so it is his to take, not a default.
- **D4 C2's auth forms in a small follow-up after both merge:** agree (no shared file now; the follow-up is one word per
  call site).
- **D5 keep the sidebar's count and `chart-1` as they are:** agree.
- **D6 a `main` WhatsApp on the space page from 768 px:** agree — the trial showed the desktop space page has no main
  action at all; this gives it the one the phone already has.
- **D7 S1–S4:** agree; S1 (fills only, no `text-main-action`) keeps ADR 0022's "no berry link" true by construction.

## For phase 2
- Before / after shots per screen, as in the trial (the owner decides by looking).
- Review focus §10's `twMerge` point is checked in the browser, not assumed.

## The approval message (typed by the owner in the worker's window)

> APPROVED by the owner: D1–D7 as recommended (the desk's «تحصيل» rows stay filled ink). Execute the plan to the end
> without stopping: commits, local verification, the Chrome pass with before / after pairs, the PR, green CI and
> CLEAN, then 7_REPORT.md. Run heavy commands in the foreground. C2 also edits
> `pages/site/public/space/SpacePage.component.test.tsx`: do not touch it — put the WhatsApp assertion in ContactBar's
> own test. Never merge.
