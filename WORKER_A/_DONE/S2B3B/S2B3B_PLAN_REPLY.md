# S2b-3b — reply to your plan

The plan is approved, with the three changes below. **Save it first** (as amended here) to
`C:\Users\basel\.prompt\MASAHA_WORKER_A\PLAN\S2B3B_PLAN.md`, then cut the branch and build.

## Design issues (§6)
- **1–6: approved** (two landmark fields; "Optional" on every optional field; the area on the grid;
  the grouped list instead of the helper; the title once, in the top bar, with the breadcrumb; the
  map's new hint and the Coordinates field).
- **7: your fallback, not the top bar.** "Add space" is a row **above the list, at the end, at every
  width** — the desktop design's place, applied to the phone too. *Why:* on a phone the top bar
  already holds the menu, the title, the theme toggle and the avatar; a labelled button there would
  crowd or wrap it. The page composes the row above the list, so no new slot is needed in
  `space-links`.
- **8:** agreed — not mistakes, the edit screen's.

## Stronger decisions (§5)
- **S1–S7, S9–S11: approved.**
- **S8 — `prepare` and `failureLines` in `shared/forms`: approved**, as a change to a shared
  mechanism, because this form is their first real user and the edit screen and the owner's profile
  will be the next; architecture §3 › *Forms* updated in the same commit, each with its test.
- The stated exceptions (the layer's surfaces `index.ts`, `data.ts`, `leaflet.css`; `shared/map` the
  one reference to `leaflet.css`) are approved; write each where its rule lives.

## Change 1 — finding 27 gets no "Studied" line
Documentation rules §1: a record changes in three ways only, and a finding gains **only its status
and a dated resolution**. A "Studied" line is a fourth. So, if 27 stays open (D13's expected
outcome, confirmed), **leave its file untouched**, and put the study — what rolldown offers, why no
group fixes it, the manifest before and after — in the PR description and the report.

## Change 2 — the navigation
`navigation.ts` gains the add page's **path** only: it must not become a sidebar item. Check it in
the routes test.

## Change 3 — the attribution's words
Keep the name **"OpenStreetMap"** untranslated in both languages (the licence's attribution names the
project), as your «© مساهمو OpenStreetMap» does; and the link to `openstreetmap.org/copyright` in both.

## The Arabic copy (§13.4)
Approved as listed: «إضافة مساحة» · «أُضيفت {name}» · «اختياري» · «الإحداثيات» ·
«لم تُحمَّل الخريطة. أدخل الإحداثيات بدلًا منها.» · «© مساهمو OpenStreetMap» ·
«هذه النقطة خارج قطاع غزة» · «أُضيفت مساحة بالاسم نفسه في اللحظة ذاتها. أضِفها مرة أخرى.» ·
«الدبوس عند {point}». List any further Arabic line in the PR for approval.

Everything else as planned: the five commits, the breaks made once each, the manifest before and
after, phase 4 in full, the real run, the screenshots, the merge-tree check against B's open PR.
An independent review follows; don't merge.
