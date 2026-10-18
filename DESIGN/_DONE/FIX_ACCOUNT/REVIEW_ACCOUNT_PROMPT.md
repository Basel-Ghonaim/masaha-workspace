# Design review 4 — the account and signing in

**The design-review-account worker** (a one-off reviewer, named after its task). **Read-only:** you
write nothing in the repository, run no git command that changes anything, and touch no worker's
folder.

**Size cap:** at most 1 subagent, no workflow; the whole review under 500,000 tokens. Two other
reviews and a building worker run beside you, so keep the load light.
**Report:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_ACCOUNT_REPORT.md`.
**Evidence images:** `C:\Users\basel\Downloads\design-review-account\` (create it).

## 1. The task in brief

The fourth of six design reviews. The shared layer, the admin's dashboard and the public site are
reviewed and **decided**. This review takes **signing in and the user's own account**: getting in
(signing in, registering, Google, a forgotten password, the forced change), and what a signed-in user
keeps (settings, favourites, their reports). Look at what each page is for, its sections and
components, its flows and states, and the better design for each.

## 2. Read first

1. **The lens:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REVIEW_LENS.md`. It sets your method and the
   report's shape; follow it exactly.
2. **What is settled:** `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_SHARED.md` (read its amended
   head), `DECISIONS_ADMIN.md` and `DECISIONS_PUBLIC.md`. Don't report any of it again (lens §2b).
3. The design's guides:
   - `docs/design/README.md`;
   - `docs/design/SCREENS.md`, rows 5–7 (sign in, register, forgot and reset password with the reset
     email) and 9–11 (my account);
   - `docs/design/INDEX.md`;
   - `docs/design/prototype/BRIEF.md`.
4. The product's documents:
   - `docs/frontend/design-system/foundation.md` §5, §7–§10, §12, §13 (*Public site* › the auth pages,
     *My account*);
   - `docs/project/overview.md` (the v1 scope, *Not in v1*); `docs/project/glossary.md`;
   - `docs/backend/security.md` › *Passwords* (the policy, the forced change, the recovery);
   - ADR 0017 (the recovery session).
5. **Most of these pages are built in code.** Read the *Web decisions* of `docs/features/auth.md`
   and `docs/features/users.md`: say where the built screen already took a better choice, and
   propose against the better of the two.
6. The prototype's source: `masaha/auth.jsx`, `account.jsx`, and `Sign in.html`,
   `Sign in - board.html`, `Register.html`, `Forgot password.html`, `Reset password.html`,
   `Reset email.html`, `Change password.html`, `Settings.html`, `Favorites.html`, `Reports.html`.

## 3. Your scope

The screens and their frames, board sections **05–09**, **13** and **15–19**:
- **5 Sign in**, with Google;
- **6 Register**;
- **7 Forgot and reset password**, with the reset email;
- **9 Profile and settings**, with the forced password change;
- **10 Favourites**;
- **11 My reports**.

**Issue IDs:** `AC-001`, `AC-002`, …

## 4. How to look

- **Serve a copy, never the repository's folder.** Extract the archive from `origin/main` to a short
  path and serve it on **port 5343**:
  `git archive origin/main docs/design | tar -x -C C:\Users\basel\design-review-account` (create the
  folder), then serve `C:\Users\basel\design-review-account\docs\design\prototype` on 5343.
- Look at every page in Arabic and English, light and dark, at 390, 768 and 1440, and with the
  keyboard. Take evidence with headless Chrome (a script in your scratchpad, never committed).
- Read the source of each page, so a proposal names what really changes.
- At the end: stop the server, delete `C:\Users\basel\design-review-account`, and check port 5343 is
  free.

## 5. Risks

- **Writing anything** in the repository or in `masaha` or `masaha-b`: other workers are building
  there.
- **Reporting settled decisions** again, or the archive's known limits.
- **A proposal outside the design system:** a colour, size or font outside its tokens.
- **A proposal against a security rule:** an answer that tells whether an email has an account, or a
  password shown or kept where security.md forbids it.
- **A design the API cannot serve** (lens §2c).
- **Many small items, no big picture:** lead with the *Patterns* (getting in, the account area's
  shell).

## 6. When you finish

Save the report. Summarise it here in ten lines at most: the five most important points, and the
counts by level and impact. Change nothing else.
