import io

ROOT = 'C:/dev/masaha/app/apps/web/src/shared/copy/'


def sub(path, old, new, count=1):
    s = io.open(ROOT + path, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (path, old[:60], s.count(old))
    s = s.replace(old, new)
    io.open(ROOT + path, 'w', encoding='utf-8', newline='').write(s)


sub('english/directory.ts', """    chooseArea: 'Choose your area',
  },
} as const;""", """    chooseArea: 'Choose your area',
  },
  /** The switch between the list and the map, its label read but not shown. */
  view: {
    label: 'View',
    list: 'List',
    map: 'Map',
  },
  /** The map of the spaces: its pins, its legend, the selected space and its notices. */
  map: {
    /** The map's own name, as an application the keys pan. */
    label: 'Map of spaces',
    /** The section around it. */
    region: 'Map',
    /** A pin's name, as a button: the space's name, isolated, and its live status. */
    pin: ({ name, status }: { name: string; status: string }) => `${name} — ${status}`,
    legend: 'Map legend',
    centre: 'Centre on my location',
    /** The visitor's point on the map. */
    you: 'Your location',
    details: 'View details',
    close: 'Close',
    failed: 'The map didn’t load. Browse the spaces in the list.',
    /** Past 1,000 pins, until the map is asked within its view. */
    truncated: 'Showing the first 1,000 spaces; zoom in to see the rest.',
  },
} as const;""")

sub('arabic/directory.ts', """    chooseArea: 'اختر منطقتك',
  },
} satisfies Catalogue['directory'];""", """    chooseArea: 'اختر منطقتك',
  },
  view: {
    label: 'طريقة العرض',
    list: 'قائمة',
    map: 'خريطة',
  },
  map: {
    label: 'خريطة المساحات',
    region: 'الخريطة',
    pin: ({ name, status }: { name: string; status: string }) => `${name} — ${status}`,
    legend: 'دليل الخريطة',
    centre: 'مركّز على موقعي',
    you: 'موقعك',
    details: 'عرض التفاصيل',
    close: 'إغلاق',
    failed: 'لم تُحمَّل الخريطة. تصفّح المساحات في القائمة.',
    truncated: 'تظهر أول 1000 مساحة؛ قرّب الخريطة لترى ما بقي.',
  },
} satisfies Catalogue['directory'];""")
print('ok')
