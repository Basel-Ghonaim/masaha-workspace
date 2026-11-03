import io

ROOT = 'C:/dev/masaha/app/'


def sub(path, old, new, count=1):
    s = io.open(ROOT + path, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (path, old[:60], s.count(old))
    s = s.replace(old, new)
    io.open(ROOT + path, 'w', encoding='utf-8', newline='').write(s)


p = 'docs/frontend/architecture.md'
sub(p, "`shared/map` wraps React Leaflet and OpenStreetMap tiles (loaded lazily). Space markers and popups belong to the `directory` feature.\n",
    "`shared/map` wraps React Leaflet and OpenStreetMap tiles (loaded lazily). **What a mark means belongs to the feature that draws it (the `directory`'s pins); `shared/map` draws the marks its caller names by shape and tone** (2026-10-21, #PRNUM).\n")
sub(p, "with the coordinates' text helpers (`parseCoordinates`, `formatCoordinates`). It opens on the box it is given, with no pin until it holds a point. A click places the pin, a drag moves it, and each hands the point back. The pin is named by its coordinates and drawn from the tokens, never Leaflet's default image.\n",
    "with the coordinates' text helpers (`parseCoordinates`, `formatCoordinates`). It opens on the box it is given, with no pin until it holds a point. A click places the pin, a drag moves it, and each hands the point back. The pin is named by its coordinates and drawn from the tokens, never Leaflet's default image.\n"
    "- **Built:** `MarkerMap`, a generic map of many places. Each mark is a button named by its caller's label, pressed when selected, chosen by a click, Enter or Space, and drawn by shape and tone (`MapMark`), so a state is never told by colour alone; its name shows beside it on hover and always beside the selected one. It also draws the visitor's point, a picture named by its label; brings a point into view, above the centre when a bottom sheet covers the map's foot; hands back the box in view after each move when asked; and draws its caller's overlay over the map, where `MapMarkSample` draws a legend's marks. To pick a point it shows a crosshair at the centre, takes the marks out of the tab order, and places the point with a tap or its caller's button; the arrow keys pan the map, and the keys' line describes it.\n")
sub(p, "arrive only when a picker renders.", "arrive only when a map renders.")
sub(p, "if any tile of one of Leaflet's loads fails, whatever loaded before it, or the map's code cannot be fetched, a line under it says to enter the coordinates instead;",
    "if any tile of one of Leaflet's loads fails, whatever loaded before it, or the map's code cannot be fetched, a line under it says so in its caller's words (the picker's: to enter the coordinates instead);")

p = 'docs/frontend/design-system/foundation.md'
sub(p, """  leaflet.css         the map's stylesheet: Leaflet's own, then its frame, controls and pin on the
                      semantic tokens; imported by shared/map only""",
    """  leaflet.css         the map's stylesheet: Leaflet's own, then its frame, controls, pin, marks and
                      crosshair on the semantic tokens; imported by shared/map only""")
sub(p, "and the pin (`.map-pin`, on `primary`), all on the semantic tokens.",
    "the pin (`.map-pin`, on `primary`), the marks of a map of many places (`.map-mark`: a dot filled, barred, hollow or dashed, toned `success`, `warning` or `muted-foreground`, the selected one ringed on `primary`, never filled), the visitor's point (`.map-user`), the crosshair at the centre while a point is picked (`.map-crosshair`) and a mark's name beside it (`.map-tooltip`), all on the semantic tokens.")
print('ok')
