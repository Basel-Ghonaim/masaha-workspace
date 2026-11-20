# GOOGLE_VERIFY — the owner's decisions (2026-11-16)

Google refused the consent screen's brand verification: "The website of your home page URL … is not registered to
you." The fix: prove the site's ownership in Google Search Console (URL-prefix property, the HTML-file method), then
wait 24 hours and request re-verification in the console's Branding page.

- **G0 — the method (the owner):** the executor is **GitHub Copilot CLI** (an Education plan — the prompt must leave it
  nothing to decide). **Phase 1: Copilot reads the requirements and writes its plan (`2_PLAN.md`), then stops.** The
  owner and the supervisor review it; the owner approves or sends corrections; **phase 2 executes only then**. The
  main supervisor does not execute (to keep his conversation's context). Copilot loads **no skill** — the prompt
  replaces `start-work-item`, `write-plan`, `open-pr` and `final-report`.
- **G1 — place:** the worktree `C:\dev\masaha\app` (on `main`, clean, no worker in it), a new branch
  `chore/google-site-verification` from `origin/main`.
- **G2 — the file and Prettier:** Google's file (`google17f1cc2beeef3f62.html`, 53 bytes, no final newline, SHA-256
  `9ede73c8…6075`) goes to `apps/web/public/` **byte for byte**; Prettier flags it, so `.prettierignore` gets one entry
  for it (the alternative — letting Prettier add a newline — risks a failed verification and another 24 hours).
- **G3 — checks:** no test lane, no lint, no typecheck (no code; the only test reading `public/` checks named icon
  files). Locally: `format:check`, `check:links`, `check:conflicts`, and a `build` to prove the file lands at the
  build's root unchanged. CI runs everything.
- **G4 — documents:** `docs/development/setup.md` still says the consent screen stays in *Testing* (line 231's row,
  step 5 on line 256) — false since the owner published it on 2026-11-05 after `/privacy` shipped (#135). Corrected in
  this PR, plus one sentence saying why the file exists and that it must never be removed. Exact texts in the prompt.
- **G5 — commits:** two — 1 `docs(setup): the consent screen is published`; 2 `chore(web): add Google's site
  verification file` (the file, its ignore entry, its sentence). Messages pre-written (`msg-1.txt`, `msg-2.txt`).
- **G6 — the PR:** Copilot pushes the branch and opens the PR (labels `chore`, `area:web`, `area:docs`; assigned to
  the owner; body `pr-body.md`); no merge, no push to `main`, **no tool attribution** (no `Co-authored-by` trailer of
  any tool, Copilot's included) — checked before the push.
- **G7 — verification and merge:** no Claude review (two small commits); the supervisor verifies (diff, the file's
  bytes, CI green, `CLEAN`, no attribution); the owner's merge word (it deploys to production); the supervisor checks
  the live file; then the owner clicks VERIFY in Search Console, waits 24 hours, and requests re-verification.
