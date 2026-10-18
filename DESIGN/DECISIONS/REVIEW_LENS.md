# The design review lens — Masaha

Every design reviewer reads this before it starts, and judges by it. It sets **what to look for**,
**how to propose**, and **the shape of the report**. The rules it applies are owned by the
repository's documents; this lens links them and adds nothing to them.

## 1. The goal

Not only to find mistakes: **to arrive at the best design** for each component, section and page.
Masaha's users are students, freelancers, space owners and reception staff in Gaza, often on a phone,
on a weak connection, in Arabic first. Everything must be **clear, easy and logical**: a user should
know at once where they are, what the page is for, what to do next, and what happened after they
did it.

## 2. What the design owns, and what it does not

- **The prototype owns the pages and the flows:** layout, order, the division of a page into
  sections and components, the place of each action, the words, the states.
- **The code's design system owns the components** (`apps/web/src/shared/design-system/`, shown at
  `/__showcase`): a flaw *in* a component (a Button's look, a Field's states) is reported with
  **level: design system** — it is fixed in code, by the web worker, not in the prototype.
- **The documents own the rules:** `docs/frontend/design-system/foundation.md` (tokens, type,
  direction, responsive, accessibility, the component contract), the ADRs, `docs/project/overview.md`
  (v1 and *Not in v1*), `docs/architecture/data-model.md`. A design that breaks a rule is a defect;
  a rule that makes the design worse is reported as a **rule in doubt**, never silently bent.
- **Known limits of the archive** (`docs/design/README.md` › *Known limits*: placeholder navigation
  icons, illustrative sample data, the Google font offline, the three superseded frames) are **not**
  reported.

## 2b. What is already settled

Read `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_SHARED.md` (and any later `DECISIONS_*.md`)
before you start. **What it settles is not reported again:** the page header, the public-state
control, the grouped navigation, the account menu, the filter bar, pagination, the states, action
feedback, confirm-or-undo, enabled saves. Report only **how a page applies them** where that needs a
choice (which action is primary here; which columns survive at 768; which of this page's actions is
"felt by others"), or a page where a settled pattern does not fit, with why.

## 2c. Three checks every review makes
- **Every width:** 390, **768** and 1440. The board has no 768 frame; look anyway — it is where shells
  and tables break.
- **Against the API contract** (`docs/api/api-contract.md`): every list is paged (§4); every action
  can answer a failure and a 429; every field the screen shows or sends exists in the contract and
  the data model. A design the API cannot serve is a defect.
- **Confirm or undo:** classify each destructive action of the page by P9 — reversible and affecting
  no one else, or irreversible / felt by others.

## 3. What to look for

### A. Defects
1. **Alignment and grid:** elements off their column or baseline; edges that do not line up; a
   control narrower or wider than its siblings for no reason.
2. **Spacing:** gaps that differ between twin elements; spacing outside the scale (foundation §5
   *Other scales*).
3. **Hierarchy and type:** more than one primary heading; a title repeated; the wrong type style
   (foundation §7); weight or size that fights the hierarchy.
4. **Colour and tokens:** a semantic role misused (danger for a non-destructive action, success for
   a neutral fact); contrast below foundation §10.
5. **Components:** the wrong component for the job (a select for three choices, a dialog for a long
   form), a wrong variant or state, a control drawn in a state it cannot be in.
6. **Direction (RTL / LTR):** what is not mirrored that should be, what is mirrored that should not
   be (numbers, phone numbers, times, Latin names), icons pointing the wrong way, mixed-direction text
   broken (foundation §8).
7. **Responsive:** a layout that breaks at 390, 768 or 1440 (foundation §9); content cut off; a
   table with no phone form; a touch target too small.
8. **States:** a missing loading, empty, error, disabled, pending, success or "too many requests"
   state; a state that says nothing useful.
9. **Accessibility:** no visible focus; a control with no name; information by colour alone;
   order that a keyboard or screen reader would follow wrongly (foundation §10).
10. **Words:** a term against the glossary (`docs/project/glossary.md`); Arabic that reads as a
    translation; the same thing named two ways; a label that does not say what happens.
11. **Truth to the product:** a public seat count (ADR 0008 — live status is a state, never a count),
    the device's location sent anywhere, anything on *Not in v1*, a field the data model has not.

### B. Better design (as important as the defects)
1. **The division of the page:** does each section have one job? Are related things together and
   unrelated things apart? Would the page be clearer split, merged or reordered? Is a component doing
   two jobs?
2. **The primary action:** one per screen, obvious, in the same place on every screen of its kind
   and at every width.
3. **The flow:** the fewest steps to the user's goal; no dead ends; a way back; nothing asked twice;
   the order a person would actually follow at a front desk or on a phone.
4. **Patterns across pages:** the same job done the same way everywhere (filtering, adding, editing,
   confirming, a list that becomes cards on a phone, a page header). Name the pattern and where it
   differs.
5. **Progressive disclosure:** the common case first, the rare one a click away; no wall of fields.
6. **Feedback and recovery:** every action says what happened; every failure says what to do; a
   destructive action can be undone or is confirmed in words that are true.
7. **Navigation:** can each role find its daily tasks first? Are menus grouped by what people do?
8. **Arabic first, phone first:** reading order, thumb reach, the length of Arabic labels.

## 4. How to propose

- Each proposal is **built from the design system's own components and tokens** (foundation §12 is
  the inventory); a proposal that needs a new component says so and why.
- Each says **why it is better for the user**, in one or two sentences, and its **cost** (S / M / L).
- A proposal at **pattern** level names every page it would change.
- Prefer one strong proposal to three options; give options only when the choice is the owner's
  (a trade-off, a taste).

## 5. The report

Save it to the file the prompt names. English, concise. In this order:

1. **Summary:** the five most important points, in one line each.
2. **Patterns** (level: pattern): the cross-page proposals first — they change the most.
3. **Issues**, one block each:
   - **ID** (the prompt gives the prefix, e.g. `SH-001`), **title**;
   - **type:** defect | improvement; **level:** design system | pattern | component | page;
   - **impact:** high | medium | low (for the user, not for the eye);
   - **where:** the frame's label in `docs/design/INDEX.md`, its prototype URL with its state
     parameters (on the reviewer's local server), and the screenshot's path in `docs/design/screens/`;
   - **evidence:** a cropped capture, saved as `<ID>.png` in the folder the prompt names;
   - **what is wrong / what could be better;**
   - **proposal**, **why it is better**, **cost**;
   - **rule:** the document and section it applies or puts in doubt, if any.
4. **Rules in doubt:** each rule of the documents the review thinks makes the design worse, with why.
5. **Not reviewed:** what was out of reach, and why.
