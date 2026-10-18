# PR #45 — review fixes (one list)

A light independent review ran on `e5bf577` (no blockers); the analyst verified items 1–5 in the
code. Fold each fix into the commit it corrects (fixup + autosquash, `--force-with-lease`); no "fix"
commits. Then post ONE "Review fixes" comment and update the PR description. No subagents.

**Keep this round tight:** only these items, the smallest change that closes each. Superpowers per
workflow §10: `receiving-code-review` to check each item first (push back with reasons if one is
wrong), `verification-before-completion` for every claim.

## 0. Rebase, only if needed
PR #44 (the admin's spaces API) may merge before you start; it also edits
`docs/backend/conventions.md` (§8 *Transactions*, the status line). If GitHub then shows #45
`DIRTY`, rebase on `origin/main` and keep both sides (your §2 and R8; its §8 rule and status line).
If it is still `CLEAN`, don't rebase.

## Must fix
1. **`useResetPassword` keeps the new password in the cache** (`hooks/reset-password/useResetPassword.ts`,
   no `gcTime`): the same leak as finding 34. **Fold it into commit 3** — `gcTime: 0`, the same
   comment, and the same "answered and unmounted → the cache holds no password" test — and make
   finding 34's evidence and resolution cover the four hooks. (Make the break once: remove `gcTime`,
   see the test fail, restore.)
2. **`docs/development/engineering-principles.md:32`** still prescribes "Factory functions with
   injectable defaults … `createService(repo = createRepository())`", against the rule commit 2
   wrote. Reword it to the rule in one line and link conventions §2 (commit 2).
3. **`docs/plans/foundation.md:33`** still says "Whoever merges second rebases." Drop or reword it to
   point to workflow §9 (commit 2).
4. **`docs/development/testing.md` §5** lists CI's checks without `format:check`, so the list now has
   two owners that disagree (setup.md › CI and `ci.yml`). **Replace the list with a link** to
   setup.md › CI (commit 4).
5. **`useResendLinkForm.component.test.tsx:49`** passes its own `{ timeout: 2500 }`, now shorter than
   the lane's 3 s. Drop the override (commit 1), so finding 28's "no test sets its own timeout" and
   the PR body are true.

## Nits — fix (one owner per fact; the owner is strict about duplication)
6. **Workflow §10 restates facts other places own:**
   - "fixes fold into their commits, with ONE 'Review fixes' comment" is a commit rule: state it once
     in workflow §3 *Commits* (its owner) and let §10 and the `open-pr` skill link to it;
   - §10's general precedence ("the prompt, then these documents, then the project's skills") is
     CLAUDE.md's *Decision precedence*: §10 keeps only that a plugin's skills rank below the project's
     skills, and links CLAUDE.md for the rest;
   - "a red test is never committed" is owned by testing §3 rule 5: §10 links it instead of restating
     it.
   (Commit 6.)
7. **`devServer`**: parse the port as plain decimal digits only (refuse `"0x14C8"`, `"1e3"`), with
   one test case, and word its error/comment to say a bad value fails the dev server, `vite build`
   and the Vitest lanes alike (commit 5).

## Checks — don't re-run what already passed
- Lint and typecheck on each rewritten commit.
- On the head, once each: `test:unit` (devServer), `test:component` (items 1 and 5). Skip
  `check:classes`, `test:api`, `build` locally; CI runs every lane.
- Report once CI is green and GitHub shows `CLEAN`: the head, what changed per item, the break you
  saw fail for item 1, the counts. Don't merge.
