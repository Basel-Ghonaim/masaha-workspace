# Review of #129 — R2: the data reports (the owner's and the admin's)

Read this file, then `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\5_REVIEW_PROMPT_LEAD_COMMON.md` whole, and do
it. Your report: `6_REVIEW_LEAD_R2_CLAUDE_CODE.md`. Your new findings, if any: **184–186**.

**Your range:** `2fa45cf8..dc427a54` — 3 commits:
`7d892c86 feat(design-system): add a removable filter tag` (finding 8) · `44e8ee1f feat(data-reports): decide a
space's reports` (screen 23, the owner's) · `dc427a54 feat(data-reports): list every space's reports` (screen 28,
the admin's; finding 167). (The user's own reports and the report dialog are R3's — but they extend the files your
range creates: read those files at the head and say what R3's commits changed in them.)

**Read in the plan:** §2 PR 3's scope and acceptance criteria; §5 the S-decisions PR 3 uses; §7 *PR 3* (its DI-*);
§8 *PR 3*; §9 *PR 3 · Commit 1–3*; §10 *PR 3* and *Review Focus*; §13's PR 3 real run. **In the lead's report:** *The
lanes as they ran* (lane B), *The joins* (lane B, and lane C's conflicts against lane B's commit 3), the real run's PR
3 cases; `scripts\lane-b\REPORT.md` whole. **On `origin/main`:** the contract's *Data reports* (the owner's list and
decision; the admin's list and decision of an **unverified** space's reports; the codes), finding 8, finding 150,
foundation §12, the layer's `index.ts`.

**Look hardest at:**
- **Privacy — the reporter is anonymous to the owner:** nothing in the owner's list, sheet, toast, cache, query key,
  URL, test fixture or document names or hints at the reporter (name, email, id, an avatar, a count per person). The
  admin sees the reporter — only on the admin's screens.
- **Who decides what:** the owner decides the space's reports **once the space is verified** (as the contract says);
  the admin reads every report but decides **only an unverified space's** — read-only on a verified space's, with
  the line saying why; reception sees nothing of it. Hiding a control is never the authority: a refusal (403/409) is
  worded truthfully if the server answers it.
- **The decision:** resolve with an optional reply, dismiss with a **required** one (trimmed, bounded as the shared
  schema); the sheet's first focus on the reply (LB-D7), the focus after close and after a row leaves; a lost answer;
  the list refreshed (which keys are invalidated — the owner's, the admin's, any badge or count).
- **The admin's filters:** status, space (the `AdminSpaceFilter` in `features/space-links`), field — in the address,
  paging back to 1, «مسح»; **`FilterTag`** (finding 8): its remove button's name, 44 px on touch, its look from
  semantic tokens only, the showcase section.
- **Tests and breaks:** §10 PR 3's present / missing / weaker, and would each fail if its behaviour regressed.
- **Documents:** `data-reports.md`, `space-links.md`, `foundation.md` §12, `architecture.md` §2, `overview.md`,
  findings 8 (*Resolved*), 150 (evidence), 167 and the index — true to the code, one home per fact, `#129`.
