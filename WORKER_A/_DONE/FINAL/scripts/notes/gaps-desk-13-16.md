# Gaps 13, 16 (agent report)

## 13 Front desk — partial
1. «السجل» tab (K8) missing: «الآن | السجل» tabs beside «الحاضرون الآن», day picker, log rows (name, in, out, duration, «تلقائي عند الإغلاق|يدوي»), empty «لا يوجد حضور في هذا اليوم». absent (DeskPage renders PresentList alone; repo never calls GET …/visits or check-ins?from&to). Desk.html LogTab. L. Fix: GET …/visits?from=to=day + GET …/check-ins?from&to merged by check-in time, 20/page, cards <768; owner any day, reception today only. Natural home for written-off visits (164).
2. Phone order wrong: below xl search → present → uncollected; design search → uncollected → present. DeskPage.tsx:232-239; masaha.css:113-115; K1. S.
3. Empty «غير محصّل» always shows, says it twice ('لا زيارات غير محصّلة' + 'لا توجد مبالغ غير محصّلة.'); design hides below xl when empty, keeps title «غير محصّل» with CircleCheckIcon line. UncollectedCard.tsx:106-109, useUncollectedCard.ts:119,125. S.
4. Usage-based subscriber's check-out dialog missing (every subscriber one tap + toast «استلام»). CheckOutAction.tsx:89-113. desk-core.jsx isQuickOut only fixed; dialog «المستحق حتى الآن», «يُحسب من الحضور: …», «اليوم N س · المدفوع …», «يبقى على اشتراك…», «خروج واستلام». M → needs API quote for open check-in (progress counts closed stays; S7 forbids web pricing) or check-out-then-pay. DI/OD.
5. Names not links to «ملف الزبون»: present rows, search «حاضر الآن» rows, uncollected rows with customer, search card titles. PresentList.tsx:96-98,185-187, PresentMatches.tsx, UncollectedRow.tsx:30-32, CustomerCard.tsx h3. S.
6. Kind badge plain: subscriber «اشتراك» neutral; design subscription name in primary; student visit «زيارة · طالب» impossible (VISIT PresentPerson no audience). usePresentList.ts:45, PresentList.tsx:104,188. M: add audience to VISIT PresentPerson (API); subscription name from useOpenCheckIns.
7. No «تجديد»/«اشتراك جديد» from the desk: search card no «تجديد» when ending soon/expired; pre-check-in no «تجديد» (expired) or «اشتراك جديد» (none). CustomerCard.tsx, PreCheckInDialog.tsx. M (renew needs SubscriptionState; read first).
8. Search card no progress lines («هذا الأسبوع 3 من 3») and no «غير حاضر» badge. CustomerRow.current {id,name,packageId,endsOn,status} no progress. M (API: progress/terms on CustomerRow.current).
9. Visit dialog's "full" from status not count (full = now?.status === 'FULL'); alert lacks count «المساحة ممتلئة 27/40». DeskPage.tsx:80. S.
10. Visit dialog «طالب» Checkbox (design Switch); «الوردية» Select with «بدون وردية» (design deselectable ToggleGroup). VisitDialog.tsx:54-83. S.
11. Check-out calc line incomplete: «4 س × 3 ₪ = 12 ₪ · تقريب…», «السقف: سعر اليوم 15 ₪», «لا يوجد سعر بالساعة — سعر اليوم 15 ₪». useCheckOutDialog.ts:212-228. S (display only per S7).
12. No live «يُضاف إلى ملف {name}» when typed phone is a known customer's (check-out debt fields, «تسجيل دين»). useCheckOutDialog.ts:281-283, DebtDialog. M: debounced GET …/customers?q=<phone>.
13. 429 in money dialogs doesn't say «لم يُسجَّل شيء. إعادة المحاولة بعد ذلك لن تسجّله مرتين.» deskRefusal.ts, FormFailure.tsx:10-16. S.
14. Phone fields lack «+970 59 000 0000» placeholder (check-out debt, «تسجيل دين», «تعديل البيانات», sheet). S.
15. Icons missing: «تسجيل زيارة», «خروج», «حضور» LogIn/LogOut; empty states UsersIcon/SearchXIcon; status control ChevronDown from 768. DeskPage.tsx:162,195, CheckOutAction, CustomerCard, PresentList.tsx:200, DeskSearch.tsx:171, LiveStatusControl.tsx:51. S.
16. Search field not large: layer Input no size prop; Desk.html size="lg". S (layer + desk).
17. Words: «منذ» cell repeats «منذ 09:10» under «منذ» header; «إجراءات» header visible (sr-only); «ساعتان» → «ساعتين»; «ملاحظة» lacks «اختياري» in «استلام دفعة» and «تحصيل». usePresentList.ts:46, occupancy.ts durations, PayDialog/CollectDialog. S.
18. Check-out dialog no description (aria-describedby undefined; kind as badge); money block stacks at 768+ («المستلم الآن», «الطريقة» side by side from md). CheckOutDialog.tsx:73-79, MoneyBlock.tsx. S.
19. Offline not own state: present list, uncollected card, search → destructive load-failure Alert, not P7 offline («لا يوجد اتصال بالإنترنت», WifiOff). PresentList.tsx:160-174, UncollectedCard.tsx:85-105. S.
20. 160. 21. 130. 22. 132. 23. 172.
24. visits.md Authority says "no web screen yet". S.
UNVERIFIED: 768 top bar wrap, dark contrast.

## 16 New / renew subscription — partial
1. Dates native <Input type="date">; package end read-only text input; should be layer DatePicker. SubscriptionSheet.tsx. S.
2. Custom end note wrong when a total is set: always «بلا تاريخ نهاية · يبقى نشطًا حتى يُنهى»; design «… ينتهي عند استهلاك 20 ساعة أو …، أيهما أسبق» (DK-008). useSubscriptionSheet.ts:430. S.
3. Prior debt plain section not warning Alert; MoneyBlock calc=[]; due labelled «المستحق» not «المجموع» with each part («التجديد: {name} {price}»). PriorDebts.tsx; SubscriptionSheet.tsx. S.
4. Usage-based custom lacks «يُحسب من الحضور: 3 ₪ للساعة» line and rate prefill from published price «من السعر المنشور». CustomTerms.tsx. S.
5. Package group heading «باقات المساحة — لا تظهر للزوار» vs design «خاصة بالمكتب — لا تظهر للزوار» + «خاصة» badge per row. desk.ts sheet.groups.packages. S.
6. 171.
Decided: DI-2, DI-3, DI-19, DI-9/DI-29, DI-12, S6/DI-14, DI-20/DI-36, DI-22, DI-32/DI-33, DI-40, S8, S10, «تبديل الموظف», «بدون سعر»; sheet DI-37, DI-50, DI-51, DI-52, DI-53, S5, decision 3 / 125.
Total 30.
