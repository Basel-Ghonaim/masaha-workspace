# Lights («أضواء»)

**The Strip at night, and the spaces are the lights.** The sign-in sits on a calm panel at the start side; the rest of
the screen is a real map of the Gaza Strip, drawn from `strip-outline.json` and `spaces.json`, with every one of the
13 spaces at its real coordinates. In the dark theme each space is a softly lit window; in the light theme it is a
berry square cut like the two dots of the logo's ة, with a faint berry glow. A rounded inset, the way an atlas shows a
city, opens Gaza City's cluster of nine so each light carries its real name.

Open `index.html`. The page reads its state from the address: `?lang=ar|en`, `?theme=light|dark`,
`?state=wrong|toomany|offline|submitting|google|session|fields`, `?from=<space>` (for example `?from=elevate`, which
changes the way back to «العودة إلى إليفييت هاب» and makes that space's light a little larger and its name bold).

## The berry's role

**The berry means one thing: a space, a place where work goes on.** Its light on the map, the one button that signs
you in, and the place your keyboard is (the focus ring). Nothing else on the page is berry. The lights say where the
spaces are, never that they are open or have power: a mock-up can't know that, and seven of the thirteen have no hours
status in the data at all.

## Drawing the map for this place

A dark map with points of light on Gaza can read as a targeting display. This one is drawn to read as an atlas
instead, and it keeps to these rules:
- **No coordinates, ticks, rings, crosshairs or reticles** on screen. Gaza City is opened in a rounded box, not a lens.
- **Lights are soft windows** (a rounded square with a wide, faint glow), never hard pinpoints, and they fade up gently
  once; nothing flickers or flashes.
- **The Strip is land among land.** The sea is drawn west of the coast (the coast carried on in a straight line past
  both ends of the outline, a schematic); the land beyond the Strip's borders is plain and unnamed. The Strip never
  floats like an island.
- **Only true things are written on it:** the spaces' names and areas, four place names, the sea's name, and the
  count, 13.

## Colour

| Token | Light | Dark | Role |
|---|---|---|---|
| `--ground` | `#F7FBFF` (n-50) | `#0D1217` (n-950) | the panel |
| `--ink` | `#1A1F25` (n-900) | `#F7FBFF` (n-50) | text, the coastline in light |
| `--ink-2` | `#5E646A` (n-600), 5.8 : 1 | `#9FA6AD` (n-400), 7.7 : 1 | secondary text, placeholders, map labels' second line |
| `--field` / `--line` | `#FFFFFF` / `#767D84` (n-500, 4.0 : 1) | `#1A1F25` / `#767D84` (4.0 : 1) | inputs |
| `--hair` | `#DDE5ED` (n-200) | `#2C3137` (n-800) | separators only |
| `--berry` | `#B55BB3` (s-500) | `#D27ED0` (s-400) | a space; the focus ring (3.9 : 1 / 6.8 : 1, non-text) |
| `--berry-fill` / `--on-berry` | `#934791` (s-600) / `#FFFFFF`, 5.9 : 1 | `#D27ED0` / `#0D1217`, 6.8 : 1 | the sign-in button |
| `--sea` | `#DCE7F1` | `#070B0F` | the sea |
| `--land` | `#F7FBFF` | `#161E26` | the Strip |
| `--beyond` | `#EAEEF2` | `#0E1419` | land beyond the borders, unnamed |
| `--water` | `#3F6E99` | `#6F93B8` | waterlines along the coast |
| `--error` / `--error-bg` | `#BE222A` (r-600) / `#FEF4F3` (r-50) | `#FC6E68` (r-400) / `#370003` (r-950) | alerts and field errors |

Light and dark are two drawings: the day map is an engraved chart (ink coastline, paper land, blue waterlines, berry
squares with a faint glow); the night map is a dark Strip between a darker sea and the land beyond, the spaces lit like
windows, and the button giving off a little of the same light.

## Type

**Readex Pro** (Arabic and Latin in one variable file, 400–700, about 22 KB Arabic + 31 KB Latin). It comes from the
Lexend family, designed for reading ease; it is wide and calm, so it stays out of the map's way. Three reading sizes and
one title:

| Style | Size / line height / weight |
|---|---|
| title (h1) | 56 / 1.15 / 700 · phone 40 |
| lede, alert title | 18 / 1.75 (lede); 16 / 600 (alert title) |
| body, newcomers line, fields, buttons | 16 / 1.75 / 400–600 |
| labels, secondary, notes, errors, switches | 14 / 1.5–1.75 / 400–500 |
| map: inset title, place names | 14 / 600 |
| map: space names, area | 13 / 500, 12 / 400 |

English tightens line height to 1.6 and the title's tracking to −0.025em.

## Spacing and layout

8 px grid; gaps of 8, 16, 24 and 32. Desktop: `minmax(464px, 560px)` for the panel and the rest for the map. The panel
is one 400 px column (the header too), the width of Google's button, so every control lines up with it. The map is
sticky and fills the window's height; it is laid out by its own geometry, so it never mirrors, and in English it simply
sits on the other side of the panel. Phone (≤ 900 px): the header, then a 216 px band with the whole Strip, its four
place names to the east and the legend, then the form; Sign in stays above the fold on a 390 × 844 screen.

## Surfaces and shape

Flat. The panel is the page and the map is the picture. Radius 8 (controls), 12 (alerts), 16 (the inset). The inset is
the one raised thing, with a soft shadow, because it sits over the sea like a card laid on a chart.

## Components

- **Switches:** two 44 px pills, «English» (in Latin, `lang="en"`) and the theme (moon / sun, `aria-pressed`).
- **Google:** Google's own button, drawn as Google renders it: outline in light, filled black with the G on a white tile
  in dark; 40 px, 400 px max, Google's font stack, never restyled.
- **Fields:** 48 px, 8 px radius, label above, error below with an icon, the email typed left to right. Validation on
  blur, the error clears as soon as the value is right, a failed submit moves the focus to the first wrong field.
  Password has a «إظهار» / «إخفاء» toggle (proposal), 44 px tall inside the field.
- **Sign in:** 48 px, full width, `--berry-fill`. While it works it keeps its width, shows a spinner and
  «جارٍ تسجيل الدخول…» (proposal), and is `aria-busy` / `aria-disabled`, never disabled.
- **Alerts:** the error tint, `role="alert"`, focus moves to it. «تعذّر تسجيل الدخول» has a title and a line; too many
  attempts and no connection are one line; Google's failure sits under Google's button. The session note is neutral,
  above Google.
- **Newcomers:** below a hairline, «ليس لديك حساب؟ **إنشاء حساب**», then the owners' note with «تواصل معنا».
- **Small links** («نسيت كلمة المرور؟», «تواصل معنا») have a 44 px hit area drawn outside the text, so nothing moves.

## Motion

One moment: on first load the lights fade up, one after another from north to south, 1.2 s each, staggered 90 ms. Off
under `prefers-reduced-motion`. The spinner slows to 2.4 s a turn under reduced motion.

## Accessibility

Text ≥ 4.5 : 1 in both themes, placeholders included (measured, see the table); controls and the focus ring ≥ 3 : 1;
every target ≥ 44 px; every field labelled; the h1 is the page's title; the document title is «تسجيل الدخول · مساحة».
Keyboard order, checked by tabbing in Chrome: logo, language, theme, way back, Google, email, forgotten password,
password, show, Sign in, Create account, Contact us, privacy. The map is `aria-hidden` art; its legend is real text.

## What it keeps from the product's design system, and what it changes

**Keeps:** the ink and the neutral ramp (n-50…n-950) for every surface and text; s-500 / s-400 for the spaces and
s-600 for the button's fill; the status reds (r-600 / r-50, r-400 / r-950); n-500 input borders; Western digits;
logical properties; 44 px targets; the logo at 40 px, uncoloured, never mirrored; 16 px typed text; submit stays
enabled and focus moves to the first invalid field; underlined links in sentences; the document title pattern.

**Changes, and why:**
- *The spark on an action.* The system says the spark is never on an action. Here the one action that matters is the
  one thing lit, on purpose: the button is s-600 with white text (5.9 : 1), the only filled control on the page. If
  the owner keeps the rule, the button goes back to the ink and the page loses one note of its idea, not the idea.
- *The focus ring.* The system's ring is the ink; here it is the berry (3.9 : 1 light, 6.8 : 1 dark), because in this
  direction the berry marks "where you are".
- *The font.* Readex Pro instead of IBM Plex Sans Arabic: one variable file, and wider, so it stays legible next to a
  busy map at small sizes. Plex would also work; the map carries the identity.
- *The title.* 56 px, not `heading-1`'s 30 px: on a page with one job, the title anchors the panel.
- *Radius.* 8 px on controls rather than 6 px: slightly softer, closer to the logo.

## Proposed words (both languages)

| Where | Arabic | English |
|---|---|---|
| map legend | 13 مساحة عمل في قطاع غزة، كلٌّ في موقعه على الخريطة. | 13 coworking spaces in the Gaza Strip, each where it is on the map. |
| sea | البحر المتوسط | Mediterranean Sea |
| inset title, phone place | مدينة غزة | Gaza City |
| busy button | جارٍ تسجيل الدخول… | Signing in… |
| password toggle | إظهار / إخفاء | Show / Hide |

## Weight

About 61 KB of HTML (the logo is inline, 14 KB of it), no images, one font family. The map is drawn by 9 KB of script
from the 13 points and 22 outline points the page already carries, and redrawn on resize and on a language change.
