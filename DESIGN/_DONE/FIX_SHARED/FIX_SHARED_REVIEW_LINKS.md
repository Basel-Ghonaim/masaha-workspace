# روابط مراجعة الإصلاح الأول — طلب الدمج ‎#59‎ (الطبقة المشتركة)

## قبل البدء

1. التشغيل من مجلد المُصلح، لا من المجلد الرئيسي (الرئيسي على `main` ولا يحوي التعديلات):

```
cd C:\Users\basel\masaha-design\docs\design\prototype; python -m http.server 5346
```

2. لماذا ليس `npx serve`: جرّبته؛ يحوّل كل رابط ‎`.html?…`‎ إلى رابط بلا امتداد **ويحذف المعاملات**، فتفتح كل حالة على وضعها الافتراضي، ويضيع `role` و`auth` و`id` عند التنقل داخل النموذج. (هذا خلل في `README.md` نفسه — مسجّل في آخر الملف.)
3. العروض الثلاثة: أدوات المطوّر ← وضع الجهاز، بعرض 390 و768 و1440.
4. اللغة والسمة: من أزرار الصفحة، أو بإضافة `&lang=en` و`&theme=dark` إلى الرابط.
5. معاملات عامة تعمل على كل صفحة لوحة تحكم: `state=loading` · `state=error` · `state=offline` · `state=403` · `state=404`، وعلى صفحات الإعدادات `state=ratelimit`.
6. فشل إجراء: أضف `&fail=<الإجراء>` ثم نفّذ الإجراء بيدك. الإجراءات: `visit` · `pay` · `checkout` · `warn` · `void` · `save`.

## ما الذي تغيّر (لتعرف أين تنظر)

- **ترويسة واحدة (P1):** العنوان والإجراءات في الشريط العلوي من 768، وتحت 768 في قائمة «⋯»؛ زر «إضافة» في صف فوق القائمة عند نهايته؛ الشريط السفلي على الهاتف فقط لـ«تسجيل زيارة» في المكتب.
- **زر الحالة العامة الواحد (P2):** على صفحات المالك والاستقبال، يفتح لوحة فيها «العودة للحالة التلقائية».
- **التنقل المجمّع (P3)** و**قائمة الحساب الواحدة (P4)** و**اللغة والسمة على الهاتف (SH-005)** و**شارة المساحة في الشريط الجانبي عند 768 (SH-006)** و**رابط «تخطَّ إلى المحتوى» بالضغط على Tab (SH-018)**.
- **شريط فلاتر واحد (P5)** وورقة الفلاتر على الهاتف، و**الترقيم في كل قائمة (P6)**، و**أولوية الأعمدة بين 768 و1023 (SH-007)**.
- **الحالات (P7)**، و**الانتظار والنجاح والفشل لكل إجراء (P8)**، و**التأكيد أو التراجع (P9)** مع «رجوع» لكل إغلاق، و**زر الحفظ مفعّل دائمًا (P10)**.

## لوحة المالك والاستقبال

1. نظرة عامة — بلا شريط سفلي على الهاتف:
   - [الافتراضي](http://localhost:5346/Owner%20overview.html)
   - [لوحة الحالة العامة مفتوحة](http://localhost:5346/Owner%20overview.html?publicstate=open)
   - [ممتلئ يدويًا لمدة](http://localhost:5346/Owner%20overview.html?override=full:84)
   - [خطأ تحميل](http://localhost:5346/Owner%20overview.html?state=error) · [بلا اتصال](http://localhost:5346/Owner%20overview.html?state=offline) · [403](http://localhost:5346/Owner%20overview.html?state=403) · [404](http://localhost:5346/Owner%20overview.html?state=404)
2. مكتب الاستقبال — الشريط السفلي الوحيد، ونخب النجاح باقية:
   - [الاستقبال](http://localhost:5346/Desk.html?role=reception) · [التحميل](http://localhost:5346/Desk.html?role=reception&state=loading)
   - [تسجيل زيارة يفشل](http://localhost:5346/Desk.html?role=reception&dialog=visit&fail=visit)
   - [الخروج يفشل](http://localhost:5346/Desk.html?role=reception&dialog=checkout&pid=pv0&fail=checkout) · [الخروج مع دين](http://localhost:5346/Desk.html?role=reception&dialog=checkout&pid=pv0&debt=1)
   - [الدفع يفشل](http://localhost:5346/Desk.html?role=reception&dialog=pay&cid=m6&fail=pay)
   - [التنبيه يفشل](http://localhost:5346/Desk.html?role=reception&dialog=warn&cid=m12&fail=warn)
3. الزبائن — 61 زبونًا مرقّمة:
   - [الافتراضي](http://localhost:5346/Customers.html) · [ورقة الفلاتر (هاتف)](http://localhost:5346/Customers.html?sheet=filters) · [التحميل](http://localhost:5346/Customers.html?state=loading)
   - [أرشفة زبون عليه دين (حوار)](http://localhost:5346/Customers.html?archive=m6) — وجرّب أرشفة زبون مسدَّد من القائمة: فورًا مع «تراجع»
   - [بصفة الاستقبال](http://localhost:5346/Customers.html?role=reception)
4. ملف الزبون — عنوانه الرئيسي اسم الزبون، ومسار التنقل للرجوع:
   - [الافتراضي](http://localhost:5346/Customer%20file.html?id=m1)
   - [إلغاء دفعة](http://localhost:5346/Customer%20file.html?id=m1&tab=pays&void=1) · [الإلغاء يفشل](http://localhost:5346/Customer%20file.html?id=m1&tab=pays&void=1&fail=void)
   - [إنهاء الاشتراك](http://localhost:5346/Customer%20file.html?id=m1&end=1)
   - [الدفع يفشل (نفّذ دفعًا)](http://localhost:5346/Customer%20file.html?id=m1&fail=pay)
5. الدفعات — 312 دفعة مرقّمة، وسبعة أعمدة كلها باقية عند 768:
   - [الافتراضي](http://localhost:5346/Payments.html) · [ورقة الفلاتر](http://localhost:5346/Payments.html?sheet=filters)
   - [إلغاء دفعة](http://localhost:5346/Payments.html?void=1) · [الإلغاء يفشل](http://localhost:5346/Payments.html?void=1&fail=void)
6. الموظفون:
   - [الافتراضي](http://localhost:5346/Staff.html) · [إضافة موظف](http://localhost:5346/Staff.html?sheet=add) · [إيقاف وصول (حوار)](http://localhost:5346/Staff.html?stop=1)
7. الإعلانات:
   - [المجدولة مع تعديل](http://localhost:5346/Announcements.html?tab=scheduled&edit=a1) · [إعلان جديد](http://localhost:5346/Announcements.html?sheet=new&type=event)
8. الباقات والأسعار:
   - [الافتراضي](http://localhost:5346/Packages.html) · [باقة جديدة](http://localhost:5346/Packages.html?sheet=new)
9. المالية:
   - [الافتراضي](http://localhost:5346/Finance.html) · [الديون](http://localhost:5346/Finance.html?tab=debts) · [ورقة الفلاتر](http://localhost:5346/Finance.html?sheet=filters)
10. بلاغات البيانات:
    - [الافتراضي](http://localhost:5346/Data%20reports.html) · [الجديدة](http://localhost:5346/Data%20reports.html?status=new) · [بلاغ مفتوح](http://localhost:5346/Data%20reports.html?open=d1)
11. إعدادات المالك — الحفظ مفعّل، و«تجاهل» تسمية واحدة:
    - [الافتراضي](http://localhost:5346/Owner%20settings.html) · [الحفظ يفشل](http://localhost:5346/Owner%20settings.html?fail=save) · [محاولات كثيرة](http://localhost:5346/Owner%20settings.html?state=ratelimit)
12. ملف المساحة (المالك):
    - [الافتراضي](http://localhost:5346/Owner%20space%20profile.html) · [الحفظ يفشل](http://localhost:5346/Owner%20space%20profile.html?fail=save)
13. دفعاتي (الاستقبال):
    - [الافتراضي](http://localhost:5346/My%20payments.html?role=reception)

## لوحة الأدمن

1. نظرة عامة: [الافتراضي](http://localhost:5346/Admin%20overview.html) · [403](http://localhost:5346/Admin%20overview.html?state=403)
2. المساحات — حذفها يبقى بتأكيد مع «تراجع»:
   - [الافتراضي](http://localhost:5346/Admin%20spaces.html) · [ورقة الفلاتر](http://localhost:5346/Admin%20spaces.html?sheet=filters) · [التحميل](http://localhost:5346/Admin%20spaces.html?state=loading)
   - [حذف مساحة](http://localhost:5346/Admin%20spaces.html?del=palm) · [فك ربط مالك](http://localhost:5346/Admin%20spaces.html?unlink=numberone) · [ربط مالك](http://localhost:5346/Admin%20spaces.html?link=golden)
3. المستخدمون — 84 مستخدمًا مرقّمين، وصارت لهم ورقة فلاتر:
   - [الافتراضي](http://localhost:5346/Admin%20users.html) · [ورقة الفلاتر](http://localhost:5346/Admin%20users.html?sheet=filters)
   - [إيقاف حساب](http://localhost:5346/Admin%20users.html?suspend=1) · [تغيير الدور](http://localhost:5346/Admin%20users.html?changerole=1)
4. أصحاب المساحات:
   - [الافتراضي](http://localhost:5346/Admin%20owners.html) · [فك ربط](http://localhost:5346/Admin%20owners.html?unlink=1) · [إضافة مالك](http://localhost:5346/Admin%20owners.html?sheet=add)
5. البلاغات: [الافتراضي](http://localhost:5346/Admin%20reports.html) · [الجديدة](http://localhost:5346/Admin%20reports.html?status=new) · [بلاغ مفتوح](http://localhost:5346/Admin%20reports.html?open=r1)
6. سجل التدقيق — 240 سطرًا مرقّمة، وورقة فلاتر جديدة:
   - [الافتراضي](http://localhost:5346/Admin%20audit.html) · [ورقة الفلاتر](http://localhost:5346/Admin%20audit.html?sheet=filters)
7. القوائم: [الافتراضي](http://localhost:5346/Admin%20lookups.html) · [تعديل منطقة](http://localhost:5346/Admin%20lookups.html?edit=area)
8. إعدادات المنصة: [الافتراضي](http://localhost:5346/Admin%20settings.html) · [الحفظ يفشل](http://localhost:5346/Admin%20settings.html?fail=save) · [محاولات كثيرة](http://localhost:5346/Admin%20settings.html?state=ratelimit)
9. تعديل مساحة — العنوان الرئيسي اسم المساحة: [الافتراضي](http://localhost:5346/Admin%20space%20edit.html?id=focus)

## الموقع العام والحساب

1. الرئيسية — «للعرض فقط · الدفع في المساحة» مرة واحدة: [الافتراضي](http://localhost:5346/Home.html?loc=none) · [مسجّل الدخول](http://localhost:5346/Home.html?loc=none&auth=1)
2. الدليل — ورقة الفلاتر صارت المشتركة:
   - [القائمة](http://localhost:5346/Directory.html?loc=none) · [ورقة الفلاتر (هاتف)](http://localhost:5346/Directory.html?loc=none&sheet=filters) · [الخريطة](http://localhost:5346/Directory.html?view=map&selected=focus&loc=none)
3. تفاصيل المساحة (الترويسة وقائمة الحساب): [الافتراضي](http://localhost:5346/Space%20details.html?id=focus&loc=none&auth=1)
4. صفحات الخطأ — صفحة 403 جديدة: [403](http://localhost:5346/Error.html?type=403) · [404](http://localhost:5346/Error.html?type=404) · [بلا اتصال](http://localhost:5346/Error.html?type=offline) · [خطأ](http://localhost:5346/Error.html?type=error)
5. المفضلة: [الافتراضي](http://localhost:5346/Favorites.html?auth=1&loc=none)
6. بلاغاتي: [الافتراضي](http://localhost:5346/Reports.html?auth=1)
7. إعدادات حسابي: [الافتراضي](http://localhost:5346/Settings.html?auth=1)
8. صفحة «عن مساحة» (الترويسة فقط): [الافتراضي](http://localhost:5346/About.html)
9. صفحات الدخول (الترويسة فقط): [الدخول](http://localhost:5346/Sign%20in.html) · [التسجيل](http://localhost:5346/Register.html) · [نسيت كلمة المرور](http://localhost:5346/Forgot%20password.html) · [تعيين كلمة المرور](http://localhost:5346/Reset%20password.html) · [تغيير كلمة المرور](http://localhost:5346/Change%20password.html)

## لوحة التصميم

1. [لوحة الحالات](http://localhost:5346/Flows%20-%20states.html) — تسميات الإطارات بعد «subscription» و`publicstate`.

## خلل وجدته أثناء التحضير (للإصلاحات)

1. **أمر التشغيل في `docs/design/README.md` يحذف المعاملات:** `npx serve .` يعيد توجيه ‎`X.html?…`‎ إلى `X` بلا معاملات، فلا تعمل روابط `INDEX.md` ولا جدول المعاملات الجديد. الإصلاح المقترح: ملف `serve.json` في `prototype/` فيه `{"cleanUrls": false}`، فيعمل أمرك `npx serve` كما هو.
