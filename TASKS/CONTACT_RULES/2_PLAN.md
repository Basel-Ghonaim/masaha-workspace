# CONTACT_RULES — the plan (for a free executor: OpenCode or Codex)

> Planner: Claude Code (Opus 5.5), read-only, from `C:\dev\masaha\app-design` detached at `main` `f073decb`
> (2026-11-15). Nothing in either repository was written; the only file written is this plan.
> Decisions: `0_OWNER_DECISIONS.md` C1–C9. Where this plan departs from a rule, it says so (§0.3).

**How to read this plan.** Do the steps in order. Every command is for **Windows PowerShell 5.1** (no `&&`: use
`;`, and `if ($?) { … }` to run a command only after a success). Every command starts in
`C:\dev\masaha\app-cr` unless it says otherwise: begin each one with `Set-Location C:\dev\masaha\app-cr;`. If
PowerShell refuses `npm` or `npx` (execution policy), use `npm.cmd` and `npx.cmd`. **`$H`** below means the grant
script: begin the command with `$H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs';` and then run
`node $H cr <command…>`. The grant script waits for memory and exits **75** when it gives up: then stop and report.
When the plan shows code, copy it exactly; Arabic and Persian digits in it are real characters, never escapes.

---

## 0. The contract

### 0.1 Scope

1. **C1 + C2 — phones.** Every phone (a contact's WhatsApp or phone, a «وسيلة أخرى» number, a customer's phone, the
   platform's WhatsApp) reads Arabic-Indic (`٠–٩`) and Eastern (`۰–۹`) digits as Western ones, before the rule reads
   them. The one reader, `toWesternDigits`, moves from the web's `shared/lib` to `@masaha/shared/core`, so the browser
   and the server read the same digits. The forms `+970`, `+972`, `00970`, `00972` and the local `0…` stay; each is
   already proven by `phone.unit.test.ts`.
2. **C3 + C4 — links.** A link's host must be a domain with a top-level domain (never an IP address, `localhost`, a
   bare word or a bare number). A Facebook link must name a page or a profile (a username, `/profile.php?id=<digits>`,
   `/people/<name>/<id>`). The Sheet already checks with the shared rule in the browser; new tests prove a refused
   value is said on its row and **no request is sent**, and that the server refuses it too.
3. **C5 — the row's ghost control.** Inside a table row, a `ghost` button hovers, and marks its open menu, with
   `hover-on-muted` over the row's `hover`, in both themes. One class string in `Button.tsx`.
4. **C6 — tests only.** The component lane's shared setup waits out a toast's removal timer before a file's jsdom is
   torn down (finding 219); the four site test files warm their lazy routes (finding 225).
5. **Documents** for each unit, and the five findings resolved.

### 0.2 Acceptance criteria

- [ ] `٠٥٩٩١٢٣٤٥٦` and `۰۵۹۹۱۲۳۴۵۶` are stored `+970599123456` (unit); the contacts' Sheet sends `+970599777888` for
      `٠٥٩٩٧٧٧٨٨٨`; the desk's edit dialog sends `+970599000304` for `٠٥٩٩٠٠٠٣٠٤`; the contacts' API stores
      `+970599123456` for `٠٥٩٩١٢٣٤٥٦`.
- [ ] A website `123`, `599123456`, `http://10.0.0.1`, `localhost`, `example` is refused; a Facebook `/watch`, video,
      reel, post, group, event, photo, share, search link is refused; a page, `profile.php?id=` and `/people/<name>/<id>`
      are stored.
- [ ] The Sheet says `http://10.0.0.1` and `facebook.com/watch?v=1` on their rows and sends nothing; the API answers
      `422` `invalid_format` for them and writes nothing.
- [ ] A ghost button carries the two row classes; the token test proves `hover-on-muted` is seen over `hover` and
      `foreground` reads over it, in both themes; captures at 1440, light and dark.
- [ ] No toast timer outlives a test file; the four site files warm their routes.
- [ ] The data count (§7) is reported; no data is changed.
- [ ] Every check of §12.1 green locally, then in CI on the pushed head, and GitHub shows `CLEAN`.

### 0.3 Out of scope, and the stated departures

- Out of scope: a schema, a migration, a dependency or a data change; any copy change; finding 103's record; the
  customers' search by partial Arabic digits (§13, *Observations*); any file of C7's list before PROTOTYPE_SPLIT's PR
  merges.
- **Departure 1 (stated):** the worktree is cut with `--no-track` (workflow §9: a plain `git push` can never target
  `main`). The prompt's command lacked it.
- **Departure 2 (stated):** each unit's documents go in its own commit (workflow §3); the **fifth commit** holds only
  what C7 makes wait for PROTOTYPE_SPLIT's merge: the five findings' status, the findings index (which must change
  in the same commit as a status, per the findings README) and `foundation.md`'s lines on C5 (that PR edits
  `foundation.md`). So C5's foundation lines are not in C5's commit.
- **Departure 3 (stated):** the prompt names `apps/api/scripts/checkClasses*`; the script is
  `apps/web/scripts/checkClasses.ts`.
- **Departure 4 (stated, a decision taken here — the owner may reverse it before the launch):** `toWesternDigits`
  moves to `packages/shared/src/core/digits.ts`. *Why:* the server must read the digits too (C4: the server enforces
  the same rule), `packages/shared` cannot import the web, and a second copy would be a second home for one rule.

---

## 1. Hard limits for the executor (copied from the prompt; they beat everything below)

1. Touch only the files this plan names (§11 lists them all). **Never** a file of C7's list:
   `docs/design/**`, `CLAUDE.md`, `docs/README.md`, `.prettierignore`, `eslint.config.js`,
   `apps/api/scripts/checkLinks.ts`, `apps/web/src/shared/design-system/components/display/Logo/drawing.ts`,
   `docs/frontend/design-system/foundation.md` and `docs/architecture/findings/README.md` (these two only in commit 5,
   §10.3, after PROTOTYPE_SPLIT's merge), `docs/features/{directory,finance,visits,payments,audit}.md`, findings 14, 19, 37,
   73, 74, 96, 110, 165, 215. Once PROTOTYPE_SPLIT's PR is open, its file list (§10.1) is added to this list.
2. **Never run a command in `C:\dev\masaha\app`**, never read its working files (C9). You launch from
   `C:\dev\masaha\app-design` and work only in `C:\dev\masaha\app-cr`.
3. Stage by path only: never `git add -A`, `git add .` or `git commit -a`. Run `git status` before each commit.
4. No schema, migration, dependency or data change. `package-lock.json` must not change.
5. Never weaken a test: never delete an assertion, raise a timeout or skip a test to make it pass.
6. No production code that only tests use.
7. No tool attribution anywhere: no `Co-Authored-By`, no "Generated with", in commits, the PR or files.
8. Never push to `main`; never merge; never create an Issue; never `--force` (only `--force-with-lease`, your branch
   only).
9. Never print, copy into a file or commit the contents of a `.env` beyond the lines §2.3 names.
10. When this plan does not cover what you meet, or a check fails twice, **stop and write it in `4_REPORT.md`**
    rather than improvise. A run killed for memory (exit 137, a signal, `heap out of memory`, `ENOMEM`, a worker
    that exited unexpectedly): retry it **once**; killed again, stop and report. **Never push anything red or untested.**
11. Watch your context: past 75 %, finish the step you are in, write
    `C:\dev\masaha\workspace\TASKS\CONTACT_RULES\4_HANDOFF_STATE.md` (branch, local head, pushed head if any, the
    step reached, what passed, the breaks log so far) and stop.

---

## 2. Setup (step 1)

### 2.1 Machine and repository

```powershell
node -v                                   # must print v24.x; otherwise stop and report
git -C C:\dev\masaha\app-design fetch origin
git -C C:\dev\masaha\app-design branch --list fix/contact-rules
git -C C:\dev\masaha\app-design ls-remote --heads origin fix/contact-rules
Test-Path C:\dev\masaha\app-cr
```

The last three must print nothing, nothing and `False`. Otherwise stop and report (an earlier run exists).

```powershell
git -C C:\dev\masaha\app-design worktree add --no-track -b fix/contact-rules C:\dev\masaha\app-cr origin/main
git -C C:\dev\masaha\app-cr log --oneline -1
git -C C:\dev\masaha\app-cr status
```

Note the head's SHA in your breaks log (`origin/main` at the cut).

### 2.2 Docker and the databases

```powershell
docker info --format '{{.ServerVersion}}'
```

If it fails: `Start-Process 'C:\Program Files\Docker\Docker\Docker Desktop.exe'`, then repeat `docker info …` every
15 s, at most 20 times; still failing, stop and report. Then:

```powershell
docker start masaha-postgres-1
docker inspect -f '{{.State.Health.Status}}' masaha-postgres-1      # repeat every 5 s until "healthy", at most 24 times
docker exec masaha-postgres-1 psql -U masaha -d postgres -tAc "SELECT datname FROM pg_database WHERE datname LIKE 'masaha_cr_%'"
```

If the last prints `masaha_cr_dev` or `masaha_cr_test`, skip creating that one (never drop it). Create the missing:

```powershell
docker exec masaha-postgres-1 psql -U masaha -d postgres -c "CREATE DATABASE masaha_cr_dev TEMPLATE masaha_dev"
```

If it fails with `source database "masaha_dev" is being accessed by other users`, never stop another session; copy
it instead (reads `masaha_dev`, writes only the new database):

```powershell
docker exec masaha-postgres-1 psql -U masaha -d postgres -c "CREATE DATABASE masaha_cr_dev"
docker exec masaha-postgres-1 sh -c "pg_dump -U masaha -d masaha_dev --no-owner | psql -q -v ON_ERROR_STOP=1 -U masaha -d masaha_cr_dev"
```

Then the test database, empty (the API lane migrates it):

```powershell
docker exec masaha-postgres-1 psql -U masaha -d postgres -c "CREATE DATABASE masaha_cr_test"
```

### 2.3 The two `.env` files

Copy them from **`app-design`** (never from `app`), then change exactly these lines (UTF-8 without BOM):

```powershell
Copy-Item C:\dev\masaha\app-design\apps\api\.env C:\dev\masaha\app-cr\apps\api\.env
Copy-Item C:\dev\masaha\app-design\apps\web\.env C:\dev\masaha\app-cr\apps\web\.env

$f = 'C:\dev\masaha\app-cr\apps\api\.env'
$t = [System.IO.File]::ReadAllText($f)
$t = [regex]::Replace($t, '(?m)^PORT=[^\r\n]*', 'PORT=3337')
$t = [regex]::Replace($t, '(?m)^CORS_ORIGIN=[^\r\n]*', 'CORS_ORIGIN=http://localhost:5337')
$t = [regex]::Replace($t, '(?m)^DATABASE_URL=[^\r\n]*', 'DATABASE_URL=postgresql://masaha:masaha@localhost:5433/masaha_cr_dev')
$t = [regex]::Replace($t, '(?m)^TEST_DATABASE_URL=[^\r\n]*', 'TEST_DATABASE_URL=postgresql://masaha:masaha@localhost:5433/masaha_cr_test')
[System.IO.File]::WriteAllText($f, $t)

$f = 'C:\dev\masaha\app-cr\apps\web\.env'
$t = [System.IO.File]::ReadAllText($f)
$t = [regex]::Replace($t, '(?m)^WEB_PORT=[^\r\n]*', 'WEB_PORT=5337')
$t = [regex]::Replace($t, '(?m)^API_PROXY_TARGET=[^\r\n]*', 'API_PROXY_TARGET=http://localhost:3337')
[System.IO.File]::WriteAllText($f, $t)

Select-String -Path C:\dev\masaha\app-cr\apps\api\.env -Pattern '^(PORT|CORS_ORIGIN|DATABASE_URL|TEST_DATABASE_URL)='
Select-String -Path C:\dev\masaha\app-cr\apps\web\.env -Pattern '^(WEB_PORT|API_PROXY_TARGET|NODE_ENV)='
```

Expected: the api file shows exactly the four new values once each; the web file shows `WEB_PORT=5337`,
`API_PROXY_TARGET=http://localhost:3337` and, in that copied file, a `NODE_ENV=development` line (leave it: §12.1 builds
with `NODE_ENV=production` set in the shell). If a line is missing or appears twice, stop and report. `.env` files are
git-ignored: `git status` must still be clean.

### 2.4 Install, build, generate, migrate (all through the grant script)

```powershell
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm ci
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run build -w @masaha/shared
Set-Location C:\dev\masaha\app-cr\apps\api; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npx prisma generate
Set-Location C:\dev\masaha\app-cr\apps\api; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npx prisma migrate deploy
Set-Location C:\dev\masaha\app-cr\apps\api; $env:DATABASE_URL = 'postgresql://masaha:masaha@localhost:5433/masaha_cr_test'; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npx prisma migrate deploy; Remove-Item Env:DATABASE_URL
docker exec masaha-postgres-1 psql -U masaha -d masaha_cr_test -tAc "SELECT count(*) FROM _prisma_migrations"
git -C C:\dev\masaha\app-cr status
```

`migrate deploy` must say the databases are up to date, or apply migrations and end without error; the count must be
above 0; `git status` must be clean (if `package-lock.json` changed, stop and report).

### 2.5 The breaks log

Keep a running list, in `C:\dev\masaha\workspace\TASKS\CONTACT_RULES\4_REPORT.md` under a heading *Breaks log*, of
every test seen failing: the test, the break (or "before the code"), the failure line, the restore. §12 needs it.

---

## 3. The gate after every commit — mandatory, no exception

After each `git commit`, run all four, in this order, each through the grant script where shown:

1. `node $H cr npm run lint`
2. `node $H cr npm run typecheck`
3. `npx prettier --check <the commit's .ts/.tsx files>` (the list is in each commit's section; Markdown is excluded
   from Prettier in this repository, so never pass a `.md` file)
4. The commit's touched test files alone (the exact commands are in each commit's section).

**On a failure:** fix it, `git add <the paths>`, `git commit --amend --no-edit` (the commit is HEAD, so this is the
fixup squashed at once), and run the whole gate again. A fix that belongs to an **earlier** commit:
`git branch backup/contact-rules-<n>` first, then `git commit --fixup=<that sha>` and
`git rebase --autosquash origin/main` (Git 2.55 needs no `-i`). Twice failing on the same check: stop and report.

**What this repository's lint and checks refuse (each has cost a red CI before):**

- `boundaries/dependencies`: a feature importing a sibling feature (`@features/<other>`); `shared/` importing a
  feature or a page; the design system importing anything outside itself; a deep path past a module's `index.ts`
  (use `@shared/lib`, never `@shared/lib/numbers/…`, from outside the module). In `packages/shared`, `core` imports
  nothing but `zod` and `@date-fns/tz`, and the package imports its own files by relative path with `.ts`.
- `@typescript-eslint/no-non-null-assertion`: no `!` after an expression.
- `@typescript-eslint/no-unnecessary-type-assertion`: no `as X` where the type is already `X` (the tests'
  `rows(sheet).at(-1) as HTMLElement` is needed, since `.at()` may be `undefined`).
- Unused imports and variables: after moving `toWesternDigits`, remove it from every import list that no longer uses
  it; after adding `beforeAll` to a `vitest` import, it must be used.
- `restrict-template-expressions`: a number in a template literal is wrapped, `String(n)`.
- `no-floating-promises`: `await` every user-event call and every `waitFor`.
- `no-confusing-void-expression`: an arrow that calls a void function takes braces: `act(() => { toast('Saved'); })`.
- `require-await`: an `async` function must `await` something.
- `prefer-nullish-coalescing`, `no-unnecessary-condition`: no `?.` or `??` on a value that cannot be nullish.
- **Prettier rewraps long lines and long import lists** (print width 100): run
  `npx prettier --write <the commit's .ts/.tsx files>` **before** each commit, then the check passes.
- `check:classes`: no physical direction classes (`ml-`, `left-`, `text-left` …) anywhere; no arbitrary-value
  utility (`bg-[…]`, `bg-(--x)`) outside `apps/web/src/shared/design-system/`; no selected tint as a hover
  (`hover:bg-accent` …). An arbitrary *variant* (`[[data-slot=table-row]_&]:`) is allowed.

---

## 4. Commit 1 — C1 + C2, phones (step 2)

**Subject:** `fix(shared): read Arabic-Indic digits in phones` (47 characters)

**Body** (write the message to `C:\dev\masaha\workspace\TASKS\CONTACT_RULES\scripts\msg-1.txt` with your file tool,
UTF-8 without BOM, and commit with `git commit -F <that file>`):

```
fix(shared): read Arabic-Indic digits in phones

Every phone the platform takes (a contact's WhatsApp or phone, a «وسيلة
أخرى» number, a customer's phone, the platform's WhatsApp) refused a
number typed on an Arabic keyboard: the rule read Western digits only
(finding 217). The owner decided that Arabic-Indic and Eastern digits
are read as Western ones.

The one reader of typed digits, toWesternDigits, moves from the web's
shared/lib to @masaha/shared/core, so the browser and the server read
the same digits; the phone rule and «وسيلة أخرى»'s test for a number
read through it. The accepted forms are unchanged: +970, +972, 00970,
00972 and the local 0, each already tested.
```

### 4.1 Tests first (they must fail before the code)

**a. `packages/shared/src/core/phone.unit.test.ts`** — inside `describe('phoneSchema', …)`, after the test
`'drops the (0) written after the country code'`, add:

```ts
  it.each([
    ['Arabic-Indic', '٠٥٩٩١٢٣٤٥٦', '+970599123456'],
    ['Eastern', '۰۵۹۹۱۲۳۴۵۶', '+970599123456'],
    ['Arabic-Indic, after +970,', '+٩٧٠ ٥٩ ٩١٢ ٣٤٥٦', '+970599123456'],
    ['Arabic-Indic, after 00972,', '٠٠٩٧٢٥٢١٢٣٤٥٦٧', '+972521234567'],
    ['Arabic-Indic and Western', '٠٥٩-٩١٢ 3456', '+970599123456'],
    ['Eastern, a landline’s,', '(۰۸) ۲۸۲ ۱۲۳۴', '+97082821234'],
  ])('reads %s digits as Western ones: %s', (_digits, input, phone) => {
    expect(stored(input)).toBe(phone);
  });
```

and in the `it.each` of `'refuses %s'`, after `['letters', '059 912 3456 ext 2'],`, add:

```ts
    ['too few Arabic-Indic digits', '١٢٣'],
    ['another country in Arabic-Indic digits', '+١٢٠٢٥٥٥٠١٠٠'],
```

*Break:* before the code (§4.2) the six new accepted cases fail (`expected { phone: ['invalid_format'] } to be …`).
The two refusals pass before and after: their break is in §4.3.

**b. `packages/shared/src/spaces/contacts.unit.test.ts`** — inside `describe('a contact of another kind («وسيلة أخرى»)', …)`,
after the test `'refuses a number the phone rule refuses, never reading it as a link'`, add:

```ts
  it('reads a number typed in Arabic-Indic or Eastern digits by the phone rule', () => {
    expect(other('٠٥٩-٩١٢ ٣٤٥٦')).toEqual([
      { type: 'OTHER', value: '+970599123456', label: 'ديسكورد' },
    ]);
    expect(other('۰۵۶۹۱۲۳۴۵۶')).toEqual([
      { type: 'OTHER', value: '+970569123456', label: 'ديسكورد' },
    ]);
    expect(other('١٢٣')).toEqual(INVALID);
  });
```

*Break:* before the code both numbers are refused (an Arabic digit is not `\d`, so the value is read as a link).

**c. `apps/web/src/features/spaces/components/contacts/ContactsSheet.component.test.tsx`** — inside
`describe('the contacts’ Sheet', …)`, after the test `'shows the form a value is saved in once it differs from what was typed'`, add:

```tsx
  it('reads a number typed in Arabic-Indic digits, and sends it in its international form', async () => {
    const user = userEvent.setup({ delay: null });
    const { writes } = renderProfile({ write: () => ok(SPACE) });
    const sheet = await openContacts(user);
    await user.click(within(sheet).getByRole('button', { name: 'Add a contact' }));
    const added = rows(sheet).at(-1) as HTMLElement;

    await user.type(within(added).getByRole('textbox', { name: 'WhatsApp' }), '٠٥٩٩٧٧٧٨٨٨');
    expect(within(added).getByRole('textbox', { name: 'WhatsApp' })).toHaveAccessibleDescription(
      /Saved as .*\+970599777888/,
    );
    await user.click(within(sheet).getByRole('button', { name: 'Save' }));

    await waitFor(() => {
      expect(writes()).toHaveLength(1);
    });
    expect(bodyOf(writes()[0])).toEqual({
      contacts: [...SPACE.contacts, { type: 'WHATSAPP', value: '+970599777888', label: null }],
    });
  });
```

*Break:* before the code, no "Saved as" description (the value is refused).

**d. `apps/web/src/features/desk/hooks/edit/useEditDialog.component.test.tsx`** — inside `describe('useEditDialog', …)`,
after the test `'sends null for a cleared phone'`, add (note the apostrophe in `isn’t` is U+2019, as the catalogue
writes it):

```tsx
  it('reads a phone typed in Arabic-Indic digits, and sends its international form', async () => {
    const user = userEvent.setup();
    const { requests } = renderDialog(() => ok({ ...SARA, phone: '+970599000304' }));

    const phone = screen.getByRole('textbox', { name: /Mobile number/ });
    await user.clear(phone);
    await user.type(phone, '٠٥٩٩٠٠٠٣٠٤');
    await user.click(screen.getByRole('button', { name: 'Save' }));

    await findToast(heard('Sara Khalid’s details saved'));
    expect(bodyOf(patches(requests)[0])).toEqual({ phone: '+970599000304' });
  });

  it('refuses in the browser a phone the rule refuses, sending nothing', async () => {
    const user = userEvent.setup();
    const { requests } = renderDialog(() => ok(SARA));

    const phone = screen.getByRole('textbox', { name: /Mobile number/ });
    await user.clear(phone);
    await user.type(phone, '١٢٣');
    await user.click(screen.getByRole('button', { name: 'Save' }));

    expect(await screen.findByText('This isn’t in a valid format.')).toBeVisible();
    expect(patches(requests)).toHaveLength(0);
  });
```

*Break:* the first fails before the code (no toast: the phone is refused). The second passes before and after: its
break is in §4.3.

**e. `apps/api/src/modules/spaces/contacts/contacts.api.test.ts`** — inside
`describe('PUT /admin/spaces/:spaceId/contacts', …)`, after the test
`'refuses an invalid contact or a repeated one with the shared rules, writing nothing'`, add:

```ts
  it('stores a number typed in Arabic-Indic or Eastern digits in its international form', async () => {
    const response = await save([
      { type: 'WHATSAPP', value: '٠٥٩٩١٢٣٤٥٦' },
      { type: 'OTHER', value: '۰۵۶۹۱۲۳۴۵۶', label: 'رقم آخر' },
    ]);

    expect(response.status).toBe(200);
    expect((await stored()).contacts).toEqual([
      { type: 'WHATSAPP', value: '+970599123456', label: null, sortOrder: 0 },
      { type: 'OTHER', value: '+970569123456', label: 'رقم آخر', sortOrder: 1 },
    ]);
  });
```

*Break:* before the code, `422`.

Run them now and see each fail as described (record in the breaks log):

```powershell
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run test:unit -w @masaha/shared -- src/core/phone src/spaces/contacts
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run test:component -w @masaha/web -- src/features/spaces/components/contacts/ContactsSheet src/features/desk/hooks/edit/useEditDialog
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run test:api -w @masaha/api -- src/modules/spaces/contacts/contacts.api
```

### 4.2 The code

**a. Move the reader, keeping its history:**

```powershell
git mv apps/web/src/shared/lib/numbers/westernDigits.ts packages/shared/src/core/digits.ts
git mv apps/web/src/shared/lib/numbers/westernDigits.unit.test.ts packages/shared/src/core/digits.unit.test.ts
```

**b. `packages/shared/src/core/digits.ts`** — the function is unchanged; only its comment's last sentence changes.
The whole file becomes:

```ts
const ARABIC_INDIC_ZERO = 0x0660;
const EXTENDED_ARABIC_INDIC_ZERO = 0x06f0;

/**
 * A text with its Arabic-Indic digits (٠–٩, U+0660–U+0669) and the extended ones a Persian or Urdu
 * keyboard types (۰–۹, U+06F0–U+06F9) as Western digits; everything else as it is. The one reader
 * of typed digits, in the browser and on the server: each field's own rule (a phone, a whole
 * number, an amount, a time, a point) reads its result.
 */
export function toWesternDigits(text: string): string {
  return text.replace(/[٠-٩۰-۹]/g, (digit) => {
    const code = digit.codePointAt(0) ?? ARABIC_INDIC_ZERO;
    return String(
      code - (code >= EXTENDED_ARABIC_INDIC_ZERO ? EXTENDED_ARABIC_INDIC_ZERO : ARABIC_INDIC_ZERO),
    );
  });
}
```

**c. `packages/shared/src/core/digits.unit.test.ts`** — replace its first two lines with the package's style (a blank
line, then the relative import with `.ts`); the rest stays:

```ts
import { describe, expect, it } from 'vitest';

import { toWesternDigits } from './digits.ts';
```

**d. `packages/shared/src/core/index.ts`** — add as the **first** line: `export * from './digits.ts';`

**e. `packages/shared/src/core/phone.ts`**:
- After `import { z } from 'zod';` add a blank line and `import { toWesternDigits } from './digits.ts';`
- The header comment (its three lines) becomes these four:

```ts
// One phone number has one form (docs/architecture/data-model.md › Conventions, Contacts): E.164,
// for a Palestinian (+970) or an Israeli (+972) number. It may arrive international (+970…,
// 00970…) or local (0…), in Western, Arabic-Indic or Eastern digits, with the separators people
// type between its digits.
```
- In `normalisePhone`, the first line becomes (Prettier will wrap it):
  `const digits = toWesternDigits(input.trim()).replace(TRUNK_AFTER_COUNTRY, '$1').replace(SEPARATORS, '');`

**f. `packages/shared/src/spaces/contacts.ts`**:
- The import becomes `import { emailSchema, normalisePhone, toWesternDigits } from '../core/index.ts';`
- The `OTHER` case and its comment become:

```ts
    // A number, in any digits people type, takes the platform's phone rule, so one number has one
    // form; anything else is a link on the web, as a website's. A number the rule refuses is
    // refused, never read as a link (a URL reads a bare number as an IP address).
    case 'OTHER':
      return LIKE_A_NUMBER.test(toWesternDigits(value))
        ? normalisePhone(value)
        : websiteAddress(value);
```

**g. The web's callers** (each now imports from `@masaha/shared/core`, which every zone may import):
- `apps/web/src/shared/lib/index.ts`: delete the line `export { toWesternDigits } from './numbers/westernDigits';`
- `apps/web/src/shared/lib/money/shekels.ts`: line 1 becomes `import { toWesternDigits } from '@masaha/shared/core';`
- `apps/web/src/shared/lib/numbers/wholeNumber.ts`: line 1 becomes `import { toWesternDigits } from '@masaha/shared/core';`
- `apps/web/src/features/packages/services/packageValues.ts`: the line
  `import { agorotOf, shekelsOf, toWesternDigits } from '@shared/lib';` becomes
  `import { agorotOf, shekelsOf } from '@shared/lib';`, and a new first line
  `import { toWesternDigits } from '@masaha/shared/core';` is added above
  `import type { SpacePackage, SUBSCRIPTION_BILLINGS } from '@masaha/shared/packages';`
- `apps/web/src/shared/map/services/coordinates.ts`: line 1 becomes
  `import { toWesternDigits } from '@masaha/shared/core';`

Then `git grep -n "westernDigits\|toWesternDigits" -- apps packages` must show only `packages/shared/src/core/…`,
`packages/shared/src/spaces/contacts.ts` and the four callers above, each importing from `@masaha/shared/core`.

### 4.3 The breaks for the tests that pass before and after (make each once, see it fail, restore)

| Test | Break (temporary) | Must fail with | Restore |
|---|---|---|---|
| `toWesternDigits` › `reads both Arabic-Indic sets as Western digits` (`digits.unit.test.ts`) | in `digits.ts`, `0x06f0` → `0x06f1` | the Eastern line | put `0x06f0` back |
| C2 — `phoneSchema` › `stores %s in its international form` (the `00970…`, `00972…` rows) | in `phone.ts`, `(?:(?:\+|00)(970|972)|0)` → `(?:(?:\+)(970|972)|0)` | the two `00…` rows | put `\+|00` back |
| the two new Arabic refusals (`١٢٣`, `+١٢٠٢٥٥٥٠١٠٠`) | in `normalisePhone`, `if (!match) return null;` → ``if (!match) return `+970${digits}`;`` (a rule that took any digits) | both rows | restore `return null;` |
| `refuses in the browser a phone the rule refuses, sending nothing` | in `phone.ts`'s `phoneSchema`, `if (phone) return phone;` → `return phone ?? input;` | a PATCH is sent | restore |

### 4.4 Documents of this commit

**`docs/architecture/data-model.md`** (› Conventions, Contacts, the phone line). Replace
`Input arrives as `+970…`, `+972…`, `00970…`, `00972…` or local `0…`, the spaces, dashes, dots and parentheses people type between digits dropped,`
with
`Input arrives as `+970…`, `+972…`, `00970…`, `00972…` or local `0…`, in Western, Arabic-Indic (`٠–٩`) or Eastern (`۰–۹`) digits, read as Western ones, the spaces, dashes, dots and parentheses people type between digits dropped,`
and set its header's `**Last Updated:**` to `2026-11-15`.

**`docs/frontend/architecture.md`** (§1, the `shared/` row). Replace
`a CSV built in the browser and its download, and the one reader of Arabic-Indic digits that every typed number goes through)`
with
`a CSV built in the browser and its download; every typed number is read through `@masaha/shared/core`'s `toWesternDigits`, the one reader of Arabic-Indic digits, which the phone rule reads too)`
and set its header's `**Last Updated:**` to `2026-11-15`.

**`docs/features/spaces.md`**:
- *API decisions*: after the bullet that starts `- **The phone rule is the platform's, in `core`** (D6).`, add:
  `- **A number is read whatever digits it is typed in** (C1): Arabic-Indic (`٠–٩`) and Eastern (`۰–۹`) digits become Western before the phone rule reads them, for every phone of the platform, a «وسيلة أخرى» number included; the reader is `core`'s `toWesternDigits`, the web's too. *Why:* an Arabic keyboard types them, and the browser and the server read one rule ([finding 217](../architecture/findings/217-contacts-and-every-phone-refuse-arabic-indic-digits.md)). 2026-11-15, #PRNUM.`
- *API history*: at its end, add `- 2026-11-15, #PRNUM — a phone or a «وسيلة أخرى» number typed in Arabic-Indic or Eastern digits is read (finding 217).`
- Header `**Last Updated:**` → `2026-11-15`.

**`docs/features/customers.md`** — *API history*, at its end:
`- 2026-11-15, #PRNUM — a customer's phone typed in Arabic-Indic or Eastern digits is read by `core`'s phone rule, and a whole phone so typed is searched as a phone (finding 217).` Header date → `2026-11-15`.

**`docs/features/desk.md`** — *API history*, at its end:
`- 2026-11-15, #PRNUM — a phone typed in Arabic-Indic or Eastern digits is read at the check-out, a debt and a payment, by `core`'s phone rule (finding 217).` Header date → `2026-11-15`.

**`docs/features/platform-settings.md`** — *API history*, at its end:
`- 2026-11-15, #PRNUM — the platform's WhatsApp typed in Arabic-Indic or Eastern digits is read by `core`'s phone rule (finding 217).` Header date → `2026-11-15`.

(`#PRNUM` is replaced in §12.2, just before the push. Write it exactly so.)

### 4.5 Commit and gate

```powershell
npx prettier --write packages/shared/src/core/digits.ts packages/shared/src/core/digits.unit.test.ts packages/shared/src/core/index.ts packages/shared/src/core/phone.ts packages/shared/src/core/phone.unit.test.ts packages/shared/src/spaces/contacts.ts packages/shared/src/spaces/contacts.unit.test.ts apps/web/src/shared/lib/index.ts apps/web/src/shared/lib/money/shekels.ts apps/web/src/shared/lib/numbers/wholeNumber.ts apps/web/src/features/packages/services/packageValues.ts apps/web/src/shared/map/services/coordinates.ts apps/web/src/features/spaces/components/contacts/ContactsSheet.component.test.tsx apps/web/src/features/desk/hooks/edit/useEditDialog.component.test.tsx apps/api/src/modules/spaces/contacts/contacts.api.test.ts
git add packages/shared/src/core/digits.ts packages/shared/src/core/digits.unit.test.ts packages/shared/src/core/index.ts packages/shared/src/core/phone.ts packages/shared/src/core/phone.unit.test.ts packages/shared/src/spaces/contacts.ts packages/shared/src/spaces/contacts.unit.test.ts apps/web/src/shared/lib/index.ts apps/web/src/shared/lib/money/shekels.ts apps/web/src/shared/lib/numbers/wholeNumber.ts apps/web/src/features/packages/services/packageValues.ts apps/web/src/shared/map/services/coordinates.ts apps/web/src/features/spaces/components/contacts/ContactsSheet.component.test.tsx apps/web/src/features/desk/hooks/edit/useEditDialog.component.test.tsx apps/api/src/modules/spaces/contacts/contacts.api.test.ts docs/architecture/data-model.md docs/frontend/architecture.md docs/features/spaces.md docs/features/customers.md docs/features/desk.md docs/features/platform-settings.md
git status
git commit -F C:\dev\masaha\workspace\TASKS\CONTACT_RULES\scripts\msg-1.txt
```

`git status` before the commit must show exactly these 21 paths staged (two as renames) and nothing else changed.

**Gate:** lint; typecheck; `npx prettier --check` on the 15 code files above; then

```powershell
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run test:unit -w @masaha/shared -- src/core src/spaces/contacts
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run test:unit -w @masaha/web -- src/shared/lib src/shared/map src/features/packages
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run test:component -w @masaha/web -- src/features/spaces/components/contacts/ContactsSheet src/features/desk/hooks/edit/useEditDialog
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run test:api -w @masaha/api -- src/modules/spaces/contacts/contacts.api
```

---

## 5. Commit 2 — C3 + C4, only real links (step 3)

**Subject:** `fix(spaces): accept only real links in contacts` (47 characters)

**Body** (`scripts\msg-2.txt`):

```
fix(spaces): accept only real links in contacts

A website took any host with a dot, so a bare number was stored as an
IP address (123 as https://0.0.0.123), and a Facebook link kept any
path, so a video's link lost its id and opened Facebook's video home
(finding 218).

A link's host is now a domain with a top-level domain. A Facebook link
must name a page or a profile: a username, profile.php?id=<digits> or
/people/<name>/<id>; a handle that names one of Facebook's own sections
is refused too. The browser runs the same shared rule first, so the
Sheet says a refused value on its row and sends nothing; the server
still refuses it.
```

### 5.1 Tests first

**a. `packages/shared/src/spaces/contacts.unit.test.ts`** — inside `describe('updateSpaceContactsSchema', …)`, after the
test `'refuses a website without a domain, of another scheme, or with credentials'`, add:

```ts
  it.each([
    ['a bare number', '123'],
    ['a longer bare number', '599123456'],
    ['an IP address', 'http://10.0.0.1'],
    ['an IP address without its scheme', '10.0.0.1/menu'],
    ['a short IP address', 'http://127.1'],
    ['an IPv6 address', 'https://[::1]/'],
    ['localhost with a port', 'http://localhost:5173'],
    ['a bare word', 'example'],
    ['a one-letter top-level domain', 'masaha.p'],
    ['a name that starts with a dash', 'https://-masaha.ps'],
  ])('refuses a website that is %s: %s', (_case, value) => {
    expect(one('WEBSITE', value)).toEqual(INVALID);
  });

  it.each([
    ['www.masaha.ps/about', 'https://www.masaha.ps/about'],
    ['https://Masaha-Hub.co.uk', 'https://masaha-hub.co.uk'],
    ['123.ps', 'https://123.ps'],
  ])('stores a website on a domain with a top-level domain: %s', (value, url) => {
    expect(one('WEBSITE', value)).toBe(url);
  });

  it.each([
    [
      'facebook.com/people/Masaha-Hub/100012345678',
      'https://www.facebook.com/people/Masaha-Hub/100012345678',
    ],
    ['https://m.facebook.com/Masaha-Space-123456/', 'https://www.facebook.com/Masaha-Space-123456'],
    ['www.facebook.com/masaha.gaza?ref=bookmarks', 'https://www.facebook.com/masaha.gaza'],
  ])('stores a Facebook page or profile: %s', (value, url) => {
    expect(one('FACEBOOK', value)).toBe(url);
  });

  it.each([
    'facebook.com/watch?v=1',
    'https://www.facebook.com/watch/?v=123',
    'facebook.com/reel/123',
    'facebook.com/masaha/videos/123',
    'facebook.com/masaha.gaza/posts/pfbid02abc',
    'facebook.com/permalink.php?story_fbid=1&id=2',
    'facebook.com/story.php?story_fbid=1&id=2',
    'facebook.com/groups/gazafreelancers',
    'facebook.com/events/123',
    'facebook.com/photo/?fbid=123',
    'facebook.com/photo.php?fbid=123',
    'facebook.com/masaha/photos/a.1/2',
    'facebook.com/share/p/abc',
    'facebook.com/sharer/sharer.php?u=x',
    'facebook.com/search/top?q=masaha',
    'facebook.com/people/Masaha-Hub',
    'facebook.com/people/Masaha-Hub/abc',
    'watch',
    '@groups',
  ])('refuses a Facebook link or handle that names no page or profile: %s', (value) => {
    expect(one('FACEBOOK', value)).toEqual(INVALID);
  });
```

and inside `describe('a contact of another kind («وسيلة أخرى»)', …)`, after the test added in commit 1:

```ts
  it('refuses a link to an IP address', () => {
    expect(other('http://10.0.0.1')).toEqual(INVALID);
  });
```

*Break:* before the code these must fail (they are stored): the website rows `123`, `599123456`, `http://10.0.0.1`,
`10.0.0.1/menu`, `http://127.1`, `masaha.p`, `https://-masaha.ps`; every Facebook refusal; «وسيلة أخرى»'s
`http://10.0.0.1`. The rows `https://[::1]/`, `http://localhost:5173` and `example` are refused already (no dot) and
pass before and after. The accepted rows pass before and after: their breaks are in §5.3.

**b. `apps/web/src/features/spaces/components/contacts/ContactsSheet.component.test.tsx`** — after the test
`'refuses a value in its type’s words, and a repeat as added before'`, add:

```tsx
  it('refuses a website on an IP address and a Facebook video on their rows, sending nothing', async () => {
    const user = userEvent.setup({ delay: null });
    const { writes } = renderProfile();
    const sheet = await openContacts(user);
    await user.click(within(sheet).getByRole('button', { name: 'Add a contact' }));
    await user.click(within(sheet).getByRole('button', { name: 'Add a contact' }));
    const [, , site, video] = rows(sheet) as [HTMLElement, HTMLElement, HTMLElement, HTMLElement];

    await choose(user, site, 'Type', 'Website');
    await user.type(within(site).getByRole('textbox', { name: 'Website' }), 'http://10.0.0.1');
    await choose(user, video, 'Type', 'Facebook');
    await user.type(
      within(video).getByRole('textbox', { name: 'Facebook' }),
      'facebook.com/watch?v=1',
    );
    await user.click(within(sheet).getByRole('button', { name: 'Save' }));

    expect(await within(site).findByText('Not a valid link')).toBeInTheDocument();
    expect(within(video).getByText('Not a valid page name or link')).toBeInTheDocument();
    expect(writes()).toEqual([]);
  });
```

**How it proves C4 (no request for a refused value):** `renderProfile` puts the fake adapter on the one client and
`writes()` lists every write it received. The row's words appear only after «حفظ» has run the form's check (the
shared `updateSpaceContactsSchema`, through `useServerForm`'s resolver); the check runs before `submit`, and a failed
check never calls it. So once the words are found, an empty `writes()` proves nothing was sent. *Break:* before the
code (§5.2) both values are valid, so one write is sent and the words never appear.

**c. `apps/api/src/modules/spaces/contacts/contacts.api.test.ts`** — after the test added in commit 1:

```ts
  it.each([
    ['WEBSITE', 'http://10.0.0.1'],
    ['WEBSITE', '123'],
    ['FACEBOOK', 'facebook.com/watch?v=1'],
  ])('refuses a %s that names no real page, %s, writing nothing', async (type, value) => {
    const response = await save([{ type, value }]);

    expect(response.status).toBe(422);
    expect(errorOf(response).errors).toEqual({ 'contacts.0.value': ['invalid_format'] });
    expect(await stored()).toEqual({ contacts: [], contactsUpdatedAt: BEFORE });
  });
```

**The server's proof:** the request goes through the real Express app and PostgreSQL (`masaha_cr_test`): the
controller parses the body with the same shared schema, answers `422` with the field's code, and the table and the
group's date are unchanged. *Break:* before the code, `200`.

Run the three files and see the failures; record them.

### 5.2 The code — `packages/shared/src/spaces/contacts.ts`

**a.** After the `LIKE_A_LINK` constant, add:

```ts
/**
 * A host that is a domain with a top-level domain (`masaha.ps`, `t.me`; an internationalised one in
 * its `xn--` form): never an IP address, which a URL reads a bare number as, `localhost` or a bare
 * word.
 */
const DOMAIN = /^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+(?:[a-z]{2,63}|xn--[a-z0-9-]{1,59})$/i;
```

**b.** The `FACEBOOK` entry of `NETWORKS` becomes:

```ts
  // A page or a profile: its username, one segment that is none of Facebook's own sections and no
  // `.php` script, or `/people/<name>/<id>` (a profile with no username, `profile.php?id=`, is read
  // apart). A video, `/watch`, a post, a group, an event, a photo, a share or a search names neither.
  FACEBOOK: {
    hosts: ['facebook.com', 'm.facebook.com', 'fb.com'],
    base: 'https://www.facebook.com',
    handlePath: (handle) => `/${handle}`,
    paths:
      /^\/(?:(?!(?:watch|reels?|videos?|posts?|groups|events|photos?|share|sharer|search|stories|story|hashtag|live|gaming|marketplace|pages|people|permalink)$)(?![^/]*\.php$)[\w.-]+|people\/[^/]+\/\d+)$/i,
  },
```

**c.** In `linkOf`, the comment and the last line become:

```ts
/**
 * A link typed with or without its scheme, as a URL on a domain; null when it is none, not on the
 * web, or on an IP address, `localhost` or a bare word.
 */
```
```ts
  return onTheWeb && !url.username && !url.password && DOMAIN.test(url.hostname) ? url : null;
```

**d.** `networkAddress` becomes (its comment gains one sentence; the handle's path is checked too; the Facebook
profile's `id` is read before the paths are):

```ts
/**
 * A network's handle or link as its full address. A link must be on the network's own host, and
 * keeps its path only: its query and fragment are dropped, except a Facebook profile's numeric
 * `id`, the only address of a profile with no username. A network that names its paths takes a
 * handle or a link only on one of them.
 */
function networkAddress(network: Network, input: string): string | null {
  const handle = HANDLE.exec(input)?.[1];
  if (network.handlePath && handle && !LIKE_A_LINK.test(handle)) {
    const path = network.handlePath(handle);
    return network.paths && !network.paths.test(path) ? null : `${network.base}${path}`;
  }

  const url = linkOf(input);
  if (!url || !onHostOf(network, url)) return null;
  const path = pathOf(url);
  if (network === NETWORKS.FACEBOOK && path === '/profile.php') {
    const id = url.searchParams.get('id');
    return id && /^\d+$/.test(id) ? `${network.base}${path}?id=${id}` : null;
  }
  if (!path || (network.paths && !network.paths.test(path))) return null;
  return `${network.base}${path}`;
}
```

Also update the `paths` field's comment in `interface Network` to:
`/** The paths a handle or a link may have, when only some name what the contact is (a channel, a page). */`

Run the three files: all pass, and the whole `contacts.unit.test.ts` and `contacts.api.test.ts` stay green.

### 5.3 Breaks (make each once, see it fail, restore)

| Test | Break | Must fail | Restore |
|---|---|---|---|
| the website refusals | in `linkOf`, `DOMAIN.test(url.hostname)` → `url.hostname.includes('.')` | `123`, `599123456`, the IP rows | put `DOMAIN.test(url.hostname)` back |
| the Facebook refusals | delete the `paths:` property of `FACEBOOK` | every refused link | restore it |
| `watch`, `@groups` | in `networkAddress`'s handle branch, `return network.paths && … : …;` → `return `${network.base}${network.handlePath(handle)}`;` | `watch`, `@groups` | restore |
| `stores a Facebook page or profile` (`/people/…`) | delete `|people\/[^/]+\/\d+` from the regex | the `/people/` row | restore |
| the profile's `id` (existing test `keeps the id of a Facebook profile…`) | move the `profile.php` block below the `paths` check | that test | move it back |
| `stores a Facebook page or profile` (`Masaha-Space-123456`) | in the regex, `[\w.-]+` → `[\w.]+` | that row | restore |
| `stores a website on a domain …` (`123.ps`) | in `DOMAIN`, the first `[a-z0-9]` → `[a-z]` | that row | restore |

### 5.4 Documents of this commit

**`docs/architecture/data-model.md`** (› Conventions, the line on the networks and a website). Replace
`a network's link must be on its own host and keeps its path only, its query and fragment dropped, except the numeric `id` of a Facebook profile with no username (`profile.php?id=…`); a website keeps its path and query, with a lowercase host.`
with
`a link's host is a domain with a top-level domain (`masaha.ps`), never an IP address (a URL reads a bare number such as `123` as one), `localhost` or a bare word; a network's link must be on its own host and keeps its path only, its query and fragment dropped, except the numeric `id` of a Facebook profile with no username (`profile.php?id=…`); a Facebook link names a page or a profile — a username, `profile.php?id=…` or `/people/<name>/<id>` — never a video, `/watch`, a post, a group, an event, a photo, a share or a search, and a handle that names one of those sections is refused too; a website keeps its path and query, with a lowercase host.`

**`docs/features/spaces.md`**:
- *API decisions*: after the bullet added in commit 1, add:
  `- **A link is on a real domain, and a Facebook link names a page or a profile** (C3): a link's host is a domain with a top-level domain, never an IP address, `localhost` or a bare word; a Facebook link is a username, `/profile.php?id=<digits>` or `/people/<name>/<id>`, never a video, `/watch`, a post, a group, an event, a photo, a share or a search. The Sheet refuses such a value on its row before sending, by the same shared rule (C4). *Why:* a URL reads a bare number as an IP address, and a Facebook link that names no page opens none ([finding 218](../architecture/findings/218-a-websites-bare-number-is-stored-as-an-ip-address-a-facebook-video-link-loses-its-id.md)). 2026-11-15, #PRNUM.`
- *API history*: after the line of commit 1, add
  `- 2026-11-15, #PRNUM — a website only on a domain with a top-level domain, never an IP address; a Facebook link only to a page or a profile (finding 218).`

### 5.5 Commit and gate

```powershell
npx prettier --write packages/shared/src/spaces/contacts.ts packages/shared/src/spaces/contacts.unit.test.ts apps/web/src/features/spaces/components/contacts/ContactsSheet.component.test.tsx apps/api/src/modules/spaces/contacts/contacts.api.test.ts
git add packages/shared/src/spaces/contacts.ts packages/shared/src/spaces/contacts.unit.test.ts apps/web/src/features/spaces/components/contacts/ContactsSheet.component.test.tsx apps/api/src/modules/spaces/contacts/contacts.api.test.ts docs/architecture/data-model.md docs/features/spaces.md
git status
git commit -F C:\dev\masaha\workspace\TASKS\CONTACT_RULES\scripts\msg-2.txt
```

**Gate:** lint; typecheck; Prettier check on the four code files; then

```powershell
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run test:unit -w @masaha/shared -- src/spaces
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run test:component -w @masaha/web -- src/features/spaces/components/contacts src/features/directory
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run test:api -w @masaha/api -- src/modules/spaces src/db/seed
```

(`src/db/seed` proves the demo seed's contacts still pass the rules; `src/features/directory` that the public page's
contacts still render.)

Then run the data count, §7.

---

## 6. Commit 3 — C5, the row's ghost control (step 4)

**Subject:** `fix(design-system): wash a row's ghost control` (46 characters)

**Body** (`scripts\msg-3.txt`):

```
fix(design-system): wash a row's ghost control

Inside a table row, which takes the hover fill under the pointer and
while its menu is open, a ghost control's own hover and open state
took the same fill and showed nothing (finding 226). The owner decided
it takes the ink's wash, hover-on-muted, over the row's hover, in both
themes.

The ghost variant's rule names the row, so it outweighs the plain hover
by specificity, never by the order the utilities are emitted in. The
token test now checks the wash seen from hover and the foreground over
it, in both themes.
```

### 6.1 Why this is the smallest change

The three menus (`StaffActionsMenu`, `CustomerMenu`, `SpaceActionsMenu`) each render `<Button variant="ghost"
size="icon">` inside a `TableRow` (`data-slot="table-row"`); `CustomerMenu` is also drawn outside a table (the
customer's file), where nothing must change. So one class string in the ghost variant, scoped to a row by an
arbitrary variant, covers all three, and nothing outside a row. Semantic token only (`hover-on-muted`), both themes
(the token is themed). Specificity: `[data-slot=table-row] .x:hover` (0,3,0) beats `.hover\:bg-hover:hover` (0,2,0),
and `[data-slot=table-row] .x[aria-expanded="true"]` beats `.aria-expanded\:bg-hover[…]`, whatever their order in the
CSS (foundation §5: never by Tailwind's order).

### 6.2 Tests first

**a. `apps/web/src/shared/design-system/components/actions/Button/Button.component.test.tsx`** — after the test
`'underlines the link variant at rest, not only under the pointer'`, add:

```tsx
  it('hovers, and marks its open menu, with the ink’s wash inside a table row, when ghost', () => {
    render(<Button variant="ghost">More</Button>);

    expect(screen.getByRole('button', { name: 'More' })).toHaveClass(
      '[[data-slot=table-row]_&]:hover:bg-hover-on-muted',
      '[[data-slot=table-row]_&]:aria-expanded:bg-hover-on-muted',
    );
  });

  it.each(['primary', 'secondary', 'outline', 'destructive', 'link'] as const)(
    'keeps the %s variant’s hover inside a table row',
    (variant) => {
      render(<Button variant={variant}>Save</Button>);

      expect(screen.getByRole('button', { name: 'Save' }).className).not.toMatch(/table-row/);
    },
  );
```

*Break:* the first fails before the code.

**b. `apps/web/src/shared/design-system/tokens/semantic.unit.test.ts`**:
- `GROUNDS`: `'hover-on-muted': ['muted'],` → `'hover-on-muted': ['muted', 'hover'],` and in the comment above it,
  `the wash over the muted track,` → `the wash over the muted track and over a hovered table row,`
- `TEXT_PAIRS`: after `{ text: 'foreground', surface: 'hover-on-muted', over: 'muted', minimum: TEXT },` add
  `{ text: 'foreground', surface: 'hover-on-muted', over: 'hover', minimum: TEXT },`
- `FILLS`: after `{ fill: 'hover-on-muted', ground: 'muted', minimum: SEEN },` add
  `// A ghost control inside a hovered table row (finding 226).` and
  `{ fill: 'hover-on-muted', ground: 'hover', minimum: SEEN },`

These measure the tokens as they are, so they pass before and after. **Check:** if
`light: hover-on-muted stands apart from hover at 1.2:1` fails without any break (the planner's estimate is 1.21:1),
**stop and report** — the token's value is the owner's decision; never change it. *Break:* in
`apps/web/src/shared/design-system/tokens/semantic.css`, the light theme's
`--hover-on-muted: color-mix(in oklab, var(--neutral-900) 10%, transparent);` → `… 2%, transparent);`; the new fill
pair fails (the old one too); restore `10%`.

### 6.3 The code — `apps/web/src/shared/design-system/components/actions/Button/Button.tsx`

- The comment above `buttonVariants` (its eight lines, from `// A hover never fades a fill` to
  `// the focus order, looks disabled too.`) becomes:

```ts
// A hover never fades a fill: fading primary to 90% would leave its label below AA. The ink's
// hover is a role of its own (`primary-hover`); secondary and destructive mix their fill toward
// the foreground, which raises the contrast with the label in both themes. Outline and ghost
// hover, and mark their open menu, with the neutral `hover` fill, never the selected tint. A ghost
// inside a table row, which already takes `hover` under the pointer and while its menu is open,
// takes the ink's wash (`hover-on-muted`) instead: its rule names the row, so it outweighs the
// plain hover by specificity, never by the order Tailwind emits them in. The outline variant is
// edged like a card, so the edge stays visible in the dark theme, where the plain border is faint.
// The link variant is underlined at rest, as a link in running text is: in ink, it would read as
// text. A button marked `aria-disabled`, which waits but keeps its place in the focus order, looks
// disabled too.
```
- The `ghost` variant becomes:

```ts
        ghost:
          'text-foreground hover:bg-hover hover:text-hover-foreground aria-expanded:bg-hover aria-expanded:text-hover-foreground [[data-slot=table-row]_&]:hover:bg-hover-on-muted [[data-slot=table-row]_&]:aria-expanded:bg-hover-on-muted',
```

The text keeps `hover-foreground`, which is `foreground`'s value: the colour a control's text takes over the wash.

### 6.4 Breaks

| Test | Break | Restore |
|---|---|---|
| `hovers, and marks its open menu, …` | delete the two `[[data-slot=table-row]_&]:…` classes | put them back |
| the new token pairs | §6.2's 2 % break | `10%` |

### 6.5 Commit and gate

```powershell
npx prettier --write apps/web/src/shared/design-system/components/actions/Button/Button.tsx apps/web/src/shared/design-system/components/actions/Button/Button.component.test.tsx apps/web/src/shared/design-system/tokens/semantic.unit.test.ts
git add apps/web/src/shared/design-system/components/actions/Button/Button.tsx apps/web/src/shared/design-system/components/actions/Button/Button.component.test.tsx apps/web/src/shared/design-system/tokens/semantic.unit.test.ts
git status
git commit -F C:\dev\masaha\workspace\TASKS\CONTACT_RULES\scripts\msg-3.txt
```

`git status` must not show `semantic.css` (the break was restored). **Gate:** lint; typecheck; Prettier check on the
three files; `node $H cr npm run check:classes`; then

```powershell
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run test:unit -w @masaha/web -- src/shared/design-system/tokens
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run test:component -w @masaha/web -- src/shared/design-system/components/actions/Button src/shared/design-system/components/data src/features/staff src/features/desk/components/menu src/features/spaces/components/menu
```

Then take the captures, §8.

---

## 7. The data count (read-only; after commit 2, before any API is started)

Write this file with your file tool (ASCII only) to
`C:\dev\masaha\workspace\TASKS\CONTACT_RULES\scripts\count-refused.sql`:

```sql
-- CONTACT_RULES: the stored contacts the new rules (C3) would refuse. Read-only: it counts, it changes nothing.
SET default_transaction_read_only = on;
WITH input AS (
  SELECT 'data'::text AS source, sc.type::text AS type, sc.value,
         s.deleted_at IS NOT NULL AS space_deleted, NULL::boolean AS expected
  FROM space_contacts sc JOIN spaces s ON s.id = sc.space_id
  UNION ALL
  SELECT 'self-test', t.type, t.value, false, t.expected
  FROM (VALUES
    ('WEBSITE', 'https://masaha.ps', false),
    ('WEBSITE', 'https://masaha.ps/about?lang=ar', false),
    ('WEBSITE', 'https://0.0.0.123', true),
    ('WEBSITE', 'https://35.181.230.0', true),
    ('WEBSITE', 'https://localhost:5173/x', true),
    ('WEBSITE', 'https://example', true),
    ('OTHER', 'https://discord.gg/focushub', false),
    ('OTHER', '+970599123456', false),
    ('OTHER', 'https://10.0.0.1', true),
    ('FACEBOOK', 'https://www.facebook.com/masaha.gaza', false),
    ('FACEBOOK', 'https://www.facebook.com/profile.php?id=100012345', false),
    ('FACEBOOK', 'https://www.facebook.com/people/Masaha-Hub/100012345678', false),
    ('FACEBOOK', 'https://www.facebook.com/watch', true),
    ('FACEBOOK', 'https://www.facebook.com/masaha/videos/123', true),
    ('FACEBOOK', 'https://www.facebook.com/photo.php', true),
    ('FACEBOOK', 'https://www.facebook.com/groups/gazafreelancers', true)
  ) AS t(type, value, expected)
), parsed AS (
  SELECT input.*,
    lower(substring(value FROM '^https?://([^/?#:]+)')) AS host,
    coalesce(rtrim(substring(value FROM '^https?://[^/?#]+(/[^?#]*)'), '/'), '') AS path
  FROM input
), judged AS (
  SELECT parsed.*,
    CASE
      WHEN type = 'WEBSITE' OR (type = 'OTHER' AND value NOT LIKE '+%') THEN
        host IS NULL
        OR host !~* '^([a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?\.)+([a-z]{2,63}|xn--[a-z0-9-]{1,59})$'
      WHEN type = 'FACEBOOK' THEN NOT (
        value ~ '^https://www\.facebook\.com/profile\.php\?id=[0-9]+$'
        OR path ~* '^/people/[^/]+/[0-9]+$'
        OR (path ~* '^/[a-z0-9_.-]+$'
            AND lower(path) NOT IN ('/watch', '/reel', '/reels', '/video', '/videos', '/post', '/posts',
              '/groups', '/events', '/photo', '/photos', '/share', '/sharer', '/search', '/stories',
              '/story', '/hashtag', '/live', '/gaming', '/marketplace', '/pages', '/people', '/permalink')
            AND path !~* '\.php$')
      )
      ELSE false
    END AS refused
  FROM parsed
)
SELECT source, type,
  count(*) AS total,
  count(*) FILTER (WHERE refused) AS refused,
  count(*) FILTER (WHERE refused AND space_deleted) AS refused_on_deleted_spaces,
  count(*) FILTER (WHERE source = 'self-test' AND refused IS DISTINCT FROM expected) AS self_test_mismatches,
  string_agg(value, ' | ' ORDER BY value) FILTER (WHERE refused AND source = 'data') AS refused_values
FROM judged
WHERE type IN ('WEBSITE', 'FACEBOOK', 'OTHER')
GROUP BY source, type
ORDER BY source, type;
```

Run it (it reads `masaha_cr_dev`, the copy; it never touches `masaha_dev`):

```powershell
docker cp C:\dev\masaha\workspace\TASKS\CONTACT_RULES\scripts\count-refused.sql masaha-postgres-1:/tmp/count-refused.sql
docker exec masaha-postgres-1 psql -U masaha -d masaha_cr_dev -v ON_ERROR_STOP=1 -P pager=off -f /tmp/count-refused.sql
docker exec masaha-postgres-1 rm /tmp/count-refused.sql
```

**Read it:** every `self-test` row must show `self_test_mismatches = 0` (the SQL mirrors the TypeScript rule; a
mismatch means the mirror is wrong: report it and do not trust the counts). Copy the `data` rows (type, total,
refused, refused on deleted spaces, the refused values) into the report and the PR's Evidence. **Change nothing**:
a refused stored contact stays as it is; it is refused only when its space's contacts are next saved. Phones are not
counted: they are stored in E.164, which the new rule accepts.

---

## 8. The captures (C5; after commit 3)

Folder: `C:\Users\basel\Downloads\contact-rules-shots\` (never committed). The proof is the design-system showcase's
DataTable, whose rows carry a ghost «⋯» (`RowActions`, `variant="ghost"`) in `TableRow`s: it needs only the web's dev
server, no API and no sign-in.

**a. Start the web dev server and note its PID:**

```powershell
$web = Start-Process -FilePath node -ArgumentList 'C:\dev\masaha\app-cr\node_modules\vite\bin\vite.js' -WorkingDirectory 'C:\dev\masaha\app-cr\apps\web' -RedirectStandardOutput 'C:\dev\masaha\workspace\TASKS\CONTACT_RULES\scripts\web.log' -RedirectStandardError 'C:\dev\masaha\workspace\TASKS\CONTACT_RULES\scripts\web.err.log' -PassThru -WindowStyle Hidden
$web.Id
```

Write the PID into the breaks log. Wait until `(Invoke-WebRequest http://localhost:5337/ -UseBasicParsing).StatusCode`
is 200 (every 2 s, at most 30 times).

**b. Write `C:\dev\masaha\workspace\TASKS\CONTACT_RULES\scripts\shots.mjs`:**

```js
// CONTACT_RULES C5's captures (finding 226): the showcase's DataTable at 1440 px, its first row
// hovered, its ghost «⋯» hovered, and its menu open with the pointer on the menu, in Arabic, light
// and dark; and the «⋯» hovered in English, light and dark. Local headless Chrome over CDP with
// Node's own WebSocket; only the web's dev server on 5337 is needed.
import { spawn } from 'node:child_process';
import { mkdirSync, mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const WEB = 'http://localhost:5337';
const SHOTS = 'C:/Users/basel/Downloads/contact-rules-shots';
const ROW = 'tbody tr[data-slot="table-row"]';
const CELL = `${ROW} td`;
const TRIGGER = `${ROW} button[aria-haspopup="menu"]`;
mkdirSync(SHOTS, { recursive: true });
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const port = 9300 + Math.floor(Math.random() * 600);
const profile = mkdtempSync(join(tmpdir(), 'cdp-'));
const chrome = spawn(CHROME, [
  '--headless=new',
  `--remote-debugging-port=${port}`,
  `--user-data-dir=${profile}`,
  '--no-first-run',
  '--no-default-browser-check',
  'about:blank',
]);
console.log('chrome pid', chrome.pid);

let targets = [];
for (let i = 0; i < 50; i += 1) {
  try {
    targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
    if (targets.some((t) => t.type === 'page')) break;
  } catch {
    /* not up yet */
  }
  await sleep(200);
}
const socket = new WebSocket(targets.find((t) => t.type === 'page').webSocketDebuggerUrl);
await new Promise((resolve) => socket.addEventListener('open', resolve));
let id = 0;
const pending = new Map();
const errors = [];
socket.addEventListener('message', (event) => {
  const message = JSON.parse(event.data);
  if (message.id !== undefined && pending.has(message.id)) {
    const { resolve, reject } = pending.get(message.id);
    pending.delete(message.id);
    if (message.error) reject(new Error(JSON.stringify(message.error)));
    else resolve(message.result);
  } else if (message.method === 'Runtime.exceptionThrown') {
    errors.push(message.params.exceptionDetails.text);
  }
});
const send = (method, params = {}) =>
  new Promise((resolve, reject) => {
    id += 1;
    pending.set(id, { resolve, reject });
    socket.send(JSON.stringify({ id, method, params }));
  });
const evaluate = async (expression) => {
  const result = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.text);
  return result.result.value;
};
const until = async (expression, what, ms = 30000) => {
  const end = Date.now() + ms;
  while (Date.now() < end) {
    try {
      if (await evaluate(expression)) return;
    } catch {
      /* page changing */
    }
    await sleep(150);
  }
  throw new Error(`timed out: ${what}`);
};
const q = (selector) => `document.querySelector(${JSON.stringify(selector)})`;
const centreOf = (selector, scroll) =>
  evaluate(`(() => {
    const element = ${q(selector)};
    if (${scroll ? 'true' : 'false'}) element.scrollIntoView({ block: 'center' });
    const box = element.getBoundingClientRect();
    return { x: Math.round(box.x + box.width / 2), y: Math.round(box.y + box.height / 2) };
  })()`);
const pointer = ({ x, y }) => send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y });
const fills = () =>
  evaluate(`(() => ({
    row: getComputedStyle(${q(ROW)}).backgroundColor,
    trigger: getComputedStyle(${q(TRIGGER)}).backgroundColor,
    expanded: ${q(TRIGGER)}.getAttribute('aria-expanded'),
    theme: document.documentElement.dataset.theme,
    dir: document.documentElement.dir,
  }))()`);

await send('Page.enable');
await send('Runtime.enable');
await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });

const report = [];
async function open(lang, theme) {
  await send('Page.navigate', { url: 'about:blank' });
  await sleep(200);
  await send('Page.navigate', { url: `${WEB}/__showcase/preview/data/data-table?theme=${theme}&lang=${lang}` });
  await until(`!!${q(TRIGGER)}`, `the table (${lang}, ${theme})`);
  await sleep(800);
  await pointer({ x: 1, y: 1 });
  await sleep(200);
}
async function shot(name) {
  await sleep(400);
  const { data } = await send('Page.captureScreenshot', { format: 'png' });
  writeFileSync(`${SHOTS}/${name}.png`, Buffer.from(data, 'base64'));
  report.push({ name, ...(await fills()) });
}
const press = async (type) =>
  send('Input.dispatchKeyEvent', { type, key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 });

try {
  for (const theme of ['light', 'dark']) {
    await open('ar', theme);
    await pointer(await centreOf(CELL, true));
    await shot(`row-hover-ar-${theme}-1440`);
    await pointer(await centreOf(TRIGGER, false));
    await shot(`ghost-hover-ar-${theme}-1440`);
    // Radix opens the menu from the keyboard; then the pointer leaves the row for the menu.
    await evaluate(`${q(TRIGGER)}.focus(); true`);
    await press('keyDown');
    await press('keyUp');
    await until(`${q(TRIGGER)}.getAttribute('aria-expanded') === 'true'`, 'the menu open');
    await pointer(await centreOf('[role="menuitem"]', false));
    await shot(`menu-open-ar-${theme}-1440`);
  }
  for (const theme of ['light', 'dark']) {
    await open('en', theme);
    await pointer(await centreOf(TRIGGER, true));
    await shot(`ghost-hover-en-${theme}-1440`);
  }
} finally {
  console.log(JSON.stringify(report, null, 1));
  console.log('errors', JSON.stringify(errors));
  socket.close();
  chrome.kill();
}
```

**c. Run it through the grant script (a Chrome batch is heavy):**

```powershell
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr node C:/dev/masaha/workspace/TASKS/CONTACT_RULES/scripts/shots.mjs
```

**Read the printed report** (copy it into `4_REPORT.md`):
- `row-hover-*`: `row` is not `rgba(0, 0, 0, 0)`; `trigger` is `rgba(0, 0, 0, 0)` (not hovered).
- `ghost-hover-*`: `trigger` is **not** `rgba(0, 0, 0, 0)` and differs from `row`.
- `menu-open-*`: `expanded` is `"true"`; `trigger` is not `rgba(0, 0, 0, 0)`.
- `theme` and `dir` match the name (`ar` → `rtl`); `errors` is `[]`.
Open each of the eight PNGs and look: the «⋯» shows a wash darker (light) or lighter (dark) than its row. A value
not as above, or a picture that does not show it: write it in the report as unexpected; do not change code for it.

**d. Stop the server by its PID, and check the port:**

```powershell
Stop-Process -Id <the PID from a> -Force
Get-NetTCPConnection -LocalPort 5337 -State Listen -ErrorAction SilentlyContinue
```

The last must print nothing; if it prints a connection, stop its `OwningProcess` by its id (only that one) and check
again. Never stop a process by name.

---

## 9. Commit 4 — C6, tests only (step 5)

**Subject:** `test(web): wait out toast timers, warm lazy routes` (50 characters)

**Body** (`scripts\msg-4.txt`):

```
test(web): wait out toast timers, warm lazy routes

A dismissed toast is removed after a 200 ms timer its unmount does not
clear; fired once a test file's jsdom was gone, it failed CI's
component lane with "window is not defined" (finding 219). The shared
setup now waits that timer out once, after the last test of a file
that drew a toast.

Four site test files rendered lazy routes without paying their first
load in a beforeAll, as testing §3 rule 8 asks (finding 225); each now
warms the modules its tests open.
```

### 9.1 Finding 219 — the reproduction first

**a. Add `apps/web/src/test/toastTeardown.component.test.tsx`:**

```tsx
import { Toaster, toast } from '@shared/design-system';
import { act, render, screen, waitFor } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

// The toast library removes a dismissed toast on a timer its unmount never clears. This file ends
// while that timer still runs, so the component lane's setup (componentSetup.ts) must wait it out
// before the file's jsdom is torn down, or the run fails with `window is not defined` (finding 219).
describe('a toast dismissed as its file ends', () => {
  it('leaves no removal timer running once the environment is gone', async () => {
    render(<Toaster label="Notifications" />);
    act(() => {
      toast('Saved');
    });
    const shown = await screen.findByText('Saved');

    act(() => {
      toast.dismiss();
    });

    await waitFor(() => {
      expect(shown.closest('[data-sonner-toast]')).toHaveAttribute('data-removed', 'true');
    });
  });
});
```

**b. Run it alone, before the fix:**

```powershell
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run test:component -w @masaha/web -- src/test/toastTeardown
```

**Expected:** the test itself passes, then Vitest reports `Unhandled Errors` with `ReferenceError: window is not
defined` (from sonner's timer) and the run exits non-zero. Record it. **Check:** if the run passes cleanly, run it
twice more; if it never fails, record "the teardown race did not reproduce locally" — keep the test and the fix (the
CI run of #143 is the evidence) and say so in the report and the finding's resolution (§11.3, the second wording).

**c. The fix — `apps/web/src/test/componentSetup.ts`:** the `vitest` import becomes
`import { afterAll, afterEach, vi } from 'vitest';`, and the final `afterEach(() => { cleanup(); });` block is
replaced by:

```ts
// The toast library removes a toast it closes (dismissed, or timed out) after a timer of its own,
// 200 ms, which unmounting the toaster does not clear, and that timer sets React state. Fired once the
// file's jsdom is gone, it fails the run with `window is not defined` (finding 219). So a file that
// drew a toast waits that timer out once, after its last test, while its environment still stands.
const TOAST_REMOVAL_MS = 200;
let drewToast = false;

afterEach(() => {
  drewToast ||= document.querySelector('[data-sonner-toast]') !== null;
  cleanup();
});

afterAll(async () => {
  if (!drewToast) return;
  // A file may leave fake timers on; the wait needs the real clock.
  vi.useRealTimers();
  await new Promise<void>((resolve) => {
    setTimeout(resolve, TOAST_REMOVAL_MS + 100);
  });
});
```

Run (b)'s command again: it passes with no unhandled error. *Break (if b reproduced):* delete the `afterAll` block →
the error comes back; restore.

### 9.2 Finding 225 — the four files

In each file below: add `beforeAll` to the `vitest` import (alphabetical: `afterEach, beforeAll, beforeEach, …`),
add `import { warm } from '../../../test/warmLazy';` on the line just before `import { siteRoutes } from '../routes';`,
and add the block just after the last `import` line (before the first comment or function):

**`apps/web/src/pages/site/shell/SiteAccount.component.test.tsx`**

```ts
// The lazy modules its tests open, loaded once before any test waits (src/test/warmLazy.ts).
beforeAll(
  () =>
    warm(
      () => import('./SiteLayout'),
      () => import('./FocusLayout'),
      () => import('../public/home/HomePage'),
      () => import('../auth/SignInPage'),
    ),
  60_000,
);
```

**`apps/web/src/pages/site/auth/changePasswordPage.component.test.tsx`**

```ts
// The lazy modules its tests open, loaded once before any test waits (src/test/warmLazy.ts).
beforeAll(
  () =>
    warm(
      () => import('../shell/FocusLayout'),
      () => import('@features/users'),
      () => import('./ChangePasswordPage'),
      () => import('../shell/SiteLayout'),
      () => import('../public/directory/DirectoryPage'),
      () => import('../public/home/HomePage'),
      () => import('./SignInPage'),
    ),
  60_000,
);
```

**`apps/web/src/pages/site/auth/forgotPasswordPage.component.test.tsx`**

```ts
// The lazy modules its tests open, loaded once before any test waits (src/test/warmLazy.ts).
beforeAll(
  () =>
    warm(
      () => import('../shell/FocusLayout'),
      () => import('./ForgotPasswordPage'),
      () => import('../shell/SiteLayout'),
      () => import('../public/about/AboutPage'),
    ),
  60_000,
);
```

**`apps/web/src/pages/site/auth/resetPasswordPage.component.test.tsx`**

```ts
// The lazy modules its tests open, loaded once before any test waits (src/test/warmLazy.ts).
beforeAll(
  () =>
    warm(
      () => import('../shell/FocusLayout'),
      () => import('./ResetPasswordPage'),
    ),
  60_000,
);
```

(The lists are what each file's tests render: the shell of each path, its page, and the pages they land on —
`/` after a sign-in or a change, `/spaces` and `/login` in the change's tests, `/about` in the forgot page's.)

*Break:* these change no assertion, so the break proves only that each warm-up runs: in one file, change one path to
`'./NoSuchPage'` → that file fails in its `beforeAll` (and typecheck fails); restore. Record it.

### 9.3 Commit and gate

```powershell
npx prettier --write apps/web/src/test/componentSetup.ts apps/web/src/test/toastTeardown.component.test.tsx apps/web/src/pages/site/shell/SiteAccount.component.test.tsx apps/web/src/pages/site/auth/changePasswordPage.component.test.tsx apps/web/src/pages/site/auth/forgotPasswordPage.component.test.tsx apps/web/src/pages/site/auth/resetPasswordPage.component.test.tsx
git add apps/web/src/test/componentSetup.ts apps/web/src/test/toastTeardown.component.test.tsx apps/web/src/pages/site/shell/SiteAccount.component.test.tsx apps/web/src/pages/site/auth/changePasswordPage.component.test.tsx apps/web/src/pages/site/auth/forgotPasswordPage.component.test.tsx apps/web/src/pages/site/auth/resetPasswordPage.component.test.tsx
git status
git commit -F C:\dev\masaha\workspace\TASKS\CONTACT_RULES\scripts\msg-4.txt
```

**Gate:** lint; typecheck; Prettier check on the six files; then

```powershell
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run test:component -w @masaha/web -- src/test src/pages/site/shell/SiteAccount src/pages/site/auth src/shared/design-system/components/feedback/Toast src/features/desk/hooks/edit
```

---

## 10. Step 6 — wait for PROTOTYPE_SPLIT (C7), rebase, commit 5

### 10.1 The bounded wait

PROTOTYPE_SPLIT's branch is `chore/design-archive-out` (expected PR #147). Check:

```powershell
gh pr list --repo Basel-Ghonaim/masaha --state all --head chore/design-archive-out --json number,state,mergedAt
```

- `MERGED`: go to §10.2.
- `OPEN`: read its files once, `gh pr view <its number> --repo Basel-Ghonaim/masaha --json files --jq '.files[].path'`,
  and compare with §11's list. Any path of §11 in its list **other than** `docs/architecture/findings/README.md` and
  `docs/frontend/design-system/foundation.md`: stop and report. Then wait.
- Empty (not opened yet) or `OPEN`: wait. One check is one command:
  `Start-Sleep -Seconds 300; gh pr list --repo Basel-Ghonaim/masaha --state all --head chore/design-archive-out --json number,state,mergedAt`
  (if your tool's time limit is under 5 minutes, use the longest sleep it allows). **At most 48 checks (about 4
  hours).** Still not merged: write `4_HANDOFF_STATE.md` (§1, item 11) with "waiting for PROTOTYPE_SPLIT's merge",
  and stop. Do not push.
- `CLOSED` without a merge: stop and report.

### 10.2 The rebase

```powershell
git branch backup/contact-rules-pre-rebase
git fetch origin
git rebase origin/main
```

A conflict only in `docs/architecture/findings/README.md`: keep both sides' lines (theirs and ours), `git add` it,
`git rebase --continue`. Any other conflict: `git rebase --abort`, stop and report. After the rebase, run the gate's
lint and typecheck once (`main` changed `eslint.config.js` and `checkLinks.ts`).

### 10.3 Commit 5 — the documents C7 held

**Subject:** `docs: resolve findings 217, 218, 219, 225, 226` (46 characters)

**Body** (`scripts\msg-5.txt`):

```
docs: resolve findings 217, 218, 219, 225, 226

Each finding is marked resolved with its resolution, and the index
moves the five to Resolved. Foundation §5, §11 and §12 say the ghost
control's wash inside a table row and the pairs the token test now
verifies. Both files waited for the design archive's PR, which edited
them.
```

**a. Each finding's file** (`docs/architecture/findings/`): its status line becomes
`**Status:** Resolved · **Date:** <its date, unchanged>`, and at its end, after a blank line, its resolution:

- `217-contacts-and-every-phone-refuse-arabic-indic-digits.md`:
  `**Resolution (2026-11-15, #PRNUM):** the owner decided that every phone reads Arabic-Indic and Eastern digits. `normalisePhone` reads its input through `toWesternDigits`, which moved from the web's `shared/lib` to `@masaha/shared/core` so the server reads the same digits, and «وسيلة أخرى» tells a number by its Western digits. `phone.unit.test.ts` types `٠٥٩٩١٢٣٤٥٦` and `۰۵۹۹۱۲۳۴۵۶`; the contacts' Sheet sends `+970599777888` for `٠٥٩٩٧٧٧٨٨٨`, the desk's edit dialog `+970599000304` for `٠٥٩٩٠٠٠٣٠٤`, and the contacts' API stores `+970599123456` for `٠٥٩٩١٢٣٤٥٦`. C2 stands as written.`
- `218-a-websites-bare-number-is-stored-as-an-ip-address-a-facebook-video-link-loses-its-id.md`:
  `**Resolution (2026-11-15, #PRNUM):** a link's host must be a domain with a top-level domain, so a bare number, an IP address, `localhost` or a bare word is refused; a Facebook link must name a page or a profile (a username, `profile.php?id=…`, `/people/<name>/<id>`), so `/watch`, a video, a reel, a post, a group, an event, a photo, a share and a search are refused, and a handle that names one of those sections too. `contacts.unit.test.ts` lists each; the contacts' Sheet refuses `http://10.0.0.1` and `facebook.com/watch?v=1` on their rows and sends nothing; the API answers `invalid_format` for them. Stored contacts are left as they are: one the rules now refuse is refused when its space's contacts are next saved.`
- `219-a-toasts-removal-timer-can-outlive-its-test-files-jsdom.md` — the first wording if §9.1 (b) reproduced the
  error, else the second:
  `**Resolution (2026-11-15, #PRNUM):** the component lane's setup (`apps/web/src/test/componentSetup.ts`) notes after each test whether a toast was drawn, and a file that drew one waits out the toast library's 200 ms removal timer once, after its last test, while its jsdom still stands. `src/test/toastTeardown.component.test.tsx` ends with that timer running: without the wait it failed with `window is not defined`.`
  — second wording: the same, ending instead `…ends with that timer running; the race did not reproduce locally, so CI's repeated component runs are its evidence.`
- `225-four-site-test-files-render-lazy-routes-without-the-warm-up.md`:
  `**Resolution (2026-11-15, #PRNUM):** each of the four files warms the modules its tests open in a `beforeAll` with a 60 s timeout (`warm(...)`), as [testing §3](../../development/testing.md#3-rules-that-bind-every-test) rule 8 says.`
- `226-a-ghost-control-inside-a-hovered-table-row-has-no-hover-of-its-own.md`:
  `**Resolution (2026-11-15, #PRNUM):** the owner decided the ink's wash. A ghost button inside a table row hovers, and marks its open menu, with `hover-on-muted` over the row's `hover`, in both themes (`Button.tsx`, by a rule that names the row and so outweighs the plain hover by specificity). `semantic.unit.test.ts` checks the wash seen from `hover` and `foreground` over it in both themes; `Button.component.test.tsx` checks the classes.`

**b. `docs/architecture/findings/README.md`:** delete the five lines `- [217. …]`, `- [218. …]`, `- [219. …]`,
`- [225. …]`, `- [226. …]` from `## Open`, and insert the same five lines, unchanged, into `## Resolved` in ascending
number order (217, 218, 219 after the line of the highest number below 217; 225, 226 after the line of the highest
number below 225). Check with `git diff`: five lines removed, five added, nothing else.

**c. `docs/features/spaces.md`** — *Open findings*: delete the two lines for 217 and 218.

**d. `docs/frontend/design-system/foundation.md`** (match the text, not line numbers; each must occur once):
1. §5's role table: `| The hover of a control drawn on a `muted` or `secondary` ground: an ink wash, where an opaque fill would vanish |`
   → `| The hover of a control drawn on a `muted` or `secondary` ground, and of a ghost control inside a hovered table row: an ink wash, where an opaque fill would vanish |`
2. §5's *Verified*: `` `foreground` on `hover-on-muted` over `muted`; `` → `` `foreground` on `hover-on-muted` over `muted` and over `hover`; ``
3. §5's *Fills seen*: `` `hover-on-muted` from `muted`, `` → `` `hover-on-muted` from `muted` and from `hover`, ``
4. §11: `never `accent`, which means selected (§5; `check:classes` refuses it, §3); on a `muted` or `secondary` ground, with `hover-on-muted`.`
   → `never `accent`, which means selected (§5; `check:classes` refuses it, §3); on a `muted` or `secondary` ground, with `hover-on-muted`; a ghost control inside a table row, which already takes `hover`, hovers and marks its open menu with `hover-on-muted` over it.`
5. §12's Table row: `a row takes `hover` when hovered and while its row menu is open, never the selected tint`
   → `a row takes `hover` when hovered and while its row menu is open, never the selected tint, and a ghost control in it (the row's «⋯») hovers, and marks its open menu, with `hover-on-muted` over it`
6. The header's `**Last Updated:**` → `2026-11-15`.

If a text is not found exactly once, stop and report (the merged PR may have changed it).

**e. Commit, and the documents' gate** (no code in this commit):

```powershell
git add docs/architecture/findings/217-contacts-and-every-phone-refuse-arabic-indic-digits.md docs/architecture/findings/218-a-websites-bare-number-is-stored-as-an-ip-address-a-facebook-video-link-loses-its-id.md docs/architecture/findings/219-a-toasts-removal-timer-can-outlive-its-test-files-jsdom.md docs/architecture/findings/225-four-site-test-files-render-lazy-routes-without-the-warm-up.md docs/architecture/findings/226-a-ghost-control-inside-a-hovered-table-row-has-no-hover-of-its-own.md docs/architecture/findings/README.md docs/features/spaces.md docs/frontend/design-system/foundation.md
git status
git commit -F C:\dev\masaha\workspace\TASKS\CONTACT_RULES\scripts\msg-5.txt
```

Gate: `node $H cr npm run format:check` and `node $H cr npm run check:links` (the workflow's rule for a commit with no
code). The full verification follows at once.

---

## 11. The files (the whole list; anything else changed is out of scope)

1. Commit 1 (21): `packages/shared/src/core/digits.ts` (renamed from `apps/web/src/shared/lib/numbers/westernDigits.ts`),
   `packages/shared/src/core/digits.unit.test.ts` (renamed from `…/westernDigits.unit.test.ts`),
   `packages/shared/src/core/index.ts`, `packages/shared/src/core/phone.ts`, `packages/shared/src/core/phone.unit.test.ts`,
   `packages/shared/src/spaces/contacts.ts`, `packages/shared/src/spaces/contacts.unit.test.ts`,
   `apps/web/src/shared/lib/index.ts`, `apps/web/src/shared/lib/money/shekels.ts`,
   `apps/web/src/shared/lib/numbers/wholeNumber.ts`, `apps/web/src/features/packages/services/packageValues.ts`,
   `apps/web/src/shared/map/services/coordinates.ts`,
   `apps/web/src/features/spaces/components/contacts/ContactsSheet.component.test.tsx`,
   `apps/web/src/features/desk/hooks/edit/useEditDialog.component.test.tsx`,
   `apps/api/src/modules/spaces/contacts/contacts.api.test.ts`, `docs/architecture/data-model.md`,
   `docs/frontend/architecture.md`, `docs/features/spaces.md`, `docs/features/customers.md`, `docs/features/desk.md`,
   `docs/features/platform-settings.md`.
2. Commit 2 (6, all already in 1): `contacts.ts`, `contacts.unit.test.ts`, `ContactsSheet.component.test.tsx`,
   `contacts.api.test.ts`, `data-model.md`, `spaces.md`.
3. Commit 3 (3): `apps/web/src/shared/design-system/components/actions/Button/Button.tsx`, its
   `Button.component.test.tsx`, `apps/web/src/shared/design-system/tokens/semantic.unit.test.ts`.
4. Commit 4 (6): `apps/web/src/test/componentSetup.ts`, `apps/web/src/test/toastTeardown.component.test.tsx` (new),
   `apps/web/src/pages/site/shell/SiteAccount.component.test.tsx`, and in `apps/web/src/pages/site/auth/`:
   `changePasswordPage.component.test.tsx`, `forgotPasswordPage.component.test.tsx`,
   `resetPasswordPage.component.test.tsx`.
5. Commit 5 (8): the five findings' files, `docs/architecture/findings/README.md`, `docs/features/spaces.md`,
   `docs/frontend/design-system/foundation.md`.

37 distinct files. Check before the push: `git diff --name-status origin/main...HEAD` lists exactly these (two `R`,
one `A`, the rest `M`).

---

## 12. Step 7 — the final verification, then the push

### 12.1 Everything, on the final head, each through the grant script

```powershell
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run lint
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run typecheck
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run format:check
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run check:classes
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run check:links
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run check:conflicts
Set-Location C:\dev\masaha\app-cr; $env:NODE_ENV = 'production'; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run build; Remove-Item Env:NODE_ENV
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run check:build
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run test:unit
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run test:component
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run test:api
```

Record each one's result and its counts (files, tests). After the build, one more check that Tailwind emitted the
row rule: `Select-String -Path C:\dev\masaha\app-cr\apps\web\dist\assets\*.css -Pattern 'data-slot="?table-row"?\]\s*\.'`
must find at least one match; none: stop and report.

**The real run (API):** start it, read its health, stop it by PID:

```powershell
$api = Start-Process -FilePath node -ArgumentList '--import','tsx','--conditions=@masaha/source','--env-file-if-exists=.env','src/server.ts' -WorkingDirectory 'C:\dev\masaha\app-cr\apps\api' -RedirectStandardOutput 'C:\dev\masaha\workspace\TASKS\CONTACT_RULES\scripts\api.log' -RedirectStandardError 'C:\dev\masaha\workspace\TASKS\CONTACT_RULES\scripts\api.err.log' -PassThru -WindowStyle Hidden
$api.Id
```

Every 2 s, at most 30 times: `Invoke-RestMethod http://localhost:3337/health` until it answers; it must report the
database up. Then `Stop-Process -Id <that PID> -Force` and `Get-NetTCPConnection -LocalPort 3337 -State Listen
-ErrorAction SilentlyContinue` must print nothing (else stop its `OwningProcess` by id and check again). The browser
run is §8's.

Any failure: fix it in the commit that introduced it (§3), then rerun **that** check and the gate of the commit; a fix
in code reruns the whole of 12.1. A lane killed for memory: retry once; killed again: stop and report. **No push until
every line above is green.**

### 12.2 Self-review, then `#PRNUM`

- `git diff --name-status origin/main...HEAD` equals §11.
- `git diff origin/main...HEAD | Select-String '^\+.*(console\.log|\.only\(|debugger)'`: nothing.
- `git log --format=%B origin/main..HEAD | Select-String -Pattern 'Co-Authored|Generated with'`: nothing.
- Every subject ≤ 50 characters: `git log --format=%s origin/main..HEAD`.

The number: `gh api "repos/{owner}/{repo}/issues?state=all&per_page=1&sort=created&direction=desc" --jq '.[0].number'`
gives the last number used (Issues and PRs share it); yours is that **plus one** (expected **148** if PROTOTYPE_SPLIT
took 147). Write `C:\dev\masaha\workspace\TASKS\CONTACT_RULES\scripts\prnum.sh` (LF line endings):

```bash
#!/usr/bin/env bash
# Replaces "#<from>" with "#<to>" in the docs of every commit of the branch, each commit's tree on its
# own, so no commit's patch conflicts with another's (a rebase that amends each one did).
set -euo pipefail
from="$1"
to="$2"
cd /c/dev/masaha/app-cr
export FILTER_BRANCH_SQUELCH_WARNING=1
git filter-branch -f --tree-filter \
  "grep -rlZ -e '#${from}\\b' docs | xargs -0 -r sed -i 's/#${from}\\b/#${to}/g'" \
  origin/main..HEAD
git update-ref -d refs/original/refs/heads/fix/contact-rules
if git grep -n "#${from}\\b" -- docs; then echo "#${from} is left"; exit 1; fi
echo "replaced #${from} with #${to}"
```

Then:

```powershell
git -C C:\dev\masaha\app-cr branch backup/contact-rules-pre-prnum
& 'C:\Program Files\Git\bin\bash.exe' C:/dev/masaha/workspace/TASKS/CONTACT_RULES/scripts/prnum.sh PRNUM 148
git -C C:\dev\masaha\app-cr diff backup/contact-rules-pre-prnum HEAD --stat
git -C C:\dev\masaha\app-cr diff backup/contact-rules-pre-prnum HEAD | Select-String '^[-+][^-+]' | Select-String -NotMatch '#148|#PRNUM'
```

(Use the number you computed in place of 148.) The `--stat` must list only `.md` files; the last command must print
nothing (every changed line is a `#PRNUM` → `#148` line). Then `node $H cr npm run format:check` and
`node $H cr npm run check:links` once more.

### 12.3 Push and open the PR — `open-pr`'s steps, written out

1. `git -C C:\dev\masaha\app-cr fetch origin`; `git -C C:\dev\masaha\app-cr status` must say nothing to commit.
2. Write the PR's description to `C:\dev\masaha\workspace\TASKS\CONTACT_RULES\scripts\pr-body.md` (§12.4).
3. Push and open **at once** (so no other PR takes the number):

```powershell
git -C C:\dev\masaha\app-cr push -u origin fix/contact-rules
Set-Location C:\dev\masaha\app-cr; gh pr create --base main --head fix/contact-rules --title "fix: contact rules, findings 217-219, 225, 226" --body-file C:\dev\masaha\workspace\TASKS\CONTACT_RULES\scripts\pr-body.md --assignee '@me' --label fix --label area:web --label area:api --label area:design-system --label area:docs
```

4. Read the number it printed. If it is not the one written: run `prnum.sh 148 <real number>` (the same way, with a
   new backup branch), the same checks as 12.2, then `git push --force-with-lease origin fix/contact-rules`, and edit
   the description's numbers (`gh pr edit <n> --body-file …`).
5. **Wait for CI**, bounded: one check is `Start-Sleep -Seconds 300; gh pr checks <n>`; at most 12 checks. Then
   `gh pr view <n> --json mergeStateStatus,headRefOid` must show `"mergeStateStatus":"CLEAN"` and `headRefOid` equal to
   `git -C C:\dev\masaha\app-cr rev-parse HEAD`.
   - A red check: `gh run list --branch fix/contact-rules --limit 3`, `gh run view <run id> --log-failed`; fix it in
     the commit that introduced it (backup branch first, `--fixup`, `git rebase --autosquash origin/main`), rerun that
     check and the commit's gate locally, `git push --force-with-lease origin fix/contact-rules`, wait again. At most
     two such rounds; a third red: stop and report.
   - `DIRTY` (a conflict with `main`): §10.2's rule (only the findings index: keep both sides; else stop), then the
     gate's lint and typecheck, `format:check`, push with `--force-with-lease`.
   - Still pending after 12 checks: stop and report.
6. **Never merge.** Stop the servers you started (§8 d, §12.1) if any still runs, by PID, and check their ports.

### 12.4 The PR's description (fill the `<…>`; no tool attribution)

```markdown
## Summary
Five findings in one PR, as the owner decided (CONTACT_RULES C1–C9): every phone reads Arabic-Indic and Eastern
digits (217); a website takes only a real domain and a Facebook link only a page or a profile (218), checked in the
browser before any request and enforced by the server; a ghost control inside a hovered table row takes the ink's
wash (226); no toast timer outlives a test file (219); four site test files warm their lazy routes (225).

## Scope
- C1 + C2: `toWesternDigits` moves from the web's `shared/lib` to `@masaha/shared/core`; `normalisePhone` and
  «وسيلة أخرى»'s number test read through it. The forms +970, +972, 00970, 00972 and the local 0 are unchanged.
- C3 + C4: a link's host is a domain with a top-level domain; Facebook takes a username, `profile.php?id=<digits>` or
  `/people/<name>/<id>`.
- C5: `Button`'s ghost variant inside `[data-slot=table-row]`: `hover-on-muted` on hover and while its menu is open.
- C6: the component setup waits out a drawn toast's removal timer after a file's last test; four `beforeAll` warm-ups.

## Acceptance criteria
- [ ] <copy §0.2 of the plan, ticked as proven>

## Out of scope
No schema, migration, dependency, copy or data change. Stored contacts are not rewritten (the count below).

## Change type
fix (web, api, shared, design system, docs)

## Evidence
- Lint, typecheck, format:check, check:classes, check:links, check:conflicts: <each result>.
- Build (`NODE_ENV=production`) and check:build: <result>; the row rule found in the built CSS.
- test:unit <n files / n tests>, test:component <n / n>, test:api <n / n>: all green, on <head sha>.
- Seen failing first: <the breaks log, one line each>.
- Data count on a local copy of the development database (`masaha_cr_dev`; read-only): <type: refused of total, …>;
  self-test mismatches 0.
- Real run: the API's `/health` on 3337 (database up); the showcase in headless Chrome (below).
- Not run: <anything, with why — e.g. the E2E smoke, which runs before a release>.

## Screenshots
Eight captures at 1440 px (the showcase's DataTable): the row hovered, its «⋯» hovered and its menu open, Arabic,
light and dark; the «⋯» hovered in English, light and dark. Below 768 px the rows are cards, not table rows, so the
rule does not apply there. Attached by the owner from `Downloads\contact-rules-shots`.

## Definition of Done checklist
- [ ] Acceptance criteria met, scope kept (37 files, listed in the commits)
- [ ] Lint and typecheck clean; build passes
- [ ] Tests in the owning lanes, each seen failing first
- [ ] No hardcoded user-facing text (no copy changed)
- [ ] UI checked: RTL and LTR, light and dark, desktop (phone: not a table row)
- [ ] Authorization unchanged; the server enforces the shared rules
- [ ] Documents updated in the same PR; the findings resolved and the index moved
- [ ] Each claim names its test or command
- [ ] Atomic history (5 commits), pushed

More than 25 files: a separate review conversation (workflow §2, phase 7).
```

---

## 13. Step 8 — `4_REPORT.md` (once CI is green on the pushed head and GitHub shows `CLEAN`)

Before writing: the early conflict check — `gh pr list --state open --json number,headRefName`; for each other open
PR: `git -C C:\dev\masaha\app-cr fetch origin <its branch>` and
`git -C C:\dev\masaha\app-cr merge-tree --write-tree HEAD origin/<its branch>`; note "clean" or the files in conflict.

Save `C:\dev\masaha\workspace\TASKS\CONTACT_RULES\4_REPORT.md` with these sections, in order:

1. The PR (number, URL) and its head (the full SHA).
2. The commits (`git log --oneline origin/main..HEAD`).
3. What was run, with the counts per lane, and what was not, with why.
4. The breaks made, and the tests seen failing first (the breaks log).
5. The data count (§7): the `data` rows and the self-test result.
6. The captures (§8): the eight file names and the printed report.
7. The problems met, and how each was solved.
8. **Anything that behaved unexpectedly, even unsolved** (e.g. §9.1 b not reproducing, a capture value not as
   expected, a lane's flake).
9. The early conflict check: each open PR and its result.
10. Each departure from this plan, with its reason (none is allowed without a stop; list the stops).
11. Observations for the owner (record only; not built): the customers' search reads a whole phone typed in
    Arabic-Indic digits as a phone, but a phone's last digits typed so are searched as a name
    (`apps/api/src/modules/customers/customerSearch.ts`, `/^\d{2,}$/`), and the desk's search of the people present
    likewise; a finding needs a number from the owner's range.

Then stop. Leave the worktree, its branch, its backups and its databases for the supervisor.

---

## 14. For the owner, before the launch (the plan's own decisions; each can be reversed)

1. **The reader's home** (departure 4): `toWesternDigits` in `@masaha/shared/core`. Alternative: keep it in the web
   and add a second copy in `core` — two homes for one rule; rejected.
2. **Facebook's username is one segment.** `facebook.com/masaha/about` (a page's tab) is refused, not cut to
   `/masaha`. Alternative: keep the first segment when the rest is a known page tab (`about`, `reviews`, `photos`
   would then need care). Recommendation: strict, as C3 lists the accepted forms.
3. **A domain's labels** are letters, digits and inner dashes: a host with an underscore (rare, never a registrable
   name) is refused.
4. **No copy change.** Facebook's refusal keeps «اسم الصفحة أو الرابط غير صحيح». Alternative: name what is accepted
   («رابط صفحة أو حساب، لا منشور أو فيديو») — a copy decision for the owner.
5. **C5 by specificity** in the ghost variant (one class string), not a new variant or a `Table` change: the smallest
   change that leaves `CustomerMenu` outside a table as it is.

### Review Focus (inputs no planned test exercises)

- An internationalised domain (`مساحة.فلسطين`), stored in its `xn--` form by the URL parser.
- A Facebook page's legacy `/pages/<name>/<id>` link (refused now) and a page's tabs (`/masaha/about`).
- Pasted text with right-to-left marks (U+200F, U+061C) around a phone: not a separator the rule drops.
- The platform's WhatsApp and the desk's debt and payment dialogs typed in Arabic digits: covered by the rule's unit
  tests and `usePhoneOwner`'s use of `phoneSchema`, not by a test of their own.
- The wash over a hovered row on a real screen (the staff list, the customers, the spaces list), signed in.
