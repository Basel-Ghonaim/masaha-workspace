# Review — PR #76 (design batch 5: the owner's management — prototype conformance)

**Head:** `5a2267633ca434b5ab32c26d58f15e1f0e95a478` (matches `gh pr view 76 --json headRefOid` and folder `HEAD`)

---

## Findings (most severe first)

### should-fix: `admin.jsx:27` — conditional-hook crash pattern identical to fixed `OwnerShell`
**Where:** `docs/design/prototype/masaha/admin.jsx:27` — `const rail = useIsTablet() && !useIsDesktop();`  
**What is wrong:** The same short-circuit hook pattern that caused a Rules-of-Hooks crash under width-cycling in `OwnerShell` (fixed in commit 1 by calling both hooks unconditionally) exists in `AdminShell` on `main`. The pass harness's width changes trigger React hook warnings on admin pages.  
**Fix:** In a future admin batch, change to unconditional hooks:
```js
const tablet = useIsTablet();
const desktop = useIsDesktop();
const rail = tablet && !desktop;
```
**Note:** This is a pre-existing defect on `main`, not introduced by this PR. `admin.jsx` is explicitly never-edited (AC19). Recorded as a finding for the next admin item.

---

### nit: `Announcements.html` — `ExtendDialog` stays open after successful extension
**Where:** `docs/design/prototype/Announcements.html:49–79` (`ExtendDialog` component)  
**What is wrong:** The `onDone` callback updates the list but does not call `onClose()`, so the `AlertDialog` remains open after the destructive action succeeds. The success toast fires and the card behind updates, but the dialog must be dismissed manually.  
**Fix:** Add `onClose()` at the end of `go()` in `ExtendDialog`, or have `onDone` return a promise that the caller uses to close.  
**Note:** Built verbatim from the plan (§3.7), which did not specify closing on success. Flagged in the fixer's report.

---

### nit: `check-classes.mjs` — three dead classes remain in KNOWN list though no longer used
**Where:** `docs/design/scripts/check-classes.mjs` (KNOWN array)  
**What is wrong:** The classes `hover:opacity-90` (was in Owner overview), `md:max-w-32` (was in Announcements), `md:w-72` (was in Finance) are reported as "gone" and the script suggests dropping them from KNOWN. They are pre-existing dead uses, not new.  
**Fix:** Remove those three entries from the KNOWN array in `check-classes.mjs` so the script's advisory output is clean.

---

## Checked and fine

- **AC1 (DI-10):** Phone top bar holds only menu, truncated title, P1's «⋯», P2's state control; account heads drawer with avatar/name·role/email, menu without theme/language. Verified in `owner.jsx:203–222`, `OwnerShell:290–291`, `323–327`. `?drawer=open` opens drawer for board.
- **AC2 (O5):** Arabic plurals via `Intl.PluralRules('ar')`, `countText`, `Counted` (`owner.jsx:341–350, 351–367`). No «1 أيام», «2 أيام», «1 زيارات», «( 2 )». Announcement tab counts are `Badge`s (`Announcements.html:200–202`).
- **AC3 (O3 amended):** `Owner overview.html` shows no ₪/money anywhere (verified by grep). Queue «يحتاج انتباهك» with counts/links: stale/missing groups → `Packages.html#prices`, new reports, uncollected visits → `Desk.html`, customers who owe → `Finance.html?tab=debts`, started closure without extension → `Announcements.html?tab=…&extend=…`, capacity not set → `Owner settings.html#attendance`. `?demo=clear` shows «كل شيء على ما يرام». No bottom bar, no desk shortcut in bar.
- **AC4 (O1 editor boundary):** `profile-a.jsx` untouched. `profile-b.jsx` only: three default-preserving props on `PricesSection` (`title`, `description`, `hoursHref`) and deletion of `CapacitySection`. `Admin space edit.html?id=golden|focus|new` identical to `main` (git diff empty).
- **AC5 (O2+OW-021):** `Owner settings.html#attendance` card «الحضور والحالة مباشرة» with capacity (optional, >0), auto check-out at closing, auto check-out after N hours (1–23). Rounding: «تقريب لأعلى بعد [15] دقيقة» with live example; student prices on. Page `max-w-3xl`. DI-38 folded: per-card `actionKey` (`save-attendance`, `save-pricing`, `save-message`).
- **AC6 (O6,O8):** `Packages.html` two h2 sections: «الأسعار المعلنة» (AD-008 table, dated «قبل 34 يومًا», «قديمة», «حفظ», «المعلومات ما زالت صحيحة») and «الباقات الخاصة» (rows: name, terms, price, «متاحة في المكتب» switch, «تعديل»; paused row muted). `#prices` lands on table. All owner «الأسعار» links → `Packages.html#prices`.
- **AC7 (O8+price>0):** Package sheet: name (required, unique), validity (required, >0), limits on demand (four-chip `ToggleGroup`, days/week 1–7, totalDays/totalHours >0), one billing choice (fixed/hour/day) with labelled amount, **amount >0 validated** («أدخل مبلغًا أكبر من صفر»), audience (all/students), shifts from space (`?demo=noshifts` shows reason + link).
- **AC8 (O9,OW-014):** Announcement sheet: Arabic text required, English optional, type as `RadioGroup` with hints, no title, no author. Type badges `neutral`, `warning` for outage/closure (`Announcements.html:31–37`).
- **AC9 (O10):** Active card: «إنهاء الآن» (at once, toast with «تراجع»). Scheduled card: «حذف» (`AlertDialog`, destructive). Sheet: «يبدأ: الآن · في موعد», «ينتهي: في موعد · بلا موعد». Closure sheet says space shows «مغلق الآن».
- **AC10 (O11):** Started unextended closure card offers «تمديد الاشتراكات» → destructive `AlertDialog` with «عدد الأيام» (≥1), count and days in words, «لا يمكن التراجع». Reception reads «يمدّد المالك الاشتراكات بعد الإغلاق». Scheduled closure offers no extension.
- **AC11 (O4,OW-017–019):** Staff columns: name (email under), status, «أُضيف في», «مقبوضاته هذا الشهر», actions. Warning badge «لم يغيّر كلمة المرور المؤقتة بعد». «إيقاف الوصول» dialog states true consequence (sessions end everywhere, name stays on payments/log, access can return). «إعادة وصول» at once. Add staff one submit «إضافة إلى الاستقبال», both outcomes said first. `StaffPassDialog` under A5 rules (no X, Escape/outside do nothing, «تم» after «نسخ», handover asked).
- **AC12 (O12+A8):** Owner never sees reporter name: «زائر» + date in list, sheet, notice. «لم يُعتمد» requires reply. «تعديل الحقل» lands on field with report above and «تم التصحيح» in place (`OwnerReportNotice` in `owner.jsx:250–269`).
- **AC13 (OW-015,OW-016):** Finance: no date range. One «الشهر» `Select` (12 months) drives month-based blocks, each names its month. Charts name windows (heatmap «آخر 4 أسابيع»). CSV labels say what they export. «عليهم مبالغ» pages. «دفعوا في …» shows five, «عرض الكل» when >5.
- **AC14 (O13):** «سجل التدقيق» in «الفريق والإعدادات» → `Owner audit.html`. Admin's audit page scoped to Focus Hub. Targets as links, `neutral` badges, `destructive` only for acts whose confirmation is destructive (`payment_voided`, `staff_deactivated`, `subscriptions_extended`, `photo_removed`). «آخر 30 يومًا» default. Actor filter: three actors (أحمد، سامي، النظام).
- **AC15 (states):** Every changed page opens under `?state=loading`, `error`, `offline`, `403`, `404`, `ratelimit` (settings/sheets), `?fail=<key>` for new actions.
- **AC16 (matrix):** Commit 13 full matrix: 21 frame URLs × 4 variants × 3 widths = 252 cells — 0 blank, 0 overflow, 0 console errors (fixer's report).
- **AC17 (checks):** `check-parse.mjs` (50/50 blocks), `check-classes.mjs` (333 classes, 5 dead pre-existing, 0 new), `format:check` (pass), `check:links` (1940 links resolve). All pass on head.
- **AC18 (archive):** `CHANGES.md` Batch 5 section (12 decision lines + Board). `INDEX.md` §55: 22 frames, parameters table with 16 rows. Board (`Flows - states.html`): section 55 with 22 frames matching INDEX. `README.md`: 515 frames / 54 sections / 41 pages. `SCREENS.md`: board section 55 added to rows 12,18–24; Owner audit line under "Also in the archive". All counts agree.
- **AC19 (boundaries):** `git diff --stat` lists only §5's 17 files. No batch 4 files beyond shared `CHANGES.md`, `INDEX.md`, `Flows - states.html`, `README.md`. `Admin space edit.html`, `shared.jsx`, `auth.jsx`, `account.jsx`, desk/account pages, `desk-core.jsx`, `desk-sheet.jsx`, `desk-data.js`, `finance.jsx`, `admin.jsx`, `admin-data.js`, `_ds/`, `_vendor/`, `screens/`, outside `docs/design/` — all untouched.
- **No object rest destructuring** in any `.jsx` (grep for `const { … } =` with `...` — none).
- **No generic top-level names** (grep for reserved names — none).
- **`O` declared once** (`owner.jsx:2`).
- **All classes** in `_ds_bundle.css` or token-only in `masaha.css` (check-classes: 0 new dead).
- **Hooks before early returns:** Fixed in `OwnerShell` (commit 1 amended). Pre-existing in `admin.jsx:27` recorded as finding.
- **DI-30/31/33** routed to worker A; **DI-32** to API; **DI-34/35/36/37/39/40** recorded — nothing built for them.

---

## Verdict

**PASS** — PR #76 meets all acceptance criteria AC1–AC19 and the hazards (§9). The two should-fix/nit items are pre-existing or plan-verbatim and do not block this PR.