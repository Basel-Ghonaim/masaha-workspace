# Review of the CONTACT_RULES PR (phones, links, a row's ghost control, test hygiene) — one reviewer

You are a **read-only reviewer** of one Masaha PR, launched headless by the main supervisor once CI was green and
GitHub said `CLEAN`. **The launch line gives the PR number, its branch and the head** — call it `<HEAD>` and pin every
read to it. Work alone (no subagents), no project skill, no branch. Claude Code, Opus 5.5. The PR was built by a free
executor (Codex) from a Claude plan: read it with that in mind — look for the plan followed to the letter but wrong in
spirit, tests that cannot fail, and shortcuts.

## Rules
- **Read only, commit objects only:** `git show <HEAD>:<path>`, `git diff origin/main...<HEAD>`, `git log
  origin/main..<HEAD>`, `git grep <pattern> <HEAD>`; fetch once only if `git cat-file -t <HEAD>` fails. Never edit,
  checkout, switch, reset, stash or commit; no installs, npm, tests, servers, database or GitHub comments.
- First `gh pr checks <n>` — red or pending: say so and stop. At the end, say whether the head moved.
- Report **verified defects only**, file and line at `<HEAD>`, scenario, severity — **blocker** (a phone or link rule
  that accepts what C1–C3 refuse or refuses what they accept; a rule enforced in the browser but not on the server or
  the reverse; data changed; a test that cannot fail or one bent to pass; production code only a test uses;
  authorization changed) · **should-fix** (a missing planned test; a case of C1–C3 untested; a false document; a
  class outside the design system; hardcoded or one-language text) · **nit**. The fix and where it belongs (folded
  into `<commit>`, or a finding — check the index for the next free number). No praise. Check a library's behaviour
  before calling a bug (zod, URL parsing in Node and browsers, Tailwind 4, jest-dom).

## Read
1. `git show <HEAD>:CLAUDE.md`; `docs/development/workflow.md`, `testing.md`, `engineering-principles.md` at `<HEAD>`.
2. `C:\dev\masaha\workspace\TASKS\CONTACT_RULES\0_OWNER_DECISIONS.md` (C1–C10, binding), `2_PLAN.md` (the plan —
   its test matrix and breaks), `4_REPORT.md` (and `4_HANDOFF_STATE.md` if present).
3. The diff commit by commit, then files at `<HEAD>`.

## Look hardest at
- **Phones (C1, C2):** Arabic-Indic and Eastern digits converted in the one shared helper, used by every caller
  (contacts, «وسيلة أخرى», customers, the desk, platform settings); +970 / +972 / 00970 / 00972 / local all accepted;
  refusals intact. `toWesternDigits` moved, not copied; no sibling-feature import.
- **Links (C3, C4):** a website only a real domain with a TLD — never an IP, `localhost`, a bare word or number;
  Facebook only a page or a profile (one segment, `profile.php?id=`, `/people/<name>/<id>`) — every video, `/watch`,
  post, group, event, photo, share or search refused; the browser refuses before sending (proved: no request), the
  server refuses too (`invalid_format`, nothing written). The data count reported and no data changed.
- **The row's ghost control (C5):** the smallest layer change, semantic tokens, both themes; `CustomerMenu` outside a
  table unchanged; the contrast claim (≈1.21:1) honest.
- **Tests (C6):** 219's teardown fixes the cause without hiding errors; 225's four warm-ups as testing §3 rule 8.
- **Documents:** the capabilities, the contract, the data model; findings 217, 218, 219, 225, 226 resolved and 228
  recorded; the index after PROTOTYPE_SPLIT's merge (C7).

## Output
Write `C:\dev\masaha\workspace\TASKS\CONTACT_RULES\7_REVIEW.md`:

```
# Review of #<n> (CONTACT_RULES) — Claude Code, Opus 5.5
Head: <HEAD> · commits <n> · files <n> · checks: <green/red> · head moved: <yes/no>
Verdict: <mergeable | mergeable after a fix round | not mergeable>
## Findings (verified defects only, most severe first)
### F1 — <blocker|should-fix|nit> · <title>
- Where / Seen in the code / Scenario / Fix · Belongs
(None → "None.")
## C1–C10, built / departed, judged
## The plan's test matrix — present / missing / weaker · would it fail on its break?
## Documents
## Scope and commits
## Not checked, and why
```
Then stop.
