# MEDIA — one addition (the owner, 2026-10-13)

Worker B now builds the session item (`C:\Users\basel\masaha-b`, branch `feat/session-ends`), the one
schema change in flight, and edits `apps/api/prisma/schema.prisma`. So that only one open item edits
that file (workflow §9, rule 3):

- **Leave `schema.prisma` untouched.** D8's comment line (`Space.profileUpdatedAt`'s "and photos")
  is written by worker B in its migration's commit. Your data-model change (photos leave the
  freshness groups) stays yours.
- **Files worker B edits — touch none of them:** `apps/api/src/shared/auth/accessToken.ts` and
  `requireAuth.ts` (+ their tests), `apps/api/src/modules/sessions/`, `modules/users/`,
  `modules/auth/`, `apps/api/prisma/`. Your `shared/auth/can.ts` change is yours alone. If your build
  needs one of B's files, stop and say so.
- Its shared documents (security.md, the data model, the findings index, the overview's *Built*
  line) take the fast path; your finding numbers stay **63–64** (B has 65–66).
- **One full test run at a time:** before `test:api` or `test:component`, check that worker A (main
  folder) and worker B (`masaha-b`) run none.

Update your plan's §7 (the schema line) when you next save it; no reply is needed.
