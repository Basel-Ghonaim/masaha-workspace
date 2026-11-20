# AXE_FIXES — the owner's approval of `2_PLAN.md` (2026-11-18)

**APPROVED.** Go to Phase 2 with the plan as written (the contract, the 18 files, the three commits), with these
answers and one correction:

1. **§13.1 — the plan:** approved.
2. **§13.2 — `docs/frontend/architecture.md` §6:** the two lines approved, as §4.5 words them.
3. **§13.3 / §5.1 — the mark's `aria-describedby`:** the **`MutationObserver`**, as you recommend (the DOM's public
   contract; no reach into Leaflet's private methods). The supervisor checked your reading of Leaflet 1.9.4:
   `openTooltip` sets it after `openOn` (about line 10931) and nothing removes it.
4. **Proposed alternative 2 — the name:** keep `ScrollRegion`, its doc comment saying it is a group, not a region.
5. **§5.2 and §5.3:** the photo `ul`'s `w-max` and no `ref` — approved.
6. **§6 — the gaps in foundation §3's table:** in the report only, as planned; the supervisor holds them. No finding
   file.

**Correction (§12, *Sign-in*):** the endpoint is **`POST /api/v1/auth/login`**, not `/api/auth/login`
(`apps/api/src/app.ts`: `API_BASE = '/api/v1'`, `AUTH_PATH = '/auth'`). Post it from the page on the web's own origin
(5320), so the API's cross-site check passes.

Everything else as the prompt says: complete local verification but `test:api` (X6), the Chrome pass with its `main`
baseline before you cut the branch, `#PRNUM` replaced just before the push, `open-pr`, green and `CLEAN`, then
`final-report` to `4_REPORT.md`. **Stop. Never merge.**
