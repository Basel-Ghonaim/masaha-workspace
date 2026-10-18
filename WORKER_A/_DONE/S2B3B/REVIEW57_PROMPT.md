# Review — PR #57 (S2b-3b: add a space, with its pin on the map)

You are an **independent reviewer** of PR #57 in the Masaha repository (Basel-Ghonaim/masaha). Two
reviewers work on it separately; this prompt is for both.
- **If you are OpenCode,** write your report to
  `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\REVIEW57_OPENCODE_REPORT.md`.
- **If you are Codex,** write it to
  `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\REVIEW57_CODEX_REPORT.md`.

## Rules

- **Run from `C:\Users\basel\masaha`** (the main folder) — not `masaha-b` or `masaha-design`.
- **Read-only.** No edits, commits, checkouts, switches, installs, npm or test runs, database
  commands, or GitHub comments. Read only from commit objects: `git fetch origin`, then pin to the
  head **`3650759`** (`gh pr view 57 --json headRefOid` must still say
  `36507590ff1783bb988883707318121c62b4a5ad`; if it does not, stop and say so). Base: `49cd088`. Use
  `git diff 49cd088...3650759 -- <paths>` and `git show 3650759:<file>`.
- **Report concrete problems only,** each verified in the code: file and line, the failing scenario
  (input → wrong result), the severity (**blocker / should-fix / nit**) and the fix. No praise, no
  summary of what the PR does. If you are not sure, say "plausible" and why.
- **No tool attribution** in what you write.

## What the PR must be (the owner's decisions)

Web, build and documents; no API change. The admin adds a space at `/dashboard/admin/spaces/new`:
one form, two sections (Basics: names and descriptions; Location: one active area, both addresses,
both landmarks, the pin), one `POST /admin/spaces`, then back to the list with a toast "{name} added".
- **The map** (`apps/web/src/shared/map/`): React Leaflet over OpenStreetMap, **loaded lazily**; no
  pin until the admin clicks; the pin is draggable and drawn from the design tokens (never Leaflet's
  default icon); a coordinates field ("31.52, 34.45", Arabic digits too) moves it both ways; a point
  outside `GAZA_STRIP_BOUNDS` is refused on the field; failing tiles show a line and the form still
  submits; `leaflet.css` lives in the design-system folder and is imported **only** by `shared/map`;
  the container is `dir="ltr"`; "© OpenStreetMap contributors" is always visible.
- **The build:** the data table moved to its own design-system entry (`@shared/design-system/data`,
  finding 45 resolved); `check:build` fails if TanStack Table, Leaflet or Leaflet's CSS reaches the
  site's first download, or if a library chunk is missing; lint keeps Leaflet inside `shared/map`.
- **`shared/forms`** gained two options, `prepare` and `failureLines`; the area field is a new
  `AreaSelect` in `features/lookups`, from the public catalogue (active areas only).
- **Project rules:** no sibling imports between features; components present, hooks prepare; no
  parameter, option or callback only tests pass; tests never `vi.mock` a module; one behaviour in one
  lane; no hardcoded user-facing text (both catalogues); no colour or CSS outside the design system;
  commit subjects ≤ 50 characters.

## Look at these, in this order

1. **Correctness of the form:** blank optional fields sent as absent; the coordinates parsed and
   validated; a 422 on its fields and the focus; a 409 and a 429; the navigation and the toast only
   after the list has been refreshed.
2. **The map:** the lazy boundary really keeps Leaflet out of the first download; the click/drag/field
   loop cannot get out of step; the tile-failure and code-failure paths; RTL; memory or listener leaks
   on unmount.
3. **The build checks:** `apps/web/scripts/checkBuild.ts`, `libraryChunks.ts`, `vite.config.ts` —
   would each check fail when it should, and never pass with nothing to check?
4. **`package-lock.json`:** the worker reports npm **cleared the dev flag on five existing packages**.
   Which, why, and does it put dev-only packages into a production install? Is anything else in the
   lock file changed beyond Leaflet, react-leaflet and their dependencies?
5. **The design-system entry:** every import of `DataTable` moved; nothing else left the barrel.
6. **The tests:** each would fail if its code broke; no `vi.mock`; titles true to their assertions.
7. **The documents:** `docs/features/spaces.md`, `lookups.md`, `frontend/architecture.md` §1, §3, §6,
   `foundation.md` §3, `setup.md`, `CLAUDE.md`, findings 45 (resolved), 46 (new), 27 (untouched) —
   each states the code truly.
8. **The commits:** five; check each subject's length — the first,
   `fix(design-system): keep the data table off the site`, looks over 50.

## Your output

One file (the path above): a one-line verdict; the findings, most severe first (severity, file:line,
scenario, fix); a short "Checked and fine" list; then stop.
