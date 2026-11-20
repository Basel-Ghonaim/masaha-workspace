# Lane B report: IDENTITY, C5 and C7

(Saved by the lead from the lane's final message, 2026-11-12.)

## Branch
- `lane/b` head: **0f921ab7bff3370bf048d7c13b16a43094017d1a**. `git log --oneline 22ddac1c..lane/b` shows exactly two commits, and the tree is clean (`git status --short` prints nothing).
- **C5** `51ff900554196574c6149369d91882f123599386`: `fix(web): raise the skeleton and photo count` (44 characters). 2 files:
  - `apps/web/src/shared/design-system/components/feedback/Skeleton/Skeleton.tsx`: `bg-muted` becomes `bg-(--skeleton)`.
  - `apps/web/src/features/spaces/components/photos/PhotosView.tsx`: «+N» `bg-foreground/60 … text-background` becomes `bg-scrim … text-scrim-foreground`.
  - Body: 1.11 becomes about 1.27 on a card; 3.64 becomes at least 4.5 over any photo, a pair the token test proves over white and black.
- **C7** `0f921ab7bff3370bf048d7c13b16a43094017d1a`: `feat(web): show the logo in every shell` (39 characters). 7 files:
  - `pages/site/shell/SiteHeader.tsx`, `pages/site/shell/FocusLayout.tsx`: the home `Link` holds `<Logo label={copy.site.wordmark} className="h-10" />` and takes SD10's focus classes.
  - `pages/site/shell/SiteMenu.tsx`: `<Logo label={copy.site.wordmark} className="h-10 self-start" />`. The SheetTitle (the dialog's name) is kept.
  - `pages/dashboard/shell/AdminLayout.tsx`: the `tile` constant is gone. It now has `mark={<Logo form="mark" className="size-9" />}`, `logo={<Logo className="h-9" />}` (both decorative), then `<span className="sr-only">{copy.site.wordmark}</span>` and the caption.
  - Tests: `SiteLayout.component.test.tsx`, `changePasswordPage.component.test.tsx`, `pages/dashboard/routes.component.test.tsx`.
  - No catalogue line changed. The "wordmark" comments were left as they were (still true: the logo is the wordmark drawn). The body says why: the owner's places, and OD3 (a).
- No tool attribution in either commit. Everything was staged by path.

## Tests
**C5:** no new test. The Skeleton test does not name `bg-muted`, so it is unchanged. T21 green: `Skeleton.component.test.tsx` and `PhotosSection.component.test.tsx`, "Test Files 2 passed (2) · Tests 15 passed (15)".

**Seen failing, before C7's code** (tests written on top of C5; run: "Test Files 3 failed (3) · Tests 4 failed | 85 passed (89)"):
- **T18, header:** `× … the site shell > draws the logo in the header’s home link, which it names «Masaha», and «مساحة» in Arabic`, "TestingLibraryElementError: Unable to find an accessible element with the role "img" and name "Masaha""
- **T18, phone menu:** `× … draws the logo, named «Masaha», at the head of the phone menu, which keeps its own name`, the same "Unable to find … role "img" and name "Masaha""
- **T18, focus shell:** `× … the change password page > shows the change in the focus shell, whose short header offers only the logo, linking home, and sign-out`, the same "Unable to find … role "img" and name "Masaha""
- **T19:** `× … the dashboard's navigation > heads the admin’s sidebar with the logo hidden from assistive technology, «مساحة» read once beside «إدارة المنصة», and no «م» tile`, "expected document not to contain element, found <span aria-hidden="true" class="flex size-9 … bg-primary …">م</span>" (routes.component.test.tsx:387).

**Green after C7:** the same 3 files gave "Test Files 3 passed (3) · Tests 89 passed (89)". After the breaks were restored, a final run of 10 files gave "Test Files 10 passed (10) · Tests 150 passed (150)". The 10 files: the 3 above, plus SiteAccount, authPages, forgotPasswordPage, resetPasswordPage, `pages/site/routes` (axe-clean Home and About, which draw the header), `AccountLayout` (two axe-clean tests) and `app/router`. Each of T18 and T19 shows `✓`, so T21 is green and axe-clean.

**Breaks** (backups copied to `scratch-b\backup\`, restored by `cp`, `cmp` identical; made in two rounds, with `-t` filtered to the two tests):
- **T18, the text wordmark back in SiteHeader:** `× … draws the logo in the header’s home link …`, "Unable to find an accessible element with the role "img" and name "Masaha"". Restored.
- **T18, the logo without its `label`:** `× …`, "Unable to find an accessible element with the role "link" and name "Masaha"". Restored.
- **T19, the «م» tile back** (as `mark` and `logo`): `× …`, "expected document not to contain element, found <span aria-hidden="true" …>م</span>" (:387). Restored.
- **T19, the name read twice** (`logo={<Logo label={copy.site.wordmark} …/>}`): `× …`, "expect(element).toHaveAttribute("aria-hidden", "true") … Received: null" (:388). Restored.

## Commands
Every heavy command went through `heavy.mjs lane-b`, and every one was granted on its first try: no wait, no kill, no slow-machine miss (see `heavy-grants.log`, 11:01–11:09 UTC).
- **C5:** eslint on its 2 files exit 0 · `npm run typecheck` exit 0 · the 2 test files green.
- **C7:** eslint on its 7 files exit 0 · `npm run typecheck` exit 0 · the red run, the green run, two break runs and the final run (results above).
- **Light:** `npx prettier --check` on every touched file is clean (`--write` was used only on SiteHeader and FocusLayout, which needed it). `npm run check:classes` reports "No physical direction or arbitrary-value classes in 1989 files" after each commit's change.
- **Not run (the lead's):** the full lanes, the build, `check:build`, the visual pass, and EC6 / EC14.

## Document lines (ready to paste into `docs/frontend/design-system/foundation.md`)
**C5, §12 `feedback`, line 440.** Replace
`| Skeleton | shadcn | Loading states |`
with
`| Skeleton | shadcn | Loading states · its fill is the `skeleton` component token (§4), at least 1.2:1 on `card` and `background` (§5, *Verified*) |`

**C7, §16.** Insert a new bullet after line 554 (`- **Forms.** The full logo: «مساحة» over "MASAHA" in the ink, …`) and before `- **Sizes.** …`:
`- **Where it shows.** The full logo, named, as the link home in the site's header and in the focus shell's (sign-in, register, the forgotten and the reset password, the forced change), and at the head of the phone's menu: 40 px tall. In the admin's sidebar, decorative beside the name kept for assistive technology and «إدارة المنصة»: the full logo 36 px tall, expanded and in the drawer, and the small mark 36 px on its rail. Not in the owner's and reception's shell: its sidebar head is the space's own (the switcher).`

## Decisions taken without the lead (what · why · undo)
1. **T19 is written in Arabic** (`startPreferences('ar')`, then `stubScreenWidth(1280)` again). Why: in English the navigation's name and the caption are both "Platform admin", and the brief names «مساحة» / «إدارة المنصة». `startPreferences` re-stubs `matchMedia`, so without the second stub the sidebar would fall into its phone mode. Undo: drop the two lines and use the English names.
2. **The focus shell's T18 strengthens the existing change-password test in place**: the title "…only the wordmark…" becomes "…only the logo, linking home, …", and it adds `href '/'` and the image inside the link. Why: it is the same claim, made stronger. Undo: revert the title and put the check in a test of its own.
3. **T19's order**: the «م» check first, then `aria-hidden`, then no `img`, then the sr-only name (one `getByText`, so read once), then the visible caption. Why: each break's red line names its own cause. Undo: reorder.
4. **One comment line added in AdminLayout**: "The logo is decorative: the name is read here, once, before the area." Undo: delete it.
5. **Breaks paired across files**, two rounds of two, filtered with `-t`. Why: it saves two runs, and each red line still belongs to its own test.

## Found, not fixed (for the lead, as possible findings or Review Focus)
- `changePasswordPage`, `forgotPasswordPage` and `resetPasswordPage.component.test.tsx` render the lazy site routes with no `beforeAll` warm (testing §3 rule 8). I touched the first one but did not add a warm (that would be a drive-by), and my change adds no new wait.
- No component test proves that AdminLayout gives the rail `form="mark"`. T17 proves the Sidebar's branch; EC6 (the visual pass) proves the form and the 36 × 36 size.
- No axe test renders the admin's sidebar header. Its aria is proven by T19 only.
- Nothing behaved unexpectedly.
