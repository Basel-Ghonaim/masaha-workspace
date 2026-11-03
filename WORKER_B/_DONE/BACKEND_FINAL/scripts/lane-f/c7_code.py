D = 'C:/dev/masaha/app-b-lane-f/apps/api/src/modules/finance/'


def rw(p, f):
    s = open(D + p, encoding='utf-8', newline='').read()
    s = f(s)
    open(D + p, 'w', encoding='utf-8', newline='').write(s)


def rep(s, old, new):
    assert s.count(old) == 1, old[:80]
    return s.replace(old, new)


def repository(s):
    s = rep(s, "import type { Window } from './windows.ts';",
            "import type { HourSlot, Window } from './windows.ts';")
    s = rep(s, """/**
 * Finance's own reads (a read model, docs/backend/conventions.md › R7): who paid in a month, from
 * the payments and the items they paid.""", """/**
 * The space's closed stays checked in within `[from, to)` (a `WITH` body): its visits and its
 * subscription check-ins, the auto check-out's included, open ones left out (the owner's decision
 * 7); each with its kind and, a member's, its customer. Bounded by the check-in on the
 * `(space_id, checked_in_at)` indexes: a stay never crosses its check-in's Gaza day.
 */
function closedStaysIn(spaceId: number, from: Date, to: Date) {
  return Prisma.sql`
    SELECT checked_in_at, checked_out_at, NULL::integer AS customer_id, 'VISIT' AS kind
    FROM visits
    WHERE space_id = ${spaceId} AND checked_out_at IS NOT NULL
      AND checked_in_at >= ${from} AND checked_in_at < ${to}
    UNION ALL
    SELECT checked_in_at, checked_out_at, customer_id, 'MEMBER'
    FROM check_ins
    WHERE space_id = ${spaceId} AND checked_out_at IS NOT NULL
      AND checked_in_at >= ${from} AND checked_in_at < ${to}`;
}

/** The windows as two arrays of instants, and the range they span (they come in order). */
function spanOf(windows: readonly Window[]) {
  const first = windows[0];
  const last = windows.at(-1);
  if (!first || !last) throw new Error('No window to read.');
  return {
    froms: windows.map(({ from }) => from.toISOString()),
    tos: windows.map(({ to }) => to.toISOString()),
    from: first.from,
    to: last.to,
  };
}

/**
 * Finance's own reads (a read model, docs/backend/conventions.md › R7): who paid in a month, from
 * the payments and the items they paid; the occupancy statistics, from the closed stays.""")
    s = rep(s, """        total,
      };
    },
  };
}""", """        total,
      };
    },

    /**
     * Per Gaza day (each window one day, in order): the closed visits checked in on it, and the
     * members who checked in on it, each once however many times. One statement.
     */
    async perDay(
      spaceId: number,
      days: readonly Window[],
    ): Promise<{ visits: number; members: number }[]> {
      if (days.length === 0) return [];
      const { froms, tos, from, to } = spanOf(days);
      return prisma.$queryRaw<{ visits: number; members: number }[]>`
        WITH stays AS (${closedStaysIn(spaceId, from, to)})
        SELECT count(s.kind) FILTER (WHERE s.kind = 'VISIT')::integer AS visits,
               count(DISTINCT s.customer_id) FILTER (WHERE s.kind = 'MEMBER')::integer AS members
        FROM unnest(${froms}::timestamptz[], ${tos}::timestamptz[]) WITH ORDINALITY AS w(f, t, i)
        LEFT JOIN stays s ON s.checked_in_at >= w.f AND s.checked_in_at < w.t
        GROUP BY w.i ORDER BY w.i`;
    },

    /**
     * Per hour slot, in order: the closed stays overlapping it (checked in before its end and out
     * after its start). The stays read once for the slots' range. One statement.
     */
    async presenceBySlot(spaceId: number, slots: readonly HourSlot[]): Promise<number[]> {
      if (slots.length === 0) return [];
      const { froms, tos, from, to } = spanOf(slots);
      const rows = await prisma.$queryRaw<{ present: number }[]>`
        WITH stays AS (${closedStaysIn(spaceId, from, to)})
        SELECT count(s.kind)::integer AS present
        FROM unnest(${froms}::timestamptz[], ${tos}::timestamptz[]) WITH ORDINALITY AS w(f, t, i)
        LEFT JOIN stays s ON s.checked_in_at < w.t AND s.checked_out_at > w.f
        GROUP BY w.i ORDER BY w.i`;
      return rows.map(({ present }) => present);
    },

    /**
     * The average stay of the closed stays checked in within the window, in whole minutes: all,
     * the members' and the visits' apart; `null` without any. One statement.
     */
    async stayMinutes(
      spaceId: number,
      { from, to }: Window,
    ): Promise<{ all: number | null; members: number | null; visits: number | null }> {
      const minutes = Prisma.sql`extract(epoch FROM checked_out_at - checked_in_at) / 60`;
      const [row] = await prisma.$queryRaw<
        { all: number | null; members: number | null; visits: number | null }[]
      >`
        WITH stays AS (${closedStaysIn(spaceId, from, to)})
        SELECT round(avg(${minutes}))::integer AS "all",
               round(avg(${minutes}) FILTER (WHERE kind = 'MEMBER'))::integer AS members,
               round(avg(${minutes}) FILTER (WHERE kind = 'VISIT'))::integer AS visits
        FROM stays`;
      return row ?? { all: null, members: null, visits: null };
    },
  };
}""")
    return s


def service(s):
    s = rep(s, """  Payer,
  PayersQuery,
} from '@masaha/shared/finance';""", """  OccupancyReport,
  Payer,
  PayersQuery,
} from '@masaha/shared/finance';""")
    s = rep(s, """import { toBalanceRow, toCollections } from './finance.mapper.ts';
import { createFinanceRepository } from './finance.repository.ts';
import {
  currentMonth,
  dayWindow,
  daysEnding,
  monthError,
  monthsEnding,
  monthWindow,
} from './windows.ts';""", """import { toBalanceRow, toCollections } from './finance.mapper.ts';
import { createFinanceRepository } from './finance.repository.ts';
import { averageDailyAttendance, averagePerHour, peakHour } from './occupancyGrid.ts';
import {
  currentMonth,
  dayWindow,
  daysEnding,
  daysOfMonth,
  fourWeeksBefore,
  hourSlots,
  monthError,
  monthsEnding,
  monthWindow,
} from './windows.ts';""")
    s = rep(s, """        total,
      };
    },
  };
}

export type FinanceService""", """        total,
      };
    },

    /**
     * The occupancy statistics (data model › Occupancy statistics), from closed stays: the month's
     * average stay, peak hour and average daily attendance, over its days up to today; visits and
     * members per day over the 14 days ending today; the average present per weekday and hour over
     * the 28 days before today. The reads in parallel, with no snapshot: each figure stands alone.
     */
    async occupancy(spaceId: number, query: FinanceMonthQuery): Promise<OccupancyReport> {
      const at = now();
      const month = monthAsked(query.month, at);
      const fortnight = daysEnding(gazaClockOf(at).date, 14);
      const monthDays = daysOfMonth(month, at);
      const weekSlots = hourSlots(fourWeeksBefore(at));
      const monthSlots = hourSlots(monthDays);
      const [byDay, monthByDay, weekPresence, monthPresence, averageStayMinutes] =
        await Promise.all([
          repository.perDay(spaceId, fortnight.map(dayWindow)),
          repository.perDay(spaceId, monthDays.map(dayWindow)),
          repository.presenceBySlot(spaceId, weekSlots),
          repository.presenceBySlot(spaceId, monthSlots),
          repository.stayMinutes(spaceId, monthWindow(month)),
        ]);
      return {
        month,
        averageStayMinutes,
        peakHour: peakHour(monthSlots, monthPresence),
        averageDailyAttendance: averageDailyAttendance(monthByDay),
        byDay: fortnight.map((date, i) => ({
          date,
          visits: byDay[i]?.visits ?? 0,
          members: byDay[i]?.members ?? 0,
        })),
        byHour: averagePerHour(weekSlots, weekPresence),
      };
    },
  };
}

export type FinanceService""")
    return s


def controller(s):
    s = rep(s, """  IncomeReport,
  Payer,""", """  IncomeReport,
  OccupancyReport,
  Payer,""")
    s = rep(s, """      sendSuccess(res, rows satisfies Payer[], { meta: buildPaginationMeta(query, total) });
    },
""", """      sendSuccess(res, rows satisfies Payer[], { meta: buildPaginationMeta(query, total) });
    },

    /** 200 with the month's `OccupancyReport`. */
    occupancy: async (req: Request, res: Response) => {
      const query = req.query as unknown as FinanceMonthQuery;
      const report = await service.occupancy(spaceOf(req).id, query);
      sendSuccess(res, report satisfies OccupancyReport);
    },
""")
    return s


def routes(s):
    return rep(s, """    controller.payers,
  );
""", """    controller.payers,
  );
  router.get(
    '/occupancy',
    requireCan('finance.read'),
    validate(financeMonthQuery, 'query'),
    controller.occupancy,
  );
""")


rw('finance.repository.ts', repository)
rw('finance.service.ts', service)
rw('finance.controller.ts', controller)
rw('finance.manage.routes.ts', routes)
print('ok')
