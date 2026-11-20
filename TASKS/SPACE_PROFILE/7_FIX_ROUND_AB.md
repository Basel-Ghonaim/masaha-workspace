# SPACE_PROFILE — fix round on #140 and #141 (sent only on the owner's word)

The Claude reviews say **mergeable after a fix round** for both:
`C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\6_REVIEW_PR-A.md` (#140, head `29bcf80a`) and
`C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\6_REVIEW_PR-B.md` (#141, head `4109534c`). The supervisor confirmed in
the code: #140 F1 (a YouTube `/watch` link keeps only its path), F2 (a bare number read as an IPv4 host); #141 F1
(Radix's Escape listener runs on `document` in the capture phase, before the handle's), F2 (the refocus effect has
no dependency list), F5 (`touch-none` on the showcase's tiles). Read both reviews whole, then:

## #140 (`feat/contact-types`)
- **F1, F2** as the review says, folded into `29bcf80a`, each with its T4/T5 cases seen failing first.
- **F3** EC8 now: name the existing test behind T16–T18 and T20 in the PR; add T19's package case (an owner's package
  on a shift; `PUT …/hours` leaving it out → 409, nothing written, no audit), seen failing by a break restored from a
  `cp` backup — as its **own** commit `test(spaces): …`.
- **F4 — the owner's decision (2026-11-10): record only.** Write **finding 217** (Open): "contacts and every phone
  refuse Arabic-Indic digits; the shared phone rule reads Western digits only; C2 assumed otherwise" — no conversion
  built, T5 unchanged. Check the index first.
- **Finding 218** (Open), as F1/F2 say: "a website's bare number is stored as an IP address; a Facebook video link
  loses its id" (existing types, not changed here).
- **F5** nothing in #140 — noted for PR-C (its contacts Sheet clears or keeps the name when a row leaves `OTHER`;
  T41 asserts it).
- **F6** accept a two-letter country subdomain of `linkedin.com`, stored on `www.linkedin.com`, with a T3 case.

## #141 (`feat/sortable-list`)
- **F1–F11** all, folded into `4109534c`, each with the test the review names, seen failing first at the old head
  (F1's test inside the layer's real open `Sheet`; F2 typing in an input outside the list keeps the focus; F4 cancel
  after moving up keeps the focus; F5 re-run EC4 with a swipe that scrolls). Correct `foundation.md` where F1, F3, F5
  and F9 say it is untrue.

## Method and verification
- `git branch backup/contact-types-1` / `backup/sortable-list-1` first; fixes as `--fixup` +
  `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main`; no fix commits left (F3's test commit excepted).
  Stage by path; no tool attribution.
- Each PR: `lint`, `typecheck`, `format:check`, `check:*`, `NODE_ENV=production` build + `check:build`, and the three
  lanes in full (`test:api` for #140; for #141 `test:api` may be left to CI — it changes no API code). Two lanes at
  once at most; a lane killed for memory: retry once, then CI judges.
- `git push --force-with-lease`; each description gains "Review fixes"; CI green on the new heads, `CLEAN`; append
  a "Fix round" section to `4_REPORT_AB.md` naming both PRs and their **new full head shas**. Then stop. Never merge.
