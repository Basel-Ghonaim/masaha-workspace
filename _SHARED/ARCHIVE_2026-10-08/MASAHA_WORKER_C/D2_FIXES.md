# PR #47 — review fixes (one list)

The review gate ran on `e840f15` (no blockers, six should-fix, nine nits); the analyst verified items
1 and 6 in the documents and the code. Fold each fix into the commit it corrects (fixup + autosquash,
`--force-with-lease`; GitHub shows the PR `CLEAN`, so don't rebase on `main`); no "fix" commits. Then
post ONE "Review fixes" comment and update the PR description (the new word counts included). No
subagents. Follow workflow §10 (`receiving-code-review`: check each item first, push back with reasons
where one is wrong).

The report is `C:\Users\basel\.prompt\MASAHA_WORKER_C\REVIEW47_REPORT.md`; its line numbers are at
`e840f15`.

## Must fix

1. **The reading order contradicts itself and has two owners** (ninth commit; the analyst's prompt
   for it caused this — "then the capability's document" was the wrong order). Workflow §2 ›
   *Reading before work* **owns the order**:
   - **Always:** CLAUDE.md, this workflow, the map, and the open findings' titles and *Resolves when*
     lines (§4).
   - **Then the capability's document first,** when the task changes a capability that has one, and
     **only the sections it or the prompt links.**
   - **Then every other document whose map line ("read it when") matches the task** — replace the
     by-kind list with this, so *when to read* has one owner: the map. If the code-task essentials
     (engineering principles, testing, the layer's architecture) are not already caught by the map's
     lines, make their lines say so rather than listing them in workflow.
   - The rules, the map's `features/` line, ADR 0018, CLAUDE.md and `start-work-item` then all agree,
     and the skill links §2 only.
2. **Capability documents restate rules owned elsewhere:** `auth.md` (four `security.md` rules;
   architecture §2's guards and its one landing), `spaces.md` (the admin edits only while unverified —
   `security.md` owns it), `users.md` (sign-out only once the server agrees, stated twice — architecture
   owns it). Replace each with the "owned by … and linked" pointer.
3. ***Behaviour* sections restate endpoints' shapes:** `auth.md` (`RecoveryPosition`'s fields),
   `spaces.md` (*Read and edit*, *Hide, delete, restore*), `lookups.md` ("a hidden governorate leaves
   with all its areas"), `space-links.md` (the admin row's fields). One line of flow each, and link the
   contract's endpoint.
4. **A fact was lost (DS-1):** what the public site's header holds (logo, directory, language and
   theme toggles, sign-in or account menu). Give it its one home: a site-shell bullet in frontend
   architecture §2 › *The two groups*, beside the dashboard's shell.
5. **The records rule contradicts workflow:** the rules say records are never rewritten except to
   repoint a link, yet workflow §7 allows an ADR's dated *Revised* line and §4 a finding's resolution.
   Name the three allowed edits once (where the rules own records) and link workflow; drop the other
   restatements (see item 7).
6. **Two untrue statements in `spaces.md`:** creation makes **three attempts in all**
   (`CREATE_ATTEMPTS = 3`), not three restarts; the audit entry is written **in the change's own
   transaction**, not a separate one.

## Length — the owner's decision: cut the duplication, keep the coherence
7. **`auth.md`:** remove what the review measured as duplication (about 250 words): *Behaviour* lines
   that repeat its own *Decisions*, the security restatements (item 2), and the refresh lock and grace
   window (conventions and security own them). Don't cut flows or decisions to reach a number.
8. **The rules document:** remove the repeated words (about 100): the records exemption stated four
   times (keep one, item 5), "no changelog in a header" twice, and the overlaps with workflow §7 (keep
   links). Keep the tables, the template and *Not adopted*.

## Nits — fix (all cheap)
- `auth.md`: the masked email dates to #38, not #25.
- `spaces.md`: "an edit screen can show", not "shows" (no screen exists yet).
- The rules' §3 table row for the map gains "when to read it".
- Rules §5 (the update trigger) and §7 (the ADR threshold): keep only the links to workflow §7.
- ADR 0018: its third decision (the ADR clause) is a rule — keep it in the rules, and let the ADR name
  it once as a consequence with a link.
- The request id: the documents' wording becomes true — the status states don't show it; a form's
  failure, the lookups section's failures and Google's failure area do (architecture §5,
  conventions §10).
- Finding 38: "37 entries before this one".
- Conventions line 284: the missing `)`.
- Architecture line 183: capital "A".

## Checks
- Your read-only link script on every changed file (and the map), and a search that each removed
  restatement's key words now have one home.
- The word counts after the cuts, in the PR description.
- No local lanes, as before. Report once CI is green and GitHub shows `CLEAN`: the head, what changed
  per item, the counts. Don't merge.
