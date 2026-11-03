"""Commit 1's words: dataReports.mine, site.account, users.account (links)."""
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


# dataReports: «بلاغاتي», a new top-level key after the toast.
edit('english\\dataReports.ts', """    inDecided: 'In “Reviewed”',
    show: 'Show',
  },
} as const;""", """    inDecided: 'In “Reviewed”',
    show: 'Show',
  },
  /** A signed-in user's «بلاغاتي» (screen 11): their own reports and the replies. */
  mine: {
    title: 'My reports',
    description: 'Reports you sent about wrong information, newest first.',
    chips: { label: 'Filter reports', all: 'All', open: 'In review', decided: 'Reviewed' },
    /** The list's region. */
    region: 'Reports',
    /** A report's line: its field group and the day it was sent. */
    meta: ({ field, day }: { field: string; day: string }) => `${field} · Sent ${day}`,
    /** A space that left the directory, its name shown as text (C7). */
    gone: 'This space is no longer listed in the directory',
    /** The toggle of a long message. */
    more: 'Show more',
    less: 'Show less',
    /** No report sent yet, with no filter (DI-53). */
    empty: {
      title: 'You haven’t sent any reports yet',
      text: 'If you see wrong information on a space’s page, report it from there.',
    },
    /** None under a chip. */
    none: 'No reports here',
    loadFailed: 'We couldn’t load your reports',
  },
} as const;""")
edit('arabic\\dataReports.ts', """    inDecided: 'في «تمت المراجعة»',
    show: 'عرض',
  },
} satisfies Catalogue['dataReports'];""", """    inDecided: 'في «تمت المراجعة»',
    show: 'عرض',
  },
  mine: {
    title: 'بلاغاتي',
    description: 'البلاغات التي أرسلتها عن معلومات خاطئة، الأحدث أولًا.',
    chips: { label: 'تصفية البلاغات', all: 'الكل', open: 'قيد المراجعة', decided: 'تمت المراجعة' },
    region: 'البلاغات',
    meta: ({ field, day }: { field: string; day: string }) => `${field} · أُرسل ${day}`,
    gone: 'لم تعد هذه المساحة معروضة في الدليل',
    more: 'عرض المزيد',
    less: 'عرض أقل',
    empty: {
      title: 'لم ترسل أي بلاغ بعد',
      text: 'إذا رأيت معلومة خاطئة في صفحة مساحة، أبلغنا منها.',
    },
    none: 'لا توجد بلاغات هنا',
    loadFailed: 'تعذّر تحميل بلاغاتك',
  },
} satisfies Catalogue['dataReports'];""")

# site.account: the account's navigation.
edit('english\\site.ts', """  browseSpaces: 'Browse spaces',
""", """  browseSpaces: 'Browse spaces',
  /** The account's pages: their navigation and its links. */
  account: {
    navigation: 'My account',
    reports: 'My reports',
  },
""")
edit('arabic\\site.ts', """  browseSpaces: 'تصفّح المساحات',
""", """  browseSpaces: 'تصفّح المساحات',
  account: {
    navigation: 'حسابي',
    reports: 'بلاغاتي',
  },
""")

# users.account.links: the account menu's links to the site's account pages (P4).
edit('english\\users.ts', """  dashboard: 'Dashboard',
  signOut: 'Sign out',
""", """  dashboard: 'Dashboard',
  /** The site's account menu: its links to the account's pages (P4). */
  account: {
    links: { reports: 'My reports' },
  },
  signOut: 'Sign out',
""")
edit('arabic\\users.ts', """  dashboard: 'لوحة التحكم',
  signOut: 'تسجيل الخروج',
""", """  dashboard: 'لوحة التحكم',
  account: {
    links: { reports: 'بلاغاتي' },
  },
  signOut: 'تسجيل الخروج',
""")
print('ok')
