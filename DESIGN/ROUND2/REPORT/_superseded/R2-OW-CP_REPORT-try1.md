# R2-OW-CP — Round 2 review: The owner's management · Content and Arabic copy

## 1. Commit SHAs

- HEAD: `02b1067a136d3c86378b3da60937c5f51124dc5b`
- origin/main: `02b1067a136d3c86378b3da60937c5f51124dc5b`
- `git diff --quiet HEAD origin/main -- docs/design` → exit 0: **design unchanged**. Continuing the review.

## 2. Verdict

The owner's management copy correctly applies the settled decisions (O1–O13, P9 verb discipline, O9 no-title announcements, O5 plurals, SH-019 subscription terminology). The two findings are: the extension confirmation dialog cannot be reached from the INDEX URL because the referenced announcement is already extended, and the extension confirmation button uses a past-tense Arabic verb for a future action.

## 3. Five most important points

1. Extension dialog unreachable — INDEX URL `Announcements.html?tab=ended&extend=a6` never opens the AlertDialog because a6 is already extended (verified: `dialog: false` on the rendered page).
2. Extension confirmation verb uses past tense — `F_EXTEND_VERB.ar.one = "مدّد اشتراكًا واحدًا"` ("he extended") for a future action; English uses imperative "Extend".
3. Settled decisions are correctly applied — O9 (no announcement title), O10 («إنهاء الآن»), O12 (reporter as «زائر»), O5 (plurals through all forms), P9 (destructive confirmation repeats the verb).
4. Tab counts render as badges with correct counts — "نشطة2", "مجدولة1", "منتهية3" on the Announcements page.
5. English mirror is clean — no leftover Arabic in content (only the intentional language-toggle label "العربية").

## 4. Issues

### R2-OW-CP-001 — Extension confirmation dialog never opens from the INDEX URL

- **type:** defect
- **level:** page
- **impact:** high
- **where:** Frame 38 · Announcements «الإعلانات» (owner + reception); `http://127.0.0.1:5426/Announcements.html?tab=ended&extend=a6`; 1440×1000, Arabic, light; screenshot `D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\OW-CP\R2-OW-CP-024b-ann-extend-a1-1440-ar.png` (same result with `extend=a6`)
- **evidence:** Capture `R2-OW-CP-024b-ann-extend-a1-1440-ar.png`; `browser_evaluate` on the rendered page returned `{ "dialog": false }` — no AlertDialog is present. Also verified `?tab=ended&extend=a6` shows no dialog.
- **what is wrong:** Announcement a6 carries `extended: { count: 19, days: 3, by: 'أحمد', on: '2026-09-17' }`, so `extendable(a6)` (`IS_OWNER && type === 'closure' && annStatus !== 'scheduled' && !a.extended`) is false. No closure in the demo data is extendable: a1 is scheduled (future), a4 and a6 are already extended. The extension dialog copy — "تمديد اشتراكات المشتركين النشطين بأيام الإغلاق؟", "لا يمكن التراجع، ولا تطبيقه مرة ثانية لهذا الإغلاق", and the action naming who moves (أحمد) and how many days — cannot be observed on any rendered page, blocking CP review of that scope item.
- **proposal:** Change the demo data so at least one ended closure is not extended (or point the INDEX URL at an extendable closure), so the AlertDialog opens and its copy can be reviewed. Keep the dialog copy as designed: it names who moves («by: أحمد»), how many days, and states it cannot be undone nor reapplied.
- **why:** The prompt's scope explicitly names "the extension dialog (who moves, how many days)" as copy to cover. If it never opens, it cannot be reviewed.
- **cost:** S (demo data fix)
- **rule:** O11 (closure extension is its own destructive AlertDialog, naming how many active subscriptions move and by how many days); INDEX §55 frame "Closure extension · the confirmation"; P9 verb discipline.

### R2-OW-CP-002 — Extension confirmation button uses a past-tense Arabic verb for a future action

- **type:** defect
- **level:** component
- **impact:** medium
- **where:** Extension AlertDialog in Announcements «الإعلانات»; `http://127.0.0.1:5426/Announcements.html` (constant present in page runtime); 1440×1000, Arabic, light; screenshot `D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\OW-CP\R2-OW-CP-020-ann-1440-ar.png`
- **evidence:** `browser_evaluate` on the rendered page returned `window.F_EXTEND_VERB.ar.one = "مدّد اشتراكًا واحدًا"` (past tense "مدّد" = "he extended one subscription"), while `en[0] = "Extend {n} subscription"` (imperative). Same mismatch across all plural forms: two "مدّد اشتراكين", few "مدّد {n} اشتراكات", etc.
- **what is wrong:** The confirmation button asks the user to perform a future action, but the Arabic uses the past tense "مدّد" ("he extended"), reading as a statement about something already done. The English "Extend" is imperative/present. Tense mismatch between languages; Arabic reads as a translation of an English past-tense statement rather than Arabic said first.
- **proposal:** Arabic: imperative "مدد اشتراكًا واحدًا" (one), "مدد اشتراكين" (two), "مدد {n} اشتراكات" (few), "مدد {n} اشتراكًا" (many), "مدد {n} اشتراك" (other). Or future "سيمدّد …". Match the English imperative "Extend {n} subscription".
- **why:** The confirmation action should ask the user to do something (imperative), not state it already happened (past tense). Consistency between AR and EN; CP axis #1 (Arabic said first, not translated) and #3 (one thing named two ways).
- **cost:** S (copy string change)
- **rule:** P9 — action `variant="destructive"` repeating the verb (DECISIONS_SHARED.md); glossary "Extension" not a term, but verb discipline applies.

## 5. Decisions in doubt

None. All settled decisions (O1–O13, P9 verb discipline, O9 no-title announcements, O5 plurals, SH-019) are correctly applied where observed. No settled line is misapplied.

## 6. What was not reviewed and why

- **Extension dialog copy (who moves, how many days):** The AlertDialog never opens because no closure in the demo data is extendable (a1 scheduled; a4 and a6 already extended). The INDEX URL `?tab=ended&extend=a6` produces no dialog (verified: `dialog: false`). The dialog's Arabic copy cannot be evaluated on the rendered page. Covered as issue R2-OW-CP-001.
- **Queue rows that need `?demo=` params:** «لم تُضف بعد» (missing section), «إغلاق لم تُمدَّد اشتراكاته» (unextended ended closure) only appear with `?demo=missing` / an unextended ended closure. Default data has capacity set, no missing sections, and all ended closures already extended, so these rows do not render on the default page.
- **Dark mode:** The prompt states "light is enough unless a string differs in dark." No string was observed to differ in dark; dark was not captured.
- **768 width:** The prompt's scope names 1440 and 390 (Arabic), then 1440 (English, plus 390 for dialogs/sheets). 768 was not captured as it is outside the named widths for this part.
- **Package sheet at 1440:** Captured at 390 (`R2-OW-CP-035-packages-sheet-390-ar.png`); the sheet's repeated-name line and validity/limit/billing lines were read in source but the sheet was not opened at 1440.
- **English mirror at 390:** Captured for staff password dialog (390 EN). Other sheets/dialogs at 390 EN were not captured beyond what the prompt requires (dialogs/sheets at 390 — staff password dialog done).
- **Void reason format «ألغاها أحمد: …»:** The audit shows the void reason in the details column ("سُجّلت مرتين بالخطأ") with the actor (أحمد) in a separate column; the combined "ألغاها أحمد: …" format was not observed in the rendered audit rows. This is a presentation choice (actor separated from reason), not a copy defect.
