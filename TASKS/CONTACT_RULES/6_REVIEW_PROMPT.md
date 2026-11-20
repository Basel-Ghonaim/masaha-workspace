# Targeted review of #149 (CONTACT_RULES) — one reviewer, requirement by requirement

You are a **read-only reviewer** of one Masaha PR. **This is not a general review.** You check the twelve requirements
below (R1–R12), each against the code, and report a verdict for each with evidence. Anything outside them is out of
scope — report it only if it breaks one of them. No style opinions, no refactor ideas, no praise.

The launch line gives the PR number, its branch and the head — call the head `<HEAD>` and pin every read to it.

## Rules

- **Read only, commit objects only:** `git show <HEAD>:<path>`, `git diff origin/main...<HEAD>`,
  `git log origin/main..<HEAD>`, `git grep <pattern> <HEAD> -- <paths>`. Fetch once only if `git cat-file -t <HEAD>`
  fails. Never edit, checkout, switch, reset, stash or commit; no npm, tests, servers, database, installs or GitHub
  comments. No sub-agents, no project skill.
- First `gh pr checks <n>`: red or pending → say so and stop. At the end, say whether the head moved.
- **Trace, don't trust:** for each input in a table below, follow it through the actual code (regexes, branches,
  `URL` parsing) and state the result you derive, with `file:line`. When a result depends on a library's behaviour
  (Node's / the browser's `URL`, zod), say which behaviour you rely on. A test's name is not evidence; its assertion is.
- A verdict is **PASS** (built and proved by a test that would fail on its break), **WEAK** (built, but untested or a
  test that cannot fail), **FAIL** (the code does otherwise), or **UNVERIFIABLE** (say why).

## Read first (briefly)

`C:\dev\masaha\workspace\TASKS\CONTACT_RULES\0_OWNER_DECISIONS.md` (C1–C10, binding). Then the diff. Use `2_PLAN.md`
and `4_REPORT.md` only to look something up.

## The requirements

**R1 — one digit reader (C1, C10).** `toWesternDigits` lives only in `packages/shared/src/core/digits.ts`; no copy is
left in `apps/web` (web imports it from `@masaha/shared/core`); it maps Arabic-Indic `٠–٩` (U+0660–0669) and Eastern
`۰–۹` (U+06F0–06F9) to `0–9` and leaves everything else as it is.

**R2 — the phone rule (C1, C2)** in `packages/shared/src/core/phone.ts`. Derive the result of each input:

| Input | Expected |
|---|---|
| `٠٥٩٩١٢٣٤٥٦` | `+970599123456` |
| `۰۵۹۹۱۲۳۴۵۶` | `+970599123456` |
| `+970599123456`, `00970599123456` | `+970599123456` |
| `+972599123456`, `00972599123456` | accepted, stored E.164 as the rule did before this PR |
| `0599123456`, `0569123456` | accepted (local form kept, C2) |
| a local landline (`02…`) if the rule accepted it before this PR | still accepted |
| `+1 202 555 0100`, `05991234`, `abc`, empty | refused as before this PR |

**R3 — every phone goes through R2 (C1).** Each of these reads the phone through the shared rule, on the browser and
on the server: a space's WhatsApp and phone contacts and «وسيلة أخرى» as a number (`spaces/contacts.ts`,
`spaces/requests.ts`, `useContactsSheet.ts`); a customer's phone (`customers/requests.ts`, `customerSearch.ts` for a
whole phone); the desk (`desk/requests.ts`, `useEditDialog.ts`, `usePhoneOwner.ts`); the platform's WhatsApp
(`platform-settings/requests.ts`, `platformContact.ts`). List any phone input that bypasses it.

**R4 — the website rule (C3)** in `packages/shared/src/spaces/contacts.ts`:

| Accepted | Refused |
|---|---|
| `example.ps`, `www.example.com`, `https://masaha.ps/about`, `http://example.com`, `123.ps` | `123`, `10.0.0.1`, `http://10.0.0.1`, `localhost`, `http://localhost:3000`, `masaha`, `http://[::1]`, `ftp://example.com`, `javascript:alert(1)` |

**R5 — the Facebook rule (C3, C10):**

| Accepted | Refused |
|---|---|
| `facebook.com/masaha`, `https://www.facebook.com/Masaha-Space-123456`, `m.facebook.com/masaha`, `facebook.com/profile.php?id=100012345`, `facebook.com/people/Some-Name/100012345` | `facebook.com/watch?v=1`, `facebook.com/watch`, `facebook.com/masaha/videos/1`, `facebook.com/reel/1`, `facebook.com/groups/x`, `facebook.com/events/1`, `facebook.com/photo?fbid=1`, `facebook.com/share/abc`, `facebook.com/search/?q=x`, `facebook.com/masaha/about` (C10: refused, not shortened), `facebook.com/masaha/posts/1`, `facebook.com/profile.php` (no id), `notfacebook.com/masaha` |

Also: «وسيلة أخرى» given an IP link is refused (as the report says), and the Facebook error's copy is unchanged (C10).

**R6 — the browser checks first, the server still enforces (C4).** The contacts' Sheet runs the shared rule and, for
a refused value, shows the error on its row and **sends no request** (find the test that asserts no request); the API
answers `invalid_format` and writes nothing (find the test that asserts nothing stored). The desk's edit dialog does
the same with `phoneSchema`.

**R7 — no data changed.** No migration, no seed or data script changes stored contacts; stored contacts the new rules
refuse are left as they are (the report's data count: none refused in `masaha_cr_dev`).

**R8 — the row's ghost control (C5).** A ghost button inside a hovered table row hovers, and keeps the look while its
menu is open, with `hover-on-muted` over the row's `hover`, in both themes; the rule is scoped to a table row (a ghost
button outside a table, such as `CustomerMenu` outside a table, is unchanged); semantic tokens only, no colour, no
physical direction class, no arbitrary value outside `apps/web/src/shared/design-system/`. Check the token values the
report quotes (light 10 %, dark 8 %) against the CSS.

**R9 — finding 219 (C6).** The toast-timer teardown waits out the library's removal timer only for a file that drew a
toast, while its jsdom stands, and **does not swallow errors or hide failures**.

**R10 — finding 225 (C6).** The four site test files warm their lazy routes in a `beforeAll`, as
`docs/development/testing.md` §3 rule 8 says (read the rule at `<HEAD>`).

**R11 — the tests can fail.** For every row of R2, R4 and R5 and for R6, name the test and line that covers it, or
mark the row **untested**. For each test you name, say whether it would fail if its rule were reverted (the report's
*Breaks log* lists the breaks the executor tried — check a few against the code).

**R12 — the documents state what the code does.** `docs/features/spaces.md` (the two new rules), `customers.md`,
`desk.md`, `platform-settings.md` (their change-log lines), `docs/frontend/design-system/foundation.md` (the row's
wash), findings 217, 218, 219, 225, 226 **Resolved** (file and index) with resolutions true to the code, 228 **Open**
and accurate. Every `#149` in the docs is right; no `#PRNUM` left.

## Output

Write `C:\dev\masaha\workspace\TASKS\CONTACT_RULES\7_REVIEW.md`:

```
# Targeted review of #<n> (CONTACT_RULES)
Head: <HEAD> · checks: <green/red> · head moved: <yes/no>
Verdict: <mergeable | mergeable after a fix round | not mergeable>

## Verdicts
R1 <PASS|WEAK|FAIL|UNVERIFIABLE> — one line, file:line
… R12

## Findings (FAIL and WEAK only, most severe first)
### F1 — <blocker|should-fix|nit> · R<k> · <title>
- Where (file:line at <HEAD>) / What the code does / The input that shows it / Fix, and the commit it folds into
(None → "None.")

## R2, R4, R5 traced (each input: derived result · file:line · test or "untested")

## Not checked, and why
```

Severity: **blocker** = a rule accepts what C1–C3 refuse or refuses what they accept, a rule on one side only (browser
or server), data changed, a test bent to pass; **should-fix** = an untested row, a test that cannot fail, a false
document line; **nit** = anything smaller. Then stop.
