# OWNERSREAD — merge and clean (the owner runs these, or an assistant with the owner's word)

Only after the verify step says the PR is ready **and** the owner approves.

```
cd C:\Users\basel\masaha-b
gh pr view <n> --json headRefOid,mergeStateStatus      # note the head; must be CLEAN
gh pr merge <n> --merge --match-head-commit <head>
git fetch --prune origin
git push origin --delete feat/space-owners-read
git switch --detach origin/main
git branch -D feat/space-owners-read
git status --short --branch                              # clean, on the new main
```
If the PR changed the schema (it should not): in the worker's folder, `cd apps/api; npx prisma migrate deploy; npx prisma generate`, then `npm run build -w @masaha/shared`.
