"""The Strip panel drawing for the auth pages (the supervisor's, for discussion with the owner).

A dot grid clipped to the Strip, a bright coastline with faint sea lines, the 13 real spaces as berry dots, and a
lens over the sea that magnifies Gaza City's cluster. Data: round 3's approximate outline (not survey data) and the
live API's snapshot of 2026-11-14. Writes one SVG per theme into this folder.
Usage: python make_strip.py  (no arguments; prints the files written)
"""
import glob, json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = r"C:\dev\masaha\workspace\DESIGN\ROUND3\directions\_shared\data"

# The panel and the room the drawing leaves for the logo (top, start) and the title (bottom, start).
W, H = 960, 1080
TOP, BOTTOM = 150, 960          # the Strip's north and south ends
EAST = 880                      # the Strip's east edge

# Tokens (masaha: ink + berry, ADR 0019).
N50, N400, N500, N900, N950 = "#f7fbff", "#9fa6ad", "#767d84", "#1a1f25", "#0d1217"
S400, S500 = "#d27ed0", "#b55bb3"

def mix(a, b, t):
    pa = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    pb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(pa, pb))

THEMES = {
    "light-page": N900,                  # the panel beside a light page (today's ink)
    "dark-tinted": mix(N950, S500, 0.07),  # the panel beside a dark page: ink leaning to the berry
    "dark-plain": N950,                  # for comparison: the page's own ink
}

outline = json.load(open(os.path.join(DATA, "strip-outline.json"), encoding="utf-8"))["outline"][:-1]
COAST = outline[:10]                 # north-west corner along the sea to Rafah's shore
spaces = []
for f in sorted(glob.glob(os.path.join(DATA, "spaces", "*.json"))):
    d = json.load(open(f, encoding="utf-8"))
    d = d.get("data", d)
    spaces.append((d["slug"], d["location"]["lat"], d["location"]["lng"]))

lat0 = max(p[0] for p in outline)
lat1 = min(p[0] for p in outline)
lng1 = max(p[1] for p in outline)
K = (BOTTOM - TOP) / (lat0 - lat1)               # px per degree of latitude
KX = K * math.cos(math.radians((lat0 + lat1) / 2))  # px per degree of longitude

def xy(lat, lng):
    return (EAST - (lng1 - lng) * KX, TOP + (lat0 - lat) * K)

poly = [xy(*p) for p in outline]
coast = [xy(*p) for p in COAST]
dots = [(s, *xy(lat, lng)) for s, lat, lng in spaces]
city = [d for d in dots if d[2] < xy(31.50, 34.45)[1]]  # the nine north of 31.50
cx = sum(d[1] for d in city) / len(city)
cy = sum(d[2] for d in city) / len(city)

# The lens: over the sea, north-west of the city; it shows a window around the city, nudged toward the coast so
# the shore runs through it.
ZOOM = 4.0
LR = 150
LX, LY = 345, 345
WX, WY = cx - 16, cy          # the window's centre on the map

def lens(p):
    return (LX + (p[0] - WX) * ZOOM, LY + (p[1] - WY) * ZOOM)

def path(pts, close=False):
    s = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return s + (" Z" if close else "")

def offset(pts, d):
    """The coastline moved d px out to sea (along the normal of its overall direction)."""
    (x0, y0), (x1, y1) = pts[0], pts[-1]
    vx, vy = x1 - x0, y1 - y0
    n = math.hypot(vx, vy)
    nx, ny = vy / n, -vx / n          # pointing west / north-west for a NE→SW coast
    if nx > 0:
        nx, ny = -nx, -ny
    return [(x + nx * d, y + ny * d) for x, y in pts]

# The ring on the Strip round the city, and the line from the lens to it.
RING = max(math.hypot(d[1] - cx, d[2] - cy) for d in city) + 12
ang = math.atan2(cy - LY, cx - LX)
line_a = (LX + math.cos(ang) * LR, LY + math.sin(ang) * LR)
line_b = (cx - math.cos(ang) * RING, cy - math.sin(ang) * RING)

def svg(bg):
    sea = "".join(
        f'<path d="{path(offset(coast, d)[1:-1])}" fill="none" stroke="{N400}" stroke-opacity="{o}" '
        f'stroke-width="1" stroke-linecap="round" stroke-linejoin="round"/>'
        for d, o in ((18, .50), (36, .34), (54, .20))
    )
    berry = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{S400}" stroke="{bg}" stroke-width="1.5"/>'
        for _, x, y in dots
    )
    lpoly = [lens(p) for p in poly]
    lcoast = [lens(p) for p in coast]
    lberry = "".join(
        f'<circle cx="{lens((x, y))[0]:.1f}" cy="{lens((x, y))[1]:.1f}" r="7.5" fill="{S400}" '
        f'stroke="{bg}" stroke-width="2.5"/>'
        for _, x, y in city
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img"
  aria-label="رسم لقطاع غزة، عليه مساحات العمل في الدليل">
  <desc>رسم فنّي لا خريطة. النقاط من بيانات الدليل في 14 نوفمبر 2026.</desc>
  <defs>
    <pattern id="grid" width="7" height="7" patternUnits="userSpaceOnUse">
      <circle cx="3.5" cy="3.5" r="1.25" fill="{N400}" fill-opacity=".85"/>
    </pattern>
    <clipPath id="lens"><circle cx="{LX}" cy="{LY}" r="{LR - 0.75}"/></clipPath>
  </defs>
  <rect width="{W}" height="{H}" fill="{bg}"/>
  <g>{sea}</g>
  <path d="{path(poly, True)}" fill="url(#grid)"/>
  <path d="{path(coast)}" fill="none" stroke="{N50}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{RING:.1f}" fill="none" stroke="{S500}" stroke-width="1.2"/>
  <line x1="{line_a[0]:.1f}" y1="{line_a[1]:.1f}" x2="{line_b[0]:.1f}" y2="{line_b[1]:.1f}" stroke="{S500}" stroke-width="1.2"/>
  <g>{berry}</g>
  <circle cx="{LX}" cy="{LY}" r="{LR}" fill="{bg}"/>
  <g clip-path="url(#lens)">
    <path d="{path(lpoly, True)}" fill="url(#grid)"/>
    <path d="{path(lcoast)}" fill="none" stroke="{N50}" stroke-width="1.6" stroke-linejoin="round"/>
    {lberry}
  </g>
  <circle cx="{LX}" cy="{LY}" r="{LR}" fill="none" stroke="{S500}" stroke-width="1.5"/>
</svg>
'''

# The one the pages use: no background (the panel paints it), every colour a CSS custom property with the
# tokens as fallbacks, so one inline SVG follows the theme. --strip-panel is the panel's own colour: it rings the
# berry dots so overlapping ones stay countable, and fills the lens so the sea lines pass under it.
def themeable():
    t = svg("var(--strip-panel, %s)" % N900)
    t = t.replace(f'  <rect width="{W}" height="{H}" fill="var(--strip-panel, {N900})"/>' + chr(10), "")
    t = t.replace(f'fill="{N400}" fill-opacity=".85"', 'fill="var(--strip-grid, %s)" fill-opacity=".85"' % N400)
    t = t.replace(f'stroke="{N400}"', 'stroke="var(--strip-sea, %s)"' % N400)
    t = t.replace(f'stroke="{N50}"', 'stroke="var(--strip-coast, %s)"' % N50)
    t = t.replace(f'fill="{S400}"', 'fill="var(--strip-space, %s)"' % S400)
    t = t.replace(f'stroke="{S500}"', 'stroke="var(--strip-lens, %s)"' % S500)
    return t

open(os.path.join(HERE, "strip.svg"), "w", encoding="utf-8", newline=chr(10)).write(themeable())
print(os.path.join(HERE, "strip.svg"))

for name, bg in THEMES.items():
    out = os.path.join(HERE, f"strip-{name}.svg")
    open(out, "w", encoding="utf-8", newline="\n").write(svg(bg))
    print(out)
print("city", len(city), "ring", round(RING, 1), "lens window", round(WX), round(WY))
