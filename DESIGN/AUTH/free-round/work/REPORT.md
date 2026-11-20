# Report: the sign-in page, free round

Three directions, each in Arabic and English, light and dark, at 1440 and 390, with every state working.
Open `work/index.html` for one-click links to everything; the captures are in `work/captures/`.

## The three directions

**Lights («أضواء»)** · `work/lights/`
The image is the place itself: a true map of the Gaza Strip with the 13 spaces as soft lights at their real coordinates,
and Gaza City opened in an atlas inset with every space named. The berry means one thing, a space: the lights, the
sign-in button and the focus ring are the only berry on the page. Quiet, readable type (Readex Pro) and the lightest
page of the three.
*Look first at* `lights-1440-ar-dark.png`, then `lights-1440-en-light.png` and `lights-390-ar-light.png`.

**Berry («توت»)** · `work/berry/`
The logo's berry is the whole page, the title is Kufam Black at 148 px, and the form is one paper sheet laid on the
colour. Along the bottom, one long shared table: tea going round, a router, laptops with the ة as a sticker, every
socket taken; at night the room goes plum and the screens light the faces. Every colour comes from the system's ramps;
text on the berry is the ink's darkest step, so the page is the logo's two colours.
*Look first at* `berry-1440-ar-light.png`, then `berry-1440-ar-dark.png` and `berry-390-ar-light.png`.

**Notebook («كرّاسة»)** · `work/notebook/`
A squared exercise book open at two pages, one for each way in. The title is written in Ruqaa and underlined in berry
pen; every line of print stands on the ruling; errors are written in red pen with a mark in the margin. The berry is the
pen, and the facing page carries a pen sketch of a real desk (lantern, laptop, sage tea, a full power strip).
*Look first at* `notebook-1440-ar-light.png`, then `notebook-1440-ar-light-wrong.png` and `notebook-1440-en-dark.png`.

## Each one's weakest point

- **Lights.** The panel is the plainest of the three: a well-made form that, on its own, could belong to anyone. All
  the character is in the map, so on a phone, where the map is a 216 px band, the idea is much smaller. The light theme
  is quieter than the dark one. And the map rests on the brief's approximate outline: fine at this scale, crude if
  anyone ever zooms in.
- **Berry.** It lives at the colour's limit. Text on the berry passes AA at 4.6 : 1 with almost no margin, so any lighter
  berry, any opacity or a thinner weight breaks it. The drawing is hand-coded SVG: it has charm at full size, but before
  it ships an illustrator should redraw it. It carries the heaviest fonts (about 160 KB until Kufam is subset), and it
  is the furthest from the system's "calm, no playful styling".
- **Notebook.** Three new typefaces, and Markazi is small for its size, so text is set large and the phone page is long
  (about 1,400 px at 390). Ruqaa is beautiful at title size but may tire some older readers; the notebook metaphor
  speaks to students more than to space owners and their staff, who also sign in here.

## Recommendation: Lights

It is the only one whose image could belong to no other product: the real Strip and the real 13 spaces, each where it
is. Everything on it is true, it says nothing a mock-up cannot know, and it carries into the rest of Masaha (the
directory's map, the home page, a space's page; arriving from a space already lights that space on the map). It also
keeps the design system almost whole: only the button's fill and the focus ring change, and it is the lightest on the
network. The reviewer's warning made it better: it is now drawn as an atlas, never as a display.

If the owner wants the boldest first impression instead, choose **Berry**: it is the most memorable at a glance, but it
bends the system the most and needs a real illustrator. Whatever is chosen, Notebook's red-pen error is the best error
state of the three and could be borrowed.

## What I could not check

- **Real devices and other browsers.** Every capture is headless Chrome on Windows. The 390 captures are a true 390 px
  layout through Chrome's device emulation, at 1× pixels. Nothing was seen on iOS Safari, Android Chrome or Firefox.
- **A real weak connection.** Fonts load with `display: swap`; I measured their sizes but did not throttle a network.
- **Screen readers.** Labels, roles, live alerts, focus moves and the tab order are in the markup and the tab order was
  walked in Chrome, but there was no NVDA, VoiceOver or TalkBack session. Forced-colours mode and 200 % zoom were not
  tried.
- **Google's real button.** It is drawn to Google's published styles; the real button renders its own Arabic font and
  may place the G differently in right-to-left.
- **People in Gaza.** Whether the map, the table and the notebook read as intended, above all the map, is a question for
  people there. I avoided what I could foresee; I can't see everything.
- **Motion.** Captures freeze animation; the lights' fade-up and the router's slow blink were checked in code only.
- **Tablets.** 1024 and 768 were spot-checked in Arabic only (they work, after one fix to Lights); they are not part of
  the hand-over captures.
- **Kufam subset with `&text=`.** Suggested in Berry's DESIGN.md, not tested.

## Notes for the owner

- **The data, as given.** «جاردن سبييس» and «إليفييت هاب» are shown as spelled in `spaces.json`; "coma,io" keeps its
  comma; Golden Hub is listed as North Gaza Strip but its coordinates sit in Gaza City's cluster (Lights shows it there,
  in the Gaza City inset). Worth correcting in the data, not in the page.
- **Proposed words** are listed in each DESIGN.md: the busy label «جارٍ تسجيل الدخول…», the password toggle
  «إظهار / إخفاء», Lights' legend and place names, and Notebook's margin note «لأصحاب المساحات». Everything else is
  production's words.
- **States.** Every page reads `?state=` (`wrong`, `toomany`, `offline`, `submitting`, `google`, `session`, `fields`) and
  `?from=<space>`; the forms also work by hand (validation, busy, then wrong credentials, then too many attempts on the
  third try). Besides the 36 hand-over captures, `work/captures/` has the other five states at 390 Arabic light and the
  "came from a space" state at 1440 for each direction.
- **How the captures were made.** The brief's `chrome --screenshot --window-size=390,…` does not work for phones:
  headless Chrome will not lay out a window narrower than 500 px, so it renders a 500 px page and crops it. I captured
  through Chrome's DevTools protocol instead (`work/tools/capture.mjs`): same Chrome, same profile folder, one Chrome at
  a time with free memory checked first, the viewport sized to the page's measured height and captured as a viewport,
  never a full-page capture.
- **Rebuilding.** Sources are in `work/src/`; `python work/tools/build.py` writes the three self-contained pages,
  `python work/tools/frieze.py` and `sketch.py` redraw the two illustrations, and `node work/tools/capture.mjs <direction>
  all` redoes a direction's captures. `work/chrome-profile/` (22 MB) is only the capture browser's profile and can be
  deleted.
