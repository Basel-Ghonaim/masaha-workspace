# Carried from #91 (OWNERS PR 3) into USERS' fix round

The owner's rule (2026-10-19): #91 merges whatever its last check finds; what is found is recorded here and
fixed in **USERS' fix round** (not its first execution). The supervisor adds these to USERS'
`7_FIXES_PROMPT.md`.

#91 merged at `a8c39bda` (head `db1fc6f0`), 2026-10-19. The supervisor's check of fix round 1: every review
fix present (the unlink reads `isFetching`; focus fallback; the person side's fresh verification; `users.md`;
«ربط مالك» `aria-disabled`), eight breaks red, CI green, `CLEAN`.

1. **The unlink dialog's line flashes its placeholder after a confirmed unlink** (the executor's own note,
   FR1.7 point 6): the admin refresh refetches the space's owners while the dialog is still open and busy, and
   `reading = owners.isFetching` turns the consequence back to "reading" until the dialog closes. Harmless (the
   action is already sent), but visible. Fix: hold the consequence once the unlink is sent (e.g. keep the last
   settled line while `unlink.isPending`). `features/space-links/hooks/unlink/useUnlinkOwnerDialog.ts`.

2. **Found in USERS' own real run (the executor's stop, 2026-10-19), deferred to the fix round by the
   owner:** after «تم» in the issued-password dialog, focus lands on `<body>`, not the row's menu button —
   the plan's `focus()` runs before Radix's own return on unmount, which then targets the removed «إصدار»
   button. Fix (the executor's option A): `TemporaryPasswordDialog` takes an optional `returnFocus`, focused
   from `onCloseAutoFocus`; one test (red, then green), folded into commit 7. OWNER_SETUP's staff dialog
   reuses it.

**For worker B, not A:** #91 recorded findings **94 and 95**; SETTINGS planned its finding as 94 — it
renumbers when it rebases (its approval note already says so).
