import io
AR_MENU = """    receive: ({ amount }: { amount: string }) => `استلام ${amount}`,
    /** A customer's «⋯» (DI-39), named by them. */
    menu: {
      label: ({ name }: { name: string }) => `إجراءات أخرى: ${name}`,
      file: 'ملف الزبون',
      edit: 'تعديل البيانات',
      archive: 'أرشفة…',
      restore: 'استرجاع',
    },
"""
EN_MENU = """    receive: ({ amount }: { amount: string }) => `Receive ${amount}`,
    /** A customer's «⋯» (DI-39), named by them. */
    menu: {
      label: ({ name }: { name: string }) => `More actions: ${name}`,
      file: 'Customer file',
      edit: 'Edit details',
      archive: 'Archive…',
      restore: 'Restore',
    },
"""
AR = """  /** A customer's name and phone, edited (finding 123). */
  edit: {
    title: 'تعديل البيانات',
    name: 'الاسم',
    phone: 'رقم الجوال',
    optional: 'اختياري',
    phoneHelp: 'إليه يُرسل تذكير الدين على واتساب.',
    save: 'حفظ',
    nothingChanged: 'لم يتغيّر شيء',
    done: ({ name }: { name: string }) => `حُفظت بيانات ${name}`,
    failed: 'تعذّر حفظ البيانات',
  },
  /** The owner's archive of a customer, and its restore (DK-014, P9). */
  archive: {
    done: ({ name }: { name: string }) => `أُرشف ${name}`,
    undo: 'تراجع',
    restored: ({ name }: { name: string }) => `استُرجع ${name}`,
    title: ({ name }: { name: string }) => `أرشفة ${name}؟`,
    text: ({ amount }: { amount: string }) =>
      `عليه ${amount} غير مسدّدة. يبقى المبلغ في سجله، ويخرج من البحث ومن المكتب، ويبقى تحت «مؤرشف» في الزبائن.`,
    confirm: 'أرشفة رغم الدين',
    back: 'رجوع',
    doneOwing: ({ name, amount }: { name: string; amount: string }) =>
      `أُرشف ${name} · عليه ${amount}`,
    present: ({ name }: { name: string }) => `${name} حاضر الآن؛ سجّل خروجه قبل الأرشفة.`,
    failed: 'تعذّرت الأرشفة',
    restorePhoneTaken: 'رقمه مسجّل الآن لزبون آخر؛ لا يُسترجع قبل تغيير أحد الرقمين.',
    restoreFailed: 'تعذّر الاسترجاع',
  },
"""
EN = """  /** A customer's name and phone, edited (finding 123). */
  edit: {
    title: 'Edit details',
    name: 'Name',
    phone: 'Mobile number',
    optional: 'Optional',
    phoneHelp: 'Debt reminders go to this number on WhatsApp.',
    save: 'Save',
    nothingChanged: 'Nothing changed',
    done: ({ name }: { name: string }) => `${name}’s details saved`,
    failed: 'We couldn’t save the details',
  },
  /** The owner's archive of a customer, and its restore (DK-014, P9). */
  archive: {
    done: ({ name }: { name: string }) => `${name} archived`,
    undo: 'Undo',
    restored: ({ name }: { name: string }) => `${name} restored`,
    title: ({ name }: { name: string }) => `Archive ${name}?`,
    text: ({ amount }: { amount: string }) =>
      `They owe ${amount}. The amount stays on their record; they leave the search and the desk, and stay under “Archived” in Customers.`,
    confirm: 'Archive anyway',
    back: 'Back',
    doneOwing: ({ name, amount }: { name: string; amount: string }) =>
      `${name} archived · owes ${amount}`,
    present: ({ name }: { name: string }) => `${name} is here now; check them out before archiving.`,
    failed: 'We couldn’t archive them',
    restorePhoneTaken:
      'Their number now belongs to another customer; change one of them before restoring.',
    restoreFailed: 'We couldn’t restore them',
  },
"""
def rep(path, old, new):
    s = io.open(path, encoding='utf-8', newline='').read()
    assert s.count(old) == 1, (path, old[:40], s.count(old))
    io.open(path, 'w', encoding='utf-8', newline='').write(s.replace(old, new))
rep('arabic/desk.ts', "    receive: ({ amount }: { amount: string }) => `استلام ${amount}`,\n", AR_MENU)
rep('english/desk.ts', "    receive: ({ amount }: { amount: string }) => `Receive ${amount}`,\n", EN_MENU)
rep('arabic/desk.ts', "} satisfies Catalogue['desk'];", AR + "} satisfies Catalogue['desk'];")
rep('english/desk.ts', "} as const;", EN + "} as const;")
