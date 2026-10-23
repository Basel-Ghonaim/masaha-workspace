import io

ROOT = 'C:/dev/masaha/app/'


def sub(path, old, new, count=1):
    s = io.open(ROOT + path, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (path, old[:60], s.count(old))
    s = s.replace(old, new)
    io.open(ROOT + path, 'w', encoding='utf-8', newline='').write(s)


p = 'docs/features/directory.md'
s = io.open(ROOT + p, encoding='utf-8', newline='').read()
i = s.index('**The map on the web.**')
j = s.index('\n', i)
s = s[:j] + """

**Setting one's location on the map.** A denied or imprecise location offers «حدّد موقعي على الخريطة» beside «اختر منطقتك», and a point set by hand offers «تغيير الموقع»; each opens the map, every filter kept. A crosshair stands at the map's centre and the map takes the focus, its arrow keys panning it under the crosshair (a visually hidden line says so); the marks cannot be chosen, and near me's button, its line, «مركّز على موقعي» and the chosen space are hidden. The card «حدّد موقعك على الخريطة» says the point is sent rounded and never stored; «ثبّت الموقع هنا» places the centre, and a tap on the map places that point. The point is rounded as the device's is, held inside the Strip's box, and kept the same way, in memory, sorting the lists by distance («مرتبة حسب المسافة من الموقع الذي حدّدته على الخريطة.»), drawn as «موقعي (يدوي)»; «رجوع» restores the location before. Either returns the focus to «الأقرب إليّ».""" + s[j:]
k = s.index("- **The map's failure line points to the list")
m = s.index('\n', k)
s = s[:m] + """
- **A location can be set by hand at the map's centre, rounded and kept as the device's is; «رجوع» restores the one before** (U7 as built). *Why:* a denied or imprecise location still leaves a way to sort by distance, with the same privacy. 2026-10-22, #PRNUM.""" + s[m:]
io.open(ROOT + p, 'w', encoding='utf-8', newline='').write(s)
sub(p, "and the view's re-ask past 1,000 pins.\n", "and the view's re-ask past 1,000 pins.\n- #PRNUM — setting one's location by hand on the map: the crosshair, «ثبّت الموقع هنا», «رجوع», «تغيير الموقع».\n")
print('ok')
