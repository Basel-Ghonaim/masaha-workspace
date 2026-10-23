import io

ROOT = 'C:/dev/masaha/app/'


def sub(path, old, new, count=1):
    s = io.open(ROOT + path, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (path, old[:60], s.count(old))
    s = s.replace(old, new)
    io.open(ROOT + path, 'w', encoding='utf-8', newline='').write(s)


p = 'docs/features/directory.md'
s = io.open(ROOT + p, encoding='utf-8', newline='').read()
# What it does: the site's map.
i = s.index('- On the site\'s «المساحات», lists the spaces')
j = s.index('\n', i)
s = s[:j] + "\n- On the site's «المساحات», shows the same spaces on a map, «قائمة | خريطة», each a pin whose live state is a shape as well as a colour, the chosen one's card leading to its page." + s[j:]
io.open(ROOT + p, 'w', encoding='utf-8', newline='').write(s)

sub(p, "the privacy line shows only while a location is asked or sent. The state line is one live region",
    "the privacy line shows only while a location is asked or sent. The state line is one live region")
# Behaviour: the map on the web, after near me's paragraph.
s = io.open(ROOT + p, encoding='utf-8', newline='').read()
i = s.index('**Near me on the web.**')
j = s.index('\n', i)
s = s[:j] + """

**The map on the web.** «قائمة | خريطة» beside the page's heading switches the view at every width, kept in the address (`view=map`) with every filter. The map asks `GET /map/spaces` with the list's filters, the whole set, and draws each space as a pin: available filled green, full a warning dot with a bar across it, closed hollow, no live status dashed and muted, so a state is never told by colour alone; the legend in the map names each mark. A pin is a button named by the space and its state, chosen by a click, Enter or Space; its name shows beside it. On the map the filters open in the sheet at every width, with no order; near me and its state line are the list's, the visitor's point drawn on the map, with «مركّز على موقعي». The chosen space is a card over the map's foot from 768 px, and a bottom sheet below it that is not modal: it takes no focus, the map behind it still pans, and a tap on the map leaves it open; the chosen pin is brought into view above it. Each shows the name, the area, the status, «موثّقة» and today's hours, with «عرض التفاصيل» to the space's page; closing it hands the focus back to the pin. A change of filter clears the choice. Past 1,000 pins the map says «تظهر أول 1000 مساحة؛ قرّب الخريطة لترى ما بقي.», and once it has moved and paused 400 ms it asks again within the box in view, whose answer replaces the marks. Loading, a failure (with «إعادة المحاولة»), an empty directory and no match (with «مسح الفلاتر») are each said over or above the map; when the map cannot load, «لم تُحمَّل الخريطة. تصفّح المساحات في القائمة.»""" + s[j:]
# Web decisions: after the imprecise one.
k = s.index("- **An imprecise position is said as")
m = s.index('\n', k)
s = s[:m] + """
- **What a pin means is the directory's; `shared/map` draws the marks it is named by shape and tone** (S12). *Why:* Leaflet stays in `shared/map`, and a map of many marks survives outside Masaha. 2026-10-21, #PRNUM.
- **Each live state is a pin's shape as well as its colour, and a space with no live status, verified or not, is one dashed mark** (U6, design issue 21). *Why:* colour alone fails the colour-blind and the sun; the card says the same «لا تتوفر حالة مباشرة» for both. 2026-10-21, #PRNUM.
- **The phone's chosen space is a sheet that is not modal** (design issue 22). *Why:* a modal sheet would trap the map behind it (U6). 2026-10-21, #PRNUM.
- **The map's failure line points to the list, and past 1,000 pins the map says so and asks within its view** (design issues 19, 20). 2026-10-21, #PRNUM.""" + s[m:]
io.open(ROOT + p, 'w', encoding='utf-8', newline='').write(s)

sub(p, "entry `index.ts` (`DirectoryList`, `DirectorySlots`), mounted by `pages/site/public/directory/`;",
    "entry `index.ts` (`DirectoryView`, `ViewSwitch`, `DirectorySlots`), mounted by `pages/site/public/directory/`;")
sub(p, "near me's store and hooks in `hooks/near/`,",
    "near me's store and hooks in `hooks/near/`, the map's in `hooks/map/` (with `services/pinMark.ts` and `boundsText.ts`), the view's in `hooks/view/`,")
sub(p, "the near-me button and state line in `components/near/`.",
    "the near-me button and state line in `components/near/`, the map, its legend and the chosen space in `components/map/`, the view switch in `components/view/`.")
sub(p, "- #PRNUM — carried from #103:", "- #PRNUM — the map: «قائمة | خريطة», the pins by state, the legend, the chosen space's card and sheet, and the view's re-ask past 1,000 pins.\n- #PRNUM — carried from #103:")

p = 'docs/architecture/findings/46-the-deployments-headers-must-let-the-maps-tiles-load.md'
sub(p, "[Finding 33](33-the-deployments-headers-must-let-googles-sign-in-work.md) records the same for Google's sign-in.\n",
    "[Finding 33](33-the-deployments-headers-must-let-googles-sign-in-work.md) records the same for Google's sign-in.\n\n**2026-10-21, #PRNUM:** the site's Directory now shows the same tiles on its map («خريطة»), so a blank map would reach every visitor, not only the admin.\n")
print('ok')
