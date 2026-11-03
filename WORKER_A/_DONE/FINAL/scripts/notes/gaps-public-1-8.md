# Gaps 1–8 (agent report)

## 1 Home — partial
1. Phone header theme/language wrong way round: SH-005 language in header at every width, theme in drawer. SiteHeader.tsx:44-45, SiteMenu.tsx. Every site page. S. Update architecture §2 line.
2. No account avatar in phone header (P4): AccountMenu hidden md:inline-flex. SiteHeader.tsx:51. S: avatar alone below 768.
+ carried 3, 4, 10.

## 2 Directory — partial
1. Map view has no result count (U2/P5). DirectoryView.tsx:57-61. S.
2. Phone map view stacks search and «الفلاتر»; U6 one row. DirectoryView.tsx:45. S.
3. Chosen space on the map has no distance «على بعد … كم» (U6). SpaceSummary.tsx. S (straightLine.ts).
+ 132–136, carried 11.

## 3 Space details — partial
1. Status card can vanish (panelShown = today || distance). SpaceDetails.tsx:89,121,137. S: always draw panel.
2. Today's line ignores running closure: «مغلقة مؤقتًا اليوم». useSpacePage.ts:169. S.
3. Location map never shows visitor's point. LocationSection.tsx:14. S.
4. «الاتجاهات» under the address; design section header action. LocationSection.tsx. S.
+ 138, carried 6, 7.

## 4 About — partial
1. Platform contact from VITE_CONTACT_* not GET /settings/public. platformContact.ts:31-35. M: public query in platform-settings, loading/failed, drop env reads (+ finding 40 seam). 
2. «تصفّح المساحات» outline self-start; design primary full-width on phone (w-full md:w-auto). AboutPage.tsx:32. S.
3. Verified card lacks CircleCheckIcon in CardTitle. AboutPage.tsx:39-42. S.
4. Contact sentence differs: built «راسلنا إن كان لديك سؤال، أو مشكلة في الموقع الإلكتروني.» design «اكتب لنا بسؤال، أو عن بلاغ لم يصلك ردّه، أو عن خطأ في الموقع.» site.ts about.contact.text. S → DI.
+ carried 1, 2, 9.

## 5 Sign in — partial
1. Description doesn't speak to owners/reception (C4): design «سجّل الدخول لحفظ مساحاتك المفضّلة ومتابعة بلاغاتك، أو لإدارة مساحتك.» auth.ts signIn.description. S.
2. Way out ignores next (AC-017/AC-019): «العودة إلى {space}» or «العودة إلى الرئيسية»; built «تصفّح المساحات بدون حساب» → /spaces. SignInPage.tsx:64; auth.jsx AuthWayBack. S.
3. next lost to forgot page and back. SignInPage.tsx:49, ForgotPasswordPage.tsx:19. S (relates 168).
4. No «أهلًا بعودتك» toast after email sign-in. useSignIn.ts. S.
5. Google linked toast closes after 10 s; C5 stays until closed (duration Infinity + closeButton). useGoogleSignIn.ts:12. S.
6. Focus shell skip link → 130.
+ 32.

## 6 Register — partial
1. Card has no way out (C4). RegisterPage.tsx. S.
2. Owner note links #contact; design «تواصل معنا» → About#owners. RegisterPage.tsx:54. S.
3. Fourth password rule missing (AC-020) «طويلة جدًا — اختصرها» only when broken; >72 bytes gets generic. shared users/passwordPolicy.ts PASSWORD_RULES three; usePasswordRules.ts. Also reset form. S.

## 7 Forgot / reset — partial
1. «استخدم بريدًا آخر» missing from sent step (C3, DI-31) — only once resends spent. LinkSent.tsx:24. S: always under resend; opens empty form, focus in it.
2. Reset card lacks «العودة إلى تسجيل الدخول» (C4). ResetPasswordCard.tsx. S.
3. «لا يمكنك الوصول إلى بريدك؟ تواصل معنا» → /about#contact; should open WhatsApp (foundation §13 #7). ForgotPasswordPage.tsx:24. S: platform WhatsApp, fallback #contact.
4. Reset email lacks copyable link «إن لم يعمل الزر، انسخ هذا الرابط:» + URL (AC-021). api resetEmail.ts:54, resetEmail.copy.ts. S (relates 22).
+ 65, 168.

## 8 404/error/offline — partial
1. General error retry only reloads; never says «ما زال الخطأ قائمًا. حاول بعد قليل.» (PU-024). RetryState.tsx:45. S/M: reset boundary first, say line on second failure; reload only when the page's code failed.
2. 403 has no shell and no way on: /admin for non-admin bare ForbiddenState; text «هذه الصفحة غير متاحة لحسابك.» vs design «إن كنت تظن أن هذا خطأ، تواصل معنا.» + «الرئيسية». routes.tsx:126, ForbiddenState.tsx. S.
+ carried 5.

Decided: six cards; distance sort keeps location (DI6); privacy line (DI5); «مطابقة» (DI3); guest heart prompt DI-60; save on return toast DI-61; DI-58; «لم نجد هذه المساحة» (DI25); «فريقنا» (DI26); hidden/stale prices (DI27,28); legend none line (DI16); idle alert.
Count: 0 built, 8 partial; 27 gaps.
