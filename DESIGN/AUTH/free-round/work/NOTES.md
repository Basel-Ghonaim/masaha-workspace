# Notes: before drawing

## What I see in the three references

**Tabby.** The green is not a colour on the page, it *is* the page: there is no white sheet, no hero box, no
"brand area". Everything sits directly on the colour, and black is the only other ink. The headline is short, heavy
and centred, with the confidence of a sign over a shop. Then there's the crowd: dozens of the same small coin-headed
figures, drawn in thick black line, marching off the bottom edge. One character repeated many times turns into a
texture, and each figure is still slightly different, which gives it warmth. The illustration is funny without telling
a joke. What I take from it: commit to the colour completely, and let one repeated, characterful figure carry the
warmth.

**Careem.** It sells the city, not the app. Real ground (Dubai at night), and only one thing in the brand's colour:
the streets the product moves along. Green there means "this is where we are". The wordmark sits in the middle of that
world, and a small card ("the captain is on the way · 3 min") makes it feel live. The darkness is a stage for one
glowing colour. What I take from it: the product's real world as the image, and the brand colour used *as a
signal* rather than as decoration.

**Thmanyah.** Editorial patience. A quiet ground, a typeface with its own handwriting, generous gaps between things,
and illustrations that are clearly drawn by a person (flat colour, a confident wobbly line, a sense of humour in the
pose). Colour is spent tiny and exact: the orange is only on author names. It trusts reading. What I take from it: the
craft of Arabic type at text size, hand-made images instead of stock, and colour spent like ink, in small precise
amounts.

**What they share.** Each one owns a single thing completely (a colour, a city, a voice) and is calm about everything
else. None of them hedges. And in all three, Arabic is not a translation: the Arabic headline is the design.

## What is true about Masaha (where the character has to come from)

- **«مساحة» means space, and the logo already knows it.** The ة is a rounded square with a square hole in it: a room
  seen from above, or a socket, with two berry dots. The two dots are the brand's whole colour story.
- **Power and internet are the scarce things.** A space that is open, lit and connected right now is news. Light is
  not a metaphor here; it is literally the service.
- **The ground is real.** Thirteen named spaces with coordinates; an outline of the Strip, north up, the sea on the
  west. Eight of them in Gaza City (Al-Rimal 4, An-Nasr 2, Al-Daraj 2), one listed as North Gaza, two in Nuseirat, one
  in Deir al-Balah, one in Al-Mawasi. I can draw the real thing and every number on it will be true.
- **The people are students, freelancers and remote workers on phones.** Long shared tables, a power strip with every
  socket taken, a router with its antennas, a glass of tea. The school notebook. Everyday life and work going on.
- **Arabic first.** The page is designed right to left; English mirrors it through logical sides.
- **Constraint I found by measuring:** the brand berry `#B55BB3` is a mid-tone. Ink on it is 4.04 : 1 and white on it
  is 4.11 : 1, so *no* small text can sit on the exact berry. Every direction needs an honest answer for that, and the
  three answers are different (see each DESIGN.md).

## Three directions

### 1 · Lights («أضواء») — the Strip at night, and the spaces are the lights

The page is split: the sign-in panel on the start side, and on the end side a real map of the Gaza Strip drawn from
`strip-outline.json`, north up, the sea against the page's edge. In the dark theme the land is a deep blue-black and
the thirteen spaces are berry lights with a soft halo, placed at their real coordinates; a round loupe over Gaza City
opens the eight-plus-one cluster so each light carries its real name. In the light theme it becomes the day map: pale
sea, paper land, ink coastline, and the lights become solid berry squares cut like the two dots of the ة. **The brand is
carried by the place.** **The berry means one thing only: a space, a light that is on.** It appears on the markers and
on the one button that turns you on (sign in), and nowhere else. **The type is quiet and wayfinding**: Readex Pro, a
wide, very readable Arabic and Latin face from the Lexend family, in two weights, so the map does the talking. One
orchestrated moment: on load the lights come on one by one, the way generators start across a city in the evening
(and only once, and not at all under reduced motion).

### 2 · Berry («توت») — the colour owns the page, and the people sit at one long table

No white page at all. The whole ground is the logo's berry, and on it the title «تسجيل الدخول» is set in Kufam Black at
monumental size, a heavy geometric Kufi that is a close cousin of the logo's own letters, so the headline and the mark
feel cut from the same block. The form is a single paper sheet laid on the colour. Along the bottom runs a long
drawing of one shared work table, as wide as the screen: a woman in a hijab typing, a student in headphones, someone
pouring tea, a guy asleep on his arms, laptops with the ة as a sticker on their lids, all of them plugged into one
power strip, and a router in the middle. Thick ink line, paper fills, the Tabby spirit of characters with personality
without copying its crowd. **The brand is carried by the colour and by the people.** **The berry is the ground**, so
text on it is either monumental (large text, where 4 : 1 is enough) or sits on ink and paper chips. At night the room
goes dark plum and the laptop screens light the faces. **The type is loud and sure**: Kufam for display, IBM Plex
Sans Arabic for everything you read (kept from the product, so only the voice changes).

### 3 · Notebook («كرّاسة») — a student's squared notebook, written by hand

The page is a sheet of squared paper: the 8 px grid made visible as a 24 px square ruling in pale blue, with a double
berry margin rule down the start side, the way Arabic exercise books have their margin on the right. It is laid out
as an open spread with two pages, and the two pages are the two ways in: the first page (right, in Arabic) is for people
coming back and holds the form; the facing page is for people new to Masaha, with the owners' note, and a hand-drawn
ink sketch of a real work desk (laptop, a glass of sage tea, a phone charging from a crowded power strip). The title is
written, not typeset: «تسجيل الدخول» in Aref Ruqaa, the hand every Palestinian learned to write in at school, over a
printed body in Markazi Text, a naskh made for reading. **The brand is carried by the hand and the craft of the
type.** **The berry is the pen**: the margin rule, a handwritten note in the margin, the line that underlines the new
path, the focus ring, and the one primary button, like a stamp. Thmanyah's spirit (paper, a typeface with a voice,
drawing instead of stock) without its look.

## Review of the plan against the generic defaults

I ran each plan against "what would I produce for any sign-in page" and changed what matched:

- *Lights* first had a hand-drawn street grid glowing in berry (Careem's streets). I removed it: I don't have street
  data, and the brief says anything that looks like data must be real. The coastline and the thirteen real points
  are enough, and they are true. I also rejected a monospace face for map labels (a known tell); labels are set in
  the same Readex Pro.
- *Berry* first put the berry on a white page as a big left-side panel, the split-screen SaaS sign-in. That is the
  default answer, so the colour now covers the entire ground, and the form is the only paper.
- *Notebook* risked the cream-paper-plus-serif cliché. The paper stays the brand's own cool `#F7FBFF`, the ruling is
  blue like a real exercise book, and the accent is the berry pen, not terracotta. The hand is Ruqaa, which is
  specific to this place, not a generic "handwritten" Latin script.
- None of the three uses eyebrow labels above headings, numbered markers, middle-dot meta strings or a "→" on buttons.
- Numbers shown are only ones I can count in `spaces.json`: 13 spaces; 8 in Gaza City's neighbourhoods, 2 in
  Nuseirat, 1 in Deir al-Balah, 1 in Al-Mawasi, 1 listed as North Gaza. No "open now" anywhere, because a mock-up cannot
  know it, and the snapshot is from 2026-11-14.

## Things I decided without asking

- **The h1 stays «تسجيل الدخول».** The brief asks for the page title as the h1, and in all three the title itself is
  the display type, rather than a slogan with a small title under it.
- **Google's button is drawn as Google renders it**: light "outline" (white, `#DADCE0` border, `#3C4043` text) and dark
  "filled black" (`#202124`, white text, G on a white disc), 40 px tall, Google's own font stack, no restyling to the
  direction. It is the one element that must look foreign, and that's what makes it trustworthy.
- **Proposed words** are marked "proposal" in each DESIGN.md. The production words are used wherever they exist.
- **UXKIN was not connected,** so the directions come from the owner's three references, the brief and the product's
  data, not from a survey of other sites.

## After the first draft: the second opinion, and what I did with it

I asked a reviewer who had not seen my reasoning to look at the captures and the code through
`ui-design-review:ui-review` and the Vectorlab `anti-slop`, `typography` and `spacing` skills, and I read
`foundation-reference.md`. I took what made each direction stronger and left what would have made it blander.

**Taken, because they were right:**
- *Lights could read as a targeting display.* A dark map of Gaza with pinpoint glows, degree ticks and a round lens on
  Gaza City is exactly the wrong picture for this audience. The ticks and graticule are gone, the lens is now a rounded
  atlas inset, the lights are soft windows that fade up (no flicker), and the legend no longer implies every space has
  power: «كلٌّ في موقعه على الخريطة», "each where it is on the map".
- *The Strip floated like an island* because the land beyond its borders used the sea's colour. The sea is now drawn
  only west of the coast, and the land beyond is plain and unnamed.
- *Notebook's LED lantern read as a walkie-talkie,* an object with a terrible recent history in the region. It is
  redrawn as a plain lantern with a ring handle, a bulb and drawn light.
- *Berry's waving woman read as startled* (a black hood, an "O" mouth, motion marks). She now wears a light scarf with
  folds and smiles; the figures vary in height and width, with noses and brows, and only three laptops carry the sticker.
- *Focus order.* Berry's DOM put "Create account" before the form; Notebook's switches lived in one page and rendered on
  the other. Both are fixed, and all three were checked by tabbing in Chrome.
- *Notebook's text didn't stand on its own ruling.* Squares are now 16 px with 32 px leading, every block is on the
  grid, the ruling is shifted to Markazi's measured baseline, and both titles share a rule.
- *Notebook's error state was a stock pink box,* the one place the notebook disappeared. Errors are now written in red
  pen with a mark in the margin.
- *Notebook's English hand was a children's school font.* It is now Kalam, an adult hand.
- Smaller ones: placeholders at full contrast; Lights' header aligned to its column; 8 px rhythm and three text sizes in
  Lights and Berry; Berry's "Create account" outlined at night; Berry's phone crop shows whole people and a whole strip.

**Taken from the product's design system:** every colour now comes from its ramps where one passes (s-600 `#934791`
for berry behind white text instead of my own; n-950 for text on the berry; the system's reds and neutrals). The logo is
never recoloured: on Berry's berry ground it sits on a paper tab. Each DESIGN.md lists what it keeps and what it
changes.

**Left, on purpose:**
- Making Berry's illustration "less uniform" by dropping the two-ink style: the sameness of line is the style, and it
  keeps the drawing from being about anyone's skin.
- Making Notebook's running text one line per two squares (48 px leading): 32 px leading on a 16 px ruling gets every
  line onto a rule without double-spacing the page.
- "coma.io": the page already shows the data's own "coma,io". The data's spellings («جاردن سبييس», «إليفييت») and Golden
  Hub's area are reported to the owner rather than corrected in the page.
