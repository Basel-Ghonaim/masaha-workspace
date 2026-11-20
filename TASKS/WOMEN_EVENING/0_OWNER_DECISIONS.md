# WOMEN_EVENING — the owner's decisions (from 2026-11-12)

One task: the owner-declared evening hours and the women's halls. Earlier direction:
`TASKS\DIRECTORY_FILTERS\0_OWNER_DECISIONS.md` A4–A5, `TASKS\DIRECTORY_PROD\0_OWNER_DECISIONS.md` decision 8,
`TASKS\SPACE_PROFILE\0_OWNER_DECISIONS.md` A3 (where they live in the profile — decided here). Analysis now;
execution only after the IDENTITY PR merges (same directory and profile files).

## What exists (read in the code, 2026-11-12)

- The live filter «مفتوحة مساءً» (`evening`, #139): a space whose week has a day closing at 20:00 or later.
- Hours: one continuous range a day, 0–1440 minutes, nothing past midnight (spaces.md, F4).
- Shifts: a name and a from–to inside the hours; prices may name a shift; packages may name one. In `masaha_dev`, six
  spaces hold two shifts named «صباحي» and «مسائي» — shifts of the main period, **not** the evening below.
- Packages are private (D7): the owner and the desk see them, visitors never.

## The evening — final (2026-11-12)

- **E1 — what it is:** the space stays open when most spaces have closed (most close between 16:00 and 18:00). It is
  **not** the «مسائي» shift (a shift lies inside the main 08:00–18:00 period) and **not** tied to a fixed clock hour.
- **E2 — the day is continuous:** a space never closes mid-day; with an evening it stays open until its closing time.
- **E3 — past midnight: deferred** — not in this task; its own task if an owner ever needs it.
- **E4 — the model (the owner's, adopted):** the space's owner **declares** that the space works in the evening (one
  switch on the space); his **regular hours** say until when it is open (e.g. 23:00). No evening prices, no evening
  section, no evening engine. Who the evening serves is the owner's call, never the platform's.
- **E5 — an evening subscription is a package** the owner makes (private, sold at the desk); visitors learn of the
  evening and its closing time, not its price.
- **E6 — where the switch lives:** inside «ساعات العمل» — a box «المساحة تعمل مساءً» in its Sheet, under the hours;
  its view adds a line «دوام مسائي»; the public page and the directory's card show a «دوام مسائي» mark. The admin's
  editor the same.
- **E7 — the directory:** «مفتوحة مساءً» passes a space **by its owner's switch only** (the 20:00 rule goes).
- **E8 — the merge day:** the switch is turned on once, for every space whose hours already close at 20:00 or later
  on at least one day, so the filter loses no space on that day; an owner turns it off if it is wrong.
- **E9 — a gentle hint, never a block:** with the switch on and no day closing after 18:00, the owner's profile says
  so («شغّلت الدوام المسائي، لكن ساعات عملك تنتهي مبكرًا») — the wording settled in the plan.

## Women's halls — final (2026-11-12, every point as the supervisor recommended)

- **W1 — the owner's facts:** there is no "women-only space"; there are **women's halls** — private, not mixed. Most
  spaces have one; some work mixed.
- **W2 — an amenity and a filter**, in the simplest way.
- **W3 — a catalogue amenity with a fixed key:** «قاعة للنساء» / "Women's hall", key `womens_hall` (an amenity's key
  never changes, lookups.md), added to the catalogue **by the task's migration in every environment**. The live
  catalogue holds no such amenity (its public list read 2026-11-12: eight amenities). The owner ticks it in «المرافق»
  like any amenity; the public page shows it with the others and its icon. No new screen, no new editor. Because the
  filter depends on this one amenity, the plan says what the admin may do to it (rename and reorder yes; its key
  fixed; deleting or retiring it — the plan proposes the rule).
- **W4 — a mark on the directory's card:** «قاعة للنساء», like «دوام مسائي» (E6).
- **W5 — the filter** «قاعة للنساء» in the panel's «أخرى» group, beside «موثّقة» and «أسعار للطلاب».
- **W6 — never «مختلطة»:** a space without the amenity says nothing about it (the owner may simply not have ticked
  it); only a women's hall that exists is shown.
- **The general amenities filter stays dropped** (R2 of DIRECTORY_FILTERS, the owner's 2026-10-12 decision): this is
  one fixed filter for one amenity that decides who can work there, not a filter over the catalogue.

## The Arabic texts (approved by the owner, 2026-11-14 — the supervisor's wordings)

- **The box's help** (under «المساحة تعمل مساءً»): «يظهر للزوار «دوام مسائي»، وساعات العمل أعلاه تحدّد حتى متى تبقى
  المساحة مفتوحة.»
- **The hint (E9):** «شغّلت الدوام المسائي، لكن ساعات العمل لا تمتد بعد 18:00 في أي يوم.»
- **`AMENITY_IN_FILTER`:** «لا يمكن إيقاف هذا المرفق، فدليل المساحات يعتمد عليه في فلتر «قاعة للنساء». يمكنك تغيير
  اسمه وأيقونته وترتيبه.»
- The English follows the same meaning. Commit `6f6a59ab`'s 51-character subject: **waived by the owner**.

## #145's review — the fix round (the owner, 2026-11-14)

- A fix round before the merge: F1, F3, F4, F5, N1 of `7_REVIEW.md`, each folded into its commit; F2 → finding 227
  and a rollback step in the PR's description (no code).
- **Only the test files the round touches run locally**; CI judges the rest (a stated, one-off exception). The message:
  `9_FIX_ROUND.md`.

## Next

A plan prompt (`1_PLAN_PROMPT.md`) for a Claude Code planner: the evening switch and its data (one migration: the
space's evening column, E8's one-time switch-on, and W3's amenity row — shown in full for the owner), the API filter
and response fields, `packages/shared`, the profile («ساعات العمل»), the directory (filters, card marks, the public
page), the admin's editor, documents and tests. **Execution after the IDENTITY PR merges** (same directory and
profile files).
