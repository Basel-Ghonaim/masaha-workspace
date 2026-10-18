# Review — PR #35 (F-5b3a, sign in and register by email, after the rework)

You are the **independent reviewer** of PR #35 in `C:\Users\basel\masaha`. You don't build, fix or merge.

## Budget (hard limits — the owner's)

- **At most 2 subagents.** No workflows.
- **The whole review stays under 800,000 tokens**, this conversation and both subagents together. Aim for about 250,000 per subagent.
- **Read the diff, not the repository.** Use `git diff origin/main...acee7f6 -- <paths>` and `git show acee7f6:<file>` for the files the PR changes. Don't read files the PR doesn't touch, except the few named below.
- **Read the documents only where named.** No full reads of the docs set.
- **Each subagent's report: at most 700 words.** Yours: at most 900.

## Rules

- **Read-only.** No edits, commits, checkouts or switches, installs, npm or test runs, database commands, or GitHub comments.
- **Pin everything to commit `acee7f6`,** compared with `origin/main`. On Windows git bash, prefix `git show` with `MSYS_NO_PATHCONV=1` if a path is mangled.
- **Report only concrete problems.** Each one gives the file and line at `acee7f6`, the scenario that fails, its severity (blocker / should-fix / nit) and the fix. No speculation.

## What the PR must be (the owner's decisions)

- **H1, the feature's shape:** `repository/` (the data calls), `hooks/` (`useXQuery`, `useX`, `useXForm`; keys in `hooks/queryKeys.ts`), `components/`, `services/` and `types/`. A folder that would be empty is absent.
- **H2:** one generic form hook in `shared/forms` (`useServerForm`), which takes the server call as an argument.
- **H3:** one exported unit per file, named after it.
- **H4:** the data layer is named `repository`, the session's included (`shared/session/repository/`).
- **H6:** components only render. They never touch `AppError`, error codes, `Retry-After`, a mutation, the transport or a query client. They get errors as text and view models.
- **H7, H8:** where state lives. H8 (Context) is marked experimental.
- **Exports:** a feature exports UI first, and a hook only when a higher layer composes it. Nothing internal leaves `index.ts`.
- **The account menu** is the `users` capability (`features/users`).
- **Tests per layer** (testing.md, *A feature, layer by layer*):
  - repository: the unit lane, with `fakeAdapter`;
  - hooks: `renderHook`, through the transport's fake adapter;
  - components: rendering only.
  - **No production parameter that only tests pass,** and no test-only injection.
- **Unchanged from before the rework:** sign-in and register with every designed state; the 429 countdown as m:ss; `EMAIL_TAKEN` on the email field with a sign-in link; register sends the interface language; landing on a safe `next`; `FocusLayout`; the account menu with sign-out and its error.

## The split

### Subagent 1 — correctness and security

**Its files:**
- `shared/forms/**`;
- `features/auth/**`;
- `features/users/**`;
- `shared/session/**` (the rename only: confirm it is a pure move);
- `pages/site/auth/**`;
- the account parts of `pages/site/shell/`;
- `packages/shared/src/core/fieldErrors.ts`;
- the password rules in `users/passwordPolicy.ts`;
- the API's `validate.ts`.

**It checks:**
- `useServerForm`: the resolver gives the contract's field codes; server field errors land on the right fields in display order; the form-level failure; pending; a double submit; a stale failure cleared on a new attempt;
- `useFormFailure`: rate limit with a countdown reaching zero; offline with retry; the general error with its reference;
- the sign-in and register hooks: the session is held before `onSuccess`, and `onSuccess` still runs when `RequireGuest` unmounts the page; the language is added;
- sign-out: its pending and failure states; the menu stays open while pending;
- the API's `validate()` behaviour is unchanged (the diff of the mapping's move);
- `passwordRules` agrees with `passwordSchema`, including Arabic letters and digits;
- the session rename changes no behaviour;
- whether any test would pass with broken code.

### Subagent 2 — conformance, tests and documents

**Its files:**
- the tree and every `index.ts` the PR adds or changes;
- every test file's titles and assertions (not their setup);
- `docs/frontend/architecture.md` §1–§4;
- `docs/development/testing.md`;
- `docs/architecture/findings.md` (finding 25);
- `docs/plans/foundation.md` (the F-5b3 entry);
- the copy files the PR changes;
- `CircleIcon` in the design system;
- the commits' subjects and bodies;
- the PR body (`gh pr view 35 --json body`, read-only).

**It checks:**
- H1–H8 and the export rule hold in the code, and the documents state them truly, with H8 marked experimental;
- tests per layer: every repository call and every hook with logic is tested in its lane; no component test re-asserts a hook's logic; no test-only parameter or injection exists anywhere;
- every user-facing string is in both catalogues, and the lines not in a design are listed for approval in the PR;
- the design-system rules: no colours or arbitrary values outside the layer, and logical classes only;
- the 8 commits are atomic, with Conventional subjects of 50 characters or fewer, and no attribution;
- the PR body has the workflow §3 sections, and its Evidence shows the before/after counts and the manual end-to-end check.

## Your output

Write **one file**, `C:\Users\basel\Downloads\REVIEW35_REPORT.md`:
1. **A verdict in one line.**
2. **The findings,** most severe first, deduplicated across the two subagents. Each gives its severity, the file and line, the failing scenario and the fix.
3. **"Verified OK":** a short list.

Then stop. The owner's analyst verifies the findings and writes the fixes list.
