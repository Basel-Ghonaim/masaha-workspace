# IDENTITY — palette lab, round 3 (the same OpenCode session in app-b)

The owner's review of the lab (2026-11-05, screenshot of `?palette=sunset&theme=light&screen=owner&device=desktop`):
the page is cramped and confusing, and he wants **10 more palettes**. Same rules as before: **new files only**
(`Palette lab.html`, `masaha/palette-lab.js`), no prototype file edited, no PR, no push, both checks, fold into the
lab's commit (`git branch backup/palette-lab-3` first, `--fixup` + `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash
origin/main`).

## 1. Bugs seen in the screenshot (fix first)

1. **The theme control says Light but the preview is dark.** The preview must always follow the lab's theme
   control: on every iframe `load`, set the iframe's `document.documentElement.dataset.theme` to the lab's value and
   keep `?theme=` in the iframe URL; a prototype page's own theme toggle or stored state must not win.
2. **Mixed-direction names break:** «غروب البحر 3 (Sea sunset 3)» renders as «(Sea» / «sunset 3)». Put the English
   name in `<bdi dir="ltr">`, on its own muted second line.
3. **Ghost elements:** faded/blurred blocks under the palette row and beside «المظهر». Remove whatever draws them.
4. **Nested scrollbars and a cropped preview:** the scaled page shows its own scrollbars inside the frame. Fix it:
   the preview fits the available width; the iframe's height is the page's full scaled height (read the inner
   document's `scrollHeight` after load and on resize), so the lab page scrolls once and nothing is cropped.

5. **"Desktop (1440)" shows the tablet or phone layout** (Home shows the hamburger menu, especially in «الاثنين
   معًا»). The page's media queries read the **iframe's own width**, so the iframe must be exactly 1440 px wide (390
   for the phone) and only then scaled down with `transform: scale(containerWidth / 1440)` and
   `transform-origin: top right` (RTL), inside a wrapper whose size is the scaled size. Never size the iframe to the
   container. Verify Home, the directory and the owner's overview show their desktop layout (sidebar, full header) in
   «الاثنين معًا» at a 1280 px window.

## 2. The new layout

- **A sticky toolbar** at the top, one row from 1024 px (wrapping cleanly below): the lab's title; then labelled
  segmented controls — «المظهر»: فاتح · داكن · الاثنين معًا; «الجهاز»: سطح المكتب · الهاتف; «الشاشة»: a Select of the
  screens; «مقارنة» (see below); «نسخ القيم».
- **The palette gallery** below the toolbar, as a grid of cards (4–6 per row on desktop, 2 on a phone), grouped under
  small headings: «الحالية», «عائلة الغروب», «دافئة», «باردة», «حر». Each card: the Arabic name (one line), the English
  name muted under it, a strip of **four large swatches** (brand-600, brand-400, neutral-50, neutral-900), a contrast
  summary (✓ 38/38 or ✗ N), and a small clash note when the brand hue is within 25° of a status colour. The active
  card has a clear ring. A ☆ on each card marks it as a favourite (kept in the URL `?fav=a,b,c`); a «المفضّلة فقط»
  toggle filters the gallery to them.
- **Compare mode:** «مقارنة» shows two palettes side by side on the same screen and theme (two Selects choose them,
  defaulting to the active palette and the first favourite). URL `?compare=sunset,dusk`.
- **The preview** takes the full content width under the gallery; in «الاثنين معًا» light and dark sit side by side
  (stacked below 1280 px). A caption above each frame names the palette, the theme and the screen.
- **Ramps and contrast** move into a panel that opens from the active card («التفاصيل») or a button in the toolbar,
  so the preview is not pushed down. Keep the Status check screen from round 2.
- The lab's own chrome stays neutral (it does not take the palette being previewed), built with the semantic
  variables only, readable in both themes.

## 3. Ten new palettes

Same generator (lightness from Sea, hue and chroma from the seed, gamut-clamped). Brand seed / neutral hue + peak
chroma / group:

1. «غسق الغروب» (Sunset dusk) — `#C2492F` / 290, 0.016 — عائلة الغروب
2. «طين وبحر» (Terracotta & sea) — `#B4532A` / 220, 0.014 — عائلة الغروب
3. «برتقال محروق وأردواز» (Burnt orange & slate) — `#B85A1E` / 240, 0.014 — عائلة الغروب
4. «ورد وطين» (Rose clay) — `#B5525F` / 30, 0.010 — دافئة
5. «رمّان» (Pomegranate) — `#9E2B45` / 20, 0.008 — دافئة
6. «برقوق وحجر» (Plum & stone) — `#6B3A6E` / 60, 0.010 — دافئة
7. «كحلي ورمل» (Navy & sand) — `#1F4E79` / 80, 0.010 — باردة
8. «أزرق المتوسط» (Mediterranean) — `#1C6BA0` / 230, 0.012 — باردة
9. «نيلي الليل» (Night indigo) — `#3A3F8F` / 260, 0.014 — باردة
10. «غابة وكتّان» (Forest & linen) — `#2E5E3E` / 85, 0.010 — باردة

Regroup the existing ones: «الحالية» Sea; «عائلة الغروب» Sea sunset, 2, 3 + 1–3 above; «دافئة» Clay & stone, Sage &
clay + 4–6; «باردة» Olive & ink, Indigo & sand + 7–10; «حر» Free colour. If a palette fails contrast pairs, keep it,
show ✗ N on its card, and list the failing pairs in the report — do not silently retune it.

## 4. Check and stop

Open the lab at 1440 and 390, Arabic, light and dark: no overflow, no nested scrollbar, no ghost element, the theme
always matching the control, every palette card readable. Both checks pass. Screenshots into
`C:\Users\basel\Downloads\palette-lab-shots\round3\`: the gallery (desktop, phone), compare mode (sunset vs dusk, both
themes), the details panel. Stop and print `git log --oneline origin/main..HEAD` and the URLs (the gallery, compare,
each new palette on Home).
