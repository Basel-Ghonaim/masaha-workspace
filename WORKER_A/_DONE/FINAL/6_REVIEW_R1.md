# Review of #132 — R1: foundation, design-system layer, build, and closing documents — git review · Auto mode
Head: a12c0790 · commits 25 · checks: green · head moved during the review: no
Verdict for my range: mergeable

## Findings (verified defects only, most severe first)
None.

## The checklist

1. **Every commit of my range read**

   - `fed3b46d` — feat(shared): carry a refusal's details.
   - `9c53b8dc` — feat(shared): refuse a published price changed.
   - `3c58a9a1` — feat(web): group the dashboard's navigation.
   - `a55da7bb` — feat(web): skip to the content in every shell.
   - `44df247c` — feat(web): give the account its place on a phone.
   - `40df132f` — feat(web): route the screens still to come.
   - `9755efe6` — feat(design-system): add a meter.
   - `06f3c154` — feat(design-system): draw bar charts and a heatmap.
   - `cee9736d` — feat(design-system): reach a held menu item.
   - `c0b8e36b` — feat(design-system): size a large input.
   - `3348faf3` — feat(lists): show a list's range and its steps.
   - `67747ed9` — feat(lists): mark the page asked while it loads.
   - `5d2797d5` — fix(lists): keep the scroll on a page change.
   - `098bc4e9` — refactor(lib): read Arabic-Indic digits once.
   - `6f5b51b7` — refactor(lists): share the row menus' triggers.
   - `43aad599` — feat(lib): build a CSV and a WhatsApp link.
   - `9a7dff2c` — docs: record finding 204.
   - `5d4178a3` — build(web): serve the site's parts by their entry.
   - `67b980a5` — build(web): keep dashboard-only code acyclic.
   - `3d5798b4` — test(web): load the lazy shells before waiting.
   - `5c1dabd8` — docs: record finding 212.
   - `9bf66b52` — docs: record every screen of v1 as built.
   - `0676d604` — docs: close the findings v1 accepts.
   - `10a72981` — refactor(web): remove the placeholder page.
   - `a12c0790` — docs: close the findings v1 resolves.

2. **Plan decisions**

   Built as approved. The refusal envelope exposes only the typed `userId` detail, and the API contract,
   shared shape, both catalogues, server handler, and web normalizer agree. `SPACE_NAV` and `ADMIN_NAV`
   provide the approved role-filtered grouped navigation; reception receives exactly desk, customers,
   announcements, and own payments, while owner-only finance, audit, and owner pages are excluded.
   All three shells render the skip link, and the account menu is placed in the phone drawer.
   The layer components use semantic tokens and accessible hidden tables/roles; the list helpers preserve
   the requested page state and scroll; the public entries and build checks enforce the intended chunk
   boundaries. The closing documents and findings index match the head's resolved/accepted/open statuses.

3. **Money, roles, privacy, keys and locks**

   Checked: the owner overview contains no amount; role filtering is explicit in route guards and
   navigation; error `details` is restricted to `{ userId }` and contains no private record data.
   No money, key, or lock defect is present in this range.

4. **Planned tests and breaks**

   Present and reported green for U0, U3, and U4. The recorded breaks cover the refusal details,
   catalogue parity, grouped navigation and role visibility, shell focus/skip-link behavior, phone
   account placement, every new layer component, list range/current/loading/scroll behavior, digit
   conversion, CSV/WhatsApp helpers, public-entry/build rules, and lazy-shell warm-up. The final report
   records the complete unit/component/API/build verification green on the head; the tests would fail
   for the documented regressions.

5. **Screens in my range**

   The range owns shared shells, navigation, account placement, and reusable layer behavior rather than
   a single feature screen. The relevant shell and account surfaces are implemented for RTL/LTR, light/
   dark, responsive phone/tablet/desktop behavior, loading/error states where applicable, and keyboard
   access. The 32-screen mapping and build documents name the prototypes and record all screens as built.
   I did not run a browser or independently render the prototypes because this review is restricted to
   read-only commit-object inspection; the lead's real-run report and component tests are the available
   evidence.

6. **Findings closed**

   Findings 103, 104, 105, 130, 132, 165, 169, 180, and the other U0/U3/U4 findings in this range are
   implemented and their resolution records/index entries are present at the head. Findings 204 and 212
   are deliberately still Open and are noted below; they are not falsely marked resolved.

7. **Documents**

   The changed plan-facing documents are consistent with the code: the API contract names the new
   envelope detail and error code; foundation and architecture document the layer and chunk rules;
   the screen archive maps all 32 screens; the build map and feature documents record the completed
   surfaces; and the findings index is regenerated once at the end. No duplicate or contradictory
   claim was found in the reviewed documents.

## Decisions taken without the owner in my range, judged

- **LL-D1:** sound. Memory-constrained validation was narrowed per commit and completed with full
  verification before hand-over.
- **LL-D2:** sound. One-page pagination remains available except where the approved announcement
  design explicitly opts out.
- **LL-D3:** sound. Range summaries are shared and isolated for bidi reading; the existing table
  layout boundary is preserved.
- **LL-D4:** acceptable. Matching the requested page from the normalized address is a direct
  implementation of the loading-state requirement.
- **LL-D5:** sound. Chart dimensions, token-based tones, hidden tables, and heatmap steps follow the
  approved component contract.
- **LL-D6:** sound. The large input is a typed layer variant and preserves the native control behavior.
- **LL-D7:** sound. Reminder substitution is centralized and literal values are preserved.
- **LL-D8:** sound. BOM verification is placed in the lane that can inspect browser-generated bytes.
- **LL-D9:** sound and correctly recorded as finding 204 rather than silently changing the approved CSV
  contract.
- **LL-D10:** sound. The held-menu behavior was corrected without disabling the item, preserving
  keyboard reachability and preventing selection.

## Outside my range

- Finding 204 remains Open because the owner has not chosen a CSV-formula neutralization rule.
- Finding 212 remains Open because the phone/tablet route to written-off visits still awaits the
  owner-approved reachability fix.
- Deployment/measurement findings 23, 33, 46, 64, 65, and 152 remain Open as documented deployment
  follow-ups. They are outside these commits and are not findings for R1.

## Not checked, and why

No installs, tests, servers, database commands, checkout, edits to repository files, or browser runs
were performed, as required by the read-only commit-object review prompt. CI status was checked with
`gh pr checks 132` and was green; the head was rechecked with `gh pr view 132 --json headRefOid` and
remained `a12c0790`.
