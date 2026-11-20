# Review of the auth designs — Claude Code, Opus 5.5
Commits a9871dc..f9dc0fc · head moved: no (local `main` at `f9dc0fc`, tree clean; not fetched)
Verdict: ready after small fixes

## للمالك، باختصار

1. التصاميم الثلاثة مبنية كما طلبت: كل صفحات الدخول بحالاتها، والمختبر يعمل، والأصل والإنتاج لم يُمسّا، ونقاط القطاع هي المساحات الثلاث عشرة الحقيقية بإحداثياتها تمامًا.
2. لكن «الساحل»، وهو توصية المصمم، يظهر مكسورًا في كل لقطاته على الشاشة الكبيرة: خطّ القطاع لا يكتمل (حدّه الشمالي وأعلى حدّه الشرقي ناقصان)، والسبب خلل في طريقة رسم الحركة. ويقصّ الرسم أيضًا مساحتين في الجنوب.
3. في «اللوح» لا يظهر التوتي على الهاتف والتابلت إلا في الشعار. و«النقاط» له تكوين «اللوح» نفسه على الشاشة الكبيرة، ولا يختلف عنه إلا في الملمس.
4. زر Google مرسوم أعرض وأطول مما يرسمه Google فعلًا في الإنتاج (400 × 40 بكسل على الأكثر)، فوعد «بعرض الحقول» لا يتحقق في البناء كما رُسم، خاصةً في «الساحل».
5. الحكم: جاهز بعد إصلاحات صغيرة. أصلحوا خط «الساحل» وأعيدوا التقاط صوره قبل أن تختار. أقوى التصاميم على الشاشة الكبيرة «النقاط»، وأقوى فكرة على الهاتف هي شريط «الساحل».

## Findings (most severe first)

**F1 — blocker · Coast's drawn line never completes, on every desktop width**
- **Where:** `prototype/variants/_auth/kit.jsx:192-194`: the three line paths have `pathLength="1"` and `vectorEffect="non-scaling-stroke"`. `prototype/variants/_auth/base.css:164` sets `.ax-draw-on path { stroke-dasharray: 1; … }`.
- **Seen:** every Coast capture at 1920, for example `1-login-coast-1920-light.png`, `-dark.png`, `2-register-…`, `3-forgot-password-…`:
  - The outline's north border is missing, and so is the east border north of outline point 17 (31.495, 34.49).
  - Both offshore echoes stop at the same point, about a quarter of the way down the coast.
  - The pattern is pixel-identical in light and dark and on every page. So it is static, not an animation frame caught mid-way: the echoes start 0.2 s apart and would end at different points.
  - The numbers match Chrome dashing a non-scaling stroke in screen pixels while `pathLength` scales the dash in user units. At the panel's ×3.64 scale the "whole" dash covers 1/3.64 (27.5 %) of each path, then leaves an equal gap:
    - each echo ends at y ≈ 81 of the drawing's 374, which is 27.5 % of its length;
    - the edge's second dash ends 4.8 units past point 17, where the capture's line stops.
  - Under `prefers-reduced-motion` the dash stays (only the animation is removed), so those readers see the same broken line.
  - At 1440 (×2.73) the gap falls elsewhere: the south-east border goes missing instead.
  - The phone/tablet band has no motion and no dash, so it draws whole. That is consistent.
- **Why:** this is the lead's recommended design, and its signature drawing is broken in every capture and lab frame the owner will compare. As shown, it is not "the Strip".
- **Fix:** remove `vectorEffect` from the three line paths and give their stroke widths in drawing units, set per breakpoint (for example `--ax-line: .42` at 1920). Alternatives:
  - keep the non-scaling stroke, drop `pathLength`, and set `stroke-dasharray` / `stroke-dashoffset` to `getTotalLength() × the CTM's scale` in a layout effect;
  - or reveal the line with an animated clip or mask instead of dashes.

  Then recapture Coast at 1440 and 1920, with and without reduced motion.

**F2 — should-fix · Coast's panel crops two of the 13 spaces, and leaves its middle empty**
- **Where:** `kit.jsx:260` (`viewBox="96 -24 220 250"`, `xMidYMin slice`) and `coast.css:54` (`inset: 38% 0 -2% 0`).
- **Seen:**
  - At 1920 the drawing shows only latitudes from about 31.59 down to 31.43. Al-Salam Hub (31.420, 34.347) and Masar Tech (31.366, 34.271) fall outside it: the captures show 9 + 2 = 11 dots. At 1440 × 900, Masar Tech alone is cut.
  - Between the copy (ending at about y 280) and the first line (y 518) the panel is an empty ink field. The caption sits at the far foot, away from the dots.
- **Why:** the caption says each dot is a space in the directory, yet the south's spaces are the ones dropped. To a Gaza reader the drawing says the directory is a Gaza City thing. It is also the brief's own example of a weak 1920 composition: "a Strip cropped so little of it shows".
- **Fix:** crop the north tip instead of the south. Beit Hanoun has no space, and the line can run off the panel's top. Or widen the viewBox to take in latitude 31.36 (for example `20 -24 300 290`). Raise the art so the line begins under the copy. Check all 13 dots at 1280, 1440 and 1920, and at the panel's 640 px minimum height.

**F3 — should-fix · Google's button is drawn at a size production's Google button cannot take**
- **Where:**
  - `base.css:86`: `.ax-google { width: 100%; height: var(--control-height) }`, which is 44, 48 or 52 px.
  - `coast.css:6`: `--ax-form-w: 440px`.
- **Seen:** production draws Google's own button with `renderButton`, `size: 'large'` and its width clamped to 400. See `apps/web/src/features/auth/hooks/google-sign-in/useGoogleButton.ts:8,67,81` and `types/GoogleIdentity.ts:17` ("Google renders between 200 and 400"). Google's `large` button is 40 px tall. The prototype's button is HTML it draws itself, so it can be any size.
- **Why:** critique points 1–2 are solved only in the drawing.
  - Built as drawn, Coast's 440 px fields would again be 40 px wider than Google's button. That is critique point 2, exactly as production has it today.
  - In all three designs, the 44–52 px fields would stand taller than Google's 40 px button.
  - The owner would be choosing on a promise the build cannot keep.
- **Fix:** draw Google's row at the box Google really gives (at most 400 × 40), and size each form to it: Coast's form at 400, or its fields at 440 with that difference accepted and stated. Alternatively, record "a custom-drawn Google button" in `decisions/auth.md` as a proposal for masaha to settle (Google's branding rules apply). Do not claim critique points 1–2 as answered until one of these is chosen.

**F4 — should-fix · The panel logo's focus ring is invisible in the light theme**
- **Where:** `base.css:42` (the outline is `var(--ring)`) and `base.css:7` (the panel is `--neutral-900`), combined with `masaha/identity-ink-spark.css:39-40`: `--ring` is `--primary`, which is `--neutral-900` in light.
- **Seen:** from 1280 px the panel's logo is the page's only link home (`base.css:151` hides the header's logo). Its 2 px focus ring is #1a1f25 drawn on #1a1f25. This affects all three designs and every page except the forced change, where the logo is not a link.
- **Why:** §1 asks for a visible focus on every control (WCAG 2.4.7), and the report says every control has one.
- **Fix:** add `.ax-panel .ax-logo:focus-visible { outline-color: var(--neutral-50); }` to `base.css`. Coast's band already does this (`coast.css:34`).

**F5 — should-fix · Coast's phone band runs through the logo's clear space and under the tools**
- **Where:** `kit.jsx:239` (`viewBox="110 34 200 80"`, `xMidYMid slice`) and `coast.css:29-35`.
- **Seen:**
  - In `1-login-coast-390-light.png` and `2-register-coast-390-light.png`, the east border rises from the logo's lower start corner up through the wordmark. Foundation §16 asks for 8 px of clear space around the 40 px logo.
  - Gaza City's dots and the coast line sit under «English» and its icon.
  - On the forced change, which has three tools (`5-change-password-coast-390-light.png`), the dots overlap the language button.
  - By geometry, not captured: in English the logo moves to the left while the drawing does not mirror, so both echoes cross the logo.
- **Why:** the logo's clear space is masaha's rule (foundation §16). The band is the design's best idea, but it reads as clutter where it meets the controls.
- **Fix:** frame the band's drawing so the dots and lines sit in its middle third. Keep it clear of the logo box plus 8 px, and of the tools, in both directions. Two ways: pick a viewBox per direction, or let the art stop short of the head row and occupy only the band's lower 52 px. Check at 360, 390 and 430, in Arabic and English.

**F6 — should-fix · Slate below 1280: the berry appears only in the logo (critique point 10)**
- **Where:** `slate.css`. Below 1280 its only berry rule is `.ax-sentto-dot`, which shows on Forgot password's *sent* state alone.
- **Seen:** `1-login-slate-390-light.png`, `2-register-slate-768-*.png`, `4-reset-password-slate-768-dark.png` and `5-change-password-slate-390-*.png` show no berry outside the logo.
- **Why:** «the berry appears only in the logo» is one of the 11 points every design must answer, and the report counts Slate as answering it. On the phone, where most people are, it does not.
- **Fix:** give Slate a berry job below 1280. For example, a small solid Strip silhouette (about 22 × 28 px) beside the logo with its dots in the berry, or the caption with its dot under the form's foot. Otherwise, state in `decisions/auth.md` that Slate answers point 10 only from 1280, so the owner chooses knowingly.

**F7 — should-fix · The lab's «قارن التصاميم» is unreadable at its default width**
- **Where:** `prototype/Auth lab.html:144` and `:168-170`. In compare mode the four frames share one width, and `scale = min(1, avail / total)` has no floor.
- **Seen (by code; no compare capture exists):** turning compare on at the default 1440 fits 4 × 1440 px into about 1330 px, which is a scale of ×0.23. Each frame is about 330 px wide, with its text at about 3 px.
- **Why:** comparing the designs is what the owner came to do. At 1440 every frame has to be opened to be read.
- **Fix:** in compare mode at 768 or 1440, lay the four frames out 2 × 2 (about ×0.45 on a 1440 screen), or floor the scale at 0.5 and let `.lab-stage` scroll (it already has `overflow-x: auto`). Start compare at 390, where four phones fit at about ×0.85.

**F8 — should-fix · Dots' three condition bars read as a strength meter, and rest almost invisible**
- **Where:** `dots.css:20-27`.
- **Seen:** `2-register-dots-1920-light.png` and `2-register-dots-768-light.png`.
  - The three equal segments under the field rest at `neutral-200` on `neutral-50`, about 1.2 : 1, so they are barely there.
  - «حرف واحد على الأقل، بأي لغة» wraps and leaves «لغة» alone on its line.
- **Why:** segments filling in under a password field are the universal strength-meter pattern. Take a password with the length and a letter but no digit: two of three bars fill, which reads as "medium strength", not "not accepted yet". The decision file itself says the bars are "not a strength meter".
- **Fix:** tie each bar to its rule rather than to a row. For example, a short bar (16 × 4 px) at the start of each label in a vertical list, filled with ink when met. Raise the resting track to `neutral-300` (light) / `neutral-600` (dark), and add `text-wrap: balance` to `.ax-cond-label`.

**F9 — should-fix · Slate and Dots share one composition from 1280 px (§2)**
- **Where:** `slate.css:21-33` against `dots.css:42-55`.
- **Seen:** `1-login-slate-1920-light.png` beside `1-login-dots-1920-light.png`. Both build the panel the same way:
  - the logo at the top start;
  - the Strip on a full-height diagonal at the far side;
  - the title and line in the empty bottom-start corner;
  - the caption at the foot.

  What differs is the fill (solid or grain), the column ratio (1 : 1 or 5 : 7) and the title size (40 or 54 px).
- **Why:** §2 asks the three to differ "in composition and character, not in colour tweaks", with two of them pushing past A1. In the lab's comparison, the owner sees one layout twice.
- **Fix:** push Dots' composition, and leave Slate as A1. One option: let the grain fill the whole panel, sea and land, with the land drawn in denser, brighter dots and the Strip at about ×1.4 running off the panel's top and bottom, and the title set over the field. Another: put the title at the top and make the dotted Strip a full-height band at the panel's inner edge.

**F10 — should-fix · Standalone links are under the 44 px target**
- **Where:** `base.css:73-74` and `:79`. `.ax-forgot` and `.ax-instead` are `.ax-link`s with no minimum height.
- **Seen:** «نسيت كلمة المرور؟» stands alone under the password field at about 24 px tall (`1-login-*-390-*.png`). «سجّل الدخول بهذا البريد» on Register's *exists* state is built the same way.
- **Why:** §1 asks for targets of at least 44 px, and the report says they are. Links inside a sentence («إنشاء حساب», «تواصل معنا») are exempt; these two are not.
- **Fix:** add `.ax-forgot, .ax-instead { display: inline-flex; align-items: center; min-height: 44px; }`, as `.ax-back` already has.

**F11 — nit · Dots' small Strip opens a gap between the title and its line**
- **Where:** `dots.css:33` and `base.css:57`.
- **Seen:** on the phone and tablet (`1-login-dots-390-light.png`, `2-register-dots-768-light.png`), the 74 px mini Strip sets the title row's height. That leaves about 70 px between the h1 and its lede; Slate has about 30.
- **Fix:** let the mini Strip span the h1 and the lede (a two-row grid with the mini in its own column), or cap it at the h1's line height (about 38 px).

**F12 — nit · Coast in dark keeps the band's hairline from 1280 px**
- **Where:** `coast.css:30`. `[data-theme=dark] .ax--coast .ax-head` outranks the `border: 0` at `:43`.
- **Seen:** `1-login-coast-1920-dark.png` has a line under the top bar across the form column. `report.txt` shows the h1 at 193 px in dark against 192 in light.
- **Fix:** inside the 1280 query, add `[data-theme=dark] .ax--coast .ax-head { border: 0; }`.

**F13 — nit · The digit rule is narrower than production's**
- **Where:** `kit.jsx:138` uses `/[0-9٠-٩]/`. Production's `packages/shared/src/users/passwordPolicy.ts:11` uses `/\p{N}/u`.
- **Why:** Persian digits (۰–۹) would read as unmet here but are accepted in production. The kit's comment says these are "the rules production holds".
- **Fix:** use `/\p{N}/u`.

**F14 — nit · Forgot password's offline note promises data that is not missing**
- **Where:** `kit.jsx:542`. The *unreachable* state shows status's «لا يوجد اتصال بالإنترنت» / «ستظهر البيانات عند عودة الاتصال» above a form that is already on the page. This layout is the lead's proposal.
- **Fix:** in the proposal, use the form's offline words: «تعذّر الاتصال» and «تحقّق من اتصالك بالإنترنت ثم حاول مرة أخرى», with «إعادة المحاولة».

**F15 — nit · Code and e-mail details**
- `prototype/variants/index.js` adds a top-level `const AUTH_DESIGNS` to the global scope shared by all 41 pages. That breaks no rule today, but it goes against README's "one scope" caution. Inline the array, or wrap the file in an IIFE.
- `kit.jsx:521` is an effect that does nothing.
- The three e-mail pages under `variants/Reset email/` link no icon. That is likely `report.txt`'s single 404 (`/favicon.ico`).
- Coast's e-mail uses 20 px side padding for its Arabic block and 4 px for its English block and footer on the phone (`6-reset-email-coast-390-light.png`), so the two halves have different edges.

**F16 — nit · The panel's words on the forced change**
- **Where:** `5-change-password-*-1920-*.png`.
- **Seen:** a staff member with a temporary password is asked «أين تعمل اليوم؟» and told about favourites and reports.
- **Fix:** on `change`, show the panel's logo and Strip only, without the title and line.

## The brief, point by point (all three)

| Point | Slate | Coast | Dots |
|---|---|---|---|
| **A1 at 1280+:** two columns, the form at the start with no card, an ink panel with the logo, title, line and Strip | ✓ | ✓, but the Strip is cropped (F2) and broken (F1) | ✓ |
| **A1 at 768–1279:** one column, fixed offset (h1 at 144 / 212 / 152 px on every page) | ✓ | ✓ | ✓ |
| **A1 on the phone:** full width, no card, no frame, 52 px controls, clearer title | ✓, no Strip | ✓. The ink band is a header, not a frame; it sits at the edge of "at most a small touch" (the owner's call) | ✓, small dotted Strip |
| **A2:** artistic drawing; no governorate lines or names; inline SVG of about 3 KB; never mirrored | ✓ | ✓ | ✓ |
| **A2:** the 13 real spaces, the snapshot's date stated | ✓ 13. The date is in the drawing's `<desc>` and `decisions/auth.md`, not on screen | 11 of 13 at 1920 (F2) | ✓ 13 |
| **A2:** reduced motion | No motion | Off, but the static dash stays (F1) | Off ✓ |
| **Identity:** ink + berry, the logo's own files | ✓ | ✓; the band crowds the logo on the phone (F5) | ✓ |
| **The berry has a job** | Only from 1280 (F6) | ✓ | ✓ |
| **Arabic first, logical sides** | ✓ | ✓ | ✓ |

On logical sides: physical properties appear only in the e-mails (unavoidable there) and in the Strip's placement by `dir`, because the Strip itself is never mirrored. Both are legitimate.

- **The product's real words:** checked against production's catalogue: `auth.ts`, `forms.ts`, `errors.ts` (`SESSION_IDLE`, `RESEND_LIMIT_REACHED`), `status.ts`, `users.ts` (the forced change) and `resetEmail.copy.ts`. All match, apart from F13's rule and F14's choice of line. The new words are marked as proposals in both languages, in the decision file and the report.
- **No fake data, nothing of *Not in v1*:** there are no counts and no claims. «15 دقيقة» is production's. The WhatsApp number is a placeholder (+970 59 000 …). There is no booking, payment or rating.
- **The 11 critique points:**

  | Point | Slate | Coast | Dots |
  |---|---|---|---|
  | 1. Google in dark, no white frame | ✓ in the drawing (F3) | ✓ in the drawing (F3) | ✓ in the drawing (F3) |
  | 2. Google as wide as the fields | ✓ at 400 | ✗ once built: 440 > 400 (F3) | ✓ at 380 |
  | 3. Forgot's form at once | ✓ | ✓ | ✓ |
  | 4. Forced change has a language switch | ✓ | ✓ | ✓ |
  | 5. Conditions never read as radio buttons | ✓ tick / dash | ✓ tick / dash | ✓, but read as a meter (F8) |
  | 6. One fixed offset | ✓ | ✓ | ✓ |
  | 7. A real hierarchy | ✓ | ✓ | ✓ |
  | 8. No frame in a frame on the phone | ✓ | ✓ | ✓ |
  | 9. The 1920 half filled | ✓ | ✓ | ✓ |
  | 10. The berry beyond the logo | ✗ below 1280 (F6) | ✓ | ✓ |
  | 11. «… بأي لغة» | ✓ | ✓ | ✓ |
- **Accessibility:**
  - Errors are tied to their fields: the design system's `Field` joins its error id into the input's `aria-describedby`, as seen in the bundle.
  - `autocomplete` matches production.
  - A failed submit moves the focus to the first invalid field.
  - Fields stay readable while pending.
  - Gaps: the panel logo's focus (F4) and two link targets (F10).
  - The caption's contrast on the panel is about 6.6 : 1 (computed from the tokens).
- **§2, three different designs:**
  - Coast is genuinely different: a line drawing, a crop and a band on the phone.
  - Slate and Dots differ in texture and proportions more than in composition (F9).
  - Slate is the one closest to A1, as asked.
  - The names are short, given in Arabic and English, and described in two lines each.
- **§3, every state:** all of the original's states are kept by name, and the added states are listed in the decision file. Because one kit holds the logic, a state behaves the same in all three designs. Two checks against production:
  - The Google-made account answering `INVALID_CREDENTIALS` is confirmed in production (`docs/api/api-contract.md:107`, `docs/backend/security.md:34`).
  - Forgot password's form shown at once and its offline note over the form are proposals, marked as such.
- **The repository's rules:**
  - Originals untouched: the diff for `prototype/*.html` other than the new lab, `masaha/*`, the sample data, `README.md` and `CLAUDE.md` is empty.
  - New styles are in the variants' own CSS, and both checks scan `variants/` recursively, so the kit is covered.
  - No object rest and no top-level `name`: the kit is one IIFE.
  - Six Conventional commits, subjects of 28–49 characters, each with a body and no attribution.

## The three designs as design

**Slate «اللوح».**
- **Strengths:**
  - The calmest and most buildable of the three.
  - The cleanest form: the system's alerts, a 30 px h1 and a quiet foot.
  - At 1920 the solid shape reads as Gaza at once, and the copy sits well in the corner the land leaves empty.
- **Weaknesses:**
  - The land is a large flat grey slab with a hairline. It reads more like a placeholder shape than a drawing.
  - The dots are sized in drawing units (about 7 px at 1920), so Gaza City's nine merge into one clump.
  - Below 1280 nothing of the brand remains but the logo (F6).
  - In dark the panel (`neutral-900`) is lighter than the page (`neutral-950`), so the ink slab reads as a grey card. This is true of all three; the lead has passed it to masaha.
- **To strengthen it:**
  - Size the dots in screen pixels (about 4–5 px) so nine read as nine.
  - Draw the coast edge brighter than the land border so the shape reads as drawn, not filled.
  - Give the berry a job on the phone.

**Coast «الساحل».**
- **Strengths:**
  - The best phone idea of the three: the brand carried on an ink band, with no frame round the form.
  - The clearest hierarchy: an editorial 40 px h1 with a 17 px lede.
  - The most refined states: an edge and words instead of a box.
  - The way back in the top bar from 1280 is a good touch.
- **Weaknesses:**
  - At 1920 it is the weakest panel: the line is broken (F1), the south is cut (F2), and a large void separates the copy from the drawing.
  - The echoes read as motion lines more than sea.
  - On the phone the band crowds the logo and the tools (F5).
  - The 440 px form cannot sit beside Google's real button (F3).
- **To strengthen it:**
  - Fix F1 and F2.
  - Start the line under the copy and let it cross the panel's full height.
  - Keep one echo, not two.
  - Clear the band's head row.
  - Bring the form to 400 px.

**Dots «النقاط».**
- **Strengths:** the most crafted panel at 1920. The grain makes it read as a drawing, not a map. The 54 px title holds the panel, and the narrow form feels precise.
- **Weaknesses:**
  - It has Slate's composition (F9).
  - On the phone the mini Strip reads as a sticker beside the title and opens a gap (F11).
  - The bars (F8).
  - Its most important messages, the states, are set in the page's smallest text (13.5 px).
- **To strengthen it:**
  - F9's full-field grain.
  - On the phone, a thin dotted band under the header instead of the sticker.
  - Conditions as in F8.
  - States at 14 px.

Taken whole: Dots has the strongest desktop and Coast the strongest phone. The owner should see Coast's desktop again only after F1 and F2 are fixed, since every Coast capture today shows the broken drawing.

## The lab

`prototype/Auth lab.html` has every control the brief asks for: design (Original and the three), page, state (each page's own list), language, theme, width (390, 768, 1440 or all three), and «قارن التصاميم».
- The view lives in the address (`?design=&page=&state=&width=&compare=1`, plus `lang` and `theme`). `i18n.js` reads `theme` back, so a dark link opens dark.
- Each frame carries `switcher=0` and a link to the full page.
- A note says when the original has no drawing of a state; the original's own parameter is used where it has one (`google=notallowed`, `state=request`).
- The e-mail page shows the three standalone designs and the original.
- It is Arabic first, has both themes and works from the keyboard: `aria-pressed` segments, fieldsets with legends, visible focus. No shared module was edited.

Weaknesses:
- The compare view at 768 and 1440 is too small to read (F7).
- `role="toolbar"` on a bar of selects and fieldsets promises arrow-key movement it does not have, so drop the role.
- The segment buttons are 36 px. That is acceptable for a desktop tool, but under the 44 px the pages keep.

The two lab captures (`lab-1440-light.png`, `lab-1440-dark.png`) show the "all three widths" view working.

## Not checked, and why
- **Nothing was run.** This review was read-only: no server, no browser, no scripts. `check-parse` and `check-classes` were not run. I read both scripts and confirmed they cover `variants/_auth/`.
- **States were judged by the code, not the screen.** Only each page's default was captured. Every state of §3 was read in `kit.jsx`, not seen rendered: sent, the resend limit, link open, invalid, unreachable, offline, errors and typing.
- **English (LTR) was not seen at any width.** No English capture exists. F5's English half comes from the drawing's geometry. The lead reports looking at English at 1440 in dark.
- **Motion was not seen.** The captures are static. F1 rests on the captures plus the geometry, which matches to a few drawing units.
- **Google's button height was not measured.** The 40 px figure for `large` is Google's documented size. The 400 px maximum is production's own code.
- **Contrast was not measured on the captures.** I checked a few pairs from the tokens and otherwise relied on the lead's probe (`report.txt`).
- **The e-mails were not tried in mail clients.** Only their markup and captures were read.
- **The remote was not fetched.** "Head moved: no" refers to the local `main`.
