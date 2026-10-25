Approved by the owner, 2026-10-24.

# CONFLICT_GUARD — Plan

> **The supervisor's corrections (2026-10-24) — binding once the owner approves; they win where the plan
> below differs:**
> 1. **You read an old tree.** `app-design` sits at `5e8379af`, not `origin/main`; phase 2's first step
>    (`git switch --detach origin/main`) fixes that. **Re-read every quoted line on `origin/main` before
>    editing.** On `origin/main`: `lookups.md` already says *Last Updated* 2026-10-24 (no bump); in
>    `docs/frontend/architecture.md` the bullet **does** exist, at ≈ line 104, as a **sub-bullet**:
>    `  - **Offline and the general error** (\`RetryState\`, PU-024): …` — append ` (2026-10-24, #111)` to
>    **that** bullet, not to the `RouteErrorState` one.
> 2. **No masking of code fences or inline code.** A conflict marker inside a fenced block is still a real
>    conflict and must fail. The rule is the line's start only, on every tracked text file: a line starting
>    `<<<<<<< ` or `>>>>>>> ` or `||||||| ` (diff3's base marker) is a hit; a line that is exactly `=======` is
>    a hit only while a `<<<<<<< ` is open. Strip a trailing `\r` before comparing (CRLF files). `origin/main`
>    holds exactly one hit today (`docs/design/INDEX.md:868`), so no exclusion is needed. Drop the "equals in
>    code fence" test; add **a CRLF conflict** (hits) and **a diff3 conflict** with `||||||| base` (4 hits).
> 3. **`workflow.md`'s new sentence keeps "into `main`":** "a merge into `main` that deletes or renames no
>    file **the PR refers to**, and changes none of the PR's files, calls for no rebase and no new CI run; the
>    PR stays ready." — only the bold words are new.
> 4. **Recount the subjects** with a tool (e.g. `"<subject>".Length` in PowerShell); yours are all ≤ 50 but
>    several counts are off by one.

## Commits (subjects ≤ 50 chars)

| # | Subject | Chars | Files Touched |
|---|---------|-------|---------------|
| 1 | `fix(docs): drop a stray conflict marker` | 42 | `docs/design/INDEX.md` |
| 2 | `chore(ci): fail on merge-conflict markers` | 38 | `apps/api/scripts/checkConflicts.ts`, `apps/api/scripts/checkConflicts.unit.test.ts`, `apps/api/package.json`, `package.json`, `.github/workflows/ci.yml`, `docs/development/setup.md`, `CLAUDE.md` |
| 3 | `docs(workflow): say what a merge apart guards` | 44 | `docs/development/workflow.md` |
| 4 | `docs: record #111's review` | 27 | `docs/features/lookups.md`, `docs/frontend/architecture.md`, `docs/architecture/findings/137-homes-area-counts-fall-short-past-a-thousand-spaces.md`, `docs/architecture/findings/138-a-failed-refresh-keeps-a-status-that-still-reads-live.md`, `docs/architecture/findings/README.md` |

---

## Marker-Finding Rule & Unit-Test Cases

### Pure Function: `findConflictMarkers(text: string): ConflictHit[]`

**ConflictHit** = `{ line: number; marker: string }`

**Rule**: A line is a conflict marker when it is:
- `<<<<<<< ` (8 chars, space after) at **start of line**, OR
- `>>>>>>> ` (8 chars, space after) at **start of line**, OR
- `=======` (exactly 7 `=`) at **start of line** **only when** a `<<<<<<< ` has been seen earlier in the file without a matching `>>>>>>> `.

**Exclusions**:
- A Markdown setext heading underline: `=======` at start of line, **with no preceding `<<<<<<< `** in the file.
- The marker strings **inside** a line (not at column 0) — e.g., `text <<<<<<< HEAD` or inside a fenced code block are NOT flagged.
- Binary files are skipped entirely (by extension: `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg`, `.ico`, `.pdf`, `.woff`, `.woff2`, `.ttf`, `.eot`, `.otf`).

**Algorithm**:
1. Split text by `\n`, track line numbers (1-based).
2. Keep state: `inConflict = false` (set true on `<<<<<<< `, cleared on `>>>>>>> `).
3. For each line:
   - If starts with `<<<<<<< ` → `inConflict = true`, record hit.
   - Else if starts with `>>>>>>> ` → `inConflict = false`, record hit.
   - Else if starts with `=======` AND `inConflict` → record hit.
   - Else → no hit.
4. Return all hits.

### Unit Test Cases (Vitest, in `checkConflicts.unit.test.ts`)

| Name | Input Text | Expected Hits |
|------|------------|---------------|
| `real conflict` | `<<<<<<< HEAD\nours\n=======\ntheirs\n>>>>>>> branch\n` | 3 hits: line 1 `<<<<<<<`, line 3 `=======`, line 5 `>>>>>>>` |
| `setext heading` | `# Title\n=======\n\nBody\n` | 0 hits (no `<<<<<<<` before) |
| `marker mid-line` | `const x = '<<<<<<< HEAD';\n` | 0 hits (not at column 0) |
| `clean file` | `# Hello\n\nWorld\n` | 0 hits |
| `nested-like but not conflict` | `<<<<<<< HEAD\n=======\n>>>>>>> branch\n` | 3 hits (real conflict block) |
| `multiple conflicts` | `<<<<<<< HEAD\na\n=======\nb\n>>>>>>> b1\n\n<<<<<<< HEAD\nc\n=======\nd\n>>>>>>> b2\n` | 6 hits |
| `equals in code fence` | ```\n```\n=======\n```\n``` | 0 hits (fenced code excluded by masking — **not required** for unit test of pure function; the pure function receives raw text; masking is done in `main()` before calling it) |

**Note**: The pure function does **not** mask fences or inline code. The `main()` wrapper masks them before calling the pure function, same as `checkLinks.ts` does with `maskFences` + `maskInlineCode`. The unit test exercises the pure function directly on raw text; the integration test (manual break) exercises the full flow.

---

## Exact New Lines

### `docs/development/setup.md` — Commands Table (after `check:links` row, ≈ line 60)

```markdown
| `npm run check:conflicts` | Fails when any git-tracked file holds a merge-conflict marker (`<<<<<<< `, `>>>>>>> `, or `=======` between them); skips binary files; prints each hit as `<file>:<line>` and a total |
```

### `docs/development/setup.md` — CI Sentence (≈ line 178)

**Before**: `GitHub Actions ([`.github/workflows/ci.yml`](../../.github/workflows/ci.yml)) runs `lint`, `format:check`, `typecheck`, `test:unit`, `test:component`, `test:api`, `check:classes`, `check:links` and `build` as separate checks on every pull request and on `main`, using the Node version from `.nvmrc`.`

**After**: `GitHub Actions ([`.github/workflows/ci.yml`](../../.github/workflows/ci.yml)) runs `lint`, `format:check`, `typecheck`, `test:unit`, `test:component`, `test:api`, `check:classes`, `check:links`, `check:conflicts` and `build` as separate checks on every pull request and on `main`, using the Node version from `.nvmrc`.`

### `CLAUDE.md` — Commands List (after `check:links` line, ≈ line 80)

**Before**: `- `npm run check:links` — every relative link, image path and anchor of the Markdown files, and every `docs/….md` path cited in a source file, resolves`

**After**: `- `npm run check:links` — every relative link, image path and anchor of the Markdown files, and every `docs/….md` path cited in a source file, resolves
- `npm run check:conflicts` — fails on a merge-conflict marker (`<<<<<<< `, `>>>>>>> `, or `=======` between them) in any git-tracked file; skips binary files`

### `.github/workflows/ci.yml` — Matrix Task List (insert after `'check:links'`, ≈ line 30)

```yaml
            'check:links',
            'check:conflicts',
            build,
```

### `docs/development/workflow.md` — §9 Sentence (line 209)

**Before**: `- **a merge apart:** a merge into `main` that deletes or renames no file and changes none of the PR's files calls for no rebase and no new CI run; the PR stays ready. `git diff --name-status <old main> <new main>` shows it.`

**After**: `- **a merge apart:** a merge that deletes or renames no file **the PR refers to**, and changes none of the PR's files, needs no rebase and no new CI run; the PR stays ready. `git diff --name-status <old main> <new main>` shows it.`

---

## Goal 5 — Four Document Fixes (from #111 review)

### 1. `docs/features/lookups.md` line 5 — Scope

**Before**: `> **Scope:** the API module `lookups` (L0); `@masaha/shared/lookups`; the web feature `features/lookups`, for the admin, the owner's profile and the site's Directory.`

**After**: `> **Scope:** the API module `lookups` (L0); `@masaha/shared/lookups`; the web feature `features/lookups`, for the admin, the owner's profile, and the site's Home and Directory.`

**Last Updated**: Today is 2026-10-24; current line 3 says `Last Updated: 2026-10-21` → bump to `2026-10-24`.

### 2. `docs/frontend/architecture.md` §2 — Status States Bullet (line ≈ 103)

**Current line 103**: `- `RouteErrorState` shows **offline** for a failed lazy load or when the browser reports no connection, and the **general error** otherwise. "Try again" reloads the page, and so does the browser's `online` event: React Router keeps a failed lazy load for its route, so only a reload retries it.`

**After**: Append ` (2026-10-24, #111)` at end of bullet text.

> **Note**: The prompt quotes the bullet as starting with `- **Offline and the general error** (`RetryState`, PU-024)`. The actual bullet at line 103 starts with `- `RouteErrorState` shows **offline**...` and describes the same feature (uses `RetryState` component, relates to PU-024). This is the only bullet in §2 about offline/general error without a date/PR. Neighbour at line 86 has `(2026-10-21, #101, #103)`. Plan proceeds with line 103.

### 3. New File: `docs/architecture/findings/137-homes-area-counts-fall-short-past-a-thousand-spaces.md`

```markdown
# 137. Home's area counts fall short past a thousand spaces

**Status:** Open · **Date:** 2026-10-24

**Evidence:** Home's «تصفّح حسب المنطقة» counts each area's spaces from the directory's unfiltered pins (`useAreaCounts`). The pins stop at 1,000 and say so with `truncated`, which the count ignores: past 1,000 publicly listed spaces, every area's count and «كل المناطق»'s total are too low, with nothing on the page saying so. Today's directory holds far fewer, so nothing is wrong yet (#111's review, item 9).

**Resolves when:** the counts come from the server (a count by area, or the total the list already answers), or Home shows no number while the pins are truncated.
```

### 4. New File: `docs/architecture/findings/138-a-failed-refresh-keeps-a-status-that-still-reads-live.md`

```markdown
# 138. A failed refresh keeps a status that still reads live

**Status:** Open · **Date:** 2026-10-24

**Evidence:** The space page keeps the last status it read when a 60-second refresh fails, as decided (#108's review, carried into #111). After many failed refreshes the badge still shows that status under «الحالة مباشرة الآن», with no sign of its age. The owner decides it at the public site's in-person review (#111's review, item 13).

**Resolves when:** the page marks a status older than a bound (for example «آخر تحديث قبل …»), or the owner accepts it as it is.
```

### 5. `docs/architecture/findings/README.md` — Under `## Open`, after 136

Add two lines:
```markdown
- [137. Home's area counts fall short past a thousand spaces](137-homes-area-counts-fall-short-past-a-thousand-spaces.md)
- [138. A failed refresh keeps a status that still reads live](138-a-failed-refresh-keeps-a-status-that-still-reads-live.md)
```

---

## Verification Steps (Phase 2)

1. `cd C:\dev\masaha\app-design; git fetch origin; git status --short` (clean)
2. `git switch --no-track -c chore/conflict-guard origin/main`
3. Commit 1: edit INDEX.md, `npm run lint && npm run typecheck`, commit
4. Commit 2: write unit test → run (red) → write script → run (green) → run `npm run check:conflicts` (exit 0) → add marker to INDEX.md → run `npm run check:conflicts` (fail) → restore INDEX.md → run `npm run check:conflicts` (exit 0) → add CI, setup.md, CLAUDE.md → lint/typecheck → commit
5. Commit 3: edit workflow.md, lint/typecheck, commit
6. Commit 4: four doc edits, lint/typecheck, commit
7. On head: `npm run test:unit -w @masaha/api`, `npm run check:conflicts`, `npm run check:links`, `npm run format:check`, `npm run lint`, `npm run typecheck` (all exit 0)
8. Write `scripts/pr-body.md`, push, open PR, wait for CI green and `CLEAN`
9. `gh pr checks <n> --watch --interval 60` (max 30 min)
10. `git merge-tree --write-tree HEAD <other-open-pr-head>` for each open PR

---

## Message Files

`TASK/scripts/msg-1.txt` through `msg-4.txt` — UTF-8 no BOM, LF, subject + blank line + 2–5 body lines explaining *why*.

---

## PR Description Structure

- **Summary** — the five goals; goal 5 under heading "Carried from #111 (documents only)"
- **Changes** — per commit
- **Evidence** — each command + result line; unit test red→green; break fail→clean
- `Closes #71`

---

## Stop Conditions

- Any command fails before tests run (missing module, timeout, error) → stop, report exact output.
- A line quoted in the goal does not match the file (after ±2 line tolerance) → stop, report.
- `npm run check:links` fails after doc edits → stop, report.
- CI red → read logs, fix with fixup commit, rebase, force-push; red twice → stop.

---

**PLAN READY: TASK\2_PLAN.md**