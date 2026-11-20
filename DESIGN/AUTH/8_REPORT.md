# Sign in — the new round (round 4): the designer's report

The designer: a Claude Code session, Opus 5.5. It started 2026-11-19 in `masaha-prototype`, on `main` at `96f7bc6`.
The brief: `7_NEW_DESIGNS_PROMPT.md`.

## § 1 Diagnosis

The current designs were looked at in Chrome at 1440 and 390, in Arabic and English, light and dark, before any
code was written. Captures: `D:\MASAHA\DT\AUTH\round4\existing\`.

### Why each existing design falls short of the owner's bar

**The original: a card in an empty page.**
- *Composition:* one 448 px block, centred both ways in a 1440 × 900 page. About 70 % of the screen is empty
  ground, and that emptiness has no job.
- *Hierarchy:* the card's title is 17–20 px over a 15 px line. Nothing on the page is larger than a label, so the eye
  has no place to start.
- *Surface:* a card with a border and a shadow, inside a header with its own line. On the phone that makes a frame
  inside a frame.
- *Brand:* the berry appears only in the logo's two dots. The page could belong to any product built on the same
  component library: it reads as the library's default.

**Slate: the form beside an ink panel with the Strip and a lens.**
- *Composition:* the panel is half the screen but carries only three things: a logo at the top, a drawing in the
  middle, and a block of words in the lower corner. Each sits on its own axis. The logo is centred on nothing, the
  drawing floats, and the words align to the corner the land leaves empty. That is what "parts unrelated" means
  here: no shared line, edge or grid ties them together.
- *Density:* the land is a diagonal band through the middle of a tall rectangle, so the two triangles it leaves are
  empty ink. That is the "half empty".
- *Meaning:* the lens works for nine dots, but there is no name, no north and no sea. A reader has to already know
  the shape to see Gaza in it.
- *The form side is sound.* The 8 px rhythm, the 40 px column and Google's real box are kept by every design below.

**Slate 2: a narrower panel, the Strip drawn large.**
- Cropping the Strip to fill the panel removes everything that makes it a place: both ends, the land borders, the
  proportion. What is left is a diagonal line with dots. The owner's "neither east nor west" is exact: without
  edges, a name or a sea, a drawing of a coastline is only a line.
- Moving the logo into the header was right. The panel's words still sit in a corner, with no relation to the
  drawing.

**What all three share.** The brand's idea is placed beside the form, not tied to it. The words of the panel never
point at anything in the drawing, and the drawing never points at the form. The fix is not a better drawing in the
same slot. It is a composition where each part is there because another part refers to it.

### What strong products do on a sign-in page (taken from, not copied)

- **Linear, Vercel:** one column with immaculate type and nothing else. The confidence comes from size steps and
  alignment, not decoration.
  - *Taken:* a real title scale, and one alignment edge that everything hangs from.
- **Stripe:** a full-bleed brand graphic behind the form gives the page energy.
  - *Taken:* the brand surface can be architecture (a band or a field), not a picture in a box.
- **GOV.UK** (the sign-in of a service with millions of users on every kind of phone and connection): a solid
  masthead with the crest, a heading, and the form under it, in one column. The new-user path is its own block,
  not a small link.
  - *Taken:* a masthead that holds the page's title, and "new here?" given a place of its own. Its weight on a weak
    connection is near zero.
- **GitHub, Amazon:** the second path ("New to …? Create an account") as a separate, equal block.
  - *Taken:* the two audiences (returning users, and new users or space owners) both answered on the page, not in
    the footer's small print.
- **Airbnb's and Booking's maps, and printed atlases:** a map reads as a place when it has names, a north and water,
  not when it is drawn larger.
  - *Taken:* name the places and the sea, show the north, and tie each name to its mark with a leader line, the way
    an atlas index does.
- **Careem and Anghami** (Arabic-first products): the Arabic layout is the design, not a mirror. The title has real
  size, and the start edge is the right edge, deliberately.

### What is specific to Masaha that a sign-in page can carry

- **Arabic first.** Titles set at a size where Arabic letterforms carry the page; one start edge (the right) that
  everything aligns to. English is the same layout read the other way.
- **Ink + berry and the logo.** The logo's two dots are rounded squares, not circles. A berry mark on these pages
  takes that shape too, so every berry mark rhymes with the logo. The berry marks a place (a space on the Strip) or
  what is current (the form you are on), and nothing else.
- **The Gaza Strip's coworking community.** The directory is a list of real places in Gaza City, Nuseirat, Deir
  al-Balah and Al-Mawasi. Their names are the directory's own areas, and the community knows them.
- **A weak connection and a phone first.** Inline SVG and CSS only, no image over a few KB, no motion. The phone
  layout is designed first, not shrunk from the desktop.

### The directions

**1. Atlas «الأطلس»: the Strip that reads as a place.** Slate's drawing fails because nothing on it can be read.
- *The idea:* the whole Strip, north up, uncropped, at a size where its shape is obvious. The sea to its west is
  hatched and named. A north mark sits at its head.
- To its east, a column of the directory's places (غزة · النصيرات · دير البلح · المواصي), each on a hairline drawn at
  its latitude, from the place's berry marks on the land to its name: an atlas index.
- The panel's question «أين تعمل اليوم؟» heads the index, so the words answer the drawing and the drawing answers
  the words. Every part refers to another.
- *Why it differs:* it keeps the ink panel the owner chose, but the panel is an index read top to bottom, not a
  picture with a caption. Its art is a labelled map, not a texture.

**2. Threshold «العتبة»: a masthead and two ways in.** No panel and no art.
- *The idea:* an ink masthead across the page, at every width, holds the logo, the tools and the page's title at
  display size.
- Under it, on the page's ground, two columns sit on one grid:
  - *Sign in:* the form, marked as the current path by the design system's own selected mark, a berry edge at its
    start.
  - *New here:* register's line, the "Create account" button, and the owners' note, from the catalogue.
- *Why it differs:* it answers "half empty" with function, not decoration: the width is spent on the page's two real
  audiences. Its brand is the ink masthead and the title's size. It is the lightest page of the round, and on the
  phone it is the masthead and a single column, designed first.

**3. Clearing «الفسحة»: the ground is the brand.** مساحة means an open space.
- *The idea:* the page is a field of the logo's own shape, small rounded squares on one grid. The form stands in a
  clearing of the field, with no card, no border and no shadow, only where the field stops. Two squares of the
  field in the berry stand over the clearing, as the ة's dots stand over the letter in the logo.
- *Why it differs:* no panel, no band, no map and no words of its own. The brand is the texture of the page and
  the gap in it.
- *The risk:* its composition is the original's, a centred form. It answers the emptiness, not the centring.
- *What it replaced:* the third direction was first **Emblem** (the logo's mark, large, on an ink panel). It was
  dropped before it was built, for the reasons in § 6.

The three differ in composition (a labelled map in a panel, a masthead over two columns, a field with a clearing),
in what carries the brand (place, function, the ground), and in what the berry marks (spaces, the current path,
the ة's dots over the form).

## § 2 The designs

Each design is `Sign in.html?v=<name>` on the supervisor's server (port 5410), listed in the page's switcher after
Slate and Slate 2. Add `&lang=en`, `&theme=dark` or `&state=…` to the address. Captures are in
`D:\MASAHA\DT\AUTH\round4\`, named `<design>-<width>-<lang>-<theme>[-<state>].png`.

### Atlas «الأطلس»: http://localhost:5410/Sign%20in.html?v=atlas
- **The idea:** the whole Strip as a place you can read: north up, its sea hatched and named, a north mark. To its
  east, an index of the directory's places (غزة · النصيرات · دير البلح · المواصي), each on a parallel from its spaces
  to its name, under «أين تعمل اليوم؟».
- **Look first at:** 1440 in Arabic, light (`atlas-1440-ar-light.png`). Then 390 Arabic: the same panel closes
  the page under the form.
- **Weak points, honestly:**
  - Gaza City's nine are a cluster at every width, and two or three of them touch. With no lens they read as "many,
    in Gaza City", not as nine.
  - Place names are a proposal against the earlier rounds' "no place names".
  - At 1920 the parallels are long (about 350 px).
  - On the phone the panel adds about 530 px of scroll under the form.
  - It is a third design with the Strip. If the owner is tired of the map itself, rather than of an unreadable
    one, this is not the answer.

### Threshold «العتبة»: http://localhost:5410/Sign%20in.html?v=threshold
- **The idea:** an ink masthead at every width holds the logo, the tools and the title at display size. Under it
  are two ways in on one grid: the form, marked as the current path by a berry edge at the masthead's foot, and
  the way for a new account and for owners, in the catalogue's words.
- **Look first at:** 1440 in Arabic, light (`threshold-1440-ar-light.png`). Then 390, where it is the phone's
  most natural page.
- **Weak points, honestly:**
  - It has the least "character" of the three. Its brand is the ink, the title's size and one berry edge, so it
    can read as a well-made service page rather than a crafted one.
  - At 1440 × 900 about 190 px of plain ground stays under the grid.
  - The berry edge's meaning (the current path) is the design system's, but a visitor may read it as decoration.
  - Sign in now carries register's line and owners' note: production's words, from another page.

### Clearing «الفسحة»: http://localhost:5410/Sign%20in.html?v=clearing
- **The idea:** the page is a field of the logo's rounded squares, and the form stands in a clearing of it, whole
  squares at a time. Two berry squares above the clearing are the ة's dots.
- **Look first at:** 1440 in Arabic, light (`clearing-1440-ar-light.png`). Then `?state=google`, where the
  clearing grows with the alert.
- **Weak point, honestly:** this is the weakest of the three, and it is shown as the quiet option.
  - Its composition is the original's: a centred form, with the empty page now a textured ground.
  - The field can read as graph paper.
  - The two berry squares over a rounded gap echo the logo's ة, but a viewer could also see a face.

## § 3 My recommendation

**Atlas.** It is the only design that answers the owner's own words point by point:
- "nothing can be understood from it": now the drawing has names, a north and a sea;
- "half empty" and "its parts unrelated": now every part of the panel points at another: the question → the
  names → the parallels → the berry squares → the key;
- "not professional": the form is Slate's, already polished and approved.

It keeps what the owner chose in Slate (the ink panel, the dot-grid land, the bright coast, the berry spaces). It
also keeps the strongest thing Masaha has that no other product has: real places in the Gaza Strip. I would build
it in masaha with the dots and names read from the directory, as the decision file says.

**If the owner wants no map at all, Threshold.** It is the most "real product" of the three, the lightest on a
weak connection, and the best on the phone. I would not choose Clearing.

## § 4 What I checked, and what I could not

**Checked**, in headless Chrome through the grant script, on port 5410, with reduced motion on:
- **Every design's default,** full page, at 390, 768, 1280, 1440 and 1920, in Arabic and English, light and dark:
  60 captures.
- **Every state** (`error`, `google`, `ratelimit`, `offline`, `loading`, `idle`) at 390 and 1440, in Arabic and
  English, light and dark: 144 captures. The fields are prefilled where the kit prefills them, and the
  rate-limit's disabled button has its reason above it.
- **Overflow:** `scrollWidth` equals the width in all 204 captures.
- **The probe** (`report-defaults.txt`, `report-states.txt`): no text under AA, no text under 12 px, no small
  targets, no console errors.
- **Contrast of the berry marks,** computed from the tokens (they are not text):
  - `spark-400` on the ink: about 6 : 1;
  - `spark-500` on `neutral-50`: about 3.9 : 1;
  - `spark-400` on dark: about 6.8 : 1.
- **Focus:** the focus ring on the logo and the language tool at 1440, light and dark, in each design. It is white
  on Threshold's masthead.
- **A failed submit** focuses the email field (`aria-invalid=true`) in all three, at 390, light and dark
  (`round4\focus\`).
- **Slate, Slate 2 and the original** were captured before any change (`round4\existing\`) and again after the
  last commit, at 1440 and 390, in both languages and themes. All 24 are pixel-identical.
- `check-parse` and `check-classes` passed before each commit.

**Not checked:**
- The states at 768, 1280 and 1920. Only the defaults were seen at those widths.
- 44 px targets on a touch tablet (`pointer: coarse` at 768 and above). Touch was emulated below 768 only.
- Motion with reduced motion off. These designs add no motion; the kit's waiting bar is unchanged.
- Safari and Firefox, a real screen reader, a real phone.
- The other auth pages. The brief is Sign in only.
- `Auth lab.html`: its design list is its own and was not changed. It does not list Slate 2 either.

## § 5 Commits

On `masaha-prototype` `main`, local only, not pushed. The two earlier local commits were left as they were.

| Hash | Subject |
|---|---|
| `d65ef9f` | feat(sign-in): add the Atlas design |
| `0b9b43c` | feat(sign-in): add the Threshold design |
| `f140f8a` | feat(sign-in): add the Clearing design |

Each commit holds its design's part of the kit (`_auth/kit.jsx`), its stylesheet (`_auth/<name>.css`), its two
variant files, its registry line and its section in `decisions/auth.md`. The kit was split by design, so each
commit stands alone. In Atlas's commit, the sign-in function is the previous one, unchanged.

## § 6 What I was unsure of

- **Emblem was dropped before it was built.** It was the third direction in § 1: the logo's mark, large, on an
  ink panel.
  - On a closer look it was "a logo and a few words": A3's plain panel, the thing the owner had already turned
    down.
  - The mark's file is also 28 KB (about 7 KB compressed), since it carries the whole logo clipped.
  - Clearing took its place. It is weaker than I hoped (§ 2), and no fourth design was built. I preferred three
    honest designs to a fourth that would repeat one of them.
- **Gaza City's name in Atlas.** The snapshot files Golden Hub under «شمال قطاع غزة», but its coordinates are in Gaza
  City. So the nine are named by their governorate, «غزة» ("Gaza City"), not by their areas. The data error is in
  production's directory, worth a report there.
- **Place names on the drawing** reverse an earlier round's choice. Is that the owner's to settle? I think it is
  what makes the map readable.
- **Threshold puts register's line and owners' note on Sign in.** These are production's words from another page.
  The catalogue has them, but `signIn` does not.
- **The panel's words** (the question, Slate 2's line, the key) are still the earlier rounds' proposals. Atlas
  reuses them and adds three of its own (the north mark, the sea's name, the index's assistive name). All are in
  the decision file's *New words* table.
- **The server:** I used the supervisor's server on 5410 throughout and started none of my own. No port to free.
