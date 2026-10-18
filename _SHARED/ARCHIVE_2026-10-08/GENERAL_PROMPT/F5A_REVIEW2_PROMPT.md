Second, independent review of PR #25 (F-5a, authentication API) — read-only

## Who you are and what you do

You are a principal engineer doing an independent, adversarial review of one pull request in a project you have never seen. You know nothing about it yet, so learn it from its documents first. Your output is a written report for the owner. You change nothing.

**The PR:** Masaha (github.com/Basel-Ghonaim/masaha), **PR #25**, branch `feat/auth-api`.
- Review the PR exactly at commit **e56664f**, against its base, `origin/main` (c427112).
- Another conversation may be fixing this branch while you work, so never read the moving working tree. Read only the pinned commit (see "Safety").

## Safety rules (mandatory)

- **Read-only.** No edit, no commit, no checkout or switch, no branch, no install, no push, no comment on GitHub, no database command, no test run.
- The repository is at `C:\Users\basel\masaha`. Use only commands that read git objects at fixed refs:
  - `git diff c427112...e56664f`, `git diff --stat …`, `git show e56664f:<path>`, `git log c427112..e56664f`, `git ls-tree -r e56664f`;
  - `gh pr view 25`, `gh pr diff 25`.
- For comfortable browsing, you may extract a snapshot into your session's scratchpad: `git archive e56664f | tar -x -C <scratchpad>/snapshot`. Never write anywhere else.
- Your only output file is the report, at `C:\Users\basel\Downloads\F5A_REVIEW_2.md`.

## Step 1 — learn the project (before reading any code)

Read, at commit e56664f (`git show e56664f:<path>`):
- CLAUDE.md;
- docs/development/workflow.md, engineering-principles.md, testing.md;
- docs/README.md (the map);
- docs/backend/conventions.md (the module rules, levels and layers), docs/backend/security.md;
- docs/api/api-contract.md, docs/architecture/data-model.md;
- ADRs 0001, 0002, 0003, 0009, 0010, 0012, 0013, 0014, 0015 in docs/architecture/decisions/;
- docs/plans/foundation.md (§ F-5a and F-5b);
- docs/architecture/findings.md.

Then read the approved plan of this Work Item: `C:\Users\basel\.claude\plans\ticklish-skipping-pixel.md`. Its "Owner amendments" section overrides the rest of it.

Then read the decisions approved while the work was under way, all binding:
- **Split:** F-5a is the API only; the web is F-5b.
- **Modules:** `sessions` (L0), `users` (L1), `space-links` (L2, minimum), `auth` (L3, the orchestrator, with the email port). Imports go only downward and only through index.ts, enforced by an ESLint level rule.
- **Forced password change:** a `mustChangePassword` claim in the access token. `/me/password` revokes all sessions, then opens a fresh session for this device: a new access token and a new refresh cookie.
- **Email:**
  - nodemailer plus Gmail SMTP behind a port;
  - modes `log` (development only) and `smtp` (required in production, or the API refuses to boot);
  - a per-recipient cap and a global ceiling;
  - no generic channel-verification layer, and no auth framework.
- **Reset token** (OWASP Forgot Password Cheat Sheet): only its hash is stored, it lives 1 hour, it is single use by one atomic statement, and forgot always answers 202. A read-only check endpoint exists. The link carries the token in the URL fragment (`#token=`).
- **Language:** register and the first Google sign-in accept the interface `language`.
- **Rate limits:** a custom limiter over PostgreSQL (express-rate-limit was dropped: it works after the response, which ADR 0014 forbids). Every write happens before the response. The keys:
  - sign-in counts failures only, keyed by IP + email, with a looser per-IP ceiling;
  - refresh is keyed by the user;
  - the general limit by the user, or by IP for guests;
  - forgot and reset by IP + email.

  Users sit behind shared coworking-space NAT.
- **Refresh reuse after the 30 s grace** revokes that token's family (`family_id`), never all of the user's sessions. Logout ends the whole family.
- **Password hashing** lives in `users`. EMAIL_TAKEN on register is an accepted trade-off.
- **Request id:** a UUID in the logs, the `X-Request-Id` header and the error envelope. Redaction covers secrets; request bodies are never logged.
- **The `requestId` → `idempotencyKey` rename:** the Prisma field only, `@map("request_id")`, no migration.

## Step 2 — review on these axes

Use subagents in parallel, one or two axes each, to go deep without losing context. Give each subagent the safety rules and the project context above. Every axis is judged against the project's own documents and the approved plan, not against generic taste. Cite the rule you rely on (the document and its section).

1. **Security.** Authentication and session flows, token handling, cookies, CSRF posture, enumeration, timing, brute force and concurrency (races under READ COMMITTED), Google account linking, reset-token lifecycle, email abuse, logging and redaction, environment and production defaults, header handling, error leakage. Think like an attacker; build concrete exploit scenarios.
2. **Architecture.** ADR 0012/0013 and conventions §7–§8:
   - the levels and index-only imports;
   - one capability per module, with each module owning its tables (R1);
   - the public entry (R2);
   - orchestration and transactions (R4);
   - ports only where allowed (R5);
   - shared knows no domain (R6);
   - the composition root;
   - whether the ESLint level rule really enforces the map (look for holes).
3. **Engineering principles.** engineering-principles.md: SOLID in its checkable form, "boundary now, generalisation at the second instance", explicit over magic, no premature abstraction, one owner per fact.
4. **Database.** The migration and the schema: naming, constraints, indexes (do the queries use them?), backfills, NOT NULL, transaction boundaries, isolation and locking, N+1, growth of tables (rate_limits, tokens), what the cleanup paths are.
5. **Scalability and operations.** The behaviour under concurrency and load, at a shared coworking IP, on serverless (ADR 0014: no work after the response; a function may be frozen; there are cold starts), and the cost of bcrypt and of database round trips per request.
6. **Tests.** testing.md: the lanes and "one behaviour, one lane". Coverage of every decision above; vacuous tests; missing negative and concurrency cases; determinism (time, randomness); test isolation; fakes vs real DB per R8.
7. **Code organization and file structure.** Layer responsibilities inside each module (routes → controller → service → repository); file naming and placement; cohesion; size of files and functions; dead code; duplication.
8. **Abstraction.** The right abstractions at the right level: the ports (email, Google), DI by factory functions, interfaces with one implementation, leaky abstractions.
9. **Types.** TypeScript strictness (no `any`, `unknown` narrowed at boundaries); types inferred from Zod; discriminated unions for outcomes; branded or opaque types where they'd prevent mistakes; type duplication between packages/shared and the API; unsafe casts.
10. **Code quality.** Readability, naming against the glossary and conventions, error handling (AppError, codes, envelopes), comments explaining why, consistency across modules, and anything a strong reviewer would block.
11. **Documentation and plan conformance.** Is every approved decision implemented exactly? Is anything built that wasn't approved? Are the docs updated in the same PR and TRUE (claim only what is built)? Are all deferred-document triggers met? Do findings 16–19 make sense?

**Rules for findings:**
- Verify every finding in the code at e56664f before reporting it: cite file:line and quote the relevant code. A finding you could not confirm is labelled UNVERIFIED.
- Prefer few, important, concrete findings over many vague ones. No style nitpicks unless they break a project rule.
- Severity:
  - **BLOCKER:** must be fixed before merge, for security, data loss, or a broken rule;
  - **SHOULD-FIX:** fix in this PR;
  - **NIT:** optional;
  - **QUESTION:** a decision for the owner.

## Step 3 — compare with the first review (only AFTER your own review is finished)

A first review already ran. Its fixes list is at `C:\Users\basel\Downloads\F5A_REVIEW_FIXES.md`. Do NOT read it before your own findings are written, so your review stays independent. Then, for each of your findings, say whether it is:
- **NEW**;
- **SAME** as an item there (give the item's id);
- **DISAGREES** with an item there (explain why).

List the first review's items you believe are wrong or unnecessary, with reasons.

## The report (`C:\Users\basel\Downloads\F5A_REVIEW_2.md`, in English)

1. **Verdict** in three lines: merge-ready or not, and why.
2. **Findings by severity,** each with:
   - id, axis, severity, and file:line at e56664f;
   - the problem;
   - a concrete failure scenario;
   - the rule or document it breaks;
   - a one-paragraph fix.
3. **Questions for the owner** (decisions), each with options and your recommendation.
4. **What is solid:** at most 10 lines, only what a future change must not break.
5. **The comparison with the first review** (step 3).
6. **What you could not check, and why.**

Be direct and specific; the owner will turn your report into fix instructions. When the report is written, stop. Reply with its path and the verdict.
