# M1 — The work method, written into the repository · plan

**Summary.** Docs and skills only, no code. Workflow §2 gains the seven phases of a Work Item. §9 is
rewritten so the two workers split by layer, with a new *Conflicts* part holding the early check and
the fast path. Documentation rules §5 gains the API/Web split of *Decisions* and *History*, as a rule
only. The build map gains one ordering note. Two new skills, `write-plan` and `final-report`, are
added, `start-work-item` and `open-pr` are updated to call them, and CLAUDE.md's checklist names
both. Every standing rule the prompts repeat is mapped to one home; two homes get one sentence each.
4 commits; `format:check` plus a link check by hand. Six stronger decisions below, all recommended.

Branch: `docs/work-method`, cut with `git switch --no-track -c docs/work-method origin/main` after
the reply. Worker B, worktree `masaha-b`, HEAD = `origin/main` = `5d692f3`, clean (checked).

## 1. Contract

- **Scope:** write the method of M1_PROMPT §3 into workflow §2, §3, §9 and §10, documentation §5,
  v1-mvp's *Ordering notes*, two new skills, two updated skills and CLAUDE.md's checklist. Give every
  standing rule one home.
- **Acceptance criteria:**
  - [ ] Workflow §2 lists the seven phases, including what the plan and the report contain, the
        save-then-stop step, and the no-code exception as an exception.
  - [ ] Workflow §9 states the split by layer, the narrow licence, the ownership of `packages/shared`
        and the contract, the one-layer-per-item rule, dependencies and the lockfile, and *Conflicts*
        (early check, fast path).
  - [ ] Documentation §5 states the API/Web split of *Decisions* and *History*, and says it is not yet
        applied to the existing documents.
  - [ ] v1-mvp's *Ordering notes* allows the API to run one step ahead of the screens.
  - [ ] The `write-plan` and `final-report` skills exist. Like the other skills, they link the owning
        sections, own no fact and name no path outside the repository.
  - [ ] `start-work-item` calls `write-plan`. `open-pr` holds phase 4, the fast path and the wait for
        CI and `CLEAN`, then calls `final-report`.
  - [ ] CLAUDE.md's session checklist names both new skills, and nothing else in it changes.
  - [ ] Every standing rule in §5 below has one home, which a skill links.
- **Out of scope:** applying the API/Web split to the existing capability documents, and finding 38
  (both M2). No edit to A's files: `findings.md`, `features/{lookups,space-links,spaces}.md`,
  `frontend/architecture.md`, `overview.md`.

## 2. Reading done

CLAUDE.md. All of the workflow. The map. Documentation rules (all of it). Testing (all of it).
v1-mvp's *Timeline*, *Sequence* and *Ordering notes*. The three skills. Engineering principles.
Setup's *Commands*, *The web* and *CI*. Backend conventions §1 and its *Growth* part. Frontend
architecture's *Capability layout* (read, not edited). Foundation §2. Localisation's *Catalogues*.
The open findings' titles and *Resolves when* lines, and findings 31, 37 and 38 in full. PR #50's
file list. The last S2B3A prompt's *owner's rules* block, to catch rules missing from M1's list.

## 3. Settled decisions, as they will be written

- **Phases (workflow §2, new *Phases* subsection).** The seven phases, worded as the prompt gives
  them. The old line "agree → design → decompose → write the contract → implement" is replaced by
  the phases. The contract still lives in the PR description. The *Reading before work* part stays as
  it is. The phases apply to a substantial item (§1); a trivial one goes straight to its PR.
- **§3 lifecycle line** becomes: Branch → Implement → Verify locally → Push → PR → CI and `CLEAN` →
  Report → Owner review → Merge → Delete branch. It links the phases.
- **§9 rewritten:** A builds the web; B builds the API, the schema, the migrations and the seed. Each
  worker has a narrow licence in the other layer, declared in its plan and approved: A never writes a
  migration, and B never builds a page. `packages/shared` and the API contract are the API worker's.
  Two items in flight never work in the same layer. Either worker may add a dependency, never both at
  once, and a lockfile conflict is never merged by hand.
  - *Conflicts*: the early check and the fast path (target ten minutes; a conflict in code adds lint
    and typecheck).
  - The folders, branches, databases, *Merging* and after-merge bullets stay. "Worker A carries the
    critical path" is replaced by the split.
- **§10:** `writing-plans` is now used in part inside `write-plan`. Its saved plan files stay unused:
  the plan is saved to the path the prompt names.
- **Documentation §5:** *Decisions* and *History* each have an **API** part and a **Web** part, and a
  part appears only when its layer's code exists. The rule says the documents written before it are
  aligned in one later item. The document is a *Contract*, so stating which rule is not yet applied
  is allowed (§4 of the same rules).
- **v1-mvp *Ordering notes*, one line:** "The API may run one step ahead of the screens, so the two
  workers never work in the same layer at once ([workflow §9])." Header date updated.
- **Skills:**
  - `write-plan`: the plan's sections in order, each linked to its rule. Then: leave plan mode with a
    short summary; the approval means "save"; write to the path the prompt names; end the turn.
  - `final-report`: the report's sections in order. Then: save to the path the prompt names, and
    summarise in the conversation.
  - `start-work-item` step 4 hands over to `write-plan`. Its list of plan contents moves there. The
    branch is cut after the reply approves building.
  - `open-pr`:
    - the old step 4 becomes phase 4, before the push, with the no-code exception;
    - a new step gives the fast path ([§9 *Conflicts*]);
    - after the push, it waits for CI on the pushed head and for `CLEAN`, then calls `final-report`;
    - review-fix rounds repeat phase 4 through the report.
- **CLAUDE.md:** step 1 adds "then `write-plan`"; step 4 adds "then `final-report` once CI passes".
  Nothing else changes.

## 4. Stronger decisions

1. **The no-code exception proves nothing on its own.** Prettier excludes Markdown (CLAUDE.md,
   setup's *Commands*), so on a docs-only change `format:check` reads none of the changed files.
   **Stronger:** the exception runs `format:check` and the link check by hand of
   [documentation §8](../../docs/architecture/documentation.md#8-link-integrity): a search for each
   anchor the change adds or moves. **Cost:** a few minutes per docs item, and it applies to M1
   itself. **Recommend: yes.** The fast path (conflict resolution) is unchanged: keeping both sides
   adds no link.
2. **Workflow §3 *Commits* claims more than the method runs.** It says "Every commit builds and
   passes lint, typecheck and tests". The new phase 4 runs the lanes once, on the head, and the
   standing rule runs lint and typecheck on each commit. The document would then state a rule nobody
   checks ("Claim only what is true"). **Stronger:** reword it as "Each commit is a complete unit;
   lint and typecheck run on each, the lanes once on the head (§2, phase 4)." **Cost:** a test
   broken in a middle commit and fixed later goes unseen, which makes `git bisect` weaker. That is
   acceptable for one developer with 3–6 commits. **Recommend: yes.**
3. **The worker runs the early conflict check itself.** The prompt gives `git merge-tree` against
   the open branches to the analyst at each report. **Stronger:** `final-report` gains a section with
   the result of `git merge-tree --write-tree` between the pushed head and every other open PR's
   head. The analyst reads the result and still decides the merge order. **Cost:** one command per
   report. **Recommend: yes.**
4. **B's licence names the error codes' catalogue entries.** Localisation requires every server error
   code in both catalogues, and `add-error-code` adds codes on the API side. Read alone, "B never
   builds a page" plus "the web is A's" leaves a new code without its words, or needs a fresh licence
   for each item. **Stronger:** §9 lists among B's examples "the catalogue entries of the error codes
   it adds", still declared in the plan. **Cost:** none. **Recommend: yes.**
5. **More triggers for a separate review conversation.** The prompt's triggers are more than about 25
   files, authorization or security, a transaction, or the schema. **Stronger:** add a new dependency
   and a change to CI or the build checks. Both are hard to reverse, and the analyst sees little of
   them in a report. **Cost:** a few more review conversations, which will be rare. **Recommend: yes.**
6. **Phase 4's lanes run one at a time.** Today's prompts say so, and the method's text does not.
   Findings 28 and 42 are failures under load. **Stronger:** phase 4 says "every lane once, one at a
   time, on the head; servers started for the real run are stopped and their ports checked free"
   ([setup › Running a second folder](../../docs/development/setup.md#running-a-second-folder)).
   **Cost:** none. **Recommend: yes.**

No rule in the documents or the ADRs other than #2 is weakened by the method.

## 5. The standing rules and their homes

| Rule | Home | Change |
|---|---|---|
| Honest test titles | [testing §3](../../docs/development/testing.md#3-rules-that-bind-every-test) rule 6 | **add** one sentence: a test's title states what it proves, and nothing it does not |
| No parameter, option or callback only tests pass | testing §3 rule 2 and *A feature, layer by layer* | none |
| …or that nothing uses | [engineering principles §1](../../docs/development/engineering-principles.md#1-mindset) | **add** one sentence: no parameter, option or callback that no caller passes |
| Tests stub the platform's seams, never `vi.mock` | testing §3 rule 3 and *layer by layer* | none |
| One responsibility per file; files by operation | engineering principles §2; frontend architecture's *Capability layout* (web); conventions §1 and *Growth* (API) | none |
| No hardcoded text, both catalogues | localisation's *Catalogues*; workflow §5 | none |
| No colours or CSS outside the design system | foundation §2 (1–2); CLAUDE.md | none |
| Lint and typecheck on each commit | workflow §3 *Commits* | reworded (stronger decision 2) |
| Lanes once on the head, one at a time; build + `check:build`; a real run | workflow §2 phase 4 | **new** |
| Commit subjects ≤ 50 characters | workflow §3 *Formats* | none |
| Report only once CI is green on the pushed head | workflow §2 phases 5–6 | **new** |
| Review fixes folded; ONE "Review fixes" comment | workflow §3 *Commits* | none |
| Rebase only on a real conflict | workflow §9 *Merging* | none |
| No tool attribution | workflow §3 *Commits*; CLAUDE.md | none |
| Never merge; never create an Issue | workflow §6, §2 | none |
| Screenshots in the folder the prompt names, never committed | workflow §5; `open-pr` | `open-pr` adds "never committed" |

- **Not a rule:** "build with `NODE_ENV=production`". It comes from the main folder's local
  `apps/web/.env`, which holds `NODE_ENV=development` (it looks like a copy of the API's). The repo's
  `apps/web/.env.example` has no such key, and worker B's file has none. Recommendation: the owner
  replaces that file with a copy of `.env.example`, and the prompts drop the line. No document home.
- **Stays in the prompt** (item-specific): which lanes an item may skip, the databases and ports,
  creating data through the API, and the token count.

## 6. Related findings

None folded. 38 is M2's. 37 (links checked by hand) is applied by stronger decision 1, not resolved.
No other open finding concerns the workflow or the skills. New findings, if any, are numbered from
48. Recording one needs `findings.md`, which is A's: if one comes up, stop and ask.

## 7. Files

| File | Change | Layer / owner |
|---|---|---|
| `docs/development/workflow.md` | §2 phases, §3 lifecycle + *Commits*, §9 rewritten + *Conflicts*, §10 line; date | B |
| `docs/architecture/documentation.md` | §5 one rule; date | B |
| `docs/plans/v1-mvp.md` | *Ordering notes* one line; date | B |
| `docs/development/testing.md` | §3 rule 6, one sentence; date | B (declared, rule home) |
| `docs/development/engineering-principles.md` | §1, one sentence; date | B (declared, rule home) |
| `.claude/skills/write-plan/SKILL.md` | new | B |
| `.claude/skills/final-report/SKILL.md` | new | B |
| `.claude/skills/start-work-item/SKILL.md` | step 4 to `write-plan`; step 5 after the reply | B |
| `.claude/skills/open-pr/SKILL.md` | phase 4, fast path, CI/`CLEAN`, `final-report` | B |
| `CLAUDE.md` | session checklist, steps 1 and 4 | B |

No file of A's (§6 of the prompt). No file of the other layer. `docs/README.md` needs no change: it
already describes the skills as a set.

## 8. Tests

None: no code. **Breaks:** none to make. **Seen failing:** not applicable.

## 9. Review Focus

- Every new link and anchor resolves. `#2-work-item` keeps its heading, and the new `#phases`,
  `#conflicts` and `#9-parallel-work` resolve from the skills (`../../../docs/...`).
- No skill states a fact: each step links §2, §3, §9 or testing.
- No path outside the repository in any skill or document (documentation §8).
- §9 still agrees with setup's *Running a second folder* and with the databases bullet.
- §10 still agrees with `write-plan` (the `writing-plans` part).
- CLAUDE.md changes only in its checklist.

## 10. Commits

1. `docs(workflow): define the work item phases`: §2 phases, §3 lifecycle and *Commits* (decision
   2), §10.
2. `docs(workflow): split the two workers by layer`: §9 with *Conflicts*, documentation §5,
   v1-mvp's *Ordering notes*.
3. `docs: give the standing rules a home`: testing §3 rule 6, engineering principles §1.
4. `chore(skills): add write-plan and final-report`: the two new skills, `start-work-item`,
   `open-pr`, CLAUDE.md.

## 11. Verification

- `npm run format:check` on the head.
- The link check by hand (stronger decision 1): a search for every anchor added or moved, from the
  documents and the skills.
- `git diff --stat origin/main` touches only §7's files.
- **Not run:** lint, typecheck, the lanes, `build` and `check:build`. There is no code: this is the
  phase-4 exception the item writes. CI runs them.
- Then `open-pr`: push, `gh pr create --assignee @me`, labels `docs` and `area:docs`. Wait for CI on
  the pushed head and for `CLEAN`. Then the report.

## 12. Decisions for the owner

- Stronger decisions 1–6: yes or no for each.
- The main folder's `apps/web/.env` (§5): a note only, the owner's file.

## Approval

Approved 2026-10-08, all six stronger decisions included (M1_PLAN_REPLY.md).
