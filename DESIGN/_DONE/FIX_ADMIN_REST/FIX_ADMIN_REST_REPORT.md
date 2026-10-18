# Design fix 2b: the rest of the admin's dashboard (report)

Worker: the design-fix worker. Worktree `C:\Users\basel\masaha-design`, branch `design/admin-rest`, cut from
`origin/main` `068efc6`. Plan: `PLAN\FIX_ADMIN_REST_PLAN.md`, approved by `PROMPT\FIX_ADMIN_REST_PLAN_REPLY.md`.
Subagents used: 0 of 2.

## 1. The pull request and its head

**#66** · `design: the rest of the admin's dashboard` · https://github.com/Basel-Ghonaim/masaha/pull/66

- Head: `15039cb2f315b02607f7b273cb8321cbd2459853`.
- Labels `docs` and `area:docs`; assigned to the owner. Not merged.
- CI is green on that head (lint, typecheck, build, check:classes, check:links, format:check, test:unit,
  test:component, test:api), and GitHub shows **CLEAN**.

## 2. The commits

There are ten commits, one per decision, as the reply allowed. Each subject was counted before its commit.
The branch touches 15 files, all under `docs/design/`.

| # | SHA | Subject (chars) | Holds |
|---|---|---|---|
| 1 | `1698915` | `docs(design): a space's own amenities` (37) | G1, `?demo=ownlimit`, the *Batch 2b* heading |
| 2 | `0d483e2` | `docs(design): amenities are no filter` (37) | G2, the board's label |
| 3 | `9ef2eb6` | `docs(design): a space's state is two facts` (42) | G3, Olive Desk, `?status=` |
| 4 | `0aae6f7` | `docs(design): one way to link an owner` (38) | A4, A6, `LinkOwnerDialog`, both `?unlink=`, `?q=` on owners, `?fail=link`, INDEX and board |
| 5 | `2b93355` | `docs(design): say what an act does, before it` (45) | A5, AD-021: add owner, password dialog, role, suspension, temporary password, `?fail=role`, منى |
| 6 | `7b7c12d` | `docs(design): the admin's lists at 768` (38) | A7, `AdminList`, the filters, the stale chip, `?space=`, `?field=` |
| 7 | `2749c03` | `docs(design): the overview is a work queue` (42) | A8, the reply rule, `?report=`, DI-21, DI-22 |
| 8 | `ff67c2f` | `docs(design): the lookups say what moved` (40) | AD-024…027, P8's exception, the icons (S10) |
| 9 | `b914820` | `docs(design): the audit log leads somewhere` (43) | AD-028 as amended, DI-25 |
| 10 | `15039cb` | `docs(design): settings: one width, one name` (43) | AD-029 as narrowed |

## 3. What was run, and what was not

| Check | Result |
|---|---|
| `node docs/design/scripts/check-parse.mjs` | 49/49 blocks (40 pages and the modules), before every commit |
| `node docs/design/scripts/check-classes.mjs` | 0 new dead classes, 8 known uses, before every commit |
| **Full browser matrix** (headless Chrome, scratchpad) | 28 targets × 390/768/1440 × ar/en × light/dark = **336 loads, 0 problems** |
| Quick passes (390 and 1440, Arabic light) | on each commit's pages before it was made: 24, 132 (full), 16, 30, 14, 6, 2, 2 loads, all clean |
| `npm run format:check` | passes. It cannot see this item: `.prettierignore` excludes `docs/design/` and `*.md` |
| `npm run check:links` | 1921 links in 109 documents and 997 source files resolve |
| CI on `15039cb` | every job green |

**What every matrix load checks:**
- no blank render and no console error;
- no horizontal overflow;
- no control cut off past the viewport;
- no `h2` drawn twice.

**What each target adds** (`targets.py` in the scratchpad):

| Area | Assertions |
|---|---|
| G1 | F1's 20 px gap on both editors; the own-amenities section; «إضافة مرفق إضافي» disabled at 20; the owner's page inherits it without the admin's link |
| G2 | no filter text on the amenities tab |
| G3 | Olive Desk absent from «كل الحالات» and present, with «استرجاع», under «محذوفة» |
| G4 | the link Combobox from both ends; `?unlink=o3&space=numberone` names Yousef; the password dialog has no close button and «تم» waits; `?email=` shows «ترقية وربط»; the role is an `AlertDialog`; `?temp=1` names Omar |
| G5 · lists | cards until 1024 for Spaces, Users and Reports, a table from 768 for Owners and the Audit log; `?space=focus` lists Focus Hub only; the stale chip is pressed under `?stale=1` |
| G5 · overview and editor | no destructive badge and no pin badge; four tiles that lead somewhere; the report alert right above `#prices` |
| G5 · lookups | a panel for every tab; every arrow carries «من N»; the live region exists; no switch in the sheet; the position field |
| G5 · audit and settings | targets are links; red only for P9's three; no actor filter with one actor; «إعدادات المنصة» and `max-w-3xl` |

**By eye:**
- every changed page at 390, 768 and 1440, Arabic, with English and dark samples;
- every dialog and sheet I added, opened.

**Images:** 51 before/after pairs and 18 new "after" frames are in `Downloads\design-fix-admin-rest\`. They are
not committed.

**Not run:** the test lanes, `build`, `check:build`, lint and typecheck locally. There is no product code (workflow
phase 4's exception), and `docs/design/` is ignored by ESLint. CI ran them anyway.

## 4. The breaks made, and the checks seen failing first

Nine deliberate breaks were made in the working tree, one at a time, each against its targets. The tree was
restored from git after each, and `git status` was clean at the end. **All nine were caught:**

1. the password dialog gets its X back;
2. `AdminList` draws cards only below 768;
3. the lookups' arrows lose their position;
4. hiding is painted red again;
5. the own-amenity limit is off by one (21);
6. missing is painted red again on the overview;
7. the report alert sits after its section;
8. a deleted space is back in «كل الحالات»;
9. suspended accounts are offered for linking (checked with a Combobox probe for Rima).

## 5. Problems met, and how each was solved

| Problem | Solved by |
|---|---|
| Long Python heredocs failed to parse in Git Bash (twice), as my notes warned | The scripts went to scratchpad files (`splice.py`, `c5_…`, `c6_…`, `c7_…`) |
| The new owner in Olive Desk's area showed «الشيخ رضوان»: `AD.areaName` read the public catalogue, which holds only Gaza City's areas, and fell back to a fixed name | `AD.areaName` now reads the admin's full catalogue (`lookups.govs`) |
| `underline` was a dead class (not in the prebuilt CSS) on the «اربطه بالمساحة» button | It became a plain link to `Admin owners.html?link=<id>`, styled like every link |
| A headless Chrome orphaned by a `timeout` kept its debugging port, so the next run could not start | Each run takes a random port, and only my `cdp-` profiles were stopped, by PID |
| The matrix reported a BLANK when a URL differed from the previous load only by its hash: that is a same-document navigation | The matrix passes through `about:blank` before each load |
| `Alert` has no `success` variant: the resolved report notice crashed the editor | It uses `info`, with the resolved wording |
| A `Select` import doubled on the audit page (a parse error) | Caught by `check-parse.mjs` before the commit and removed |

## 6. Anything that behaved unexpectedly

- **The archive's `ActionButton` breaks on a page that loads `profile-a.jsx` after `shared.jsx`.**
  - *Cause:* in-browser Babel compiles each script on its own and puts its helper list `_excluded` at the top level
    of each one. `profile-a.jsx`'s list (its `ClockInput`, the only rest destructuring in a module the editor
    loads) overwrites `shared.jsx`'s, so `ActionButton`'s rest props keep `actionKey`
    and `onAction`, and React warns.
  - *Why it never showed:* no page used `ActionButton` with those modules loaded until the report alert in the
    editor.
  - *What I did:* the alert uses `useActionRun` and a plain `Button`, with a comment saying why. The cause is left
    as it is and recorded below (DI-27).
- **A top-level `const name` breaks a page.** Babel's `var` makes it `window.name`, which the browser always keeps a
  string, so the lookups page went blank («name is not a function»). It is now `lname`, with a comment.
- **The `#report` anchor never scrolled.** The page renders after the browser looked for the anchor. The alert now
  brings itself into view on mount.
- **The disabled menu items' reasons render at the field's 50 % opacity** (foundation §5). They are readable but
  faint. I kept them, matching a disabled `Field`'s helper (DI-28).
- **The section chips mark «ساعات العمل» while the report alert is in view above the prices**, because the alert is
  no section. Minor, and left.

## 7. The early conflict check

`git merge-tree --write-tree 15039cb <head>`:

| PR | Head | Result |
|---|---|---|
| **#65** `design: the public site` (`design/public`) | `51685d0` | **Conflict in `docs/design/CHANGES.md` only.** Both items append their batch's section at the end of the file. The resolution is to keep both sections, in merge order. `INDEX.md` and `Flows - states.html` merge on their own |
| **#64** `feat(spaces): own amenities, no amenity filter` | `2e4aa4d` | clean |

## 8. Departures from the prompt and the plan

- **`ActionButton` → `useActionRun` in the report alert.** The plan did not name the component; the reason is
  §6's collision.
- **The resolved report alert is `info`, not a success colour.** The bundle's `Alert` has no `success`.
- **«يعدّلها أحمد» on the verified page now lands on that owner** (`Admin owners.html?q=<email>`) rather than the
  whole list. This is a small change inside A6/S15.
- **`?fail=link` landed in commit 4** with the dialog, not in commit 5 as the plan's table placed it.
- **The spaces list's three filter fields sit on one row from 768** (`md:grid-cols-3`). Once A7 made the switch a
  chip, the old four-column grid left one field alone on a second row.
- **Audit sample truths, beyond DI-25:**
  - a role change «مالك ← مستخدم» by hand, which the API refuses, became «أدمن ← مستخدم»;
  - Yousef's «مستخدم ← مالك» is now dated with his link and says it came «بربطه بمساحة»;
  - the log is shown in time order.
- **The audit log's fill repeats «ندى سكيك ← ZM Hub · أصبحت المساحة موثّقة»** while ZM Hub is unverified. This
  sample noise predates the item and was left (see DI-29).

## 9. New design issues (none built)

- **DI-23 · the layer's `DataTable` has no card breakpoint** *(design system; recorded as the reply asks, for
  worker A)*.
  - *Problem:* A7's "cards until 1024" for Spaces, Users and Data reports cannot be built with it.
  - *Better:* a `cards` prop (`md` by default, `lg` for these lists). The prototype imitates it with `AdminList`,
    which copies the `DataTable`'s own card markup.
- **DI-24 · `AdminUserRow` carries owner links only** *(API + prototype; recorded as the reply asks, for step 6)*.
  - *Problem:* a person's reception link is invisible, so a role change (`ACCOUNT_HAS_LINKS`) or a link
    (`RECEPTION_LINK_ACTIVE`) can only be refused after the act.
  - *Better:* the row gains the reception links, and the items are disabled first with their reason. Until then
    the prototype shows the refusals (`?fail=role`, `?fail=link`).
- **DI-26 · «بيانات قديمة فقط» keeps the missing groups too** *(prototype and web)*.
  - *Problem:* the chip's words say "stale only", but it keeps stale **or** missing, as the contract's
    `stale=true` does. The overview's tile already says «بيانات قديمة أو ناقصة».
  - *Better:* the chip reads «قديمة أو ناقصة», so one filter has one name on both pages. The label is A7's settled
    words, so this is for the analyst.
- **DI-27 · the archive's Babel helpers collide across scripts** *(prototype)*.
  - *Problem:* `ActionButton` (and any rest-destructuring component in `shared.jsx`) misbehaves on a page that
    loads `profile-a.jsx` after it. *Corrected at the review:* `map.jsx` has no rest destructuring and does not
    collide; only `profile-a.jsx`'s `ClockInput` does, plus two inline page scripts on pages without `ActionButton`.
  - *Better:* `shared.jsx` picks its props explicitly instead of a rest spread. Or the archive compiles each
    module inside its own function scope. This is one small change in `shared.jsx`, the shared layer's file,
    outside this item.
- **DI-28 · a disabled menu item's reason is drawn at 50 %** *(design system)*.
  - *Problem:* foundation §5 dims a disabled control with its helper. In a menu the reason is the only thing the
    admin reads there, and at 50 % it is faint.
  - *Better:* the layer's `DropdownMenuItem` takes a `description` drawn at full muted colour while the item is
    disabled.
- **DI-29 · the audit log's generated fill contradicts the sample's state** *(prototype)*.
  - *Problem:* «ندى سكيك ← ZM Hub · أصبحت المساحة موثّقة» repeats on many days, but ZM Hub is unverified (2b adds
    her unlink on 22 September, older than some of those lines).
  - *Better:* the fill's link line names a pair that stays linked (Ahmad → Focus Hub).

## 10. Owner's additions

None were asked for while the work ran.

## 11. Review focus: what no check exercises

- A screen reader on the Combobox options, the disabled items' reasons, the lookups' live region, and the password
  dialog's trapped focus. Also real keyboard focus (`:focus-visible` does not fire under scripted focus).
- Touch on a `Combobox` inside a `Dialog` on a phone: scrolling and the on-screen keyboard.
- The six inline lucide icons against the web's `GlyphIcon`, by eye.
- The handover's own failure after «تم» (`TEMPORARY_PASSWORD_NOT_PENDING`): not drawn.
- Whether the muted «محذوفة» rows read as muted enough in dark mode.

## 12. Review fixes (2026-10-12)

From the analyst's conformance review of `15039cb` (`PROMPT\FIX_ADMIN_REST_FIXES.md`).

### 12.1 The pull request and its head

**#66**, new head **`4a1260d5453efd424290c7dfa6e2c6e166491667`**. CI is green on it (every job), and GitHub
shows **CLEAN**. One "Review fixes" comment is posted on the PR. Not merged.

### 12.2 The commits, and the fixes in each

Every fix is folded into the commit of its decision: `git commit --fixup`, then
`GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash 068efc6`, onto the branch's own base. There are still ten
commits. `git diff 15039cb 4a1260d` shows exactly the fixes. `git range-diff` shows commits 1–3 unchanged and
commits 4–10 carrying only the folded lines.

| # | New SHA | Subject | Folded fixes |
|---|---|---|---|
| 1–3 | `1698915` `0d483e2` `9ef2eb6` | unchanged | — |
| 4 | `e6ac8b0` | one way to link an owner | the unlink titles' «؟» through `tr()`, on both pages |
| 5 | `483ca76` | say what an act does, before it | **R2** (`?link=` opens only for an active owner); «اربطه بالمساحة» carries `&space=` and `LinkOwnerDialog`'s `preset` chooses it; its `INDEX.md` row |
| 6 | `75d8a59` | the admin's lists at 768 | `?space=` is read only from the spaces the field offers |
| 7 | `058a8c2` | the overview is a work queue | **DI-26**: the chip reads «قديمة أو ناقصة», the board's frames and `INDEX.md` say "Stale or missing", and the A7/A8 lines follow. Also the report alert's punctuation through `tr()`, and the queue counting fact groups only |
| 8 | `663f6e4` | the lookups say what moved | **R3** (one `place()` rule in every list's save); **R1** (G2's line now reads "in the line above each panel") |
| 9 | `80747f0` | the audit log leads somewhere | **DI-29** (the fill's link line names Ahmad → Focus Hub) |
| 10 | `4a1260d` | settings: one width, one name | the settings line: two cards shared the error object, not three |

### 12.3 What was run

| Check | Result |
|---|---|
| `check-parse.mjs` and `check-classes.mjs` | pass at **every** rewritten commit (49/49 blocks; 0 new dead classes) |
| Full browser matrix | 33 targets × 390/768/1440 × ar/en × light/dark = **396 loads, 0 problems** |
| After moving the report target off its hash (§12.6) | that target alone: **24 loads, 0 problems**, now really in English |
| `npm run format:check` | passes (it cannot see `docs/design/`) |
| `npm run check:links` | 1921 links in 109 documents and 997 source files resolve |
| CI on `4a1260d` | every job green |

**The new targets** (five new, one changed):
- `?link=o4` opens no dialog;
- `?link=o1&space=golden` has Golden Hub chosen;
- `?space=olive` lists all six reports;
- the English unlink title has no Arabic punctuation;
- the English report alert has no Arabic punctuation;
- the stale chip's words now say "missing" (the changed target).

**By eye, at 390 and 1440,** each fixed part:
- the English unlink title;
- the chip;
- the carried space;
- the overview;
- a far move in Gaza City («الترتيب» 1 → «الشجاعية: 1 من 11», and the row first).

**Not run:** the test lanes, build, lint and typecheck locally. There is still no product code; CI ran them.

### 12.4 Breaks, and checks seen failing first

Six deliberate breaks, each undoing one fix in the working tree, were run against their targets. The tree was
restored after each and was clean at the end. **All six were caught:**
1. R2 undone;
2. the carried space ignored;
3. `?space=` read from deleted spaces;
4. the unlink title back to «؟»;
5. the report alert back to «،»;
6. the chip back to «بيانات قديمة فقط».

The report alert's break was **missed at first**: see §12.6. It was caught once its target moved off the hash.
The nine breaks of §4 still stand for the rest.

### 12.5 Problems met

- **The autosquash conflicted wherever a fix touched a line beside one a later commit rewrote.**
  - **R2's line** sits above the add-owner state lines that commit 5 rewrote. I resolved it to commit 4's own
    text, then folded R2 into commit 5 and autosquashed a second time.
  - **Each `CHANGES.md` fix to the last row of its commit** conflicted with the next commit's appended row. A
    scratchpad resolver kept each commit's own rows, in the fixup's wording, and appended each later commit's new
    row (six conflicts).
  - After both passes, the tree was **identical** to the pre-rebase fixups' tree (`git diff` empty).
- **R1 lives in commit 8, not 2.** G2's row became untrue when commit 8 removed the sheet's helper and the toast.
  A fix in commit 2 would also have conflicted with every later append.
- **One break script's quoting** collapsed a string; I fixed it before it changed anything (the tree stayed
  clean).

### 12.6 Unexpected

- **The matrix never ran the editor's report target in English.**
  - *Cause:* it appends `&lang=en` and `&theme=dark` after the URL, and that target's URL ended in `#report`, so
    the parameters went into the hash. Its "English" and "dark" loads ran Arabic light, and passed vacuously
    (in §3's 336 loads and §12.3's 396).
  - *How it showed:* the report alert's punctuation break went uncaught.
  - *Fixed:* the target dropped its hash, the break was caught, and the target passes in real English and dark (24
    loads). No other target used a hash.
- **`main` moved during the round** (#64 merged, `ae3bb05`). It merges clean with this branch, so there was no
  rebase on main; GitHub shows CLEAN.

### 12.7 The early conflict check

| PR | Head | Result |
|---|---|---|
| **#65** `design/public` | `1f3fb91` | **conflict in `docs/design/CHANGES.md` only**: both batches' sections sit at the end. The fast path is to keep both |
| **#67** `feat/admin-deleted-spaces` | `8a0bbc8` | clean |
| **#68** `refactor/web-storage-titles` | `9cb6382` | clean |

### 12.8 Departures, including the ones the review named

- **«تعديل الحقل» lands on `#report`, not on `#<section>`.**
  - The report's alert sits right above its section and brings itself into view, so the admin reads the report
    with the field directly below it.
  - A section anchor would scroll the alert out of view.
- **The role dialog's action is `destructive` for «جعله أدمن» too**, though the plan marked only the demotion.
  - P9 makes the action of every confirmation felt by others `destructive`, repeating the verb.
  - Granting the whole platform is the strongest grant the admin can make, and AD-020 asks that it be confirmed
    like the least. Kept.
- **The settings line said three cards shared one error object; two did.** The contact and freshness cards check
  their fields; the defaults card checks none. Corrected in `CHANGES.md`.
- **R1's and DI-26's `CHANGES.md` wording is folded where each became true or untrue** (commits 8 and 7), not
  into the rows' first commits (2 and 6). This keeps the history replayable (§12.5).
- **DI-27's root fix goes to #65**, as the owner decided. My workaround in the editor's report alert stays, and
  DI-27 is corrected above: only `profile-a.jsx` collides, not `map.jsx`.
