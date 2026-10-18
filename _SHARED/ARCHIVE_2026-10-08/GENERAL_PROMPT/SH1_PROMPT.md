# SH-1 — Structure `packages/shared` by capability

**Worker B** · folder `C:\Users\basel\masaha-b` · branch `refactor/shared-by-capability`

**Do not start before F-5b2 (the session, worker A) is merged.** The owner will tell you when.

**Size cap:** use at most 4 subagents in total. Do not run any workflow.

## 1. How to work

- **Start with the `start-work-item` skill.**
- **The owning documents for this item:**
  - `docs/backend/conventions.md` §3 and §7 (the module list and the level map);
  - `docs/api/api-contract.md` §2 (the envelope);
  - `docs/frontend/architecture.md` §1 and §3.
- **Read the whole of `packages/shared`,** and every importer of `@masaha/shared` (`git grep "@masaha/shared" -- apps packages`). Read also `eslint.config.js`, the API level map and its test, `apps/api/test/levelRule.unit.test.ts`.
- **When finished, follow the `open-pr` skill.**
- **The owner's rules the skills don't carry yet:**
  - every test's title states what it asserts;
  - on a lockfile conflict, take main's `package-lock.json` and run `npm install`;
  - **report only once CI is green on the pushed head**;
  - **review fixes are folded into the commits they correct** (fixup + autosquash, `--force-with-lease`), with ONE "Review fixes" comment.
- **The Issue:** if the owner created one for this item, put `Closes #<n>` in the PR. Ask for the number if you don't have it.

## 2. Why

`packages/shared` is the contract between the web and the API in code. Today it is a flat set of files, and some mix capabilities: `auth.ts` holds the languages, the email field, the sign-in schemas, the password change and the roles. Every endpoint will add its contract here, so this item gives every fact one obvious home before the features arrive.

**This is a pure refactor:** no behaviour changes, no new contract, no new dependency.

## 3. Decisions already made (do not reopen)

The owner approved these.

### The structure, with clear names

```
packages/shared/src/
  core/                       the foundation: knows no capability; imports only zod
    errors.ts                 error types, field-error codes, domain error codes
    envelope.ts               the success and error envelopes (api-contract §2)
    pagination.ts             PaginationMeta, the page query schema and limits
    fields.ts                 field schemas any capability uses: textSchema, emailSchema
    languages.ts              LANGUAGES, Language
    index.ts
  lookups/                    L0
    amenityIcons.ts           AMENITY_ICON_KEYS, AmenityIconKey
    index.ts
  users/                      L1
    passwordPolicy.ts         the password policy both sides check
    requests.ts               the account's name field, changePasswordSchema
    responses.ts              Role, PasswordChanged
    index.ts
  space-links/                L2
    responses.ts              SessionSpaceLink (a user's link to a space)
    index.ts
  auth/                       L3
    requests.ts               register, login, Google, forgot, reset-check, reset schemas
    responses.ts              Session, SessionUser, GoogleSession, ResetCheck
    index.ts
```

Each symbol lands in the folder of the capability that owns it. Where the plan finds a symbol whose owner is unclear, list it in the plan with your proposal. Don't guess.

### The rules (R1–R7) — they go into the document of §4

| Rule | Why |
|---|---|
| **R1** One folder per backend module that has a contract, with the module's own name and level (conventions §7). | You find a fact from its capability's name, the same in the API, the web and here. |
| **R2** Each folder has `index.ts`, its only entry; `requests.ts` for what enters the server (Zod schemas and their inferred types); `responses.ts` for what the server answers (types); a rule both sides compute gets its own file named after it (`passwordPolicy.ts`). A file that would be empty is absent. | One predictable shape per capability. |
| **R3** `core` imports nothing but zod. A capability imports `core` and capabilities at **lower** levels only, through their `index.ts`. Lint enforces it. | No cycles or tangles as it grows. |
| **R4** Consumers import by capability path, `@masaha/shared/auth` or `@masaha/shared/core`. There is no root barrel, and deep paths are blocked by the package's `exports`. | An import says where a fact lives. |
| **R5** Only what crosses the wire, or a rule both sides must compute, belongs here. Never a web-only type or a database type. | The package stays small and means one thing. |
| **R6** Requests are Zod schemas with inferred types; responses are types only, with no runtime validation on the web. | Validation happens where data enters the server; the typecheck on both sides keeps the shapes in step. |
| **R7** Names: `registerSchema` / `RegisterRequest`; a response is named for its resource (`Session`, `SpaceSummary`), with no `Dto` suffix. | Names you can predict. |

**And the rule this enables:** every request body and every response the web uses is defined once here, and both apps import it. The API's mappers return these types, and the web's endpoint calls are typed by them.

### P3 — domain error codes

They stay **one list in `core/errors.ts`**, grouped by capability with a comment per group. Revisit if it grows past about 50 codes; say so in the document.

### The envelope moves to `core/envelope.ts`

- **The web:** `shared/api`'s `ApiEnvelope`, and anything F-5b2 added that uses it, imports the shared types instead of its own.
- **The API:** `sendSuccess` and the error handler are typed by the same envelope types.
- **No runtime change.**

### Exports and resolution

- **Exports:** in `packages/shared/package.json`, one subpath pattern replaces the `"."` entry:
  ```json
  "./*": { "@masaha/source": "./src/*/index.ts", "types": "./dist/*/index.d.ts", "default": "./dist/*/index.js" }
  ```
  Check that the build emits `dist/<capability>/index.*`.
- **Resolution:** check that both apps resolve the subpaths in dev, test, typecheck and build: the API (`NodeNext`, `tsx --conditions`, Vitest) and the web (`bundler`, Vite's client and SSR conditions).
- **Proof:** with `packages/shared/dist` deleted, every lane passes, and so do `build` and a dev smoke.

### Lint (R3)

- **Elements:** add `packages/shared/src/core` and `packages/shared/src/*` to the boundaries setup.
- **The level map:** reuse the API's level map. Don't write a second copy: one map, read by both blocks.
- **The test:** extend the existing probe test (`levelRule.unit.test.ts`, or its web or shared twin) with in-memory probes:
  - `core` importing a capability fails;
  - `users` importing `auth` fails;
  - `auth` importing `users` passes;
  - a deep import past a capability's `index.ts` fails.

## 4. The document: short, rules and why

- **Write `docs/architecture/shared-package.md`. Keep it short:** about 40 lines, no more.
- **Its sections:**
  - **purpose:** the contract in code, in one paragraph;
  - **the structure:** the tree, one line per folder;
  - **the rules R1–R7,** each with its one-line why (the table above);
  - **how to add a capability:** 3–4 steps;
  - **P3's note.**
- **No file-by-file listing.** It owns these rules, and nothing else repeats them.
- **Links to it, one line each:**
  - `docs/README.md`'s map;
  - `api-contract.md`: "its types live in code in `packages/shared`";
  - `conventions.md` §3: where the schemas come from;
  - `architecture.md` §3: where a feature's wire types come from.
- **No ADR.**

## 5. Scope

**In:**
- move the files and the symbols as in §3;
- update every import in `apps/api`, `apps/web` and `packages/shared`;
- the exports, resolution and lint changes;
- move the existing tests beside their files;
- the document and its links.

**Out:**
- any behaviour change;
- any new schema or type beyond moving `ApiEnvelope` and naming the error envelope;
- any rename of a public symbol, unless the plan proposes it with a reason and the owner approves;
- the copy catalogues, except an import path.

## 6. Tests and checks

- **Every lane passes,** with `packages/shared/dist` deleted: lint, typecheck, check:classes, unit (shared, API, web), component, API (`masaha_b_test`), build and `check:build`.
- **The lint probes of §3** are committed as tests.
- **The dev smoke:** web on 5320, API on 3320, `/api/v1/...` through the proxy.

## 7. Commits

Propose the split in the plan. Each commit builds and passes on its own. A likely one:
1. `refactor(shared): add the capability folders and subpath exports`, moving the files and updating every importer in the same commit, so nothing is broken in between;
2. `refactor(shared): share the envelope types`;
3. `feat(lint): enforce the shared package's levels`;
4. `docs(architecture): add the shared package's rules`.

## 7b. Parallel work — expect conflicts

**Worker A** works at the same time in `C:\Users\basel\masaha` on **F-5b3a** (sign in and register by email, the first feature). The owner decided to run both side by side and resolve the conflicts, not to avoid them.

**A adds two things to `packages/shared`,** in the old flat structure:
- the Zod-issue → field-code mapping, moved out of the API's `validate.ts`;
- the password rules' evaluation, beside `password.ts`.

A also adds new importers of `@masaha/shared` in the web (`features/auth`, `shared/forms`).

- **If A merges first,** rebase on `origin/main` at a commit boundary and fold A's additions into your structure: the mapping into `core/`, the rules into `users/passwordPolicy.ts`. Switch A's new imports to the subpaths, resolve every conflict keeping both sides' intent, and re-run every lane. Each rewritten commit must still pass on its own. Say in the PR what you moved.
- **If you merge first,** A moves its additions into your structure when it rebases.
- **Your files, which A won't touch:** the structure, `package.json` exports, the lint rule and its tests, `docs/architecture/shared-package.md`. **The shared zone:** `packages/shared/src/**` and the importers in both apps.

## 8. Pull request

- **Labels:** `refactor`, `area:api`, `area:web`, `area:docs`.
- **Review:** one independent review.
- No tool or AI attribution anywhere. Don't merge. Don't create an Issue.
