# PRIVACY — the prototype's privacy page (one small PR, docs/design only)

You are a worker in `C:\dev\masaha\app-b` (a git worktree of the Masaha repository, detached at `origin/main`). You add
**one new screen, «سياسة الخصوصية» / "Privacy Policy", to the design prototype** in `docs/design/prototype/`, link it
from two places, record it in three documents, and open one pull request. **Everything you need is in this file.**
Work fast and focused: the decisions are all made, the text is final.

## 0. Rules

- **This IS a Work Item:** read `CLAUDE.md` (the repository's rules) and follow them — but do **not** run any
  `start-work-item`, `write-plan` or other skill, and do not wait for approval at any point.
- **Write a short plan first, then go straight on, no stop:** before touching any file, write
  `C:\dev\masaha\workspace\TASKS\PRIVACY\2_PLAN_PROTOTYPE.md` with (a) the exact files you will change or add, (b)
  where the site footer is defined (it should be one shared component — confirm), (c) how you will check your work.
  Then do it. Never stop to ask; decide by the safest option and record the decision in the report.
- **Scope — touch only these:** `docs/design/prototype/Privacy.html` (new), `docs/design/prototype/masaha/shared.jsx`
  (the footer link only), the prototype's Register screen file (one link only), `docs/design/SCREENS.md`,
  `docs/design/CHANGES.md`, `docs/frontend/design-system/foundation.md` (§13 only). **Nothing under `apps/` or
  `packages/`**, no other screen, no screenshots/boards, no `docs/project/overview.md`. If a change outside this list
  seems needed, do not make it: write it in the report.
- **No tests, no install:** do not run `npm ci`, the test lanes (`test:unit`, `test:component`, `test:api`), lint,
  typecheck or a build — this PR changes no application code. The only checks are in §4.
- Never touch the live site, any database, `C:\dev\masaha\app` (the owner's folder) or any other worktree. Never
  print a secret. No `git add -A` / `git add .` — stage by path. No tool attribution anywhere (no `Co-Authored-By`
  of a tool, no "generated with").

## 1. Base and branch

```
git fetch origin
git switch -c docs/privacy-page origin/main
```

## 2. What to build

### 2.1 The page — `docs/design/prototype/Privacy.html`

- **Copy `About.html`'s structure:** the same `<head>` (the same scripts in the same order: `masaha/i18n.js`, the
  vendored React, ReactDOM, Babel, the design-system bundle, the data files it needs, `masaha/shared.jsx`), the same
  `SiteHeader` and `SiteFooter`, the same page width and spacing. Read `About.html` first and mirror it.
- **Layout:** a calm reading page — the title «سياسة الخصوصية» / "Privacy Policy"; under it the line «آخر تحديث:
  …» / "Last updated: …" with a placeholder date; then each section as a heading and its paragraphs and bullet
  lists, exactly as the text in §7 gives them (bold where the text is bold). No table of contents, no cards, no
  icons, no images. Readable line length on desktop (like About's text column).
- **Both languages:** every string through the prototype's `tr("…arabic…", "…english…")` helper (as `About.html` and
  `shared.jsx` do), Arabic from §7.1 and English from §7.2 — **word for word, no rewording, no added or dropped
  sentence**. The page must work with `?lang=en` (LTR) and `?theme=dark`, at 360 and 1280 wide, like every screen.
- **The contact email** in the last section: show it the way `About.html` shows the platform's contact email (the
  same sample data and link style). The «آخر تحديث» date: a fixed sample date, `2026-11-04`.
- **Design system only:** use only the Masaha design-system components and the classes the prototype already uses.
  The prebuilt `_ds_bundle.css` holds **only** the utility classes the prototype already uses, so a new class may
  silently do nothing — copy classes from `About.html` and other pages. No new colours, fonts, sizes, radii, shadows,
  no inline `style`. Logical sides only (`ms-`/`me-`/`ps-`/`pe-`/`start`/`end`), never `left`/`right`/`ml-`/`mr-`/
  `pl-`/`pr-`.
- **The prototype's trap — shared globals:** all `text/babel` scripts on a page share one global scope. **Never
  declare a top-level `const`/`let`/`function` whose name may already exist** in `shared.jsx` or another loaded
  script (e.g. `name`, `_excluded`, `Page`, `App`, `Section`, `links`): a duplicate name breaks the page, or another
  component. Give your page's top-level names a unique prefix (`Privacy…`), or wrap the page in one function.

### 2.2 The two links

- **Footer, every public page:** in `SiteFooter` (`docs/design/prototype/masaha/shared.jsx`), add a link
  «سياسة الخصوصية» / "Privacy Policy" to `Privacy.html`, beside the existing «عن مساحة» and «تواصل معنا» links, same
  style. This one edit puts it on every page that uses the footer.
- **Register screen:** under the register button (the prototype's `Register.html` and the component it loads — find
  where the form is), add one small muted line with a link: «اقرأ سياسة الخصوصية» / "Read the privacy policy" →
  `Privacy.html`. Same muted text style the form already uses for its small lines. Nothing else on that screen
  changes.

### 2.3 The documents

- **`docs/frontend/design-system/foundation.md` §13:** the heading «## 13. Screens to design (32)» becomes «(33)»;
  under *Public site (8)* → «(9)», add at the end of that list a new item numbered **33** (do **not** renumber any
  other screen): `33. **Privacy policy** — what Masaha collects and why, who sees it, how it is protected; linked
  from the footer and from Register (the owner's decision, 2026-11-04)`. Keep the file's existing wording style.
- **`docs/design/SCREENS.md`:** the title says 33 screens; in the *Public site* table add the row
  `| 33 | Privacy policy | \`Privacy.html\` | — |` (no board sections). If the file's first line or any count says
  32, update it to 33.
- **`docs/design/CHANGES.md`:** a new short section at the end, in the file's style: the date (2026-11-04), "the
  privacy page": the new `Privacy.html`, the footer link, the Register link, and that the text is the owner's
  approved text, to be built in the web app in a separate PR.

## 3. Commits

Conventional Commits, each subject ≤ 50 characters, each with a short body, atomic. For example:
1. `docs(design): add the privacy page prototype` — `Privacy.html`.
2. `docs(design): link the privacy page` — the footer and Register links.
3. `docs: list the privacy page as screen 33` — foundation.md, SCREENS.md, CHANGES.md.

## 4. The only checks (all must pass before the push)

From the repository's root:

```
node docs/design/scripts/check-parse.mjs
node docs/design/scripts/check-classes.mjs
npm run check:links
npm run check:conflicts
```

Then **look at the page**: serve the prototype (`cd docs/design/prototype` then `npx serve . -l 5999`, or `python -m
http.server 5999`), and take screenshots with headless Chrome (`"C:\Program Files\Google\Chrome\Application\chrome.exe"
--headless=new --hide-scrollbars --virtual-time-budget=6000 --window-size=1280,2400 --screenshot=<path>
"http://localhost:5999/Privacy.html"`) of: Arabic light 1280, Arabic light 360 (`--window-size=360,3200`), English
1280 (`?lang=en`), dark 1280 (`?theme=dark`); plus `Home.html` 1280 (the footer link) and `Register.html` 1280 (the
new line). Save them in `C:\dev\masaha\workspace\TASKS\PRIVACY\shots\` and **open each one and check it**: the page is
not blank, the text is right-to-left in Arabic and left-to-right in English, nothing overflows at 360, the links show.
Stop the server by its process id.

## 5. Push and PR

- Just before the push, check the next number: `gh api "repos/Basel-Ghonaim/masaha/issues?state=all&per_page=1" --jq
  '.[0].number'` plus one (Issues and PRs share numbers); if any document you wrote names this PR, use that number.
- `git push -u origin docs/privacy-page`; `gh pr create --assignee @me --label docs --label area:docs --title "docs:
  add the privacy page to the prototype"` (≤ 50 characters — recount), with a description: what was added, the two
  links, the three documents, that the text is the owner's approved text (unchanged), the checks and their results,
  the screenshots taken, and anything recorded instead of changed.
- `gh pr checks <n> --watch` until every check is green; then `gh pr view <n> --json mergeStateStatus` shows `CLEAN`.
  A red check: fix it, fold the fix into its commit (`git commit --fixup <sha>` then `GIT_SEQUENCE_EDITOR=: git rebase
  -i --autosquash origin/main`), push with `--force-with-lease`, watch again. **Never merge.**

## 6. The report and the final reply

Write `C:\dev\masaha\workspace\TASKS\PRIVACY\4_REPORT_PROTOTYPE.md`: the files changed, the commits, each check's
result line, the screenshots and what you saw, every decision you took, anything left out. Then reply with:

```
Status: READY FOR REVIEW | INCOMPLETE (what, why)
PR: #<n> · head <sha> · CI <green/red> · <CLEAN/not CLEAN> · files <n>
Files: <list>
Checks: check-parse <ok> · check-classes <ok> · check:links <ok> · check:conflicts <ok>
Screenshots: <n> in TASKS\PRIVACY\shots — <anything wrong seen>
Text: identical to the approved text (AR and EN) — yes/no
Decisions: <each, one line>   (or "none")
Report: C:\dev\masaha\workspace\TASKS\PRIVACY\4_REPORT_PROTOTYPE.md
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
