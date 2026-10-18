# Review — PR #47 (head `e840f15`, base `d8884c4`, nine commits)

## 1. Verdict

**Not ready to merge: no blockers, six should-fix findings.** The worst is the ninth commit, which contradicts itself on when the capability document is read.

## 2. Findings

1. **Should-fix: the reading order contradicts itself, and has two owners.**
   - These say the capability document comes first, then the sections it links: rules §5 and §9, the map's `features/` line, ADR 0018 and CLAUDE.md.
   - Workflow §2 › *Reading before work* and `start-work-item` step 3 put whole layer documents first, "**Then** the capability's document".
   - The by-kind list repeats the map's *read it when* lines, and they already differ. For security, the map says "…handles a password or a token…" and workflow leaves that out.
   - *Always* omits the findings' titles, which §4 requires.
   - **Fix:** §2 owns the order: the capability document first, then its linked sections. Replace the by-kind list with "open each document whose line matches". Add the findings to *Always*. The skill links §2 only.

2. **Should-fix: capability decisions restate rules owned elsewhere.**
   - `auth.md` lines 48–50 and 53 repeat four `security.md` rules (lines 53, 55, 58), although its own *Boundary* (line 24) leaves them to security.
   - `auth.md` lines 56 and 60 repeat architecture §2's guards and its one landing.
   - `spaces.md` line 52, "editable by the admin only while … unverified", is owned by security (§10 answer 2).
   - `users.md` lines 40 and 50 state sign-out "only once the server agrees" twice; architecture line 245 owns it.
   - **Fix:** link each in the "Owned by … and linked" line.

3. **Should-fix: *Behaviour* restates the endpoints' shapes.**
   - `auth.md` line 40 lists `RecoveryPosition`'s fields.
   - `spaces.md` *Read and edit* and *Hide, delete, restore* repeat the contract's `PATCH`, `hidden`, `DELETE` and `restore` text.
   - `lookups.md` repeats "a hidden governorate leaves with all its areas".
   - `space-links.md` repeats the admin row's fields.
   - **Fix:** one line of flow, and link the endpoint.

4. **Should-fix: a fact was lost (DS-1).** At the base, foundation §9 listed the public header: logo, directory, language switch, theme toggle, sign-in / account menu. At head it says only "a top header" and points to architecture §2, which describes only the dashboard's shell. **Fix:** add a site-shell bullet to *The two groups*.

5. **Should-fix: the rule on records contradicts workflow.** `documentation.md` §1 says "Records are never rewritten; only a link … is repointed". Yet workflow §7 allows an ADR's `Revised:` line (ADRs 0001–0004 and 0007 carry one), and workflow §4 and rules §3 allow a finding's resolution. **Fix:** §1 and §3 name all three allowed edits and link workflow §7.

6. **Should-fix: two statements in `spaces.md` are untrue at the code.**
   - "starts again … up to three times": `CREATE_ATTEMPTS = 3` (`space.service.ts:27`) is three attempts in all.
   - "audited … in its own transaction": the audit is written in the change's own `tx`.

**Nits:**
- `auth.md` line 52 dates "masked" to #25. At #25 the check returned the full email; masking came in #38 (2026-10-05).
- `spaces.md` line 39 says an edit screen "shows" the space editable or read-only. No such screen exists, so: "can show".
- The rules' §3 table row for the map lacks "when to read it", which §9 has.
- Rules §5 restates workflow §7's update trigger, and §7 restates the ADR threshold; keep only the links.
- ADR 0018's third numbered decision, the ADR clause, belongs in the rules.
- The request id is also shown in the lookups section's failures and in Google's failure area, not "only a form's failure" (architecture §5, conventions §10).
- Finding 38 says "36 entries before this one"; it should be 37.
- Conventions line 284 is missing a `)`.
- Architecture line 183: "a sign-in's hook" needs a capital A.

## 3. The length question

- **`auth.md` (1,477): duplication, not coherence.** About 250 words can leave, bringing it to about 1,230:
  - about 150 words of *Behaviour* repeat its own *Decisions* (the mutation's callback, the Google button without a client id, the m:ss countdown, the server-read step and its retry, the toasts);
  - about 75 words restate security (finding 2);
  - about 25 words restate the refresh lock and grace window, which conventions and security own.
- **`documentation.md` (1,498): mostly coherence** (the tables, the template, *Not adopted*). About 100 words can leave:
  - the records exemption, stated four times (§1, §3, §4, §8);
  - "no changelog in a header", stated twice (§3, §6);
  - the workflow §7 overlaps.
  - The rest justifies the length.

## 4. Verified OK

**Subagent 1 (duplication, nothing lost):**
- Every ledger row has one home, except DS-1.
- No platform document keeps a ledger fact behind.
- The departures:
  - (a) photos, (c) the dates, (d) DS-2 and (e) DM-4 are correct;
  - (b) the request id is right for the status states but too narrow;
  - (f) the smaller shrink is justified by the links, the kept examples and the audit list.

**Subagent 2 (truth, structure, rules):**
- **The code:** 6–12 decisions sampled per capability are true, apart from finding 6 and the nits. Every "built" claim is true, the code maps exist, and the PRs and dates match.
- **The template:** followed in all five documents. `spaces` has no web section, the classes are true, and there are no local paths.
- **ADR 0018:** about 445 words, no file names.
- **The triggers:**
  - workflow §7 and §5 link the rules;
  - CLAUDE.md stays a pointer;
  - the map stays a guide;
  - §4's findings rule has one owner.
- **Links:** none broken (1,437 links, 574 anchors), at head and at each commit.
- **The records:** they change only by ADR 0018 and findings 37–41, and findings 37 and 39–41 are accurate.
- **The commits:** nine, Conventional, subjects of 33–48 characters, no attribution.

**Tokens:** about 470,000 in all (subagents about 209,000 and 164,000, this conversation about 100,000).
