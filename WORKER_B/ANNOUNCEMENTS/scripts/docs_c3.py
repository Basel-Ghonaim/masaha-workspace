R = 'C:/dev/masaha/app-b/docs/'


def ed(p, pairs):
    s = open(R + p, encoding='utf-8', newline='').read()
    for a, b in pairs:
        assert s.count(a) == 1, (p, a[:80])
        s = s.replace(a, b)
    open(R + p, 'w', encoding='utf-8', newline='').write(s)


ed('api/api-contract.md', [
("""- **Deleted, never removed** ([ADR 0007](../architecture/decisions/0007-soft-delete.md)): a deleted announcement keeps its row and leaves every read and the live status at once.""",
"""- **Deleted, never removed** ([ADR 0007](../architecture/decisions/0007-soft-delete.md)): a deleted announcement keeps its row and leaves every read and the live status at once.
- **The list and its summary** show each closure's extension of the subscriptions it covered, which `subscriptions` owns: they are composed there ([conventions §9](../backend/conventions.md#composed-reads)), on the same path. Reads of the staff, asking no `can()`."""),
("""  state: 'RUNNING' | 'UPCOMING' | 'ENDED'
}
```

#### `POST /manage/spaces/:spaceId/announcements` · 🧾 · `Idempotency-Key`""",
"""  state: 'RUNNING' | 'UPCOMING' | 'ENDED'
}

ExtensionApplied = {
  days: number,
  subscriptions: number,           // how many it moved
  appliedAt: string,
  appliedBy: { id: number, name: string }
}

ManagedAnnouncement = Announcement & {
  extension?: ExtensionApplied | null   // on a CLOSURE only: null until its subscriptions are extended
}

AnnouncementsSummary = { running: number, upcoming: number, ended: number, closuresAwaitingExtension: number }
```

#### `GET /manage/spaces/:spaceId/announcements` · 🧾
- **Query:** `state` (`RUNNING`, the default, `UPCOMING` or `ENDED`; `invalid_choice` otherwise) and §4's `page` and `limit`.
- **200:** `ManagedAnnouncement[]` of that state, not deleted, with §4's `meta`: running and upcoming by start, then id; ended by end, the latest first, then id. Built 2026-10-24, #PRNUM.

#### `GET /manage/spaces/:spaceId/announcements/summary` · 🧾
- **200:** `AnnouncementsSummary`: how many announcements, not deleted, are running, upcoming and ended (the list's tabs), and `closuresAwaitingExtension`, the closures started within the last 30 days, not deleted, whose subscriptions were not extended (the owner's overview reads the same count). Built 2026-10-24, #PRNUM.

#### `POST /manage/spaces/:spaceId/announcements` · 🧾 · `Idempotency-Key`"""),
])

ed('backend/conventions.md', [
("""| `subscriptions` | L3 | `subscriptions`, `check_ins`, `closure_extensions`, `subscription_extensions` | manage | Subscriptions, their check-ins and closure extensions; the pure progress and status; auto check-out of its own check-ins |""",
"""| `subscriptions` | L3 | `subscriptions`, `check_ins`, `closure_extensions`, `subscription_extensions` | manage | Subscriptions, their check-ins and closure extensions; the managed announcements list with each closure's extension, and its summary (§9); the pure progress and status; auto check-out of its own check-ins |"""),
("""- **The customers list and the customer file** → `desk`.
""", """- **The customers list and the customer file** → `desk`.
- **The managed announcements list and its summary** → `subscriptions` (`closures`), the lowest module above `announcements` that owns a closure's extension: `announcements` pages one state and counts them, and `subscriptions` adds each closure's extension, how many it moved and who applied it, and counts the started closures with none. The writes stay `announcements`'. The owner's overview will read `closures.summary`. 2026-10-24, #PRNUM.
"""),
])

ed('features/subscriptions.md', [
("**Last Updated:** 2026-10-22", "**Last Updated:** 2026-10-24"),
("""- Closes the check-ins due by the auto check-out, as a timed job.
""", """- Closes the check-ins due by the auto check-out, as a timed job.
- Answers the space's managed announcements list, each closure with the extension of the subscriptions it covered, and its summary, composed with [`announcements`](announcements.md).
"""),
("""- **The timed jobs** (`shared/jobs`), which run its auto check-out.
""", """- **The timed jobs** (`shared/jobs`), which run its auto check-out.
- **The space's staff**, who read the managed announcements list and its summary through it.
"""),
("""- **Leaves** the money paid on a subscription to [`payments`](payments.md), which reads a subscription's due through this module's function.""",
"""- **Leaves** the money paid on a subscription to [`payments`](payments.md), which reads a subscription's due through this module's function; the announcements, their writes and their states to [`announcements`](announcements.md), whose pages and counts the managed list composes."""),
("""- Its attendance is counted in the database, by `subscription_usage`;""", """- The managed announcements list and its summary are its `closures` router, mounted at `/announcements` beside `announcements`' writes (S10, [conventions §9](../backend/conventions.md#composed-reads)).
- Its attendance is counted in the database, by `subscription_usage`;"""),
("""- **A subscription of at most seven days by its dates is ending soon on its last day only.**""",
"""- **The managed announcements list is composed here, not in `announcements`** (S10, the owner's Q2). *Why:* the list shows each closure's extension, which `subscriptions` owns, and `announcements` (L2) cannot read it; `subscriptions` is the lowest module above both. 2026-10-24, #PRNUM.
- **The summary counts a closure as awaiting its extension only for 30 days from its start** (the owner's Q6). *Why:* a closure the owner chose not to extend must stop asking. 2026-10-24, #PRNUM.
- **A subscription of at most seven days by its dates is ending soon on its last day only.**"""),
("""the controller and the manage router (the corrections).""", """the controller and the manage router (the corrections); `closures/`, the managed announcements list and its summary."""),
("""- #109 — a check-in's minutes in SQL;""", """- #PRNUM — the managed announcements list, each closure with its extension, and its summary (`closures/`).
- #109 — a check-in's minutes in SQL;"""),
])

ed('features/announcements.md', [
("""- Tells the live status which spaces a running closure covers ([occupancy](occupancy.md)).""",
"""- Pages one state's announcements and counts them by state, for the managed list and its summary, which [`subscriptions`](subscriptions.md) composes with each closure's extension.
- Tells the live status which spaces a running closure covers ([occupancy](occupancy.md))."""),
("""- **The live status** ([occupancy](occupancy.md)): a running `CLOSURE` makes a space `CLOSED`.""",
"""- **The live status** ([occupancy](occupancy.md)): a running `CLOSURE` makes a space `CLOSED`.
- **[`subscriptions`](subscriptions.md),** whose managed list and summary read its pages, its counts and its started closures."""),
("""**End now, start now, delete.**""", """**The list's reads.** A page of one state, not deleted: the state a filter on the instants, running and upcoming by start then id, ended by end, latest first, then id; its count in parallel. The counts of the three states are one grouped query; the started closures (since a given day) one more. `subscriptions` adds the extensions ([its document](subscriptions.md)).

**End now, start now, delete.**"""),
("- 2026-10-24, #PRNUM — posted (idempotent), edited, ended, started and deleted by the staff.",
 "- 2026-10-24, #PRNUM — posted (idempotent), edited, ended, started and deleted by the staff; the pages and counts the managed list composes."),
])
print('ok')
