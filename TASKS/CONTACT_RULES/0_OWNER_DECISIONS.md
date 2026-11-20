# CONTACT_RULES — five findings in one PR (the owner, 2026-11-15)

Runs beside PROTOTYPE_SPLIT (the owner relaxed "one worker at a time"); never touches that item's files.

- **C1 — finding 217, Arabic-Indic digits:** every phone (WhatsApp, phone, «وسيلة أخرى» as a number, a customer's
  phone, the platform's WhatsApp) **accepts Arabic-Indic digits and converts them to Western ones** before the rule
  reads them. The supervisor adds: the Eastern (Persian) forms `۰–۹`, which some Arabic keyboards type, convert too.
- **C2 — the phone forms (the owner's note, added to the scope):** a phone or WhatsApp number is accepted with the
  Palestinian code **+970** or the Israeli **+972**, and with `00` for the `+` (**00970**, **00972**). The rule
  already reads these four and stores E.164 (`packages/shared/src/core/phone.ts`); the item proves each with a test.
  **The local form (`059…`, `056…`, `02…`), accepted today: kept — the owner confirmed (2026-11-15).**
- **C3 — finding 218, only real links:** a **website** accepts only a valid web address — http(s), a real domain with
  a top-level domain; never an IP address, `localhost`, a bare word or a bare number. **Facebook** accepts only a link
  to a **page or a profile** (a username path, `/profile.php?id=<digits>`, `/people/<name>/<id>`); a video, `/watch`,
  a post, a group, an event, a photo, a share or a search link is refused.
- **C4 — the browser checks before the server:** the same shared rule runs in the browser first, so a wrong value is
  said on its row and **no request is sent**; the server still enforces it. (Already the design: the contacts' Sheet
  calls the shared `normaliseContact`, the desk the shared `phoneSchema` — keep it so and prove it.)
- **C5 — finding 226:** a ghost control inside a hovered table row hovers with the ink's wash (`hover-on-muted`) over
  the row's `hover`, and keeps it while its menu is open, in both themes — the supervisor's recommendation, approved.
- **C6 — findings 219 and 225** (tests only): no toast timer outlives a test file's environment; the four site test
  files warm their lazy routes in a `beforeAll` (testing §3 rule 8).
- **C7 — the no-conflict rule with PROTOTYPE_SPLIT:** never edit a file that item changes (its PR will list them; until
  it opens: `docs/design/**`, `CLAUDE.md`, `docs/README.md`, `.prettierignore`, `eslint.config.js`,
  `apps/api/scripts/checkLinks.ts`, `Logo/drawing.ts`, `docs/frontend/design-system/foundation.md`,
  `docs/features/{directory,finance,visits,payments,audit}.md`, findings 14, 19, 37, 73, 74, 96, 110, 165, 215 and
  **`docs/architecture/findings/README.md`**). The findings index lines for 217, 218, 219, 225, 226 are written only
  after that PR merges (rebase then).
- **C10 — the plan's choices, approved as recommended (the owner, 2026-11-15):** `toWesternDigits` moves to
  `@masaha/shared/core` (one home for the browser and the server); a Facebook link is one path segment only — a
  page's tab (`/masaha/about`) is refused, not shortened; the Facebook error's copy unchanged; **finding 228** records
  the observation that the customers' search reads a phone's last digits typed in Arabic digits as a name — recorded
  in commit 5 (its file, and its index line with the others after PROTOTYPE_SPLIT merges), not fixed in this item.
- **C11 — the fix round takes everything (the owner, 2026-11-16):** after the review (`7_REVIEW.md`), one round fixes
  **every** point of the branch — nothing is left for a later PR: F1 (217's quoted number), F2 (the untested link
  rows), **F3 made real** (219's test must fail without the wait), the review's untested phone rows, and **finding 228
  fixed here** — this **overrides C10's "recorded, not fixed"** (stated, the owner's word): a phone's last digits typed
  in Arabic-Indic or Eastern digits search the end of the phone, in the customers' search and wherever the desk's
  search of the people present reads digits the same way. Executor: **OpenCode with a free model**, a new
  conversation, alone on the machine (≈ 7 GB free), in `app-cr`. Prompt: `8_FIX_ROUND.md`.
- **C9 — places (2026-11-15):** `C:\dev\masaha\app` belongs to PROTOTYPE_SPLIT's worker. The planner and the executor
  run from `C:\dev\masaha\app-design`; the executor creates and works in `C:\dev\masaha\app-cr` and never runs a
  command in `app`.
- **C8 — the method, a trial (the owner, 2026-11-15):** **Claude Code plans** (Opus high, read-only, from
  `app-design` at `main`) a plan detailed enough for a less capable executor; **a free executor builds it — OpenCode
  or Codex** (the owner's pick at launch). The plan leaves the executor no design decision. Learned from DASH_FIXES
  (three red CI rounds from skipped local checks): lint, typecheck and format are **mandatory after every commit**,
  and the full verification before the push, with no "if memory allows" exception.
