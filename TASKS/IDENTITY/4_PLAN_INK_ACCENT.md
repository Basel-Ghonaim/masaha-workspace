# IDENTITY — trial: "ink + spark" in the prototype (plan, 2026-11-11)

**Why.** The owner likes a warm coral, but every coral / orange / earthy brand fails the measured criteria as the
**primary** colour: next to the destructive red it differs by hue only, and under protan/deutan simulation the two are
practically the same (Sea sunset: ΔE 0.036, CVD 0.006). The idea taken from Oyoun Academy's design system (an idea,
not its values): the brand has **two roles** — a dark **ink** carries actions and structure, a warm **spark** marks
"what matters now", sparingly. Ink vs red then differ in **lightness**, which survives colour blindness.

## Where

- A new worktree **`C:\dev\masaha\app-identity`**, branch **`design/ink-spark`** from `origin/main`; local only — **no
  commit pushed, no PR** until the owner decides. Port **5402** (`python -m http.server 5402 --directory
  docs/design/prototype`). The lab in `app-b` (5401) and `main`'s prototype stay as they are, for side-by-side
  comparison.
- **Only `docs/design/`**; no production file. The vendored bundle (`_ds/*/_ds_bundle.css`) is not edited: one new
  stylesheet `masaha/identity-ink-spark.css`, loaded last by the pages, remaps the semantic tokens.

## What changes (token remap, both themes)

| Role | Today | Trial |
|---|---|---|
| `--primary` (buttons, primary links) | brand-600 / dark brand-400 | **ink**: neutral-900 / dark neutral-50, its foreground white / neutral-950 |
| `--ring` (focus) | brand-500 / 400 | ink (≥ 3:1 on every ground) |
| `--sidebar-primary`, `--sidebar-accent` (current nav item) | brand | **spark** fill / spark tint with ink text |
| `--accent` (hover, selected tint) | brand-50 / 900 | spark-50 / spark-950 |
| selected map pin, sortable lift, `tone-primary` | primary | **spark** |
| links in text | primary | ink, **underlined** (colour alone no longer marks a link) |
| destructive, success, warning, info | unchanged | unchanged (true red stays) |

A **spark** ramp (11 steps) is built with the lab's own engine; the **neutral** ramp gets the chosen ink hue.

## Candidates (measured before they reach the owner)

Ink × spark: **slate-blue ink + coral spark** (the owner's Sea sunset family), **slate ink + berry spark**, **warm
charcoal ink + coral spark**. Each must pass: the lab's 38 contrast pairs in both themes; **ink primary vs destructive
red** apart in lightness (ΔE ≥ 0.10 and CVD ≥ 0.08); the spark used only for fills, large text and icons (≥ 3:1 on its
ground — never small text); the spark never on an action button; destructive red stays red in dark mode. One
`?identity=` switch picks the candidate on every page.

## Look at

Home, the directory (cards, filters, map pin), a space's page, the desk (check-in, «إلغاء الدفعة» dialog), the
owner's overview and space profile, the admin's list — at 390 and 1440, Arabic and English, light and dark.
Screenshots to `Downloads\identity-shots\`. The prototype's two checks pass.

## Then

The owner chooses (or rejects the idea). If chosen: an ADR-level change in `foundation.md` (a new spark role) for his
approval, then the logo in the chosen ink + spark, then production tokens.

## Who executes (the owner's choice)

(a) The main supervisor, here, in `app-identity` (fast; Claude). (b) A fresh Claude Code worker from this file.
