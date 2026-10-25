R = 'C:/dev/masaha/app-b/'


def ed(p, pairs):
    s = open(R + p, encoding='utf-8', newline='').read()
    for a, b in pairs:
        assert s.count(a) == 1, (p, a[:80])
        s = s.replace(a, b)
    open(R + p, 'w', encoding='utf-8', newline='').write(s)


ed('packages/shared/src/core/errors.ts', [
("""  'OUTSIDE_OPENING_HOURS',
  // occupancy""", """  'OUTSIDE_OPENING_HOURS',
  // warning only: a check-in while the space is announced closed (occupancy)
  'CLOSURE_IN_FORCE',
  // occupancy"""),
])
ed('packages/shared/src/desk/responses.ts', [
("""  'OUTSIDE_OPENING_HOURS',
  'SUBSCRIPTION_NOT_STARTED',""", """  'OUTSIDE_OPENING_HOURS',
  'CLOSURE_IN_FORCE',
  'SUBSCRIPTION_NOT_STARTED',"""),
])
ed('apps/web/src/shared/copy/arabic/errors.ts', [
("""  OUTSIDE_OPENING_HOURS: 'سُجّل هذا الحضور خارج ساعات عمل المساحة.',
""", """  OUTSIDE_OPENING_HOURS: 'سُجّل هذا الحضور خارج ساعات عمل المساحة.',
  CLOSURE_IN_FORCE: 'المساحة معلَنة مغلقة الآن، وسُجّل الحضور رغم ذلك.',
"""),
])
ed('apps/web/src/shared/copy/english/errors.ts', [
("""  OUTSIDE_OPENING_HOURS: 'This check-in is outside the space’s opening hours.',
""", """  OUTSIDE_OPENING_HOURS: 'This check-in is outside the space’s opening hours.',
  CLOSURE_IN_FORCE: 'The space is announced closed now; the check-in was recorded anyway.',
"""),
])
ed('apps/api/src/modules/occupancy/occupancy.service.ts', [
("""     * `SPACE_FULL` when as many are present as it seats (none without a capacity), then
     * `OUTSIDE_OPENING_HOURS` when it has hours and is not open by them.
     */""", """     * `SPACE_FULL` when as many are present as it seats (none without a capacity), then
     * `OUTSIDE_OPENING_HOURS` when it has hours and is not open by them, then `CLOSURE_IN_FORCE`
     * while a closure it announced runs (the live status's `closedAt`).
     */"""),
("""      if (week !== null && !openRangeAt(week, gazaClockOf(now))) {
        warnings.push('OUTSIDE_OPENING_HOURS');
      }
      return warnings;""", """      if (week !== null && !openRangeAt(week, gazaClockOf(now))) {
        warnings.push('OUTSIDE_OPENING_HOURS');
      }
      if ((await announcements.closedAt([spaceId], now, tx)).has(spaceId)) {
        warnings.push('CLOSURE_IN_FORCE');
      }
      return warnings;"""),
])
print('ok')
