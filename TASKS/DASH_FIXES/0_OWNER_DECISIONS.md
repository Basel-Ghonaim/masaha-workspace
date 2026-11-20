# DASH_FIXES — the owner's decisions (2026-11-14)

- **D1 — the item:** one small PR by **OpenCode** (not Claude Code), in parallel with DESIGN ROUND3's lead: findings
  **227** (unknown icon key crashes), **220** (the admin's top bar on a deleted space), **222** (the photo's focus
  ring), **223** (Occupancy scrolls sideways at 390). Dashboard and design-system files only; nothing on the public
  pages (round 3 will redesign them). No schema, no dependency.
- **D2 — "one worker at a time" relaxed** for this item (the owner's word, 2026-11-14): the design lead keeps priority
  on the machine.
- **D3 — tests (the owner's words):** light tests only — the test files the item touches, each alone. Heavy runs
  (lint, typecheck, build, a full lane, a Chrome batch) only when memory allows: through the grant script, which
  checks free memory; if it does not grant within 10 minutes, skip that run and let CI judge, said in the PR's
  Evidence and the report.
- **D4 — review:** no Claude review (small, no schema, money or auth); the supervisor verifies the code and the shots.
- **D5 — #146's fix round (the owner, 2026-11-14):** S1, S2 and N1 of the supervisor's review (`7_FIX_ROUND.md`),
  folded; a fresh OpenCode session (the first reached 80% of its context); lint, typecheck and format:check required
  before the push; then the supervisor sees 222 and 223 in a browser before the merge word.
- Left out, and why: 217 / 218 need the owner's decisions; 23 / 65 / 152 need production dashboards; 221 / 224 touch
  the public site (after round 3); 219 / 225 (tests) later.
