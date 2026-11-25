# WI-B — the fix round for PR #158 (one round, every point; the owner's rule C11)

The review (`9_REVIEW.md`, read it whole) says **after a fix round**, no blocker. Fold every fix into the commit it
belongs to (`backup/berry-main-action-pre-fix` first, `--fixup` + autosquash on the same base), run the full local
verification, push with `--force-with-lease` pinned to `071e9214fb15438e20fa9103e148a50559cb89cd`, post one "Review
fixes" comment on the PR (each point → its commit), update the PR description if it changes, wait for green CI and
`CLEAN`, and add a "Fix round" section to `7_REPORT.md` with a fresh after-shot of each screen you changed. Run heavy
commands in the foreground. Never merge. Prove each code fix with a test seen failing first.

1. **S1 — Packages' empty state draws the main action.** Keep `main` on the header copy only; the empty state's copy
   stays ink, as Staff's does (foundation §5's rule). Fold into `b284e80a`, with an assertion.
2. **S2 — D6 was approved as "the first contact channel in the side panel a `main` Button, first channel filled, the
   others outline" (the plan §8 issue 1, the `PlatformContact` pattern).** The build added a second «واتساب» above
   the list, so WhatsApp shows twice (shot `space-1440-ar-light-2-after.png`). **Build it as approved:** the list's
   own first channel (WhatsApp when the space has it) becomes the `main` button and is not repeated; the others keep
   their look. Update `directory.md`'s line, the component's test, and the shot.
3. **N1** — foundation §5: link ADR 0022 right after "a step darker", as the plan's §5 asked.
4. **N2** — say plainly in the report's §4 that the hover's distance case stands on the shared `it.each` (no hover value
   was seen failing it); no code.
