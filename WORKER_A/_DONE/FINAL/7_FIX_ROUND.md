# #132 (`feat/final`) — the fix round: every review finding, as new commits on top

You are **worker A's fix-round executor** in `C:\dev\masaha\app` (web 5320, API 3320, `masaha_dev` / `masaha_test`),
on your own PR **#132** (`feat/final`, head `a12c0790`, 124 commits). Six reviews are in, all in
`C:\dev\masaha\workspace\WORKER_A\FINAL\`: `6_REVIEW_R2.md` (the API), `6_REVIEW_R3.md` (owner/admin screens),
`6_REVIEW_R5.md` (desk/customers), `6_REVIEW_R14_CLAUDE.md` (foundation, layer, build, documents, public site,
account), and Copilot's `6_REVIEW_R1.md` and `6_REVIEW_R4.md` (only R4-F1 is taken from those two). **No blocker.**
**The owner's decisions and the supervisor's on his behalf** are below (§2); every finding listed there is fixed in
this round. Read the reviews' *Findings* sections for the full text of each, then this file. Do not run the
`start-work-item` skill.

## 0. The rules of this round

- **NEW: fixes go on top as new commits — never folded.** The owner's instruction (2026-11-01): **no `--fixup`, no
  autosquash, no rebase of the 124 commits, no force-push.** Each fix is a **new commit after `a12c0790`**: one commit
  per finding, or one per closely related group (the same files, the same cause) — Conventional Commits, subject ≤ 50,
  a body naming the finding(s) it fixes (e.g. `Fixes review R2-F1 (finding 114)`); a fix's test in the same commit. A
  plain `git push` at the end.
- **No stop, no question,** until #132 is ready for review again (pushed, CI green on the new head, `CLEAN`, the report
  and the PR description updated, the final reply sent). Every decision taken on your own: recorded (met, options,
  chose, why, undo); a SERIOUS one first.
- **Hard limits:** never merge or push to `main`; **no migration** (none of these fixes needs one — a need for one is
  SERIOUS: find another way or leave that fix out, named); never change data through the app, the API or the database
  beyond the real run's named writes, never reseed; never skip or weaken a test, check or lane; never print a secret or
  keep an `/auth/` body; no tool attribution; never `git checkout -- <file>`, `stash` or `reset --hard`; stage by path.
  A refused command → carry on, print it in the reply.
- **You may use sub-agents** (the Agent tool, your own worktrees, a test database each for an API lane) if it is
  faster; the joins then **rebase only the new fix commits** onto `feat/final` — never the 124. Your call, recorded.
- `#132` is known: write it directly where a document needs the number.

## 1. The base

`git -C C:\dev\masaha\app status -sb` → `feat/final`, clean, at `origin/feat/final` (`a12c0790`); `git fetch origin`;
`gh pr view 132 --json mergeStateStatus` → if not `CLEAN` because `main` moved, `git merge origin/main` **is not
allowed either** — record it and carry on; CI and the supervisor judge it. `npm ci`; `npm run build -w
@masaha/shared`; `docker start masaha-postgres-1` if down.

## 2. The fixes — every one in this round

**The API (R2)**
1. **R2-F1** (finding 114 reopened) — "stalled" only when the batch was **full**: `batch.length ===
   AUTO_CHECKOUT_BATCH && closed === 0 && failed - failedBefore === batch.length`, in `visits.service.ts` and
   `subscriptions.service.ts`; T54 and its twin with a full batch of failing stays (`generate_series(1, 500)`); a test
   that one failing stay alone answers 200 with `failed: 1`; the contract line and finding 121's *Resolution* say "its
   batch full".
2. **R2-F2** — **the owner approved:** an account is replaceable (finding 91) **only if someone else created it** — a
   `user.created` audit entry naming it as the entity (the owner's staff add, the admin's owner add) — in the same read
   as `hasActed`; a T29 case: a self-registered account with an expired admin-issued temporary password →
   `EMAIL_TAKEN`; `security.md:53` states the rule.
3. **R2-F3** — the race test passes `RACE_TIMEOUT_MS`.
4. **R2-F4** — `sum(amount_agorot)::bigint` in `balancesOf`, `Number()` where `itemBalances` maps `paid`; a test with a
   paid sum past `integer`.

**The owner's and the admin's screens (R3)**
5. **R3-F1** (105) — the owners page's «ربط بمساحة» `held`, not `disabled`; a test that ArrowDown lands on it; 105's
   *Resolution* true.
6. **R3-F2** — finance's counted Arabic values out of `dir="ltr"` (keep it on the money and the peak hour only, or
   isolate the number); a test in Arabic.
7. **R3-F3** — the overview's «… بلا سعر» row lands on a real anchor (`id="unpriced"` with `scroll-mt-*`, an exported
   constant); a test.
8. **R3-F4 and R14-F7** (finding 204) — **the owner's rule:** `csvOf`'s `fieldOf` prefixes `'` to a **text** value
   starting with `=`, `+`, `-`, `@`, a tab or a CR (OWASP) — numbers stay numbers; this also keeps a phone (`+970…`) as
   text; unit tests; finding 204 *Resolved*.
9. **R3-F5** — «تعديل الحقل» with `?report=` lands on `#report` (the notice), not the section's heading; a test.

**The front desk and customers (R5)**
10. **R5-F1** (finding 212) — the «لن تُحصَّل» card's header with its toggle kept below `xl` for the owner even when
    empty (only the empty body hidden); a test at a phone width; 212 *Resolved*.
11. **R5-F2** (160) — `customerId: number | null` on the `VISIT` `PresentPerson` (an answer change, no migration); the
    search card shows them present; their present row links to the file; tests (API and web).
12. **R5-F3** — «استلام {amount}» and «أقدم بند» name the earliest **owing** item across both kinds, by the server's
    rule; a test with an older subscription debt and a newer visit.
13. **R5-F4** — the customers list's «⋯» never moves under the pointer: its state items' place reserved while the file
    reads (held, `aria-busy`), or the read started on hover/focus; a test.
14. **R5-F5** — each «تراجع» named «تراجع عن شطب زيارة {name} · {day}», both catalogues.
15. **R5-F6** — the WhatsApp reminder's default in one language: the space's (Arabic) words with the Arabic name, or
    the English default with `nameEn`; a test.

**The foundation, layer, documents, public site and account (R14, and Copilot's R4-F1)**
16. **R14-F1** (132) — `refreshing={query.isPlaceholderData}` on every paged list's `DataTable` (customers, payments,
    and the rest the review names) and the Directory's results in `Refreshing`; tests for the Directory and one table
    list; 132's *Resolution* true.
17. **R14-F2** (136) — near me under a `prompt` that never settles: a longer bound from the press (60 s), the 15 s once
    `granted`; the `change` listener removed when settled; a test.
18. **R14-F3 (and Copilot's R4-F2, R4-F3)** — **the supervisor's decision on the owner's behalf** (see §3): the stored
    guest action is confirmed **only by the round trip it serves** — a sign-in in the tab that held it, or a sign-in that
    follows a password reset completed in this browser (the reset page sets a short-lived flag); any other sign-in drops
    it without running it; 168's *Resolution* and its document say the rule; tests for: another tab's unrelated
    sign-in, a later visit, the reset round trip (runs once).
19. **R14-F4** — the map view's search row at 390: `min-w-0` on the search, `shrink-0` on «الفلاتر»; checked in both
    languages.
20. **R14-F5** — «اختر منطقتك» from the favourites focuses the place filter from 1024 px (deferred after the shell's
    focus rule, or the shell skips a navigation that carries a focus target); a routes test at 1440.
21. **R14-F6** — screen 9's "set a password": `features/auth`'s `LinkSent` (the masked address, resend with its
    countdown) and the rate-limit alert with the button held; T256 checks the block.
22. **R14-F8** — finding 55's line and `spaces.md:4, :20` true (take the slowest route file's time from CI run
    41288412120, or reword 55 to the branch its *Resolves when* allows; drop the two `spaces.md` sentences).
23. **R14-F9** — `downloadFile` revokes the object URL after a tick (`setTimeout`).
24. **Copilot's R4-F1 (confirmed by the supervisor)** — `next` kept through the password recovery: the forgot page's
    «متابعة» to the reset page, and the reset page's «العودة لتسجيل الدخول» and post-success sign-in links, carry the
    validated `next` (the existing `nextSearch`/`returnUrlOf`, never raw input); a test.

## 3. The supervisor's decisions in this round (on the owner's behalf; logged)

- **Item 18 overrides the earlier "accept" of Copilot's R4-F2/F3:** Claude's independent R14 confirmed the case and
  gave a narrow, buildable rule tied to the reset round trip; the safer course is to build it. The owner reviews it at
  the end.
- Every other item as the reviewers proposed, the owner's two (R2-F2, the CSV rule) as he approved.

## 4. What runs — complete before the push (the owner's rule)

- **While fixing:** each new test **red before its fix** (copy the line), green after; only the touched test files.
- **Before the push, once, on the final head, all green:** `npm run build -w @masaha/shared`; `npm run format:check`;
  `lint`; `typecheck`; `check:classes`; `check:links`; `check:conflicts`; `test:unit`; `test:component`; `test:api` (no
  command timeout, ≈ 10 min); `NODE_ENV=production npm run build` then `npm run check:build`. Memory: before each heavy
  run ≥ 4 GB free, else wait 2 minutes (bounded); a run killed for memory → re-run, then in parts, until every file has
  run green. Finding 87's family missed in a full run and passing alone: re-run alone, record.
- **A short real run** (web 5320, API 3320, `masaha_dev`, headless Chrome over CDP on the model of
  `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\scripts\cdp2.mjs`, no `/auth/` body kept): items 6 (finance in
  Arabic), 10 (the desk at 390), 13 (the customers «⋯»), 19 (the map at 390, both languages), 20 (the favourites →
  the place filter at 1440), 24 (`next` through recovery, read-only — no reset sent); shots in
  `C:\dev\masaha\workspace\WORKER_A\FINAL\shots\fix\`; no write unless named; servers stopped by process id.

## 5. Push and the end

- `git push origin feat/final` (a plain push — the 124 commits untouched).
- `gh pr checks 132 --watch` (bounded; no command timeout) → green; `CLEAN`. A red lane → fix in a new commit, re-run
  that lane locally in full, push, watch again.
- `gh pr edit 132 --body-file …`: a *Review fixes* section — each item (1–24), its commit, and the decisions of §3.
- Append to `C:\dev\masaha\workspace\WORKER_A\FINAL\4_REPORT_LEAD.md` a section *The reviews' fix round
  (2026-11-01)*: each fix (commit, red/green lines), the runs (memory readings), the real run, push, CI, decisions.
  Write nothing else outside the repository except `C:\dev\masaha\workspace\WORKER_A\FINAL\scripts\` and `shots\`.
- `git status --short` clean; name any branch or worktree you made and removed.

```
Status: READY FOR REVIEW | INCOMPLETE (only if nothing at all could continue)
SERIOUS decisions: <each>   (or "none")
PR: #132 · head <sha> · CI <green/red> · <CLEAN/not CLEAN> · commits <124 + n>
Fix commits: <sha> <subject> (<chars>) — <items> — one line each
Left out: <item, why>   (or "nothing")
Verification (local, on <sha>): <each command with its result line; memory readings>
Real run: <cases> · writes <none / each>
CI on the head: <each lane>
Decisions taken on my own: <each>   (or "none")
Refused commands: <command>   (or "none")
Report: C:\dev\masaha\workspace\WORKER_A\FINAL\4_REPORT_LEAD.md
```
