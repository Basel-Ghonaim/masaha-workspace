import io

WEB = 'C:/dev/masaha/app/apps/web/src/'
ROOT = WEB + 'features/directory/'


def sub(path, old, new, count=1, root=ROOT):
    s = io.open(root + path, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (path, old[:60], s.count(old))
    s = s.replace(old, new)
    io.open(root + path, 'w', encoding='utf-8', newline='').write(s)


# Copy.
sub('shared/copy/english/directory.ts', """      title: 'We couldn’t find your location',
      text: 'Choose your area to browse its spaces.',
    },""", """      title: 'We couldn’t find your location',
      text: 'Choose your area or set your location on the map to sort the spaces by distance.',
    },""", root=WEB)
sub('shared/copy/english/directory.ts', """    chooseArea: 'Choose your area',
  },""", """    chooseArea: 'Choose your area',
    /** The refused states' other way: a point set by hand on the map. */
    pickOnMap: 'Set my location on the map',
    /** Beside a point set by hand: set it again. */
    change: 'Change location',
  },
  /** Setting one's location by hand, at the map's centre. */
  pick: {
    title: 'Set your location on the map',
    text: 'Move the map until the mark is on your approximate location, or tap it. We sort the spaces by distance from it; it is sent rounded and never stored.',
    /** Read with the map while picking. */
    keys: 'The arrow keys move the map under the mark in the centre.',
    confirm: 'Set location here',
    back: 'Back',
  },""", root=WEB)
sub('shared/copy/english/directory.ts', """    you: 'Your location',""", """    you: 'Your location',
    /** The visitor's point when set by hand. */
    yourPin: 'My location (manual)',""", root=WEB)

sub('shared/copy/arabic/directory.ts', """      title: 'تعذّر تحديد موقعك',
      text: 'اختر منطقتك لتصفّح مساحاتها.',
    },""", """      title: 'تعذّر تحديد موقعك',
      text: 'اختر منطقتك أو حدّد موقعك على الخريطة لنرتّب المساحات حسب المسافة.',
    },""", root=WEB)
sub('shared/copy/arabic/directory.ts', """    chooseArea: 'اختر منطقتك',
  },""", """    chooseArea: 'اختر منطقتك',
    pickOnMap: 'حدّد موقعي على الخريطة',
    change: 'تغيير الموقع',
  },
  pick: {
    title: 'حدّد موقعك على الخريطة',
    text: 'حرّك الخريطة حتى تقع العلامة على مكانك التقريبي، أو اضغط عليه. نرتّب المساحات حسب المسافة منه، ويُرسَل مقرَّبًا ولا يُحفظ.',
    keys: 'الأسهم تحرّك الخريطة تحت العلامة في الوسط.',
    confirm: 'ثبّت الموقع هنا',
    back: 'رجوع',
  },""", root=WEB)
sub('shared/copy/arabic/directory.ts', """    you: 'موقعك',""", """    you: 'موقعك',
    yourPin: 'موقعي (يدوي)',""", root=WEB)

# The state.
sub('types/NearState.ts', """/**
 * Near me, in memory only: whether it is asking, has a point, or was refused (denied or
 * unavailable) or given a position too imprecise or outside the Strip; where the point came from;
 * and whether the lists sort by distance from it.
 */
export type NearState = {
  status: 'idle' | 'locating' | 'granted' | 'denied' | 'imprecise';
  point: NearPoint | null;
  source: 'device' | 'pin' | null;
  sorting: boolean;
};""", """/**
 * Near me, in memory only: whether it is asking, has a point, or was refused (denied or
 * unavailable) or given a position too imprecise or outside the Strip, or a point is being picked
 * on the map; where the point came from; and whether the lists sort by distance from it.
 */
export type NearState = {
  status: 'idle' | 'locating' | 'granted' | 'denied' | 'imprecise' | 'picking';
  point: NearPoint | null;
  source: 'device' | 'pin' | null;
  sorting: boolean;
};""")

sub('hooks/near/nearMeStore.ts', """const store = createStore<NearState>()(() => IDLE);
""", """const store = createStore<NearState>()(() => IDLE);

// While a point is picked on the map, the state before it, which «رجوع» restores.
let beforePick: NearState = IDLE;
""")
sub('hooks/near/nearMeStore.ts', """  /** Back to idle, with no point. */
  clear: () => {
    store.setState(IDLE);
  },""", """  /** Back to idle, with no point. */
  clear: () => {
    store.setState(IDLE);
  },
  /** Picking a point on the map; what was there waits to be restored. */
  startPick: () => {
    const now = store.getState();
    if (now.status === 'picking') return;
    beforePick = now;
    store.setState({ ...IDLE, status: 'picking' });
  },
  /** «رجوع»: the state before the pick, a point kept as it was. */
  cancelPick: () => {
    if (store.getState().status !== 'picking') return;
    store.setState(beforePick);
  },
  /** A point placed by hand, already rounded: kept as the device's is, sorting the lists. */
  placePin: (point: NearPoint) => {
    store.setState({ status: 'granted', point, source: 'pin', sorting: true });
  },""")
print('ok')
