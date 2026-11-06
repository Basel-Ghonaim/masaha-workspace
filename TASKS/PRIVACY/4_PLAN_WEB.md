# PRIVACY — web plan (worker A)

Base: `main` at b0682fd6 (#134). Branch: `feat/privacy-page`. `docs/design/prototype/Privacy.html` exists.

## Files

### Commit 1 — `feat(web): add the privacy page`

- `apps/web/src/pages/site/public/privacy/PrivacyPage.tsx` (new) — the page, in `pages/site/public/` beside About
  (architecture §2: the site's public pages; a page composes, it owns no rule). One column `max-w-3xl`, the
  prototype's spacing (`gap-14`, `py-10 md:py-16`): the title (h1), the muted «آخر تحديث: 2026-11-05» line, then
  eleven sections, each an `h2` naming its `section` (`aria-labelledby`), paragraphs and `list-disc` lists
  (`ps-6`, logical side), bold through `<strong>`; the «how we use» closing line muted, as the prototype has it.
  The contact section: a `Card` with the sentence and the platform's email as an outline button
  (`mailto:`, the value `dir="ltr"` and muted) — read through `usePlatformContact()` of
  `@features/platform-settings/public` (the site's contact, what About reads): nothing while it is read (DI31), no
  button when no email is set or the read failed; the sentence always shows, as About's text does.
- `apps/web/src/pages/site/routes.tsx` — `/privacy`, public (no guard), lazy, titled `copy.site.links.privacy`.
- `apps/web/src/pages/site/navigation.ts` — `SITE_PATHS.privacy = '/privacy'`.
- `apps/web/src/shared/copy/english/site.ts`, `arabic/site.ts` — `links.privacy` (the footer's link, the page's
  title and h1) and `privacy: { updated, intro, collect, dontCollect, use, cookies, whoSees, protect, retention,
  rights, changes, contact }`, word for word from §7. A list item is a string, or its parts in order — a string or
  `{ strong }` — where the text is bold; the two catalogues have the same parts (the catalogue test holds it).
- `apps/web/src/pages/site/public/privacy/PrivacyPage.component.test.tsx` (new) — modelled on About's: as a guest
  (the route is public), the title and every section heading in English and in Arabic; the bold parts in
  `<strong>`; the email link from `GET /settings/public` (`mailto:`); no email link when none is set. The page's
  `<title>` is covered by `app/pageTitles.unit.test.ts`, which walks every route.

### Commit 2 — `feat(web): link the privacy page`

- `apps/web/src/pages/site/shell/SiteFooter.tsx` — «سياسة الخصوصية» after «عن مساحة», before «تواصل معنا», as the
  prototype's footer orders them.
- `apps/web/src/pages/site/auth/RegisterPage.tsx` — in the card's footer, after «لديك حساب؟», one `text-caption`
  line «اقرأ سياسة الخصوصية», its link to `/privacy` (as the prototype's Register).
- `apps/web/src/shared/copy/{english,arabic}/auth.ts` — `register.privacy: { read, link }`.
- Tests: `shell/SiteLayout.component.test.tsx` (the footer's link to `/privacy`),
  `auth/authPages.component.test.tsx` (Register's line and its link).

### Commit 3 — `docs: record the privacy page as built`

- `docs/project/overview.md` — *Built*: the privacy page (2026-11-05, #n), on the platform-settings line, which
  owns the site's contact the page reads; *Last Updated*.
- `docs/features/platform-settings.md` — *Who uses it*: the site reads the contact on Privacy too; *Web history*.
- `docs/frontend/architecture.md` — the layout tree's and the groups' `public/` lists name the privacy page, and
  *Built so far* names it (so "every screen of v1 is built" stays true with screen 33).

### Commit 4 — `docs: run the online cron every 60 minutes`

- `docs/development/setup.md` (*Timed jobs*, *The deployment* step 7), `docs/architecture/decisions/0014-deployment.md`
  (a new *Revised* line, 2026-11-04), `docs/backend/conventions.md` §12, `docs/api/api-contract.md` (*Internal*),
  `docs/architecture/findings/213-…md` (a dated note: 60 minutes since 2026-11-04, to revisit at launch),
  `docs/features/spaces.md` (the reclamation's line counts the runs of the 03:00 hour: one a day at 60 minutes),
  `apps/api/src/server.ts` (the comment only). The local timer stays 5.

## Tests, each red first

1. Privacy: `/privacy` as a guest shows the h1 «Privacy Policy» and the eleven headings (EN) — red: no route (404).
2. Privacy: the same in Arabic — red with 1.
3. Privacy: the email link `mailto:` from the platform contact; none set → no link — red with 1.
4. Footer: a «Privacy Policy» link to `/privacy` — red: no link.
5. Register: «Read the privacy policy», its link to `/privacy` — red: no line.

## Decisions (safest option)

- The text follows §7 for words, bold and punctuation (the date's label bold, the period after the email); the
  layout follows the prototype. Where they differ, the text wins and the difference is reported.
- The contact shows the email only (the text names the email), through `usePlatformContact()`, not
  `PlatformContact`, which would also draw WhatsApp and make the email primary; the button as the prototype's.
- `architecture.md` and `spaces.md` touched beyond the prompt's list: each would state a fact this PR makes false.

## Proposed alternatives

- None needed to proceed.
