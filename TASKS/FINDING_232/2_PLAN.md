# Plan — FINDING_232

## Summary

Remove the unused exported `PASSWORD_RULES` list while keeping `PasswordRule` as the same four-ID literal union and leaving `passwordRules()` behavior unchanged. Replace the test's list assertions with an assertion on the returned record's key order, update the four stale comments, and resolve finding 232 after the PR number is known.

## Contract

**Scope:** Only the shared password policy and its unit test, the two named comments under `apps/web/src/features/users`, finding 232, and its findings-index entry.

**Acceptance criteria:**
- `PASSWORD_RULES` is removed; `PasswordRule` remains `'minLength' | 'letter' | 'digit' | 'bytes'`; `passwordRules()` is otherwise unchanged.
- The unit test asserts `Object.keys(passwordRules('x'))` is `['minLength', 'letter', 'digit', 'bytes']` and contains no assertions or imports for `PASSWORD_RULES`.
- Both feature comments and the two policy doc comments describe the password policy as a line, not a checklist.
- Finding 232 is marked resolved with a dated resolution naming the actual PR; its index entry moves from Open to Resolved.
- The requested failing-test demonstration and every planned verification command pass in their proper final state.

**Out of scope:** Any runtime behavior change, any other source/document changes, refactoring, dependency changes, and changes to generated files beyond what the requested shared build necessarily produces.

## Reading done

Read `CLAUDE.md`, `docs/development/workflow.md`, `docs/README.md`, finding 232, `docs/architecture/findings/README.md`, `docs/features/users.md`, `docs/backend/security.md`, `docs/architecture/shared-package.md`, `docs/development/testing.md`, `docs/development/engineering-principles.md`, `packages/shared/src/users/passwordPolicy.ts`, its unit test, both named feature files, and the root/shared package manifests. Searched `packages/` and `apps/` for `PasswordRule`, `passwordRules`, and `PASSWORD_RULES`.

The search found `PASSWORD_RULES` only in the policy module and its unit test. The type is locally derived from the list; the API temporary-password generator and the web's password-rules hook consume `passwordRules()`. No additional reader needs changing.

## Prompt decisions as planned

- Replace the derived `PasswordRule` type with the explicit four-member literal union, retaining all currently used IDs.
- Leave `passwordRules()` implementation and policy behavior unchanged.
- Replace the two `PASSWORD_RULES` test cases with an assertion that the record keys appear in the four-condition order.
- Demonstrate the new assertion fails by temporarily omitting `bytes` from the returned record, run the focused unit test, then restore the implementation before final verification.
- Reword both policy comments and the two `features/users` comments to refer to the policy's one line.
- Mark finding 232 resolved and move its entry to Resolved in the index. Use the actual PR number in its dated resolution before pushing.
- Do not push to `main` or merge. Use one Conventional Commit with a subject no longer than 50 characters and a body, with no tool attribution.

## Stronger decisions

- **Workflow verification:** The prompt lists the shared build and repository checks; workflow phase 4 also calls for the full build and `check:build`. **Why:** the shared package feeds both apps and its `dist` is rebuilt by the required shared build. **Cost:** additional build/check time. **Recommendation:** include `npm run build` and `npm run check:build` after the prompt's required checks, and run all checks on the final state. No browser check is planned because no screen or UI behavior changes.
- No other in-scope prompt or document decision can be strengthened, and no project rule needs weakening.

## Related findings

- **Finding 232 — folded.** This work directly meets its “Resolves when” condition, including both comments and the retained `PasswordRule` type. Cost: one finding file and one index edit in the same commit.
- No other finding is folded; no other open finding read for this task applies to the scoped change.

## Files to change

1. `packages/shared/src/users/passwordPolicy.ts` — delete `PASSWORD_RULES`; define `PasswordRule` as the explicit four-ID union; rewrite the two checklist doc comments to describe the single policy line; leave `passwordRules()` unchanged.
2. `packages/shared/src/users/passwordPolicy.unit.test.ts` — remove the `PASSWORD_RULES` import and its two assertions; add `it('lists the policy conditions in order', ...)` asserting `Object.keys(passwordRules('x'))` equals `['minLength', 'letter', 'digit', 'bytes']`.
3. `apps/web/src/features/users/hooks/settings/usePasswordChangeForm.ts` — change “rules' checklist” in the doc comment to the policy's line.
4. `apps/web/src/features/users/components/forced-change/ForcedPasswordChangeForm.tsx` — change the “rules ticking as the user types” comment to describe the policy's line.
5. `docs/architecture/findings/232-password-rules-is-read-only-by-its-test-and-two-comments-still-say-checklist.md` — change status to Resolved, date it 2026-11-26, and add a dated resolution describing the removal and both comments, naming `#PRNUM` until the real PR number is inserted before push.
6. `docs/architecture/findings/README.md` — move finding 232's unchanged number/title from Open to Resolved.

No other layer's files or shared files owned by another open item are included. No design issue applies: no screen changes.

## Tests and breaks

- **Unit (`packages/shared/src/users/passwordPolicy.unit.test.ts`):** Assert the ordered keys of `passwordRules('x')`. Omitting `bytes` from the returned record must make this assertion fail. Existing unit cases continue to prove each rule's values, byte boundaries, and agreement with schema acceptance.
- **Demonstration:** With that test in place, temporarily remove the `bytes` property from the return object and run only the new test; observe failure, restore the property, and do not retain the deliberate break.

## Review Focus

The new key-order assertion uses only `'x'` and proves the keys/order, not each condition's values or the schema's acceptance rule. The existing tests cover those values and the schema relationship; verify they remain unchanged and passing.

## Commit

One commit:

```text
refactor(shared): remove unused password rules

Remove the exported list now that the UI renders one policy line.
Keep the condition IDs typed independently and verify the returned
record's keys.
```

Stage only the six paths listed above. The PR title will match the subject.

## Verification and PR

From `C:\dev\masaha\app`, after approval and on `chore/finding-232`:

1. `git status --short --branch`; require a clean tree. `git fetch origin`; `git switch -c chore/finding-232 origin/main`.
2. After implementing the planned test, temporarily omit `bytes` from `passwordRules()` and run:
   `npm run test:unit -w @masaha/shared -- src/users/passwordPolicy.unit.test.ts -t "lists the policy conditions"`
   Observe the expected failure, restore `bytes`, and confirm no deliberate mutation remains.
3. Run `npm run build -w @masaha/shared` to rebuild `dist`, then run each final-state check:
   `npm run format:check`
   `npm run lint`
   `npm run typecheck`
   `npm run check:links`
   `npm run check:conflicts`
   `npm run test:unit`
   `npm run build`
   `npm run check:build`
4. Before finalizing the finding reference, run `gh pr list --state all --limit 1` and `gh issue list --state all --limit 1`; use the next number specified by the prompt's rule (expected #160). Replace `#PRNUM` with that actual PR number, stage only the finding file, and amend the one commit with `git commit --amend --no-edit`.
5. Push `chore/finding-232`; open a PR assigned to `@me`, with title `refactor(shared): remove unused password rules` and the body below. Apply the `chore` type label and relevant existing area label(s) per workflow.
6. Wait for CI by checking `gh pr checks <n>` at two-minute intervals, at most 20 times; then verify `gh pr view <n> --json mergeStateStatus` reports `CLEAN`. Do not merge. Finish on `main` as the prompt directs.

**PR body (use after all listed checks pass):**

```markdown
## Summary
- Remove the unused `PASSWORD_RULES` export while retaining the four condition IDs in `PasswordRule`.
- Keep `passwordRules()` unchanged and test the returned record's ordered keys.
- Update the policy and users-feature comments to describe the single-line password condition.
- Resolve finding 232.

## Scope / Acceptance criteria / Out of scope
- In scope: the shared policy and unit test, the two named users-feature comments, and finding 232 plus its index entry.
- Acceptance: all four IDs remain typed; the record's key order is tested; the finding is resolved.
- Out of scope: runtime behavior changes, unrelated refactors, and other files.

## Change type
Refactor.

## Evidence
- `npm run build -w @masaha/shared`
- `npm run format:check`
- `npm run lint`
- `npm run typecheck`
- `npm run check:links`
- `npm run check:conflicts`
- `npm run test:unit`
- `npm run build`
- `npm run check:build`
- The new unit assertion failed when `bytes` was temporarily omitted, then passed after restoration.

## Definition of Done checklist
- [x] Acceptance criteria met; scope kept.
- [x] Build, lint, typecheck, and tests pass.
- [x] Finding status and index are updated.
- [x] One atomic commit; PR ready for owner review.
```

## Decisions needed from the owner

None beyond approval of this plan. No branch or repository file will be changed until approval.

## Differences

None found: the code, test, finding evidence and “Resolves when” condition, comment locations, and requested resolution all agree with the prompt.
