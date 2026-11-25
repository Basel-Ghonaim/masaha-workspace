# AUTH_IN_PLACE — the owner's decisions

- **2026-11-24 — the direction (A19):** sign in over the page the user was on; settle every axis first
  (`1_ANALYSIS.md`).
- **2026-11-24 — I1–I13 approved as recommended:** sign-in and register in place; no modal routes; the header's
  «تسجيل الدخول» stays a full page; the user stays on the page and the held action runs, focus back to its trigger;
  the action waits for a forced password change; Google in place behind the executor's first checks; a dialog on
  desktop; a lazy chunk + a `check:build` rule; ADR 0021 and the four documents; the tests of I12; one Work Item after
  the pictures, a Claude Code worker (Opus high), a Claude review.
- **2026-11-24 — the phone (I7):** a full-screen panel, **with a close button and a very good experience** (the owner's
  words) — its details in `1_ANALYSIS.md` I15.
- **Open:** the forgotten password (I14) and the phone's details (I15), asked of the owner.
- **2026-11-24 — I14 approved:** the request for a reset link in place, the link's page a page, A1 (the waiting tab
  learns of the reset), no automatic sign-in after a reset (A2 rejected). The owner's condition, for the whole task:
  **no security risk and no user-experience risk — the experience as comfortable as it can possibly be**; every plan
  and review checks both.
- **2026-11-24 — I15, the phone:** the owner's "exit button" meant **the panel's close button** (a wording slip on his
  side). Kept as written in I15; the browser's Back also closing the panel stays the supervisor's recommendation,
  unless the owner objects.
- **Open:** the order of the work (ADR, prototype, production) — proposed to the owner.
- **2026-11-24 — the order of the work (approved):**
  - **WI-A** ADR 0021 «Sign in where the action is», docs only; the supervisor writes the text, the owner reviews,
    a free executor commits it word for word.
  - **WI-C1** the layer component (a dialog from `md`, a full-screen panel below it: top bar, close button, Back
    closes it), with today's `SignInPrompt` moved onto it as its first real use.
  - **WI-C2** sign in in place (sign-in, register, the reset link's request, Google, the held action, A1, the lazy
    chunk + `check:build`, tests, the four documents); Claude Code, Opus high; a Claude review with security and UX
    requirements.
  - **WI-B** the berry on the primary action site-wide (A18): an ADR revising 0019, the token, the contrast tests —
    after the owner approves the pictures.
  - **WI-C3** the full `/login` and `/register` pages on the same form, last.
  - **Prototype rounds** (the supervisor with the owner, in `masaha-prototype`): P1 the shell (for C1), P2 the content
    and every state (for C2 and B), P3 the full pages (for C3).
  - **Parallel:** WI-A ∥ P1 now; C1 ∥ P2 after the ADR's merge and P1's approval; C2 ∥ B after C1's merge (no shared
    file — checked in each plan; B never beside C1: both edit `foundation.md`); P3 → C3 last. Heavy test runs one at
    a time through the grant script.
- **2026-11-24 — ADR 0021's text and P1 approved** (the owner: «موافق على الاثنين»). masaha-prototype pushed
  (`0c8d7ad` the variant, `a6e77b9` the approval in `decisions/Space details.md`). WI-A's executor prompt:
  `3_EXEC_PROMPT_WI-A.md` (the texts as files in `WI-A\`), for a free executor; merge on the owner's word.
- **2026-11-24 — P2 loop 1 approved** (the views and states inside the overlay; masaha-prototype `671a53d`, pushed).
  Loop 2: the reset link's page (its last step leading back to the page and the action) and the English pass.
- **2026-11-24 — P2 loop 2 approved; P2 done** (masaha-prototype `b3b9f4d`, pushed). The owner, leaving for an hour:
  wait for Copilot's PR, **merge it if everything is right**, then **launch WI-C1 with Claude Code, Opus high** — no
  blocking of the execution.
- **2026-11-24 — WI-C1's plan approved by the owner** (D1 one width 30 rem, D2 the history API, D3 S1–S4, D4 the
  title on the scale; the supervisor's three notes folded in). Execution resumed in the worker's session.
- **2026-11-24 — WI-C2's plan approved by the owner, D2 = B** (no e-mail stored: the reset page's sign-in opens with
  the e-mail empty, autocomplete set; A1's tab fills it from memory); D1 (the one line everywhere), D3–D8 and design
  issues 1–7 as recommended; the NEW words as listed. Phase 2 starts once #155 merges (the message in
  `WI-C2\2b_SUPERVISOR_REVIEW.md`).
- **2026-11-24 — #155 merged** (the owner tested it locally, then «تمام»; pinned to f2b8dff6). WI-C2's phase 2 resumed.
- **2026-11-25 — #157 merged** (the owner's word after his own look on 5323; pinned to ad0ba75e). `main` = 95c33fe9.
