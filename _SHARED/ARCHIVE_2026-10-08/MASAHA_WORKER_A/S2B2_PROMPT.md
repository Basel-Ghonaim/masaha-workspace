# S2b-2 — The spaces' facts API: hours, shifts, prices, amenities, contacts

**Worker A** · main folder `C:\Users\basel\masaha` (on `main` at `a1f5aba`, clean) · branch
`feat/space-facts-api`, cut from the latest `origin/main`. Databases `masaha_dev` / `masaha_test`;
API on 3320.

**Size cap:** at most 4 subagents in total, and **no self-review subagent** (the independent review
gate follows the PR). Do not run any workflow. Read what the task needs; don't sweep the repository.

## 1. How to work

- **Start with the `start-work-item` skill.** Plan in plan mode before writing code.
- **Read in the order `docs/development/workflow.md` §2 › *Reading before work* gives:** the
  essentials and the open findings' titles; then **`docs/features/spaces.md` first** (what the
  capability owns, its decisions S1–S9 and the profile edit, its code map) and only the sections it
  links; then the documents whose *read it when* line matches — for this item at least
  `backend/conventions.md` (§3–§6, §8 *Transactions* with the one-statement-at-a-time rule, §9),
  `backend/security.md` › *Authorization*, `architecture/data-model.md` (*Spaces*, *Derived values*,
  freshness), `api/api-contract.md` §4–§5, `development/testing.md`.
- **Related findings** (workflow §4): your plan lists the open findings that touch this item, each
  folded in or not, why and its cost; the owner decides. The analyst sees at least **36** (a new
  space's empty groups count as fresh — in scope, decision F2), **41** (the request log doesn't name
  the space — this item adds space routes), and **31** (the older `spaces` service still takes a
  repository parameter — this item touches that module). Judge them and any other.
- **Superpowers: follow workflow §10.** Testing follows `testing.md` §3 rules 5–7: every test seen
  failing first and naming the break it catches; **make the break once** for every transaction,
  ordering and authorization property (for example: drop the row lock, write outside the
  transaction, let a used shift be deleted, let a verified space be edited) and watch its test fail.
- **The designs** (for what the API must serve): `docs/design/screens/43-admin-spaces/` frames 11–16
  (edit while unverified, verified read-only, add a space: the hours with their shifts, the prices,
  the amenities, the contacts, each section saved alone with "the information is still correct");
  `49-fixes-batch-4` (24-hour hours).
- **When finished, follow the `open-pr` skill.**
- **The owner's rules:** honest test titles; **no parameter, option or callback that only tests pass
  or nothing uses** (a service creates its own repository; the composition root passes only real
  dependencies); one responsibility per file, one service / repository / controller per resource;
  checks: lint and typecheck per commit, the full lanes once on the head, one at a time, never re-run
  a lane that already passed on unchanged code; commit subjects ≤ 50 characters; report only once CI
  is green; review fixes fold into their commits with ONE "Review fixes" comment; rebase only on a
  real conflict; a migration is created once with `--create-only` and checked before it is applied;
  no tool or AI attribution.

## 2. What this item delivers

Build step 2's second spaces item (the owner's split: S2b-1 API, **S2b-2 this API**, S2b-3 the list
and add screen, S2b-4 the edit screen). The admin edits an **unverified** space's facts, one group at
a time, and confirms a group unchanged. **API, `packages/shared` and documents only; no web file.**

**What exists:** the tables (`space_hours`, `space_shifts`, `space_prices`, `space_contacts`,
`space_amenities`), the fact groups' dates on `spaces`, the admin's space routes with the
non-refusing links loader and `can('space.facts.update')` (admin while unverified, else the owner),
the profile edit as the model to follow (lock, read, `can()`, change, audit in the same
transaction), the staleness rule.

**It builds,** for the admin under `/admin/spaces/:spaceId/…`, each in one transaction, locked and
audited:
- **hours** (seven days, each closed or one range) **with the shifts** (decision F3);
- **prices** (period, audience, optional shift, optional custom label, amount in agorot);
- **the space's amenities** (a set);
- **contacts** (type and value);
- **confirming a group unchanged** (its date renewed, nothing else changed);
- the admin's one-space read gains the facts, for the edit screen.
- **Documents:** `docs/features/spaces.md` gains the facts (its behaviour, decisions F1–F7 with
  reason, date and PR, its code map and history) **in this PR**; api-contract.md (the endpoints);
  data-model.md (the freshness groups and nullable dates, if F2 and F3 change them); anything else
  your changes make untrue.

## 3. The proposed decisions

These came out of the analysis and the owner approved them, **but they are proposals, not orders.**
If you find a stronger option, put it in your plan under **"Proposed alternatives"** with its
trade-off and your recommendation; build an alternative only once it is approved.

- **F1 — one endpoint per group, replacing the group whole** (`PUT …/hours`, `…/prices`,
  `…/amenities`, `…/contacts`), plus **one confirm endpoint per group**. It matches the design (each
  section saves alone); each save is atomic, renews its group's date, and writes one audit entry.
  This replaces the plan's draft of one `PATCH` for the profile and every fact (`v1-mvp.md`, updated
  in this PR).
- **F2 — an empty group is missing, not fresh** (finding 36): a migration makes the dates of the
  groups that can be empty (hours, prices, amenities, contacts) nullable; a new space leaves them
  null until the first save; staleness reports a null group as missing. Spaces that already have
  rows keep their dates (the migration fills them). Resolves finding 36.
- **F3 — the shifts are saved with the hours,** as the design places them, and their freshness
  follows the hours: data-model.md's "prices (with shifts)" is corrected. Deleting a shift that a
  price uses is refused (409) until the price is changed first.
- **F4 — hours within one day, with a 24-hour option** (0 to 1,440 minutes); no range past midnight in
  v1 (it would complicate live status and auto check-out in step 7).
- **F5 — replacing the shifts keeps each existing shift's id:** update by id, add the new, delete only
  shifts nothing uses (else 409). Never delete-and-recreate: packages, subscriptions and visits will
  reference shifts.
- **F6 — contacts validated per type** in `packages/shared`: phone and WhatsApp in international form
  (+970 or +972), a valid email, a URL or handle for the networks, normalised before saving.
- **F7 — amenities:** only an **active** amenity can be added; a retired one already linked stays
  until removed (data-model: a retired amenity keeps its links).

**Kept (the owner looked again and confirmed):**
- shift names and price labels keep the Arabic required and the English optional — common words, not
  a brand's name (unlike a space's name, S1);
- the admin's and the owner's edits stay separate endpoints over one service logic (S9): build the
  facts' logic so the owner's `/manage` endpoints in step 5 reuse it, but build only the admin's.

## 4. Your plan decides

- the files per group (*Growth*), the request and response shapes in `@masaha/shared/spaces`, the
  migration (checked with `--create-only` first), and how the confirm endpoints are shaped;
- the 409 mapping for the prices' four partial unique keys, each on the right field;
- the audit action names (stable, `space.<group>Edited` / `…Confirmed` or better) and payloads;
- the related findings to fold in (with the owner's yes);
- the tests, per testing.md: every endpoint as a guest, a USER, an OWNER of another space, the OWNER of
  this space, the ADMIN, and an admin with a pending password change; each group's validation and
  its 409s; the replace semantics (F5: ids kept, a used shift refused); a verified space refused; the
  group's date renewed and the others untouched; confirm renews only its date; F2's missing state and
  the migration on existing rows; the audit entry in the same transaction; the one-space read;
- the commits (3–6, each a complete unit).

## 5. Out of scope

- Any web file (S2b-3, S2b-4). The owner's `/manage` endpoints (step 5). Photos and the storage port
  (step 5). Packages (step 5). Capacity and live status (step 7). The space's settings (step 11).
- Ranges past midnight (F4). New dependencies — if you think one is needed, stop and ask.

If the plan finds the documents missing something this item needs, or a decision that can't hold,
stop and report.

## 6. Parallel work

Worker B works in its own worktree on the admin's amenities tab (web): `features/lookups`, the
design system's icons and button, the copy catalogues, `docs/features/lookups.md`, foundation.md,
`overview.md`'s lookups line, `findings.md`.
- **Declare your shared files in the plan** (at least `apps/api/src/app.ts`, api-contract.md,
  data-model.md, conventions.md if touched, `overview.md`'s spaces line, `findings.md`), and edit each
  minimally, in your own section.
- **Findings numbering:** main ends at 41; **number yours from 42** (worker B uses 46 onwards).
- **This item changes the schema:** after the merge the analyst applies the migration to worker B's
  database; say in the PR what it changes.

## 7. Pull request

- **Title:** `feat(spaces): add the spaces' facts API` (or the main commit's subject).
- **Labels:** `feat`, `area:api`, `area:docs`. Assigned to the owner.
- **The description:** scope, acceptance criteria and out of scope; F1–F7 and any alternative
  approved; the related findings folded in; the migration; **which tests you saw fail first, and the
  breaks you made**; evidence per lane; what was not run.
- **Review:** the independent review gate, after you report.
- After CI is green on the pushed head, stop and report: the head, the commits, the counts per lane,
  your tokens. Don't merge. Don't create an Issue.
