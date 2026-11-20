/* The words. The product's catalogue verbatim (apps/web/src/shared/copy/{arabic,english}/*.ts) where it has them;
   the direction's new words (DESIGN.md › New copy (proposed)) are marked NEW. */
(function () {
  var arPlural = function (n, f) {
    if (n === 0) return f.zero; if (n === 1) return f.one; if (n === 2) return f.two;
    var m = n % 100; if (m >= 3 && m <= 10) return f.few; if (m >= 11) return f.many; return f.other;
  };
  window.COPY = {
    ar: {
      title: function (p) { return p + ' · مساحة'; },
      skip: 'تخطَّ إلى المحتوى', nav: 'التنقّل الرئيسي',
      links: { home: 'الرئيسية', spaces: 'المساحات', about: 'عن مساحة', privacy: 'سياسة الخصوصية' },
      signIn: 'تسجيل الدخول', menu: 'القائمة', closeMenu: 'إغلاق القائمة',
      tagline: 'مساحة — دليل مساحات العمل المشتركة في قطاع غزة',
      contact: 'تواصل معنا', browse: 'تصفّح المساحات',
      langName: 'English', langLabel: 'Switch to English',
      theme: { light: 'المظهر الداكن', dark: 'المظهر الفاتح' },
      account: { nav: 'حسابي', favorites: 'المفضّلة', reports: 'بلاغاتي', settings: 'إعدادات حسابي', menu: function (n) { return 'قائمة الحساب: ' + n; }, signOut: 'تسجيل الخروج' },
      footerContact: 'واتساب وبريد فريق مساحة', // NEW
      whatsapp: 'واتساب', email: 'بريد',
      // home
      home: {
        title: 'اعثر على مساحة عمل في قطاع غزة',
        lead: 'ساعات العمل والأسعار والحالة المباشرة لمساحات العمل المشتركة، في مكان واحد.',
        searchLabel: 'ابحث عن مساحة', searchPh: 'اسم المساحة أو المنطقة', searchSubmit: 'بحث',
        gazaTime: 'بتوقيت غزة', // NEW
        openOf: function (n, m) { return 'مفتوحة الآن: ' + n + ' من ' + m + ' مساحة'; }, // NEW
        openNow: 'مفتوحة الآن', viewAll: 'عرض الكل',
        openingNext: 'تفتح قريبًا', // NEW
        empty: { title: 'لا توجد مساحات مفتوحة الآن', text: 'قد تكون المساحات مغلقة في هذا الوقت. تصفّح كل المساحات لمعرفة ساعات عملها.', action: 'تصفّح كل المساحات' },
        areas: 'تصفّح حسب المنطقة', all: 'كل المناطق', strip: 'قطاع غزة',
        chapterOpen: function (n) { return arPlural(n, { one: 'واحدة مفتوحة الآن', two: 'اثنتان مفتوحتان الآن', few: n + ' مفتوحة الآن', many: n + ' مفتوحة الآن', other: n + ' مفتوحة الآن', zero: '' }); }, // NEW
        owners: { title: 'هل تدير مساحة عمل؟', text: 'تواصل معنا لإضافة مساحتك، وإدارة ساعاتها وأسعارها، وتظهر حالتها المباشرة تلقائيًا من تسجيل الحضور.', action: 'تواصل معنا' }
      },
      count: function (n) { return arPlural(n, { zero: n + ' مساحة', one: 'مساحة واحدة', two: 'مساحتان', few: n + ' مساحات', many: n + ' مساحة', other: n + ' مساحة' }); },
      // directory
      dir: {
        title: 'مساحات العمل',
        all: function (n) { return arPlural(n, { zero: n + ' مساحة في قطاع غزة', one: 'مساحة واحدة في قطاع غزة', two: 'مساحتان في قطاع غزة', few: n + ' مساحات في قطاع غزة', many: n + ' مساحة في قطاع غزة', other: n + ' مساحة في قطاع غزة' }); },
        matching: function (n) { return arPlural(n, { zero: n + ' مساحة مطابقة', one: 'مساحة واحدة مطابقة', two: 'مساحتان مطابقتان', few: n + ' مساحات مطابقة', many: n + ' مساحة مطابقة', other: n + ' مساحة مطابقة' }); },
        searchLabel: 'ابحث عن مساحة', searchPh: 'اسم المساحة أو المنطقة',
        refine: 'تنقيح', // NEW
        refineTitle: 'تنقيح القائمة', // NEW
        sortLabel: 'الترتيب', sorts: { updated: 'الأحدث تحديثًا', name: 'حسب الاسم', priceAsc: 'الأرخص شهريًا', priceDesc: 'الأغلى شهريًا', distance: 'حسب المسافة' },
        priceAsc: { HOUR: 'الأرخص بالساعة', DAY: 'الأرخص يوميًا', WEEK: 'الأرخص أسبوعيًا', MONTH: 'الأرخص شهريًا' },
        priceDesc: { HOUR: 'الأغلى بالساعة', DAY: 'الأغلى يوميًا', WEEK: 'الأغلى أسبوعيًا', MONTH: 'الأغلى شهريًا' },
        near: 'الأقرب إليّ', locating: 'جارٍ تحديد موقعك…', sortedNear: 'مرتبة حسب المسافة من موقعك.', approx: 'المسافات تقريبية بخط مستقيم.',
        stopNear: 'إيقاف الترتيب حسب المسافة', nearPrivacy: 'يُرسَل موقعك مقرَّبًا لترتيب المساحات حسب المسافة فقط، ولا يُحفظ.',
        nearDemo: 'في هذا النموذج: موقع تقريبي في الرمال.', // NEW (mock-up only)
        view: 'طريقة العرض', list: 'قائمة', map: 'خريطة',
        filters: 'الفلاتر', applied: 'تُطبَّق فورًا على النتائج',
        area: 'المنطقة', price: 'السعر', schedule: 'الدوام', other: 'أخرى',
        subscription: 'نوع الاشتراك', allP: 'الكل', periods: { HOUR: 'ساعة', DAY: 'يوم', WEEK: 'أسبوع', MONTH: 'شهر' },
        subHint: 'اختر نوع الاشتراك لتحديد نطاق السعر أو الترتيب حسبه.', from: 'من', to: 'إلى',
        rangeHelp: function (p) { return 'بالشيكل، على ' + p + '.'; },
        priceNames: { HOUR: 'السعر بالساعة', DAY: 'السعر اليومي', WEEK: 'السعر الأسبوعي', MONTH: 'السعر الشهري' },
        belowMin: '«إلى» أقل من «من».', invalid: 'اكتب مبلغًا بالشيكل أكبر من صفر',
        openNow: 'مفتوحة الآن', evening: 'مفتوحة مساءً', friday: 'مفتوحة يوم الجمعة',
        verified: 'المساحات الموثّقة فقط', students: 'أسعار للطلاب', womens: 'قاعة للنساء',
        show: function (n) { return n === 0 ? 'لا توجد نتائج' : arPlural(n, { one: 'عرض نتيجة واحدة', two: 'عرض نتيجتين', few: 'عرض ' + n + ' نتائج', many: 'عرض ' + n + ' نتيجة', other: 'عرض ' + n + ' نتيجة' }); },
        clearFilters: 'مسح الفلاتر', clear: 'مسح', close: 'إغلاق',
        noMatch: { title: 'لا توجد مساحات تطابق ما اخترت', text: 'جرّب إزالة بعض الفلاتر أو البحث باسم آخر.' },
        distance: function (km) { return 'على بعد ' + km + ' كم'; },
        // the active filters as a sentence — NEW patterns
        s: {
          inAreas: function (list) { return 'في ' + list; }, and: ' و', comma: '، ',
          openNow: 'مفتوحة الآن', evening: 'مفتوحة مساءً', friday: 'مفتوحة يوم الجمعة',
          per: { HOUR: 'بسعر بالساعة', DAY: 'بسعر يومي', WEEK: 'بسعر أسبوعي', MONTH: 'بسعر شهري' },
          between: function (a, b) { return 'بين ' + a + ' و' + b + ' ₪'; }, fromOnly: function (a) { return 'من ' + a + ' ₪'; }, toOnly: function (b) { return 'حتى ' + b + ' ₪'; },
          verified: 'موثّقة فقط', students: 'فيها أسعار للطلاب', womens: 'فيها قاعة للنساء',
          q: function (q) { return 'تطابق «' + q + '»'; }
        },
        chapterCount: function (n) { return arPlural(n, { one: 'مساحة واحدة', two: 'مساحتان', few: n + ' مساحات', many: n + ' مساحة', other: n + ' مساحة', zero: '' }); },
        oneList: 'كل المساحات' // NEW: the heading when the chapters dissolve
      },
      map: {
        label: 'خريطة المساحات', legend: 'دليل الخريطة', close: 'إغلاق', details: 'عرض التفاصيل',
        whole: 'القطاع كاملًا', // NEW
        zoomIn: 'تكبير', zoomOut: 'تصغير', north: 'الشمال', // NEW (north)
        cluster: function (n) { return arPlural(n, { two: 'مساحتان هنا، اضغط للتقريب', few: n + ' مساحات هنا، اضغط للتقريب', many: n + ' مساحة هنا، اضغط للتقريب', other: n + ' مساحة هنا، اضغط للتقريب', one: '', zero: '' }); }, // NEW
        pin: function (n, s) { return n + ' — ' + s; },
        you: 'موقعك', km: function (k) { return k + ' كم'; },
        style: 'خريطة مرسومة لهذا النموذج؛ في الموقع: خريطة بهذه الألوان محصورة في القطاع.' // NEW (mock-up note)
      },
      gov: { 'رفح': 'رفح' },
      // states
      st: {
        none: 'لا تتوفر حالة مباشرة', open: 'مفتوحة الآن', closed: 'مغلقة الآن',
        available: 'متاح', full: 'ممتلئ', closedNow: 'مغلق الآن',
        verified: 'موثّقة', byHoursShort: 'الحالة حسب ساعات العمل', // NEW (short)
        live: 'الحالة مباشرة الآن', byHours: 'حسب ساعات العمل؛ الحالة المباشرة تظهر للمساحات الموثّقة فقط',
        unset: 'لم تكتمل معلومات الحالة المباشرة لهذه المساحة بعد.', unverified: 'الحالة المباشرة تظهر للمساحات الموثّقة فقط'
      },
      // the composed sentence — NEW patterns
      sen: {
        available: function (t) { return 'فيها مكان الآن، ومفتوحة حتى ' + t; },
        full: function (t) { return 'ممتلئة الآن، ومفتوحة حتى ' + t; },
        liveClosed: 'مغلقة الآن',
        open: function (t) { return 'مفتوحة الآن حتى ' + t; },
        openAllDay: 'مفتوحة الآن على مدار الساعة',
        closedOpens: function (d, t) { return 'مغلقة الآن، وتفتح ' + d + ' ' + t; },
        closed: 'مغلقة الآن',
        todayRange: function (r) { return 'تعمل اليوم ' + r; },
        closedToday: 'مغلقة اليوم',
        inArea: function (a) { return 'في ' + a; },
        inAreaCap: function (a) { return 'في ' + a; },
        price: function (p, per) { return 'ويبدأ سعرها من ' + p + ' ' + per; },
        per: { HOUR: 'للساعة', DAY: 'لليوم', WEEK: 'للأسبوع', MONTH: 'للشهر' },
        noHours: 'ساعات عملها غير متوفرة.',
        sep: '، ', end: '.', today: 'اليوم', tomorrow: 'غدًا'
      },
      days: ['الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت'],
      // a space's page
      sp: {
        breadcrumb: 'مسار التنقّل', back: 'العودة إلى المساحات',
        save: function (n) { return 'حفظ ' + n + ' في المفضّلة'; }, remove: function (n) { return 'إزالة ' + n + ' من المفضّلة'; },
        statusContact: 'الحالة والتواصل', today: 'اليوم', todayRange: function (r) { return 'اليوم ' + r; },
        hoursCaption: 'ساعات العمل الأسبوعية', hours: 'ساعات العمل', closed: 'مغلقة', allDay: 'على مدار الساعة', noHours: 'ساعات العمل غير متوفرة',
        prices: 'الأسعار', amenities: 'المرافق', about: 'عن المساحة', location: 'الموقع', contacts: 'التواصل',
        lowest: 'الأسعار', // fact box heading
        displayOnly: 'للعرض فقط · الدفع في المساحة', students: 'للطلاب', subscription: 'نوع الاشتراك', price: 'السعر',
        noPrices: 'لم تُضف أسعار بعد', check: 'تأكّد من السعر مع المساحة قبل الذهاب.',
        noAmenities: 'لم تُضف مرافق بعد', // NEW
        noContacts: 'لم تُضف وسائل تواصل بعد', // NEW
        periods: { HOUR: 'ساعة', DAY: 'يوم', WEEK: 'أسبوع', MONTH: 'شهر' },
        directions: 'الاتجاهات', mapOf: function (n) { return 'موقع ' + n + ' على الخريطة'; },
        report: 'الإبلاغ عن معلومة غير صحيحة',
        inTheirWords: 'بكلمات المساحة', // NEW
        photoFrom: 'صورة من المساحة', // NEW
        photos: function (n) { return 'صور ' + n; },
        unverified: function (ago) { return 'جمع فريقنا هذه المعلومات، ولم تؤكّدها إدارة المساحة بعد · آخر تحديث للمعلومات ' + ago; },
        runIt: 'هل تدير هذه المساحة؟ تواصل معنا',
        dialogTitle: 'تواصل مع فريقنا', dialogText: 'أخبرنا أنك تدير هذه المساحة، وسنتواصل معك لتأكيد معلوماتها.',
        updated: { profile: 'آخر تحديث للمعلومات ', prices: 'آخر تحديث للأسعار ', hours: 'آخر تحديث لساعات العمل ', amenities: 'آخر تحديث للمرافق ', contacts: 'آخر تحديث للتواصل ' },
        stale: 'قد يكون تغيّر',
        announcement: 'إعلان', // terms.announcement
        demoAnnounce: 'تمديد ساعات العمل حتى 22:00 طوال الأسبوع', // illustrative (demo states)
        types: { WHATSAPP: 'واتساب', PHONE: 'اتصال', EMAIL: 'بريد', INSTAGRAM: 'إنستغرام', FACEBOOK: 'فيسبوك', TELEGRAM: 'تيليجرام', WEBSITE: 'الموقع الإلكتروني', OTHER: 'وسيلة أخرى' },
        bar: 'التواصل السريع', call: 'اتصال',
        notFound: 'لم نجد هذه المساحة', notFoundText: 'ربما أُزيلت من الدليل، أو أن الرابط غير صحيح.',
        signInFav: 'سجّل الدخول لحفظ المساحات في المفضّلة', signInFavText: 'تجد المساحات التي تحفظها في حسابك على أي جهاز.',
        signInReport: 'سجّل الدخول للإبلاغ عن معلومة', signInReportText: 'لتجد الردّ على بلاغك في «بلاغاتي».',
        register: 'إنشاء حساب', added: 'أُضيفت إلى المفضّلة', removed: 'أُزيلت من المفضّلة', undo: 'تراجع'
      },
      // auth
      auth: {
        title: 'تسجيل الدخول', description: 'سجّل الدخول لحفظ مساحاتك المفضّلة ومتابعة بلاغاتك، أو لإدارة مساحتك.',
        google: 'المتابعة باستخدام Google', // Google's own rendered button in production
        or: 'أو', email: 'البريد الإلكتروني', emailEx: 'name@example.com', password: 'كلمة المرور',
        submit: 'تسجيل الدخول', forgot: 'نسيت كلمة المرور؟', noAccount: 'ليس لديك حساب؟', create: 'إنشاء حساب',
        emailErr: 'تحقّق من كتابة البريد الإلكتروني، مثل name@example.com', passErr: 'أدخل كلمة المرور',
        mock: 'نموذج للعرض: لا يُرسَل شيء. يفتح «إعدادات حسابي» كأنك سجّلت الدخول.' // NEW (mock-up only)
      },
      // about
      about: {
        intro: 'مساحة دليل لمساحات العمل المشتركة في قطاع غزة. نجمع في مكان واحد ساعات عمل كل مساحة وأسعارها ومرافقها وطرق التواصل معها، ونعرض حالتها المباشرة إن كانت موثّقة، لتعرف قبل أن تخرج إن كانت مفتوحة وفيها مكان.',
        audience: 'لمن يعمل عن بعد، وللطلاب، ولكل من يحتاج مكانًا فيه كهرباء وإنترنت ليعمل أو يدرس.',
        source: 'من أين تأتي المعلومات؟',
        note: '«آخر تحديث» هو آخر مرة تأكّدنا فيها من المعلومة أو حدّثتها المساحة. كلما طالت المدة زاد احتمال أن تكون قد تغيّرت، فنعرض «قد يكون تغيّر» بجانب المعلومة القديمة.',
        wrong: 'إن وجدت معلومة خاطئة،', wrongLink: 'تواصل معنا', wrongEnd: '.',
        verified: 'مساحة موثّقة', verifiedSub: 'تديرها المساحة نفسها', verifiedText: 'تحدّث إدارة المساحة ساعاتها وأسعارها وإعلاناتها، وتظهر حالتها المباشرة تلقائيًا، ويمكنها ضبطها يدويًا لفترة قصيرة.',
        unverified: 'مساحة غير موثّقة', unverifiedSub: 'جمعها فريقنا', unverifiedText: 'جمع فريقنا معلوماتها من المساحة ومن صفحاتها العامة، ونراجعها دوريًا. لا تظهر لها حالة مباشرة.',
        status: 'ماذا تعني الحالة؟',
        available: 'فيها مكان الآن، وتُحدَّث الحالة تلقائيًا من حركة الحضور في المساحة.',
        full: 'مفتوحة، لكن لا أماكن شاغرة الآن.',
        closed: 'خارج ساعات العمل، أو مغلقة مؤقتًا بإعلان من المساحة.',
        none: 'المساحة غير موثّقة، أو لم تكتمل معلومات حالتها، فلا تظهر لها حالة لحظة بلحظة. راجع ساعات العمل أو تواصل معها.',
        byHours: 'مساحة غير موثّقة نعرف ساعات عملها: نحسب من ساعاتها إن كانت مفتوحة الآن بتوقيت غزة، دون أن نعرف إن كان فيها مكان.', // NEW
        byHoursTerm: 'مفتوحة الآن · مغلقة الآن', liveGroup: 'للمساحات الموثّقة', hoursGroup: 'لغير الموثّقة', // NEW
        contact: 'تواصل معنا', contactText: 'اكتب لنا بسؤال، أو عن بلاغ لم يصلك ردّه، أو عن خطأ في الموقع.',
        owners: 'لأصحاب المساحات',
        steps: ['تواصل معنا وأخبرنا باسم مساحتك وموقعها.', 'نتأكّد معك من المعلومات وننشئ حساب إدارة المساحة.', 'تصبح مساحتك موثّقة: تحدّث أسعارها وساعاتها بنفسك، وتظهر حالتها المباشرة تلقائيًا من تسجيل الحضور.']
      },
      // account
      acc: {
        title: 'إعدادات حسابي', profile: 'الملف الشخصي', name: 'الاسم', email: 'البريد الإلكتروني', emailNote: 'تسجّل الدخول بهذا البريد', save: 'حفظ', saved: 'حُفظت التغييرات',
        prefs: 'التفضيلات', prefsNote: 'تُطبَّق فورًا.', language: 'اللغة', languageHelper: 'تُحفظ في حسابك', theme: 'المظهر', themeHelper: 'على هذا الجهاز',
        themes: { light: 'فاتح', dark: 'داكن', system: 'حسب الجهاز' },
        signIn: 'تسجيل الدخول', signInNote: 'الطرق التي تدخل بها إلى حسابك.', google: 'Google', googleLine: function (e) { return 'تسجّل الدخول باستخدام Google · ' + e; }, linked: 'مربوط',
        password: 'كلمة المرور', passwordLine: 'تسجّل الدخول ببريدك وكلمة المرور', change: 'تغيير',
        current: 'كلمة المرور الحالية', newPass: 'كلمة المرور الجديدة', othersLine: 'تغيير كلمة المرور يسجّل خروجك من كل الأجهزة الأخرى', savePass: 'حفظ كلمة المرور', back: 'رجوع',
        nameErr: 'أدخل اسمك'
      },
      fav: {
        title: 'المفضّلة', description: 'المساحات التي حفظتها، بحالتها الآن.',
        count: function (n) { return arPlural(n, { zero: 'لا مساحات محفوظة', one: 'مساحة واحدة محفوظة', two: 'مساحتان محفوظتان', few: n + ' مساحات محفوظة', many: n + ' مساحة محفوظة', other: n + ' مساحة محفوظة' }); },
        gone: 'لم تعد هذه المساحة معروضة في الدليل', remove: 'إزالة', removeName: function (n) { return 'إزالة ' + n + ' من المفضّلة'; },
        removed: 'أُزيلت من المفضّلة', undo: 'تراجع',
        empty: 'لم تحفظ أي مساحة بعد', emptyText: 'اضغط على القلب في صفحة أي مساحة لتجدها هنا.',
        region: 'المساحات المحفوظة'
      },
      nf: { title: 'الصفحة غير موجودة', text: 'ربما تغيّر الرابط أو حُذفت الصفحة.', way: 'تصفّح الدليل من فصوله', home: 'العودة إلى الرئيسية' }, // way: NEW
      review: { button: 'مراجعة / Review', demo: 'حالات تجريبية / Demo states', demoNote: 'تشغيلها يجعل أربع مساحات موثّقة بحالات مباشرة، وإليفييت «متاح»، ولبرانش إعلان. الحقيقة أولًا: مطفأة افتراضيًا.' },
      ago: function (iso) { return agoFmt(iso, 'ar'); }
    },
    en: {
      title: function (p) { return p + ' · Masaha'; },
      skip: 'Skip to content', nav: 'Main navigation',
      links: { home: 'Home', spaces: 'Spaces', about: 'About Masaha', privacy: 'Privacy Policy' },
      signIn: 'Sign in', menu: 'Menu', closeMenu: 'Close menu',
      tagline: 'Masaha — a directory of coworking spaces in the Gaza Strip',
      contact: 'Contact us', browse: 'Browse spaces',
      langName: 'العربية', langLabel: 'التبديل إلى العربية',
      theme: { light: 'Dark theme', dark: 'Light theme' },
      account: { nav: 'My account', favorites: 'Favourites', reports: 'My reports', settings: 'Account settings', menu: function (n) { return 'Account menu: ' + n; }, signOut: 'Sign out' },
      footerContact: 'The Masaha team on WhatsApp and email',
      whatsapp: 'WhatsApp', email: 'Email',
      home: {
        title: 'Find a workspace in the Gaza Strip',
        lead: 'Opening hours, prices and live status of coworking spaces, in one place.',
        searchLabel: 'Search for a space', searchPh: 'Space name or area', searchSubmit: 'Search',
        gazaTime: 'Gaza time',
        openOf: function (n, m) { return 'Open now: ' + n + ' of ' + m + ' spaces'; },
        openNow: 'Open now', viewAll: 'View all',
        openingNext: 'Opening next',
        empty: { title: 'No spaces open right now', text: 'Spaces may be closed at this time. Browse all spaces to see their hours.', action: 'Browse all spaces' },
        areas: 'Browse by area', all: 'All areas', strip: 'The Gaza Strip',
        chapterOpen: function (n) { return n + ' open now'; },
        owners: { title: 'Do you run a coworking space?', text: 'Contact us to add your space and manage its hours and prices; its live status shows automatically from the check-ins.', action: 'Contact us' }
      },
      count: function (n) { return n + (n === 1 ? ' space' : ' spaces'); },
      dir: {
        title: 'Workspaces',
        all: function (n) { return n + (n === 1 ? ' space' : ' spaces') + ' in the Gaza Strip'; },
        matching: function (n) { return n + (n === 1 ? ' matching space' : ' matching spaces'); },
        searchLabel: 'Search for a space', searchPh: 'Space name or area',
        refine: 'Refine', refineTitle: 'Refine the list',
        sortLabel: 'Sort', sorts: { updated: 'Latest updates', name: 'By name', priceAsc: 'Monthly price: low to high', priceDesc: 'Monthly price: high to low', distance: 'By distance' },
        priceAsc: { HOUR: 'Hourly price: low to high', DAY: 'Daily price: low to high', WEEK: 'Weekly price: low to high', MONTH: 'Monthly price: low to high' },
        priceDesc: { HOUR: 'Hourly price: high to low', DAY: 'Daily price: high to low', WEEK: 'Weekly price: high to low', MONTH: 'Monthly price: high to low' },
        near: 'Nearest to me', locating: 'Finding your location…', sortedNear: 'Sorted by distance from your location.', approx: 'Distances are approximate, in a straight line.',
        stopNear: 'Stop sorting by distance', nearPrivacy: 'Your location is sent rounded, only to sort spaces by distance, and is never stored.',
        nearDemo: 'In this mock-up: an approximate point in Al-Rimal.',
        view: 'View', list: 'List', map: 'Map',
        filters: 'Filters', applied: 'Applied to the results right away',
        area: 'Area', price: 'Price', schedule: 'Hours', other: 'Other',
        subscription: 'Subscription', allP: 'All', periods: { HOUR: 'Hour', DAY: 'Day', WEEK: 'Week', MONTH: 'Month' },
        subHint: 'Choose a subscription to set a price range or to sort by price.', from: 'From', to: 'To',
        rangeHelp: function (p) { return 'In shekels, on the ' + p + '.'; },
        priceNames: { HOUR: 'hourly price', DAY: 'daily price', WEEK: 'weekly price', MONTH: 'monthly price' },
        belowMin: '“To” is below “From”.', invalid: 'Enter an amount in shekels, above zero',
        openNow: 'Open now', evening: 'Open in the evening', friday: 'Open on Friday',
        verified: 'Verified spaces only', students: 'Student prices', womens: 'Women’s hall',
        show: function (n) { return n === 0 ? 'No results' : 'Show ' + n + (n === 1 ? ' result' : ' results'); },
        clearFilters: 'Clear filters', clear: 'Clear', close: 'Close',
        noMatch: { title: 'No spaces match your choice', text: 'Try removing some filters, or searching for another name.' },
        distance: function (km) { return km + ' km away'; },
        s: {
          inAreas: function (list) { return 'in ' + list; }, and: ' and ', comma: ', ',
          openNow: 'open now', evening: 'open in the evening', friday: 'open on Friday',
          per: { HOUR: 'with an hourly price', DAY: 'with a daily price', WEEK: 'with a weekly price', MONTH: 'with a monthly price' },
          between: function (a, b) { return 'between ₪' + a + ' and ₪' + b; }, fromOnly: function (a) { return 'from ₪' + a; }, toOnly: function (b) { return 'up to ₪' + b; },
          verified: 'verified only', students: 'with student prices', womens: 'with a women’s hall',
          q: function (q) { return 'matching “' + q + '”'; }
        },
        chapterCount: function (n) { return n + (n === 1 ? ' space' : ' spaces'); },
        oneList: 'All spaces'
      },
      map: {
        label: 'Map of spaces', legend: 'Map legend', close: 'Close', details: 'View details',
        whole: 'The whole Strip', zoomIn: 'Zoom in', zoomOut: 'Zoom out', north: 'North',
        cluster: function (n) { return n + ' spaces here, press to zoom in'; },
        pin: function (n, s) { return n + ' — ' + s; },
        you: 'Your location', km: function (k) { return k + ' km'; },
        style: 'A map drawn for this mock-up; on the site: a map in these colours, bounded to the Strip.'
      },
      st: {
        none: 'No live status', open: 'Open now', closed: 'Closed now',
        available: 'Available', full: 'Full', closedNow: 'Closed now',
        verified: 'Verified', byHoursShort: 'Status by opening hours',
        live: 'Live right now', byHours: 'By its opening hours; live status is shown for verified spaces only',
        unset: 'This space’s live status isn’t set up yet.', unverified: 'Live status is shown for verified spaces only'
      },
      sen: {
        available: function (t) { return 'Has room now, open until ' + t; },
        full: function (t) { return 'Full right now, open until ' + t; },
        liveClosed: 'Closed now',
        open: function (t) { return 'Open now until ' + t; },
        openAllDay: 'Open now, around the clock',
        closedOpens: function (d, t) { return 'Closed now; opens ' + d + ' at ' + t; },
        closed: 'Closed now',
        todayRange: function (r) { return 'Open today ' + r; },
        closedToday: 'Closed today',
        inArea: function (a) { return 'in ' + a; },
        inAreaCap: function (a) { return 'In ' + a; },
        price: function (p, per) { return 'from ' + p + ' ' + per; },
        per: { HOUR: 'an hour', DAY: 'a day', WEEK: 'a week', MONTH: 'a month' },
        noHours: 'Its hours aren’t available.',
        sep: ', ', end: '.', today: 'today', tomorrow: 'tomorrow'
      },
      days: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
      sp: {
        breadcrumb: 'Breadcrumb', back: 'Back to spaces',
        save: function (n) { return 'Save ' + n + ' to favourites'; }, remove: function (n) { return 'Remove ' + n + ' from favourites'; },
        statusContact: 'Status & contact', today: 'Today', todayRange: function (r) { return 'Today ' + r; },
        hoursCaption: 'Weekly opening hours', hours: 'Opening hours', closed: 'Closed', allDay: 'Around the clock', noHours: 'Hours not available',
        prices: 'Prices', amenities: 'Amenities', about: 'About the space', location: 'Location', contacts: 'Contact',
        lowest: 'Prices',
        displayOnly: 'Display only · Pay at the space', students: 'For students', subscription: 'Subscription', price: 'Price',
        noPrices: 'No prices added yet', check: 'Check the price with the space before you go.',
        noAmenities: 'No amenities added yet', noContacts: 'No contacts added yet',
        periods: { HOUR: 'Hour', DAY: 'Day', WEEK: 'Week', MONTH: 'Month' },
        directions: 'Directions', mapOf: function (n) { return n + ' on the map'; },
        report: 'Report wrong information',
        inTheirWords: 'In the space’s words', photoFrom: 'Photo from the space',
        photos: function (n) { return 'Photos of ' + n; },
        unverified: function (ago) { return 'Our team collected this information; the space hasn’t confirmed it yet · Information updated ' + ago; },
        runIt: 'Do you run this space? Contact us',
        dialogTitle: 'Contact the Masaha team', dialogText: 'Tell us you run this space, and we’ll get in touch to confirm its information.',
        updated: { profile: 'Information updated ', prices: 'Prices updated ', hours: 'Hours updated ', amenities: 'Amenities updated ', contacts: 'Contacts updated ' },
        stale: 'May have changed',
        announcement: 'Announcement',
        demoAnnounce: 'Opening hours extended to 22:00 all week',
        types: { WHATSAPP: 'WhatsApp', PHONE: 'Call', EMAIL: 'Email', INSTAGRAM: 'Instagram', FACEBOOK: 'Facebook', TELEGRAM: 'Telegram', WEBSITE: 'Website', OTHER: 'Other' },
        bar: 'Quick contact', call: 'Call',
        notFound: 'We couldn’t find this space', notFoundText: 'It may have been removed from the directory, or the link is wrong.',
        signInFav: 'Sign in to save spaces to your favourites', signInFavText: 'You’ll find the spaces you save in your account, on any device.',
        signInReport: 'Sign in to report information', signInReportText: 'So you can find the reply to your report in “My reports”.',
        register: 'Create account', added: 'Added to favourites', removed: 'Removed from favourites', undo: 'Undo'
      },
      auth: {
        title: 'Sign in', description: 'Sign in to save your favourite spaces and follow your reports, or to run your space.',
        google: 'Continue with Google',
        or: 'or', email: 'Email', emailEx: 'name@example.com', password: 'Password',
        submit: 'Sign in', forgot: 'Forgot password?', noAccount: 'No account?', create: 'Create account',
        emailErr: 'Check the email address, for example name@example.com', passErr: 'Enter your password',
        mock: 'A mock-up: nothing is sent. It opens Account settings as if you had signed in.'
      },
      about: {
        intro: 'Masaha is a directory of coworking spaces in the Gaza Strip. It brings together each space’s hours, prices, amenities and contacts, and shows its live status if it’s verified, so you know before you leave whether it’s open and has room.',
        audience: 'For remote workers, students, and anyone who needs a place with power and internet to work or study.',
        source: 'Where does the information come from?',
        note: '“Updated” is the last time we confirmed the information or the space updated it. The longer ago, the more likely it has changed, so we show “May have changed” next to old information.',
        wrong: 'If you find wrong information,', wrongLink: 'contact us', wrongEnd: '.',
        verified: 'Verified space', verifiedSub: 'Managed by the space itself', verifiedText: 'The space updates its hours, prices and announcements; its live status shows automatically, and the space can set it by hand for a short time.',
        unverified: 'Unverified space', unverifiedSub: 'Collected by our team', unverifiedText: 'Our team collected its information from the space and its public pages, and reviews it periodically. It has no live status.',
        status: 'What does the status mean?',
        available: 'Has room now; the status updates itself from who comes and goes at the space.',
        full: 'Open, but no free places right now.',
        closed: 'Outside opening hours, or temporarily closed by an announcement from the space.',
        none: 'The space isn’t verified, or its status isn’t set up, so it shows no live status. Check its hours or contact it.',
        byHours: 'An unverified space whose hours we know: we work out from its hours whether it’s open now on Gaza’s clock, without knowing whether it has room.',
        byHoursTerm: 'Open now · Closed now', liveGroup: 'For verified spaces', hoursGroup: 'For unverified spaces',
        contact: 'Contact us', contactText: 'Write to us with a question, about a report that got no reply, or about a mistake on the site.',
        owners: 'For space owners',
        steps: ['Contact us with your space’s name and location.', 'We confirm the information with you and create the space’s management account.', 'Your space becomes verified: you keep its prices and hours yourself, and its live status shows automatically from check-ins.']
      },
      acc: {
        title: 'Account settings', profile: 'Profile', name: 'Name', email: 'Email', emailNote: 'You sign in with this email', save: 'Save', saved: 'Changes saved',
        prefs: 'Preferences', prefsNote: 'Applied right away.', language: 'Language', languageHelper: 'Saved to your account', theme: 'Theme', themeHelper: 'On this device',
        themes: { light: 'Light', dark: 'Dark', system: 'Device setting' },
        signIn: 'Signing in', signInNote: 'The ways you sign in to your account.', google: 'Google', googleLine: function (e) { return 'You sign in with Google · ' + e; }, linked: 'Linked',
        password: 'Password', passwordLine: 'You sign in with your email and password', change: 'Change',
        current: 'Current password', newPass: 'New password', othersLine: 'Changing your password signs you out on all your other devices', savePass: 'Save password', back: 'Back',
        nameErr: 'Enter your name'
      },
      fav: {
        title: 'Favourites', description: 'The spaces you saved, with their status now.',
        count: function (n) { return n + (n === 1 ? ' saved space' : ' saved spaces'); },
        gone: 'This space is no longer listed in the directory', remove: 'Remove', removeName: function (n) { return 'Remove ' + n + ' from favourites'; },
        removed: 'Removed from favourites', undo: 'Undo',
        empty: 'You haven’t saved any spaces yet', emptyText: 'Tap the heart on any space’s page to find it here.',
        region: 'Saved spaces'
      },
      nf: { title: 'Page not found', text: 'The link may have changed or the page was removed.', way: 'Find your way from the guide’s chapters', home: 'Back to home' },
      review: { button: 'مراجعة / Review', demo: 'حالات تجريبية / Demo states', demoNote: 'On: four spaces verified with live states, Elevate “Available”, an announcement on Branch. Truth first: off by default.' },
      ago: function (iso) { return agoFmt(iso, 'en'); }
    }
  };
  function agoFmt(iso, lang) {
    if (!iso) return '';
    var day = function (d) { var p = new Intl.DateTimeFormat('en-CA', { timeZone: 'Asia/Gaza' }).format(d).split('-').map(Number); return Date.UTC(p[0], p[1] - 1, p[2]); };
    var days = Math.round((day(new Date()) - day(new Date(iso))) / 86400000);
    return new Intl.RelativeTimeFormat(lang === 'ar' ? 'ar-u-nu-latn' : 'en', { numeric: 'auto' }).format(-days, 'day');
  }
})();
