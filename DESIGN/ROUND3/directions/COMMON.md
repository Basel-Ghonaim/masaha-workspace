# Round 3 — what every direction shares (the lead's brief to the three builders)

You build **one design direction** for **Masaha (مساحة)**: a bilingual, **Arabic-first (RTL)** / English directory of
coworking spaces in the Gaza Strip, live at https://masaha-omega.vercel.app. Your direction's idea and system are in
its `DESIGN.md` (same folder as your `PROMPT.md`). This file holds what all three directions share. Read
`..\DIAGNOSIS.md` first: it says what is wrong today and why it reads as AI-made. **The owner's bar: "a design I
look at and am shocked by its quality and by the difference."** Clean and correct is the floor, not the goal.

## 1. Fixed — never change (R3-14)

**Colours: ink + berry spark (ADR 0019).** Use only these ramps (OKLCH-drawn; hexes as built):

| Ramp | 50 | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900 | 950 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| neutral (the ink's hue) | #F7FBFF | #ECF4FC | #DDE5ED | #C9D0D7 | #9FA6AD | #767D84 | #5E646A | #484E54 | #2C3137 | #1A1F25 | #0D1217 |
| spark (berry) | #FEF3FE | #FFE3FD | #FAC8F7 | #EBA5E8 | #D27ED0 | #B55BB3 | #934791 | #773A75 | #5A2A59 | #3F1B3E | #260D25 |
| green | #ECFCEF | #D9F5DF | #BAE8C5 | #90D3A2 | #63B77C | #39995B | #137D41 | #026732 | #034D25 | #013517 | #001F0A |
| amber | #FFF5EA | #FFE9CF | #FBD3A2 | #EEB56C | #D6912B | #B27406 | #905C01 | #754B04 | #593700 | #3E2500 | #261400 |
| red | #FEF4F3 | #FDE7E4 | #FFCDC8 | #FEA69E | #FC6E68 | #DE4544 | #BE222A | #A20419 | #7C0110 | #580007 | #370003 |
| blue | #F1F8FE | #E0EFFF | #C0DEFF | #90C6FE | #64A6E9 | #3E87CE | #1F6CB0 | #075796 | #004174 | #002C52 | #001934 |

Plus white. The roles (foundation §5): light — page `n-50`, text `n-900`, card/popover white, muted `n-100` /
muted text `n-600`, border `n-200`, input border `n-500`, focus ring `n-900`, **primary (the ink) `n-900` on white
text**, primary-hover = n-900 mixed 18% toward n-50, **selected = `s-100`** (text n-900), **hover = `n-200`**,
**spark = `s-500`**, destructive `r-600`, success `g-600` (subtle g-50/g-800), warning fill `a-500` (subtle a-50/a-800),
info `i-600`. Dark — page `n-950`, text `n-50`, card `n-900`, muted `n-800`/`n-400`, border `n-800`, input `n-500`,
ring `n-50`, **primary `n-50` with `n-950` text**, selected = s-900 mixed 30% toward s-800 (text n-50), hover `n-800`,
**spark `s-400`**, destructive `r-400`, success `g-400`, warning `a-400`, info `i-400`. You may use other steps of these
ramps for surfaces and marks your `DESIGN.md` names (an ink band, a tint), never a colour outside them.

**The spark's rules (hard):** the berry is **never text, never on an action (no berry button, link or icon button),
never destructive.** It marks *what matters now* — as a fill, an edge, an outline, a dot or a bar. **Hover is never
the selected tint**, and selected keeps its tint under the pointer. **Status is never colour alone** (always its
word). Warning is never text on its own. Links in running text are underlined. Text over a photo sits on a scrim
(n-900 at 70% / dark: n-50 at 70% with n-950 text), never straight on the image.

**The logo:** `..\_shared\logo\` — `masaha-logo-berry.svg` (light) and `masaha-logo-dark-berry.svg` (dark): «مساحة»
over "MASAHA" in the ink, the ة's two dots in the spark; `masaha-mark-berry.svg` / `-dark-` the small mark (the ة).
Never under 36 px tall (mark from 16 px), clear space 20% of its height, never mirrored, cropped, stretched,
recoloured, or on a photo without a plain ground. Same drawing in both directions. It is the link home in the header.

**Arabic first, RTL.** `<html lang="ar" dir="rtl">` by default; English switches to `lang="en" dir="ltr"`. Logical
CSS properties only (`margin-inline-start`, `inset-inline-end`, `text-align: start` — no `left`/`right`). Western digits
(0–9) in both languages. Phone numbers, emails, prices, times are `dir="ltr"` inside RTL text (`<bdi>` or `dir=ltr`
spans). Directional icons (arrows, chevrons) mirror in RTL; non-directional ones never do.

**The v1 scope (Not in v1 — never show, even as a teaser):** booking or reserving a seat, online payment, reviews or
ratings, QR check-in, an in-app "claim this space" flow (owners **contact** Masaha by WhatsApp or email), a mobile app,
notifications. **Truth:** only data the product has. **No ratings, no seat counts, no capacity, no occupancy
percentages, no "busy" scale** (ADR 0008: the live status is a *state* — متاح · ممتلئ · مغلق الآن — never a count, and only
for verified spaces; an unverified space shows its state *by its hours* on a **neutral** badge, «مفتوحة الآن» / «مغلقة
الآن», or «لا تتوفر حالة مباشرة» with no hours). No invented testimonials, user counts, prices, reviews, "trusted by",
awards. Counts of *spaces* (13 in the Strip, 4 in الرمال) are real and fine.

## 2. The real content

- **The live site's 13 spaces**, as fetched on 2026-11-14: `..\_shared\data\spaces.json` (the directory's cards:
  names in both languages, area, verified, the week's hours `days[0..6]` (**index = JavaScript's `getDay()`: 0 Sunday … 5
  Friday, 6 Saturday** — Branch Hub's `days[5]` is `null`, shown on the live site as «الجمعة: مغلقة»; each `days[i]` is
  `{opensMinute, closesMinute}` (minutes from midnight) or `null` = closed; `days: null` = hours not available), `hoursStatus` (OPEN/CLOSED/null), `liveStatus`,
  `worksEvenings`, `womensHall`, cover URL) and `..\_shared\data\spaces\<slug>.json` (each space's page: description
  in both languages, address, `location {lat,lng}`, hours, prices in agorot — 3000 = 30 ₪ — with period
  HOUR/DAY/WEEK/MONTH and audience GENERAL/STUDENT, amenities with their Lucide icon names, contacts (WHATSAPP, PHONE,
  INSTAGRAM, FACEBOOK, EMAIL …), `updatedAt` per group, `staleGroups`, photos). `lookups.json`: governorates and their
  areas (both languages). `price-ranges.json`: each period's min and max. The platform contact (About):
  WhatsApp **+970597063545**, email **masahatgaza@gmail.com** (as on the live About page).
- **Photos:** `..\_shared\photos\<slug>-<n>-card.webp` (card size) and `-page.webp` (large); `index.json` lists them.
  **Know what they are:** 10 of 13 covers are the spaces' own social-media posters (logos, slogans, phone numbers);
  real interior photos are `coma-io-1`, `branch-hub-2`, `branch-hub-3` (and `garden-hub-1` is a poster over a photo).
  Your `DESIGN.md` says how your direction treats a poster, a real photo, and no photo. Never write over, recolour or
  crop away a space's logo in a way that misrepresents it; never invent a photo; no stock photos.
- **States the live data does not show today.** Today every live space is unverified except Elevate Hub (verified,
  but no live status: its capacity is not set). The product supports more, so each mock-up has a **«حالات تجريبية /
  Demo states»** switch in its review panel (below) that, when on, marks Branch Hub, Focus Hub, Garden Space and
  Number One Hub as **verified** with live states (Branch: متاح, Focus: ممتلئ, Garden: متاح, Number One: مغلق الآن),
  Elevate Hub متاح, and gives Branch Hub a running announcement (an `info` notice, e.g. «تمديد ساعات العمل حتى 22:00
  طوال الأسبوع» — mark it in your DESIGN.md as illustrative copy). Off by default (the truth first); the owner sees both.
- **The signed-in sample user:** «سلمى الأغا», demo-user@example.com (the local demo account); favourites: Branch
  Hub, Focus Hub, Coma Space, Masahat and Pal Hub (one with no photo to show your no-photo state — use Masahat with its
  photo removed in the favourites and say so). One favourite that left the directory: «نور هب» shown by its name
  with «لم تعد هذه المساحة معروضة في الدليل».
- **The copy:** the product's real words are in `C:\dev\masaha\app-design\apps\web\src\shared\copy\arabic\*.ts` and
  `english\*.ts` (read `site.ts`, `directory.ts`, `status.ts`, `auth.ts`, `users.ts`, `favorites.ts`, `map.ts`,
  `forms.ts`, `preferences.ts`, `dataReports.ts`, `announcements.ts` as you need). **Use them verbatim.** Where your new
  page division needs a word the catalogue does not have, write it in both languages in the product's voice (plain,
  specific, no filler: no «اكتشف»، «تجربة فريدة»، "seamless", "unlock") and list it in your `DESIGN.md` under
  *New copy (proposed)*.
- **Gaza's clock.** "Open now" and "today" are by Asia/Gaza time (`Intl.DateTimeFormat('en', {timeZone:
  'Asia/Gaza'})`): compute them live from the week's hours in the mock-up; never fake them.

## 3. The pages to build

Static HTML/CSS/JS in your direction's folder (`directions\<A|B|C>\`), **working from `file://`** (the lead's capture
tool opens them so): classic `<script src>` only (no ES modules, no `fetch`), the data embedded as a JS file you
generate from `..\_shared\data\` (e.g. `js\data.js`), images by relative path to `..\_shared\photos\`. Web fonts from
Google Fonts only (`<link>` to fonts.googleapis.com; the fallback stack still renders). Icons: **Lucide only**, inlined
SVG — copy each icon's nodes from `C:\dev\masaha\app-dr\node_modules\lucide-react\dist\esm\icons\<name>.mjs` (the
`__iconNode` array) into an icon helper; 24-unit viewBox, stroke `currentColor`, stroke-width per your DESIGN.md.
No other library, no framework, no CDN script, no build step.

1. `home.html` — Home.
2. `spaces.html` — the directory's list; `spaces.html?filters=open` with the filters open (the sheet on a phone; on
   desktop whatever your DESIGN.md says "open" means); `spaces.html?view=map` — the map. The filters (foundation +
   DIRECTORY_PROD decisions, as built today): **المنطقة** (areas, multiple, grouped by governorate), **السعر** (the
   subscription «الكل · ساعة · يوم · أسبوع · شهر», then «من / إلى» in ₪ once one is chosen), **الدوام** («مفتوحة
   الآن»، «مفتوحة مساءً»، «مفتوحة يوم الجمعة»), **أخرى** («المساحات الموثّقة فقط»، «أسعار للطلاب»، and «قاعة للنساء»);
   the sort («الأحدث تحديثًا»، «حسب الاسم»، with a subscription «الأرخص شهريًا» / «الأغلى شهريًا»); **«الأقرب إليّ»** its own
   control (asks for location only when pressed; in the mock-up, pressing it may simulate a point in الرمال and show
   «على بعد 0.7 كم» distances computed from the real coordinates, with the line «مرتبة حسب المسافة من موقعك. المسافات
   تقريبية بخط مستقيم.»); the search («اسم المساحة أو المنطقة»). **Make the filters actually filter** the 13 spaces.
   Your DESIGN.md may change their *look and placement* (and must say so); keep their *content*. The owner rejected
   chips for the filters (DIRECTORY_FILTERS, revision 1): a direction that brings chips back must say so as an
   overturned decision. The map: **draw it yourself as SVG** from the real coordinates (no tile service, no Leaflet): a
   simplified outline of the Gaza Strip, fitted to the frame, the spaces as pins at their real `location`. An
   approximate outline (lat, lng), north to south along the coast, then back along the border:
   `[31.594,34.491],[31.546,34.437],[31.504,34.402],[31.458,34.365],[31.410,34.322],[31.358,34.275],[31.316,34.221],
   [31.243,34.244],[31.222,34.268],[31.268,34.320],[31.330,34.372],[31.383,34.402],[31.448,34.455],[31.502,34.512],
   [31.540,34.567],[31.592,34.560],[31.594,34.491]` (equirectangular projection with the x scaled by cos 31.4° is
   fine). Label in the interface's language only; **no Hebrew, no labels outside the Strip.** Your DESIGN.md states the
   production map's tile style that this drawing stands for.
3. `space.html?slug=<slug>` — a space's page (every one of the 13 must render; the owner will open
   `?slug=branch-hub` (3 photos, prices, amenities, contacts), `?slug=elevate-hub` (verified, one price, no amenities,
   no contacts), `?slug=jreas-hub` (no hours)). Its content (foundation §13, DECISIONS_PUBLIC U8): status and contact,
   announcements, prices per audience (with «للعرض فقط · الدفع في المساحة» once), hours (today marked; the week), amenities
   (one list), about, location (with «الاتجاهات» to Google Maps by coordinates), the report link
   («الإبلاغ عن معلومة غير صحيحة»), each group's «آخر تحديث …» freshness; an unverified space's notice with «هل تدير
   هذه المساحة؟ تواصل معنا»; the heart (save). The order may change if your DESIGN.md says why.
4. `login.html` — sign in (Google, or email and password; «نسيت كلمة المرور؟»; «ليس لديك حساب؟ إنشاء حساب»).
5. `about.html` — About (the real About copy: the intro, verified / unverified, the status legend, «تواصل معنا», «لأصحاب
   المساحات»).
6. `account.html` — «إعدادات حسابي» signed in (name, email, language, theme, sign-in methods), with the account
   area's navigation (المفضّلة · بلاغاتي · إعدادات حسابي).
7. `favorites.html` — «المفضّلة».
8. `404.html` — the 404.

Each page: the site's header (logo home, الرئيسية · المساحات · عن مساحة, the language switch, the theme switch, sign
in — or, on the account pages, the user's menu) and footer, a skip link first, one `h1`, headings in order, labels on
every field, real links and buttons, a document title «{page} · مساحة» / "{page} · Masaha".

**Language and theme:** each page reads `?lang=ar|en` and `?theme=light|dark` from its address (the capture tool
sets them), else the last choice (localStorage, wrapped in try/catch), else Arabic and the device's scheme. The
header's switches change them in place and keep the address in step. **Every visible string exists in both
languages.**

**The review panel** (not part of the design): one small fixed panel, visibly outside the design (a dashed outline,
the corner opposite the header's actions), collapsed by default to a button «مراجعة / Review», with links to every
page and state above, and the «حالات تجريبية / Demo states» switch. Keep it out of the tab order until opened.

## 4. Quality — your gate before you report

The lead checks every direction at **390 and 1440 (and 768)**, Arabic and English, light and dark, and runs
`ui-review` and `anti-slop` on it. Before you report, check it yourself the same way:

- Capture with the lead's tool, **always through the grant script** (one headless Chrome at a time on this machine,
  shared with another worker), e.g.:
  `node C:\dev\masaha\workspace\TASKS\IDENTITY\scripts\heavy.mjs design-<a|b|c> node C:\dev\masaha\workspace\DESIGN\ROUND3\tools\shoot.mjs --dir <A|B|C> --pages home.html,spaces.html,spaces.html?filters=open,spaces.html?view=map,space.html?slug=branch-hub,login.html,about.html,account.html,favorites.html,404.html --widths 390,768,1440 --full`
  It writes `<dir>\shots\*.jpg` and `shots\report.txt` (overflow, contrast under 4.5:1, text under 12 px, missing focus
  style, broken images, console errors). **Look at the images** (Read them) — the report is not the review.
- **Pass means:** no horizontal overflow at 390 / 768 / 1440; text contrast ≥ 4.5:1 (3:1 for ≥ 24 px) in both themes;
  nothing under 12 px; every interactive element reachable by Tab with a visible focus ring; touch targets ≥ 44 px at
  390; the spark never text / never on an action; hover ≠ selected; no console error; both languages complete; the
  logo's rules kept; nothing from *Not in v1*; no invented data; the filters filter; it holds at 768.
- Then judge it as the owner will: **does it look like a real, strong product with a point of view — or like a
  template?** Run the `anti-slop` checklist and `frontend-design`'s list of generated-design tells on your own
  screens, and fix what you find. One element is the memorable thing; everything around it is disciplined.
- Keep each Chrome batch small enough (a page set, not everything at every width at once, when iterating); the final
  full run once. Never start a second Chrome while one of yours runs.

## 5. Limits

Write only inside your direction's folder (`directions\<A|B|C>\`). Never edit the repository (`C:\dev\masaha\app-*`),
`_shared\`, the other directions, or anything else in the workspace. No git, no commit, no install, no server, no
form submitted anywhere, no request to the live site (everything you need is in `_shared`). Never print a secret.
Never stop on the volume of work — finish all eight pages; if something cannot be done, say what and why.

## 6. Your report (your final message to the lead, and `directions\<X>\REPORT.md`)

What you built (the pages and states), how you checked (the runs, the widths, what the report said, what you saw and
fixed), what is weak or unfinished, every decision your direction overturns (it must match the `DESIGN.md`'s list),
the new copy you proposed, and anything you could not do. Short and true.
