# Masaha — Design System Foundation & Claude Design Brief

> **Status:** Draft v0.1 — structure decided, visual values open (to be set in Claude Design).
> **Owner:** Basel Ghoneim
> **Last Updated:** 2026-09-26
> **Audience:** Claude Design (to design every screen), Claude Code and the developer (to build the layer).

This document defines **how** Masaha's Design System is structured and **what** it must cover. It deliberately does **not** fix colours, fonts or radii. Those are chosen in Claude Design (Step 1 of §14), then written back here as the values of the tokens named below.

---

## 1. Product context

**Masaha (مساحة)** is a bilingual (Arabic / English) web platform for coworking spaces in the Gaza Strip. It has three areas:

| Area | Who | Purpose |
|---|---|---|
| **Public site** | everyone | Directory of coworking spaces (list + map), space details, live available seats |
| **My account** | User, Owner | Profile, favourites, reports the user submitted |
| **Dashboard** | Owner, Admin | One role-based dashboard: Owner manages their own space(s); Admin manages the platform |

**Roles:** `USER` (freelancer or student looking for a space), `OWNER` (space owner; also does the receptionist's work), `ADMIN` (platform administrator).

**Context that shapes the design:**
- Users are freelancers and students in Gaza. Internet is weak and intermittent, so pages must stay light.
- Arabic is the primary language, and RTL is a first-class direction, not an adaptation.
- Owners manage a daily operation: check-ins, members, announcements. Speed of repeated actions matters more than decoration.
- Tone: calm, trustworthy, practical. No playful or decorative styling.

---

## 2. Principles

1. **One layer, one place.** Every visual decision lives in `shared/design-system/`. Pages and features compose it and never restyle it.
2. **Semantic, never raw.** Consumers bind semantic roles (`primary`, `muted-foreground`), never palette values (`blue-500`) or arbitrary values (`text-[13px]`).
3. **Themes are a resolution layer.** Light and dark are two complete resolutions of the same semantic keys. Components never know which theme is active.
4. **RTL is first-class.** Every component works identically in both directions, using logical properties only.
5. **Components hold no words.** Every visible or assistive string arrives as a prop from the copy catalogue.
6. **Responsive everywhere.** Public site and dashboard alike work on phone, tablet and desktop.
7. **Accessible by default.** AA contrast in both themes, visible focus, keyboard reachable, adequate hit targets.
8. **Admission test.** A component belongs to the layer only if its meaning survives outside Masaha's domain. `Button`, `Badge` and `Table` belong. `SpaceCard` and `OccupancyMeter` belong to features, built *from* the layer.

---

## 3. Architecture

```
src/shared/design-system/
  tokens/
    primitives.css    raw scales (palette, radius, shadow) — the only place raw values exist
    semantic.css      semantic roles, per theme ([data-theme="light"] / [data-theme="dark"])
    typography.css    font stacks per script + composite text styles
    tailwind.css      @theme mapping: exposes semantic roles as Tailwind utilities
  components/
    <ComponentName>/  one folder per component (shadcn-sourced or hand-built), own index.ts
  icons/              single wrapper over the icon library + mirroring rule
  lib/cn.ts           class-merge helper (lives inside the layer — the layer imports nothing from outside)
  index.ts            the only public surface
```

**Rules:**
- **Public surface:** consumers import from `@shared/design-system` only, never from inside a component folder.
- **Closure:** the layer imports nothing from outside itself (no features, pages, app, or other `shared/` modules).
- **shadcn/ui** is configured (`components.json` aliases) to copy components into `components/`. Once copied, a component is ours and follows this contract (§11).
- **Radix primitives, the icon library and variant utilities** (`class-variance-authority`) are imported **only** inside the layer.
- **No CSS files outside the layer.** Pages and features use Tailwind for layout only (grid, flex, gap, spacing, sizing).

**Enforcement:** lint rules forbid (a) imports into the layer's internals, (b) importing Radix, the icon library or `cva` outside the layer, and (c) raw palette or arbitrary-value classes outside the layer. A test checks theme key parity (§6).

---

## 4. Token tiers

| Tier | What it holds | Who binds it |
|---|---|---|
| **Primitive** | Raw scales with no meaning: palette ramps (`brand-50…950`, `neutral-50…950`, `green-*`, `amber-*`, `red-*`, `blue-*`), radius scale, shadow scale | Only `semantic.css` |
| **Semantic** | Roles with meaning, resolved per theme | Components, and pages/features for colour needs |
| **Component** | Optional, derived from semantic; only when a component needs a value no role covers | That component only |

**Binding rule:** use the semantic role where one exists; otherwise the primitive scale inside the layer; never a literal.

**Coincidence is not identity:** two roles that happen to share a value in one theme stay separate if they mean different things.

---

## 5. Semantic roles

Names follow shadcn/ui's convention so copied components work unchanged, plus Masaha's additions. Every role with a surface has a matching `-foreground`.

### Surfaces and text
| Role | Purpose |
|---|---|
| `background` / `foreground` | Page ground and default text |
| `card` / `card-foreground` | Raised surfaces: cards, panels, table containers |
| `popover` / `popover-foreground` | Floating surfaces: menus, popovers, dropdowns |
| `muted` / `muted-foreground` | Subtle fills; secondary text (captions, meta, placeholders) |
| `border` | Default borders and dividers |
| `input` | Form control borders |
| `ring` | Focus indicator (one focus style for the whole system) |

### Actions
| Role | Purpose |
|---|---|
| `primary` / `primary-foreground` | Main action, links, selected state, the brand accent |
| `secondary` / `secondary-foreground` | Secondary actions |
| `accent` / `accent-foreground` | Hover and highlighted rows or items |
| `destructive` / `destructive-foreground` | Delete, deactivate, errors |

### Status (Masaha additions)
| Role | Purpose | Domain uses (decided by features, not the layer) |
|---|---|---|
| `success` / `success-foreground` | Positive state | Seats available, active membership, verified |
| `warning` / `warning-foreground` | Attention | Space filling up, membership ending within 7 days, possibly outdated data |
| `info` / `info-foreground` | Neutral notice | Announcements, tips |
| `destructive` (above) | Negative state | Space full, expired membership, errors |

Each status also needs a **subtle** surface for badges and alerts (`success-subtle`, `warning-subtle`, `info-subtle`, `destructive-subtle`) with text that meets AA on it.

### Dashboard shell
`sidebar`, `sidebar-foreground`, `sidebar-primary`, `sidebar-primary-foreground`, `sidebar-accent`, `sidebar-accent-foreground`, `sidebar-border`, `sidebar-ring` — as in shadcn's Sidebar component.

### Data visualisation
`chart-1` … `chart-5` — for the occupancy reports (occupancy by hour and by day).

### Other scales
| Family | Tier | Notes |
|---|---|---|
| Radius | Primitive scale + one semantic `radius` base | shadcn derives `sm`, `md`, `lg`, `xl` from `--radius` |
| Shadow | Primitive scale | 3 levels: raised, floating, overlay |
| Spacing | Tailwind's 4px scale | Layout spacing binds the scale; control padding is owned by components |
| Z-index | Named layers | `dropdown`, `sticky`, `overlay`, `modal`, `toast` |
| Motion | 2 durations + 1 easing | Respect `prefers-reduced-motion` |

---

## 6. Theming

- **Themes:** `light` and `dark`, each a complete resolution of every semantic key (**key parity**, checked by a test).
- **Mechanism:** `data-theme` on `<html>`. Tailwind's `dark:` variant is redefined to read `[data-theme="dark"]` instead of shadcn's `.dark` class.
- **Pre-paint script:** an inline script in `index.html` sets `data-theme`, `lang` and `dir` before first paint (no flash).
- **Policy (owned by the app, not the layer):** follow the system preference until the user chooses. The explicit choice is stored and wins.
- **Both themes are designed, not generated.** Claude Design delivers every key screen in both.

---

## 7. Typography

- **Script axis:** font stacks resolve per language via `:lang(ar)` / `:lang(en)`.
- **Candidate font (to confirm in Claude Design):** *IBM Plex Sans Arabic*, which covers Arabic and Latin in one family, keeping both languages visually consistent. Alternatives to explore: *Noto Sans Arabic* + *Inter*; *Tajawal* + *Inter*.
- **Composite text styles** (size + weight + line height as one unit), not a raw size ramp:

| Style | Use |
|---|---|
| `display` | Home hero only |
| `heading-1` | Page titles |
| `heading-2` | Section titles |
| `heading-3` | Card and panel titles |
| `body` | Default text |
| `body-sm` | Dense tables, secondary content |
| `label` | Form labels, buttons, tabs |
| `caption` | Meta text, timestamps, helper text |

- **Arabic line height is taller** than Latin (around 1.7–1.8 for body, 1.5–1.6 for headings). The script axis resolves it, not each component.
- **Digits:** Western (0–9) in both languages.

---

## 8. Direction (RTL / LTR)

- **Logical properties only:** `ms-/me-/ps-/pe-/start-/end-/text-start/text-end/border-s/border-e/rounded-s/rounded-e`. Physical ones (`ml-`, `left-`, `text-left`) are forbidden.
- **Direction follows language:** `ar` → `rtl`, `en` → `ltr`. It is never chosen separately.
- **Radix `DirectionProvider`** wraps the app so Radix-based components (menus, tabs, sliders) respect direction.
- **Icons declare mirroring:** directional icons (arrows, chevrons, "back") mirror in RTL; non-directional ones (search, calendar, check) never do. The mirroring rule lives in the `icons/` wrapper, not in each component.
- **Always-LTR values:** phone numbers, emails, prices, times and numeric IDs render with `dir="ltr"` inside RTL text. User-written text uses `dir="auto"`.
- **Mixed content:** a value inserted into a sentence is isolated (`<bdi>` or Unicode isolates) so it never reorders the sentence.

---

## 9. Responsive layout

| Size | Width | Behaviour |
|---|---|---|
| Phone | 360–767px | Single column. Dashboard sidebar becomes a drawer (`Sheet`). Tables become stacked cards. Directory shows list **or** map with a toggle. Filters open in a bottom sheet. |
| Tablet | 768–1023px | Two columns where useful. Sidebar collapses to icons. |
| Desktop | ≥1024px | Full layout: visible sidebar, full tables, directory list and map side by side. |

Tailwind breakpoints: `md` = 768, `lg` = 1024 (defaults).

**Shells:**
- **Public shell:** top header (logo, directory, language switch, theme toggle, sign-in / account menu), content, footer.
- **Dashboard shell:** sidebar (items built from the role), top bar (space switcher for owners with more than one space, language, theme, account menu), content.

---

## 10. Accessibility baseline

- WCAG AA contrast for text and UI in **both** themes, including status-subtle surfaces.
- One visible focus ring (`ring`) on every interactive element.
- Minimum hit target: 44×44px on touch.
- Every control has a programmatic label; errors are linked with `aria-describedby`.
- Full keyboard use in dashboards (tables, dialogs, menus).
- `prefers-reduced-motion` respected.

---

## 11. Component contract (applies to every component, including copied shadcn ones)

When a shadcn component is added, it is adapted before it is used:

1. **No built-in words.** Hardcoded strings ("Close", "Previous", "Next", "More", `sr-only` text) become props, supplied from the catalogue.
2. **Logical properties.** Convert any physical class to its logical form (§8).
3. **Icons through the wrapper**, with the mirroring flag.
4. **Semantic roles only.** No palette or arbitrary values.
5. **Variants via `cva`**, typed. Props extend the native element's props.
6. **Accessibility** as in §10, using Radix behaviour where available.
7. **Own `index.ts`**, exported from the layer's root `index.ts`.

---

## 12. Component inventory

| Component | Source | Notes / variants |
|---|---|---|
| Button | shadcn | primary, secondary, outline, ghost, destructive, link · sizes sm/md/lg/icon · loading state |
| Input, Textarea | shadcn | with error state; `dir` prop for LTR values |
| Field | hand-built | Label + control + helper + error, wiring ids and `aria-describedby` |
| Select / Combobox | shadcn | Area filter, amenity filter (multi-select) |
| Checkbox, RadioGroup, Switch | shadcn | |
| Badge | shadcn | neutral, primary, success, warning, info, destructive (subtle variants) |
| Card | shadcn | |
| Table + DataTable | shadcn | Sorting, empty state, loading rows; **stacked-card mode on phones** |
| Pagination | shadcn | Words as props |
| Dialog, AlertDialog | shadcn | Confirmations (check-out, deactivate member, hide space) |
| Sheet | shadcn | Mobile navigation, filter panel |
| DropdownMenu | shadcn | Row actions, account menu |
| Tabs | shadcn | |
| Tooltip | shadcn | |
| Toast | shadcn (Sonner) | Success and error feedback |
| Alert | shadcn | info, warning, destructive |
| Skeleton | shadcn | Loading states |
| Avatar | shadcn | Initials fallback |
| Separator | shadcn | |
| Calendar / DatePicker | shadcn | Membership start and end dates |
| Sidebar | shadcn | Dashboard shell |
| Breadcrumb | shadcn | Dashboard sub-pages |
| EmptyState | hand-built | Icon + title + text + action |
| StatCard | hand-built | Dashboard overview numbers |
| Spinner | hand-built | |

**Not in the layer (built by features from it):** SpaceCard, SpaceMap and markers, OccupancyIndicator, MemberRow, AnnouncementBanner, VerifiedBadge (a Badge usage).
**Not in the layer (app-level):** theme and language *policy*. The toggles' visual controls are ordinary layer components.

---

## 13. Screens to design (27)

Every screen: phone and desktop, light and dark. Key screens also in LTR (English). States: default, loading (skeleton), empty, error.

### Public site (8)
1. **Home** — hero with search, quick area filters, featured or nearby spaces
2. **Directory** — list + map; filters: area, price range, amenities, verified only, available now; sort
3. **Space details** — photos, prices (display only), amenities, hours, contact, announcements, live available seats (verified spaces), "last updated" notes, "Are you the owner? Contact us" (unverified), report wrong info
4. **About / Contact** — contact email and WhatsApp
5. **Sign in**
6. **Register**
7. **Forgot / reset password**
8. **404**

### My account (3)
9. **Profile & settings** — name, password, language, theme
10. **Favourites**
11. **My reports** — submitted reports and their status

### Owner dashboard (8)
12. **Overview** — present now / capacity, memberships ending this week, active announcements, new reports
13. **Space profile** — bilingual fields, map location, hours, capacity, amenities, prices, photos, contact
14. **Members** — list, search, add / edit / deactivate; status: active, ending soon, expired
15. **Attendance** — present now; check in a member or a daily visitor; check out; history with date filter
16. **Announcements** — create with type and duration
17. **Reports** — occupancy by hour and by day, peak times, average stay (charts)
18. **Data reports** — users' reports about the space's info
19. **Settings** — auto check-out rule, account

### Admin dashboard (8)
20. **Overview** — spaces verified / unverified, open reports, new users, data completeness
21. **Spaces** — all spaces, filters, add / edit / hide, link owner
22. **Space owners** — create an Owner account or upgrade a user; link to one or more spaces
23. **Data reports** — all reports and their status
24. **Users** — search, suspend, change role
25. **Lookups** — areas and amenities, in Arabic and English
26. **Audit log**
27. **Settings** — contact email and WhatsApp, default auto check-out, data-staleness threshold

---

## 14. Workflow with Claude Design

1. **Visual direction (Claude Design).** Use this document as the brief. Explore 2–3 directions on three anchor screens: *Home*, *Space details*, *Owner overview*, each in light and dark, RTL. Choose one direction. **Output:** the palette ramps, semantic role values for both themes, font choice, radius and shadow.
2. **Lock the tokens.** Write the chosen values into §4–§7 of this document.
3. **Build the layer in code (Claude Code).** Tokens, themes, pre-paint script, the shadcn components from §12 adapted per §11. Push to GitHub.
4. **Sync into Claude Design.** Import the repository's design system (`/design-sync` from Claude Code, or a GitHub import) so every screen is designed with the real components.
5. **Design the 27 screens** (§13) in Claude Design.
6. **Hand off** each area to Claude Code with Claude Design's handoff bundle, and implement.

Steps 3–4 make the design and the code share one design system, so what is designed is what gets built.

---

## 15. Open decisions (settled in Step 1)

| # | Decision | Owner |
|---|---|---|
| 1 | Brand colour and full palette | Claude Design exploration + Basel |
| 2 | Font family (confirm IBM Plex Sans Arabic, or an alternative) | Claude Design exploration + Basel |
| 3 | Radius style (sharp / soft / round) and density (compact / comfortable) | Claude Design exploration + Basel |
| 4 | Icon library (default: Lucide, shadcn's default) | Basel |
| 5 | Logo / wordmark for «مساحة» / Masaha | Claude Design exploration + Basel |
