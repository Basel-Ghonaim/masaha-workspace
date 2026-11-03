"""Commit 2's words: dataReports.report, site.signInPrompt."""
import sys

ROOT = r'C:\dev\masaha\app-lane-c\apps\web\src\shared\copy'


def edit(path, old, new):
    full = ROOT + '\\' + path
    with open(full, encoding='utf8', newline='') as f:
        text = f.read()
    if text.count(old) != 1:
        sys.exit(f'{path}: anchor found {text.count(old)} times')
    text = text.replace(old, new, 1)
    with open(full, 'w', encoding='utf8', newline='') as f:
        f.write(text)


edit('english\\dataReports.ts', """    none: 'No reports here',
    loadFailed: 'We couldn’t load your reports',
  },
} as const;""", """    none: 'No reports here',
    loadFailed: 'We couldn’t load your reports',
  },
  /** A space's page: «الإبلاغ عن معلومة غير صحيحة» and its dialog. */
  report: {
    trigger: 'Report wrong information',
    title: 'Report wrong information',
    /** Who reads it, by the space's verification (DI-45, U10). */
    toSpace: ({ name }: { name: string }) =>
      `Your report on ${name} goes to the space’s management; you’ll find their reply in “My reports”.`,
    toTeam: ({ name }: { name: string }) =>
      `Our team reviews your report on ${name}; you’ll find the reply in “My reports”.`,
    field: 'What’s wrong?',
    choose: 'Choose',
    fieldRequired: 'Choose what’s wrong',
    message: 'Details',
    optional: 'Optional',
    helper: 'For example: the monthly price is now ₪320',
    messageRequired: 'Write what is wrong under “Other”.',
    send: 'Send',
    back: 'Back',
    failed: 'We couldn’t send the report',
    lost: 'No answer came back. Try again — the report won’t be sent twice.',
    gone: 'This space is no longer in the directory.',
    /** The toast: where the reply lands (DI-47), or that one is already open (DI-48). */
    sentSpace: 'We sent your report to the space’s management. You’ll find their reply in “My reports”.',
    sentTeam: 'We sent your report to our team. You’ll find the reply in “My reports”.',
    repeated: 'You already reported this, and it is still in review.',
    showMine: 'View my reports',
  },
} as const;""")
edit('arabic\\dataReports.ts', """    none: 'لا توجد بلاغات هنا',
    loadFailed: 'تعذّر تحميل بلاغاتك',
  },
} satisfies Catalogue['dataReports'];""", """    none: 'لا توجد بلاغات هنا',
    loadFailed: 'تعذّر تحميل بلاغاتك',
  },
  report: {
    trigger: 'الإبلاغ عن معلومة غير صحيحة',
    title: 'الإبلاغ عن معلومة غير صحيحة',
    toSpace: ({ name }: { name: string }) =>
      `بلاغك عن ${name} يصل إلى إدارة المساحة، وتجد ردّها في «بلاغاتي».`,
    toTeam: ({ name }: { name: string }) =>
      `بلاغك عن ${name} يراجعه فريقنا، وتجد الردّ في «بلاغاتي».`,
    field: 'ما المعلومة غير الصحيحة؟',
    choose: 'اختر',
    fieldRequired: 'اختر نوع المعلومة',
    message: 'التفاصيل',
    optional: 'اختياري',
    helper: 'مثلًا: السعر الشهري أصبح 320 ₪',
    messageRequired: 'اكتب ما الخطأ في «أخرى».',
    send: 'إرسال',
    back: 'رجوع',
    failed: 'تعذّر إرسال البلاغ',
    lost: 'لم يصل الرد. أعد المحاولة — لن يُرسَل البلاغ مرتين.',
    gone: 'لم تعد هذه المساحة في الدليل.',
    sentSpace: 'أرسلنا بلاغك إلى إدارة المساحة. ستجد ردّها في «بلاغاتي».',
    sentTeam: 'أرسلنا بلاغك إلى فريقنا. ستجد الردّ في «بلاغاتي».',
    repeated: 'أرسلت بلاغًا عن هذا من قبل، وما زال قيد المراجعة.',
    showMine: 'عرض بلاغاتي',
  },
} satisfies Catalogue['dataReports'];""")

edit('english\\site.ts', """  account: {
    navigation: 'My account',
    reports: 'My reports',
  },
""", """  account: {
    navigation: 'My account',
    reports: 'My reports',
  },
  /** A guest's press of what needs an account: why to sign in, by the action (DI-60). */
  signInPrompt: {
    favorite: {
      title: 'Sign in to save spaces to your favourites',
      text: 'The spaces you save are in your account on any device.',
    },
    report: {
      title: 'Sign in to report information',
      text: 'So you’ll find the reply to your report in “My reports”.',
    },
    register: 'Create account',
    signIn: 'Sign in',
    close: 'Close',
  },
""")
edit('arabic\\site.ts', """  account: {
    navigation: 'حسابي',
    reports: 'بلاغاتي',
  },
""", """  account: {
    navigation: 'حسابي',
    reports: 'بلاغاتي',
  },
  signInPrompt: {
    favorite: {
      title: 'سجّل الدخول لحفظ المساحات في المفضّلة',
      text: 'تجد المساحات التي تحفظها في حسابك على أي جهاز.',
    },
    report: {
      title: 'سجّل الدخول للإبلاغ عن معلومة',
      text: 'لتجد الردّ على بلاغك في «بلاغاتي».',
    },
    register: 'إنشاء حساب',
    signIn: 'تسجيل الدخول',
    close: 'إغلاق',
  },
""")
print('ok')
