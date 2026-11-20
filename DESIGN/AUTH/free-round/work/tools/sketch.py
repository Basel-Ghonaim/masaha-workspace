"""Notebook's pen sketch of a real work desk: work/src/notebook-sketch.svg.
A rechargeable lantern (light when the power is out), a laptop with Masaha open, a glass of sage tea,
a phone charging from a power strip under the desk with every socket taken. Ink line, one berry accent."""
import pathlib
OUT = pathlib.Path(__file__).resolve().parents[1] / 'src' / 'notebook-sketch.svg'
W, H, DY = 560, 330, 236          # canvas and the desk-top line
o = []
def add(s): o.append(s)

add(f'<svg class="sketch" viewBox="0 0 {W} {H}" aria-hidden="true" focusable="false">')
add('<defs><filter id="pen" x="-3%" y="-3%" width="106%" height="106%"><feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" seed="11"/>'
    '<feDisplacementMap in="SourceGraphic" scale="2.2" xChannelSelector="R" yChannelSelector="G"/></filter>'
    '<radialGradient id="lantern-light"><stop offset="0" stop-color="#D27ED0" stop-opacity=".55"/><stop offset="1" stop-color="#D27ED0" stop-opacity="0"/></radialGradient></defs>')
add('<circle class="night" cx="64" cy="168" r="120" fill="url(#lantern-light)"/>')
add('<g filter="url(#pen)" class="pen">')

# desk: top edge drawn twice, slightly off, the way a pen goes over a line
add(f'<path d="M8,{DY} L552,{DY+1}"/><path class="thin" d="M14,{DY+5} L546,{DY+6}"/>')
add(f'<path class="thin" d="M40,{DY+6} L40,{H-6} M520,{DY+6} L520,{H-6}"/>')

# a lantern: what lights a desk when the power goes (ring handle, cap, glass with a bulb, base, light rays)
import math
add('<circle cx="64" cy="124" r="8"/>')
add('<path d="M50,142 L56,132 L72,132 L78,142 Z"/>')
add('<rect x="46" y="142" width="36" height="62" rx="5"/>')
add('<path class="thin" d="M52,146 L52,200 M76,146 L76,200"/>')
add('<circle class="bulb" cx="64" cy="168" r="9"/>')
add('<path class="thin" d="M60,182 L60,194 M68,182 L68,194 M58,194 L70,194"/>')
add('<rect x="40" y="204" width="48" height="32" rx="6"/>')
add('<rect class="berry-fill" x="56" y="214" width="16" height="9" rx="2"/>')
for ang in (160, 135, 45, 20):
    r1, r2 = 36, 48
    a_ = math.radians(ang)
    add(f'<path class="ray" d="M{64 + r1*math.cos(a_):.1f},{168 - r1*math.sin(a_):.1f} L{64 + r2*math.cos(a_):.1f},{168 - r2*math.sin(a_):.1f}"/>')

# laptop: screen and base, front view with a little perspective
add('<path d="M118,206 L124,62 Q125,52 136,52 L340,52 Q351,52 352,62 L358,206 Z"/>')
add('<path class="thin" d="M134,196 L139,70 L337,70 L342,196 Z"/>')
add('<path d="M98,206 L378,206 L394,232 Q395,236 390,236 L86,236 Q81,236 82,232 Z"/>')
add('<path class="thin" d="M114,214 L362,214 M110,222 L368,222 M206,230 L270,230"/>')
# on the screen: Masaha, with the ة and its two berry dots, and a few lines of a page
add('<rect class="paper-fill" x="226" y="96" width="24" height="20" rx="7"/><path d="M226,103 Q226,96 233,96 L243,96 Q250,96 250,103 L250,109 Q250,116 243,116 L233,116 Q226,116 226,109 Z"/>')
add('<rect class="berry-fill nostroke" x="228" y="84" width="8" height="7" rx="2"/><rect class="berry-fill nostroke" x="240" y="84" width="8" height="7" rx="2"/>')
add('<path class="thin" d="M176,136 L300,136 M188,148 L288,148 M200,172 L276,172 Q280,172 280,176 L280,182 Q280,186 276,186 L200,186 Q196,186 196,182 L196,176 Q196,172 200,172"/>')

# a glass of tea with sage, on a saucer
add('<path d="M412,236 Q440,242 468,236"/>')
add('<path d="M420,166 C418,184 428,192 428,202 C428,214 420,222 424,232 L456,232 C460,222 452,214 452,202 C452,192 462,184 460,166 Z"/>')
add('<path class="thin" d="M424,190 L456,190"/>')
add('<path class="hatch" d="M426,196 L454,196 M427,202 L453,202 M427,208 L453,208 M426,214 L454,214 M425,220 L455,220 M425,226 L455,226"/>')
add('<path d="M448,170 C452,150 460,134 470,122"/>')
add('<path d="M462,138 C474,130 482,132 486,138 C478,144 468,144 462,138 Z"/><path d="M456,152 C446,142 440,144 436,150 C444,156 452,156 456,152 Z"/><path d="M466,126 C470,112 478,110 484,112 C482,122 474,128 466,126 Z"/>')
add('<path class="thin steam" d="M432,156 q-6,-10 0,-18 q6,-8 0,-18 M444,152 q-5,-8 0,-15"/>')

# a phone lying on the desk, charging; the cable goes over the edge to the strip
add('<path d="M488,236 L492,222 L540,222 L536,236 Z"/>')
add('<path class="thin" d="M536,230 C552,232 556,250 548,262 C536,276 452,266 441,280"/>')
add('<path class="thin" d="M88,232 C100,262 150,262 161,284"/>')
add('<path class="thin" d="M380,236 C392,258 330,262 321,284"/>')
# power strip under the desk, every socket taken
add('<path d="M140,288 L470,288 Q480,288 480,298 L480,308 Q480,318 470,318 L140,318 Q130,318 130,308 L130,298 Q130,288 140,288 Z"/>')
for i, x in enumerate((150, 230, 310, 390, 430)):
    add(f'<rect class="paper-fill" x="{x}" y="280" width="22" height="20" rx="5"/>')
# the two other sockets feed the neighbours, off the edge of the page
add('<path class="thin" d="M241,280 C236,262 180,270 120,262 C80,256 40,270 2,262"/>')
add('<path class="thin" d="M401,280 C404,264 470,262 500,254 C524,248 540,256 558,250"/>')
add('<circle class="berry-fill nostroke" cx="466" cy="303" r="4"/>')
add('</g></svg>')

OUT.write_text('\n'.join(o), encoding='utf-8')
print(f'wrote {OUT}')
