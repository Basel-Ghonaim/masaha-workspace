# PRIVACY — web report (worker A)

**Status:** READY FOR REVIEW · **PR:** #135 (https://github.com/Basel-Ghonaim/masaha/pull/135) · **head** 791e53de · **CI** green (every check, `test:api` included) · **CLEAN** · **22 files**, +587 −18

Base: `main` at b0682fd6 (#134); `docs/design/prototype/Privacy.html` present. Plan: `4_PLAN_WEB.md`.

## Commits

1. `d283f841` feat(web): add the privacy page
2. `7fc72740` feat(web): link the privacy page
3. `331adbff` docs: record the privacy page as built
4. `791e53de` docs: run the online cron every 60 minutes

## Files

- **Page:** `apps/web/src/pages/site/public/privacy/PrivacyPage.tsx` (new), its `PrivacyPage.component.test.tsx` (new); `pages/site/routes.tsx` (`/privacy`, public, lazy, titled); `pages/site/navigation.ts` (`SITE_PATHS.privacy`).
- **Copy:** `shared/copy/{english,arabic}/site.ts` (`links.privacy`, `privacy.*`), `shared/copy/{english,arabic}/auth.ts` (`register.privacy`).
- **Links:** `pages/site/shell/SiteFooter.tsx`, `pages/site/auth/RegisterPage.tsx`; tests in `shell/SiteLayout.component.test.tsx`, `auth/authPages.component.test.tsx`.
- **Documents:** `docs/project/overview.md`, `docs/features/platform-settings.md`, `docs/frontend/architecture.md`.
- **Cron:** `docs/development/setup.md`, `docs/architecture/decisions/0014-deployment.md`, `docs/backend/conventions.md`, `docs/api/api-contract.md`, finding 213, `docs/features/spaces.md`, `apps/api/src/server.ts` (comment only).

## Text

Checked by a script (`scratchpad textcheck.ts`, run with tsx): the catalogue rendered back to Markdown against §7, line by line. Arabic 43 lines, 0 different; English 43 lines, 0 different. The straight quotes and apostrophes of the approved text are kept as they are.

## Red → green

- Privacy page (4 tests): red, the page did not exist (`./PrivacyPage` failed to resolve) → green.
- Footer link: red, `Unable to find … role "link" and name "Privacy Policy"` → green.
- Register line: red, `Unable to find role="link" and name "privacy policy"` → green.
- Arabic date left to right (found in the screenshots): red, `Expected the element to have attribute: dir="ltr"` (the date sat in the RTL paragraph) → green; folded into commit 1 (`--fixup`, autosquash, `backup/privacy-web` first, deleted after).
- The page's `<title>` in both languages: `app/pageTitles.unit.test.ts`, which walks every route, passes with it.

## Local verification (on 791e53de, after the fold)

format:check pass · lint pass · typecheck pass · check:classes pass · check:links pass · check:conflicts pass · test:unit pass (280 + 917 + 1186) · test:component pass (2039) · build (NODE_ENV=production) pass · check:build pass. `test:api` left to CI (passed there).

## Screenshots — `shots\web\`

`privacy-ar-light-1280`, `privacy-ar-light-390`, `privacy-en-light-1280`, `privacy-ar-dark-1280`, `home-footer-ar-1280`, `register-ar-390`, `register-en-1280`. Each opened and checked: `dir` rtl/ltr and `lang` right, the page title in both languages, no raw tag, 15 `<strong>` (as the text), the email shown as «بريد …» / "Email …", no horizontal overflow at 390; the footer's «سياسة الخصوصية» between «عن مساحة» and «تواصل معنا»; Register's muted line under «لديك حساب؟». Script: `scripts\shots.mjs`.

Only the web server ran (`npm run dev -w @masaha/web`), stopped by PID (15772, 6236, 4360), port 5320 checked free; headless Chrome killed by the script. **The API was not started:** its in-process timer runs the timed jobs (auto check-out, the photos' reclamation) 10 s after start against `masaha_dev`, the owner's demo, which must never be written; Docker was also not running. The public contact was answered in the browser (CDP `Fetch`) with a sample email, `hello@masaha.example`; other API calls answered 503, so Home's cards show their skeletons in its shot.

## Matches Privacy.html

Yes in layout (column, spacing, headings, lists, the muted closing line of «كيف نستخدم بياناتك», the contact card with its outline email button, footer and Register). Differences, each the approved text or the task over the prototype:
- «آخر تحديث:» / "Last updated:" bold (the text bolds it; the prototype does not), the date 2026-11-05 (the prototype's sample is 2026-11-04), and the date left to right in Arabic.
- The contact sentence ends with its period after the email (the text has it; the prototype drops it).
- Register's English line "Read the privacy policy" (the task's words; the prototype says "Read privacy policy").

## Decisions

- The approved text wins over the prototype for words, bold and punctuation; the prototype for layout.
- The contact gives the email only, through `usePlatformContact` (not `PlatformContact`, which draws WhatsApp and makes the email primary); the sentence stays alone with no email or a failed read.
- The date lives in the catalogue, one line per language.
- `docs/frontend/architecture.md` and `docs/features/spaces.md` changed beyond the named list: each stated a fact this PR makes false (the site's public pages / every screen built; four reclamation runs a day).
- The API not started for the screenshots (above).

## Left out

- Nothing of the task. The finding 213 *Resolution* paragraph and ADR 0014's 2026-11-01 *Revised* line keep "15 minutes" as history; the new note and line say 60.
