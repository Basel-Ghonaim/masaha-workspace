# Review of #144 (R1 — the colour system) — Claude Code, Opus 5.5
Head: 4cff26c7de4ea1b4b8454ad48f1f440b9a0ae84b · commits 12 · files 81 · checks: green (10 jobs pass, CodeRabbit skipped) · head moved: no (re-read at the end: same head, `CLEAN`)
Verdict (my role): mergeable after a fix round

R1 commits read: c602db41 (C1), e1cc1a7f (C2), c74e8c79 (C3), 38c695a4 (C4), 2a4b8ace (C5), with their parts of
`foundation.md`, ADR 0019, `docs/README.md`, `setup.md` and `CLAUDE.md`. All reads pinned to `4cff26c7` (`git show`,
`git diff origin/main...4cff26c7`, `git grep … 4cff26c7`); `origin/main` = `f58c12a8` = the merge base.

## Findings (verified defects only, most severe first)

### F1 — should-fix · The contact tile's caption drops under 4.5:1 while its link is hovered, in both themes
- **Where:** `apps/web/src/features/spaces/components/contacts/ContactsView.tsx:20` (the `<a>`'s `hover:bg-hover-on-muted`) and `:29` (the caption, `text-caption text-muted-foreground`), on the `<li>`'s `bg-muted` (`:15`). Commit e1cc1a7f (D1's restructure).
- **Seen in the code.** The caption keeps `muted-foreground` under the wash; nothing changes its colour on hover. `muted-foreground` on `hover-on-muted` over `muted` is not a verified pair: neither T4 nor foundation §5 lists it. Foundation §5 says the wash's text is "the control's `foreground`", and §11 says "Verified pairs only".
- **Scenario, computed by hand.** Grounds are the visual pass's Chrome pixels (EC3) and the test's model; WCAG 2 luminance:
  - light: `#5e646a` (n-600) on the wash `#d7dee6` (model `#d7dfe7`) → **4.41** (4.45); at rest on `#ecf4fc`, 5.39;
  - dark: `#9fa6ad` (n-400) on `#3d4147` (model `#3c4147`) → **4.17** (4.18); at rest on `#2c3137`, 5.33.

  An owner or admin points at a contact tile in the space profile, and its phone number or address, which is small
  caption text, falls below AA in both themes. Before this PR the tile hovered with `accent`, where
  `muted-foreground` is verified ≥ 4.5. The visual pass measured contrast at rest only, and the hover set compared
  fills only.
- **Near the blocker line:** a role carries text under its threshold in both themes. I rate it should-fix because
  the role's own measured pair (`foreground` on the wash: 12.31 / 9.90) holds. The defect is the component putting an
  unverified text on it.
- **Fix:** give the anchor `group` and the caption `group-hover:text-foreground`, the same as DataTable's sort
  header, SegmentedControl and the `md` tabs, which all switch to `foreground` on the wash. Alternatively, tile text
  that stays `muted-foreground` must not sit under the wash. **Belongs:** the fix round, folded into e1cc1a7f.

### F2 — should-fix · Hover equals selected in dark where "selected" is still drawn with `secondary`: the account navigation, the editor's section index, «الأقرب إليّ»
- **Where:**
  - `apps/web/src/pages/site/account/AccountLayout.tsx:31` (`variant={current ? 'secondary' : 'ghost'}`);
  - `apps/web/src/features/spaces/components/editor/SectionIndex.tsx:39` (same);
  - `apps/web/src/features/directory/components/near/NearMeButton.tsx:20` (`variant={button.on ? 'secondary' : 'outline'}`, `aria-pressed`).

  The cause: `semantic.css:136` `--secondary: var(--neutral-800)` and `:142` `--hover: var(--neutral-800)` (dark).
  None of the three files is in the PR. The PR's token change creates the clash. Under Sea, the ghost and outline
  hover was `accent` (b-900), a different hue from `secondary`.
- **Seen in the code.** This is exactly the visual pass's F3 (SiteMenu: current `#2c3137`, hovered `#2c3137`). The
  lead fixed it in SiteMenu (LEAD-D5) but did not sweep for the pattern. `git grep -nE "\? ?'secondary'"` finds the
  three above, plus LiveStatusControl (already F4).
- **Scenario:**
  - In dark, at `/me/favorites` (desktop), hovering «البلاغات» paints it `#2c3137`, the same fill as the current
    «المفضلة». In light, a hovered sibling (`#dde5ed`) reads stronger than the current page (`#ecf4fc`).
  - The space editor's section index at `lg` behaves the same.
  - On «الأقرب إليّ» in dark, the hovered un-pressed button is already `#2c3137`. Pressing it changes no fill, only
    the edge (card-border → transparent).
  - Foundation §5: "selected is the spark's tint".
- **Fix:** as SiteMenu. The current entry gets `variant={null}` with `bg-accent text-accent-foreground` and no ghost
  hover (AccountLayout, SectionIndex). The pressed toggle takes the chip's selected look (`bg-accent
  text-accent-foreground border-spark`, kept under the pointer), or another selected look the owner names; a toggle
  is not a page, so that is the owner's call. **Belongs:** the fix round, folded into e1cc1a7f ("tell hover from
  selected").

### F3 — should-fix · `check:classes` misses the tint under other spellings of its own states; the gap is recorded only in a lane report
- **Where:** `apps/web/scripts/checkClasses.ts:86-99` (`HOVER_OR_HIGHLIGHT`, `hoversOrHighlights`), commit e1cc1a7f;
  foundation §3 (e).
- **Seen in the code.** The set is compared literally after stripping `group-` / `peer-` and `/name`, so these all
  pass:
  - `data-[state=open]:bg-accent`: the same state as the project's `data-open:` custom variant (`tailwind.css:27`),
    and the spelling of shadcn's Tailwind 3-era copies (SubTrigger, Menubar and ContextMenu triggers);
  - `aria-[expanded=true]:bg-accent`;
  - `data-[highlighted]:bg-accent`;
  - `active:bg-sidebar-accent`: shadcn's SidebarMenuButton presses with it.

  SD2's reason was "the next copied component would bring the old meaning back silently". Lane A wrote "known gap,
  recorded", but it is recorded only in `lanes\REPORT_A.md`: there is no finding, and §3 (e) does not say it.
- **Scenario:** a menu or nav copied from an older shadcn snippet with
  `data-[state=open]:bg-accent data-[state=open]:text-accent-foreground` passes `check:classes`. The open trigger then
  shows the selected tint again.
- **Fix:** normalise the arbitrary spellings before the lookup: `data-[state=open]` → `data-open`,
  `aria-[expanded=true]` → `aria-expanded`, `data-[highlighted]` (and `=true`) → `data-highlighted`. Add `active`.
  Add T12 cases for each, and one line in §3 (e). Not `aria-selected`: react-day-picker uses it for a chosen day.
  **Belongs:** the fix round, folded into e1cc1a7f. If the owner declines, record it as finding **227**.

### F4 — nit · A ghost control inside a hovered table row has no hover of its own (older; outside D1's list)
- **Where:** `Table.tsx:64` (row `hover:bg-hover has-data-open:bg-hover`) and `Button.tsx:26` (ghost
  `hover:bg-hover … aria-expanded:bg-hover`). The rows' «⋯» menus, e.g.:
  - `StaffActionsMenu.tsx:52` (a StaffList DataTable column);
  - `CustomerMenu.tsx:58`;
  - `SpaceActionsMenu.tsx:60`.
- **Seen in the code.** With the pointer on the «⋯», the row and the button take the same `hover` fill in both
  themes. With its menu open, the row (`has-data-open`) and the button (`aria-expanded`) also match. This was the
  same under Sea (accent on accent), so the PR did not cause it. D1 and EC10 looked only at muted grounds.
- **Fix:** a finding, **226**. One possible remedy: a ghost control inside a row hovers with the wash over the row's
  hover. That is the owner's call.

### F5 — nit · T9 does not pin the OKLab→sRGB inverse's chroma terms
- **Where:** `semantic.unit.test.ts:437-441` (the references) and `:265` (`OKLAB_TO_LMS`); commit c602db41.
- **Seen in the code.** I checked every constant against Ottosson's and Machado's published values, and they are
  right today. But only two expectations go through `fromOklab`:
  - `#636363` has no chroma, so only the first column and the row sums count;
  - the red wash round-trips at the gamut corner, where `clamp` hides any error that pushes r above 1 or g/b below 0.

  Worked by hand: `OKLAB_TO_LMS[0][1]` `0.3963…` → `0.4963…` gives red `(1.157, −0.049, −0.0001)`, which clamps to
  `#ff0000`. Every other assertion is a threshold. So a wrong inverse constant would shift the dark `accent` and
  `primary-hover` unseen, and T9's stated break ("a wrong constant") holds only for the forward transform.
- **Fix:** one hand-written chromatic expectation through the inverse: `painted('dark', 'accent')` is `#471f46`,
  Chrome's painted pixel (EC3), not computed by the code. **Belongs:** the fix round, folded into c602db41.

## The test matrix rows of my role (present / missing / weaker · would it fail on its break?)

| # | State | Would it fail on its break? |
|---|---|---|
| T1 | present (`semantic.unit.test.ts` ROLES, THEMED_TOKENS, key parity, "resolves every role and themed token") | yes: a role missing in one theme fails both parity and presence (report: dark role removed, 5 red) |
| T2 | present, **narrowed by design**: OKLab and `transparent` only; OKLCH is refused, with a test (LEAD-D4) | yes: a typo or an unknown method throws ("hex-only resolver", 29 red); the translucent set must equal `GROUNDS` exactly. Weakness: F5 |
| T3 | present | yes (leftover `brand-500`: 1 red) |
| T4 | present, every planned pair, plus `-foreground` pairs for all new roles | yes (scrim at 60 %: 1 red over white). **Missing a pair the code uses:** `muted-foreground` on `hover-on-muted` over `muted` (F1); it would fail if added (4.41 / 4.17) |
| T5 | present (spark on six grounds, ring on four fills) | yes (paler spark: 7 red) |
| T6 | present (hover ×4, the wash, skeleton ×2, the tints ×2) | yes (skeleton on n-100: 2 red; hover back to `muted` would read 1.11) |
| T7 | present (both tints, both themes; ΔE ≥ 0.02) | yes (hover = tint: 6 red) |
| T8 | present, **stronger** (sidebar-accent too; Machado severity 1 on linear RGB) | yes (coral dark spark: 4 red). The constants and matrices match the published ones; rows sum to 1 |
| T9 | present, plus the red-wash round trip and the OKLCH refusal | partly: the transfer function and forward matrices, yes (wrong exponent: 8 red); the inverse's chroma terms, no (F5) |
| T10 | present (six hexes) | yes |
| T11 | present (the four utilities exactly; no `--color-spark`; `var(--spark)` count = utilities) | yes (`--color-spark`: 1 red; a `text-spark` utility: 1 red) |
| T12 | present (33 cases: each variant, compounded, group/peer, opacity, `!`, `@apply`, at rest allowed, line/column; column 16 checked by hand) | yes for the listed spellings (rule removed: 23 red; narrowed: 10). Weaker than its purpose for the other spellings (F3) |
| T20 | present (`Button.component.test.tsx`: underline at rest, no `hover:underline`; no variant's class names the spark) | yes (both breaks made) |
| T21 | existing axe tests, green on CI | n/a in jsdom (no colour); the restructures (ContactsView `<li>`/`<a>`, SiteMenu) keep their roles |

Every expectation is written by hand. No threshold is fitted: 4.5 / 3 / 1.2 / 1.15 / 0.02 / 0.10 / 0.08 / 15–45° are
§5.4's criteria. Nothing was weakened against `main`: the removed lines are the old hex-only resolver and the
`accent` row pairs, both replaced by stronger ones. I recomputed several of the trial's numbers from the token hexes
and got the same results: `muted-foreground` on `hover` 4.71; `hover` on card 1.27 and on background 1.22;
`foreground` on the wash 12.31.

## Decisions, ODs, SDs and Ds of my role (built / departed, judged)

- **I1 / I4, the values:** built.
  - Every primitive equals plan §5.1.
  - Every binding equals §5.2, except two mixes written in OKLab: `primary-hover` and `overlay-scrim` (deviation,
    sound).
  - Status colours unchanged; `brand-*` gone; no Sea value in `apps/web`, `apps/api/src` or `docs/frontend`. The one
    hit, `bg-(--brand-600)`, is a test sample string.
- **I1, the spark's rules:** built. The spark appears as fills, edges and marks only: the bar, the chip's edge, the
  line tab, the map ring, the lifted item, `chart-1` bars and the count badge's fill. It is never text (no
  `text-spark`; `text-sidebar-primary` / `text-chart-1` unused) and never destructive. The chip that is on carries a
  spark edge, as approved; that is a selected state, not an action.
- **Links in running text underlined:** built.
  - The link Button, RegisterPage, AboutPage, SiteFooter and FieldSection are underlined.
  - Every other link in running text is a link Button, an outline Button (the privacy page's e-mail), or already
    underlined.
  - Table names and card titles are left `hover:underline`, as the plan says.
- **Hover vs selected:** built on the layer, the features' hovers and the showcase. Two gaps:
  - three selected-as-`secondary` surfaces (F2);
  - a muted caption under the wash (F1).
- **SD1:** built.
- **SD2:** built, with a spelling gap (F3).
- **SD3:** built (Button, Calendar).
- **SD4:** built; every Skeleton use I opened sits on card or background.
- **SD5:** built; T4 over white and black is the right worst case, since compositing is monotone per channel.
- **SD6:** built (DataTable sort header, today, FilterTag, contact tile, plus SegmentedControl and the `md` tabs).
- **SD7:** built.
- **SD8:** built (EC4 kept; OKLCH dropped from the model, sound).
- **D1:** built for the planned four. The contact tile's restructure brought F1.
- **D5:** accepted, not tested, as planned.
- **ODs:** none is R1's beyond OD2 (one PR).

## The report's deviations, judged (R1: those touching its commits)

- **Every token mix and the secondary hover in OKLab; the resolver refuses OKLCH (LEAD-D4, F1 of the pass):
  sound.**
  - EC3 measured the warm hover in Chrome.
  - OKLab of two near-greys is the grey the model predicts.
  - A model that cannot reproduce Chrome's powerless hue should refuse it rather than pass a wrong colour; the
    refusal is tested.
  - Destructive stays OKLCH, with its reason in §11.
- **SiteMenu's current entry selected, without hover (LEAD-D5): sound but incomplete** (F2). Its `matchPath` agrees
  with NavLink for every `SITE_LINKS` entry: home is `end: true`, and spaces and about are prefixes in both.
- **LiveStatusControl's neutral tone on the secondary variant (LEAD-D6): acceptable.** The open state loses its fill;
  `aria-expanded` and the popover still show it.
- **The lifted photo's edge drawn inside (F2 of the pass): acceptable.** While lifted, the keyboard focus indicator
  is the spark inset over the photo rather than `ring`, so foundation §10/§11's "one focus style" bends. The reason
  is in a code comment, and the plain ring was clipped anyway (finding 222). §12's Sortable row does not say it
  (Documents).
- **T8 also covers `sidebar-accent` (LEAD-D3): sound.**
- **Lane A's decisions:**
  - the calendar's range middle has no ghost variant: sound;
  - the rule reads group/peer, opacity and `!`: sound; its arbitrary spellings left unrecorded in the repository:
    wrong (F3);
  - one variant parser: sound;
  - EC10's outline buttons with their own fill left on `hover`: sound, since the fill itself changes;
  - ShowcaseNav hovers only off the current entry: sound;
  - the line/column expectation recounted by hand: correct (column 16).
- **C1 and C6 first, the lanes' documents folded by the lead: acceptable.** Each R1 commit carries its code, test
  and document lines. The subjects are ≤ 50 characters and the bodies say why.

## Documents

- **foundation.md (R1's parts):** accurate to the code.
  - Status, §3 (e), §4 tiers and ramps, the `skeleton` component token, §5 roles, values and the OKLab line.
  - *Verified* matches the test pair for pair.
  - §11's hover rule; the §12 rows for Button, DropdownMenu, Select / Combobox, Calendar, ToggleGroup,
    SegmentedControl, Sortable, FilterTag, Table / DataTable, Skeleton, Tabs and Sidebar; §15 row 1.

  The code departs from its §5 rules in F1 and F2: the document is right and the code must follow. Two silences:
  - §3 (e) does not say the arbitrary spellings pass (F3);
  - §12 Sortable does not say the lifted photo's spark edge is drawn inside and stands in for the focus ring.
- **ADR 0019:** short and decision-level (Context · Decision · Alternatives · Consequences), with no file, class or
  code named. It records the trial's criteria as tests. It calls the ink "a dark slate", which is the light theme's
  value, but "one brand in two themes" covers the dark one. Not a defect.
- **Map, setup.md, CLAUDE.md:** the ADR line, foundation's "the logo", the `check:classes` row and line. All accurate.

## Scope and commits (R2)

Not my role. R2 covers it. Within R1's five commits I saw no file outside the plan's §7 tables. The exceptions are
SiteMenu and LiveStatusControl (the pass's F3 and F4, stated in the report) and the `checkClasses` test's sample
string. I saw no drive-by change.

## Not checked, and why

- **Nothing was run:** no test, lane, build, server or browser (the review's rules). CI's green head stands for the
  lanes.
- **Chrome's painted values** (`#d7dee6`, `#3d4147`, `#471f46`) are the visual pass's (EC3), not re-measured.
- **F1's and F5's arithmetic was done by hand,** because a local Python check needed approval. The method and inputs
  are in each finding.
- **Chrome's powerless-hue behaviour** for chroma ≈ 0.014 is taken from the pass's measurement, not from a spec
  reading.
- **R2's commits** (Logo, shells, icons, e-mail, prototype, findings) were not reviewed, apart from the files they
  share with R1. I met no defect outside my role.
- **The screenshots** in `Downloads\identity-prod-shots\` were not opened.
