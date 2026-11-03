# Review of #132 — R1: the foundation, the design-system layer, the build, the closing documents

Read this file, then `C:\dev\masaha\workspace\WORKER_A\FINAL\5_REVIEW_PROMPT_COMMON.md` whole, and do it. Your report:
`C:\dev\masaha\workspace\WORKER_A\FINAL\6_REVIEW_R1.md`. New findings, if any: **220–223**.

**Your commits (25):**
- U0 and U3 (the foundation, the layer, the lists, the library): `fed3b46d 9c53b8dc 3c58a9a1 a55da7bb 44df247c 40df132f
  9755efe6 06f3c154 cee9736d c0b8e36b 3348faf3 67747ed9 5d2797d5 098bc4e9 6f5b51b7 43aad599 9a7dff2c`
- U4 (the build and the tooling): `5d4178a3 67b980a5 3d5798b4`
- U10 (the closing documents): `5c1dabd8 9bf66b52 0676d604 10a72981 a12c0790`

**Read in the plan:** §5.0 (U0), §5.3 (U3), §5.4 (U4), §5.10 (U10); §5.11 S…; the DIs on the layer, the navigation,
the shells; §9.1's commits for these units; §9.3 (the shared files); §10.1 and §10.4's tests for U0, U3, U4; §12.

**Look hardest at:**
- **The refusal's `details` and the new error code** (C0.1–C0.2): the envelope's shape in `packages/shared`, both
  catalogues, the contract §6 — the web reads them right; nothing private in `details`.
- **The grouped navigation (finding 165):** `SPACE_NAV` and `ADMIN_NAV` groups, labels hidden on the rail, each role's
  items exactly (reception sees no owner page; the owner's audit and finance the owner's only); the skip link in every
  shell (finding 130); the account's place on a phone.
- **The layer's new components** (meter, bar charts and heatmap, the large input, the held menu item reached by the
  keyboard — finding 105): semantic tokens only, no colour or font outside the layer, both themes, RTL, 44 px on touch,
  accessible names, the showcase sections.
- **The lists** (range and steps, the page asked while it loads — 132, the scroll kept on a page change), **the
  library** (Arabic-Indic digits read once — 103; the CSV builder and the WhatsApp link — injection-safe CSV cells, a
  number in E.164 only).
- **The build** (finding 180's `public.ts` entries — OD8; the site's first download not reaching dashboard code or a
  heavy library; the acyclic dashboard-only code; the lazy shells loaded before waiting in tests — does it hide a real
  slowness?).
- **The closing documents:** every build-map step *Built*, every screen built in `SCREENS.md`/`overview.md`, the
  findings index (OD9: moved once at the end) — **no open finding left but the deployment's six (23, 33, 46, 64, 65,
  152) and any recorded by this PR (200+)**; the accepted ones with the owner's line (84, 187, 193; 22, 112, 115);
  finding 98's revised size guide (OD4).
