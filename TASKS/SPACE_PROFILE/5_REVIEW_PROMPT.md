# Review of the space-profile prototype PR (design/space-profile) — one reviewer

You are a **read-only reviewer** of Masaha's prototype PR on `design/space-profile`, launched headless by the main
supervisor once CI was green and GitHub said `CLEAN`. **The PR number and the head you review are given in the launch
line** — call the head `<HEAD>` and pin every read to it. **Work alone — no subagents.** No project skill, no branch.
Tool and model: Claude Code, Opus 5.5.

**What it is:** the redesign of the owner's space profile and the admin's space editor **in the design prototype
only** (`docs/design/` and nothing else): view first, one Sheet per section (photos edited in place), the order of the
public page, the header with the completeness bar, the side index, prices as rows (R6–R9), hours simple/custom
(W1–W5), shifts apart (S1–S5), amenities, about, location, contacts as tiles with the new types and «وسيلة أخرى»
(M3–M4), drag with the keyboard, and «الباقات والأسعار» showing prices read-only (R1).

## Rules

- **Read only, commit objects only.** The supervisor fetched before launching you; fetch once only if
  `git cat-file -t <HEAD>` fails. Reads: `git show <HEAD>:<path>`, `git diff origin/main...<HEAD>`, `git log
  origin/main..<HEAD>`. **Never** edit, checkout, switch, reset, stash or commit; no installs, no npm, no servers, no
  comments on GitHub. Your cwd's working tree is not the PR; ignore it. A `.lock` failure: wait 30 s, retry once. The
  only file you write is your report.
- First `gh pr checks <n>` — red or pending: say so and stop. At the end, say whether the head moved.
- Report **verified defects only**, with file and line at `<HEAD>`, the scenario, severity — **blocker** (a page that
  breaks: a duplicate top-level name across a page's scripts, a browser-owned global such as `name`, object rest, a
  class absent from the prebuilt CSS; a file outside `docs/design/`; an owner's decision built the opposite way) ·
  **should-fix** (a decision missing or built differently without a written reason; a leftover old control — an
  always-open field, a per-section Save on the page, «نسخ إلى كل الأيام», move buttons, the custom price description;
  a dismiss not reading «رجوع» (P9); a Sheet that closes with changes without «تجاهل التغييرات؟»; a disabled control
  without its reason; text not in both languages through `tr()`; numbers/links not LTR-isolated; keyboard drag not
  announced; a link still landing on `Packages.html#prices` to edit; Space details broken by a shared module) ·
  **nit** — and the fix. "Plausible" when unsure. No praise. Do not report what `check-parse` / `check-classes` / CI
  enforce and passed.

## Read, in this order

1. `git show <HEAD>:CLAUDE.md` and `git show <HEAD>:docs/design/README.md` (the prototype's rules and traps).
2. `C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\0_OWNER_DECISIONS.md` — whole; **M1–M4 override earlier lines; R3/R4
   were replaced by R6–R9.** These bind.
3. `C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\3_PLAN_AND_EXEC_PROMPT.md` and `2_PLAN.md` (the worker's plan, its
   "cannot be built as written" and "Proposed alternatives" — judge each: sound / acceptable / wrong).
4. The diff, then each changed page with all the scripts it loads (for the global-name check).

## Look hardest at

- Each decision G1–G5, H1–H4, P1–P7, R1/R2/R5–R9, W1–W5, S1–S5, A1–A2, B1–B2, L1–L2, C1–C2, M1–M4: built / missing /
  different (one line each).
- The phone layouts the owner called out: the header (M2: 64 px cover beside the name, buttons and bar full width),
  photos (M1: 16:9 cover then one sideways row of 96×72 thumbnails, no «+N» on a phone).
- The admin's page (H4 badges, actions in the top bar) and «الباقات والأسعار» read-only with «تعديل الأسعار في ملف
  المساحة».
- `INDEX.md`, `CHANGES.md` («Refactor 2 — the space profile (2026-11-08)», one line per decision, naming what it
  revises) and `Flows - states.html` true to the pages.
- Scope: only `docs/design/`; one commit, Conventional, no tool attribution.

## Your output

Write `C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\6_REVIEW_CLAUDE_CODE.md`:

```
# Review of #<n> (space profile, prototype) — Claude Code, Opus 5.5
Head: <HEAD> · files <n> · checks: <green/red> · head moved: <yes/no>
Verdict: <mergeable | mergeable after a fix round | not mergeable>

## Findings (most severe first)
### F1 — <blocker|should-fix|nit> · <title>
- Where / Seen in the code / Scenario / Fix
(None → "None.")

## The decisions, one line each (built / missing / different)
## The plan's alternatives and workarounds, judged
## Records (INDEX, CHANGES, Flows)
## Not checked, and why (the browser pass is the supervisor's)
```

Then stop.
