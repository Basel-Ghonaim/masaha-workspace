# MEDIA — build now (the second message)

**DIRECTORY merged:** PR #73, `main` = `3c3dc47`. Its review changed none of the shapes you extend
(`DirectorySpace`, `MapPin`, `PublicSpace`, `spaces/public/`). Your folder is already detached at
`3c3dc47`; the analyst applied the migration to `masaha_media_dev` (`prisma migrate status`: up to
date; `masaha_media_test` is migrated by the test lane's global setup), regenerated the Prisma client
and rebuilt the shared `dist`. Check these, then cut the branch:
`git fetch --prune origin`, `git switch --no-track -c feat/space-photos origin/main`; first push
`git push -u origin feat/space-photos`. Build the plan as saved, with the reply's changes.

## Added to your scope: Issue #69 (the owner's decision)

#73's two independent reviews left five small findings. The owner added them to Issue #69, reopened
for them; **read its last comment** (`gh issue view 69 --comments`): it names each file and fix. You
open these files anyway (D12), so:
1. **The tie-break tests** (`list.api.test.ts`, `near.api.test.ts`) made able to fail: a row's
   physical order moved away from its id order before asserting; the break (`, id` removed from
   `orderOf`) made once and the test seen failing.
2. **`no-store` on every answer to a request carrying `Masaha-Near`, errors included,** set as soon as
   the header is present, before validation; a test on a refused request (422) with the header.
3. **A space's page reads "verified" and its facts under one transaction and lock** (`page()` in
   `directory.service.ts`); if you find a reason to keep the gap, record it instead, and say why in
   the report.
4. **The `q` refusal:** the code and the contract say the same code for a `q` of spaces only.
5. **security.md › Location:** the screen, not the answer, labels the distance approximate.

**One commit of its own**, before your photos commits or after them (say which), for example
`fix(directory): close #69's review leftovers` (count it: ≤ 50), its body naming the five. The PR
body says `Closes #69` and has a short **Issue #69** section listing the five with where each is
proven. Add the commit to your plan's §11 and its tests to §9 when you save any update; no new plan
round is needed.

## Reminders

- The four photos commits as the reply approved them; every subject ≤ 50.
- **One full test run at a time:** check worker A (main folder) runs none before `test:api` or
  `test:component`. Worker B is idle.
- `CLOUDINARY_URL` is a secret: never print, log or echo it. The owner is adding it to this folder's
  `apps/api/.env`; check it by its shape only (`cloudinary://<digits>:<secret>@dj1pqmwnz`), and if it
  is absent or malformed at the real run, run with the local adapter and say so.
- An independent review follows. Don't merge. At the report, `git merge-tree --write-tree` against
  every open PR. Stop every background shell you start; `jq` is not installed — use `gh … --jq`.
