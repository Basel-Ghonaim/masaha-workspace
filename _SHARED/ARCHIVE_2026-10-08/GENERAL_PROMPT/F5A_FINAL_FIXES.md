F-5a — final review fixes for PR #25 (supersedes F5A_REVIEW_FIXES.md)

Two independent reviews ran against commit e56664f. The owner's analyst verified the blockers and the key findings in the code. This is the ONE list to apply.

Read `C:\Users\basel\Downloads\F5A_REVIEW_2.md` for every item's exact location, failure scenario and suggested fix. Where this file differs from that report, THIS file wins. Do not read F5A_REVIEW_FIXES.md; it is superseded.

Apply everything below on this same branch and PR (`feat/auth-api`). Each fix comes with its test, and each commit is an atomic unit. Then re-run every lane, update the PR description, and add the review comment (part E). Don't merge.

## A. Owner decisions (approved)

D1 — Google account linking (report Q1, option B):
- Link automatically ONLY when Google is authoritative for the address: `@gmail.com`, or the ID token carries an `hd` claim.
- Otherwise, refuse the link. The person signs in with the password, or resets it. A clear error code goes into api-contract and both catalogues.
- An authoritative link runs in one transaction: set googleSubject only where it is still null; clear the existing password; end every session of the account.
- Record the rule and its reason in security.md › Sign-in methods. F-5b's toast says the password was removed; add that line to F-5b's entry.

D2 — /me/password (report Q2, option B):
- CURRENT_PASSWORD_INCORRECT counts under a per-USER failures limit, using the race-free reserve/refund of B1.
- The current password is skipped only when BOTH the token's claim and the database flag say a change is pending.
- A Google-only account sets its first password through the reset email, not /me/password.
- The write is a compare-and-set (B2).

D3 — Abuse bounds (report Q3, option 2, in this PR):
- count every registration per address before hashing (20 an hour);
- failed Google tokens get their own per-address policy, which refuses only /auth/google;
- reset checks the token (read-only) before hashing.

Option 3 (a per-address ceiling for signed-in requests) waits for F-7: record it in ADR 0014's deviations or as a finding.

D4 — Reset email (report Q4, a + b, with S8):
- no name in the greeting (record the divergence from the design in the PR);
- a daily count of delivered reset emails per requesting address (10).

D5 — Grace branches (report Q5): option A now. Correct security.md's Reuse sentence to say what holds, and record a finding that within the 30 s grace a replayed token can start an independent branch (option B, a deterministic successor, resolves it later).

D6 — Clock (report Q6, option a): wire one clock in createApi. Rate-limit windows and Retry-After use one source of time, so the database's and the API's clocks are never mixed.

D7 — Request log line (report Q7, option a): a synchronous stdout destination, and §10/§12 state that the access line is best effort online.

D8 — Tests (report S9): add focused UNIT tests with plain-object fakes and a fixed `now` for the service rules:
- the grace boundary (30,000 vs 30,001 ms) and the TTLs;
- the credential order and the dummy compare;
- every Google branch, including the authoritative-domain rule;
- the current-password rule;
- how the failures-only limit counts a 4xx, a 5xx and a success.

The API lane keeps the database-dependent proofs.

D9 — R2: amend conventions §8 R2 to admit what the composition root and the seed need from a module's index: controller factories, port adapters, `hashPassword` for the seed. Remove the unused exports.

D10 — Findings to record (not build):
- no absolute session lifetime (each rotation grants 7 more days);
- the reset email's copy lives outside the web copy catalogue;
- finding 19 widened to the email's colours, fonts and inline CSS, and left Open until the owner accepts it;
- the grace-branch item from D5;
- a per-address ceiling for signed-in requests (D3, option 3).

Correct findings 17 and 18 per S6 and S12.

D11 — overview.md › Built: unchanged. Authentication becomes Built with F-5b.

D12 — The Arabic copy (three error lines and the reset email) is approved, except the greeting (D4). Any new error code from D1 or D3 gets both catalogues; its Arabic needs the owner's approval in the PR.

## B. Blockers (fix exactly as the report says, with these notes)

- **B1 (report B1):** reserve, then refund, for every failures-only limit:
  - count atomically before the attempt;
  - on success or a 5xx, refund before answering, only within the same window;
  - remove `check` and `peek`.

  The Promise.all tests as specified.
- **B2 (report B2):** one per-user lock, `FOR NO KEY UPDATE` on the users row, owned by `users`, taken first by EVERY transaction that writes a user's refresh tokens:
  - login, register and Google issue under the lock, with the hash re-checked by equality;
  - refresh locks, then rotates, and asserts markRotated;
  - logout and the suspended-refresh revokeAll run in a transaction;
  - /me/password writes with a compare-and-set.

  bcrypt stays OUTSIDE every transaction. Interleaving API tests as specified. Record the mechanism in conventions §13. Needs S5 first.
- **B3 (report B3):** the replacement depends on delivery:
  - issue only inserts;
  - on sent:true, delete the user's OTHER unused links (`id < new`);
  - on sent:false, delete the new token, so the delivered link stays live;
  - log every refusal once, with a fixed reason and no address.

  The two tests as specified.

## C. Should-fix (report S1–S14, as written there, with these notes)

- **S1:** NODE_ENV becomes required (no default). Cookies are Secure unless development. TRUST_PROXY is required in production. Env tests for each refusal.
- **S2:** one env-to-ports function in app.ts, called by every entry. The email settings become a discriminated union in env.ts.
- **S3:** `users.maySignIn`, used by forgot.
- **S4:** constraint-aware conflicts. Register maps only the email key to EMAIL_TAKEN. A concurrent first Google sign-in re-reads by subject. The link becomes conditional (`googleSubject: null`).
- **S5:** an optional `tx` on the seven repository functions, threaded through the services.
- **S6:** delete expired tokens inside rotate, and used reset tokens in the reset transaction. Correct finding 17.
- **S7:**
  - Google key-fetch failures become 503 and are not counted;
  - the email caps distinguish a cap from an infrastructure error;
  - one warn line per unsent email, with codes only, never nodemailer's message;
  - a try/catch around the inner send.
- **S8:** textSchema refuses control characters, including line breaks. Unit tests in packages/shared, with its test script (also the email and password schemas).
- **S10:** every listed test gap, and drop the redundant proofs.
- **S11:** split the lint elements into `infrastructure` and `root`. Forbid modules, platform and infrastructure → root, and exempt `*.test.ts` in their own block. Files placed directly under modules/ are `unplaced`. Add a unit-lane test that lints in-memory probe files through ESLint's API.
- **S12, S13, S14:** the documentation pass exactly as listed:
  - the status lines split into built and not built;
  - the rate-limit digest wording;
  - R5, R6 and §1–§2, §10, §12, §13;
  - ADR 0003's Revised line;
  - data-model's key-as-primary-key exception;
  - api-contract §3 (503) and §5 (422 and 429);
  - README "twelve Work Items";
  - the stale lines: architecture.md "F-5 builds the guards" → F-5b, and conventions §1's text normalisation → packages/shared.

## D. Nits (report N1–N10)

- **N1 to N9:** fix them if each is small and safe; otherwise list it in the PR as not done, with the reason.
- **N10:** fold it into D2.
- Commit-title history: don't rewrite it (no interactive rebase); mention it in the PR.

## E. When done

1. Update the PR description so it describes the FINAL state:
   - scope;
   - decisions D1–D12;
   - the new error codes and their copy;
   - the new findings;
   - Evidence, with every lane run (state what wasn't run);
   - the Definition of Done.
2. Add ONE PR comment titled "Review fixes": a table with every item id from this file, its severity and the commit that fixed it, or "not done" with the reason. No AI attribution anywhere.
3. Stop. The owner's analyst re-checks the fixes before merge.
