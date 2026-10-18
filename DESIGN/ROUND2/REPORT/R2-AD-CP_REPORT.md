# R2-AD-CP — Round 2 review: The admin's dashboard · Content and Arabic copy

## 1. Commit SHAs

- `git rev-parse HEAD`: `34a6c59aab049e8f2992b29b88c8a700b926ddba`
- `git rev-parse origin/main`: `34a6c59aab049e8f2992b29b88c8a700b926ddba`

## 2. Verdict

The admin dashboard's Arabic is functional but inconsistent — one concept appears under four to six different phrasings across pages, and several labels omit the consequence they promise.

## 3. The five most important points

1. **"Stale or missing" has no stable name.** The same condition is «بيانات قديمة أو ناقصة» (overview tile), «قديمة أو ناقصة» (quick-filter chip), «قديمة:»/«ناقصة:» (badges), «ناقصة» (badge), and «لم تُضف بعد» (checklist) — five forms for one idea, none matching the glossary's «قد تكون قديمة».
2. **Unlink is named three ways.** «فك ربط» (dropdown, space edit), «فك الربط» (dialog action button, owners page), «فُك الربط» (toast) — inconsistent declension of the same verb.
3. **Restore conflates two different things.** «استرجاع» restores a space; «استرجاع الحساب» restores a user account; «استرجعه أولًا» asks to restore an account before linking. The same verb with no shared pattern.
4. **Hidden/inactive uses two terminologies.** Areas and governorates use «مخفية»/«ظاهرة»; amenities use «غير النشط»/«نشط» — different words for the same concept on the same page.
5. **Role-change dialog titles are asymmetric.** «جعل [اسم] أدمن؟» uses «جعل» (make); «إعادة [اسم] مستخدمًا؟» uses «إعادة» (return) — different verbs, same operation.

## 4. Issues

### R2-AD-CP-001
- **Title:** Five names for "stale or missing"
- **Type:** defect
- **Level:** pattern
- **Impact:** medium
- **Where:** Overview tile, spaces quick-filter chip, freshness badges, missing checklist; AR 1440
- **What is wrong:** One concept appears as «بيانات قديمة أو ناقصة», «قديمة أو ناقصة», «قديمة:»/«ناقصة:», «ناقصة», and «لم تُضف بعد» — five forms, none matching the glossary.
- **Proposal:** AR: «قديمة» for stale, «ناقصة» for missing, consistent across all surfaces. EN: "Stale" / "Missing".
- **Why:** One concept, one name; faster mental model.
- **Cost:** S
- **Rule:** glossary «Stale»

### R2-AD-CP-002
- **Title:** Unlink named three ways
- **Type:** defect
- **Level:** pattern
- **Impact:** medium
- **Where:** Spaces dropdown, owners dropdown, dialog action, toast; AR 1440
- **What is wrong:** «فك ربط», «فك الربط», and «فُك الربط» for the same action.
- **Proposal:** AR: «فكّ الربط» everywhere. EN: "Unlink".
- **Why:** One verb, one form; matches audit log's «فك ربط مالك».
- **Cost:** S
- **Rule:** P9 verb discipline; DECISIONS_ADMIN A4

### R2-AD-CP-003
- **Title:** «استرجاع» conflates space restore and account restore
- **Type:** defect
- **Level:** pattern
- **Impact:** medium
- **Where:** Spaces list, owners error link, users action, audit log; AR 1440
- **What is wrong:** Two different operations share the bare verb «استرجاع»; the audit log distinguishes them but the UI does not.
- **Proposal:** AR: «استرجاع المساحة» for spaces, «استرجاع الحساب» for users. EN: "Restore space" / "Restore account".
- **Why:** Matches the audit log's vocabulary; removes ambiguity.
- **Cost:** S
- **Rule:** A3; glossary (no entry for "restore")

### R2-AD-CP-004
- **Title:** Hidden/inactive uses two terminologies on the same page
- **Type:** defect
- **Level:** page
- **Impact:** low
- **Where:** Lookups page areas tab vs amenities tab; AR 1440
- **What is wrong:** «مخفية»/«ظاهرة» for areas vs «غير النشط»/«نشط» for amenities.
- **Proposal:** AR: «مخفية» everywhere. EN: "Hidden" / "Shown".
- **Why:** One page, one concept, one word; glossary already settled «مخفية».
- **Cost:** S
- **Rule:** glossary («The admin hides an unreachable area»)

### R2-AD-CP-005
- **Title:** Role-change dialog titles use different verbs
- **Type:** defect
- **Level:** component
- **Impact:** low
- **Where:** Users role dialog; AR 1440
- **What is wrong:** «جعل [اسم] أدمن؟» vs «إعادة [اسم] مستخدمًا؟» — different verbs for the same operation.
- **Proposal:** AR: «تغيير الدور: أدمن؟» / «تغيير الدور: مستخدم؟». EN: "Change role: admin?" / "Change role: user?".
- **Why:** One operation, one frame.
- **Cost:** S
- **Rule:** A5

### R2-AD-CP-006
- **Title:** Overview helper «الباقي» is vague
- **Type:** defect
- **Level:** page
- **Impact:** medium
- **Where:** Overview tile helper; AR 1440
- **What is wrong:** «الأسعار > 30 يومًا · الباقي > 60 · أو لم تُضف بعد» — «الباقي» does not name which groups it covers.
- **Proposal:** AR: «الأسعار > 30 يومًا · ساعات العمل والتواصل والمرافق > 60 · أو لم تُضف بعد». EN: "Prices > 30 days · hours, contacts, amenities > 60 · or not added yet".
- **Why:** The overview is the admin's landing page; it should name what it counts.
- **Cost:** S
- **Rule:** A8 (overview is a work queue)

### R2-AD-CP-007
- **Title:** «ردّ فريق مساحة» vs «ردّ إدارة المساحة» — same entity named two ways
- **Type:** defect
- **Level:** page
- **Impact:** low
- **Where:** Reports sheet reply labels; AR 1440
- **What is wrong:** Reply field reads «ردّ فريق مساحة» but the read-only verified-space reply reads «ردّ إدارة المساحة».
- **Proposal:** AR: «ردّ فريق مساحة» everywhere. EN: "Reply from the Masaha team".
- **Why:** One team, one name.
- **Cost:** S
- **Rule:** glossary (no entry for the admin team name)

### R2-AD-CP-008
- **Title:** Temp password handover line differs between owners and users pages
- **Type:** defect
- **Level:** pattern
- **Impact:** low
- **Where:** Owners and users TempPassDialog; AR 1440
- **What is wrong:** Owners: «سلّمها للمالك؛ سيُطلب منه تغييرها عند أول دخول.» Users: «سلّمها له بعد التأكد من هويته؛ سيُطلب منه تغييرها عند الدخول التالي.»
- **Proposal:** AR: one shared line; users variant adds «بعد التأكد من هويته» as prefix.
- **Why:** Same dialog, same product behaviour.
- **Cost:** S
- **Rule:** A5 (the one-time password dialog)

### R2-AD-CP-009
- **Title:** «فُكّ ربطه أولًا» uses passive participle where imperative is expected
- **Type:** defect
- **Level:** component
- **Impact:** low
- **Where:** Users page disabled dropdown item; AR 1440
- **What is wrong:** «فُكّ ربطه أولًا» is a passive participle in a sentence that addresses the admin directly; the parallel text uses imperatives («استرجعه أولًا», «فك روابطه»).
- **Proposal:** AR: «فكّ ربطه أولًا» (imperative). EN: "Unlink them first".
- **Why:** Surrounding text addresses the admin with imperatives; this breaks the pattern.
- **Cost:** S
- **Rule:** A5 (disabled items say why)

### R2-AD-CP-010
- **Title:** «عُلّم «تم التصحيح»» uses passive where active is expected
- **Type:** defect
- **Level:** component
- **Impact:** low
- **Where:** Reports sheet and space edit report notice; AR 1440
- **What is wrong:** The toast and post-action alert use «عُلّم «تم التصحيح»» (passive: "was marked") while the action button uses «تم التصحيح» (active). The same for «لم يُعتمد» vs «عُلّم «لم يُعتمد»».
- **Proposal:** AR: «تم التصحيح» toast: «تم التصحيح — عُلم البلاغ» or simply «تم التصحيح». EN: "Corrected".
- **Why:** Active voice matches the action button and the admin's mental model.
- **Cost:** S
- **Rule:** A8 (report resolve lines)

### R2-AD-CP-011
- **Title:** «جديد» for reports vs «تم التصحيح»/«لم يُعتمد» — status names lack a shared pattern
- **Type:** improvement
- **Level:** page
- **Impact:** low
- **Where:** Reports status filter chips; AR 1440
- **What is wrong:** «جديد» (new) is an adjective describing the report's age, while «تم التصحيح» (corrected) and «لم يُعتمد» (not accepted) describe the resolution. Two different semantic axes in one filter.
- **Proposal:** AR: «مفتوح» (open) instead of «جديد» to pair with the resolution statuses. EN: "Open".
- **Why:** One filter, one semantic axis (status of resolution).
- **Cost:** S
- **Rule:** A8 (report statuses)

## 5. Decisions in doubt

None. The settled wording is applied where it fits; the issues above are about internal consistency, not about a settled decision causing harm.

## 6. What was not reviewed and why

- **Visual rendering (browser screenshots).** The built-in browser tools were not available in this session; the review is based on source-code reading of the prototype HTML/JSX and admin-data.js.
- **Dark mode.** Only light mode was reviewed; no copy difference between themes was found in the source.
- **Phone width (390).** String lengths were reviewed for potential overflow, but no rendering was possible without the browser.
- **English mirror (?lang=en).** The tr() calls were reviewed for meaning parity; no rendering check was possible.
- **Out of axis:** flow (UX), layout (VD), breakage/overflow (DF), removals (EX), focus/names/contrast (AX), permissions/data-depth truth (TR).
