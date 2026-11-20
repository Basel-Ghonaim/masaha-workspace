# PROTOTYPE_SPLIT — the owner's decisions (2026-11-15)

Why: round 3's directions were judged weak overall (some ideas kept); the owner moves to page-by-page design work,
starting with the auth pages, each new design a **variant of the same page chosen by a query parameter**
(`Sign in.html?v=<name>`), the original untouched and switchable. Keeping the prototype inside the production repo no
longer serves: every prototype change costs a PR, the full CI and a production deploy on merge, and the design worker
would work inside the production repo. A copy would mean editing twice.

- **P1 — a full separation (the supervisor's option 1, approved):** `docs/design/prototype` (and what belongs only to
  it — the planner proposes the exact list) moves to its own repository **with its history** (`git subtree split` or
  equivalent); one PR in `masaha` removes it, repoints the documents and code comments that cite it, drops the
  exclusions that only existed for it (`.prettierignore`, `eslint.config.js`, `checkLinks.ts`), and records the
  decision in a short ADR. Rejected: a copy with the original frozen (two homes), a submodule (cost, no gain).
- **P2 — the new repository is PUBLIC** (the owner's word), `Basel-Ghonaim/masaha-prototype`. Before it is made public,
  its whole history is scanned: no secret, no real personal data, and never the university, the supervisor or the
  defence (the project's identity rule).
- **P3 — executed by Claude Code** (a worker, not the supervisor).
- **P4 — documentation (approved 2026-11-15):** no second documentation set. The production repository (public)
  stays the one home of product facts (scope, glossary, product rules, copy, design system), read **read-only** by the
  prototype's workers (`--add-dir C:\dev\masaha\app`). The new repository holds only its own working documents: a
  `README.md` (what it is, how to run it, how variants work), a `CLAUDE.md` (the workers' rules), an updated
  `BRIEF.md` (who the users are, what is fixed, what a variant may freely change — new type, spacing, surfaces, each
  stated as a proposal), and a `decisions/` folder (one file per page: what the owner chose and why).
- **P5 — the sensitive step is the removal from production, not the publication:** `masaha` is already public, so the
  prototype and its history are public today; the history scan (P2) still runs. The worker plans and **stops**; the
  owner approves the plan before anything is pushed or created on GitHub.
- **P7 — the plan's answers (2026-11-15):** R1b (redact the new repository's history: About.html's line, the five
  About screenshots painted, U11 reworded; the supervisor looks at the five images before publishing); the sample
  names and numbers left; the switcher hidden without variants; findings' links pinned to a commit. **`masaha`'s own history
  (2026-11-15, after the options were explained): option A — left as it is.** The tip is clean once the split PR
  merges; a rewrite (B: 942 of 1,081 commits re-hashed, every cited sha broken, PR refs kept by GitHub) and making the
  repository private (C: the public face lost, Actions minutes capped) are **rejected**. No finding is added
  (`_PRIVATE_HISTORY_NOTE.md`).
- **P6 — variants:** `<Page>.html` stays the original; `<Page>.html?v=<name>` a variant; a small switcher on each page
  lists the original and its variants. The split item sets up the mechanism only — no variant is designed in it.
