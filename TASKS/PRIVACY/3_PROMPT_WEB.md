# PRIVACY — the privacy page in the web app (one PR; launch only after the prototype PR is merged)

You are **worker A** in `C:\dev\masaha\app` (web **5320**, API **3320**, `masaha_dev` / `masaha_test`), in Claude
Code. You build the public page
**«سياسة الخصوصية» / "Privacy Policy"** at `/privacy` in the web app, **exactly as the merged prototype
`docs/design/prototype/Privacy.html` shows it**, link it from the site footer and from Register, update the documents,
fix one stale fact (the online cron's interval), and open one pull request. **Everything you need is in this file.**
Merging to `main` deploys to production, so the owner merges, never you.

## 0. Rules

- **This IS a Work Item:** follow `CLAUDE.md` and `docs/development/workflow.md` — but do **not** run any
  `start-work-item`, `write-plan` or other skill.
- **Plan first, then go on without waiting:** before any edit, write `C:\dev\masaha\workspace\TASKS\PRIVACY\
  4_PLAN_WEB.md` — the files you will add and change, where each piece belongs by `docs/frontend/architecture.md`,
  the tests you will add. Then build. Decide by the safest option, record each decision in the report.
- **Web only:** **no change under `apps/api/` or `packages/shared/`** (the page reads the platform's contact through
  what the web already has). No migration, no new dependency.
- **No stop, no question** until the PR is open, CI is green on its head, it is `CLEAN`, the report is written and
  the final reply sent. You run the local verification yourself (§4).
- **`masaha_dev` holds the owner's presentation demo** (two months of data, photos in `apps/api/.storage`): never
  reset, seed, migrate or write it, and never delete `.storage`. This task needs no database: the web's lanes run
  without one; `test:api` is left to CI (§4).
- Never touch production, `C:\dev\masaha\app-b` or any other worktree. No `git add -A` / `.`; no tool attribution;
  never print a secret; never merge. Stop every server you start by its process id.

## 1. Base and branch

```
git fetch origin
git status --short          # must be clean
git switch main
git pull --ff-only          # main at b0682fd6 (#134) or later
git switch -c feat/privacy-page
```

The lockfile has not moved since the last `npm ci` here; run `npm run build -w @masaha/shared` once.

Confirm `docs/design/prototype/Privacy.html` exists on this base (the prototype PR is merged). If it does not, stop
and say so — nothing else.

## 2. What to build

1. **Read first:** `docs/design/prototype/Privacy.html` (the design to match — layout, spacing, the date line, the
   contact line, the footer and Register links in `docs/design/prototype/masaha/shared.jsx` and the prototype's
   Register screen); `docs/frontend/architecture.md`; `docs/frontend/design-system/foundation.md` §13 (screen 33);
   the About page, the closest model: `apps/web/src/pages/site/public/about/AboutPage.tsx` and its test; the site's
   routes `apps/web/src/pages/site/routes.tsx` and navigation `apps/web/src/pages/site/navigation.ts`; the copy
   catalogue `apps/web/src/shared/copy/` (`arabic/`, `english/`, `catalogues.ts`); the page titles
   (`apps/web/src/app/pageTitles.unit.test.ts` and what it tests); `RegisterPage.tsx`
   (`apps/web/src/pages/site/auth/`); the platform contact the About page shows
   (`apps/web/src/features/platform-settings/public.ts`).
2. **The page** `/privacy`, public (no sign-in), lazy-loaded like the other site pages, in the site shell: the title,
   «آخر تحديث: …» / "Last updated: …" with the date **of this PR's merge — write `2026-11-05`** (the owner sets the
   real date in review if it differs), then every section of the approved text (§7), headings and paragraphs and
   bullet lists, bold where the text is bold. The last section's contact email comes from the platform's public
   contact, the way About shows it (its loading and its "no contact set" cases handled as About handles them).
3. **All text in the copy catalogue,** Arabic and English, **word for word from §7** — no rewording, no sentence
   added or dropped. No string in a component. The page's `<title>` in both languages, as every page has.
4. **The links:** «سياسة الخصوصية» / "Privacy Policy" in the site footer, beside the existing links, as the
   prototype's footer has it; and under Register's submit button one small muted line «اقرأ سياسة الخصوصية» /
   "Read the privacy policy" linking to `/privacy`, as the prototype's Register shows. Nothing else on either.
5. **Design system only:** semantic tokens and the design system's components; no colour, font or arbitrary value
   outside it; logical sides only (`check:classes` enforces it). Readable text column, RTL in Arabic, LTR in English.
6. **Tests** (component lane, `*.component.test.tsx`), modelled on About's: the page renders its title and every
   section heading in Arabic and in English; the contact email shows from the platform contact; the footer link and
   the Register link point to `/privacy`; the route is public. Each test written to fail before its code (note the
   red line). No production code that only a test uses.
7. **Documents:** `docs/project/overview.md` — *Built*: the privacy page, linked from the footer and Register
   (2026-11-05); the feature document the page belongs to under `docs/features/` (the About page's capability, or the
   one the architecture names) — one short line; nothing claims more than is built.
8. **The cron's interval (its own commit):** the online cron now runs **every 60 minutes**, not 15 (the owner's
   decision, 2026-11-04, while the site is not launched: fewer database wake-ups; a late run never corrupts data,
   the auto check-out records its due cut-off). Change every document that says the online cron runs every 15
   minutes: `docs/development/setup.md` (*Timed jobs* and *The deployment*), `docs/architecture/decisions/
   0014-deployment.md` (one new *Revised* line, 2026-11-04; the decision unchanged), `docs/backend/conventions.md`
   §12's table, `docs/api/api-contract.md` (*Internal*), and finding 213 (a dated note: 60 minutes since 2026-11-04,
   to revisit at launch). Find them with `git grep -n "15 minutes"` and read each hit — change only the cron's.
   `apps/api/src/server.ts`'s comment says 15 too: change that comment only (no code). The local timer stays 5.

## 3. Commits

Conventional Commits, subject ≤ 50 characters, each with a body, atomic. For example:
1. `feat(web): add the privacy page` — the route, the page, the copy, its tests.
2. `feat(web): link the privacy page` — footer and Register, their tests.
3. `docs: record the privacy page as built` — overview and the feature document.
4. `docs: run the online cron every 60 minutes` — the cron documents and the comment.

## 4. The local verification — by you, before the push

While building, run only the test files your change touches. When all four commits are made, run, on the branch's
head, in this order (each in the background where it is long, no command timeout; at most two heavy runs at once,
each with at least 4 GB free; a run killed for memory: re-run it once, then in parts, until every file ran green):

```
npm run format:check
npm run lint
npm run typecheck
npm run check:classes
npm run check:links
npm run check:conflicts
npm run test:unit
npm run test:component
$env:NODE_ENV='production'; npm run build; Remove-Item Env:NODE_ENV
npm run check:build
```

(`test:api` is left to CI: this PR changes no API code — the owner's decision.) Every line green → a quick look:
start the API (`npm run dev -w @masaha/api`) and the web (`npm run dev`), open `http://localhost:5320/privacy` in
headless Chrome (Arabic light 1280 and 390, English 1280, dark 1280), the footer on Home and the line on Register;
screenshots in `C:\dev\masaha\workspace\TASKS\PRIVACY\shots\web\`, each opened and checked (no raw tag, RTL/LTR right,
the contact email shown, nothing overflowing at 390); stop both servers by process id. A failure anywhere → fix it,
**fold the fix into its commit** (`git commit --fixup <sha>`, then `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash
origin/main`, a `backup/privacy-web` branch first), re-run what it touched and the lane it failed in, go on.

## 5. Push and PR

- Just before the push: the next number, `gh api "repos/Basel-Ghonaim/masaha/issues?state=all&per_page=1" --jq
  '.[0].number'` plus one; write it where a document names this PR (same style as other dated lines, e.g.
  `2026-11-05, #<n>`).
- `git push -u origin feat/privacy-page`; `gh pr create --assignee @me --label feat --label area:web --label area:docs
  --title "feat: add the privacy page"`. Description: the page and its route; the links; that the text is the
  owner's approved text, unchanged; the documents; the cron's commit and why; the local verification (each
  command's result line); `test:api` left to CI and why; the screenshots; decisions.
- `gh pr checks <n> --watch` → green; `gh pr view <n> --json mergeStateStatus` → `CLEAN`. A red check: fix, fold,
  push with `--force-with-lease`, watch again. **Never merge** (a merge deploys).

## 6. The report and the final reply

`C:\dev\masaha\workspace\TASKS\PRIVACY\5_REPORT_WEB.md`: the files, the commits, the red/green lines, the local
verification, the screenshots, decisions, anything left out. Reply:

```
Status: READY FOR REVIEW | INCOMPLETE (what, why)
PR: #<n> · head <sha> · CI <green/red> · <CLEAN/not CLEAN> · files <n>
Page: /privacy · matches Privacy.html: yes/no (differences)
Text: identical to the approved text (AR and EN): yes/no
Links: footer yes/no · Register yes/no
Cron docs: <files changed>
Local verification (on <sha>): <each command: pass/fail> · test:api: CI
Screenshots: shots\web — <what you checked>
Decisions: <each, one line>   (or "none")
Report: C:\dev\masaha\workspace\TASKS\PRIVACY\5_REPORT_WEB.md
```

## 7. The approved text (use it exactly; the headings are the section headings)

### 7.1 Arabic (the title: «سياسة الخصوصية»)

**آخر تحديث:** [تاريخ النشر]

#### مقدمة

مساحة منصة تجمع مساحات العمل في قطاع غزة في دليل واحد، وتساعد أصحابها على إدارتها. نحترم خصوصيتك، ونجمع أقل ما نحتاجه لتعمل المنصة. توضح هذه الصفحة ما نجمعه، ولماذا، ومن يراه، وكيف نحميه.

#### البيانات التي نجمعها

- **عند إنشاء حساب:** اسمك، وبريدك الإلكتروني، وكلمة المرور، ولغة الواجهة التي تختارها. لا نحفظ كلمة المرور كما هي أبدًا، بل نحفظها مشفّرة بطريقة لا يمكن عكسها.
- **عند الدخول بحساب Google:** نتلقى من Google اسمك وبريدك ومعرّف حسابك فقط. لا نصل إلى كلمة مرورك في Google، ولا إلى أي بيانات أخرى في حسابك.
- **ما تضيفه بنفسك:** المساحات التي تحفظها في المفضّلة، والبلاغات التي ترسلها عن معلومات مساحة، والردود عليها.
- **لأصحاب المساحات وموظفيهم:** معلومات المساحة وصورها، وما يسجّلونه عن زبائنهم: الاسم، ورقم الجوال، والزيارات، والاشتراكات، والدفعات. تحفظ مساحة هذه البيانات نيابةً عن المساحة، ولا يراها إلا طاقمها.

#### ما لا نجمعه

- **موقعك الجغرافي لا يُحفظ:** عند استخدام «الأقرب إليّ» يُقرَّب موقعك على جهازك (إلى نحو 100 متر)، ويُرسَل فقط لترتيب المساحات حسب المسافة، ثم لا يُحفظ ولا يُسجَّل.
- **لا بيانات دفع:** لا يوجد دفع إلكتروني في مساحة في الوقت الحالي، ولا نطلب بطاقة بنكية أبدًا. الدفعات تُسجَّل يدويًا لدى المساحة.
- **لا تتبّع ولا إعلانات:** لا نستخدم أدوات تحليل أو تتبّع أو إعلانات من أي طرف ثالث.
- **الصور بلا بيانات مخفية:** قبل حفظ أي صورة نزيل منها كل البيانات المخفية، مثل موقع التصوير ونوع الكاميرا.

#### كيف نستخدم بياناتك

- لتشغيل حسابك وإبقائك مسجّلًا للدخول.
- لعرض دليل المساحات، وحفظ مفضّلتك، ومتابعة بلاغاتك.
- لتشغيل لوحة التحكم لأصحاب المساحات وموظفيهم.
- لإرسال رابط استعادة كلمة المرور إلى بريدك عندما تطلبه.
- لحماية الحسابات من محاولات الدخول المتكررة.

لا نبيع بياناتك، ولا نشاركها مع أي جهة لأغراض تسويقية.

#### ملفات تعريف الارتباط (Cookies) والتخزين في المتصفح

نستخدم ملفات تعريف ارتباط ضرورية فقط، لإبقائك مسجّلًا للدخول بأمان. ويحفظ متصفحك بعض تفضيلاتك، مثل اللغة والمظهر (فاتح أو داكن). لا نستخدم أي ملفات تعريف ارتباط للتتبّع أو الإعلانات.

#### من يرى بياناتك

- **أنت:** ترى بيانات حسابك ومفضّلتك وبلاغاتك.
- **طاقم المساحة:** يرى صاحب المساحة وموظفوه ما يخص مساحتهم فقط، ولا يرون شيئًا عن مساحات أخرى.
- **البلاغات:** يصل بلاغك عن مساحة إلى صاحبها **دون اسمك**.
- **فريق مساحة:** لإدارة المنصة والرد على البلاغات وتقديم الدعم.

#### كيف نحمي بياناتك

- كلمات المرور مشفّرة، ولا يطّلع عليها أحد، ولا حتى فريقنا.
- صلاحيات كل مستخدم تُفحص على الخادم في كل طلب.
- تنتهي جلسة الدخول تلقائيًا بعد مدة محددة، وتنتهي جلسة موظف الاستقبال بعد فترة دون استخدام.
- نحدّ من محاولات الدخول المتكررة، ونستخدم عنوان الشبكة (IP) لهذا الغرض مؤقتًا فقط.

#### مدة الاحتفاظ بالبيانات

- يبقى حسابك ما دام فعّالًا. عند طلب إيقافه، **يُوقَف الحساب ولا يُحذف** في النسخة الحالية من مساحة.
- السجلات المالية وسجل التدقيق محفوظة، لأنها جزء من سجلات المساحات وحساباتها.
- روابط استعادة كلمة المرور والجلسات المنتهية تُحذف تلقائيًا.

#### حقوقك

- يمكنك تعديل اسمك ولغتك وطرق دخولك من «إعدادات حسابي».
- يمكنك أن تطلب إيقاف حسابك، أو أن تسألنا عن بياناتك، عبر التواصل معنا.

#### التغييرات على هذه السياسة

قد نحدّث هذه السياسة عندما تتغيّر المنصة. سنُظهر تاريخ آخر تحديث أعلى الصفحة.

#### تواصل معنا

لأي سؤال عن خصوصيتك: [بريد التواصل].

### 7.2 English (the title: "Privacy Policy")

**Last updated:** [publication date]

#### Introduction

Masaha brings the coworking spaces of the Gaza Strip together in one directory, and helps their owners run them. We respect your privacy and collect only what the platform needs to work. This page explains what we collect, why, who sees it, and how we protect it.

#### What we collect

- **When you create an account:** your name, your email address, your password, and the interface language you choose. We never store your password as it is: we store it encrypted in a way that cannot be reversed.
- **When you sign in with Google:** Google gives us only your name, your email and your Google account ID. We never see your Google password or any other data in your account.
- **What you add yourself:** the spaces you save to your favourites, the reports you send about a space's information, and the replies to them.
- **For space owners and their staff:** the space's information and photos, and what they record about their customers: name, mobile number, visits, subscriptions and payments. Masaha keeps this data on the space's behalf, and only its staff can see it.

#### What we don't collect

- **Your location is never stored:** when you use "Nearest to me", your location is rounded on your device (to about 100 metres) and sent only to sort spaces by distance; it is never stored or logged.
- **No payment data:** Masaha has no online payment at present, and we never ask for a bank card. Payments are recorded by hand at the space.
- **No tracking, no ads:** we use no third-party analytics, tracking or advertising tools.
- **Photos without hidden data:** before a photo is stored, we remove all its hidden data, such as where it was taken and the camera used.

#### How we use your data

- To run your account and keep you signed in.
- To show the directory of spaces, keep your favourites and follow your reports.
- To run the dashboard for space owners and their staff.
- To email you a password reset link when you ask for one.
- To protect accounts from repeated sign-in attempts.

We do not sell your data, and we do not share it with anyone for marketing.

#### Cookies and browser storage

We use only the cookies needed to keep you signed in securely. Your browser also keeps some of your preferences, such as the language and the appearance (light or dark). We use no cookies for tracking or advertising.

#### Who sees your data

- **You:** you see your account, your favourites and your reports.
- **A space's staff:** a space's owner and staff see only what belongs to their space, and nothing about other spaces.
- **Reports:** your report about a space reaches its owner **without your name**.
- **The Masaha team:** to run the platform, answer reports and give support.

#### How we protect your data

- Passwords are encrypted, and no one can read them, not even our team.
- Every user's permissions are checked on the server, on every request.
- Your session ends automatically after a set period, and a reception session ends after a period without use.
- We limit repeated sign-in attempts, and use your network address (IP) for this purpose only, and only temporarily.

#### How long we keep data

- Your account stays as long as it is active. When you ask to close it, **the account is suspended, not deleted**, in the current version of Masaha.
- Financial records and the audit log are kept, because they are part of the spaces' records and accounts.
- Password reset links and ended sessions are deleted automatically.

#### Your rights

- You can change your name, your language and how you sign in from "My account settings".
- You can ask us to suspend your account, or ask us about your data, by contacting us.

#### Changes to this policy

We may update this policy when the platform changes. The date of the last update is shown at the top of this page.

#### Contact us

For any question about your privacy: [contact email].
