R = 'C:/dev/masaha/app-b/docs/'


def ed(p, pairs):
    s = open(R + p, encoding='utf-8', newline='').read()
    for a, b in pairs:
        assert s.count(a) == 1, (p, a[:80])
        s = s.replace(a, b)
    open(R + p, 'w', encoding='utf-8', newline='').write(s)


ed('api/api-contract.md', [
("""`OUTSIDE_OPENING_HOURS` when the space has hours and is not open by them; and, for a subscriber,""",
 """`OUTSIDE_OPENING_HOURS` when the space has hours and is not open by them; `CLOSURE_IN_FORCE` while a closure the space announced runs ([Announcements (managed)](#announcements-managed), 2026-10-24, #PRNUM); and, for a subscriber,"""),
("""`OUTSIDE_OPENING_HOURS` (warning only; the check-in succeeds with `meta.warnings`) ·""",
 """`OUTSIDE_OPENING_HOURS` (warning only; the check-in succeeds with `meta.warnings`) · `CLOSURE_IN_FORCE` (warning only: a check-in, a visit's or a subscriber's, while a closure the space announced runs; the check-in succeeds with `meta.warnings`, 2026-10-24, #PRNUM) ·"""),
])

ed('architecture/data-model.md', [
("""- **Full warning:** a check-in (visit or subscription) while present ≥ capacity warns, never blocks (a subscriber's since 2026-10-22, #109).""",
 """- **Full warning:** a check-in (visit or subscription) while present ≥ capacity warns, never blocks (a subscriber's since 2026-10-22, #109); and while a closure runs, `CLOSURE_IN_FORCE`, never a refusal either (2026-10-24, #PRNUM)."""),
])

ed('backend/conventions.md', [
("""- **check-in** of a visit or a subscription, with the full-space warning from `occupancy`;""",
 """- **check-in** of a visit or a subscription, with the full-space warning from `occupancy`, and its closure warning, from the closures `announcements` reads (2026-10-24, #PRNUM);"""),
])

ed('features/occupancy.md', [
("**Last Updated:** 2026-10-22", "**Last Updated:** 2026-10-24"),
("""the closures in force from `announcements`, and the week from [`spaces`](spaces.md); each through its service, which alone reads its table. `announcements` holds only these reads so far, with no capability document of its own.""",
 """the closures in force from [`announcements`](announcements.md), and the week from [`spaces`](spaces.md); each through its service, which alone reads its table."""),
("""then `OUTSIDE_OPENING_HOURS` when the space has hours and is not open by them now. They never refuse the check-in.""",
 """then `OUTSIDE_OPENING_HOURS` when the space has hours and is not open by them now, then `CLOSURE_IN_FORCE` while a closure the space announced runs (the live status's `closedAt`, in the same transaction). They never refuse the check-in."""),
("""- #109 — *present* written once (`present.ts`), for every reader; whether a customer is present, for the desk.
""", """- #109 — *present* written once (`present.ts`), for every reader; whether a customer is present, for the desk.
- #PRNUM — the closure warning at check-in, `CLOSURE_IN_FORCE`.
"""),
])

ed('features/desk.md', [
("""- Checks a visitor in, with what the check-in warns of: the space full, or outside its hours.""",
 """- Checks a visitor in, with what the check-in warns of: the space full, outside its hours, or announced closed."""),
("""with what it warns of: the space full, outside its hours, the subscription not started or expired,""",
 """with what it warns of: the space full, outside its hours, announced closed, the subscription not started or expired,"""),
("""- #110 — a subscriber's check-out after its due time closed at it;""",
 """- #PRNUM — the closure warning on both check-ins, from `occupancy`.
- #110 — a subscriber's check-out after its due time closed at it;"""),
])

ed('plans/v1-mvp.md', [
("""- **Closes:** [finding 8](../architecture/findings/8-the-stress-tests-applied-filter-tag-has-no-component.md), at the start of the step: the removable filter tag.

### 11. Finance, audit and settings""",
 """- **Closes:** [finding 8](../architecture/findings/8-the-stress-tests-applied-filter-tag-has-no-component.md), at the start of the step: the removable filter tag.
- **Built:** announcements and the closure warning, on the API: posted (idempotent), edited, ended, started and deleted by the staff; the managed list with each closure's extension state and its summary; a space's page's announcements; `CLOSURE_IN_FORCE` at check-in (#PRNUM, [api-contract › Announcements (managed)](../api/api-contract.md#announcements-managed)). The screens remain planned.

### 11. Finance, audit and settings"""),
("""the lists (`GET …/check-ins`) (#109) (""",
 """the lists (`GET …/check-ins`) (#109), and the announcements: the post, the edit, the end, the start and the delete, the list and its summary (#PRNUM) ("""),
("""| GET / POST | `/manage/spaces/:spaceId/announcements` | 🧾 | |
| PATCH / DELETE | `/manage/spaces/:spaceId/announcements/:id` | 🧾 | |""",
 """| GET / POST | `/manage/spaces/:spaceId/announcements` | 🧾 | the list by state, each closure with its extension state, and `…/summary`; the post, idempotent (built, #PRNUM) |
| PATCH / DELETE | `/manage/spaces/:spaceId/announcements/:id` | 🧾 | edit, delete (soft); `POST …/:id/end`, `POST …/:id/start` (built, #PRNUM) |"""),
])

ed('project/overview.md', [
("**Last Updated:** 2026-10-22", "**Last Updated:** 2026-10-24"),
("""- [Occupancy](../features/occupancy.md): on the API, a space's private capacity,""",
 """- [Announcements](../features/announcements.md): on the API, a space's announcements, posted, edited, ended, started and deleted by its staff; the managed list with each closure's extension state and its summary; a space's page's running and upcoming announcements; the closure warning at check-in.
- [Occupancy](../features/occupancy.md): on the API, a space's private capacity,"""),
])

ed('README.md', [
("""- [desk.md](features/desk.md) —""",
 """- [announcements.md](features/announcements.md) — a space's announcements: posted (idempotent), edited, ended, started and deleted by its staff, the closures the live status reads, and the public ones (API only).
- [desk.md](features/desk.md) —"""),
])
print('ok')
