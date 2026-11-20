# DASH_FIXES — #146's fix round (the supervisor's review; for a FRESH OpenCode session in `C:\dev\masaha\app`)

The supervisor read #146 at `e396951072b0fe9cf9887e6cc0cc5cb8ac73ea6c` (CI green, CLEAN). Two defects and a nit:

- **S1 (220):** `useSpaceEditorActions` hides the actions on **any** error (`query.isError`), while its siblings read
  only a 404 as gone (`useSpaceEditor.ts:43` `query.error?.status === 404`, `useSpaceName.ts:13`). A transient 500
  or network failure on a background refetch would now remove «إخفاء عن الزوار» / «حذف المساحة» from a space that
  exists. The finding asks for the 404.
- **S2 (222):** the lifted branch lost `focus-visible:outline-spark`. A photo lifted **by keyboard** keeps the
  keyboard's focus, and `focus-visible:outline-ring` (a class plus `:focus-visible`) beats `outline-spark`, so the
  lift draws the ring's colour, not #144's spark edge. No test covers either state.
- **N1 (227):** `AmenityRow.tsx` checks `knownAmenityIcon(row.icon) !== null` before `<AmenityIcon>`, which already
  draws nothing for an unknown key — one guard is enough.

Paste:

```
You continue DASH_FIXES (PR #146, branch fix/dashboard-findings, head e3969510). Read whole: C:\dev\masaha\workspace\TASKS\DASH_FIXES\0_OWNER_DECISIONS.md, 1_EXEC_PROMPT.md (every rule binds you), 4_REPORT.md, then 7_FIX_ROUND.md (this review). Check the state yourself (git status, git log origin/main..HEAD, gh pr checks 146).
A backup/dash-fixes-pre-review first; each fix folds into its commit (--fixup + autosquash), no fix commits:
1. S1 → "hide actions for gone space": gone = `query.error?.status === 404`, exactly as useSpaceEditor and useSpaceName; the test also proves a 500 on a later read keeps the actions. Correct the commit's body and the finding's text ("a 404", not "fails").
2. S2 → "show photo focus ring": while lifted or dragging the edge stays the spark under keyboard focus too (`focus-visible:outline-spark` back in that branch). A component test: a focused photo carries the inside ring classes; a lifted one carries the spark's, not the ring's.
3. N1 → "guard unknown amenity icons": drop AmenityRow's extra check.
Each new assertion: break it once, watch it fail, restore. Before the push, required (through the grant script, which waits for memory): `npm run lint`, `npm run typecheck`, `npm run format:check`, then the touched test files alone.
Push with --force-with-lease (your branch only), update the PR description ("Review fixes" with S1, S2, N1), wait for every check green and CLEAN, add a "Fix round" section to 4_REPORT.md with the full head sha, stop. Never merge.
```

After it: the supervisor looks at 222 and 223 in a browser himself (the report could not).
