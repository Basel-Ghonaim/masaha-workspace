# D-2 — Execute the feature-documents plan (plan-mode map)

## Context

PR #46 merged `docs/plans/feature-documents.md`, the contract for this item: one document per capability under `docs/features/`, a documentation strategy, ADR 0018, every ledger row moved to one home, the *Built* header lines cut to the platform, and a verification pass — one branch (`docs/feature-documents`, cut `--no-track` from `origin/main` d8884c4), one PR. Workers A and B are paused. Documents only; no code.

**Ledger re-verified against `main`:** `git diff 5a17db5 d8884c4` touches only `docs/README.md` (the plan's map line) and the plan itself. **No row moved.** Two rows read slightly differently from the plan's wording and are applied to what is there:
- **DS-2:** foundation §6 holds no key names at `main`; its duplicate is the *Pre-paint script* bullet (localisation › Before first paint owns it) → replaced by a link.
- **Claim 5:** the route status states do **not** show the request id; only the form failure and `useRefusalView` (a reset link's refusal) do (`shared/forms/hooks/useRefusalView.ts`). Architecture §5 is corrected to that.

**Checks (owner's update):** no `npm ci`, no local lanes (Prettier ignores Markdown; ESLint lints code only). Nothing run from the main folder. CI runs every lane on the pushed head. Word counts by `wc -w` (the plan's counts used another tokenizer: architecture 6,061 by `wc` vs 6,127 in the plan; the PR reports `wc -w` before/after consistently).

## 1. Contracts I build to

**Strategy, `docs/architecture/documentation.md`** (≤ ~1,500 words, class *Contract*). Sections and the rule each states:
1. *The boundary question* — "a shared mechanism, or a capability-specific application of one?" Mechanism → platform document; application → capability document, which links and never restates.
2. *One owner per kind of fact* — table: fact → owner → linked by (endpoint/payload → api-contract; entity/derived value → data-model; security rule → security.md; module placement/levels → conventions; web zones/routing/guards → frontend architecture; v1 scope and *Built* → overview; a capability's flow, experience, decisions, code map → its `features/` doc; a decision meeting the ADR threshold → ADR; a divergence → findings; ordering of work → a plan).
3. *What each category owns and must not contain* — table: platform docs (rules, one short example per rule, no capability enumerations or changelogs), capability docs (applications, decisions, folders/entry points; no restated mechanism, no file lists, no endpoint shapes), records (ADRs, findings, plans: never rewritten, only links repointed), the map (guides, never enumerates files; lists the capability documents).
4. *Classes* — Contract, Description, Record, Plan, Commitment, one line each; a declared class must be true.
5. *A section appears only when its code exists.*
6. *Rules and intent, not inventories* — incl. Q4: a platform rule keeps one short example naming a capability; enumerations live in the capability documents.
7. *Capability documents* — the template (decision 4), the stable-core rule (decision 5), ≤ ~1,200 words, named after the backend module, one per capability across API/shared/web; security stays whole (decision 8); routing that serves one capability stays in frontend architecture §2 (owner's answer 1).
8. *ADRs* — new clause: no ADR when a document naturally owns the decision (threshold itself stays in workflow §7 — see open decision B).
9. *Link integrity* — a move updates every link in the same PR; checked by hand until a checker exists (finding).
10. *One entry point* — the map.
11. *Not adopted* — the four, one line.

**ADR 0018** — *Capability documents own capability-specific applications*. Context · Decision · Alternatives · Consequences, short, no file names; one decision (the capability layer, ownership boundary, ADR clause as consequence).

**Capability template** (decision 4), each `docs/features/<module>.md`, class *Description*, ≤ ~1,200 words:
header (Status · Class · Last Updated · Owner; Authority; Scope: API module / shared folder / web feature) → What it does → Who uses it → Responsibility boundary → How it composes the platform (links only) → Behaviour and flows → Decisions (each: decision; *why*; date, PR) → Code map (folders and entry points only) → Open findings (links) → History (PRs). Section absent when its code is (no web section for `spaces`; no public web section for `lookups`). Decisions are prose lines without the plan's AU/US ids (the PR description maps them). Dates are merge dates (`gh pr list`): #25 10-03, #27 10-02, #31 10-03, #33 10-04, #34 10-04, #35 10-05, #36 10-04, #38 10-05, #39 10-05, #40 10-05, #41–#45 10-06.

## 2. Constants

- No fact in two homes at any commit; each capability commit writes its document **and** makes its rows' moves.
- No fact lost: every ledger row ends in exactly one home (tracked per step below).
- A move and its link land in the same commit.
- Nothing claimed that the code does not show; each decision's status re-checked in code in its step.
- Records (`plans/`, `findings.md` entries, ADRs) not rewritten; only links repointed. New findings are appended.
- Security rules stay whole in `backend/security.md`.
- Commit subjects ≤ 50 chars; no attribution; stage by path; no local paths in documents.

## 3. The map (steps and commits)

| Step | Commit | Rows / writes | Decisions-index entries | Contradictions corrected | Checks |
|---|---|---|---|---|---|
| X-1 | `docs(architecture): add the documentation rules` | `architecture/documentation.md`; `decisions/0018-capability-documents.md`; README: *Rules for this set* → one line + link, strategy + ADR 0018 entries, `features/` folder entry (lines added per step as each doc lands); findings **37** (no link checker) and **38** (one file per finding deferred) | — | — | strategy ≤ 1,500; ADR names no file; links resolve |
| X-2 | `docs(workflow): add capability document triggers` | workflow §7 capability row (+ ADR threshold links strategy's clause); §5 DoD documentation check; `start-work-item` step 3: capability's document first; CLAUDE.md: strategy + `docs/features/` | — | — | skill only links; CLAUDE.md stays a pointer |
| X-3 | `docs(lookups): add the lookups document` | `features/lookups.md`; AC-1, DM-5, FA-24 (example stays, detail moves), lookups parts of FA-1, FA-3, FA-12, FA-18, CO-1; map line | LK1–LK15 (LK7 links finding 30) | — | step checks |
| X-4 | `docs(spaces): add the spaces document` | `features/spaces.md` (no web section); CO-4, AC-8 + CO-7 → security › Authorization (answer 2; conventions keeps "`spaces` never imports `space-links`", contract keeps the 403), AC-9, spaces part of CO-1; overview scope line "Spaces (add, edit, hide, delete and restore)" (answer 6); map line | SP1–SP10 (SP7 re-checked) | — | step checks |
| X-5 | `docs(space-links): add the space-links document` | `features/space-links.md`; FA-6 (switcher clause), FA-10, FA-11, CO-6, AC-7, SO-1 (its half), space-links parts of FA-1, FA-12, FA-18, SE-1, CO-1; map line | SL1–SL12 (SL5 as changed, links finding 18) | **15** (governorate filter resolved by `lookups` first) | step checks |
| X-6 | `docs(users): add the users document` | `features/users.md`; FA-8, FA-22, users parts of FA-1, FA-3, FA-12, FA-14, FA-18, SE-1, CO-1; map line | US3–US11 (US1–US2 linked in security; US7 re-checked) | **6** (route table gains `/change-password`), **8** (security: only `/me/password` allows a pending change; public and cookie routes never read the claim), **14** (conventions §2 names users' `passwords` parameter + finding **39**) | step checks |
| X-7 | `docs(auth): add the auth document` | `features/auth.md`; FA-9, FA-13, FA-17, FA-19–FA-21, FA-23, SE-2–SE-11, CO-8, AC-2–AC-6, SO-1 (its half), auth parts of FA-1, FA-3, FA-12, FA-14, FA-18, SE-1, CO-1; map line | AU2, AU6–AU23 (AU1, AU3–AU5 linked in security; AU6–AU7 link ADR 0017; AU10, AU11, AU21 re-checked) | **2** (FA-23), **4** (FA-13 recovery repository, FA-18 space-links exports — handled in X-5/X-7) | step checks (over the limit: keep it whole, no stop; listed in the PR) |
| X-8 | `docs: cut the built lines to the platform` | header *Built* remnants (architecture, security, conventions, localisation; decision 10); overview *Built* → one line per capability with links (answer 5; `spaces` "the admin's, on the API only"); FA-2, FA-4, FA-5, FA-7, FA-15, FA-16, SE-12, CO-5, CO-9, DM-1–DM-4, DM-6, LO-1, LO-2, SO-2, DS-1, DS-2, ST-1, GL-1; CO-2 stays (answer 3), CO-3 stays as one-phrase index with links | — | **1** (LO-1), **3** (layout tree: `AdminLayout`/`SpaceLayout` each render `DashboardLayout`), **5** (§5 request id), **7** (conventions §6: `space.restored`, temp-password link → security › Passwords), **9** (data-model *Setting* + conventions §9: catalogue holds `newSpaceDefaults` and two thresholds; seed writes the contact keys + finding **40**), **10** (OV-1), **11** (engineering-principles example `SpaceDto` → `SpaceSummary`), **12** (conventions §10: the space is not yet logged + finding **41**), **13** (setup: spaces entered through the admin's API) | every header states only the platform |
| X-9 | — (fixes fold into the step they correct) | verification pass | — | — | exit criteria §9 |

Note on X-7/X-5 and claim 4: the recovery repository and the `space-links` exports are named in the capability documents' code maps, not in architecture (the generic rule stays there, answer 4).

**Per-step checks:** each named row applied (old place is a link or gone; `grep` of its key words across `docs/` finds one home); template followed, sections only where code exists; `wc -w` ≤ ~1,200; code map folders/entry points only; each decision has reason, date, PR and was checked in code; every link and anchor in touched documents resolves (grep for the heading); the map lists the new document; header class *Description*.

**Verification pass (X-9):** every relative link in `docs/`, `CLAUDE.md`, `.claude/skills/` resolves to file and heading (scripted read-only check in the scratchpad: parse `](…)` links, check files exist and anchors match GitHub slugs of headings); residual-duplication grep per ledger row; word counts; declared classes true; `git diff --stat` shows only `.md` files; records changed only by repointed links/appended findings.

## 4. Open decisions (answered by the owner, 2026-10-06)

- **A. system-overview's declared class "Overview"** → relabelled *Description* in X-8.
- **B. Home of the new ADR clause** → the strategy; workflow §7's threshold line links it (X-2).

Settled by me (convention, not architecture): decisions without plan ids; FA-12 leaves name + audience + link for the five documented capabilities (unbuilt placement survives in conventions' modules table and §9), parentheticals of undocumented capabilities untouched; claims 5, 6, 7, 11 placed in X-6/X-8 as above because no ledger row's step owns their sections.

**Owner's change on approval:** no stop for word limits. A document past its limit (~1,200 capability, ~1,500 strategy) is kept whole and coherent, never split or cut; the strategy still states the limits as planned; the PR lists every document over its limit with its count and one line on why.

## 5. PR and report

`docs: add the feature documents`, labels `docs`, `area:docs`, assignee owner. Description: steps, rows closed and decisions recorded per step; `wc -w` before/after per platform document; contradictions corrected and findings 37–41; differences from the plan (DS-2 wording, claim 5 wording, decisions A/B, no local lanes per the owner). Plan saved to `C:\Users\basel\.prompt\MASAHA_WORKER_C\PLAN_MODE\D2_PLAN.md` after approval. Subagents: none planned (cap 3). After CI green on the pushed head: report head, commits, counts, tokens, subagents. No merge, no Issue.
