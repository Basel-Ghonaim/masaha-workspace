"""Draw Berry's long shared table as SVG: work/src/berry-frieze.svg.
Front view: people behind their laptops, one table, power strips on the table's front with every socket taken,
a router, tea. Colours come from CSS classes so both themes work. Run it after any change, then build berry."""
import pathlib

W, H, TY = 1440, 272, 204           # canvas, table-top line
OUT = pathlib.Path(__file__).resolve().parents[1] / 'src' / 'berry-frieze.svg'
o = []
def add(s): o.append(s)

# ---------------------------------------------------------------- parts
def torso(cx, shirt='paper', top=144, w=52):
    add(f'<path class="{shirt} line" d="M{cx-w},{TY+6} C{cx-w},{top+26} {cx-w+12},{top+6} {cx-20},{top+1} Q{cx},{top-2} {cx+20},{top+1} '
        f'C{cx+w-12},{top+6} {cx+w},{top+26} {cx+w},{TY+6} Z"/>')

def neck(cx, y=124):
    add(f'<path class="skin line" d="M{cx-8},{y} L{cx-8},{y+18} Q{cx},{y+24} {cx+8},{y+18} L{cx+8},{y} Z"/>')

def head(cx, hy=100, rx=24, ry=27):
    add(f'<ellipse class="skin line" cx="{cx}" cy="{hy}" rx="{rx}" ry="{ry}"/>')

def eyes(cx, hy=100, kind='dot', dx=9):
    if kind == 'dot':
        add(f'<ellipse class="featf" cx="{cx-dx}" cy="{hy+1}" rx="2.6" ry="3.4"/><ellipse class="featf" cx="{cx+dx}" cy="{hy+1}" rx="2.6" ry="3.4"/>')
    elif kind == 'closed':   # content, eyes shut
        add(f'<path class="feat nofill" d="M{cx-dx-4},{hy+2} Q{cx-dx},{hy-2} {cx-dx+4},{hy+2} M{cx+dx-4},{hy+2} Q{cx+dx},{hy-2} {cx+dx+4},{hy+2}"/>')
    elif kind == 'down':     # looking down at the screen
        add(f'<path class="feat nofill" d="M{cx-dx-4},{hy+1} Q{cx-dx},{hy+5} {cx-dx+4},{hy+1} M{cx+dx-4},{hy+1} Q{cx+dx},{hy+5} {cx+dx+4},{hy+1}"/>')

def brows(cx, hy=100, dx=9, lift=0):
    add(f'<path class="feat nofill thin" d="M{cx-dx-5},{hy-8-lift} Q{cx-dx},{hy-11-lift} {cx-dx+5},{hy-8-lift} M{cx+dx-5},{hy-8-lift} Q{cx+dx},{hy-11-lift} {cx+dx+5},{hy-8-lift}"/>')

def nose(cx, hy=100, side=1):
    add(f'<path class="feat nofill thin" d="M{cx+side},{hy+3} Q{cx+5*side},{hy+9} {cx-side},{hy+10}"/>')

def mouth(cx, hy=100, kind='smile'):
    if kind == 'smile':
        add(f'<path class="feat nofill" d="M{cx-6},{hy+14} Q{cx},{hy+20} {cx+6},{hy+14}"/>')
    elif kind == 'flat':
        add(f'<path class="feat nofill" d="M{cx-5},{hy+16} L{cx+5},{hy+16}"/>')
    elif kind == 'talk':
        add(f'<path class="featf" d="M{cx-6},{hy+14} Q{cx},{hy+22} {cx+6},{hy+14} Z"/>')
    elif kind == 'grin':
        add(f'<path class="featf" d="M{cx-8},{hy+13} Q{cx},{hy+24} {cx+8},{hy+13} Z"/>')

def glasses(cx, hy=100, dx=9):
    add(f'<circle class="feat nofill" cx="{cx-dx}" cy="{hy+1}" r="7.5"/><circle class="feat nofill" cx="{cx+dx}" cy="{hy+1}" r="7.5"/>'
        f'<path class="feat nofill" d="M{cx-dx+7.5},{hy} Q{cx},{hy-3} {cx+dx-7.5},{hy}"/>')

def hair(cx, kind, hy=100):
    if kind == 'short':
        add(f'<path class="hair line" d="M{cx-24},{hy-2} C{cx-26},{hy-30} {cx-8},{hy-34} {cx+4},{hy-31} C{cx+20},{hy-30} {cx+27},{hy-18} {cx+24},{hy-2} '
            f'C{cx+20},{hy-14} {cx+8},{hy-18} {cx-4},{hy-17} C{cx-14},{hy-16} {cx-20},{hy-10} {cx-24},{hy-2} Z"/>')
    elif kind == 'curly':
        bumps = [(-20, -14, 9), (-10, -24, 10), (3, -27, 10), (15, -22, 10), (22, -10, 8), (-24, -2, 6), (24, 0, 6)]
        add('<g class="hair line">' + ''.join(f'<circle cx="{cx+x}" cy="{hy+y}" r="{r}"/>' for x, y, r in bumps) + '</g>')
        add(f'<path class="hair" d="M{cx-20},{hy-6} Q{cx},{hy-30} {cx+20},{hy-6} Z"/>')
    elif kind == 'bun':
        add(f'<circle class="hair line" cx="{cx+2}" cy="{hy-33}" r="11"/>')
        add(f'<path class="hair line" d="M{cx-25},{hy+4} C{cx-28},{hy-28} {cx+28},{hy-30} {cx+25},{hy+4} C{cx+18},{hy-12} {cx-10},{hy-16} {cx-25},{hy+4} Z"/>')
    elif kind == 'cap':
        add(f'<path class="hair line" d="M{cx-24},{hy-6} C{cx-24},{hy-34} {cx+24},{hy-34} {cx+24},{hy-6} Z"/>')
        add(f'<path class="hair line" d="M{cx+10},{hy-8} L{cx+40},{hy-6} Q{cx+42},{hy-1} {cx+36},{hy-1} L{cx+4},{hy-2} Z"/>')
        add(f'<circle class="paper line" cx="{cx}" cy="{hy-30}" r="3"/>')
    elif kind == 'side':   # short hair with a side parting
        add(f'<path class="hair line" d="M{cx-25},{hy+2} C{cx-28},{hy-26} {cx-6},{hy-36} {cx+10},{hy-31} C{cx+24},{hy-27} {cx+28},{hy-12} {cx+24},{hy+2} '
            f'C{cx+22},{hy-12} {cx+12},{hy-20} {cx-2},{hy-21} C{cx-10},{hy-10} {cx-18},{hy-6} {cx-25},{hy+2} Z"/>')

def hijab(cx, hy=100, fill='hair', fold=False):
    # a scarf framing the face and falling onto the shoulders
    add(f'<path class="{fill} line" d="M{cx-31},{hy+6} C{cx-33},{hy-30} {cx-14},{hy-36} {cx},{hy-36} C{cx+14},{hy-36} {cx+33},{hy-30} {cx+31},{hy+6} '
        f'C{cx+33},{hy+26} {cx+42},{hy+40} {cx+46},{hy+50} Q{cx},{hy+60} {cx-46},{hy+50} C{cx-42},{hy+40} {cx-33},{hy+26} {cx-31},{hy+6} Z"/>')
    if fold:   # the scarf's folds, so it reads as cloth
        add(f'<path class="line nofill thin" d="M{cx+24},{hy-24} C{cx+30},{hy-4} {cx+28},{hy+22} {cx+38},{hy+44} M{cx-26},{hy+30} C{cx-14},{hy+40} {cx+10},{hy+42} {cx+30},{hy+34}"/>')
    add(f'<ellipse class="skin line" cx="{cx}" cy="{hy+3}" rx="18" ry="22"/>')

def beard(cx, hy=100):
    # a short, neat beard along the jaw: the cheeks and the whole face stay open
    add(f'<path class="hair line" d="M{cx-21},{hy+12} C{cx-18},{hy+28} {cx-9},{hy+31} {cx},{hy+31} C{cx+9},{hy+31} {cx+18},{hy+28} {cx+21},{hy+12} '
        f'C{cx+14},{hy+22} {cx+8},{hy+24} {cx},{hy+24} C{cx-8},{hy+24} {cx-14},{hy+22} {cx-21},{hy+12} Z"/>')

def headphones(cx, hy=100):
    d = f'M{cx-28},{hy-2} C{cx-32},{hy-46} {cx+32},{hy-46} {cx+28},{hy-2}'
    add(f'<path class="line nofill" style="stroke-width:9" d="{d}"/><path class="band" d="{d}"/>')
    add(f'<rect class="paper line" x="{cx-35}" y="{hy-10}" width="13" height="23" rx="6"/><rect class="paper line" x="{cx+22}" y="{hy-10}" width="13" height="23" rx="6"/>')

def laptop(cx, w=80, h=50, sticker=False):
    x, y = cx - w / 2, TY - h
    add(f'<ellipse class="screen-glow" cx="{cx}" cy="{y-6}" rx="{w*0.75}" ry="{h*0.9}"/>')
    add(f'<rect class="lid line" x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>')
    add(f'<path class="lid-edge" d="M{x+6},{y+h-5} L{x+w-6},{y+h-5}"/>')
    if sticker:   # the ة as a sticker: a rounded square ring and two berry dots
        sx, sy = cx, y + h / 2 + 3
        add(f'<rect class="sticker" x="{sx-8}" y="{sy-6}" width="16" height="13" rx="4.5" fill="none" stroke-width="3.6"/>')
        add(f'<rect class="sticker-dot" x="{sx-6.5}" y="{sy-14}" width="5.5" height="5" rx="1.6"/><rect class="sticker-dot" x="{sx+1}" y="{sy-14}" width="5.5" height="5" rx="1.6"/>')

def arm(d, sleeve='paper'):
    add(f'<path class="{sleeve} line" d="{d}"/>')

def hand(x, y, r=7):
    add(f'<circle class="skin line" cx="{x}" cy="{y}" r="{r}"/>')

def tea_glass(x, y, s=1.0, steam=False):
    w1, w2, h = 9 * s, 7 * s, 17 * s
    add(f'<path class="paper line" d="M{x-w1},{y-h} L{x-w2},{y} L{x+w2},{y} L{x+w1},{y-h} Z"/>')
    add(f'<path class="tea" d="M{x-w1*0.86},{y-h*0.62} L{x-w2},{y-1.5} L{x+w2},{y-1.5} L{x+w1*0.86},{y-h*0.62} Z"/>')
    if steam:
        add(f'<path class="line nofill steam" d="M{x-3},{y-h-6} q-4,-6 0,-11 q4,-5 0,-11 M{x+4},{y-h-4} q-4,-6 0,-11"/>')

def person(cx, hairkind=None, shirt='paper', eyes_kind='dot', mouth_kind='smile', glasses_on=False, beard_on=False,
           phones=False, pose='type', scarf=None, dy=0, w=52, sticker=False, nose_side=1, brows_on=False):
    # the body may sit a little higher or lower; the laptop always stands on the table
    add(f'<g transform="translate(0,{dy})">')
    torso(cx, shirt, w=w)
    if scarf: hijab(cx, fill=scarf[0], fold=scarf[1])
    else:
        neck(cx); head(cx)
    if hairkind: hair(cx, hairkind)
    if beard_on: beard(cx)
    eyes(cx, kind=eyes_kind)
    if brows_on: brows(cx)
    if nose_side: nose(cx, side=nose_side)
    if glasses_on: glasses(cx)
    mouth(cx, kind=mouth_kind)
    if phones: headphones(cx)
    add('</g>')
    laptop(cx, sticker=sticker)
    add(f'<g transform="translate(0,{dy})">')
    if pose == 'tea':
        arm(f'M{cx+44},{TY} C{cx+52},{TY-40} {cx+40},{TY-62} {cx+20},{TY-74} L{cx+12},{TY-62} C{cx+26},{TY-54} {cx+32},{TY-36} {cx+28},{TY}', shirt)
        tea_glass(cx + 13, TY - 70, 1.05)
        hand(cx + 19, TY - 76, 6.5)
    elif pose == 'wave':
        arm(f'M{cx-44},{TY-30} C{cx-56},{TY-60} {cx-62},{TY-96} {cx-58},{TY-128} L{cx-46},{TY-128} C{cx-48},{TY-98} {cx-42},{TY-66} {cx-30},{TY-44}', shirt)
        hand(cx - 52, TY - 134, 8)
    elif pose == 'phone':
        arm(f'M{cx-46},{TY} C{cx-52},{TY-44} {cx-44},{TY-74} {cx-30},{TY-92} L{cx-20},{TY-84} C{cx-30},{TY-68} {cx-34},{TY-40} {cx-30},{TY}', shirt)
        add(f'<rect class="ink line" x="{cx-34}" y="{TY-122}" width="12" height="24" rx="3" transform="rotate(-12 {cx-28} {TY-110})"/>')
        hand(cx - 25, TY - 96, 7)
    elif pose == 'chin':
        arm(f'M{cx+44},{TY} C{cx+46},{TY-30} {cx+30},{TY-58} {cx+12},{TY-66} L{cx+8},{TY-56} C{cx+22},{TY-50} {cx+30},{TY-28} {cx+28},{TY}', shirt)
        hand(cx + 9, TY - 72, 8)
    add('</g>')

def pourer(cx):
    # standing, pouring tea for the table
    top = 128
    add(f'<path class="paper line" d="M{cx-48},{TY+6} C{cx-48},{top+20} {cx-38},{top} {cx-18},{top-6} Q{cx},{top-9} {cx+18},{top-6} C{cx+38},{top} {cx+48},{top+20} {cx+48},{TY+6} Z"/>')
    neck(cx, 102); head(cx, 80)
    hair(cx, 'short', 80)
    add(f'<path class="hair line" d="M{cx-14},{80+15} Q{cx},{80+9} {cx+14},{80+15} Q{cx},{80+12} {cx-14},{80+15} Z"/>')  # moustache
    eyes(cx, 80, 'down'); brows(cx, 80); nose(cx, 80); mouth(cx, 80, 'smile')
    arm(f'M{cx+40},{top+20} C{cx+58},{top+30} {cx+70},{top+40} {cx+82},{top+34} L{cx+84},{top+46} C{cx+70},{top+54} {cx+52},{top+50} {cx+34},{top+44}')
    tx, ty = cx + 104, top + 40
    add(f'<path class="paper line" d="M{tx-20},{ty} C{tx-22},{ty-24} {tx+20},{ty-24} {tx+20},{ty} C{tx+20},{ty+16} {tx-20},{ty+16} {tx-20},{ty} Z"/>')
    add(f'<path class="paper line" d="M{tx-19},{ty-2} Q{tx-26},{ty+4} {tx-24},{ty+12} Q{tx-14},{ty+6} {tx-16},{ty-4} Z"/>')
    add(f'<path class="paper line" d="M{tx+18},{ty-2} Q{tx+32},{ty-2} {tx+38},{ty+10} L{tx+34},{ty+12} Q{tx+28},{ty+4} {tx+18},{ty+6} Z"/>')
    add(f'<rect class="ink line" x="{tx-6}" y="{ty-26}" width="12" height="6" rx="3"/>')
    hand(cx + 86, top + 40, 8)
    add(f'<path class="tea-stream" d="M{tx+37},{ty+11} C{tx+40},{ty+30} {tx+40},{ty+44} {tx+40},{TY-17}"/>')
    tea_glass(tx + 40, TY - 1, 1.1)

def router(cx):
    add(f'<path class="line nofill thick" d="M{cx-18},{TY-26} L{cx-26},{TY-66} M{cx+18},{TY-26} L{cx+26},{TY-66}"/>')
    add(f'<circle class="ink" cx="{cx-26}" cy="{TY-68}" r="3.5"/><circle class="ink" cx="{cx+26}" cy="{TY-68}" r="3.5"/>')
    add(f'<rect class="paper line" x="{cx-34}" y="{TY-28}" width="68" height="28" rx="7"/>')
    for i, k in enumerate((-18, -6, 6, 18)):
        add(f'<circle class="led led{i}" cx="{cx+k}" cy="{TY-14}" r="3.2"/>')

def plant(cx):
    add(f'<path class="leaf line" d="M{cx},{TY-30} C{cx-30},{TY-50} {cx-30},{TY-86} {cx-6},{TY-96} C{cx-4},{TY-70} {cx-4},{TY-50} {cx},{TY-30} Z"/>')
    add(f'<path class="leaf line" d="M{cx},{TY-30} C{cx+26},{TY-46} {cx+34},{TY-78} {cx+14},{TY-92} C{cx+8},{TY-66} {cx+4},{TY-48} {cx},{TY-30} Z"/>')
    add(f'<path class="leaf line" d="M{cx},{TY-30} C{cx-6},{TY-66} {cx+2},{TY-104} {cx+4},{TY-112} C{cx+10},{TY-96} {cx+8},{TY-60} {cx},{TY-30} Z"/>')
    add(f'<path class="paper line" d="M{cx-18},{TY-32} L{cx-14},{TY} L{cx+14},{TY} L{cx+18},{TY-32} Z"/>')

def strip(x0, cables_from):
    # a power strip hung on the table's front, every socket taken: cables come over the edge from each device
    n = len(cables_from)
    w = 34 * n + 28
    y = TY + 26
    for i, fx in enumerate(cables_from):
        sx = x0 + 22 + 34 * i
        add(f'<path class="cable" d="M{fx},{TY-3} C{fx},{TY+14} {sx},{TY+4} {sx},{y-4}"/>')
    add(f'<rect class="strip" x="{x0}" y="{y}" width="{w}" height="28" rx="9"/>')
    for i in range(n):
        sx = x0 + 22 + 34 * i
        add(f'<rect class="plug" x="{sx-8}" y="{y-8}" width="16" height="18" rx="4"/>')
    add(f'<circle class="switch-led" cx="{x0 + w - 13}" cy="{y + 14}" r="4"/>')

# ---------------------------------------------------------------- compose
TOP = 34
add(f'<svg class="frieze" viewBox="0 {TOP} {W} {H-TOP}" preserveAspectRatio="xMidYMax slice" aria-hidden="true" focusable="false">')
add('<defs><pattern id="stripes" width="10" height="10" patternUnits="userSpaceOnUse"><rect class="stripe-bg" width="10" height="10"/><rect class="stripe-fg" width="10" height="4"/></pattern>'
    '<filter id="hand" x="-2%" y="-5%" width="104%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="2" seed="7"/>'
    '<feDisplacementMap in="SourceGraphic" scale="2.4" xChannelSelector="R" yChannelSelector="G"/></filter></defs>')
# the table's front first, then the people (with a hand-drawn wobble), then the crisp table edge, cables and strips
add(f'<rect class="table-front" x="-20" y="{TY+4}" width="{W+40}" height="{H-TY}"/>')
add('<g filter="url(#hand)">')
pourer(96)
person(300, scarf=('hair', False), eyes_kind='down', mouth_kind='smile', shirt='ink', dy=4, w=50, nose_side=0)
tea_glass(370, TY, 0.95, steam=True)
person(468, hairkind='curly', phones=True, eyes_kind='closed', mouth_kind='grin', dy=8, w=48, sticker=True)
person(636, hairkind='short', beard_on=True, pose='tea', shirt='stripe', eyes_kind='closed', dy=-6, w=56, brows_on=True)
router(760)
person(884, hairkind='bun', glasses_on=True, eyes_kind='down', mouth_kind='flat', shirt='ink', dy=2, w=48, sticker=True, nose_side=-1)
plant(978)
person(1064, hairkind='cap', pose='phone', mouth_kind='talk', dy=-4, w=54, brows_on=True)
person(1232, scarf=('paper', True), pose='wave', mouth_kind='grin', shirt='stripe', dy=6, w=50, sticker=True, nose_side=0)
person(1392, hairkind='side', glasses_on=True, pose='chin', mouth_kind='flat', eyes_kind='dot', shirt='ink', dy=-2, w=54, nose_side=-1)
add('</g>')
add(f'<rect class="table-top" x="-20" y="{TY-2}" width="{W+40}" height="8"/>')
strip(160, [300, 468])
strip(740, [668, 760, 884, 1064])
strip(1150, [1232, 1392])
add('</svg>')

OUT.write_text('\n'.join(o), encoding='utf-8')
print(f'wrote {OUT} ({len(chr(10).join(o))/1024:.1f} KB)')
