# SHOTS59 — screenshots of every prototype page PR #59 changed

You take screenshots of the design prototype as PR #59 leaves it ("design: apply the shared layer's
decisions"), at three widths, into one flat folder. **That is the whole task.**

## Rules

- You run in **`C:\Users\basel\masaha-design`**, the worktree of PR #59's branch (`design/shared`).
  **Change nothing in it or in any repository.** No edit, commit, checkout, switch, pull, stash,
  install, `npm`, database or Docker command, and no GitHub comment. Read-only `git` and `gh`, Python
  and Chrome only. Your scripts live in your own scratch space, never in the worktree.
- **No tool attribution** in anything you write.

## 1. Check the worktree is the PR's head

1. `gh pr view 59 --json headRefOid` must say **`bc7f2919f406ac01a3f55c38dd78a567771694e2`**,
   `git rev-parse HEAD` the same, and `git status --short` nothing. If any differs, stop and say so.
2. Serve the prototype: `python -m http.server 5347 --bind 127.0.0.1` from
   `C:\Users\basel\masaha-design\docs\design\prototype`. **Not `npx serve`**: its clean URLs drop
   every `?…` parameter. Check that 5347 is free first.
3. Before you finish, `git status --short` must still say nothing.

## 2. Capture

- **Browser:** headless Chrome (`C:\Program Files\Google\Chrome\Application\chrome.exe
  --headless=new --remote-debugging-port=9334`) driven over CDP from a small Node or Python script in
  your scratch space (Node 24 has a built-in `WebSocket`; no new package). Browse `http://localhost:5347/…`.
- **Widths** (`Emulation.setDeviceMetricsOverride`, device scale factor 1):
  - **SM** = phone **390** (mobile: true);
  - **MD** = tablet **768**;
  - **LG** = laptop **1440**.
- **The whole page, top to bottom.** The pages are RTL, and `captureBeyondViewport` shifts an RTL page
  sideways in headless Chrome: instead, read the page's `document.documentElement.scrollHeight`, set
  the viewport to that height, wait, then capture the **viewport**. Cap the height at 8000 px and say
  which pages were cut.
- **Wait for the page:** the prototype compiles its `.jsx` in the browser (Babel). Wait for the load
  event, then until `#root` (or the page's root) has children and `document.fonts.ready` resolves,
  then 1.5 s more. A blank or half-drawn shot is retaken once; if still blank, list it.
- **Arabic, light theme** (the defaults). Clear `localStorage` before each page so no earlier choice
  of theme or language carries over.
- **PNG**, no annotations.

## 3. Names and folder

- **One flat folder:** `C:\Users\basel\Downloads\pr59-shots\`, **no subfolders**. Create it; if it
  exists already, stop and ask.
- **Name:** `NN_PAGE_N<SIZE>.png` — the page's two-digit number from the list below, its name in
  capitals with underscores, then `1SM`, `2MD` or `3LG`, so a name sort shows each page's three
  widths together, phone first:
  `05_ADMIN_SPACES_1SM.png`, `05_ADMIN_SPACES_2MD.png`, `05_ADMIN_SPACES_3LG.png`.
- Also write `00_LIST.txt` in that folder: each number, name and the exact URL captured.

## 4. The pages (35, in this order)

`shared.jsx` and `masaha.css` changed, and every page below loads them, so every one changed.

| # | Name | URL path (after `http://localhost:5347/`) |
|---|---|---|
| 01 | OWNER_OVERVIEW | `Owner%20overview.html` |
| 02 | DESK | `Desk.html?role=reception` |
| 03 | CUSTOMERS | `Customers.html` |
| 04 | CUSTOMER_FILE | `Customer%20file.html?id=m1` |
| 05 | PAYMENTS | `Payments.html` |
| 06 | FINANCE | `Finance.html` |
| 07 | PACKAGES | `Packages.html` |
| 08 | OWNER_SPACE_PROFILE | `Owner%20space%20profile.html` |
| 09 | ANNOUNCEMENTS | `Announcements.html` |
| 10 | DATA_REPORTS | `Data%20reports.html` |
| 11 | STAFF | `Staff.html` |
| 12 | OWNER_SETTINGS | `Owner%20settings.html` |
| 13 | MY_PAYMENTS | `My%20payments.html?role=reception` |
| 14 | ADMIN_OVERVIEW | `Admin%20overview.html` |
| 15 | ADMIN_SPACES | `Admin%20spaces.html` |
| 16 | ADMIN_SPACE_EDIT | `Admin%20space%20edit.html?id=focus` |
| 17 | ADMIN_OWNERS | `Admin%20owners.html` |
| 18 | ADMIN_REPORTS | `Admin%20reports.html` |
| 19 | ADMIN_USERS | `Admin%20users.html` |
| 20 | ADMIN_LOOKUPS | `Admin%20lookups.html` |
| 21 | ADMIN_AUDIT | `Admin%20audit.html` |
| 22 | ADMIN_SETTINGS | `Admin%20settings.html` |
| 23 | HOME | `Home.html?loc=none` |
| 24 | DIRECTORY | `Directory.html?loc=none` |
| 25 | DIRECTORY_MAP | `Directory.html?view=map&selected=focus&loc=none` |
| 26 | SPACE_DETAILS | `Space%20details.html?id=focus&loc=none` |
| 27 | ABOUT | `About.html` |
| 28 | FAVORITES | `Favorites.html?auth=1&loc=none` |
| 29 | MY_REPORTS | `Reports.html?auth=1` |
| 30 | ACCOUNT_SETTINGS | `Settings.html?auth=1` |
| 31 | ERROR_403 | `Error.html?type=403` |
| 32 | SIGN_IN | `Sign%20in.html` |
| 33 | REGISTER | `Register.html` |
| 34 | FORGOT_PASSWORD | `Forgot%20password.html` |
| 35 | CHANGE_PASSWORD | `Change%20password.html` |

That is 105 images. Take nothing else: no states, dialogs or dark theme.

## 5. Finish

- Stop the server and Chrome; check ports 5347 and 9334 are free. Stop every background shell you
  started. `jq` is not installed in Git Bash: use `gh … --jq`.
- **Your last message:** the head captured, the count of images (105 expected), and every page that
  was blank, cut at 8000 px or retaken. Nothing else.
