# DASH_FIXES — #146 red on Prettier only (the message to paste to OpenCode)

```
Supervisor's message (relayed by the owner). #146 on fd65982c: lint, typecheck, test:unit and build pass; only format:check fails — Prettier wants apps/web/src/features/directory/hooks/page/useSpacePage.ts (its long `@shared/lib` import line). Run `npx prettier --write` on that file, fold it into 682717e6 "guard unknown amenity icons" (backup first; --fixup + autosquash), run `npm run format:check` before the push, push with --force-with-lease, wait for every check green and CLEAN, write 4_REPORT.md (all three red rounds), stop. Never merge.
```
