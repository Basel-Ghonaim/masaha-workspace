Work Item P-1 — The build map in the v1 plan · branch `docs/build-map`

## How to work (mandatory)

1. Read CLAUDE.md, then docs/development/workflow.md, then docs/README.md. Follow the project's workflow exactly: task classes, Git lifecycle, scope control, Definition of Done, decision authority, stop rules.
2. You are **worker B**. You work in the worktree `C:\Users\basel\masaha-b`, which the owner has already created detached at `origin/main`, with `npm ci` run. Never work in the main folder `C:\Users\basel\masaha`.
   - Before planning, check:
     - `git rev-parse --show-toplevel` is that folder;
     - the tree is clean;
     - after `git fetch`, HEAD is at the latest `origin/main`.

     If not, stop and report.
3. Start in PLAN MODE. No edit, no branch and no commit before the owner approves a written plan. The plan lists:
   - the proposed text structure;
   - every file to change;
   - the commits;
   - how you verify;
   - any question or divergence you found.

   Wait for approval.
4. After approval, create the branch: `git fetch origin` then `git switch --no-track -c docs/build-map origin/main`. Implement only the approved plan. The first push is `git push -u origin docs/build-map`.
5. Finish at "Ready for review": self-review, push, open the PR. Never merge.

## Context

`docs/plans/v1-mvp.md` › *Sequence inside the build* lists the build steps (1–11) in one line each. The owner and an analyst checked them against the 32 designed screens (`docs/design/SCREENS.md`) and found the sequence incomplete. P-1 turns it into the **build map** the project follows next. It is documentation only.

## The owner's rules for the map (mandatory)

- **No implementation details.** A step names its goal and points to what supports it: its screens (SCREENS.md row numbers), its ADRs, the owning documents, the findings it closes, and the deferred decisions it settles. **How** a step is built is decided in that step's own plan, because details change as the project evolves.
- **A direction, not a contract.** The map states that it changes as the project learns. It does not bind the work to it rigidly.
- **Targets, not dates.** Don't tie steps to days or weeks. The *Timeline* section may be reworded into targets in the same spirit: propose it in the plan. The defence and the end of the project are real external deadlines; they stay.

## What the map must settle

**1. Every screen belongs to a step.** Today six are unassigned. The analyst proposes:
- **4** About / Contact → step 3, the public site (it reads the platform's public contact).
- **8** 404 / error / offline, and **9** account settings → step 1 (the foundation's shells). The forced password change in row 9 belongs to F-5.
- **12** owner overview and **25** admin overview → a **new final step**. They compose figures from every module (conventions § overview), so they come last.
- **29** admin users → step 4, with owner linking: both manage accounts.

Check every one of the 32 rows. Propose any other change.

**2. Each step's supporting documents.** For example:
- the ADRs, and the conventions sections for the modules it builds;
- the findings it closes: 8 (the removable filter tag, at the start of the data-reports work), 10 (amenity icons), 11 (the first nested write: the admin's space creation), 14 (the owner's audit screen design, with the audit work), 15 (the payment constraint's two causes, with the payments endpoint);
- the deferred decisions it settles, listed in `docs/plans/foundation.md` › A-3:
  - the scheduler mechanism: the front desk;
  - photos: the space-management work;
  - CSV exports: finance;
  - live-status delivery: the directory;
  - charts: finance;
  - the map: the admin's space editing places a pin on a map, so the map belongs to step 2, not step 3;
  - date inputs.

**3. Ordering notes**, kept to the reasons only. For example:
- the directory's live status shows "no live state" until the front desk exists;
- the overviews come last.

## Parallel work (read before planning)

**Worker A** runs at the same time in the MAIN folder `C:\Users\basel\masaha`, on F-5 (`feat/auth`, or `feat/auth-api` if split). Never touch that folder.

**Shared file: `docs/plans/v1-mvp.md`.**
- P-1 edits ONLY *Sequence inside the build*, and *Timeline* if the owner approves the rewording.
- F-5 edits ONLY *Planned API surface*: the password change moves to `/me/password`.
- Never edit the other's section. If both change the status line's date, keep the later date when rebasing.

**Not yours:**
- `docs/plans/foundation.md`: worker A's, since F-5 edits it. Step 1 of the map points to the foundation items (F-5 to F-7) instead of copying their contracts.
- All code, and every other document.

If P-1 truly needs another file, say so in the plan first.

**Before opening the PR:** fetch and rebase on the latest `main`. Whoever merges second rebases, and resolves any conflict by keeping both sides.

## Out of scope

- Implementation details, schedules in days or weeks, and any change to a decision.
- `docs/plans/foundation.md` and every file outside `docs/plans/v1-mvp.md`, unless the plan justifies it.

## Verification and PR

- Every relative link and anchor resolves: SCREENS.md rows, ADRs, findings, conventions sections.
- Every one of the 32 screens appears in exactly one step: list the check in the PR's Evidence.
- One owner per fact: no contract or decision is copied; the map links.
- `npx prettier --check .` and `npm run lint` pass, run from the uppercase `C:\` path (finding 9).

The PR follows workflow §3:
- labels `docs` + `area:docs`, assigned to me (`--assignee @me`);
- the description template, with `@coderabbitai ignore` in the body;
- no AI attribution.

Don't merge.
