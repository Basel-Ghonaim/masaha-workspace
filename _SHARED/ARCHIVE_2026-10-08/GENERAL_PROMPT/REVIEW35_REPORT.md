# Review — PR #35 at `acee7f6` (against `origin/main` 0333fa4)

**Verdict: changes requested.** One blocker: the documents say no test-only parameter exists, and one does. The behaviour is sound otherwise. The rest is should-fix test and evidence work, plus nits.

## Findings

### Blocker

1. **A test-only parameter is still there, and the PR's documents say there isn't one.**
   - **Where:** `apps/web/src/shared/session/hooks/useSignOut.ts:15`, `useSignOut(dependencies = appDependencies)`. Its one production caller, `features/users/hooks/useAccount.ts:17`, passes nothing. Only `useSignOut.component.test.tsx:21,44` passes fakes. The services have the same seam: `refresh.ts:25`, `restore.ts:19` and `signOut.ts:9`, which the new page tests also use (`authPages.component.test.tsx:32`, `SiteAccount.component.test.tsx:59`).
   - **What fails:** `docs/development/testing.md:46`, `docs/frontend/architecture.md:174` and the PR body all say "No hook takes a parameter only a test passes". That is false, and the owner's rule is that no test-only injection exists anywhere. The parameter was already on `main`, but this PR edits these files and makes the claim.
   - **Fix:** drop the parameter and test `useSignOut` through `fakeTransport`, as `useAccount`'s test already does. For the services, do the same, or record a finding and word the documents truly.

### Should-fix

2. **Two documented test seams don't exist in practice.**
   - **Where:** `createAuthRepository(client = api)` (`features/auth/repository/authRepository.ts:13`) and `createSessionRepository`'s `client` (`shared/session/repository/sessionRepository.ts:15`). No caller passes either.
   - **What fails:** `architecture.md:156` documents the first. `architecture.md:222` says "a test passes a plain fake", but no test does: `sessionRepository.unit.test.ts:7` calls `createSessionRepository()`.
   - **Fix:** remove the unused parameters and correct both lines.

3. **Component tests re-check hook logic, though the PR body says they were "trimmed to rendering".**
   - **Where, and what each one repeats:**
     - `SignInForm.component.test.tsx:75-87`: the countdown re-enabling the submit. This waits on real timers for up to 3 s, and `useFormFailure.component.test.tsx:39` already covers it.
     - `SignInForm.component.test.tsx:89-104`: the stale failure cleared. Already in `useServerForm.component.test.tsx:136`.
     - `SignInForm.component.test.tsx:150-164` and `RegisterForm.component.test.tsx:90-105`: code-to-line mapping.
     - `RegisterForm.component.test.tsx:107-141`: `EMAIL_TAKEN` and server field errors. These repeat `useRegisterForm:81` and `useServerForm:98`.
   - **Also:** `RegisterForm.component.test.tsx:101` and `PasswordRules.component.test.tsx:57-59` assert the class `text-destructive`. That checks how it looks, not what it says.
   - **Fix:** keep one rendering assertion per view state and delete the logic re-checks. Assert the screen-reader "not met" text instead of the class.

4. **The `users` components have no tests of their own.**
   - **Where:** there is no `AccountMenu` or `AccountMenuSection` component test. `pages/site/shell/SiteAccount.component.test.tsx:92-147,168` does that rendering job, and also re-checks `useAccount`'s pending and failure logic (`useAccount.component.test.tsx:45,62`).
   - **Fix:** move the rendering tests to `features/users/components/`. Leave the page test only the swap between sign-in and the account.

5. **A schema issue at the root makes a form send `{}`.**
   - **Where:** `shared/forms/validation/schemaResolver.ts:29`. `toFieldErrors` returns `null` for an issue with `path: []`, so `?? {}` gives `{ values: {}, errors: {} }`.
   - **What fails:** for example, a future schema with a refine on the whole object. React Hook Form treats the empty errors as valid and calls `submit({})`. The comment on line 28 ("every issue is a field's") is false in that case. Today's two schemas can't hit this, but this is the one generic form hook.
   - **Fix:** turn `null` into a non-empty root error and add a unit test with `.refine(() => false)`.

6. **The Evidence counts compare against the wrong base.** The "before" column is the old PR head `31391a7`, not `main`. So the new tests (`fieldErrors`, `passwordRules`, the repositories, the forms tests) are counted on both sides. **Fix:** give the counts on `origin/main` against this head.

7. **"Forgot password?" goes to a route that doesn't exist.**
   - **Where:** `pages/site/auth/SignInPage.tsx:41` links to `/forgot-password` (`navigation.ts:17`). `routes.tsx` has no such route, so the link lands on NotFound until F-5b3c.
   - **What's missing:** neither *Out of scope* nor the acceptance criteria mention it.
   - **Fix:** hide the link until F-5b3c, or state it in the PR for approval.

### Nits

8. **H6:** `shared/forms/components/PasswordRules.tsx:22,27-28` calls `passwordRules(value)` and works out met or failed itself. Return the rule views from a hook (or from `useRegisterForm`).
9. **Hardcoded text:** `PasswordRules.tsx:47` renders `{' — '}` as screen-reader text. Move it into `forms.passwordRules.met/notMet` in both catalogues.
10. **The landing has two owners:** after `establishSession`, `RequireGuest` already sends the page to the same `safeReturnUrl`. Deleting the pages' `onSuccess` navigation (`SignInPage.tsx:36-38`, `RegisterPage.tsx:37-39`) leaves `authPages.component.test.tsx:73-98,120-133` green. Keep one owner, and test it.
11. **A weak focus test:** `SignInForm.component.test.tsx:134-146` answers with `email` first, so server order and display order agree. Answer `{ password, email }` and expect `email` to have focus. `useServerForm`'s tests have no focus or order test at all.
12. **The unmount guarantee is untested:** `useSignIn` and `useRegister` correctly use the hook-level `onSuccess`, but no test calls `unmount()` before the answer arrives. A test should unmount first, then expect both the session and `onSuccess`.
13. **H1/§3:** `shared/forms/validation/` is a folder name §3 doesn't define. Name it in §3, or file the helpers under `services/`.
14. **Atomicity:** `acee7f6` (`feat(users)`) also adds finding 25 (format `--check`). Give it its own `docs(findings)` commit.
15. **A stale comment:** `apps/web/src/test/fakeTransport.ts:11` still says "the hook, the endpoints".

## Verified OK

- **Session rename:** a pure move, with no change in behaviour. `sessionHint.ts` is 100% similar, and no old names are left.
- **API `validate()`:** unchanged after the mapping moved to `packages/shared/src/core/fieldErrors.ts`. Every issue code, the dotted paths, de-duplication, first-seen order, root issue → `badRequest()` and empty issues all match.
- **`passwordRules` agrees with `passwordSchema`:** both use the same `\p{L}`/`\p{N}` constants, so Arabic letters and ٠–٩ count in both. Both measure length in code units.
- **`useServerForm`:** contract codes; display order; focus; the form-level failure; pending (fields disabled, submit busy, so a double submit is blocked, Enter included); stale failure cleared.
- **`useFormFailure` and `useRetryCountdown`:** m:ss (65 s gives 1:05); the countdown reaches 0 and the submit re-enables; a missing or HTTP-date `Retry-After` gives a neutral wait; offline offers a retry; the reference shows only without a domain code.
- **Sign-in and register:** the session is held before `onSuccess`; the callback survives unmount; register sends the language; `EMAIL_TAKEN` lands on the email field with the sign-in link.
- **Safe `next`:** `//host`, `/\host`, full URLs, `/.//host` and encoded variants are all rejected.
- **Sign-out:** pending and failure work in the dropdown and the phone sheet; the menu stays open; a failed sign-out keeps the session.
- **Shape:** `FocusLayout`; H1–H4, H6 and H7 in code; H8 marked experimental; exports are UI only; one unit per file; `features/users` owns the account menu; repository tests are in the unit lane through `fakeTransport`, with no `vi.mock`.
- **Copy:** English and Arabic keys match, and the lines not in a design are listed for approval.
- **Design system:** no colours, arbitrary values or physical classes outside the layer; `CircleIcon` follows the icon set and is in the showcase and the icon test.
- **Commits and PR body:** 8 Conventional subjects of 50 characters or fewer, no attribution; the PR body has every workflow §3 section and a manual end-to-end check.

---

*Process note:* I launched a third, empty subagent by mistake. It did nothing (about 40,000 tokens), but it breaks the two-subagent limit. The whole review used about 420,000 tokens.
