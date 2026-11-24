# WI-B — ADR 0022, the draft for the owner's review (2026-11-24)

> The owner's decision A18 (`DESIGN\AUTH\0_OWNER_DECISIONS.md`, 2026-11-24): the berry is the identity, the main
> action and a few brand moments — not the site's main colour, and no longer a mark only. Seen and approved in the
> pictures of P1 / P2 (masaha-prototype `Space details.html?v=inplace`, `Reset password.html?v=inplace`).
>
> **What is committed, word for word:**
> 1. the file `docs/architecture/decisions/0022-the-berry-on-the-main-action.md` — the text between the two rules;
> 2. in ADR 0019, a dated *Revised* line under its status line (the documentation rules' one way to change an ADR):
>    `> **Revised:** <date> — the main action takes the berry; links, controls and structure keep the ink; the berry-to-plum scale on a few brand surfaces ([ADR 0022](0022-the-berry-on-the-main-action.md)). The body below is left as first written.`
> 3. in `docs/README.md`'s list of decisions, after 0021:
>    `  - [0022](architecture/decisions/0022-the-berry-on-the-main-action.md) the berry on the main action: the ink keeps links, controls and structure; brand surfaces take the berry-to-plum scale`
>
> Decision-level only: no token, file or component names. WI-B's plan names them (a role of its own for the main
> action is likely, since today's `primary` also draws links and checked controls, which keep the ink).
> **Contrast, measured by the supervisor** (WCAG 2): the berry's 600 step with white text 5.91 : 1, its 700 (hover)
> 7.94 : 1; the 400 step with the darkest ink in dark 6.84 : 1; as a shape on the light page 5.69 : 1, on the dark page
> 6.84 : 1. Today's spark (500) with white text is 4.11 : 1 — below AA, which is why the action takes a darker step.

---

# ADR 0022 — The berry on the main action

> **Status:** Accepted · **Date:** 2026-11-24

## Context
[ADR 0019](0019-ink-and-spark-brand.md) gave the brand two roles: an ink for actions, links and structure, and a berry spark for what matters now, never on an action. Built across the site, it kept the pages clear, but the berry became almost invisible: two dots in the logo and a few selected states. Design rounds on the public pages kept reading as grey and empty, and the owner found the identity missing from the screens people see first.

Making the berry the site's main colour was considered and rejected. The directory's first information is the live state of each space, shown in the status colours, and a berry everywhere would compete with it. The dashboard is a daily tool of dense tables. And a wide berry ground behind running text cannot pass contrast at the spark's own step.

## Decision
1. **The main action takes the berry.** One main action per screen — the action the screen exists for — is drawn in the berry: a step darker than the spark in the light theme, so white text passes AA, and the spark's lighter step with dark text in the dark theme.
2. **The ink keeps everything else it has.** Secondary actions, links (underlined in running text), checked and active controls, focus and structure stay in the ink. A destructive action stays red.
3. **Content and work surfaces stay neutral.** Cards, tables, lists, forms and the dashboard's screens are ink on paper; the status colours keep their meaning alone.
4. **A few brand surfaces carry the berry-to-plum scale,** from the berry to its darkest step: large areas whose purpose is the identity — such as the home page's opening, the sign-in's brand area, the footer — never behind data or a form's fields. Text on them passes AA.
5. **The dashboard is quieter than the public pages:** there, the berry marks the selected item and the main action only.
6. **ADR 0019's spark keeps its other roles** (what matters now: the selected tint, an edge, a mark), and its measured criteria stay the tests a berry must pass: contrast on its grounds, and its distance from the destructive red, with and without simulated colour blindness — now applied to the main action's steps too.

## Alternatives
- **Keep ADR 0019 as it is,** the berry never on an action. Rejected: the identity stays invisible where people first meet the product.
- **The berry as the main colour of the site,** grounds, headings, links and actions. Rejected: it competes with the status colours, tires a daily tool, and fails contrast as a ground for running text.
- **The berry on every primary-styled control,** links and checked controls included. Rejected: a berry link beside a berry button blurs which is the action, and checked controls are state, not action.
- **The spark's own step on the action,** with white text. Rejected: 4.11 : 1, below AA.

## Consequences
- Every screen's main action changes colour at once, in both themes; secondary actions and links do not.
- The design system gains a role for the main action of its own, apart from the ink's role for links and controls.
- Each screen is designed with one main action; a screen that seems to need two shows one as secondary.
- The brand surfaces are designed page by page, starting with the sign-in and the home page.
- The logo, the browser's icons and the e-mails are unchanged.

---

## Notes for the owner (not part of the committed text)
- **Point 4's examples** (the home's opening, the sign-in's brand area, the footer) are examples, not a commitment
  to build them in WI-B. WI-B changes the main action only; each brand surface is designed with you later (P3 for
  the sign-in pages; the home page in its own round).
- **WI-B after your approval:** a Claude Code worker plans (the role, which buttons become the main action screen by
  screen, the contrast tests), stops for your approval, then builds. It may run beside C2 if its plan shows no shared
  file.
