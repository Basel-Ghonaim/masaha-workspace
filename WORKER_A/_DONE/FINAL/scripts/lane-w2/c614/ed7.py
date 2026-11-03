def edit(p, pairs):
    s = open(p, encoding='utf8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)
B = 'C:/dev/masaha/app-lane-w2/apps/web/src/shared/copy/'
edit(B + 'english/lookups.ts', [
 ("""  /** The page's hint, under its title. */
  hint: 'Hidden: not shown in filters and forms. Spaces already using it stay as they are. The order here is the display order.',
  governorates: {
    /** The section's name. */
    title: 'Governorates and areas',""", """  governorates: {
    /** The section's name. */
    title: 'Governorates and areas',
    /** The tab's hint, under the tabs. */
    hint: 'Hidden: not shown in filters and forms. Spaces already using it stay as they are. The order here is the display order.',"""),
 ("""    title: 'Amenities',
    add: 'Add amenity',""", """    title: 'Amenities',
    /** The tab's hint, under the tabs. */
    hint: 'An inactive amenity is offered in no form; the spaces that have it keep it. The order here is the order shown.',
    add: 'Add amenity',"""),
 ("""    moveUp: ({ name }: { name: string }) => `Move up: ${name}`,
    moveDown: ({ name }: { name: string }) => `Move down: ${name}`,""", """    /** A row's arrows, named after it and where it stands in its list. */
    moveUp: ({ name, position, count }: { name: string; position: number; count: number }) =>
      `Move up: ${name} — ${String(position)} of ${String(count)}`,
    moveDown: ({ name, position, count }: { name: string; position: number; count: number }) =>
      `Move down: ${name} — ${String(position)} of ${String(count)}`,
    /** Said, politely, once a row has moved: where it now stands. */
    moved: ({ name, position, count }: { name: string; position: number; count: number }) =>
      `${name}: ${String(position)} of ${String(count)}`,"""),
 ("""    /** An amenity's switch, when editing: a new amenity is always active. */
    amenityActive: 'Active',
    amenityActiveHint: 'Inactive: not offered in forms; spaces that have it keep it.',
""", ""),
 ("""    /** The switch, when editing: a new governorate or area is always active. */
    active: 'Active',
    activeHint: 'Hidden: not shown in filters and forms.',
""", """    /** A row's place in a list of more than ten, typed when editing it. */
    position: 'Position',
    positionRange: ({ count }: { count: number }) => `From 1 to ${String(count)}`,
"""),
])
edit(B + 'arabic/lookups.ts', [
 ("""  hint: 'مخفية: لا تظهر في الفلاتر والنماذج. المساحات المرتبطة بها تبقى كما هي. الترتيب هنا هو ترتيب الظهور.',
  governorates: {
    title: 'المحافظات والمناطق',""", """  governorates: {
    title: 'المحافظات والمناطق',
    hint: 'مخفية: لا تظهر في الفلاتر والنماذج. المساحات المرتبطة بها تبقى كما هي. الترتيب هنا هو ترتيب الظهور.',"""),
 ("""    title: 'المرافق',
    add: 'إضافة مرفق',""", """    title: 'المرافق',
    hint: 'غير النشط لا يظهر في النماذج، وتحتفظ به المساحات التي لديها. الترتيب هنا هو ترتيب الظهور.',
    add: 'إضافة مرفق',"""),
 ("""    moveUp: ({ name }: { name: string }) => `تحريك لأعلى: ${name}`,
    moveDown: ({ name }: { name: string }) => `تحريك لأسفل: ${name}`,""", """    moveUp: ({ name, position, count }: { name: string; position: number; count: number }) =>
      `تحريك لأعلى: ${name} — ${String(position)} من ${String(count)}`,
    moveDown: ({ name, position, count }: { name: string; position: number; count: number }) =>
      `تحريك لأسفل: ${name} — ${String(position)} من ${String(count)}`,
    moved: ({ name, position, count }: { name: string; position: number; count: number }) =>
      `${name}: ${String(position)} من ${String(count)}`,"""),
 ("""    amenityActive: 'نشط',
    amenityActiveHint: 'غير نشط: لا يظهر في النماذج، وتحتفظ به المساحات التي لديها.',
""", ""),
 ("""    active: 'نشطة',
    activeHint: 'مخفية: لا تظهر في الفلاتر والنماذج.',
""", """    position: 'الترتيب',
    positionRange: ({ count }: { count: number }) => `من 1 إلى ${String(count)}`,
"""),
])
print('ok')
