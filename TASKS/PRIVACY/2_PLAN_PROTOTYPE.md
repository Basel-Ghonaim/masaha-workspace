# Plan — Privacy Page Prototype

## 1. Files to change or add

### New file
- `docs/design/prototype/Privacy.html` — the privacy policy page, mirroring `About.html` structure

### Modified files
- `docs/design/prototype/masaha/shared.jsx` — add Privacy link to `SiteFooter` (between "About" and "Contact")
- `docs/design/prototype/Register.html` — add "Read privacy policy" link under the register button in the CardFooter
- `docs/frontend/design-system/foundation.md` — §13: change "(32)" to "(33)", Public site from "(8)" to "(9)", add item 33
- `docs/design/SCREENS.md` — update count from 32 to 33, add row for Privacy policy in Public site table
- `docs/design/CHANGES.md` — add new section at the end for 2026-11-04 privacy page

## 2. Where the site footer is defined

The footer is defined in `docs/design/prototype/masaha/shared.jsx` in the `SiteFooter` component (lines 341-353). It contains two links: "About Masaha" and "Contact us". This is a shared component used by every page that loads `shared.jsx`.

## 3. How to check the work

Run the four checks from the repository root:
```
node docs/design/scripts/check-parse.mjs
node docs/design/scripts/check-classes.mjs
npm run check:links
npm run check:conflicts
```

Then serve the prototype and take screenshots:
```
cd docs/design/prototype
npx serve . -l 5999
```

Screenshots to take (headless Chrome):
- Arabic light 1280: `Privacy.html`
- Arabic light 360: `Privacy.html` (window-size=360,3200)
- English 1280: `Privacy.html?lang=en`
- Dark 1280: `Privacy.html?theme=dark`
- Home.html 1280 (footer link)
- Register.html 1280 (register link)

Verify each screenshot: page not blank, RTL in Arabic / LTR in English, no overflow at 360, links visible.

## 4. Implementation order

1. Create `Privacy.html` (copy `About.html` structure, use exact text from §7)
2. Update `shared.jsx` footer links
3. Update `Register.html` CardFooter
4. Update `foundation.md` §13
5. Update `SCREENS.md`
6. Update `CHANGES.md`
7. Run checks
8. Take screenshots
9. Commit (3 atomic commits)
10. Push and open PR
11. Write report

## 5. Key decisions (recorded upfront)

- Use `PrivacyScreen` as the component name prefix to avoid global collisions
- Contact email: use same sample data as `About.html` (`M.platformContact.email`)
- "Last updated" date: fixed sample `2026-11-04`
- Register link text: «اقرأ سياسة الخصوصية» / "Read the privacy policy" in muted small text
- No table of contents, no cards, no icons — calm reading page like `About.html`
- All strings through `tr("arabic", "english")` helper
- Logical properties only (ms-/me-/ps-/pe-/start/end)
- Classes copied from `About.html` and other pages