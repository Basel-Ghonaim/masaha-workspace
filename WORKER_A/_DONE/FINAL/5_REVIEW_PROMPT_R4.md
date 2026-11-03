# Review of #132 — R4: the public site and the account

Read this file, then `C:\dev\masaha\workspace\WORKER_A\FINAL\5_REVIEW_PROMPT_COMMON.md` whole, and do it. Your report:
`C:\dev\masaha\workspace\WORKER_A\FINAL\6_REVIEW_R4.md`. New findings, if any: **232–235**.

**Your commits (15, U9):** `79d8bdcd 20869f1b 7e2d442a 95ea07af 1f1ce675 2048fdc4 43e69574 36c88ec3 c611a7ad b8eb7ff5
167dcd70 974ab466 8f804bad 00017140 f91b34cf`

**Read in the plan:** §5.9 (U9) and its DIs; §2's carried public-site fixes (from #111's review, copied in full);
§9.1's U9 commits; §10.4's U9 tests; §11's site and account cases. The prototypes: `Home.html`, `Directory.html`,
`Space details.html`, `About.html`, `Sign in.html`, `Register.html`, `Forgot password.html`, `Reset password.html`,
`Error.html`, `Settings.html`, `Change password.html`, `Favorites.html`, `Reports.html`.

**Look hardest at:**
- **The account (screen 9):** the name and the language edited through `PATCH /me`; the language applied at once and
  kept; validation and errors in both languages; nothing else of the account editable here.
- **Sign-in flows:** `next` and the way back kept (no open redirect: `next` only a same-site path); the password too
  long said; a first Google sign-in welcomed (32); **a guest's action kept through a password reset (168)** — a
  short-lived, same-origin store the session confirms, never in the address; it cannot fire into another account or
  later visit.
- **The directory and the map:** the results and the map finished; the marks drawn as on light tiles in dark (135,
  OD5); near me's wait counted only after the permission (136); area counts hidden past the pins (137); the place
  filter capped (133); markers not rebuilt each render (134).
- **Home, About, the space page, the error pages:** each against its prototype; a second retry while offline announced;
  the route retried and the 403 given a way out; the footer, the areas and the pick.
- **Favourites:** the list's line once ready.
- **Every screen of your range complete, no gap** — both languages (RTL), dark, 390 / 768 / 1440, empty / loading /
  error, accessibility; the site's first download untouched by dashboard code.
