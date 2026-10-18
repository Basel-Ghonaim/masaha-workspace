# Review — PR #47 (D-2: the feature documents and the documentation rules)

You are the **independent reviewer** of PR #47, a documents-only change that restructures Masaha's
documentation. Run from `C:\Users\basel\masaha` (the main folder). You don't build, fix or merge.

## Budget (hard limits — the owner's)

- **At most 2 subagents. Never a third.** No workflows. Use no plugin skill (workflow §10: review
  sessions use none).
- **The whole review stays under 700,000 tokens**, this conversation and both subagents together.
- **Reports:** at most 800 words per subagent, and at most 1,000 for yours.

## Rules

- **Read-only.** No edits, commits, checkouts, switches, installs, npm or test runs, or GitHub
  comments. Read only from commit objects: `git show <head>:<file>`, `git diff d8884c4...<head>`.
  You may write throwaway read-only scripts in a temporary folder outside the repository (for links
  and searches).
- **Pin everything to the PR's current head:** run `git fetch origin`, then
  `gh pr view 47 --json headRefOid` and use that commit as `<head>` everywhere below (it is the
  ninth commit's, after `d4dc235`), base `d8884c4`. State the head in your report.
- **The ninth commit** (the owner's addition: the map's "read it when" lines, the reading-before-work
  rule and the related-findings rule in workflow, the `start-work-item` steps, CLAUDE.md's pointer)
  is reviewed with the rest: one owner per rule, the skill links rather than restates, the map stays
  a guide, and the rules are clear enough for a worker to follow alone.
- **Report concrete problems only:** the file and heading (or line), what is wrong, the evidence, the
  severity (blocker / should-fix / nit) and the fix. **Verify each before reporting it;** drop
  anything speculative.

## What the PR must be

**The contract is the merged plan:** `docs/plans/feature-documents.md` at `d8884c4` — its decisions
(§2), its duplication ledger (§4, 69 rows, each ending with exactly one home), its decisions index
(§5), its steps (§6), its review axes (§7) and exit criteria (§9) — with the owner's answers to its
§10 questions:
1. routing that serves one capability stays in frontend architecture §2;
2. "the admin edits a space only while it is unverified" lives in `backend/security.md` ›
   Authorization; conventions keeps only the placement rule;
3. the audit list stays in conventions §6;
4. a platform rule keeps one short example; full per-capability lists move to the capability
   documents;
5. the overview's *Built*: one line per capability, linking its document;
6. the code governs: what is built (space delete and restore) is documented as built;
7. contradictions corrected where their section is touched; a finding where the code may be what
   should change;
8. the map lists `docs/features/` and one line per document.

**The owner's later instruction:** the word limits (~1,200 per capability document, ~1,500 for the
rules) were **not** to stop the work; a document may exceed its limit if it stays coherent, and the
owner judges after this review. The worker reports `auth.md` at 1,477 words, the rules at 1,499.

**The worker reports these departures from the plan** (judge each): photos not recorded as "in no
fact group" (data-model counts them in the profile group); the request id shown only by a form's
failure; two decision dates moved to where each first landed (#25, #16); DS-2 applied to the text at
`main`; DM-4 needing no change. The platform documents shrank about 1,000 words, not the plan's
~2,300 (links left behind, one example kept per rule, the audit list kept).

## The split

### Subagent 1 — duplication and nothing lost (the owner's first concern)

**Its files:** every changed and new document; the plan at `d8884c4`.

**It checks:**
- **No fact has two homes** across `docs/`, CLAUDE.md and `.claude/skills/`: for each ledger row,
  search its key phrases and confirm exactly one home and, elsewhere, only a link. Then look beyond
  the ledger: does any new capability document restate a mechanism, an endpoint's shape, an entity's
  fields, a security rule, or another capability's facts? Does the new rules document restate
  workflow §7, CLAUDE.md, `docs/README.md` or ADR 0018, or do they restate it?
- **Nothing lost:** every ledger row's fact is present once at `<head>` (moved, merged, kept), or
  its deletion as a duplicate left the original owner intact.
- **The length question, for the owner:** for `auth.md` (1,477) and the rules document (1,499), is
  the length coherence (needed flows and decisions) or does it hold duplication, mechanism, or
  another document's facts? Name exactly what could leave, if anything, and where it would go.
- **The departures** above: is each correct against the code and the plan?

### Subagent 2 — truth against the code, structure and the rules

**Its files:** the five `docs/features/*.md`, `docs/architecture/documentation.md`, ADR 0018, the
changed sections of the platform documents, workflow §5 and §7, the `start-work-item` skill,
CLAUDE.md, `docs/README.md`, the new findings 37–41.

**It checks:**
- **Every claim in the capability documents is true at `<head>`'s code** (the decisions, the
  behaviour, the code maps' folders and entry points, the statuses, the PRs and dates): sample at
  least five decisions per capability against the code, and every claim of "built".
- **The template:** each capability document follows it; a section appears only when its code exists
  (no web section for `spaces`); code maps are folders and entry points, never file lists; headers'
  declared classes are true; no local paths.
- **The rules document:** states the adopted rules (the boundary question, the two tables, the
  classes, sections only when code exists, rules not inventories, capability documents and the
  stable-core rule, the ADR clause, link integrity, one entry point, what was not adopted) clearly
  enough that a worker can apply them alone; nothing contradicts workflow or CLAUDE.md.
- **ADR 0018:** short, decision-level, no file names, one decision.
- **The triggers:** workflow §7's capability row and §5's documentation check say the same as the
  rules document without restating it; `start-work-item` points a worker to the capability document
  first; CLAUDE.md stays a pointer.
- **Links and anchors** across `docs/`, CLAUDE.md and the skills resolve (a read-only script);
  the records (`plans/`, `findings.md`, ADRs) changed only by repointed links and appended findings.
- **The commits:** eight, Conventional, ≤ 50 characters, each a complete step; no attribution.

## Your output

Write **one file**, `C:\Users\basel\.prompt\MASAHA_WORKER_C\REVIEW47_REPORT.md`:
1. **A verdict in one line.**
2. **The findings,** most severe first, deduplicated (severity, place, evidence, fix).
3. **The length question,** answered for `auth.md` and the rules document, for the owner to decide.
4. **"Verified OK":** a short list per subagent's area.

State the total tokens used. Then stop. The owner's analyst verifies the findings and writes the
fixes list.
