# Review of the PROTOTYPE_SPLIT PR (the design archive leaves `masaha`) — one reviewer

You are a **read-only reviewer** of one Masaha PR, launched headless by the main supervisor once CI was green and
GitHub said `CLEAN`. **The launch line gives the PR number, its branch and the head** — call it `<HEAD>` and pin every
read to it. Work alone (no subagents), no project skill, no branch. Claude Code, Opus 5.5.

## Rules
- **Read only, commit objects only:** `git show <HEAD>:<path>`, `git diff origin/main...<HEAD>`, `git log
  origin/main..<HEAD>`, `git grep <pattern> <HEAD>`; fetch once only if `git cat-file -t <HEAD>` fails. Never edit,
  checkout, switch, reset, stash or commit; no installs, npm, tests, servers or GitHub comments. `curl -sI` on the
  public URLs the PR adds is allowed (read-only).
- First `gh pr checks <n>` — red or pending: say so and stop. At the end, say whether the head moved.
- Report **verified defects only**, file and line at `<HEAD>`, with the scenario and severity — **blocker** (a link or
  pointer that now resolves nowhere in a document the project relies on; a check weakened beyond the archive's own
  exclusion; anything of `docs/design/` left half-removed; a build, lint or `check:*` behaviour changed for files that
  are not the archive's) · **should-fix** (a false or stale statement; a pointer to `main` where the record needed a
  pinned commit, or the reverse; an ADR that breaks the ADR style — short, decision-level, no file names) · **nit**.
  The fix and where it belongs. No praise. Do not report what CI enforces.
- **The identity rule:** never write the university, the supervisor or the defence; the PR must not either — check its
  files, commit messages and description for any word that says for whom, where or as what the project was made.

## Read
1. `CLAUDE.md`, `docs/README.md`, `docs/architecture/documentation.md`, `docs/development/workflow.md` at `<HEAD>`.
2. `C:\dev\masaha\workspace\TASKS\PROTOTYPE_SPLIT\0_OWNER_DECISIONS.md` (P1–P7, binding), `2_PLAN.md` (§4.2 every
   pointer and its fate; §6.6; §10.2), `3_APPROVAL.md`, `5_IMAGES_APPROVED.md`, and `4_REPORT.md` if present.
3. The diff commit by commit.

## Look hardest at
- **Completeness:** `git grep -n -i -E "docs/design|design/prototype|design/screens|\.\./design/" <HEAD>` — every
  remaining hit is a record's prose or a deliberate URL; nothing points into a folder that no longer exists.
- **Each repointed URL** answers 200 at `https://github.com/Basel-Ghonaim/masaha-prototype/...` (records pinned to a
  commit, active documents to `main`, per P7); anchors exist.
- **The exclusions removed** (`.prettierignore`, `eslint.config.js`, `checkLinks.ts`'s `NOT_SCANNED`,
  `.coderabbit.yaml`): only the archive's entries go; nothing else loosens.
- **ADR 0020** and its line in the map; `CLAUDE.md`'s *Design archive* line; `docs/README.md`.
- The code comments repointed (`Logo/drawing.ts`, `resetEmail.ts`, `resetEmail.copy.ts`): comments only, no behaviour.
- Commits: subjects ≤ 50 with bodies, no attribution, no `#PRNUM`, staged by path, nothing outside the plan.

## Output
Write `C:\dev\masaha\workspace\TASKS\PROTOTYPE_SPLIT\7_REVIEW.md`:

```
# Review of #<n> (PROTOTYPE_SPLIT) — Claude Code, Opus 5.5
Head: <HEAD> · commits <n> · files <n> · checks: <green/red> · head moved: <yes/no>
Verdict: <mergeable | mergeable after a fix round | not mergeable>
## Findings (verified defects only, most severe first)
### F1 — <blocker|should-fix|nit> · <title>
- Where / Seen in the code / Scenario / Fix · Belongs
(None → "None.")
## Every pointer of the plan's §4.2 — done / missed / wrong
## The URLs checked
## Documents and the ADR
## Scope and commits
## Not checked, and why
```
Then stop.
