# IDENTITY — "ink + spark" trial, worker plan (2026-11-11)

Worktree `C:\c\dev\masaha\app-identity` (the path git lists; the prompt's `C:\dev\…` does not exist), branch `design/ink-spark`. Only `docs/design/`; nothing committed.

**Where the tokens live.** Primitives (`--brand-*`, `--neutral-*`, …) on `:root` and the semantic roles on `[data-theme='light'|'dark']` (= `<html>`), both in the vendored `_ds_bundle.css`; utilities read `var(--role)` directly (`.bg-accent{background-color:var(--accent)}`), so a role can also be re-scoped on a subtree. 38 pages load `fonts.css → _ds_bundle.css → styles.css → masaha/masaha.css`, then `masaha/i18n.js` (a plain IIFE that reads `?lang`/`?theme` and carries them on every `.html` link). The 4 others (two boards of iframes, the reset e-mail, the Wordmark sheet) load neither and stay out.

**Loading and switching.** `masaha/identity-ink-spark.css` is linked right after `masaha.css` on the 38 pages and the 5 `_*head.txt` templates. `i18n.js` reads `?identity=` against the list (`slate-coral`, `slate-berry`, `charcoal-coral`), sets `<html data-identity>`, and carries it on links like `lang`/`theme`; no or unknown value = no attribute = today's *Sea*, untouched. Every rule is under `html[data-identity…]` (higher specificity than the bundle's, unlayered, so it wins), so the default pages cannot change.

**The remap (both themes).** Per candidate: `--neutral-*` = the ink-hued neutral ramp, `--spark-*` = a spark ramp from the lab's `makeRamp`, and `--brand-*` = the spark ramp too, so any leftover brand use shows spark, never teal. Shared: `primary` = n-900 / n-50 (fg white / n-950), `ring` = `sidebar-ring` = ink, `accent` = spark-50 / spark-900 with **ink** text, `sidebar-accent` the same, `sidebar-primary` = `--spark` with its foreground, `chart-1` = `--spark`; destructive, success, warning, info, and their subtle pairs unchanged. `--spark` = the step that passes on every ground (light 500; dark 300 coral, 400 berry).

**Spark shows on:** sidebar current item (spark tint + a 3px spark bar at the inline start), the sidebar's count badge, selected filter chips (spark tint + spark border), the line-tabs' indicator, `Badge variant="primary"` and the "today" rows (spark tint), the selected map pin's ring, the sortable item dragged over / lifted, `tone-primary` covers, the brand mark (header wordmark: ink word + spark dot; admin tile: spark fill).
**Spark never on:** action buttons (primary = ink; outline/ghost hover re-scoped to a neutral `muted` tint inside `[data-slot=button]` and dropdown-menu items), small text (no spark text anywhere; `accent-foreground` is ink), destructive (unchanged red). Links in text: ink, **underlined**.
**Hover fix needed:** the bundle's primary hover mixes `primary` with `foreground` — with ink they are the same colour, so the hover would vanish; the trial mixes toward `background` 18% instead.

**Criteria (measured by `measure.mjs`, the lab's engine + Machado 2009):** foundation §5's pairs on the remap, both themes (66 per theme: every `-foreground` on its surface incl. the hover, muted-fg/primary/destructive/success/info as text on background/card/muted at 4.5; input, ring, chart-1…5, status fills on background/card at 3; ring on muted/accent; spark on background, card, muted, accent, sidebar, sidebar-accent at 3); ink↔red ΔE ≥ 0.10, protan/deutan ≥ 0.08; red-400 hue stays 15–45° in dark. Added guard: spark↔red ≥ 0.08 also under CVD (dark coral spark-400 measured ΔE 0.036 / CVD 0.005 — same as the red — so dark coral uses 300).

| Candidate | ink L / D | spark L / D | pairs | ink↔red ΔE (protan, deutan) L · D | spark min | spark↔red (CVD) L · D |
|---|---|---|---|---|---|---|
| slate-coral (h255 c.030, #C2492F) | #151F2C / #F7FBFF | #D2573D / #FEA793 | 66/66 · 66/66 | .353 (.193, .326) · .329 (.365, .278) | 3.63 · 7.00 | .099 (.089) · .121 (.096) |
| slate-berry (h250 c.014, #A149A0 h328) | #1A1F25 / #F7FBFF | #B55BB3 / #D27ED0 | 66/66 · 66/66 | .346 (.190, .319) · .329 (.365, .278) | 3.70 · 4.77 | .191 (.184) · .156 (.154) |
| charcoal-coral (h60 c.012, #C2492F) | #231D19 / #FFF9F5 | #D2573D / #FEA793 | 66/66 · 66/66 | .336 (.192, .310) · .322 (.359, .274) | 3.64 · 7.01 | .099 (.089) · .121 (.096) |

## Proposed alternatives

1. **Wordmark text in spark.** WCAG exempts logotypes from contrast, but heading-3 is 17px/600 (not "large"), so the rule "never small text" wins: the trial keeps the word ink and adds a spark dot. If the owner prefers a spark word, the logo step can make it ≥ 24px.
2. **Spark↔red as a criterion.** The prompt measures only ink↔red; the coral spark sits 0.099 from the red in light (0.089 CVD). I propose a recorded guard (≥ 0.08 under CVD) for any spark — it is what forced dark coral to step 300.
3. **`accent` as hover.** The plan maps hover and selected to one spark tint; I keep it on selections and re-scope it to neutral on buttons and menu actions. Cleaner in production: a separate `hover` role (neutral) and `accent` only for selected.
