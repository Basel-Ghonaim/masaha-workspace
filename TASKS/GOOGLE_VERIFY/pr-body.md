## Summary

Google's brand verification of the sign-in consent screen refused the home page as not registered to the owner. This
adds the ownership file Google Search Console gave, served at the site's root, and corrects `setup.md`, which still
said the consent screen stays in *Testing*.

## Scope / Acceptance criteria / Out of scope

**Scope:** `apps/web/public/google17f1cc2beeef3f62.html` (new, byte for byte as Google gave it), `.prettierignore`
(one entry), `docs/development/setup.md` (the `GOOGLE_CLIENT_ID` row and step 5).

**Acceptance criteria:**

- The build serves the file at its root unchanged (`apps/web/dist/google17f1cc2beeef3f62.html`, same SHA-256 as the
  source). After the deploy, Search Console verifies the property (the owner's step).
- `setup.md` states the consent screen as it is: published, any Google account signs in, the name and logo shown only
  after the branding's verification, and why the file must stay.

**Out of scope:** the re-verification request and the logo (the owner's steps in the Google Cloud console); a custom
domain.

## Change type

`chore`: a static file, one ignore entry, documentation. No code.

## Evidence

- Run on the head: `npm run format:check` (pass), `npm run check:links` (pass), `npm run check:conflicts` (pass),
  `npm run build` (pass; `apps/web/dist/google17f1cc2beeef3f62.html` is 53 bytes, SHA-256
  `9ede73c80741852053b7fc3fd0347f429344e8f97636b8e7adefd4aecc3e6075`, the same as the source).
- Not run: lint, typecheck and the test lanes — no code changed, and no test reads the new file (the owner's decision
  for this item). CI runs every check.

## Screenshots

None: no UI change.

## Definition of Done checklist

- [x] Acceptance criteria met within scope (the live verification after the deploy is the owner's step).
- [x] No code: lint, typecheck and tests not applicable; the build passes.
- [x] Documentation updated in the same PR; one home per fact.
- [x] Atomic history (two commits), pushed, description complete, no tool attribution.
