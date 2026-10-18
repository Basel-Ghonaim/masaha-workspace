# OWNERS — amendment to the prompt (read before you finish the plan)

The prompt was written before checking the admin's design decisions, which the owner approved on
2026-10-10: `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_ADMIN.md` (read **A4, A5, A6** and the
*Rules changed* line on `PATCH /admin/users`). Where they differ, **they win**. Rework the plan on
these points. Everything else in the prompt stands.

1. **D1 is replaced: one space at a time.**
   - Adding an owner creates the account (a temporary password, shown once) or upgrades an existing
     one, and links it to **one** space, in one transaction. The design's submit is «إنشاء حساب وربط».
   - Linking more spaces is the separate link call, one space each time.
2. **D5 and D6 are widened: linking from a space may choose any person** (A4), an owner or a user,
   by name or email.
   - Linking a user makes them an owner.
   - Still refused: a suspended account, an admin, a soft-deleted space, and an active reception link
     at that same space (D6 stands).
   - D2's explicit upgrade still applies to the add-owner call. The link call's choice of a user is
     itself the deliberate act: the web says what will happen before it is done (A5).
3. **The global role `OWNER` follows the links** (A5, ADR 0009). This replaces the prompt's "it stays
   when the last link goes".
   - A user becomes `OWNER` with their first active owner link, and is `USER` again when their last
     one ends.
   - Both are role changes, so security.md's revocation applies: the user's sessions end.
   - An unlink that leaves the person other owner links changes no role, and ends no session (D4
     stands for that case).
   - Record the rule as ADR 0009's *Revised* line, and in `docs/plans/v1-mvp.md`'s `PATCH /admin/users`
     row: the role offered there is `USER` or `ADMIN`, and `OWNER` follows the links.
4. **D7 is replaced: the owners page is a view of the users list** (A6).
   - Build the read side of `GET /admin/users`: paged (20), `?q=` on the name or the email, a role
     filter (`role=owner` gives the owners page), a state filter (active or suspended).
   - Each row carries the account's id, name, email, role, whether it is suspended, and its active
     owner links (each space's id and both names).
   - Build no `GET /admin/owners`.
   - The users item (later) adds the actions only: suspend, the role change, the admin's temporary
     password.
5. **New: the temporary password's handover is recorded** (A5). The one-time password dialog asks
   how it was handed over (WhatsApp, in person, other), after the password is shown. Add a small
   follow-up call that writes the chosen channel to the audit, tied to the creation it follows. Settle
   its path and payload in the plan. The users item will reuse it for the admin's temporary password.
6. **Not in this item:** A3's `status=deleted` filter on `GET /admin/spaces` (finding 44). It waits for
   a later item.

Show in the plan's *Stronger decisions* where these change your design, and keep finding 43 (D8) as
it is.
