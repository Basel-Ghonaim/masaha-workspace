# Review of #131 — R3: the overviews and the closing documents

Read this file, then `C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\5_REVIEW_PROMPT_COMMON.md` whole, and do it.
Your report: `6_REVIEW_R3_CLAUDE_CODE.md`. **Head: `c41a5397`.** New findings, if any: **196–198**.

**Your range:** `53c6a7e3..c41a5397` — 5 commits: `feat(api): count what the owner's overview shows`, `feat(overview):
read the owner's overview`, `feat(api): count what the admin's overview shows`, `feat(overview): read the admin's
overview`, `docs: record the API of v1 as built`.

**Read in the plan:** §2.3 and §2.4 (OV1–OV8, O3, A8 — binding); OD1–OD4; §3.2; §4.2; §5.1, §5.2, §5.4 (the
services, the counting functions each owning module gained, their costs); §5.6; §9.4, §9.5, §9.7, §9.8; §10's overview
cases; §11 (documents) and §11.3.

**Look hardest at:**
- **No amount anywhere in the owner's overview (OV1, O3):** not in the answer's shape, not in a nested object, not in
  a debug field — debts as a **count of customers** only (OV2).
- **Who reads what:** the owner's overview the owner's only (OV3 — reception refused); the admin's the admin's;
  `platform.stats.read` removed (OD4) and nothing else depending on it.
- **No logic in `overview` (OV7):** every figure from its owning module's set-based count; **each count equal to the
  total of the list its tile links to** (the plan's claim — check the filters match exactly: OD1's `ENDING_SOON` and
  the customers list, OD2's unverified = not hidden, OD3's `status=editable` with `stale=true`, the reports' open
  ones, new users = 30 Gaza days (OV5)); "stale" by #130's thresholds (OV6), never a constant; fetched in parallel; one
  endpoint per screen; `overview` never imports `finance`.
- **«اكتمال البيانات»:** the first five the admin can act on, missing and stale both counted, hidden ones included as
  A8 says.
- **Cost:** the counts on a busy platform; no N+1.
- **The closing documents (C16):** v1-mvp (steps 11 and 12 *Built*, the `/me`, `visits`, `/admin/stats` rows),
  `overview.md` *Built*, `docs/README.md`, conventions (the "total owed" line corrected to a count), foundation §13's
  screen 12 line (OV8), the findings index, `overview.md` the capability document (new) — true to the code, one home
  per fact, `#131` where it goes.
- Tests and breaks (§9.4–§9.5) — would each fail?
