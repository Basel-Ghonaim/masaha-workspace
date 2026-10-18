# M4 — Check the documents' links in CI (finding 37)

**Continue in this conversation** (the owner's choice for this small item: you have read what it
needs during M3, so read only what is new below — a stated exception to workflow §9's "one fresh
conversation per Work Item"). Worker B · `masaha-b`, detached at `origin/main` (`49cd088`, after
#56) · branch `chore/check-links`, cut with `git fetch --prune origin`, then
`git switch --no-track -c chore/check-links origin/main`.

**Size cap:** no subagents, no workflow. **Plan:** `…\MASAHA_WORKER_B\PLAN\M4_PLAN.md` (save, then
stop for the reply). **Report:** `…\MASAHA_WORKER_B\REPORT\M4_REPORT.md`.

## 1. The task in brief

Links between documents are checked by hand (finding 37). M2 and the README showed a script finds
every broken link and anchor in seconds. Make it a real check: `npm run check:links`, run in CI, so
a broken link fails the PR. Finding 37 is resolved.

## 2. Read (new for this item only)

Finding 37; `.github/workflows/ci.yml`; root `package.json` (the `check:*` scripts); one existing
check with its unit test as the model (`apps/web/scripts/checkClasses.ts`); documentation §8 and
`setup.md` (*Commands*, *CI*) — you know the rest.

## 3. The settled decisions (review them in "Stronger decisions")

- **D1 — where:** `apps/api/scripts/checkLinks.ts` with `checkLinks.unit.test.ts` in the API's unit
  lane; the root script `check:links` runs it (`npm run check:links -w @masaha/api`, as `check:classes`
  does for the web). **No new dependency, no change to `package-lock.json`** (worker A's #57 changes
  it). Your plan may propose a better place under those two constraints.
- **D2 — the anchor rule is our own** (GitHub's slugs: inline markup dropped, lowercased, punctuation
  out but `-` and `_`, spaces to `-`, a repeated heading `-1`, `-2`), the one M2's and the README's
  checkers agreed on over 600 anchors. No `github-slugger`.
- **D3 — what it checks:** every `*.md` in the repository except `node_modules`, `dist`,
  `.design-sync/` and `docs/design/prototype/`: each relative link and image path (Markdown and
  `src`/`srcset`/`href` in HTML) resolves to a file or folder, each `#anchor` to a heading of its
  file; and each `docs/….md` path cited in a code comment under `apps/` and `packages/`. **External
  links (`http(s):`, `mailto:`) are not checked.** Fenced code and inline code are skipped.
- **D4 — CI:** `check:links` joins the `check` job's matrix (one entry).
- **D5 — the documents:** documentation §8 and workflow §2's phase-4 exception say
  `npm run check:links` instead of "the link check by hand"; `setup.md` (*Commands*, *CI*) and
  `CLAUDE.md`'s *Commands* list it; finding 37 resolved (status, dated resolution, the index).
- **D6 — review:** a light independent review follows (a CI change).

## 4. Tests and breaks

The unit test, seen failing first: a fixture tree with a good link, a missing file, a missing
anchor, a repeated heading (`-1`), a link inside fenced code (ignored), an image path, and a code
comment citing a missing document. **Make the break once** on the real repository: break one link in
a document, see `check:links` fail, restore it.

## 5. Checks — only these

`test:unit -w @masaha/api` (your new test's lane), `check:links`, lint and typecheck once, and
`format:check`. **Not** the component lane, `test:api`, the build: nothing they cover changes.

## 6. Pull request

Title `chore(ci): check the documents' links` (≤ 50 — count it), labels `chore`, `area:ci`,
`area:docs`, assigned to the owner. Two commits (the check with its test and script; CI and the
documents). Report as `final-report` says, with the merge-tree check against #57. Don't merge.
