# The auth pages' design — the owner's decisions (2026-11-15)

Page by page, in the prototype's own repository (`masaha-prototype`), each design a `?v=<name>` variant of its page,
the original untouched. The critique's confirmed points: `1_CRITIQUE_CHECKED.md`.

- **A1 — the layout direction (approved):** not a card centred in an empty page.
  - **From 1280 px:** two columns. The form on the start side (right in Arabic), **no card**. The other side is an
    **ink brand panel**: the logo, a confident title, one line saying what an account gives, and **the Strip** —
    round 3's direction B drawing (`DESIGN\ROUND3\directions\_shared\data\strip-outline.json`) — drawn full height.
  - **768–1279 px:** one column, the form starting at a fixed offset from the top (no vertical centring).
  - **The phone:** the form at full width, no card and no frame; larger fields and buttons; a clearer title; the
    Strip at most as a small touch.
- **A2 — the Strip's conditions:** an artistic drawing, not an official map (no governorate borders as fact, no
  geographic detail held to accuracy); its dots are **real spaces** from the directory's data, in the berry, or no
  dots at all — never decorative fake ones; light on the network (an inline SVG, no image).
- **A3 — not chosen:** a photo (the owner's word), a product glimpse, a plain text panel ("not a beginner's design").
- **A4 — order:** the variant's prompt is written **after PROTOTYPE_SPLIT's PR merges**; sign-in first, then the
  other auth pages if the owner likes it.
- Copy (the title's wording) is settled with the owner when the variant is shown.
- **A5 — the output (the owner, 2026-11-15):** **three designs** applied to **every auth page** (sign in, register,
  forgot, reset, the forced change, the reset e-mail), with their states, switchable through **one simple
  dashboard-like page** (`Auth lab.html`); the prompt complete and self-contained (`2_VARIANTS_PROMPT.md`). It starts
  now, beside #147 (the prototype is its own repository); it never edits that repository's `README.md` / `CLAUDE.md`.
  A lead (Claude Code, Opus high) + up to three sub-agents, one per design.
- **A6 — the choice (the owner, 2026-11-15): «اللوح» Slate**, "the one I like most, but with errors and things to fix
  so it looks more professional". Coast and Dots stay in the lab as they are, with no further work. A Slate-only
  polish round (`6_FIX_ROUND.md`): the review's Slate items (F3, F4, F6, F7, F10, F13–F16) and the supervisor's
  points (a crafted Strip instead of a flat slab, countable dots, the dark panel not a grey card, the phone's brand
  touch, the 8 px rhythm, the sign-in button's arrow).
- **A7 — the owner's points (2026-11-15):** the foot's links and register's owners' note centred; **the password
  conditions as one line** that says, before typing, «8 أحرف على الأقل، فيها حرف ورقم», while typing only what is
  missing, and once met «✓ كلمة المرور مناسبة» (the supervisor's recommendation; a row of three ticks rejected).
- **A8 — the Strip drawing (the owner, 2026-11-15):** a mix — **the dot grid** («Dot Field»), **a bright coastline
  with faint sea lines**, **the lens** over the sea magnifying Gaza City, and **the berry dots at the real spaces**
  (the prototype's). ChatGPT's images were references only. **The supervisor draws it himself** (the owner's wish, so
  the two can iterate): `DESIGN\AUTH\strip\make_strip.py` → `strip-*.svg` / `.png` (round 3's approximate outline;
  the snapshot of 2026-11-14). **Approved by the owner (2026-11-15).** The pages use **`strip.svg`**: no background,
  every colour a CSS custom property (`--strip-panel`, `--strip-grid`, `--strip-sea`, `--strip-coast`,
  `--strip-space`, `--strip-lens`) with the tokens as fallbacks, so one inline SVG follows the theme; the
  `strip-*.svg/png` with backgrounds are previews only.
- **A9 — applied by the supervisor himself in masaha-prototype (the owner's word, 2026-11-15), not by a worker:**
  Slate's panel draws the mix (dot grid, coast, three sea lines, the berry lens fully over the sea, ×3.5); the
  phone's small Strip mark removed (it read as a stray icon). **The dark panel:** the berry tint was tried and
  rejected by the owner (two blacks of different hue, and lighter than the page); the rule is **the panel is the
  deepest surface in both themes** — in dark a step deeper than the page in the same cool ink
  (`neutral-950` 70 % with black).
- **A10 — Coast and Dots retired (the owner, 2026-11-19):** "we won't adopt them". Removed from the prototype by the
  supervisor (masaha-prototype `b84fc7f`, local). The designs now: **the original, Slate, Slate 2**.
- **A11 — Slate 2 and the owner's look (2026-11-19):** the owner found Slate's panel half empty and its parts
  unrelated; the supervisor drew **Slate 2** on Sign in (`96f7bc6`, local): a 5 : 7 panel, the Strip larger than the
  panel with no lens, one word block, the logo in the page header. The owner's verdict: **no count of the spaces**
  ("it will change, and has nothing to do with a sign-in page" — removed), and **the cropped Strip reads as nothing**
  ("neither east nor west"). Slate and Slate 2 stay to compare.
- **A12 — a new round by a worker of its own (the owner, 2026-11-19):** a fresh Claude Code session that analyses,
  understands and builds **3–4 new designs of Sign in**, different from the existing ones, **with or without the
  Strip** (the map is no longer required). Its prompt: `7_NEW_DESIGNS_PROMPT.md`; its report: `8_REPORT.md`. Still
  binding from A2/A3: no photo, no product glimpse, not a plain text panel; if a drawing of the Strip is used, it must
  read as a place (north up, the sea to the west) and its dots real; no counts or figures that change.
- **A13 — round 4 rejected, the method changed (the owner, 2026-11-19):** none of Atlas, Threshold or Clearing
  adopted ("what are these empty designs"); **design as pictures before any code**. Round 5 on a private claude.ai
  Design canvas: five grayscale layouts A–E → **B chosen**: an ink masthead (the logo, the tools, the title at 56 px
  and its line), under it two ways in on one 12-column grid — the form (Google, email, password, «نسيت كلمة
  المرور؟», «تسجيل الدخول») and «جديد على مساحة؟» (register's line, «إنشاء حساب», the owners' note); phone: the
  masthead, then the form, then the new-account block. Tried and dropped by the owner on the way: a berry rule under
  the masthead (partial, then full width), berry dots, grey dots, and four masthead textures (a workspace floor plan,
  a tatreez stitch, the logo's mark as a watermark, plain ink); the tatreez was applied, then removed.
  **Fixed: B with a plain ink masthead, no texture.** Saved in `DESIGN\AUTH\round5-B\` (four standalone pages
  1440 / 390 × light / dark, their PNGs, the canvas sources); the canvas deleted from claude.ai (shared company login).
- **A14 — a free round, principles not prohibitions (the owner, 2026-11-20):** after the supervisor's finding that the
  briefs, not the designers, narrowed every round (round 4's Threshold and round 5's B converged on one composition; the
  round-4 prompt banned the photo, the product glimpse, figures, any new font, the berry on actions, motion), the owner
  wants **a free round with no restrictions, to see what the AI makes**. The brief gives the worker **principles to
  start from, never prohibitions**: the design system, the preferred pattern and the requirements. Nothing is
  forbidden. B stays fixed unless the owner says otherwise; the round compares. Plugins checked: nothing to install
  (the Figma connector here is a colleague's account — not used).
  **Settled (the owner, 2026-11-20, every point as the supervisor recommended):** the page is **Sign in**, beside B;
  the design system is given as **principles** (the logo, ink + berry, Arabic first, an 8 px rhythm, AA contrast,
  light and dark), `foundation.md` only as a reference after the first draft; the pattern is the page's **type** only
  ("a sign-in page with two ways in: returning and new"), the layout the worker's; the requirements written by the
  supervisor from production, in positive form; the executor **a fresh Claude Code worker, not the supervisor** (who
  carries every past constraint), Opus 5.5 effort high, in **a new empty folder** (no CLAUDE.md, no memory); three
  directions as standalone HTML pages with captures, then a stop for the owner's look. **The prompt is a new kind,
  written with care** (context and principles, no prohibitions). The owner has no favourite sites: the supervisor
  proposed references (captures in `C:\Users\basel\Downloads\free-round-refs\`) for the owner to pick from.
  **The owner chose three: Tabby, Careem, Thmanyah** (2026-11-20). The round's folder: `C:\dev\masaha\free-round\`
  (`PROMPT.md`; `materials\`: the berry logo files, the three references, the 13 real spaces with coordinates, the
  Strip's outline, `foundation-reference.md`; the worker's output in `work\`). Not a repository; copy `work\` into
  the workspace once done.
  **Done 2026-11-20 17:27** (copied to `DESIGN\AUTH\free-round\`, without the capture browser's profile):
  - **The three directions:**
    - **Lights «أضواء»:** the real Strip with the 13 spaces as berry lights and a Gaza City inset; the berry means a
      space; the button and the focus ring are berry; Readex Pro.
    - **Berry «توت»:** the berry as the whole page, Kufam Black at 148 px, a paper sheet for the form, and a
      hand-coded frieze of a shared table (tea, a router, a full power strip).
    - **Notebook «كرّاسة»:** a squared exercise book, a Ruqaa title underlined in berry pen, a red-pen error state,
      a pen sketch of a desk.
  - **The worker's recommendation: Lights.**
  - **Open for the owner:**
    - Lights keeps the line «13 مساحة عمل في قطاع غزة» (A11 had removed counts);
    - Berry's text on the berry is 4.58 : 1 (passes AA, no margin) and its drawing needs an illustrator;
    - the data spells «جاردن سبييس» and «إليفييت هاب», and files Golden Hub under North Gaza.
