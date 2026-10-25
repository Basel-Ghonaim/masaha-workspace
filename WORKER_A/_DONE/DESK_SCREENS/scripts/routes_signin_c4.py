p='C:/dev/masaha/app/apps/web/src/pages/dashboard/routes.component.test.tsx'
s=open(p,encoding='utf-8',newline='').read()
old='''  fakeTransport(() =>
    ok(
      user.spaces.map((link: SessionSpaceLink) => ({
        ...FOCUS,
        ...link,
        nameEn: link.spaceId === FOCUS.spaceId ? FOCUS.nameEn : 'Nook',
      })),
    ),
  );'''
assert s.count(old)==1
new='''  fakeTransport((request) => {
    // The desk, where reception lands: its reads answered as the server would, with no one present.
    if (request.url?.endsWith('/occupancy') === true) return ok(NO_ONE_PRESENT);
    if (request.url?.endsWith('/visit-terms') === true) return ok(VISIT_TERMS);
    return ok(
      user.spaces.map((link: SessionSpaceLink) => ({
        ...FOCUS,
        ...link,
        nameEn: link.spaceId === FOCUS.spaceId ? FOCUS.nameEn : 'Nook',
      })),
    );
  });'''
s=s.replace(old,new)
old2='/** Signs in a user (id 1) with `fields`; their spaces are answered from their links. */'
assert s.count(old2)==1
s=s.replace(old2,'''/** The desk's state now, with no one present. */
const NO_ONE_PRESENT = { status: 'AVAILABLE', capacity: 40, present: 0, override: null, people: [] };

/** The desk's terms: an hour and a day price, no student rates, no typed price. */
const VISIT_TERMS = {
  rounding: { rule: 'UP_AFTER_MINUTES', minutes: 15 },
  capAtDayPrice: true,
  mayTypePrice: false,
  rates: [{ shiftId: null, general: { hourAgorot: 500, dayAgorot: 2500 }, student: null }],
};

'''+old2)
# The desk block's own terms reuse the constant.
old3='''      if (request.url === '/manage/spaces/7/visit-terms') {
        return ok({
          rounding: { rule: 'UP_AFTER_MINUTES', minutes: 15 },
          capAtDayPrice: true,
          mayTypePrice: false,
          rates: [{ shiftId: null, general: { hourAgorot: 500, dayAgorot: 2500 }, student: null }],
        });
      }'''
assert s.count(old3)==1
s=s.replace(old3,"      if (request.url === '/manage/spaces/7/visit-terms') return ok(VISIT_TERMS);")
open(p,'w',encoding='utf-8',newline='').write(s)
