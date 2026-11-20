# The auth pages — what ChatGPT's critique got right (checked by the supervisor, 2026-11-15)

Only the points confirmed in the captures (`D:\MASAHA\DT\AUTH\`) and the code are kept (the owner's word).

## Defects in production
1. **Google's button in dark:** a white frame around it, wider than the fields (390 and 1920). The button is already
   `filled_black` in dark; Google's iframe does not take the page's dark `color-scheme`.
2. **Google's button is narrower than the fields** (its maximum ~400 px; the fields ~422 px).
3. **Forgot password shows a bare spinner** until the recovery check answers — on a slow network the user waits on
   it with nothing to read. (The fix is the form shown at once, or the spinner with words — not server rendering.)
4. **The forced password change has no language switch** in its header (only «تسجيل الخروج»).

## Design points
5. The password conditions, drawn as large empty circles, read like radio buttons — the heaviest element on its page.
6. The card is centred vertically, so the title's height changes from page to page.
7. Weak hierarchy: the title ~20 px over a ~16 px subtitle.
8. At 390: a frame inside a frame (the header's line, the card's border and shadow, its margin).
9. At 1920: a ~448 px form alone in an empty page.
10. The pages read as a template (a library's default card); the berry appears only in the logo.
11. «حرف واحد على الأقل»: the rule accepts any letter (`\p{L}`, Arabic included); the copy can say so.
