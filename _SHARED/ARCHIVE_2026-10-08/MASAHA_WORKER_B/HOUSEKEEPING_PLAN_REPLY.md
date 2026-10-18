The plan is approved. Build it, with the answers below.

## Your decisions
1. **ADR 0014, point 3 — approved:** revise it in place ("a port of its own, 5320 and 3320 unless the
   folder sets others") with the `> **Revised:** 2026-10-06 — …` line. The decision itself is
   unchanged.
2. **The other "rebase" lines — approved:** align `.claude/skills/open-pr/SKILL.md` step 3 and
   `docs/plans/foundation.md` (§2 and the risk row), each pointing to workflow §9 instead of
   restating it.

## Your proposed alternatives
- **The wait: 3 s — accepted,** for the reason you gave (a missing element still fails with Testing
  Library's message, under Vitest's 5 s). Take 4 s if the measured slowest lazy wait comes close to
  3 s, and say so.
- **The format check — changed:** don't record a finding. Since it is one file, **format
  `apps/web/src/shared/preferences/preferences.unit.test.ts` with Prettier in Task 4** (formatting
  only, no other change), so `npm run format:check` passes on the head, and **add `format:check` to
  CI** (`.github/workflows/ci.yml`, as a step of the lint job or its own job — your plan's choice) so
  the repository can't drift again. Add the `area:ci` label. Finding 26 resolves with both; there is
  no finding 36 from this item.

## Finding numbers
Worker A's item records **finding 36**; if this item records any new finding, number it **37**.

Everything else stands: the five commits, the tests (item 3's three tests failing first, item 5's
pure helper and its tests), the checks (two consecutive full component runs, the `dist` grep), the
manual second-folder run with the ports freed afterwards, and the PR.
