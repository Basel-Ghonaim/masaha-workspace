# The auth pages — three designs, every page, and the lab — the lead's report (2026-11-15)

## للمالك، باختصار

صمّمتُ **ثلاثة تصاميم** لكل صفحات الدخول (تسجيل الدخول، إنشاء حساب، نسيت كلمة المرور، تعيين كلمة مرور جديدة،
تغيير كلمة المرور المؤقتة، ورسالة الاستعادة)، بكل حالاتها، وكلها تلتزم بقرارك A1 وA2: النموذج في جهة البداية
بلا بطاقة، ومن 1280 لوح بلون الحبر عليه الشعار وعنوان وسطر ورسم القطاع، ونقاطه هي المساحات الثلاث عشرة الحقيقية
بالتوتي (لقطة الدليل في 14 نوفمبر 2026).

- **«اللوح» (Slate)** — الأقرب إلى A1 كما كُتب: نصفان متساويان، القطاع مرسوم كاملًا مصمتًا بطول اللوح، والنموذج
  هادئ بمقاسات نظام التصميم (عنوان 30 بكسل) وتنبيهاته المعتادة. بلا حركة. على الهاتف: الشعار والنموذج فقط.
- **«الساحل» (Coast)** — القطاع خطًّا مرسومًا: الساحل يُرسم مرة واحدة عند الفتح ومعه خطّا موج في البحر، أكبر من
  اللوح فيقصّه اللوح. خطّ أكبر (عنوان 40 بكسل)، حقول 48 بكسل، والحالات حافّة ملوّنة لا صناديق. على الهاتف والتابلت
  **شريط بالحبر** أعلى الصفحة يحمل الشعار والخط نفسه فوق نقاط مدينة غزة — الهوية حاضرة بلا إطار حول النموذج.
- **«النقاط» (Dots)** — القطاع مرسومًا بحبيبات صغيرة، والمساحات تضيء بالتوتي من الشمال إلى الجنوب. أعرض لوح وأكبر
  عنوان (54 بكسل)، ونموذج ضيّق دقيق، وشروط كلمة المرور ثلاثة أشرطة قصيرة تمتلئ بالحبر. على الهاتف رسم صغير
  منقّط للقطاع بجانب العنوان.

**توصيتي: «الساحل».** هو الوحيد الذي يحمل الهوية على الهاتف — وأغلب الناس على الهاتف — دون أن يعود إلى الإطار
داخل الإطار، وخطّه المرسوم يقول «غزة» دون أن يدّعي أنه خريطة، والحركة الوحيدة فيه لحظة واحدة تتوقف لمن يطلب ذلك.
«اللوح» هو الخيار الآمن إن أردت الأقرب إلى ما كتبته؛ و«النقاط» أجملها على شاشة كبيرة وأضعفها على الهاتف.

قارن بنفسك في **`Auth lab.html`** (صفحة واحدة: التصميم، الصفحة، الحالة، اللغة، المظهر، العرض، أو «قارن التصاميم»
الأربعة جنبًا إلى جنب)، وكل لقطة في `D:\MASAHA\DT\AUTH\variants\`.

الكلمات الجديدة (عنوان اللوح وسطره، وتعليق الرسم، و«حرف واحد على الأقل، بأي لغة») **مقترحات** تقرّها أنت.

---

## The three designs

Each is a `?v=` variant of the five auth pages (`slate`, `coast`, `dots`), plus a standalone reset e-mail;
the original pages are untouched. One kit (`prototype/variants/_auth/kit.jsx`) holds the page logic,
the states and the Strip, so a state behaves the same in all three and only the design differs; each design
is its stylesheet over a common base. Full specification: `masaha-prototype/decisions/auth.md`.

- **«اللوح» Slate**, closest to A1 as written. Two equal columns, the whole Strip in a solid fill
  (`neutral-800`) the full height of the ink panel, its title and line in the corner the land leaves empty.
  The form uses the design system's own scale (h1 `heading-1`, 30 px) and its alerts; no motion; no Strip below
  1280. Best captures: `1-login-slate-1920-light.png`, `2-register-slate-390-light.png`.
- **«الساحل» Coast**, the Strip as a drawn line. A narrower panel (5 : 7): the outline in one line with two
  offshore echoes, drawn in once (1.4 s, then the dots north to south; off under reduced motion), cropped
  so Gaza City's cluster fills its lower half. Editorial type (h1 40 px, lede 17 px, 48 px controls); states as
  an edge, not a box. Below 1280 an **ink band** carries the logo, the tools and the same line: the phone keeps
  the brand with no frame round the form. Best captures: `1-login-coast-1920-dark.png`,
  `3-forgot-password-coast-390-dark.png`, `6-reset-email-coast-390-light.png`.
- **«النقاط» Dots**, the Strip drawn by its grain. The widest panel (7 : 5): a field of small dots clipped to
  the outline, the spaces lit in the berry north to south; the largest title (54 px). A narrow, precise form
  (380 px, h1 28 px); the password conditions as three short bars; compact tinted states; a small dotted Strip
  beside the h1 below 1280. Best captures: `2-register-dots-1920-light.png`, `1-login-dots-1920-dark.png`.

## How each answers §1

All three, the same way (the kit is one):
- **A1:** from 1280 two columns, the form on the start side with no card, the ink panel at the end with the
  logo, the title, the line and the Strip. The h1 sits at the same height on every page of a design (measured
  at 1920: 200 px Slate, 192 Coast, 208 Dots): no vertical centring. The phone: full width, no card, no frame,
  no line under the header; fields and buttons 52 px.
- **A2:** an inline SVG (about 3 KB), north up, never mirrored; round 3's approximate outline with no
  governorate lines and no names; the dots are the directory's 13 spaces at their coordinates from the live
  API's snapshot of 14 November 2026 (the date is in the drawing's description); the berry on the panel is
  `spark-400`; motion only in Coast and Dots, off under `prefers-reduced-motion`.
- **The identity:** ink + berry; the panel stays the ink in both themes (a hairline at its edge in dark); the
  dark logo on it; the berry marks the spaces, the caption's dot and the address a reset link went to — never
  text, an action or an error.
- **The critique's points:** Google's button in Google's own dark theme with no white frame, the fields' width
  and height (1, 2); forgot password's form at once, the recovery's read a thin bar over it (3); the forced
  change has the language and theme switches beside «تسجيل الخروج» (4); conditions as a tick or a dash (Slate,
  Coast) or bars (Dots), never a circle (5); one fixed offset (6); a real h1 of 26–40 px (7); no frame in a
  frame on the phone (8); the 1920 screen's other half is the panel (9); the berry beyond the logo (10);
  «حرف واحد على الأقل، بأي لغة» (11).
- **Accessibility:** the probe over all 134 captures found, in the variants, no text under AA contrast, no
  horizontal overflow and no text under 12 px. Every control has a visible focus (the tools, Google's button,
  the show-password button, the links); targets are 44 px; errors are tied by the system's `Field`;
  `autocomplete` is production's; a failed submit moves the focus to the first invalid field. Fields are no
  longer greyed out while a sign-in is pending (their labels fell to 3.2 : 1); the button carries the wait.
- **The words** are production's catalogue's (sign-in's line, the forced change's line and the way back
  «العودة إلى الرئيسية» replace the prototype's older ones).

## Proposals against masaha's design system (a masaha decision only if the owner chooses one)

| | Slate | Coast | Dots |
|---|---|---|---|
| **Type** | auth h1 at `heading-1` (30 / 28 px) instead of the card title's 17 px; panel title 40 px | auth h1 40 px (30 on the phone), lede 17 px, labels 15 px; panel title 46 px | auth h1 28 px; panel title 54 px; states 13.5 px |
| **Spacing** | form 400 px, h1 128 px from the top | form 440 px, 120 px | form 380 px, 136 px |
| **Controls** | 44 px desktop, 52 phone | 48 px desktop, 52 phone | 44 px desktop, 52 phone |
| **Surfaces** | the full-height ink panel (new); the system's alerts | the ink panel; the ink band as the focus shell's header below 1280; states as a 3 px edge, no box | the ink panel; compact tinted bars; conditions as bars |
| **Motion** | none | the line drawn once (1.4 s), longer than the system's 250 ms | the dots appear, 70 ms apart |
| **The berry** | the spaces; a dot by the sent address | the spaces; an edge on the sent address | the spaces; a dot by the sent address |
| **E-mail** | an ink band with the word; no spark | no card, a large title; a berry edge on the hour the link lasts (against foundation §16) | a compact card, the link in its own box; a berry dot before the word (against §16) |

The typeface stays IBM Plex Sans Arabic in all three: no display face is proposed (Arabic shaping first).

## New words (proposals)

| Where | Arabic | English |
|---|---|---|
| The panel's title | أين تعمل اليوم؟ | Where will you work today? |
| The panel's line | بحسابك تحفظ مساحاتك المفضّلة وتتابع بلاغاتك، ومنه يدير أصحاب المساحات مساحاتهم. | Your account keeps your favourite spaces and follows your reports; space owners run their space from it. |
| The Strip's caption | كل نقطة مساحة عمل في الدليل | Each dot is a space in the directory |
| The Strip's name (assistive) | رسم لقطاع غزة، عليه مساحات العمل في الدليل | A drawing of the Gaza Strip, with the directory's coworking spaces on it |
| The Strip's description (assistive) | رسم فنّي لا خريطة. النقاط من بيانات الدليل في 14 نوفمبر 2026. | An artistic drawing, not a map. The dots are from the directory's data of 14 November 2026. |
| The letter rule | حرف واحد على الأقل، بأي لغة | At least one letter, in any language |

## States added (the original's names kept)

Sign in: `offline`, `google` (Google's failure area; the original's `?google=notallowed`), `idle` (production's
`SESSION_IDLE`). Forgot password: `failed` (the general error). The forced change: `errors`, `offline`.
Changed: forgot password's default is the form at once, `loading` is the form with a thin bar, `unreachable`
the form with the offline note above it (production shows the note alone — a proposal); reset's `loading` is
the form's skeleton. A password sign-in of a Google-made account answers `INVALID_CREDENTIALS` by design, so
its state is `error`.

## The lab

`prototype/Auth lab.html`: the design (Original, Slate, Coast, Dots), the page, the state, the language, the
theme, the width (390, 768, 1440 or all three), and «قارن التصاميم» (the four at one width). Each frame is the
page itself, with a link to it; the view lives in the address, e.g.
`Auth lab.html?design=coast&page=forgot&state=sent&width=all` or
`Auth lab.html?page=register&state=typing&width=390&compare=1&theme=dark`. It says when the original has no
drawing of a state. Captures: `variants\lab-1440-light.png`, `lab-1440-dark.png`.

## Commits (masaha-prototype, `main`, pushed; head `f9dc0fc`)

- `a9871dc` feat(auth): add the three designs of sign in
- `97c3a50` feat(auth): extend the designs to the auth pages
- `b04ce54` feat(auth): add the reset e-mail's three designs
- `fd2a4c8` feat(auth): add the auth lab
- `88b89f7` docs(auth): record the three auth designs
- `f9dc0fc` fix(auth): review fixes from the owner's captures

`check-parse` and `check-classes` passed before each commit. Nothing in masaha (production) was touched, and
neither this repository's `README.md` nor its `CLAUDE.md`.

## The captures

`D:\MASAHA\DT\AUTH\variants\` — 134 PNG at 2x, the switcher hidden: pages 1–5 × the original and the three
designs × 390 / 768 / 1920 × light / dark, Arabic, full page; the reset e-mail (6) × the four × three widths;
the lab at 1440, light and dark. `report.txt` beside them holds each frame's measured h1 offset and the probe's
findings (none in the variants; the original's one is its logo's hidden word, a false positive). I looked at
every capture (on contact sheets per page, and the key ones at full size), at every state of every page at 390
in light, and at each page at 1440 in dark English. Tools: `DESIGN\AUTH\tools\` (`shoot.mjs`, `job.mjs`,
`sheet.mjs`), run only through the grant script (lane `auth`).

## What I did not do, and why

- **No sub-agents.** The three designs share one kit by design (one logic, three stylesheets); splitting the
  pages per design would have tripled the logic and let the states drift apart. One session was enough.
- **The reset e-mail is not a `?v=`.** `Reset email.html` has no script to replace and the original is never
  edited, so its designs are standalone pages under `variants/Reset email/`, reached from the lab. Captured in
  light only: the e-mail has no dark theme (production's is `color-scheme: light`).
- **The server** was the supervisor's on 5410, already running; I started none.
- **Not every state in every language, theme and width** was looked at: every state at 390 Arabic light, the
  defaults in all six combinations, and English at 1440 dark and Sign in at 1440 light.
- **For masaha to settle, not here:** forgot password's offline note shown over the form (production shows the
  note alone); a spark in the e-mail (foundation §16 says none); the panel staying the ink in dark. The original
  prototype pages have no `h1` (a card title in a `div`), unlike production: a finding about the original, left
  unchanged.
- **The Strip's limits:** the outline is approximate (round 3's, "not survey data"); nine of the 13 spaces sit
  within 2 km in Gaza City and touch at this scale. That is the data, kept rather than spread out.

---

## Slate polish round (2026-11-15)

The owner chose «اللوح» Slate. Coast and Dots are as they were: every change below is behind Slate's own
flag (`polish` in the kit's `AX_DESIGNS`) and stylesheet, except two that change nothing seen (the digit
rule and a dead effect). Head: **`5c540a5`** on `main`, pushed.

### للمالك، باختصار
- **الرسم:** القطاع صار مرسومًا لا كتلة: اليابسة هادئة، والساحل خطّ أدقّ وأفتح من حدود اليابسة، والنقاط
  بحجم ثابت على الشاشة. ولأن مساحات مدينة غزة التسع متلاصقة، دائرة فوق البحر تكبّر المدينة أربع مرات
  فتُقرأ التسع تسعًا. كل النقاط الثلاث عشرة ظاهرة في كل العروض.
- **الداكن:** اللوح بعمق الصفحة نفسها، يفصله خط رفيع، لا بطاقة رمادية.
- **الهاتف:** رسم صغير للقطاع بنقاطه بجانب الشعار.
- **الشروط:** سطر واحد تحت الحقل: «8 أحرف على الأقل، فيها حرف ورقم»، ثم ما ينقص فقط، ثم «✓ كلمة المرور
  مناسبة».
- **التذييل:** الروابط وملاحظة أصحاب المساحات في المنتصف، مجموعة واحدة هادئة.
- **زر Google:** بحجمه الحقيقي في الإنتاج (40 بكسل)، والحقول بالارتفاع نفسه من 768.

### Each point and what changed
1. **The Strip as a drawing:** land `neutral-800` mixed half into `neutral-900` with a `neutral-700`
   border; the coast its own line, `neutral-300`, 1.25 px (1.5 from 1440). Dots 9 px across with a 1.5 px
   ring of the panel's colour, sized in screen pixels (measured on layout and resize). Gaza City's nine
   sit closer than a dot is wide (two are 1.4 drawing units apart), so a **circle over the sea** shows the
   city ×4 with its coast through it, tied to a ring on the Strip by a line. All 13 show at 1280 (the
   panel's 640 px minimum height captured), 1440 and 1920.
2. **Dark:** the panel is `neutral-950`, the page's own; its hairline (`neutral-800`) and the drawing
   (land `neutral-900`) set it apart.
3. **Below 1280:** a solid Strip mark, 27 × 34 px (`neutral-400`; dark `neutral-600`), beside the logo
   outside its 8 px space, its spaces in the berry.
4. **Google's row:** 40 px tall, as wide as the column up to 400, Google's 4 px corners; Google's own dark
   button in dark. Fields and the submit are 40 from 768 with a mouse, 44 on touch, and 48 on the phone
   (stated in `decisions/auth.md`).
5. **The smaller items:**
   - F4: the panel logo's focus in `neutral-50`.
   - F10: «نسيت كلمة المرور؟» and «سجّل الدخول بهذا البريد» at 44 px.
   - F13: the digit rule is `\p{N}` (all three designs; nothing visible changes).
   - F14: forgot password's offline note uses «تعذّر الاتصال» and its line.
   - F16: on the forced change the panel shows the logo, the drawing and its caption only.
   - F15: `index.js` builds the registry inside a function; the kit's empty effect is gone.
   - F7: compare lays the four out 2 × 2 at 768 and 1440 and opens at 390. A resize that changes only
     the height no longer reloads the frames; that was also why full-page captures of the lab came out
     blank.
6. **Polish:**
   - The sign-in buttons have no icon.
   - One 8 px rhythm: label 8, field 8, its line 8, 24 between fields, 32 to the button and between head,
     body and foot.
   - The foot is one centred group with the owners' note at its head, 13 px.
   - The states keep the system's alerts, 12 × 16 px padding.
7. **The owner's points:** the foot's links and the owners' note are centred on the form's column.
8. **The password conditions:** one line under the field on register, reset and the forced change; it is
   the field's description and `aria-live="polite"`.
   - Before typing, muted: «8 أحرف على الأقل، فيها حرف ورقم».
   - While typing, only what is missing, worded for each case (examples below).
   - Once met: a berry tick and «كلمة المرور مناسبة».
   - Past 72 bytes: production's «طويلة جدًا — اختصرها».
   - A submit with a rule unmet shows production's field error, focused.

   Coast and Dots keep their own conditions.

### New words (proposals, both languages)

| Case | Arabic | English |
|---|---|---|
| Before typing | 8 أحرف على الأقل، فيها حرف ورقم | At least 8 characters, with a letter and a number |
| A letter / a digit / both missing | ينقصها حرف · ينقصها رقم · ينقصها حرف ورقم | Needs a letter · Needs a number · Needs a letter and a number |
| Only the length (1 / 2 / 3–7) | ينقصها حرف واحد / حرفان / 3 أحرف لتصل إلى 8 | Needs 1 more character / 3 more characters to reach 8 |
| Kind and length | ينقصها رقم، وحرفان آخران لتصل إلى 8 · ينقصها حرف ورقم، و5 أحرف أخرى لتصل إلى 8 | Needs a number and 2 more characters to reach 8 · Needs a letter, a number and 5 more characters to reach 8 |
| All met | ✓ كلمة المرور مناسبة | ✓ Good password |

### Commits
- `a430c80` feat(auth): polish slate after the owner's choice
- `696ab3b` fix(auth): lab compare view and registry scope
- `5c540a5` docs(auth): record slate's polish round

`check-parse` and `check-classes` passed before each commit. The originals, the shared modules, `README.md`
and `CLAUDE.md` are untouched.

### The captures
- **Overwritten in `D:\MASAHA\DT\AUTH\variants\`:** Slate's 30 at 2x (five pages × 390 / 768 / 1920 ×
  light / dark, Arabic).
- **Added there:**
  - `1-login-slate-1440-{light,dark}-en.png` and `2-register-slate-1440-{light,dark}-en.png`;
  - `lab-compare-390.png` and `lab-compare-1440.png`.
- **Reports:** `report.txt` now holds this round's probe; the first round's is kept as `report-round1.txt`.
  The probe found no contrast failure, no overflow and no console error. The h1 sits at 88 / 144 / 200 px on
  every page.
- **What I looked at:**
  - every capture above;
  - every state of every page at 390, in Arabic light and in English dark (60 frames);
  - Sign in at 1280 × 640, the panel's minimum.

### Not done, and why
- **Coast and Dots** were not touched, by the owner's word. Their findings (F1, F2, F5, F8, F9, F11, F12)
  stay open, including Coast's broken line.
- **The lab is slow to fill:** its three design frames each compile the kit with the page's in-browser
  Babel, on one thread, so they take several seconds. This is a prototype cost, not the product's.
