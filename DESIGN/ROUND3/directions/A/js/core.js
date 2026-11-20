/* Direction A — the shared core: words (both languages), Gaza's clock, the status rules, the
   components every page uses (header, footer, row, plate, review panel), and the boot.
   Words are the product's catalogue verbatim (apps/web/src/shared/copy) unless marked NEW. */
(function () {
  'use strict';

  /* ───────────── Words ───────────── */
  var AR = 'ar', EN = 'en';
  var arPl = new Intl.PluralRules('ar');
  function arabicPlural(n, f) { return f[arPl.select(n)] || f.other; }
  function enPlural(n, f) { return n === 1 ? f.one : f.other; }

  var W = {
    ar: {
      title: function (p) { return p + ' · مساحة'; },
      skip: 'تخطَّ إلى المحتوى', navLabel: 'التنقّل الرئيسي',
      home: 'الرئيسية', spaces: 'المساحات', about: 'عن مساحة', privacy: 'سياسة الخصوصية', spacePage: 'صفحة المساحة',
      signIn: 'تسجيل الدخول', menu: 'القائمة', closeMenu: 'إغلاق القائمة',
      tagline: 'مساحة — دليل مساحات العمل المشتركة في قطاع غزة', contact: 'تواصل معنا', browseSpaces: 'تصفّح المساحات',
      acc: { nav: 'حسابي', favorites: 'المفضّلة', reports: 'بلاغاتي', settings: 'إعدادات حسابي' },
      prompt: {
        favorite: { title: 'سجّل الدخول لحفظ المساحات في المفضّلة', text: 'تجد المساحات التي تحفظها في حسابك على أي جهاز.' },
        report: { title: 'سجّل الدخول للإبلاغ عن معلومة', text: 'لتجد الردّ على بلاغك في «بلاغاتي».' },
        register: 'إنشاء حساب', signIn: 'تسجيل الدخول', close: 'إغلاق'
      },
      langName: 'English', switchTheme: { light: 'المظهر الداكن', dark: 'المظهر الفاتح' },
      homeT: {
        title: 'اعثر على مساحة عمل في قطاع غزة',
        lead: 'ساعات العمل والأسعار والحالة المباشرة لمساحات العمل المشتركة، في مكان واحد.',
        searchLabel: 'ابحث عن مساحة', placeholder: 'اسم المساحة أو المنطقة', submit: 'بحث',
        areas: 'تصفّح حسب المنطقة', allAreas: 'كل المناطق', strip: 'قطاع غزة',
        count: function (n) { return arabicPlural(n, { zero: n + ' مساحة', one: 'مساحة واحدة', two: 'مساحتان', few: n + ' مساحات', many: n + ' مساحة', other: n + ' مساحة' }); },
        ownersTitle: 'هل تدير مساحة عمل؟',
        ownersText: 'تواصل معنا لإضافة مساحتك، وإدارة ساعاتها وأسعارها، وتظهر حالتها المباشرة تلقائيًا من تسجيل الحضور.',
        openNow: 'مفتوحة الآن', nearest: 'المساحات الأقرب إليك', viewAll: 'عرض الكل',
        emptyTitle: 'لا توجد مساحات مفتوحة الآن', emptyText: 'قد تكون المساحات مغلقة في هذا الوقت. تصفّح كل المساحات لمعرفة ساعات عملها.', emptyAction: 'تصفّح كل المساحات'
      },
      /* NEW (proposed) — the board */
      board: {
        now: 'الآن في غزة',
        openCount: function (n) { return arabicPlural(n, { zero: 'لا مساحات مفتوحة الآن', one: 'مساحة واحدة مفتوحة الآن', two: 'مساحتان مفتوحتان الآن', few: n + ' مساحات مفتوحة الآن', many: n + ' مساحة مفتوحة الآن', other: n + ' مساحة مفتوحة الآن' }); },
        next: 'تفتح لاحقًا',
        opens: function (day, time) { return 'تفتح ' + day + ' ' + time; },
        today: 'اليوم', tomorrow: 'غدًا',
        cluster: function (n) { return arabicPlural(n, { zero: '', one: 'مساحة واحدة هنا، تكبير', two: 'مساحتان متقاربتان، تكبير', few: n + ' مساحات متقاربة، تكبير', many: n + ' مساحة متقاربة، تكبير', other: n + ' مساحة متقاربة، تكبير' }); },
        fromPrice: function (price, period) { return 'من ' + price + ' / ' + period; },
        priceCol: 'السعر', todayCol: 'اليوم', stateCol: 'الحالة', spaceCol: 'المساحة',
        studentsCol: 'للطلاب', generalCol: 'السعر'
      },
      dir: {
        title: 'مساحات العمل',
        all: function (n) { return arabicPlural(n, { zero: n + ' مساحة في قطاع غزة', one: 'مساحة واحدة في قطاع غزة', two: 'مساحتان في قطاع غزة', few: n + ' مساحات في قطاع غزة', many: n + ' مساحة في قطاع غزة', other: n + ' مساحة في قطاع غزة' }); },
        matching: function (n) { return arabicPlural(n, { zero: n + ' مساحة مطابقة', one: 'مساحة واحدة مطابقة', two: 'مساحتان مطابقتان', few: n + ' مساحات مطابقة', many: n + ' مساحة مطابقة', other: n + ' مساحة مطابقة' }); },
        searchLabel: 'ابحث عن مساحة', placeholder: 'اسم المساحة أو المنطقة',
        sort: 'الترتيب', sorts: { updated: 'الأحدث تحديثًا', name: 'حسب الاسم', distance: 'حسب المسافة' },
        asc: { HOUR: 'الأرخص بالساعة', DAY: 'الأرخص يوميًا', WEEK: 'الأرخص أسبوعيًا', MONTH: 'الأرخص شهريًا' },
        desc: { HOUR: 'الأغلى بالساعة', DAY: 'الأغلى يوميًا', WEEK: 'الأغلى أسبوعيًا', MONTH: 'الأغلى شهريًا' },
        results: 'النتائج',
        noMatchTitle: 'لا توجد مساحات تطابق ما اخترت', noMatchText: 'جرّب إزالة بعض الفلاتر أو البحث باسم آخر.', clearFilters: 'مسح الفلاتر',
        range: function (r, t) { return 'عرض ' + r + ' من ' + t; },
        f: {
          title: 'الفلاتر', description: 'تُطبَّق فورًا على النتائج',
          applied: function (n) { return arabicPlural(n, { zero: 'لا فلاتر مطبّقة', one: 'فلتر واحد مطبّق', two: 'فلتران مطبّقان', few: n + ' فلاتر مطبّقة', many: n + ' فلترًا مطبّقًا', other: n + ' فلتر مطبّق' }); },
          show: function (n) { return arabicPlural(n, { zero: 'لا توجد نتائج', one: 'عرض نتيجة واحدة', two: 'عرض نتيجتين', few: 'عرض ' + n + ' نتائج', many: 'عرض ' + n + ' نتيجة', other: 'عرض ' + n + ' نتيجة' }); },
          clear: 'مسح', close: 'إغلاق', schedule: 'الدوام', openNow: 'مفتوحة الآن', evening: 'مفتوحة مساءً', verified: 'المساحات الموثّقة فقط',
          price: 'السعر', subscription: 'نوع الاشتراك', all: 'الكل', periods: { HOUR: 'ساعة', DAY: 'يوم', WEEK: 'أسبوع', MONTH: 'شهر' },
          hint: 'اختر نوع الاشتراك لتحديد نطاق السعر أو الترتيب حسبه.', from: 'من', to: 'إلى', currency: '₪',
          rangeHelp: function (p) { return 'بالشيكل، على ' + p + '.'; },
          priceNames: { HOUR: 'السعر بالساعة', DAY: 'السعر اليومي', WEEK: 'السعر الأسبوعي', MONTH: 'السعر الشهري' },
          invalid: 'اكتب مبلغًا بالشيكل أكبر من صفر', belowMin: '«إلى» أقل من «من».',
          other: 'أخرى', students: 'أسعار للطلاب', friday: 'مفتوحة يوم الجمعة', womens: 'قاعة للنساء',
          area: 'المنطقة', allAreas: 'كل المناطق'
        },
        near: { button: 'الأقرب إليّ', locating: 'جارٍ تحديد موقعك…', privacy: 'يُرسَل موقعك مقرَّبًا لترتيب المساحات حسب المسافة فقط، ولا يُحفظ.', sorted: 'مرتبة حسب المسافة من موقعك.', approx: 'المسافات تقريبية بخط مستقيم.', stop: 'إيقاف الترتيب حسب المسافة' },
        view: { label: 'طريقة العرض', list: 'قائمة', map: 'خريطة' },
        map: { label: 'خريطة المساحات', legend: 'دليل الخريطة', you: 'موقعك', details: 'عرض التفاصيل', close: 'إغلاق', zoomIn: 'تكبير', zoomOut: 'تصغير', pin: function (n, s) { return n + ' — ' + s; } }
      },
      card: {
        verified: 'موثّقة', today: 'اليوم', closedToday: 'مغلقة اليوم', allDay: 'مفتوحة اليوم على مدار الساعة', noHours: 'ساعات العمل غير متوفرة',
        distance: function (km) { return 'على بعد ' + km + ' كم'; },
        periods: { HOUR: 'ساعة', DAY: 'يوم', WEEK: 'أسبوع', MONTH: 'شهر' }, noPrice: 'لم تُضف أسعار بعد'
      },
      st: { live: 'متاح', full: 'ممتلئ', closedLive: 'مغلق الآن', open: 'مفتوحة الآن', closedHours: 'مغلقة الآن', none: 'لا تتوفر حالة مباشرة' },
      page: {
        breadcrumb: 'مسار التنقّل',
        gallery: function (n) { return 'صور ' + n; }, allPhotos: function (c) { return 'عرض كل الصور (' + c + ')'; },
        photo: function (n, t, name) { return 'الصورة ' + n + ' من ' + t + ' — ' + name; }, viewPhoto: function (n) { return 'عرض الصورة ' + n; },
        prev: 'السابقة', next: 'التالية', close: 'إغلاق',
        unverified: function (ago) { return 'جمع فريقنا هذه المعلومات، ولم تؤكّدها إدارة المساحة بعد · آخر تحديث للمعلومات ' + ago; },
        claim: 'هل تدير هذه المساحة؟ تواصل معنا',
        dlgTitle: 'تواصل مع فريقنا', dlgText: 'أخبرنا أنك تدير هذه المساحة، وسنتواصل معك لتأكيد معلوماتها.',
        status: 'الحالة', live: 'الحالة مباشرة الآن', unverifiedLine: 'الحالة المباشرة تظهر للمساحات الموثّقة فقط',
        byHours: 'حسب ساعات العمل؛ الحالة المباشرة تظهر للمساحات الموثّقة فقط', unset: 'لم تكتمل معلومات الحالة المباشرة لهذه المساحة بعد.',
        sections: { prices: 'الأسعار', hours: 'ساعات العمل', amenities: 'المرافق', about: 'عن المساحة', location: 'الموقع', contacts: 'التواصل' },
        upd: {
          profile: function (a) { return 'آخر تحديث للمعلومات ' + a; }, prices: function (a) { return 'آخر تحديث للأسعار ' + a; },
          hours: function (a) { return 'آخر تحديث لساعات العمل ' + a; }, amenities: function (a) { return 'آخر تحديث للمرافق ' + a; },
          contacts: function (a) { return 'آخر تحديث للتواصل ' + a; }
        },
        stale: 'قد يكون تغيّر',
        displayOnly: 'للعرض فقط · الدفع في المساحة', students: 'للطلاب', periods: { HOUR: 'ساعة', DAY: 'يوم', WEEK: 'أسبوع', MONTH: 'شهر' }, noPrices: 'لم تُضف أسعار بعد',
        hoursCaption: 'ساعات العمل الأسبوعية', days: 'الأيام', hoursCol: 'الساعات', today: 'اليوم', closed: 'مغلقة', allDay: 'على مدار الساعة', noHours: 'ساعات العمل غير متوفرة',
        directions: 'الاتجاهات', onMap: function (n) { return 'موقع ' + n + ' على الخريطة'; },
        types: { WHATSAPP: 'واتساب', PHONE: 'اتصال', EMAIL: 'بريد', INSTAGRAM: 'إنستغرام', FACEBOOK: 'فيسبوك', TELEGRAM: 'تيليجرام', TIKTOK: 'تيك توك', X: 'X (تويتر)', LINKEDIN: 'لينكدإن', YOUTUBE: 'يوتيوب', WEBSITE: 'الموقع الإلكتروني', OTHER: 'وسيلة أخرى' },
        bar: 'التواصل السريع', whatsapp: 'واتساب', call: 'اتصال', announcement: 'إعلان', report: 'الإبلاغ عن معلومة غير صحيحة',
        notFoundTitle: 'لم نجد هذه المساحة', notFoundText: 'ربما أُزيلت من الدليل، أو أن الرابط غير صحيح.', back: 'العودة إلى المساحات'
      },
      demoAnnouncement: 'تمديد ساعات العمل حتى 22:00 طوال الأسبوع',
      dayNames: ['الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت'],
      fav: {
        save: function (n) { return 'حفظ ' + n + ' في المفضّلة'; }, remove: function (n) { return 'إزالة ' + n + ' من المفضّلة'; },
        added: 'أُضيفت إلى المفضّلة', removed: 'أُزيلت من المفضّلة', undo: 'تراجع',
        removedLeft: function (n) { return 'أُزيلت ' + n + ' من المفضّلة. لا يمكن حفظها من جديد ما دامت خارج الدليل.'; },
        title: 'المفضّلة', description: 'المساحات التي حفظتها، بحالتها الآن.',
        count: function (n) { return arabicPlural(n, { zero: 'لا مساحات محفوظة', one: 'مساحة واحدة محفوظة', two: 'مساحتان محفوظتان', few: n + ' مساحات محفوظة', many: n + ' مساحة محفوظة', other: n + ' مساحة محفوظة' }); },
        gone: 'لم تعد هذه المساحة معروضة في الدليل', removeBtn: 'إزالة',
        emptyTitle: 'لم تحفظ أي مساحة بعد', emptyText: 'اضغط على القلب في صفحة أي مساحة لتجدها هنا.', region: 'المساحات المحفوظة'
      },
      auth: {
        title: 'تسجيل الدخول', description: 'سجّل الدخول لحفظ مساحاتك المفضّلة ومتابعة بلاغاتك، أو لإدارة مساحتك.',
        submit: 'تسجيل الدخول', forgot: 'نسيت كلمة المرور؟', noAccount: 'ليس لديك حساب؟', create: 'إنشاء حساب',
        email: 'البريد الإلكتروني', password: 'كلمة المرور', or: 'أو', google: 'المتابعة باستخدام Google',
        emailInvalid: 'تحقّق من كتابة البريد الإلكتروني، مثل ⁦name@example.com⁩', passwordEmpty: 'أدخل كلمة المرور',
        show: 'إظهار كلمة المرور', hide: 'إخفاء كلمة المرور', failed: 'تعذّر تسجيل الدخول'
      },
      users: {
        menu: function (n) { return 'قائمة الحساب: ' + n; }, signOut: 'تسجيل الخروج',
        title: 'إعدادات حسابي', name: 'الاسم', email: 'البريد الإلكتروني', emailNote: 'تسجّل الدخول بهذا البريد', save: 'حفظ', saved: 'حُفظت التغييرات',
        prefsDescription: 'تُطبَّق فورًا.', language: 'اللغة', languageHelper: 'تُحفظ في حسابك', theme: 'المظهر', themeHelper: 'على هذا الجهاز',
        themes: { light: 'فاتح', dark: 'داكن', system: 'حسب الجهاز' },
        signInTitle: 'تسجيل الدخول', signInDescription: 'الطرق التي تدخل بها إلى حسابك.', password: 'كلمة المرور', passwordLine: 'تسجّل الدخول ببريدك وكلمة المرور', change: 'تغيير',
        current: 'كلمة المرور الحالية', newPw: 'كلمة المرور الجديدة', othersLine: 'تغيير كلمة المرور يسجّل خروجك من كل الأجهزة الأخرى', savePw: 'حفظ كلمة المرور', back: 'رجوع',
        pwSaved: 'تم تغيير كلمة المرور، وسُجّل خروجك من الأجهزة الأخرى',
        rulesLabel: 'شروط كلمة المرور', rules: ['8 أحرف على الأقل', 'حرف واحد على الأقل', 'رقم واحد على الأقل'], met: '— تحقّق', notMet: '— لم يتحقّق بعد',
        nameEmpty: 'أدخل اسمك'
      },
      aboutT: {
        intro: 'مساحة دليل لمساحات العمل المشتركة في قطاع غزة. نجمع في مكان واحد ساعات عمل كل مساحة وأسعارها ومرافقها وطرق التواصل معها، ونعرض حالتها المباشرة إن كانت موثّقة، لتعرف قبل أن تخرج إن كانت مفتوحة وفيها مكان.',
        audience: 'لمن يعمل عن بعد، وللطلاب، ولكل من يحتاج مكانًا فيه كهرباء وإنترنت ليعمل أو يدرس.',
        sourceTitle: 'من أين تأتي المعلومات؟',
        note: '«آخر تحديث» هو آخر مرة تأكّدنا فيها من المعلومة أو حدّثتها المساحة. كلما طالت المدة زاد احتمال أن تكون قد تغيّرت، فنعرض «قد يكون تغيّر» بجانب المعلومة القديمة.',
        wrong: 'إن وجدت معلومة خاطئة،', wrongLink: 'تواصل معنا', wrongEnd: '.',
        vTitle: 'مساحة موثّقة', vSub: 'تديرها المساحة نفسها', vText: 'تحدّث إدارة المساحة ساعاتها وأسعارها وإعلاناتها، وتظهر حالتها المباشرة تلقائيًا، ويمكنها ضبطها يدويًا لفترة قصيرة.',
        uTitle: 'مساحة غير موثّقة', uSub: 'جمعها فريقنا', uText: 'جمع فريقنا معلوماتها من المساحة ومن صفحاتها العامة، ونراجعها دوريًا. لا تظهر لها حالة مباشرة.',
        statusTitle: 'ماذا تعني الحالة؟',
        sAvailable: 'فيها مكان الآن، وتُحدَّث الحالة تلقائيًا من حركة الحضور في المساحة.', sFull: 'مفتوحة، لكن لا أماكن شاغرة الآن.',
        sClosed: 'خارج ساعات العمل، أو مغلقة مؤقتًا بإعلان من المساحة.',
        sNone: 'المساحة غير موثّقة، أو لم تكتمل معلومات حالتها، فلا تظهر لها حالة لحظة بلحظة. راجع ساعات العمل أو تواصل معها.',
        contactTitle: 'تواصل معنا', contactText: 'اكتب لنا بسؤال، أو عن بلاغ لم يصلك ردّه، أو عن خطأ في الموقع.',
        ownersTitle: 'لأصحاب المساحات',
        steps: ['تواصل معنا وأخبرنا باسم مساحتك وموقعها.', 'نتأكّد معك من المعلومات وننشئ حساب إدارة المساحة.', 'تصبح مساحتك موثّقة: تحدّث أسعارها وساعاتها بنفسك، وتظهر حالتها المباشرة تلقائيًا من تسجيل الحضور.'],
        whatsapp: 'واتساب', email: 'بريد'
      },
      nf: { title: 'الصفحة غير موجودة', description: 'ربما تغيّر الرابط أو حُذفت الصفحة.', home: 'العودة إلى الرئيسية' },
      review: {
        button: 'مراجعة / Review', title: 'صفحات النموذج', demo: 'حالات تجريبية / Demo states',
        demoNote: 'تجعل برانش وفوكس وجاردن ونمبر ون موثّقة بحالات مباشرة، وإليفييت متاحة، وتضيف إعلانًا لبرانش. للعرض فقط.',
        pages: { home: 'الرئيسية', list: 'المساحات — القائمة', filters: 'المساحات — الفلاتر مفتوحة', map: 'المساحات — الخريطة', branch: 'برانش هاب (3 صور)', elevate: 'إليفييت هاب (موثّقة)', jreas: 'جريس هاب (بلا ساعات)', other: 'بقية المساحات', login: 'تسجيل الدخول', about: 'عن مساحة', account: 'إعدادات حسابي', favorites: 'المفضّلة', nf: 'صفحة 404' },
        notBuilt: 'هذه الصفحة خارج نطاق النماذج.'
      }
    },
    en: {
      title: function (p) { return p + ' · Masaha'; },
      skip: 'Skip to content', navLabel: 'Main navigation',
      home: 'Home', spaces: 'Spaces', about: 'About Masaha', privacy: 'Privacy Policy', spacePage: 'Space',
      signIn: 'Sign in', menu: 'Menu', closeMenu: 'Close menu',
      tagline: 'Masaha — a directory of coworking spaces in the Gaza Strip', contact: 'Contact us', browseSpaces: 'Browse spaces',
      acc: { nav: 'My account', favorites: 'Favourites', reports: 'My reports', settings: 'Account settings' },
      prompt: {
        favorite: { title: 'Sign in to save spaces to your favourites', text: 'The spaces you save are in your account on any device.' },
        report: { title: 'Sign in to report information', text: 'So you’ll find the reply to your report in “My reports”.' },
        register: 'Create account', signIn: 'Sign in', close: 'Close'
      },
      langName: 'العربية', switchTheme: { light: 'Dark theme', dark: 'Light theme' },
      homeT: {
        title: 'Find a workspace in the Gaza Strip',
        lead: 'Opening hours, prices and live status of coworking spaces, in one place.',
        searchLabel: 'Search for a space', placeholder: 'Space name or area', submit: 'Search',
        areas: 'Browse by area', allAreas: 'All areas', strip: 'The Gaza Strip',
        count: function (n) { return enPlural(n, { one: n + ' space', other: n + ' spaces' }); },
        ownersTitle: 'Do you run a coworking space?',
        ownersText: 'Contact us to add your space and manage its hours and prices; its live status shows automatically from the check-ins.',
        openNow: 'Open now', nearest: 'Spaces nearest you', viewAll: 'View all',
        emptyTitle: 'No spaces open right now', emptyText: 'Spaces may be closed at this time. Browse all spaces to see their hours.', emptyAction: 'Browse all spaces'
      },
      board: {
        now: 'Now in Gaza',
        openCount: function (n) { return n === 0 ? 'No spaces open now' : enPlural(n, { one: n + ' space open now', other: n + ' spaces open now' }); },
        next: 'Opening next',
        opens: function (day, time) { return 'Opens ' + day + ' ' + time; },
        today: 'today', tomorrow: 'tomorrow',
        cluster: function (n) { return n + ' spaces close together, zoom in'; },
        fromPrice: function (price, period) { return 'From ' + price + ' / ' + period; },
        priceCol: 'Price', todayCol: 'Today', stateCol: 'Status', spaceCol: 'Space',
        studentsCol: 'For students', generalCol: 'Price'
      },
      dir: {
        title: 'Workspaces',
        all: function (n) { return enPlural(n, { one: n + ' space in the Gaza Strip', other: n + ' spaces in the Gaza Strip' }); },
        matching: function (n) { return enPlural(n, { one: n + ' matching space', other: n + ' matching spaces' }); },
        searchLabel: 'Search for a space', placeholder: 'Space name or area',
        sort: 'Sort', sorts: { updated: 'Latest updates', name: 'By name', distance: 'By distance' },
        asc: { HOUR: 'Hourly price: low to high', DAY: 'Daily price: low to high', WEEK: 'Weekly price: low to high', MONTH: 'Monthly price: low to high' },
        desc: { HOUR: 'Hourly price: high to low', DAY: 'Daily price: high to low', WEEK: 'Weekly price: high to low', MONTH: 'Monthly price: high to low' },
        results: 'Results',
        noMatchTitle: 'No spaces match your choice', noMatchText: 'Try removing some filters, or searching for another name.', clearFilters: 'Clear filters',
        range: function (r, t) { return 'Showing ' + r + ' of ' + t; },
        f: {
          title: 'Filters', description: 'Applied to the results right away',
          applied: function (n) { return enPlural(n, { one: n + ' filter applied', other: n + ' filters applied' }); },
          show: function (n) { return n === 0 ? 'No results' : enPlural(n, { one: 'Show ' + n + ' result', other: 'Show ' + n + ' results' }); },
          clear: 'Clear', close: 'Close', schedule: 'Hours', openNow: 'Open now', evening: 'Open in the evening', verified: 'Verified spaces only',
          price: 'Price', subscription: 'Subscription', all: 'All', periods: { HOUR: 'Hour', DAY: 'Day', WEEK: 'Week', MONTH: 'Month' },
          hint: 'Choose a subscription to set a price range or to sort by price.', from: 'From', to: 'To', currency: '₪',
          rangeHelp: function (p) { return 'In shekels, on the ' + p + '.'; },
          priceNames: { HOUR: 'hourly price', DAY: 'daily price', WEEK: 'weekly price', MONTH: 'monthly price' },
          invalid: 'Enter an amount in shekels, above zero', belowMin: '“To” is below “From”.',
          other: 'Other', students: 'Student prices', friday: 'Open on Friday', womens: 'Women’s hall',
          area: 'Area', allAreas: 'All areas'
        },
        near: { button: 'Nearest to me', locating: 'Finding your location…', privacy: 'Your location is sent rounded, only to sort spaces by distance, and is never stored.', sorted: 'Sorted by distance from your location.', approx: 'Distances are approximate, in a straight line.', stop: 'Stop sorting by distance' },
        view: { label: 'View', list: 'List', map: 'Map' },
        map: { label: 'Map of spaces', legend: 'Map legend', you: 'Your location', details: 'View details', close: 'Close', zoomIn: 'Zoom in', zoomOut: 'Zoom out', pin: function (n, s) { return n + ' — ' + s; } }
      },
      card: {
        verified: 'Verified', today: 'Today', closedToday: 'Closed today', allDay: 'Open around the clock today', noHours: 'Hours not available',
        distance: function (km) { return km + ' km away'; },
        periods: { HOUR: 'hour', DAY: 'day', WEEK: 'week', MONTH: 'month' }, noPrice: 'No prices added yet'
      },
      st: { live: 'Available', full: 'Full', closedLive: 'Closed now', open: 'Open now', closedHours: 'Closed now', none: 'No live status' },
      page: {
        breadcrumb: 'Breadcrumb',
        gallery: function (n) { return 'Photos of ' + n; }, allPhotos: function (c) { return 'View all photos (' + c + ')'; },
        photo: function (n, t, name) { return 'Photo ' + n + ' of ' + t + ' — ' + name; }, viewPhoto: function (n) { return 'View photo ' + n; },
        prev: 'Previous', next: 'Next', close: 'Close',
        unverified: function (ago) { return 'Our team collected this information; the space hasn’t confirmed it yet · Information updated ' + ago; },
        claim: 'Do you run this space? Contact us',
        dlgTitle: 'Contact the Masaha team', dlgText: 'Tell us you run this space, and we’ll get in touch to confirm its information.',
        status: 'Status', live: 'Live right now', unverifiedLine: 'Live status is shown for verified spaces only',
        byHours: 'By its opening hours; live status is shown for verified spaces only', unset: 'This space’s live status isn’t set up yet.',
        sections: { prices: 'Prices', hours: 'Opening hours', amenities: 'Amenities', about: 'About the space', location: 'Location', contacts: 'Contact' },
        upd: {
          profile: function (a) { return 'Information updated ' + a; }, prices: function (a) { return 'Prices updated ' + a; },
          hours: function (a) { return 'Hours updated ' + a; }, amenities: function (a) { return 'Amenities updated ' + a; },
          contacts: function (a) { return 'Contacts updated ' + a; }
        },
        stale: 'May have changed',
        displayOnly: 'Display only · Pay at the space', students: 'For students', periods: { HOUR: 'Hour', DAY: 'Day', WEEK: 'Week', MONTH: 'Month' }, noPrices: 'No prices added yet',
        hoursCaption: 'Weekly opening hours', days: 'Days', hoursCol: 'Hours', today: 'Today', closed: 'Closed', allDay: 'Around the clock', noHours: 'Hours not available',
        directions: 'Directions', onMap: function (n) { return n + ' on the map'; },
        types: { WHATSAPP: 'WhatsApp', PHONE: 'Call', EMAIL: 'Email', INSTAGRAM: 'Instagram', FACEBOOK: 'Facebook', TELEGRAM: 'Telegram', TIKTOK: 'TikTok', X: 'X (Twitter)', LINKEDIN: 'LinkedIn', YOUTUBE: 'YouTube', WEBSITE: 'Website', OTHER: 'Other' },
        bar: 'Quick contact', whatsapp: 'WhatsApp', call: 'Call', announcement: 'Announcement', report: 'Report wrong information',
        notFoundTitle: 'We couldn’t find this space', notFoundText: 'It may have been removed from the directory, or the link is wrong.', back: 'Back to spaces'
      },
      demoAnnouncement: 'Opening hours extended to 22:00 all week',
      dayNames: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
      fav: {
        save: function (n) { return 'Save ' + n + ' to favourites'; }, remove: function (n) { return 'Remove ' + n + ' from favourites'; },
        added: 'Added to favourites', removed: 'Removed from favourites', undo: 'Undo',
        removedLeft: function (n) { return n + ' removed from favourites. It can’t be saved again while it’s out of the directory.'; },
        title: 'Favourites', description: 'The spaces you saved, with their status now.',
        count: function (n) { return enPlural(n, { one: n + ' saved space', other: n + ' saved spaces' }); },
        gone: 'This space is no longer listed in the directory', removeBtn: 'Remove',
        emptyTitle: 'You haven’t saved any spaces yet', emptyText: 'Tap the heart on any space’s page to find it here.', region: 'Saved spaces'
      },
      auth: {
        title: 'Sign in', description: 'Sign in to save your favourite spaces and follow your reports, or to run your space.',
        submit: 'Sign in', forgot: 'Forgot password?', noAccount: 'No account?', create: 'Create account',
        email: 'Email', password: 'Password', or: 'or', google: 'Continue with Google',
        emailInvalid: 'Check the email address, for example ⁦name@example.com⁩', passwordEmpty: 'Enter your password',
        show: 'Show password', hide: 'Hide password', failed: 'Couldn’t sign in'
      },
      users: {
        menu: function (n) { return 'Account menu: ' + n; }, signOut: 'Sign out',
        title: 'Account settings', name: 'Name', email: 'Email', emailNote: 'You sign in with this email', save: 'Save', saved: 'Changes saved',
        prefsDescription: 'Applied right away.', language: 'Language', languageHelper: 'Saved to your account', theme: 'Theme', themeHelper: 'On this device',
        themes: { light: 'Light', dark: 'Dark', system: 'Device setting' },
        signInTitle: 'Signing in', signInDescription: 'The ways you sign in to your account.', password: 'Password', passwordLine: 'You sign in with your email and password', change: 'Change',
        current: 'Current password', newPw: 'New password', othersLine: 'Changing your password signs you out on all your other devices', savePw: 'Save password', back: 'Back',
        pwSaved: 'Password changed, and you were signed out on your other devices',
        rulesLabel: 'Password rules', rules: ['At least 8 characters', 'At least one letter', 'At least one number'], met: '— met', notMet: '— not met yet',
        nameEmpty: 'Enter your name'
      },
      aboutT: {
        intro: 'Masaha is a directory of coworking spaces in the Gaza Strip. It brings together each space’s hours, prices, amenities and contacts, and shows its live status if it’s verified, so you know before you leave whether it’s open and has room.',
        audience: 'For remote workers, students, and anyone who needs a place with power and internet to work or study.',
        sourceTitle: 'Where does the information come from?',
        note: '“Updated” is the last time we confirmed the information or the space updated it. The longer ago, the more likely it has changed, so we show “May have changed” next to old information.',
        wrong: 'If you find wrong information,', wrongLink: 'contact us', wrongEnd: '.',
        vTitle: 'Verified space', vSub: 'Managed by the space itself', vText: 'The space updates its hours, prices and announcements; its live status shows automatically, and the space can set it by hand for a short time.',
        uTitle: 'Unverified space', uSub: 'Collected by our team', uText: 'Our team collected its information from the space and its public pages, and reviews it periodically. It has no live status.',
        statusTitle: 'What does the status mean?',
        sAvailable: 'Has room now; the status updates itself from who comes and goes at the space.', sFull: 'Open, but no free places right now.',
        sClosed: 'Outside opening hours, or temporarily closed by an announcement from the space.',
        sNone: 'The space isn’t verified, or its status isn’t set up, so it shows no live status. Check its hours or contact it.',
        contactTitle: 'Contact us', contactText: 'Write to us with a question, about a report that got no reply, or about a mistake on the site.',
        ownersTitle: 'For space owners',
        steps: ['Contact us with your space’s name and location.', 'We confirm the information with you and create the space’s management account.', 'Your space becomes verified: you keep its prices and hours yourself, and its live status shows automatically from check-ins.'],
        whatsapp: 'WhatsApp', email: 'Email'
      },
      nf: { title: 'Page not found', description: 'The link may have changed or the page was removed.', home: 'Back to home' },
      review: {
        button: 'مراجعة / Review', title: 'Mock-up pages', demo: 'حالات تجريبية / Demo states',
        demoNote: 'Makes Branch, Focus, Garden and Number One verified with live states, Elevate available, and adds an announcement to Branch. Illustrative only.',
        pages: { home: 'Home', list: 'Spaces — list', filters: 'Spaces — filters open', map: 'Spaces — map', branch: 'Branch Hub (3 photos)', elevate: 'Elevate Hub (verified)', jreas: 'Jreas Hub (no hours)', other: 'The other spaces', login: 'Sign in', about: 'About Masaha', account: 'Account settings', favorites: 'Favourites', nf: '404 page' },
        notBuilt: 'This page is outside the mock-ups’ scope.'
      }
    }
  };

  /* ───────────── Preferences: language, theme, demo ───────────── */
  var Q = new URLSearchParams(location.search);
  function lsGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* storage blocked: the address keeps the choice */ } }
  var state = {
    lang: (Q.get('lang') === 'en' || Q.get('lang') === 'ar') ? Q.get('lang') : (lsGet('masaha-a-lang') || AR),
    themePref: (['light', 'dark', 'system'].indexOf(Q.get('theme')) >= 0) ? Q.get('theme') : (lsGet('masaha-a-theme') || 'system'),
    themeExplicit: !!Q.get('theme'),
    demo: Q.get('demo') === '1' ? true : (Q.get('demo') === '0' ? false : lsGet('masaha-a-demo') === '1')
  };
  if (state.lang !== AR && state.lang !== EN) state.lang = AR;
  var mq = window.matchMedia ? matchMedia('(prefers-color-scheme: dark)') : null;
  function resolvedTheme() { return state.themePref === 'system' ? (mq && mq.matches ? 'dark' : 'light') : state.themePref; }
  function applyPrefs() {
    var h = document.documentElement;
    h.lang = state.lang; h.dir = state.lang === AR ? 'rtl' : 'ltr';
    h.setAttribute('data-theme', resolvedTheme());
  }
  applyPrefs();
  if (mq && mq.addEventListener) mq.addEventListener('change', function () { if (state.themePref === 'system') applyPrefs(); });

  function syncAddress() {
    var q = new URLSearchParams(location.search);
    q.set('lang', state.lang);
    if (state.themePref !== 'system') q.set('theme', state.themePref); else q.delete('theme');
    if (state.demo) q.set('demo', '1'); else q.delete('demo');
    try { history.replaceState(null, '', location.pathname + '?' + q.toString() + location.hash); } catch (e) { /* file:// may refuse */ }
  }
  /* A link to another mock-up page carries the language, an explicit theme and the demo switch. */
  function href(page, params) {
    var q = new URLSearchParams(params || {});
    q.set('lang', state.lang);
    if (state.themePref !== 'system') q.set('theme', state.themePref);
    if (state.demo) q.set('demo', '1');
    var s = q.toString();
    return page + (s ? '?' + s : '');
  }

  /* ───────────── Gaza's clock ───────────── */
  var DOW = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
  var gazaFmt = new Intl.DateTimeFormat('en-US', { timeZone: 'Asia/Gaza', weekday: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' });
  function gaza(d) {
    d = d || new Date();
    var p = {}; gazaFmt.formatToParts(d).forEach(function (x) { p[x.type] = x.value; });
    var h = parseInt(p.hour, 10) % 24, m = parseInt(p.minute, 10);
    return { dow: DOW[p.weekday], minute: h * 60 + m, hhmm: pad(h) + ':' + pad(m), date: d };
  }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function clockOf(min) { return pad(Math.floor(min / 60)) + ':' + pad(min % 60); }

  /* ───────────── Data views (the demo switch) ───────────── */
  var DEMO = { 'branch-hub': 'AVAILABLE', 'focus-hub': 'FULL', 'garden-hub': 'AVAILABLE', 'number-one-hub': 'CLOSED', 'elevate-hub': 'AVAILABLE' };
  var SPACES = window.MD.spaces.map(function (s) { return s; });
  function view(s) {
    if (!state.demo || !DEMO[s.slug]) return s;
    var v = Object.assign({}, s, { isVerified: true, liveStatus: DEMO[s.slug] });
    if (s.slug === 'branch-hub') v.announcements = [{ demo: true, type: 'INFO' }];
    return v;
  }
  function bySlug(slug) { for (var i = 0; i < SPACES.length; i++) if (SPACES[i].slug === slug) return view(SPACES[i]); return null; }
  function allSpaces() { return SPACES.map(view); }

  /* ───────────── The status rules (ADR 0008) ───────────── */
  function openByHours(s, g) {
    if (!s.days) return null;
    var r = s.days[g.dow];
    if (!r) return false;
    return g.minute >= r.opensMinute && g.minute < r.closesMinute;
  }
  /* kind: live (متاح) · full · closedLive · open (by hours) · closedHours · none.
     A verified space's live state is closed outside its hours (the server derives it so). */
  function statusOf(s, g) {
    g = g || gaza();
    var o = openByHours(s, g);
    if (s.isVerified) {
      if (s.liveStatus) {
        if (s.liveStatus === 'CLOSED' || o === false) return { kind: 'closedLive', mark: 'closed', live: true, openNow: false };
        return { kind: s.liveStatus === 'FULL' ? 'full' : 'live', mark: s.liveStatus === 'FULL' ? 'full' : 'live', live: true, openNow: true };
      }
      return { kind: 'none', mark: 'none', verifiedUnset: true, openNow: o === true };
    }
    if (o === null) return { kind: 'none', mark: 'none', openNow: false };
    return o ? { kind: 'open', mark: 'hours', openNow: true } : { kind: 'closedHours', mark: 'closed', openNow: false };
  }
  function stateWord(st) { return t().st[st.kind]; }

  /* ───────────── Formatting ───────────── */
  function t() { return W[state.lang]; }
  function nm(s) { return state.lang === AR ? s.nameAr : s.nameEn; }
  function other(s) { return state.lang === AR ? s.nameEn : s.nameAr; }
  function L(o, k) { return o[k + (state.lang === AR ? 'Ar' : 'En')] || o[k + 'Ar'] || ''; }
  function gov(id) { var gs = window.MD.governorates; for (var i = 0; i < gs.length; i++) if (gs[i].id === id) return gs[i]; return null; }
  function areaLine(s) { var g = gov(s.govId); return L(s.area, 'name') + (g ? ' · ' + L(g, 'name') : ''); }
  function money(agorot) {
    var n = agorot / 100, v = (n % 1 ? n.toFixed(2) : String(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    return state.lang === AR ? v + ' ₪' : '₪' + v;
  }
  function ltr(x) { return '<bdi class="ltr">' + x + '</bdi>'; }
  function esc(x) { return String(x == null ? '' : x).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  var gazaDayFmt = new Intl.DateTimeFormat('en-CA', { timeZone: 'Asia/Gaza' });
  function gazaDay(d) { var p = gazaDayFmt.format(d).split('-').map(Number); return Date.UTC(p[0], p[1] - 1, p[2]); }
  function ago(iso) {
    var days = Math.round((gazaDay(new Date()) - gazaDay(new Date(iso))) / 86400000);
    return new Intl.RelativeTimeFormat(state.lang === AR ? 'ar-u-nu-latn' : 'en', { numeric: 'auto' }).format(-days, 'day');
  }
  var ORDER = ['HOUR', 'DAY', 'WEEK', 'MONTH'];
  function priceOf(s, period, audience) {
    var best = null;
    s.prices.forEach(function (p) { if (p.period === period && p.audience === (audience || 'GENERAL') && (best === null || p.amountAgorot < best)) best = p.amountAgorot; });
    return best;
  }
  /* The one price a row or a board shows: the chosen period's, else the day's, else the first period's. */
  function headlinePrice(s, period) {
    if (period) { var v = priceOf(s, period); return v == null ? null : { period: period, amount: v }; }
    var d = priceOf(s, 'DAY'); if (d != null) return { period: 'DAY', amount: d };
    for (var i = 0; i < ORDER.length; i++) { var x = priceOf(s, ORDER[i]); if (x != null) return { period: ORDER[i], amount: x }; }
    return null;
  }
  function todayHTML(s, g) {
    var c = t().card;
    if (!s.days) return '<span>' + c.noHours + '</span>';
    var r = s.days[(g || gaza()).dow];
    if (!r) return '<span>' + c.closedToday + '</span>';
    if (r.opensMinute === 0 && r.closesMinute === 1440) return '<span class="v">' + c.allDay + '</span>';
    return '<span>' + c.today + '</span> <span class="v">' + ltr(clockOf(r.opensMinute) + '–' + clockOf(r.closesMinute)) + '</span>';
  }
  /* When the space next opens, for the board after hours (NEW copy «تفتح غدًا 08:00»). */
  function nextOpening(s, g) {
    if (!s.days) return null;
    for (var k = 0; k < 8; k++) {
      var dow = (g.dow + k) % 7, r = s.days[dow];
      if (!r) continue;
      if (k === 0 && g.minute >= r.opensMinute) continue;
      var day = k === 0 ? t().board.today : k === 1 ? t().board.tomorrow : t().dayNames[dow];
      return { k: k, minute: r.opensMinute, text: t().board.opens(day, ltr(clockOf(r.opensMinute))) };
    }
    return null;
  }
  function km(a, b) {
    var R = 6371, toR = Math.PI / 180, dLat = (b.lat - a.lat) * toR, dLng = (b.lng - a.lng) * toR;
    var x = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(a.lat * toR) * Math.cos(b.lat * toR) * Math.sin(dLng / 2) * Math.sin(dLng / 2);
    return 2 * R * Math.atan2(Math.sqrt(x), Math.sqrt(1 - x));
  }
  /* The simulated point for «الأقرب إليّ»: a point in الرمال, rounded as the product rounds (≈100 m). */
  var NEAR_POINT = { lat: 31.5205, lng: 34.4425 };
  function lastUpdated(s) {
    var u = s.updatedAt, best = 0;
    Object.keys(u).forEach(function (k) { if (u[k]) best = Math.max(best, Date.parse(u[k])); });
    return best;
  }

  /* ───────────── Icons ───────────── */
  function icon(name, cls, label) {
    var nodes = window.ICON_NODES[name];
    if (!nodes) return '';
    var inner = nodes.map(function (n) {
      var a = Object.keys(n[1]).map(function (k) { return k + '="' + n[1][k] + '"'; }).join(' ');
      return '<' + n[0] + ' ' + a + '/>';
    }).join('');
    return '<svg class="i' + (cls ? ' ' + cls : '') + '" viewBox="0 0 24 24"' + (label ? ' role="img" aria-label="' + esc(label) + '"' : ' aria-hidden="true"') + '>' + inner + '</svg>';
  }
  function chevronFwd(cls) { return icon(state.lang === AR ? 'chevron-left' : 'chevron-right', cls); }

  /* ───────────── Components ───────────── */
  function plate(s, opts) {
    opts = opts || {};
    var p = s.photos && s.photos[0];
    if (!p || opts.noPhoto) return '<span class="plate initial" aria-hidden="true">' + esc(Array.from(nm(s))[0]) + '</span>';
    return '<span class="plate"><img src="../_shared/photos/' + p.card + '" alt="" loading="lazy" style="object-position:' + s.focus + '"></span>';
  }
  function stateHTML(st) { return '<span class="state"><span class="dot k-' + st.mark + '"></span>' + stateWord(st) + '</span>'; }

  /* A space as a row: bar · plate · name+area · state · today · price · save. */
  function row(s, o) {
    o = o || {};
    var g = o.g || gaza(), st = statusOf(s, g), c = t().card;
    var hp = headlinePrice(s, o.period);
    var priceCell = hp ? '<span class="v">' + ltr(money(hp.amount)) + '</span> <span>/ ' + c.periods[hp.period] + '</span>'
      : '<span class="none" aria-hidden="true">—</span><span class="sr">' + c.noPrice + '</span>';
    var dist = o.near ? '<span class="row__dist"> · ' + c.distance(ltr(km(o.near, s.location).toFixed(1))) + '</span>' : '';
    var ver = s.isVerified ? ' · <span class="ver">' + c.verified + '</span>' : '';
    var todayCell = o.next ? '<span class="v">' + o.next + '</span>' : todayHTML(s, g);
    var save = '';
    if (o.save !== false) {
      var saved = !!o.saved;
      save = '<button type="button" class="btn btn-icon heart row__save" data-heart="' + s.slug + '" aria-pressed="' + saved + '" aria-label="' + esc(saved ? t().fav.remove(nm(s)) : t().fav.save(nm(s))) + '">' + icon('heart') + '</button>';
    }
    return '<li class="row" data-row="' + s.slug + '">' +
      '<span class="bar k-' + st.mark + '"></span>' + plate(s, { noPhoto: o.noPhoto }) +
      '<div class="row__main"><a class="row__name" href="' + href('space.html', { slug: s.slug }) + '">' + esc(nm(s)) + '</a>' +
      '<span class="row__area">' + esc(areaLine(s)) + ver + dist + '</span></div>' +
      '<div class="row__facts"><span class="row__state">' + stateHTML(st) + '</span><span class="row__today">' + todayCell + '</span><span class="row__price">' + priceCell + '</span></div>' +
      save + '</li>';
  }
  function rowsHead(o) {
    var b = t().board;
    return '<div class="rows__head" aria-hidden="true"><span>' + b.spaceCol + '</span><span>' + b.stateCol + '</span><span>' + b.todayCol + '</span><span class="hp">' + b.priceCol + '</span><span class="hs"></span></div>';
  }

  function logoImg(dark) {
    return dark ? '<img src="../_shared/logo/masaha-logo-dark-berry.svg" alt="' + (state.lang === AR ? 'مساحة' : 'Masaha') + '" width="110" height="40">'
      : '<img class="l-light" src="../_shared/logo/masaha-logo-berry.svg" alt="' + (state.lang === AR ? 'مساحة' : 'Masaha') + '" width="110" height="40">' +
        '<img class="l-dark" src="../_shared/logo/masaha-logo-dark-berry.svg" alt="' + (state.lang === AR ? 'مساحة' : 'Masaha') + '" width="110" height="40">';
  }
  var USER = { name: 'سلمى الأغا', email: 'demo-user@example.com' };

  function header(active, signedIn) {
    var w = t();
    var links = [['home.html', w.home, 'home'], ['spaces.html', w.spaces, 'spaces'], ['about.html', w.about, 'about']];
    var nav = links.map(function (l) { return '<li><a href="' + href(l[0]) + '"' + (active === l[2] ? ' aria-current="page"' : '') + '>' + l[1] + '</a></li>'; }).join('');
    var dark = resolvedTheme() === 'dark';
    var themeBtn = '<button type="button" class="btn btn-icon hide-narrow" data-act="theme" aria-label="' + w.switchTheme[resolvedTheme()] + '" title="' + w.switchTheme[resolvedTheme()] + '">' + icon(dark ? 'sun' : 'moon') + '</button>';
    var langBtn = '<button type="button" class="btn btn-quiet" data-act="lang" lang="' + (state.lang === AR ? 'en' : 'ar') + '">' + icon('languages') + '<span>' + w.langName + '</span></button>';
    var account = signedIn
      ? '<div style="position:relative"><button type="button" class="user-btn" data-act="usermenu" aria-expanded="false" aria-haspopup="true" aria-label="' + esc(w.users.menu(USER.name)) + '"><span class="avatar" aria-hidden="true">س</span><span class="hide-narrow">' + USER.name + '</span>' + icon('chevron-down', 's16 hide-narrow') + '</button>' +
        '<div class="pop anim-in" id="usermenu" hidden style="inset-inline-end:0;top:calc(100% + 6px)"><div class="who"><b>' + USER.name + '</b><div class="t-sec c2">' + ltr(USER.email) + '</div></div><hr>' +
        '<a href="' + href('favorites.html') + '">' + w.acc.favorites + '</a><a href="#" data-act="notbuilt">' + w.acc.reports + '</a><a href="' + href('account.html') + '">' + w.acc.settings + '</a><hr>' +
        '<button type="button" class="item" data-act="signout">' + icon('log-out') + w.users.signOut + '</button></div></div>'
      : '<a class="btn btn-secondary hide-narrow" href="' + href('login.html') + '">' + w.signIn + '</a>';
    var menu = '<div class="hdr__menu" id="hdrmenu" data-open="false"><ul>' + links.map(function (l) { return '<li><a href="' + href(l[0]) + '"' + (active === l[2] ? ' aria-current="page"' : '') + '>' + l[1] + '</a></li>'; }).join('') + '</ul><hr>' +
      '<button type="button" class="item" data-act="theme">' + icon(dark ? 'sun' : 'moon') + w.switchTheme[resolvedTheme()] + '</button>' +
      (signedIn ? '' : '<a href="' + href('login.html') + '">' + icon('log-in', 'dir') + w.signIn + '</a>') + '</div>';
    return '<a class="skip" href="#main">' + w.skip + '</a>' +
      '<header class="hdr"><div class="wrap hdr__in">' +
      '<a class="logo" href="' + href('home.html') + '">' + logoImg(false) + '</a>' +
      '<nav aria-label="' + w.navLabel + '"><ul class="nav">' + nav + '</ul></nav>' +
      '<div class="hdr__end">' + langBtn + themeBtn + account +
      '<button type="button" class="btn btn-icon menu-btn" data-act="menu" aria-expanded="false" aria-controls="hdrmenu" aria-label="' + w.menu + '">' + icon('menu') + '</button>' +
      '</div></div>' + menu + '</header>';
  }

  function footer() {
    var w = t(), c = window.MD.contact;
    return '<footer class="ftr"><div class="ink"><div class="wrap">' +
      '<div class="ftr__top"><div class="ftr__brand"><a class="logo" href="' + href('home.html') + '">' + logoImg(true) + '</a><p class="t-sec c2">' + w.tagline + '</p></div>' +
      '<nav aria-label="' + w.tagline + '"><ul class="ftr__links">' +
      '<li><a href="' + href('spaces.html') + '">' + w.browseSpaces + '</a></li><li><a href="' + href('about.html') + '">' + w.about + '</a></li>' +
      '<li><a href="#" data-act="notbuilt">' + w.privacy + '</a></li><li><a href="' + href('about.html') + '#contact">' + w.contact + '</a></li></ul></nav></div>' +
      '<div class="ftr__contact"><span>' + w.contact + '</span>' +
      '<a href="https://wa.me/' + c.whatsapp.replace(/\D/g, '') + '"><span>' + w.aboutT.whatsapp + '</span>' + ltr(c.whatsapp) + '</a>' +
      '<a href="mailto:' + c.email + '">' + ltr(c.email) + '</a></div>' +
      '</div></div></footer>';
  }

  function reviewPanel() {
    var w = t().review, p = w.pages;
    var others = SPACES.filter(function (s) { return ['branch-hub', 'elevate-hub', 'jreas-hub'].indexOf(s.slug) < 0; })
      .map(function (s) { return '<a tabindex="-1" href="' + href('space.html', { slug: s.slug }) + '">' + esc(nm(s)) + '</a>'; }).join('');
    var L2 = [['home.html', null, p.home], ['spaces.html', null, p.list], ['spaces.html', { filters: 'open' }, p.filters], ['spaces.html', { view: 'map' }, p.map],
      ['space.html', { slug: 'branch-hub' }, p.branch], ['space.html', { slug: 'elevate-hub' }, p.elevate], ['space.html', { slug: 'jreas-hub' }, p.jreas],
      ['login.html', null, p.login], ['about.html', null, p.about], ['account.html', null, p.account], ['favorites.html', null, p.favorites], ['404.html', null, p.nf]];
    return '<aside class="review" data-open="false" aria-label="Review"><button type="button" class="review__toggle" data-act="review" tabindex="-1" aria-expanded="false">' + w.button + '</button>' +
      '<div class="review__panel" id="reviewpanel"><label><input type="checkbox" data-act="demo" tabindex="-1"' + (state.demo ? ' checked' : '') + '> ' + w.demo + '</label><p>' + w.demoNote + '</p>' +
      '<h2>' + w.title + '</h2>' + L2.map(function (l) { return '<a tabindex="-1" href="' + href(l[0], l[1]) + '">' + l[2] + '</a>'; }).join('') +
      '<h2>' + p.other + '</h2>' + others + '</div></aside>';
  }

  /* ───────────── Toasts and the sign-in prompt ───────────── */
  var toastTimer;
  function toast(text, action) {
    var old = document.querySelector('.toast'); if (old) old.remove();
    clearTimeout(toastTimer);
    var el = document.createElement('div');
    el.className = 'toast anim-in'; el.setAttribute('role', 'status');
    el.innerHTML = '<span>' + text + '</span>' + (action ? '<button type="button" class="btn btn-quiet">' + action.label + '</button>' : '');
    document.body.appendChild(el);
    if (action) el.querySelector('button').addEventListener('click', function () { action.run(); el.remove(); });
    toastTimer = setTimeout(function () { el.remove(); }, 6000);
  }
  function signInPrompt(kind, trigger) {
    var old = document.querySelector('.prompt'); if (old) old.remove();
    var w = t().prompt, k = w[kind];
    var el = document.createElement('div');
    el.className = 'prompt anim-in'; el.setAttribute('role', 'dialog'); el.setAttribute('aria-labelledby', 'prompt-t');
    el.innerHTML = '<button type="button" class="btn btn-icon x" aria-label="' + w.close + '">' + icon('x') + '</button>' +
      '<h2 class="t-row" id="prompt-t">' + k.title + '</h2><p class="t-sec c2">' + k.text + '</p>' +
      '<div class="acts"><a class="btn btn-primary" href="' + href('login.html') + '">' + w.signIn + '</a><a class="btn btn-secondary" href="' + href('login.html') + '">' + w.register + '</a></div>';
    document.body.appendChild(el);
    function close() { el.remove(); if (trigger) trigger.focus(); document.removeEventListener('keydown', onKey); }
    function onKey(e) { if (e.key === 'Escape') close(); }
    el.querySelector('.x').addEventListener('click', close);
    document.addEventListener('keydown', onKey);
    el.querySelector('a').focus();
  }

  /* ───────────── Boot and global actions ───────────── */
  var PAGE = null;
  function render(focusAct) {
    applyPrefs();
    var w = t();
    var title = PAGE.title ? PAGE.title() : '';
    document.title = w.title(title);
    var ae = document.activeElement, keep = focusAct || (ae && ae.getAttribute && ae.getAttribute('data-act'));
    document.body.innerHTML = header(PAGE.nav, PAGE.signedIn) + '<main id="main" tabindex="-1">' + PAGE.render() + '</main>' + footer() + reviewPanel();
    if (PAGE.mount) PAGE.mount();
    if (keep) { var el = document.querySelector('.hdr [data-act="' + keep + '"]:not(.hide-narrow), [data-act="' + keep + '"]'); var vis = document.querySelectorAll('[data-act="' + keep + '"]'); for (var i = 0; i < vis.length; i++) { if (vis[i].offsetParent) { vis[i].focus(); break; } } }
  }
  function setLang(l) { state.lang = l; lsSet('masaha-a-lang', l); syncAddress(); render('lang'); }
  function setTheme(th) { state.themePref = th; lsSet('masaha-a-theme', th); syncAddress(); render('theme'); }
  function setDemo(on) { state.demo = on; lsSet('masaha-a-demo', on ? '1' : '0'); syncAddress(); render(); var r = document.querySelector('.review'); if (r) { r.setAttribute('data-open', 'true'); setReviewTab(true); } }
  function setReviewTab(open) { document.querySelectorAll('.review__panel a, .review__panel input').forEach(function (a) { a.tabIndex = open ? 0 : -1; }); }

  document.addEventListener('click', function (e) {
    var a = e.target.closest('[data-act]');
    var menuOpen = document.getElementById('usermenu');
    if (menuOpen && !menuOpen.hidden && !e.target.closest('#usermenu') && !(a && a.getAttribute('data-act') === 'usermenu')) { menuOpen.hidden = true; var ub = document.querySelector('[data-act="usermenu"]'); if (ub) ub.setAttribute('aria-expanded', 'false'); }
    if (!a) return;
    var act = a.getAttribute('data-act');
    if (act === 'lang') setLang(state.lang === AR ? EN : AR);
    else if (act === 'theme') setTheme(resolvedTheme() === 'dark' ? 'light' : 'dark');
    else if (act === 'menu') { var m = document.getElementById('hdrmenu'), o = m.getAttribute('data-open') !== 'true'; m.setAttribute('data-open', String(o)); a.setAttribute('aria-expanded', String(o)); a.innerHTML = icon(o ? 'x' : 'menu'); a.setAttribute('aria-label', o ? t().closeMenu : t().menu); }
    else if (act === 'usermenu') { var um = document.getElementById('usermenu'); um.hidden = !um.hidden; a.setAttribute('aria-expanded', String(!um.hidden)); if (!um.hidden) um.querySelector('a').focus(); }
    else if (act === 'review') { var r = a.closest('.review'), op = r.getAttribute('data-open') !== 'true'; r.setAttribute('data-open', String(op)); a.setAttribute('aria-expanded', String(op)); setReviewTab(op); }
    else if (act === 'signout') { location.href = href('home.html'); }
    else if (act === 'notbuilt') { e.preventDefault(); toast(t().review.notBuilt); }
  });
  document.addEventListener('change', function (e) { if (e.target.matches('[data-act="demo"]')) setDemo(e.target.checked); });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var um = document.getElementById('usermenu'); if (um && !um.hidden) { um.hidden = true; var b = document.querySelector('[data-act="usermenu"]'); b.setAttribute('aria-expanded', 'false'); b.focus(); }
    var m = document.getElementById('hdrmenu'); if (m && m.getAttribute('data-open') === 'true') { var mb = document.querySelector('[data-act="menu"]'); mb.click(); mb.focus(); }
  });

  /* The board's minute tick: the clock's digits cross-fade; a row whose state changed swaps its marks. */
  var lastMinute = gaza().minute;
  setInterval(function () {
    var g = gaza();
    if (g.minute === lastMinute) return;
    lastMinute = g.minute;
    document.querySelectorAll('[data-clock]').forEach(function (el) {
      el.classList.add('fading');
      setTimeout(function () { el.textContent = g.hhmm; el.classList.remove('fading'); }, 150);
    });
    document.querySelectorAll('[data-row]').forEach(function (r) {
      var s = bySlug(r.getAttribute('data-row')); if (!s) return;
      var st = statusOf(s, g), bar = r.querySelector('.bar');
      if (bar && !bar.classList.contains('k-' + st.mark)) {
        bar.className = 'bar k-' + st.mark;
        var cell = r.querySelector('.row__state'); if (cell) cell.innerHTML = stateHTML(st);
        var word = r.querySelector('.stw'); if (word) word.textContent = stateWord(st);
      }
    });
    if (PAGE && PAGE.tick) PAGE.tick(g);
  }, 1000);

  window.A = {
    W: W, state: state, t: t, gaza: gaza, clockOf: clockOf, pad: pad, statusOf: statusOf, stateWord: stateWord, stateHTML: stateHTML, openByHours: openByHours,
    nm: nm, other: other, L: L, gov: gov, areaLine: areaLine, money: money, ltr: ltr, esc: esc, ago: ago, priceOf: priceOf, headlinePrice: headlinePrice,
    todayHTML: todayHTML, nextOpening: nextOpening, km: km, NEAR_POINT: NEAR_POINT, lastUpdated: lastUpdated, icon: icon, chevronFwd: chevronFwd,
    plate: plate, row: row, rowsHead: rowsHead, href: href, bySlug: bySlug, allSpaces: allSpaces, view: view, toast: toast, signInPrompt: signInPrompt,
    setLang: setLang, setTheme: setTheme, syncAddress: syncAddress, render: function () { render(); }, ORDER: ORDER, USER: USER, Q: Q, resolvedTheme: resolvedTheme,
    page: function (p) { PAGE = p; if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { render(); }); else render(); }
  };
})();
