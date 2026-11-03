# Masaha logo — the decision (for the main supervisor)

> **Status: pending.** The direction is settled (LOGO_NOTES.md); the logo itself is **not made yet**. The owner fills
> the marked gaps once the files exist, then brings this file to the main supervisor's conversation.

## 1. The files

In `C:\dev\masaha\workspace\TASKS\LOGO\final\`. Every SVG is black, one fill colour; the code colours it.

| File | What it is | Ready |
|---|---|---|
| `masaha-mark.svg` | the full mark (pin, «م», desk) | ☐ |
| `masaha-mark-small.svg` | the simplified mark for 16–32 px (pin and «م») | ☐ |
| `masaha-wordmark-ar.svg` | «مساحة» | ☐ |
| `masaha-wordmark-en.svg` | "Masaha" | ☐ |
| `masaha-lockup-ar-horizontal.svg` | mark right of «مساحة» | ☐ |
| `masaha-lockup-en-horizontal.svg` | mark left of "Masaha" | ☐ |
| `masaha-lockup-ar-stacked.svg` | mark above «مساحة» | ☐ |
| `masaha-lockup-en-stacked.svg` | mark above "Masaha" | ☐ |
| `favicon.svg` | the small mark, switching shade with the light/dark scheme | ☐ |
| `favicon.ico` | 16, 32 and 48 px | ☐ |
| `apple-touch-icon.png` | 180 px, teal mark on white | ☐ |

Chosen variant, tools used and date: **[owner fills]**.

## 2. The decision

> **Outdated (2026-11-02):** the idea was reopened and the «م» dropped (LOGO_NOTES.md, "Axis 1 reopened"). This
> paragraph is rewritten once the new mark is chosen.

Masaha's mark is one continuous thick monoline that fuses a location pin, the Arabic letter «م» and a work desk:
the pin's head is the «م»'s rounded-square loop, its point is the «م»'s tail, and the tail lands on a short line
that reads as a desk; a simplified version drops the desk line for 16–32 px. It is geometric, with soft corners and
rounded ends, and it fits a square. The words are IBM Plex Sans Arabic and IBM Plex Sans at weight 600, outlined,
with no kashida. The whole logo takes one colour: `brand-600` (`#02787d`) on light, `brand-400` (`#50b3b8`) on
dark, white on teal, black in print; never a live-status colour. The mark is never mirrored: it sits right of the
Arabic word and left of the English one.

## 3. The rules of use

- **Clear space:** the height of the mark's «م» loop, on every side.
- **Minimum size:** the full mark from 32 px; the small mark below 32 px; a horizontal lockup no less than about
  20 px high.
- **Do not:** mirror the mark; recolour it outside the brand ramp; use the live-status colours (green, amber, red);
  put it in a coloured tile (it would look like the spaces' letter tiles); add shadows, glows or effects; stretch
  or squash it; place it on a photo without a plain background.
- **Clean SVG checklist:** exported from Figma and passed through SVGOMG; no embedded image; no live text (all
  letters outlined); one fill colour; a square viewBox for the mark; about 1–2 KB for the mark.

## 4. What the code change will need

For the main supervisor to plan as a Work Item; listed, not planned.

- The logo as a design-system component (`apps/web/src/shared/design-system/`), coloured by semantic tokens, with
  its accessible name from the copy catalogue in both languages (today `copy.site.wordmark`).
- The site's header (`apps/web/src/pages/site/shell/SiteHeader.tsx`): the lockup in place of the text wordmark.
- The dashboard sidebar's `mark` slot (`apps/web/src/pages/dashboard/shell/AdminLayout.tsx`): the mark in place of
  the «م» tile; the small mark on the rail.
- The favicon set in a new `apps/web/public/` and its links in `apps/web/index.html`.
- `docs/frontend/design-system/foundation.md` §15 row 5 settled, with the rules of use summarised or linked.
- The design-system showcase (`/__showcase`): the logo in both themes and both languages.
