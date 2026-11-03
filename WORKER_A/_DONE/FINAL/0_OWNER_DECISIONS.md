# WORKER_A · FINAL — the owner's decisions for the last mission (2026-10-29), binding

Settled by the owner with the supervisor before planning. The planning prompt (`1_PLAN_PROMPT.md`, written once
worker B's BACKEND_FINAL PR has merged) copies these verbatim into the plan's binding section.

## The mission

- **Close everything:** after it, **every one of the 32 screens is complete, with no gap**, and every open finding
  below is closed — built, or accepted by the owner.
- **The screens missing or partial on `main` (2026-10-29):** 9 (the name and language — `GET`/`PATCH /me`, built by
  B's BACKEND_FINAL); 12 (the owner's overview); 19 (finance); the owner's audit (O13, `Owner audit.html`, finding
  14); 25 (the admin's overview); 31 (the admin's audit log); 32 (the platform settings). Gaps on built screens that
  B's new routes close: finding 161's visits of a day, finding 167's filter on screen 28. Plus every gap the planner
  finds by checking each screen against its prototype and `foundation.md` §13.
- **The home-page review is cancelled;** a full review of the whole project follows this mission.

## The framework

- **F1 — scope (a):** every open finding is in, **except** (1) those B's BACKEND_FINAL closes — 97, 153, 161, 167,
  170 — and (2) those only deployment or a measurement there can close — **23** (a per-address ceiling), **33, 46,
  64** (the deployment's headers), **65** (the reset wait measured), **152** (the audit's retention) — which go to the
  deployment item. `0_CARRIED_FROM_111.md` (the public site's small fixes) is in.
- **F2 — one PR may change `apps/web`, `apps/api`, `packages/shared` and `docs` together.** The web/API split between
  the workers is lifted for this mission (the owner: the project's end; speed matters).
- **F3 — migrations (a):** allowed when the approved plan names each; its SQL read at the review; no PR number in
  SQL.
- **F4 — one PR (a)**, the reviews split by lanes.
- **Planner:** Opus 5.5 at **xhigh** effort. **It starts once worker B's BACKEND_FINAL PR has merged.**
- **Execution:** as #129 and B's lead run — a lead with sub-agents (the lead decides how many), a test database per
  API lane, heavy runs scheduled on the memory, the complete verification and the real run before the PR, no stop.

## The findings that needed the owner

**Built** (each as its finding's *Resolves when* says):
- **14** — the owner's audit screen (design O13), with its place in the owner's navigation.
- **21** — a refresh token replayed within the grace returns the same successor, derived deterministically (an HMAC of
  the presented token under a server key).
- **32** — the Google sign-in's answer says the account was created (`created` beside `linked`); a first Google
  sign-in is welcomed as registration is.
- **83** — `ALREADY_OWNER`'s 409 names the account (a contract change).
- **89** — the person search reads a larger page or an exact email filter; a failed read is worded as such.
- **92** — deactivating a reception link ends that person's sessions only when no other active link remains.
- **99** — the owner's checklist names the retired amenities the space holds, marked, until a save leaves them out.
- **160** — a visit's check-in may take its customer (`customerId`), and the desk sends it.
- **162** — the statement names who recorded and who voided each payment.
- **163** — the subscription's corrections get a place: its card in the customer's file, on the routes as they are
  (the planner designs it in the layer; its DIs go to the owner).
- **164** — a read lists a space's written-off visits (reason, who, when) and a screen offers their undo there.
- **165** — the dashboard's navigation grouped by task (`SPACE_NAV`, `ADMIN_NAV` with groups; labels hidden on the
  rail).
- **166** — the ledger's staff filter names the space's other owners.
- **168** — a guest's held action survives a password recovery in a short-lived, same-origin store the session
  confirms, never in the address.
- **171 (a)** — the desk sends the published price it showed (`published.amountAgorot`); the server compares and
  answers 409 when it differs (a new error code, both catalogues).
- **91 (a)** — creating an account with the address of a pending account whose temporary password expired replaces
  that pending account.

**Accepted (closed without code; each finding moved to *Accepted* with the owner's line):**
- **84** — v1 needs no linking of an existing account to a second front desk (close to in-app claiming, *Not in v1*).
- **187** — no undo after «إزالة» of a space that left the directory (the owner's DI-58 (a), 2026-10-28).

**Added 2026-10-29, after #131 merged (`main` = `ce671b37`, the API of v1 complete):**
- **193 — accepted:** finance's «غير محصّلة» stays the desk's list (equal to what the overview's tile links to); the
  documents already say owed and uncollected are never added. Moved to *Accepted* with the owner's line.
- **158** (the admin's spaces list's second schema for "editable", left by #131 for screen 25) — **in**: screen 25's
  «عرض الكل» uses it, and the planner closes it as its *Resolves when* says.
- **97, 153, 161, 167, 170** are resolved on `main` (#131).

**The run (the owner, 2026-10-29):** the plan is written by **a planning session of worker A's own (in
`C:\dev\masaha\app`, read-only, from `origin/main`'s commit objects)**; worker A executes in **a second, clean session
in the same folder** that waits for the execution prompt. The supervisor reviews the plan, **settles every open point on the owner's behalf** (the safest recommendation,
each logged in `WORKER_A\FINAL\SUPERVISOR_DECISIONS.md`), writes the approval note and the execution prompt, then
creates `WORKER_A\FINAL\READY`; worker A's waiting script starts the run on it. #125 closed (2026-10-29).

**Every other open finding** (≈ 40: tests, performance, accessibility, documents, tooling) — **built** as its own
*Resolves when* says; where a finding offers "or the owner accepts", the planner recommends one and lists it for the
owner's approval note.
