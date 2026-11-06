# Report — Privacy Page Prototype

## Files changed

### New files
- `docs/design/prototype/Privacy.html` — the privacy policy page prototype

### Modified files
- `docs/design/prototype/masaha/shared.jsx` — added Privacy link to `SiteFooter`
- `docs/design/prototype/Register.html` — added "Read the privacy policy" link in `CardFooter`
- `docs/frontend/design-system/foundation.md` — §13: (32)→(33), Public site (8)→(9), item 33 added
- `docs/design/SCREENS.md` — title 32→33, Public site table 8→9, row 33 added
- `docs/design/CHANGES.md` — new section "Privacy page (2026-11-04)"
- `docs/README.md` — fixed heading anchor reference (32→33)
- `docs/architecture/findings/14-the-owners-audit-screen-has-no-design.md` — fixed heading anchor reference
- `docs/plans/foundation.md` — fixed heading anchor reference
- `docs/plans/v1-mvp.md` — fixed heading anchor references (32→33, 8→9)
- `docs/project/overview.md` — fixed heading anchor reference

## Commits

1. `b3b661f9` — `docs(design): add the privacy page prototype` — Privacy.html
2. `5ea501b3` — `docs(design): link the privacy page` — shared.jsx, Register.html
3. `16f2345f` — `docs: list the privacy page as screen 33` — foundation.md, SCREENS.md, CHANGES.md
4. `341c3b3d` — `docs: fix links broken by the screen count change` — 5 referencing documents

## Checks

- check-parse: 51/51 blocks parsed ✓
- check-classes: 0 new dead classes ✓
- check:links: 3239 links all resolve ✓
- check:conflicts: no conflict markers found ✓

## Screenshots

6 screenshots in `TASKS\PRIVACY\shots\`:
1. `01-ar-light-1280.png` — Arabic, light theme, 1280px
2. `02-ar-light-360.png` — Arabic, light theme, 360px
3. `03-en-1280.png` — English, 1280px
4. `04-dark-1280.png` — Dark theme, 1280px
5. `05-home-footer-1280.png` — Home page showing footer link
6. `06-register-1280.png` — Register page showing privacy policy link

Verification via Playwright: page loads without errors, all sections render, footer link present, contact email link works (mailto:).

## Decisions

1. Used `Button` component for contact email (matching About.html pattern) instead of inline styled link, since `underline`/`underline-offset-*` classes are not in the prebuilt bundle.
2. Register privacy link uses plain `<a>` tag (relying on base CSS `a{color:var(--primary)}`) since underline classes are not available.
3. Fixed heading anchor references in 5 other documents that broke when the heading numbers changed from (32) to (33) and (8) to (9). These are outside the task's scope list but were necessary to make check:links pass, per the task's "fix red checks" instruction.
4. Used `current="privacy"` for SiteHeader even though privacy is not in the header nav (it's a footer link), matching the pattern used by About.

## Text verification

Identical to the approved text (AR and EN) — yes. All strings pass through `tr()` helper. No rewording, no added or dropped sentences.

## PR

- PR #134: https://github.com/Basel-Ghonaim/masaha/pull/134
- Head: 341c3b3d
- CI: all green
- mergeStateStatus: CLEAN