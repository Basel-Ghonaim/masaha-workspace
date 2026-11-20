# Carried from #144 (the identity) — the WOMEN_EVENING PR's first commit

#144 (ink + berry and the logo) merged on 2026-11-13 at `88c5eb3f` on the owner's word, with its review findings
**carried to the next PR's first commit** (the owner's rule: small review fixes ride the next PR's first commit, named
in its description). Both reviews: `C:\dev\masaha\workspace\TASKS\IDENTITY\6_REVIEW_PROD_R1.md` and `…_R2.md` —
read each finding's *Where*, *Scenario* and *Fix* there. **Every one below was verified by the supervisor in the
code at `4cff26c7`** (= `main`'s tree after the merge).

One commit, first on the rebased branch: `fix(design-system): identity review follow-ups` (≤ 50 characters, a body
listing each item), its tests seen failing first, as the project's rules say.

## From R1 (the colour system)

1. **R1-F1 — the contact tile's caption under AA while hovered** (`features/spaces/components/contacts/ContactsView.tsx`):
   the caption takes `foreground` while its link is hovered (`group` on the anchor, `group-hover:text-foreground` on
   the caption), as DataTable's sort header, SegmentedControl and the `md` tabs do on the wash. A test of the class
   or the pair; foundation §5's wash sentence holds.
2. **R1-F2 — hover equals selected in dark where "selected" is still `secondary`:** `pages/site/account/AccountLayout.tsx`
   and `features/spaces/components/editor/SectionIndex.tsx` — the current entry as SiteMenu's (the selected tint,
   `bg-accent text-accent-foreground`, no ghost hover on it); `features/directory/components/near/NearMeButton.tsx` —
   the pressed toggle takes **the chip's selected look** (`bg-accent text-accent-foreground border-spark`, kept under
   the pointer) — the supervisor's recommendation, approved with the merge. Search for any other
   `? 'secondary'` current/pressed variant and treat it the same (`git grep -nE "\? ?'secondary'"`); list them.
3. **R1-F3 — `check:classes` misses other spellings of its states** (`apps/web/scripts/checkClasses.ts`): normalise
   `data-[state=open]` → `data-open`, `aria-[expanded=true]` → `aria-expanded`, `data-[highlighted]` and
   `data-[highlighted=true]` → `data-highlighted`; add `active`. Not `aria-selected` (react-day-picker's chosen day).
   T12 cases for each; one line in foundation §3 (e).
4. **R1-F5 — T9 pins the OKLab → sRGB inverse** (`tokens/semantic.unit.test.ts`): one hand-written chromatic
   expectation through the inverse — `painted('dark', 'accent')` is `#471f46` (Chrome's painted pixel, EC3).
5. **R1-F4 — a ghost «⋯» inside a hovered table row has no hover of its own** (older, Sea's too): **record only**, as
   a finding (the next free number — 226 expected; check the index), naming `Table.tsx`, `Button.tsx` and the three
   menus the review lists. No change.

## From R2 (the logo and the rest)

6. **R2-F1 — T14 also asserts the favicon's shapes use their classes** (`apps/web/scripts/browserIcons.unit.test.ts`,
   `apps/web/public/favicon.svg`): both `<use>` carry `class="ink"`, the dots' `<path>` `class="spark"`, no drawn shape
   outside `<defs>` without a class.
7. **R2-F2 — T19 asserts the admin shell's logo form per sidebar mode** (`pages/dashboard/routes.component.test.tsx`):
   the full form's `viewBox` (`263 45 2473 903`) at 1280; a second case at 800 asserts the mark's (`190 17 778 778`).
8. **R2-F3 — the prototype's reset e-mail tab icon** (`docs/design/prototype/Reset email.html:5`): link
   `masaha/logo/masaha-mark-berry.svg` (the page is light-only). Prototype checks: `check-parse`, `check-classes`.
9. **R2-F4 — the first download's growth in words:** no code — the WOMEN_EVENING PR's description, under *Review fixes
   carried from #144*, gives #144's figure right (+15,681 B, +8,073 compressed) for the record.
10. **R2-F5 — foundation §16's source files line:** «the full logo and the mark, light and dark, and the app icon»
    (there is no dark app icon).

## Also for the design review round 3

R1-F1 and R1-F2 are known: the round-3 reviewers cite them (`IDENTITY\6_REVIEW_PROD_R1.md`), never as new.
