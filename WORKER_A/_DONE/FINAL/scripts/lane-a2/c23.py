def sub(p, pairs):
    s = open(p, encoding='utf8', newline='').read()
    for a, b in pairs:
        assert s.count(a) == 1, (p, a)
        s = s.replace(a, b)
    open(p, 'w', encoding='utf8', newline='').write(s)

sub('src/modules/subscriptions/subscriptions.repository.ts', [
("""/** A check-in's Gaza date, dated by PostgreSQL as `subscription_usage` dates it. */
const GAZA_DAY = Prisma.sql`(checked_in_at AT TIME ZONE 'Asia/Gaza')::date`;
""",
"""/** A check-in's Gaza date, dated by PostgreSQL as `subscription_usage` dates it. */
const GAZA_DAY = Prisma.sql`(checked_in_at AT TIME ZONE 'Asia/Gaza')::date`;

/**
 * The space's check-ins whose Gaza date is from `from` to `to`, both included: checked in from the
 * Gaza midnight that starts `from` up to the one that ends `to`, as instants from the shared
 * calendar, so the `(space_id, checked_in_at)` index serves the range (finding 127). PostgreSQL's
 * Gaza dates equal the calendar's (src/db/gazaZone.api.test.ts).
 */
export function checkInsOnDays(spaceId: number, { from, to }: { from: string; to: string }) {
  return Prisma.sql`space_id = ${spaceId} AND checked_in_at >= ${gazaInstant(from, 0)}
    AND checked_in_at < ${gazaInstant(addDays(to, 1), 0)}`;
}
"""),
("""import { isForeignKeyViolation, isUniqueViolation, prisma, type Tx } from '../../db/index.ts';""",
"""import { addDays, gazaInstant } from '@masaha/shared/core';

import { isForeignKeyViolation, isUniqueViolation, prisma, type Tx } from '../../db/index.ts';"""),
("""    /**
     * A page of the space's check-ins whose Gaza date (dated as `subscription_usage` dates them) is
     * from `from` to `to`, both included, the latest first, then by id; and how many there are.
     */""",
"""    /**
     * A page of the space's check-ins whose Gaza date is from `from` to `to`, both included
     * (`checkInsOnDays`), the latest first, then by id; and how many there are.
     */"""),
("""      const where = Prisma.sql`space_id = ${spaceId} AND ${GAZA_DAY} BETWEEN ${from}::date AND ${to}::date`;""",
"""      const where = checkInsOnDays(spaceId, { from, to });"""),
])
