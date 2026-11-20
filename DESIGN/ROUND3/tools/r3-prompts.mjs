// r3-prompts — writes the six reviewers' prompts (ROUND3\PROMPT\R3-<PART>.md) from one template, the
// inventory and each part's own section. Usage: node r3-prompts.mjs <head sha> <PR number> "<frames taken, e.g. 2026-11-13 14:30–16:10 UTC>"
import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const R3 = resolve(HERE, '..');
const W = 'C:\\dev\\masaha\\workspace';
const D = W + '\\DESIGN';
const R = D + '\\ROUND3';
const APP = 'C:\\dev\\masaha\\app-dr';
const [HEAD, PR, TAKEN] = process.argv.slice(2);
const inv = JSON.parse(readFileSync(join(HERE, 'inventory.json'), 'utf8'));
mkdirSync(join(R3, 'PROMPT'), { recursive: true });

const PARTS = {
  PU: {
    name: 'the public site',
    skills: ['page-patterns', 'viewports', 'empty-states', 'loaders'],
    decisions: ['DECISIONS_PUBLIC.md'],
    features: ['directory.md', 'favorites.md', 'data-reports.md', 'platform-settings.md', 'occupancy.md', 'lookups.md'],
    decided: [`${W}\\TASKS\\DIRECTORY_FILTERS\\0_OWNER_DECISIONS.md`, `${W}\\TASKS\\DIRECTORY_PROD\\0_OWNER_DECISIONS.md`],
    focus: [
      'Home: the «open now» / «nearest» section, the areas, the owners\' card; nearest-to-me in its states (granted PU-03, refused PU-04) and the privacy line\'s truth (the location **is** sent, rounded, to sort — DECISIONS_PUBLIC\'s 2026-10-13 change).',
      'The directory: the filters as decided (DIRECTORY_FILTERS revision 2 and DIRECTORY_PROD — judge how they are built, never re-decide them), the sidebar from 1024 and the bottom sheet below (the P5 exception), the sort, the result count, pagination (REFACTOR_NOTES: a bar on a single page), the empty state, the cards (U12: the photo leads, **no price on the card except the chosen subscription\'s while sorting by it**, as decided), the map (U6, U7: pins as shapes and colours, the chosen space, placing a location by hand).',
      'A space\'s page: U8\'s order at every width, U9\'s prices, U4\'s freshness per group, U3\'s one name (the other name under the h1; a space with no Arabic name, PU-17), U10\'s report wording, the photo viewer, the live status (ADR 0008: a state, never a count; FULL in PU-14), the closure (PU-16), the long name (PU-18), the phone\'s contact bar.',
      'About (U11), the privacy policy, the 404 and the missing space.',
    ],
  },
  AU: {
    name: 'signing in and the account',
    skills: ['forms', 'errors', 'labels', 'verbs', 'defaults'],
    decisions: ['DECISIONS_ACCOUNT.md'],
    features: ['auth.md', 'users.md', 'favorites.md', 'data-reports.md'],
    decided: [],
    focus: [
      'The focus shell (sign in, register, forgot, reset, the forced change): the logo, the way back, the Google button and «أو» (the review\'s origin `localhost:5336` may not be registered with Google: a blank or erroring Google button is the environment — say so, never a defect), field errors, the password rules (AC-020), failures and the 429 (AU-04: the countdown and the held submit).',
      'C1–C8: the forgot/reset flow (C3 «استخدم بريدًا آخر», masked email), the forced change line as amended 2026-10-13 (AU-12), signing in that keeps the intent.',
      'The account area: «إعدادات حسابي» (C6), the password change (C2, C5), a Google-only account (AU-15), favourites (C7: a space that left, AU-17; empty AU-18), my reports (the reply\'s author; empty AU-20).',
    ],
  },
  OW: {
    name: 'the owner\'s dashboard',
    skills: ['forms', 'errors', 'empty-states', 'labels', 'verbs', 'loaders'],
    decisions: ['DECISIONS_OWNER.md'],
    features: ['overview.md', 'payments.md', 'finance.md', 'packages.md', 'spaces.md', 'announcements.md', 'data-reports.md', 'space-links.md', 'audit.md', 'space-settings.md', 'occupancy.md'],
    decided: [`${W}\\TASKS\\SPACE_PROFILE\\0_OWNER_DECISIONS.md`],
    focus: [
      'The overview as a work queue (O3; **no money on it**, the owner\'s rule).',
      'The payments ledger (K4: a voided payment struck through with who and why; filters; the void dialog under P9), finance (O-15/16; finding 223 is known: occupancy scrolls sideways on a phone — cite it).',
      'Packages & prices (O6, O8), the space profile (O1 and the SPACE_PROFILE decisions: view first, the sheets, discard and leave questions, photos as immediate actions O7, an open report\'s notice).',
      'Announcements (O9–O11; the extension dialog is not captured — judge it from the source), data reports (O12: the reporter anonymous), staff (OW-017–019, a held menu item with its reason), the audit log (O13), settings (O2, P10).',
      'P1 (one page header; the phone\'s «⋯»), P2 (the public-state control), P8 (feedback), P9 (confirm or undo), P10 (save stays enabled) — how each page applies them.',
    ],
  },
  DK: {
    name: 'the front desk and reception',
    skills: ['keyboard', 'errors', 'loaders', 'verbs', 'defaults'],
    decisions: ['DECISIONS_DESK.md'],
    features: ['desk.md', 'visits.md', 'customers.md', 'subscriptions.md', 'payments.md', 'occupancy.md', 'announcements.md'],
    decided: [],
    focus: [
      'The desk as the place used all day, on a phone and at a counter: K1\'s one search (people present first), K2\'s one money block, K3 (renewal with a debt), K5–K7, the check-in and check-out dialogs, the uncollected visits and the write-off (K6), the live status control (P2), the phone\'s bottom bar (P1: «تسجيل زيارة» is the one action it holds) and «⋯».',
      'Customers (K-list: DK-013, DK-014, DK-017), the customer file (statement, voids, correction, credit, unpaid visits), the subscription sheet (DK-008, K2), reception\'s «دفعاتي اليوم», reception\'s announcements.',
      'Keyboard first: a live keyboard path at the desk (search → check in → the dialog → its submit, then Escape and the focus\'s return) is expected — a still frame cannot show it.',
      'Reception\'s session ends after 15 minutes idle (contract §1); the owner\'s and reception\'s views differ (survey-space.md lists how).',
    ],
  },
  AD: {
    name: 'the admin\'s dashboard',
    skills: ['forms', 'labels', 'empty-states', 'errors', 'defaults'],
    decisions: ['DECISIONS_ADMIN.md'],
    features: ['overview.md', 'spaces.md', 'space-links.md', 'users.md', 'data-reports.md', 'lookups.md', 'audit.md', 'platform-settings.md'],
    decided: [],
    focus: [
      'A1–A8 and the amendments: the shared space editor (five groups and the gallery, «لم تُضف بعد», the A2 checklist, the sheets; a verified space read-only), hours (no «24 ساعة» switch), prices, contacts (the carrier derived), own amenities beside the common ones.',
      'Owners and users: A4 (one way to link), A5 (say what an action does to someone else before it is done; the one-time password dialog AD-21), A6, AD-021, a held role change with its reason (AD-23).',
      'Lists: A7 (cards until 1024 for spaces, users and reports), filters, the «stale or missing» chip, deleted spaces and restore (A3), data reports (A8, a verified space\'s report read only), lookups (never paged; arrows; the amenities\' icons), the audit log, platform settings (AD-029).',
    ],
  },
  SH: {
    name: 'the shared layer: the design system, the identity, the shells, and consistency across parts',
    skills: ['colour-palette', 'typography', 'spacing', 'surfaces', 'icon-buttons', 'motion', 'transitions', 'reduced-motion', 'keyboard'],
    decisions: [],
    features: [],
    decided: [],
    focus: [
      'The design system as the showcase draws it (SH-01…08, the layer\'s own preview pages): every component\'s look and states against foundation §11–§12, in both themes and directions.',
      'The shells: the site header and phone menu (SH-09/10), the account menus (SH-11, SH-14), the focus shell (the AU frames), the dashboard\'s sidebars, the 768 rail (SH-15), the phone drawers (SH-12/13), page headers, the skip link (SH-16).',
      'States across parts: loading (SH-17…20), failure (SH-21…23), 429 (SH-24/25), offline (SH-26), 403 (SH-27), 404 (SH-28 and PU-25), toasts (SH-29/30), and the empty states in the other parts.',
      '**The identity across the product** (ADR 0019, foundation §4–§5, §16): ink on every action; the spark only where ADR 0019 allows (never small text, never an action, never destructive); hover never the selected tint; links underlined in running text; the logo (its places, sizes, its name in both languages, never mirrored) and the favicon (`/favicon.svg`, `/favicon.ico`, `/apple-touch-icon.png` on 5336); any of Sea\'s old values still painted. Start from `pack\\LEADS-ALL.md` (every part\'s measured leads, grouped across parts).',
      'RTL / LTR, dark, the three widths, motion and reduced motion (live and in the source), and **the same job done the same way in every part**: filtering (the filter sheet, chips, selects), adding (where «add» sits), row menus, confirm-or-undo dialogs, empty states, page headers, pagination, toasts. For this, besides your own sheets, open at least the first-screen sheets at 390, 768 and 1440 of one base per screen of every other part (named in §4) and list them.',
    ],
  },
};
const AXES = [
  ['AX', 'accessibility — contrast, focus, names, order, targets, reduced motion (foundation §10)'],
  ['CP', 'content and Arabic copy — the glossary, Arabic that reads as Arabic, one name per thing, labels that say what happens'],
  ['DF', 'defects — what is broken: overflow, overlap, clipping, wrong state, console errors, a layout that breaks at a width'],
  ['EX', 'excess — what could go: a duplicate, a decoration, a word too many, a control nobody needs'],
  ['TR', 'truth to product, data and API — v1 and Not in v1, ADR 0008, the data model, the contract (every list paged, every action can fail and answer 429)'],
  ['UX', 'the way through — the flow, the primary action, feedback and recovery, the fewest steps, the phone and the counter'],
  ['VD', 'visual — alignment, spacing, hierarchy, type, colour roles, the design system used as designed'],
  ['ID', 'the identity — ink + berry (ADR 0019), the spark\'s rules, hover vs selected, links underlined, the logo and its rules (§16)'],
];

for (const [P, cfg] of Object.entries(PARTS)) {
  const bases = inv.filter((b) => b.part === P);
  const sheets = bases.reduce((n, b) => n + (b.widths || [390, 768, 1440]).length * 2, 0);
  const others = P === 'SH' ? Object.keys(PARTS).filter((x) => x !== 'SH').map((x) => {
    const firsts = []; const seen = new Set();
    for (const b of inv.filter((y) => y.part === x)) { if (!seen.has(b.screen)) { seen.add(b.screen); firsts.push(b.id); } }
    return `- ${x}: ${firsts.join(', ')}`;
  }) : [];
  const t = [];
  t.push(`# Round 3 design review — part ${P}: ${cfg.name}`, '');
  t.push('> **This is not a Work Item.** Use no project skill (`start-work-item`, `write-plan`, `open-pr`, `final-report`), no plan mode, no branch, commit, push, pull request, issue or comment, and ignore a `CLAUDE.md` or `AGENTS.md` that asks for them. **You never edit the repository**: `' + APP + '` and every other `C:\\dev\\masaha\\app*` folder are read-only to you. You write only the files this prompt names, all under `' + R + '`.', '');
  t.push('## 1. Your task', '');
  t.push(`You are the **${P}** reviewer of Masaha's design review round 3: one of six reviewers, one per part (PU public · AU sign-in and account · OW owner · DK desk and reception · AD admin · SH shared), each applying every axis to its part. Masaha (مساحة) is a bilingual Arabic RTL / English platform for coworking spaces in Gaza: a public directory with live status, an account area, and one dashboard for owners, their reception staff and the platform admin. Its users are students, freelancers, space owners and reception staff, often on a phone, on a weak connection, in Arabic first.`, '');
  t.push('**The goal is not only to find defects: it is to arrive at the best design** for every page, pattern and component of your part. **Nothing is fixed in this round**: you write one report; a lead reviewer checks it and merges the six; then the owner decides. **The owner\'s bar:** production-ready, no errors; he reacts strongly to sloppy UI and to an unexplained disabled control. **Never revive a decision the owner cancelled** (search the decisions files first): for example, amenities are no filter of the directory; a directory card shows no price except the chosen subscription\'s while sorting by it; no «24 ساعة» switch; no money on the owner\'s overview; no «sign out of all devices».', '');
  t.push('## 2. The subject', '');
  t.push(`- **The real web app** at the identity PR's head \`${HEAD}\` (PR #${PR}, \`feat/ink-berry-identity\`: the ink + berry colours and the logo), with real data and every role. It runs from its own worktree \`${APP}\` on **http://localhost:5336** (web) and **http://localhost:3336** (API), over the database \`masaha_dr_dev\` (a copy of the demo data). Its source at that head is \`${APP}\` — read it freely, never change it.`);
  t.push('- **The prototype** (`docs/design/prototype/`, `docs/design/README.md`) is the reference for the intended design, not the subject. Report a difference between the app and the prototype only when the app is the worse of the two (or the prototype is — say which).');
  t.push(`- **When:** the frames were taken ${TAKEN}. Gaza is UTC+2, and 2026-11-13 is a Friday: many spaces close early on Fridays, Pal Hub (space 26) from 20:00 Gaza; open / closed / live states depend on the hour a frame was taken — read the frame's own state before calling one wrong.`);
  t.push(`- **How each state was reached** is in \`${R}\\INVENTORY.md\` (§2 and the base's row): by address, by scripted clicks, or by the capture tool answering a request at the network layer — held (loading), a 500 or a 429 simulated (the contract's envelope, \`Retry-After: 60\`), aborted (offline), mocked (an empty list), or a real answer patched (one field). Those are faithful to what the app draws for that answer. The **named states** written to \`masaha_dr_dev\` (people present, payments today, a long name) are listed there (§3); so is what was not captured (§4).`, '');
  t.push('## 3. Read first', '');
  t.push(`- In \`${APP}\` (the head): \`CLAUDE.md\`; \`docs/frontend/design-system/foundation.md\` **whole**; \`docs/frontend/architecture.md\`; \`docs/project/overview.md\` (v1 and *Not in v1*); \`docs/project/glossary.md\`; \`docs/api/api-contract.md\` (§1–§4, and the endpoints your screens call: every list is paged, every action can fail and answer 429); \`docs/architecture/decisions/0019-ink-and-spark-brand.md\` and \`0008-live-status-not-counts.md\`; \`docs/design/README.md\`${cfg.features.length ? '; your capabilities: ' + cfg.features.map((f) => '`docs/features/' + f + '`').join(', ') : '; `docs/features/README.md` if present, and the capability of any screen you judge'}.`);
  t.push(`- The lens: \`${D}\\DECISIONS\\REVIEW_LENS.md\` (§3 what to look for, §4 how to propose, §5 the report), **adapted to the app**: an issue's *level* is page | pattern | component | design system | rule; *where* is the app's URL, the role, the state and the frame's path in the pack.`);
  t.push(`- Settled decisions — **never reported again**, only how a page applies them, or a "rule in doubt" with why: \`${D}\\DECISIONS\\DECISIONS_SHARED.md\`${cfg.decisions.map((d) => ', `' + D + '\\DECISIONS\\' + d + '`').join('')}${P === 'SH' ? ' and every other `DECISIONS_*.md` in that folder (you judge consistency across parts)' : ''}.`);
  t.push(`- The identity's rules and values: \`${W}\\TASKS\\IDENTITY\\0_OWNER_DECISIONS.md\` and \`${W}\\TASKS\\IDENTITY\\2_PLAN_PROD.md\` §4–§6 and §9 (D1–D5 were accepted).`);
  if (cfg.decided.length) t.push(`- Decided screens — judge how they are built, do not re-decide them: ${cfg.decided.map((d) => '`' + d + '`').join(', ')}.`);
  t.push(`- Known items — cite them by their number, never as new: \`${W}\\REFACTOR_NOTES.md\` and the repository's findings index \`${APP}\\docs\\architecture\\findings\\README.md\` (search it for your topic before you write an issue).`);
  t.push(`- The data you will see: \`${R}\\tools\\survey-${P === 'PU' || P === 'AU' ? 'site' : P === 'AD' || P === 'SH' ? 'admin' : 'space'}.md\` (a read-only survey of the screens, their states and the demo data)${P === 'SH' ? `, and \`survey-site.md\`, \`survey-space.md\` beside it` : ''}.`, '');
  t.push('## 4. Your screens and your evidence', '');
  t.push(`- **Frames:** \`${R}\\pack\\${P}\\frames\\\` — each \`<ID>-<width>-<lang>-<theme>\`: \`.png\` (the first screen), \`.full.png\` (the whole page, at most 9000 px) and \`.json\` (measured facts).`);
  t.push(`- **Contact sheets:** \`${R}\\pack\\${P}\\sheets\\\` — per base and width, \`<ID>-<width>.png\` (its four first screens side by side: ar light, ar dark, en light, en dark) and \`<ID>-<width>-full.png\` (its four whole pages). **${sheets} sheets** for your ${bases.length} bases.`);
  t.push(`- **Measured leads:** \`${R}\\pack\\${P}\\summary.md\` — each fact once per base, with the frames it was measured on${P === 'SH' ? `; and \`${R}\\pack\\LEADS-ALL.md\`, the leads of every part grouped across parts` : ''}. A lead is not an issue until you have looked at the frame.`);
  t.push('- **The facts JSON** (per frame; `firstScreen` read at the viewport, `wholePage` read with the viewport stretched to the page): `consoleErrors` and `apiErrors`; `horizontalPageOverflow`; `contrast.fails` (each visible text against the colour painted under it: `fg`, `ground`, `ratio`, `need` 4.5 or 3 for large text; text over a photo or the map is skipped and counted; disabled text is exempt); `targets.small` (an interactive element under 40 px, or 44 px on a coarse pointer — 390 and 768 are emulated as touch, 1440 as a mouse; `hit` counts a pseudo-element hit area; links inside running text are excluded); `seaValues` (any of the old *Sea* identity\'s 22 ramp values still painted); `sparkAsText`, `sparkOnAction`, `sparkMarks` (the berry ramp\'s values as text, on an action, or as a mark); `focusAfterTab` (the first Tab stops: the element, its outline, the outline\'s ratio to its ground, whether it is in view); `clipped`, `offscreen`, `headings`, `landmarks`, `dialogs`, `toasts`, `skeletons`, `text`.');
  t.push(`- **Index:** \`${R}\\pack\\INDEX.md\` (every base of every part, its frames and sheets).`, '');
  t.push(`Your bases (${bases.length}):`, '', '| ID | Screen | State | Role | URL | Widths |', '|---|---|---|---|---|---|');
  for (const b of bases) t.push(`| ${b.id} | ${b.screen} | ${b.state} | ${b.role} | \`${typeof b.url === 'string' ? b.url : b.url.ar}\` | ${(b.widths || [390, 768, 1440]).join(', ')} |`);
  t.push('');
  if (others.length) t.push('For consistency across parts, also open the first-screen sheets (`-390`, `-768`, `-1440`) of these bases — one per screen of each other part — in `pack\\<PART>\\sheets\\`:', '', ...others, '');
  t.push('## 5. What to look at especially', '', ...cfg.focus.map((f) => '- ' + f), '');
  t.push('## 6. The axes — apply all eight', '', ...AXES.map(([k, v]) => `- **${k}** ${v}`), '', 'Tag every issue with its axis or axes.', '');
  t.push('## 7. Skills — as lenses', '');
  t.push(`Load with the Skill tool, first: \`vectorlab-ux-skills:ux-audit\`, \`vectorlab-ux-skills:anti-slop\`, \`frontend-design:frontend-design\` (polish and character, never a restyle against the design system), and for your part ${cfg.skills.map((s) => '`vectorlab-ux-skills:' + s + '`').join(', ')}. **Never \`brand-guidelines\`** (it is Anthropic's own brand; Masaha's is \`foundation.md\`, ADR 0019 and §16). The owner's word sets aside workflow §10's "review sessions use no plugin skill" for this round. A skill's advice that contradicts \`foundation.md\` or a settled decision is a **rule in doubt**, never a defect (for example, P9's «رجوع» on every dismiss button, or Arabic action labels written as a verbal noun such as «تسجيل الدخول»). List under **Skills loaded** which loaded; one that does not: say so and go on with the lens alone.`, '');
  t.push('## 8. The method — gates the lead checks', '');
  t.push(`1. **Open every contact sheet of your part** — all ${sheets}, no sampling — base by base. After each base, append to your notes file \`${R}\\REPORT\\_work\\R3-${P}-notes.md\` what you saw and the sheets you opened, so nothing is lost if your context is compacted. When a sheet shows something, open that frame's own \`.png\` / \`.full.png\` at full size and read its \`.json\`.`);
  t.push('2. **Every issue states an observed fact with its measured value** — a ratio, a size in px, a count, the exact words on the screen, the console line, the element. Never "ensure", "must", "should be verified", "unverified", "no browser", "might".');
  t.push(`3. **Every issue has its own cropped capture**, \`${R}\\shots\\issues\\R3-${P}-NNN.png\`, no two issues sharing one: cut it from a pack frame with \`node ${R}\\tools\\r3-crop.mjs <frame.png> <out.png> <x> <y> <w> <h> [--mark x,y,w,h] [--scale 2]\` (pixels of the frame; a \`.full.png\`'s y is the page's; \`--mark\` draws a red box on the defect), or capture it live (8.5). Open each crop once to check it shows the defect.`);
  t.push(`4. **At least one issue re-checked in the app's source**: name the file and line in \`${APP}\` that causes it.`);
  t.push(`5. **Live checks** only where a still frame cannot answer (a keyboard path, focus order and its return, a discard question, a 429's countdown, hover): only on 5336 / 3336, **through the grant script, one Chrome at a time**, with the pack tool and an inventory of your own — write \`${R}\\live\\${P}\\inv.json\` (the same shape as \`${R}\\tools\\inventory.json\`; a step \`{ "shot": "name" }\` saves a screenshot and the focused element mid-path; \`"tabStops": 15\` records 15 Tab stops; \`"widths"\`, \`"langs"\`, \`"themes"\` narrow it), then run from \`${APP}\`: \`node ${W}\\TASKS\\IDENTITY\\scripts\\heavy.mjs dr node ${R}\\tools\\r3-pack.mjs ${R}\\live\\${P}\\inv.json --out ${R}\\live --widths 390 --langs ar --themes light\` (it may wait for memory; that is expected). Never start, stop or restart the servers. **No write to the database** — a live check that would write (a check-in, a save, a sign-out) is not done; if one is truly needed, it is named in your report.`);
  t.push('6. Settled decisions are not reported again; a known item is cited by its number; a skill\'s contrary advice is a rule in doubt.', '');
  t.push('## 9. The report', '');
  t.push(`Write \`${R}\\REPORT\\R3-${P}_REPORT.md\`, in English, concise, in this order:`, '');
  t.push(`1. **Head and scope:** the head \`${HEAD}\`, your ${bases.length} bases, when the frames were taken.`);
  t.push('2. **Summary:** the five most important points, one line each.');
  t.push('3. **Patterns** (level: pattern) — the cross-page proposals first; each names every page it changes.');
  t.push(`4. **Issues**, most important first, IDs \`R3-${P}-001\`…, one block each: **title**; **axis** (AX | CP | DF | EX | TR | UX | VD | ID, one or more); **type** (defect | improvement); **level** (page | pattern | component | design system | rule); **impact** (high | medium | low, for the user); **where** (the URL, the role, the state, and the frame paths: \`pack\\${P}\\frames\\<frame>.png\`); **evidence** (\`shots\\issues\\R3-${P}-NNN.png\`); **observed** (the fact and its measured value); **what is wrong / what could be better**; **proposal** (built from the design system's own components and tokens — foundation §12; a new component says so and why); **why it is better** for the user; **cost** (S | M | L); **rule** (the document and section it applies or puts in doubt).`);
  t.push('5. **Rules in doubt:** each rule of the documents (or a settled decision) you think makes the design worse, with why.');
  t.push('6. **Not reviewed:** what was out of reach, and why.');
  t.push('7. **Skills loaded** · **Sheets opened** (every sheet file name) · **Source re-checks** (file and line) · **Live checks** (what, the command, what it showed) · **Database writes** (expected: none).', '');
  t.push('Prefer one strong proposal to three options; give options only where the choice is the owner\'s. Fewer true issues beat many: an issue a reader cannot see in its capture is not an issue.', '');
  t.push('## 10. Limits', '');
  t.push('Never edit the repository; no commit, branch, push, PR, issue or comment; no migration, no dependency, never `db:seed`; only `masaha_dr_dev`, and no write to it; never print a secret (the passwords live in `' + APP + '\\apps\\api\\.env` — the pack tool reads them itself); ports 5336 / 3336 only; never stop on the volume of work — report it. When your report is written, reply with only: its path, the number of issues, and the number of sheets opened.');
  writeFileSync(join(R3, 'PROMPT', `R3-${P}.md`), t.join('\n') + '\n');
  console.log(`R3-${P}.md: ${bases.length} bases, ${sheets} sheets`);
}
