# PROTOTYPE_SPLIT — the plan

> Worker: Claude Code, main folder `C:\dev\masaha\app`, on `main` `f073decb` (clean, equal to `origin/main`,
> fetched 2026-11-15). Phase 1 was read-only: no branch, no repository file written. The only files written are
> this plan and the scan's script and output in `TASKS\PROTOTYPE_SPLIT\scan\`. I also wrote one scratch list of
> the archive's links to the session scratchpad by mistake; it is outside both repositories and holds no secret.
> **Override, stated:** the `write-plan` skill plans in plan mode and leaves it with a summary. The prompt says to save
> the plan to this file and stop, and the prompt wins (CLAUDE.md, *Decision precedence*).

## 1. Summary

`docs/design/` (the prototype, the screenshots it was drawn from, its two check scripts and its four documents)
moves **with its history** to a new public repository, `Basel-Ghonaim/masaha-prototype`, built in
`C:\dev\masaha\masaha-prototype` with `git subtree split`. The new repository gains its own README, CLAUDE.md,
an updated BRIEF, a `decisions/` folder and the `?v=` variant mechanism with its switcher. One PR in `masaha`
(**#147**, branch `chore/design-archive-out`) then deletes `docs/design/`. The same PR repoints every pointer to the
public URL, drops the four exclusions that existed only for the archive, and records **ADR 0020**.

**One blocker for the owner before anything is published (§6.3):** the archive as it stands on `main` today breaks
the identity rule. Five About screenshots show «مشروع تخرّج — جامعة …» / "Graduation project — … University …", and
the first `About.html` has the same line in its source. I propose redacting both in the new repository's history
(R1), and I stop for the owner's choice.

## 2. The contract

**Scope**
- A public repository `Basel-Ghonaim/masaha-prototype` whose history is the 89 commits of `docs/design/`, its tree at
  the split identical to `main:docs/design` (or identical except for the redacted files the owner approves, §6.3).
- In it: the root made standalone (scripts, line endings, five links out), the variant mechanism with its switcher
  (no variant designed), `README.md`, `CLAUDE.md`, the updated `BRIEF.md`, `decisions/README.md`.
- In `masaha`, PR #147: ADR 0020, every pointer repointed or reworded, `docs/design/` deleted, its four exclusions
  dropped.

**Acceptance criteria**
- [ ] The new repository's split tip has `^{tree}` = `c9183a63ff75e6e3138a455ad68f89424828afe9`
  (`git rev-parse main:docs/design` in `masaha` today), 89 commits, authors and dates kept. If R1 is approved, the
  redacted tip differs from it by exactly the approved files (`git diff --name-status`).
- [ ] The tag `design-2026-09-29` exists in the new repository, on the split commit of `14fdc60b`.
- [ ] `node scripts/check-parse.mjs` and `node scripts/check-classes.mjs` pass at the new root, with the baseline
  counts (`52/52 blocks parsed, from 42 pages and the modules`; `361 classes used, 5 dead uses, 0 new`, measured
  today in `masaha`), plus the mechanism's own files.
- [ ] Served over HTTP, a page loads unchanged without `?v=`. With a registered variant, `?v=<name>` renders the
  variant, and the switcher lists the original and the variant.
- [ ] The history scan approved by the owner; nothing published before.
- [ ] PR #147: no relative link and no path citation into `docs/design` remains (`git grep`); every repointed URL
  answers 200 once the repository is public; every check of §8 green locally and in CI; GitHub shows `CLEAN`.

**Out of scope**
- Designing any variant. Changing any prototype page beyond adding the two mechanism script tags.
- Finding 215's fix (the prototype's Home and today's line): it moves with the prototype, see §7.
- Rewriting `masaha`'s own history (it also carries the university, §6.3). That is the owner's, if ever.
- `.design-sync/` (it syncs the production design system to Claude Design; it stays in `masaha`).
- Regenerating the screenshots, or refreshing the vendored design-system bundle (`prototype/_ds/`).

## 3. Reading done

CLAUDE.md; `docs/development/workflow.md`; `docs/README.md`; `docs/architecture/documentation.md`; the open
findings' titles in `findings/README.md`, and findings 14, 19, 37, 73, 74, 96, 110, 130, 165, 215;
`docs/design/README.md`, `INDEX.md` (the parameter tables and the About rows), `SCREENS.md`, `CHANGES.md` (head and
U11), `prototype/BRIEF.md`; `docs/design/scripts/check-parse.mjs`, `check-classes.mjs`; ADR 0018, ADR 0019 (the
format; the next is 0020); foundation §13 and §16; `checkLinks.ts` (the walk and `NOT_SCANNED`); `eslint.config.js`,
`.prettierignore`, `.coderabbit.yaml`, `.gitattributes`; `Sign in.html`, `masaha/i18n.js`, `masaha/shared.jsx`'s
`pageParams`, the `?demo=` and `?prices=` readers; the grant script's header.

## 4. Inventory

### 4.1 What is in `docs/design/` (verified)

| Path | Files | Size | Notes |
|---|---|---|---|
| `prototype/` | 117 | 7.5 MB | 42 HTML pages (38 load `masaha/i18n.js`; not the board `Flows - states.html`, `Reset email.html`, `Sign in - board.html`, `Wordmark.html`), 14 `.jsx` modules, 5 `_*head.txt` templates, `_vendor/` (React, Babel), `_ds/` (the vendored design-system bundle and fonts), `masaha/logo/` (10 SVGs), `BRIEF.md`, `serve.json`, `.thumbnail` (a WebP of the admin overview) |
| `screens/` | 437 | 17 MB | WebP screenshots, each added once in `14fdc60b` and never changed |
| `scripts/` | 2 | | `check-parse.mjs`, `check-classes.mjs` |
| `README.md`, `INDEX.md`, `SCREENS.md`, `CHANGES.md` | 4 | | |

560 files in all. **89 commits** touch `docs/design` (no merge among them); **86** touch `prototype/` since
2026-09-30, as the supervisor said. The tag **`design-2026-09-29`** (annotated, on `14fdc60b`) is the design as
delivered; README and CHANGES name it, so it must exist in the new repository too. The folders `app-design` and
`app-dr` are clean, detached worktrees at older `main` heads, and no PR is open. Nothing else edits `docs/design`
in flight.

### 4.2 Every pointer from outside, and its fate

*Repoint* = the link or path becomes `https://github.com/Basel-Ghonaim/masaha-prototype/blob/main/<path>` (spaces as
`%20`, the anchor kept). *Reword* = the sentence changes. *Leave* = a word that means "the design", or a record's
prose that cites no path.

**Configuration and code**

| Where | What | Fate | Supervisor |
|---|---|---|---|
| `.prettierignore:8–9` | `docs/design/` and its comment | **Drop** | listed |
| `eslint.config.js:248–249` | `globalIgnores(['docs/design/'])` and its comment | **Drop** | listed |
| `apps/api/scripts/checkLinks.ts:175` | `NOT_SCANNED`'s `'docs/design/prototype/'` | **Drop the entry**, keep `'.design-sync/'` | listed |
| `.coderabbit.yaml:9–11` | `path_filters: '!docs/design/**'` and its comment | **Drop** the filter and comment, keep the rest | **missed** |
| `apps/web/.../Logo/drawing.ts:2` | comment: copied from `docs/design/prototype/masaha/logo/masaha-logo-berry.svg` | **Reword** to the repository's URL | listed |
| `apps/api/src/modules/auth/email/resetEmail.ts:4–5` | comment: «as the design draws them (docs/design: Reset email.html)» | **Reword** to `masaha-prototype: prototype/Reset email.html` | **missed** |
| `apps/api/src/modules/auth/email/resetEmail.copy.ts:4` | comment: «the design's (docs/design: Reset email.html)» | **Reword**, same | **missed** |
| `apps/web/src/features/finance/services/reminderText.ts:5` | «as the prototype's (DI28)» | Leave (a word) | — |
| 13 test files and `componentSetup.ts`, `fakeCanvas.ts` | `Element.prototype`, `Navigator.prototype`, … | Leave (JavaScript's `prototype`) | — |

Nothing else needs the exclusions. `npm run check:classes` reads only `apps/web`. `check:conflicts` and
`format:check` walk git-tracked files, and none will be left. TypeScript includes no `docs/`. CI
(`.github/`) and `package.json` name no `docs/design`.

**Bootstrap, map and platform documents** (active documents: reworded where the sentence says "archived here")

| Where | What | Fate |
|---|---|---|
| `CLAUDE.md:71` | `- **Design archive** → \`docs/design/\` (screens, prototypes)` | **Reword:** `- **Design archive and prototype** → the public repository [masaha-prototype](URL), read-only from here ([ADR 0020](docs/architecture/decisions/0020-…md))` |
| `docs/README.md:78–79` | the `### design/` section and its entry | **Replace** with a section *The design, in its own repository*: one line with the URL, what it holds, and «read it when your task builds a screen» (SCREENS.md's URL kept). The map links an outside repository by URL only (documentation §8 forbids paths, not URLs) |
| `docs/README.md` ADR list | — | **Add** `[0020](…) the design archive and the prototype in their own repository` |
| `foundation.md:474` (§13) | «archived in [docs/design/](../../design/README.md): [SCREENS.md](../../design/SCREENS.md) maps …» | **Reword:** «are in the public repository [masaha-prototype](URL) ([ADR 0020](…)): its [SCREENS.md](URL) maps …» |
| `foundation.md:562` (§16) | «The source files, the owner's: `docs/design/prototype/masaha/logo/` …» | **Repoint:** the folder's URL (`…/tree/main/prototype/masaha/logo`), text otherwise unchanged |
| `docs/features/auth.md:42` | `[SCREENS.md](../design/SCREENS.md) row 7` | **Repoint** |
| `docs/features/directory.md:144` | `(\`docs/design/CHANGES.md\`, R9)` | **Repoint** as a link to CHANGES.md's URL |
| `docs/features/directory.md:141, 168, 182`; `audit.md:64`; `finance.md:70–71`; `payments.md:69`; `visits.md:74` | «the prototype's …» | Leave (words) |
| `docs/plans/v1-mvp.md` (18 links: lines 29, 40, 41, 49, 62, 73, 83, 94, 101, 113, 124, 132, 133, 134, 143, 144, 161, 162) | `../design/SCREENS.md#…` | **Repoint**, anchors kept (GitHub's anchors equal ours: `#public-site-9`, `#my-account-3`, `#owner-and-reception-dashboard-13`, `#admin-8`) |
| `docs/plans/foundation.md:217, 311, 348` | `../design/README.md`, `../design/SCREENS.md` | **Repoint** |
| `docs/plans/historical/design-system-layer.md:246` | `docs/design-system-built` | Leave (a branch name) |
| `foundation.md:3, 527, 530` | Claude Design | Leave |

**Records** (documentation §1: only the link whose target moved is repointed; a path in backticks is turned into
the same text linked to its URL, nothing else changes)

| Where | What | Fate | Supervisor |
|---|---|---|---|
| finding 14 `:10–11` | `[design archive](../../design/SCREENS.md)`, `[design brief](../../design/prototype/BRIEF.md)` | **Repoint** both | listed |
| finding 19 `:5` | `` `docs/design/prototype/Reset email.html` `` | **Repoint** | listed |
| finding 32 `:5` | `[SCREENS.md](../../design/SCREENS.md)` | **Repoint** | **missed** |
| finding 37 `:9` | prose: «except … `docs/design/prototype/`» | Leave (a record of what the check did then) | listed |
| finding 73 `:5` | `[docs/design/prototype/masaha/profile-b.jsx](../../design/prototype/masaha/profile-b.jsx)` | **Repoint** | listed |
| finding 74 `:5` | `[…](../../design/prototype/Admin%20space%20edit.html)` | **Repoint** | listed |
| finding 96 `:5` | `` `docs/design/prototype/Owner settings.html` `` | **Repoint** | listed |
| finding 110 `:1, 5, 10` | «the desk prototype (`desk-core.jsx`, `desk-data.js` in the design archive)» | Leave (no path) | listed |
| finding 130 `:5` | `[the design's changes](../../design/CHANGES.md)` | **Repoint** | **missed** |
| finding 165 `:5` | «the settled prototypes» | Leave | listed |
| finding 215 `:6–7` | `` `docs/design/prototype/Home.html` ``, `` `docs/design/prototype/masaha/shared.jsx` `` | **Repoint** both | listed |
| findings README `:19, 127` | titles 215 and 110 | Leave (titles) | listed |
| ADR 0019 `:8, 23` | «in the design archive» | Leave (still true: the archive keeps coral) | **missed** |

**From inside the archive out** (they break at the new root; fixed in the new repository's first own commit)

| Where | Link | Fate |
|---|---|---|
| `CHANGES.md:25` | `../api/api-contract.md#4-pagination` | masaha URL |
| `CHANGES.md:30` | `../architecture/findings/44-…md` | masaha URL |
| `CHANGES.md:355` | `../architecture/decisions/0019-…md`, `../frontend/design-system/foundation.md` | masaha URLs |
| `SCREENS.md:60` | `../frontend/design-system/foundation.md#16-the-logo` | masaha URL |
| `README.md:43–46`, both scripts' usage comments | `node docs/design/scripts/…`, «`docs/design/` is outside ESLint …» | reworded for the new root (README is rewritten anyway, §6.4) |
| `CHANGES.md:242–245` | `docs/design/prototype/…` in the *Where* column | Leave (a record's text, no link) |

All other 487 relative links in the archive's Markdown stay inside it and keep working at the new root. The scripts
resolve `prototype/` from their own folder (`join(dirname(…), '..', 'prototype')`), so their paths hold too. **One
thing breaks:** `check-parse.mjs` reads Babel through `globalThis.Babel`, which only works because `masaha`'s root
`package.json` says `"type": "module"`. The comment says so. Without it, Node loads the UMD file as CommonJS, it
sets `module.exports`, and `Babel` is `undefined`. The fix takes whichever is set:
`const loaded = require(babelPath); const Babel = loaded?.transform ? loaded : globalThis.Babel;`.

## 5. The scan (P2), over every commit

Method (`scan\scan_history.py`, read-only): every one of the 89 commits' trees under `docs/design`, giving **1,079
distinct blobs**. The 631 text blobs were matched line by line. The 448 binaries (423 WebP, 24 fonts, `.thumbnail`)
cannot be read as text. The 89 commit messages were matched too, with their authors and committers. No path has
ever been deleted (560 paths, all at the tip), so nothing hides in a removed file. Full lists:
`scan\out\{secret,email,phone,identity,owner-name,messages,blobs}.txt`.

**Secrets: none.** 11 unique hits: the demo password fields of `Register.html`'s sample states, the reset email's
sample link `https://masaha.example/reset-password#token=…`, and identifiers named `token`/`password` inside
`_vendor/` (Babel, React) and the vendored bundle. No connection string, key, JWT, `.env` content or variable name of
`apps/api/.env`. No `.env` file ever.

**E-mails: placeholders only.** 24 addresses, all `@example.com`, `hello@masaha.example`, and `sara@gmial.com`
(39 hits). The last is Register's typo-suggestion demo; `gmial.com` is a real typo domain but no one's address.

**Phones: placeholders only.** `+970 59 000 0000`–`0099`, `+970 59/56 000 1001`–`1016`, all on the reserved-looking
`000` block. One exception to list: **`0599 123 456` / `+970599123456`** (81 hits, `profile-b.jsx`'s input example,
`profile-c.jsx`'s sample contacts, CHANGES.md:103). It is a syntactically valid Jawwal number in an obvious
`123456` pattern. I take it for a placeholder; it is the owner's to confirm. `0890-0891` is a font's Unicode range.

**People.** The commits: 89 by `Basel-Ghonaim <baselghonaim@gmail.com>` (author and committer), already public in
`masaha`. The owner's own first name is the sample admin's: «باسل» in `Flows - states.html` («Admin «باسل»»),
`basel@example.com` (20 hits). The other sample people are common first names (سارة أحمد, نور, سامي, أحمد,
ريم, …). Nothing marks them as real people. The sample spaces are named Focus Hub, Branch Hub, Number One Hub, ZM
Hub, Golden Hub and White Space, with coordinates in An-Nasr and Al-Rimal. If any is a real business, its name and
rough position are public sample data. That is not personal data, but the owner should know.

**The identity rule: every hit**, with its first commit and file (the pattern of the prompt, case-insensitive):

| First commit | File | Hit | At the tip? |
|---|---|---|---|
| `14fdc60b` | `prototype/About.html:99` | «مشروع تخرّج — جامعة القدس المفتوحة، فرع غزة» / "Graduation project — Al-Quds Open University, Gaza branch" (**names the university**) | **No:** removed in `32f0eacd` (U11). One blob, `93f287e5` |
| `14fdc60b` | `screens/10-about-error-pages/01-about-desktop-1440.webp` | the same line, **drawn in the screenshot** (I looked at it) | **Yes** |
| `14fdc60b` | `screens/10-about-error-pages/02-about-phone-390.webp` | the same, Arabic (looked at) | **Yes** |
| `14fdc60b` | `screens/11-variants/35-about-en-light-desktop-1440.webp` | the same, English (looked at) | **Yes** |
| `14fdc60b` | `screens/11-variants/34-about-ar-dark-desktop-1440.webp`, `36-about-en-dark-desktop-1440.webp` | the same About page as delivered (INDEX rows 324, 326). Not yet opened; Phase 2 opens them before any redaction | **Yes** (expected) |
| `32f0eacd` | `CHANGES.md:139` (52 versions) | «**U11** About. The university line goes (the owner's rule: …)» (says *the university*, does not name it) | **Yes** |
| `14fdc60b` | `prototype/masaha/details-data.js:28` | «يتطلب بطاقة جامعية سارية» / "The student price needs a valid university ID" (sample space rule) | Yes |
| `14fdc60b` | `prototype/masaha/details-data.js:26, 32` | "short tech courses", «دورة أساسيات البرمجة» / "programming basics course" (sample announcements) | Yes |
| `a9b06b4a`, `516ce763` | `Admin lookups.html:37–39`, `admin-data.js:84`, `profile-b.jsx:13, 420` | the amenity icon `graduation-cap`, «قبعة تخرّج» / "Graduation cap" | Yes |
| `14fdc60b` | `About.html:42` | «قبل أن تخرج» ("before you leave"; the verb خرج, not تخرّج) | Yes |
| `b2ba7ac0` | `masaha/desk-core.jsx:550` | «تخرج الزيارة من «غير محصّل»» (the same verb) | Yes |
| `14fdc60b` | `_vendor/babel.min.js`, `_vendor/react.js` | `wrapParenthesis`, `SpeechSynthesis`, `fontSynthesis` ("thesis" inside words) | Yes |
| — | the 89 commit messages | no hit | — |

No supervisor, defence, college, instructor, «مشرف», «مناقشة», «كلية», «مساق» or «دكتور» anywhere.

**The scan's limit:** text only. Of the 423 screenshots I opened three About images (and the `.thumbnail`). The
About line is the only identity text the source of any page ever had (`git log -S` over `docs/design` finds only
`14fdc60b` and `32f0eacd`), and only About draws it, so no other screenshot can show it. **Outside the archive, for
the owner's knowledge:** `masaha`'s own history named the university too (`8db442b2`, `b93c9e88`, removed in
`5cf983e6` «docs: remove the university and the defence»). The PR removes the screenshots from `masaha`'s tip, not
from its history.

## 6. Decisions, as they will be built

### 6.1 What moves: the whole `docs/design/` (P1, the supervisor's recommendation, kept)

One home for the design archive: the prototype, the screenshots and INDEX that map its frames, SCREENS and CHANGES
(its record), its scripts and BRIEF. **Nothing must stay.** The one judgment call is **the logo's source files**
(`prototype/masaha/logo/`, foundation §16 «the source files, the owner's»). They move: the prototype's pages draw
them (the tab icon in `i18n.js`), production carries its own derived forms (`Logo/drawing.ts`,
`apps/web/public/`), and a copy left in `masaha` would be a second home. foundation §16 links the folder's URL.
(Alternative in §12.)

`.design-sync/` stays: it belongs to the production design system.

### 6.2 How the history moves, and the proof

Phase 2, step by step (no other folder than `C:\dev\masaha\masaha-prototype`):

1. `git clone --no-checkout C:\dev\masaha\app C:\dev\masaha\masaha-prototype`, then `git config core.autocrlf false`
   in it (this machine's global `autocrlf=true` would check the files out as CRLF, which `masaha`'s `eol=lf` prevents).
2. `git subtree split --prefix=docs/design -b split` in the clone; record `S = split`'s sha.
   *Executor check:* if `subtree` refuses on a `--no-checkout` clone, check out `main` first.
3. **The proof:** `git rev-parse S^{tree}` must equal `c9183a63ff75e6e3138a455ad68f89424828afe9`
   (`git -C C:\dev\masaha\app rev-parse main:docs/design`); `git rev-list --count S` = 89; the oldest commit's
   message «docs(design): add the design archive» and the tip's author date equal `3b5d9e89`'s.
4. `git switch -C main S`; delete `origin`, every other branch and every tag; `git reflog expire --expire=now --all`;
   `git gc --prune=now`. Only the split history remains: `git count-objects -vH` and `git log --all` show it.
5. Recreate the tag `design-2026-09-29` on the split commit of `14fdc60b` (the oldest), annotated with the same
   message.
6. Run the scan on the new repository's own history (the same script, prefix-free) and compare the counts.
7. If R1 is approved (§6.3), redact now, before any commit of mine, then prove the difference.
8. The new repository's own commits (§10.1).

`git filter-repo --subdirectory-filter` would do the same but is not installed. `subtree` is built in, which is
why I picked it.

### 6.3 The scan's outcome: the identity hits (the owner decides; I recommend R1)

- **R1 (recommended): redact while splitting.** With `git filter-branch --index-filter` on the new repository only
  (built in, no install), map the one `About.html` blob (`93f287e5`) to the same text without line 99, and the five
  About screenshots to copies with that line painted over in the page's background. The painting uses Pillow in a
  throwaway virtual environment in the session scratchpad, so neither repository changes. Same dimensions, the
  rest of each image unchanged, and each one looked at before and after. Then
  `git diff --name-status <split tip> main` lists exactly those five WebP files (About.html differs only in history),
  `refs/original` is deleted, gc runs, and the scan is rerun on the rewritten history: zero hits for the
  university's name in text. The tip proof becomes «identical except these five files», stated in the PR's
  Evidence and the report. *Option R1b:* also reword CHANGES.md's U11 «The university line goes» to «The project line
  goes» in its 52 versions (the same filter, a text substitution). I lean to R1b, since the rule says "never write
  the university". But it only *refers* to it, so it is the owner's call.
- **R2: publish as split, byte-identical.** Defensible under P5 (the same files are public in `masaha` today), but it
  publishes a new copy that breaks P2's own words.
- **R3: drop the five screenshots** from every commit instead of painting them, and mark their INDEX rows. That
  changes INDEX in every version and loses five frames.

The owner's own first name as the sample admin, the `0599 123 456` example, and the sample spaces' names (§5) are
listed for the owner. I propose leaving them.

### 6.4 The new repository's own documents (P4, P6)

At the root (= today's `docs/design/`):

- **`README.md`** (rewritten from today's archive README, which it replaces):
  1. what it is: the clickable prototype and the design archive of Masaha, moved out of `masaha` on 2026-11-15
     with its history (link to ADR 0020 in `masaha`), the tag `design-2026-09-29`;
  2. what is here (today's table, paths unchanged, plus `decisions/` and `variants/`);
  3. how to run it (`python -m http.server <port> --directory prototype`, or `npx serve prototype`; `file://` does
     not work);
  4. how variants work (`<Page>.html?v=<name>`, the switcher, where a variant's files and its decision live, the
     registry);
  5. checking (`node scripts/check-parse.mjs`, `node scripts/check-classes.mjs`, what they cannot see: today's
     text, paths fixed);
  6. one scope for every script (today's text: no object rest, no top-level `name`; a variant replaces the page's
     inline script, so it may reuse its names);
  7. rules for implementing from it in `masaha` (today's four, linked to `masaha`'s documents by URL);
  8. known limits (today's three).
- **`CLAUDE.md`**, the workers' rules:
  - What this repository is, and that **`masaha` is the one home of product facts**, read-only from here
    (`--add-dir C:\dev\masaha\app`): scope and *Not in v1* (`docs/project/overview.md`), the glossary, the design
    system (`docs/frontend/design-system/foundation.md`), localisation, copy, ADRs. Each is cited by its path in
    `masaha` and its GitHub URL.
  - **The original page is never edited.** Every idea is a variant: `prototype/<Page>.html?v=<name>`, its code in
    `prototype/variants/<Page>/<name>.jsx` (optionally `<name>.css`), registered in `prototype/variants/index.js`.
    Promoting a chosen variant into the original is the owner's decision, recorded in the page's decision file.
  - The switcher lists the original and its variants; it is the owner's way to compare.
  - **The fixed points** (a variant never changes them): ink + berry and the logo
    ([ADR 0019](…), [foundation §16](…)); Arabic first and RTL, English LTR as the second; the v1 scope and
    *Not in v1* (no booking, no online payment, no QR, no reviews, no in-app claiming); **no fake data**: no ratings,
    no seat counts or capacity in public (ADR 0008), no invented figures; the product rules of BRIEF.md.
  - **What a variant may change freely:** layout, type scale and typeface (as a proposal), spacing, surfaces,
    imagery, motion. **Each change is stated in the page's decision file** as a proposal, since production's
    design system changes only through `masaha`'s own PR.
  - The two checks before each commit; the one-scope rules (object rest, top-level `name`).
  - How to run it.
  - Git: commits straight to `main` of this repository, Conventional Commits, subject ≤ 50 characters, a body, no
    tool attribution, staged by path; never edit `masaha` from here.
  - The identity rule: never the university, the supervisor or the defence.
- **`prototype/BRIEF.md`**, updated (the original stays in history and at the tag; README stops calling it a frozen
  record). It covers who the users are: the visitor, the owner, the receptionist, the admin (from today's roles).
  What is fixed is today's product rules and scope, kept. The line «No new colours, fonts, radii, shadows» becomes:
  «production's design system is the start; a variant may propose new type, spacing and surfaces, each stated in
  its decision file». The colours stay the identity's. Sample data is kept as it is.
- **`decisions/README.md`**: one file per page, `decisions/<Page>.md`, created with the page's first variant. Its
  template has the page; its variants (name, what each changes, each change as a proposal against the design system
  with its reason); the owner's choice, why, and the date; and once built, the `masaha` PR. No page file is created
  in this item.

### 6.5 The variant mechanism (P6, mechanism only)

In the prototype's existing style (a plain script read from the URL, like `i18n.js`'s `?identity=`):

- **`prototype/variants/index.js`**, the registry, a plain script: `window.MASAHA_VARIANTS = {}`, keyed by the page's
  file name without `.html` (`'Sign in': [{ name: 'calm', ar: '…', en: '…', css: false }]`). Empty in this item.
- **`prototype/masaha/variants.js`**, a plain script (one IIFE, no top-level name), loaded right after `i18n.js` and
  **before** `_vendor/babel.min.js`:
  - reads the page (`decodeURIComponent(location.pathname)`'s last part) and `?v=`;
  - when `?v=` names a registered variant: on **`document`**'s `DOMContentLoaded`, which runs before Babel's
    listener on `window`, it sets every inline `<script type="text/babel">` without `src` to `type="text/x-original"`
    (inert), and appends `<script type="text/babel" src="variants/<Page>/<name>.jsx">` (and the variant's
    stylesheet when `css: true`). Babel then compiles the shared modules and the variant instead of the page's own
    block. The variant starts as a copy of that block, so it may reuse its names;
  - an unknown `?v=` is the original, like an unknown `?identity=`;
  - `?v=` is carried by a link only to the same page (a variant's own states: `?v=calm&state=error`), by a capture
    listener of its own; `i18n.js` is untouched;
  - **the switcher:** a small native `<select>` labelled «النسخة» / "Version", fixed at the block-end, inline-end
    corner. It lists «الأصل» / "Original" and each variant by its label, and changing it reloads the page with `v`
    set or removed, the other parameters kept. It is drawn **only on a page with at least one variant** (or with
    `?v=`), never inside a frame (the board), and not with `?switcher=0` (screenshots). Its classes are the
    vendored bundle's, so `check-classes` verifies them.
- **Each of the 38 pages that load `i18n.js`**, and the five `masaha/_*head.txt` templates, gain the same two
  `<script>` lines after `i18n.js`. **This is the one edit to the original pages**, and it is the mechanism.
  `Flows - states.html`, `Reset email.html`, `Sign in - board.html` and `Wordmark.html` are left alone.
- **The checks:** `check-parse` also parses `variants/**/*.jsx`; `check-classes` also reads `variants/**/*.jsx` and
  `masaha/variants.js` as users and `variants/**/*.css` as stylesheets.

### 6.6 The removal PR in `masaha`

- Branch `chore/design-archive-out` from the latest `main`; **#147** expected (the last PR #146 and the last
  Issue #126; checked again before the push).
- **ADR 0020 — The design archive and the prototype live in their own repository** (short, decision-level, no file
  names, per the ADR style):
  - *Context:* the prototype became the living design. Each change cost a PR, the full CI and a production deploy,
    and a design worker worked inside the production repository. Page-by-page design with variants is next.
  - *Decision:* the archive and the prototype move, with their history, to a public repository of their own. The
    production repository stays the one home of product facts (scope, glossary, rules, copy, design system), which
    the prototype's workers read and never edit. The prototype holds only its own working documents. A design
    reaches production only as a Work Item here: the owner chooses a variant there, recorded with its reasons, and
    a Work Item builds it with the design system, carrying any change to the design system through this
    repository's documents.
  - *Alternatives:* a copy with the original frozen (two homes, editing twice); a submodule (cost, no gain);
    keep it here (the cost above).
  - *Consequences:* prototype work no longer runs CI or deploys; links to the design are URLs, which `check:links`
    does not check; the screenshots and history leave this repository's tip, but its history keeps them; an
    implementing Work Item reads two repositories.
- The pointers of §4.2; the map's entries; `CLAUDE.md`'s line.
- *Deferred documents:* the table's only row (*Endpoints*) is not met. No trigger.
- `#PRNUM`: none planned (the ADR carries no PR number). If one is added, it is replaced just before the push.

## 7. Related findings

- **215 (Open), the prototype's Home and today's line disagree with production.** Not folded. Its fix is a
  prototype change, now in the other repository, and this item designs nothing. It stays open in `masaha` (a
  divergence production's documents track), its two paths repointed. Cost of folding: a prototype edit outside the
  item's scope.
- **14, 19, 32, 73, 74, 96, 130**: resolved, accepted or open records whose links are repointed (§4.2); nothing
  else changes.
- **37**: its record names `NOT_SCANNED`'s old entry as of its date; left.
- **New finding (proposed, 228):** «`masaha`'s history still names the university». Its evidence would be the
  commits of §5 and the five screenshots in `14fdc60b`, the university not named; it *resolves when* the owner
  decides on a history rewrite or accepts it. Recording a finding is allowed; I add it only if the owner says so,
  since it puts the matter in a public document.

## 8. Files

**New repository** (`C:\dev\masaha\masaha-prototype`): `.gitattributes` (`* text=auto eol=lf`), `.editorconfig`
(today's root one), `README.md`, `CLAUDE.md`, `prototype/BRIEF.md`, `decisions/README.md`, `scripts/check-parse.mjs`,
`scripts/check-classes.mjs`, `CHANGES.md` and `SCREENS.md` (five links out), `prototype/masaha/variants.js`,
`prototype/variants/index.js`, 38 pages, 5 `_*head.txt`; with R1, the history of 1 blob and 5 images.

**`masaha`, PR #147** (25 edited, 1 added, 560 deleted):
`docs/architecture/decisions/0020-design-archive-own-repository.md` (new); `docs/README.md`; `CLAUDE.md`;
`docs/frontend/design-system/foundation.md`; `docs/features/auth.md`; `docs/features/directory.md`;
`docs/plans/v1-mvp.md`; `docs/plans/foundation.md`; findings 14, 19, 32, 73, 74, 96, 130, 215;
`.prettierignore`; `eslint.config.js`; `.coderabbit.yaml`; `apps/api/scripts/checkLinks.ts`;
`apps/web/src/shared/design-system/components/display/Logo/drawing.ts`; `apps/api/src/modules/auth/email/resetEmail.ts`;
`apps/api/src/modules/auth/email/resetEmail.copy.ts`; `docs/design/**` (deleted). (+1 finding if approved.)

No other open item: no file is shared. **Review:** more than 25 files, and it changes a build check
(`checkLinks.ts`, the ESLint config), so a separate review conversation (workflow §2, phase 7).

## 9. Tests, and the *Review Focus*

No behaviour of `masaha` changes, and no test is added. `NOT_SCANNED` is a constant read by `main()`, which
`checkLinks.unit.test.ts` does not run: the proof that dropping the entry breaks nothing is `npm run check:links`
itself, green with the archive gone. In the new repository the checks are its two scripts and a served run (§11.1).
No test lane exists there, by P4.

*Review Focus* (inputs nothing exercises):
- every repointed URL: `check:links` skips external links, so I check each distinct URL by hand (`curl -I`, 200),
  once the repository is public;
- the GitHub anchors of SCREENS.md (`#owner-and-reception-dashboard-13` …) as GitHub renders them;
- the variant mechanism with a real variant: the swap of the inline block, the `?v=` carry, the switcher in RTL and
  LTR, light and dark, phone and desktop; an unknown `?v=`; a page with two inline blocks;
- the redacted images (if R1), looked at, not measured.

## 10. Commits

### 10.1 `masaha-prototype` (straight to its `main`, P4)

1. The 89 split commits (rewritten only by R1/R1b), and the tag `design-2026-09-29`.
2. `chore: stand alone at the repository's root`: `.gitattributes`, `.editorconfig`, the Babel load and usage
   lines of both scripts, the five links out of CHANGES.md and SCREENS.md.
3. `feat: add page variants and their switcher`: `variants.js`, `variants/index.js`, the 38 pages and 5 templates,
   both checks extended.
4. `docs: add the README and the workers' rules`: README.md rewritten, CLAUDE.md.
5. `docs: update the brief and add decisions`: BRIEF.md, `decisions/README.md`.

### 10.2 `masaha`, PR #147

1. `docs(adr): record the design archive's own repo`: ADR 0020 and its line in the map's ADR list.
2. `docs: point the design links to masaha-prototype`: every document and code comment of §4.2, the map's
   design section and CLAUDE.md's line. The links already resolve, since the repository is public by then.
3. `chore: remove the design archive`: `docs/design/` deleted, with the four exclusions that existed for it.
4. *(if approved)* `docs(findings): record the history's university line`: finding 228 and its index line.

Every subject ≤ 50 characters, a body with the why, no attribution, staged by path.

## 11. Verification

### 11.1 The new repository
The proof of §6.2 (and R1's diff); `git status` clean and `git ls-files --eol` all `lf` for text; both checks at
the new root (baseline counts, then with the mechanism). One served run:
`python -m http.server <free port> --directory C:\dev\masaha\masaha-prototype\prototype`. In it, `Sign in.html` with
no `?v=`: unchanged, no switcher. Then, with a **temporary, uncommitted** variant: a registry entry and a copy of
Sign in's inline block with its title changed. `?v=<it>` shows the variant and the switcher, in Arabic and in
`?lang=en`, light and dark. An unknown `?v=` shows the original. The temporary files are removed (`git status`
clean). The server is stopped by PID and the port checked free. If the session refuses to start a server, I say so
and go on. Then `gh repo create Basel-Ghonaim/masaha-prototype --public --source C:\dev\masaha\masaha-prototype
--push`, only once the scan's outcome is approved. Then `gh repo view`, `git ls-remote` (main and the tag), and each
URL of §4.2 answering 200.

### 11.2 The PR (each heavy command through `heavy.mjs split …`, one at a time)
`npm run lint`, `typecheck`, `format:check`, `check:links`, `check:conflicts`, `check:classes`; `build` with
`NODE_ENV=production`, then `check:build`. The test lanes: `checkLinks.ts` changes beyond a comment, so by the
prompt's rule I run **all three**: `test:unit`, `test:component`, and `test:api` with the database up. A lane killed
for memory is retried once, then CI judges. `git grep -n -E "docs/design|\.\./design/"` outside records' prose is
empty. Then push, open with `open-pr` (Evidence: the tree proof, the scan summary, the URL), and wait for
`gh pr checks 147` all green on the pushed head and `CLEAN`. Then the report (`4_REPORT.md`). Never merge.

## 12. Risks and rollback

- **The PR is reverted while the new repository stays:** `git revert` of the three commits restores
  `docs/design/` byte for byte (the tree proof). The prototype then has two homes until one is removed again. The
  owner chooses which.
- **The new repository is wrong** (a bad split, a missed hit): until the PR merges, `masaha` still holds everything.
  The repository is deleted (`gh repo delete`, the owner's) and redone. After publication, its content was public
  anyway (P5), except for what R1 removed.
- **R1 rewrites the new history only.** `masaha` keeps the original commits, so the new repository's commit ids
  differ from a plain split. The tag is recreated on the rewritten commit.
- **External links rot quietly** (`check:links` skips them): one host, one path layout. Renaming a file in the
  prototype breaks a `masaha` link silently. CLAUDE.md there says: never rename or move a file `masaha` cites
  without a PR here that repoints it.
- **Line endings:** the global `autocrlf=true` with no `.gitattributes` would leave the new working tree
  CRLF. The clone sets `autocrlf=false` first, and commit 2 adds `.gitattributes`.
- **The design workers' folder `app-design`** keeps an old `docs/design` copy. After the merge it is obsolete. Its
  cleanup is the owner's.

## 13. Decisions needed from the owner

1. **The identity hits (§6.3): R1, R1b (my recommendation), R2 or R3.** Nothing is published before this answer.
2. **The rest of the scan:** leave the owner's first name as the sample admin, `0599 123 456`, and the sample spaces'
   names (recommended: leave)?
3. **Finding 228** about `masaha`'s own history: record it (recommended, it records without fixing), or not?
4. **The switcher on a page with no variant:** hidden (recommended; 38 pages and every screenshot stay as they are),
   or always shown with «الأصل» alone (P6's words read literally)?

## 14. Proposed alternatives

- **Pin the records' links to a commit.** The prompt repoints to `blob/main/<path>`. For the **findings** (records of
  what was found at a date), a permalink to the split tip's commit (`blob/<sha>/<path>`) keeps the evidence as it was,
  even after the prototype changes. Active documents keep `main`. Cost: none beyond the sha. My recommendation: take
  it. Otherwise I follow the prompt.
- **Keep the logo's source files in `masaha`** (for example `docs/assets/logo/`) as the brand's home, and let the
  prototype copy them. Rejected by me: two homes, and the prototype draws them. Listed because foundation §16 calls
  them the owner's source files.
- **No other disagreement** with P1–P6.
