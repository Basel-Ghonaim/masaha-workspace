# OWNERSREAD — resume the execution (the first executor stopped at its usage limit)

You are a **new executor** continuing a Work Item another session started. Do not redo its work.
**Do not use any project skill.** Work in `C:\Users\basel\masaha-b` only.

## Where it stands (checked by the analyst)
- Branch `feat/space-owners-read`, **one commit**, `74983dd2 feat(spaces): include owners in admin
  space reads` (49 characters): the code, its tests and the documents, 14 files. The tree is clean.
- **Not pushed, no PR, no report.** Whether the local lanes ran on this commit is unknown.

## What you do
1. Read `C:\Users\basel\masaha\CLAUDE.md` and the plan
   `C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\OWNERSREAD_PLAN.md` (its approval note at the top), from
   its *Executor procedure* on. Compare the commit with the plan (`git show --stat HEAD`, `git show HEAD`):
   anything the plan lists that the commit lacks, add it — **as the plan says, nothing more**. If the
   gap is larger than a few lines, stop and say so.
2. The commit has **no body**: amend it with a short body saying why (2–4 lines), the subject unchanged
   (`git commit --amend`; it is not pushed yet, so this is safe).
3. **Local verification, one at a time:** first check that no other folder runs a test lane (the main
   folder `C:\Users\basel\masaha` may); then `npm run test:unit`, `npm run test:api`, `npm run lint`,
   `npm run typecheck`, `npm run format:check`, `npm run check:links`; and `npm run test:component`
   (the commit changes `AdminSpace`, which the web imports, and two web test fixtures). Record the counts.
   Prove the plan's breaks: for each test the plan names with a break, make the break once **from a
   backup copy of the file (never `git checkout`)**, see it fail, restore it.
4. Real requests against the API on 3321 as the plan says (the owners on a verified space's read; none
   on an unverified one). Stop the server by its PID; check the port free.
5. `git push -u origin feat/space-owners-read`; `gh pr create --assignee @me --label feat --label
   area:api --label area:docs` with the description the plan writes out; wait for
   `gh pr checks <n>` to pass and `gh pr view <n> --json mergeStateStatus` to say `CLEAN`.
6. The conflict check: `git merge-tree --write-tree` against every other open PR's head.
7. Write the report to `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\OWNERSREAD_REPORT.md`: the PR and
   head, the commit, what was run with counts, the breaks made, problems met, anything unexpected,
   the conflict check, departures (say that a first session wrote the commit and stopped at its limit).

Never merge, create an Issue, add tool attribution, print a secret, or use `git add -A` / `.`. Then stop.
