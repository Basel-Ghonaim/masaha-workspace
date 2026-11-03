import io
import os

os.chdir(r'C:\dev\masaha\app-b\apps\api\src\modules\audit')


def edit(path, reps):
    s = io.open(path, encoding='utf-8', newline='').read()
    for a, b in reps:
        assert s.count(a) == 1, (path, a[:90])
        s = s.replace(a, b)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)


RAW = '''            id: number;
            created_at: Date;
            action: string;
            entity_type: string;
            entity_id: number | null;
            before: Record<string, unknown> | null;
            after: Record<string, unknown> | null;
            actor_id: number | null;
            linked: boolean;
            actor_name: string | null;
            target_name: string | null;
            target_name_ar: string | null;
            target_deleted: boolean | null;
'''

MAPPING = '''        rows: rows.map((row) => ({
          id: row.id,
          createdAt: row.created_at,
          action: row.action,
          entityType: row.entity_type,
          entityId: row.entity_id,
          before: row.before,
          after: row.after,
          actorId: row.actor_id,
          linked: row.linked,
          actorName: row.actor_name,
          targetName: row.target_name,
          targetNameAr: row.target_name_ar,
          targetDeleted: row.target_deleted ?? false,
        })),'''

edit('audit.repository.ts', [
('''/** An actor of `meta.actors`: a linked person, the platform or the system. */''',
 '''/** An entry of the admin's log, with the space it names; `null` for none. */
export type PlatformAuditRow = AuditRow & {
  space: { id: number; nameEn: string; nameAr: string | null; deleted: boolean } | null;
};

/** An actor of `meta.actors`: a linked person, the platform or the system. */'''),
('''/** The most actors `meta.actors` lists. */''',
 '''/** What the admin's log filters by: the actor is a person's id. */
export interface PlatformLogFilter {
  since: Date | null;
  q?: string;
  actions?: readonly string[];
  actor?: number;
}

/** The most actors `meta.actors` lists. */'''),
('''/** `q` against the target's names, as the directory searches (`masaha_search_text`). */
const matches = (q: string) =>
  Prisma.sql`strpos(masaha_search_text(concat_ws(' ', t.name, t.name_ar)), masaha_search_text(${q})) > 0`;
''', '''/**
 * `q` against the target's names, and any other names given, as the directory searches
 * (`masaha_search_text`).
 */
const matches = (q: string, others: Prisma.Sql = Prisma.empty) =>
  Prisma.sql`strpos(masaha_search_text(concat_ws(' ', t.name, t.name_ar${others})), masaha_search_text(${q})) > 0`;

/** An entry's columns as the page selects them. */
interface RawRow {
''' + RAW.replace('            ', '  ') + '''}

const ENTRY_COLUMNS = Prisma.sql`a."id", a."created_at", a."action", a."entity_type", a."entity_id",
  a."before", a."after", a."actor_id", t.name AS target_name, t.name_ar AS target_name_ar,
  t.deleted AS target_deleted`;

const toRow = (row: RawRow): AuditRow => ({
  id: row.id,
  createdAt: row.created_at,
  action: row.action,
  entityType: row.entity_type,
  entityId: row.entity_id,
  before: row.before,
  after: row.after,
  actorId: row.actor_id,
  linked: row.linked,
  actorName: row.actor_name,
  targetName: row.target_name,
  targetNameAr: row.target_name_ar,
  targetDeleted: row.target_deleted ?? false,
});
'''),
('''        prisma.$queryRaw<
          {
''' + RAW + '''          }[]
        >`
          SELECT a."id", a."created_at", a."action", a."entity_type", a."entity_id", a."before",
            a."after", a."actor_id", sm."user_id" IS NOT NULL AS linked,
            CASE WHEN sm."user_id" IS NOT NULL THEN au."name" END AS actor_name,
            t.name AS target_name, t.name_ar AS target_name_ar, t.deleted AS target_deleted
          FROM''', '''        prisma.$queryRaw<RawRow[]>`
          SELECT ${ENTRY_COLUMNS}, sm."user_id" IS NOT NULL AS linked,
            CASE WHEN sm."user_id" IS NOT NULL THEN au."name" END AS actor_name
          FROM'''),
(MAPPING, '''        rows: rows.map(toRow),'''),
])

s = io.open('audit.repository.ts', encoding='utf-8', newline='').read()
tail = '''        total: count?.total ?? 0,
        actors,
      };
    },
  };
}
'''
assert s.endswith(tail)
s = s[: -len('''  };
}
''')] + '''
    /**
     * A page of the platform's events the filter keeps (D3's list, default deny), of every space and
     * of none, newest first, then by id; how many it keeps; and the actors every filter but the
     * actor's keeps (at most 50, by name). Each entry with the space it names, whose names `q` also
     * matches. Three statements in parallel, sharing one `WHERE`.
     */
    async platformLog(
      { since, q, actions, actor }: PlatformLogFilter,
      { skip, take }: { skip: number; take: number },
    ): Promise<{ rows: PlatformAuditRow[]; total: number; actors: ActorRow[] }> {
      const shared = [platformEventsSql()];
      if (since) shared.push(Prisma.sql`a."created_at" >= ${since}`);
      if (actions) shared.push(Prisma.sql`a."action" = ANY(${[...actions]}::text[])`);
      if (q !== undefined) shared.push(matches(q, Prisma.sql`, es."name_en", es."name_ar"`));
      const all = actor === undefined ? shared : [...shared, Prisma.sql`a."actor_id" = ${actor}`];
      const where = Prisma.join(all, ' AND ');
      const actorsWhere = Prisma.join(shared, ' AND ');
      const searchJoins =
        q === undefined ? Prisma.empty : Prisma.sql`${SPACE_JOIN} ${TARGET_JOIN}`;

      const [rows, [count], actors] = await Promise.all([
        prisma.$queryRaw<
          (RawRow & {
            space_id: number | null;
            space_name_en: string | null;
            space_name_ar: string | null;
            space_deleted: boolean | null;
          })[]
        >`
          SELECT ${ENTRY_COLUMNS}, true AS linked, au."name" AS actor_name, es."id" AS space_id,
            es."name_en" AS space_name_en, es."name_ar" AS space_name_ar,
            es."deleted_at" IS NOT NULL AS space_deleted
          FROM "audit_logs" a LEFT JOIN "users" au ON au."id" = a."actor_id" ${SPACE_JOIN}
            ${TARGET_JOIN}
          WHERE ${where}
          ORDER BY a."created_at" DESC, a."id" DESC LIMIT ${take} OFFSET ${skip}`,
        prisma.$queryRaw<{ total: number }[]>`
          SELECT count(*)::integer AS total FROM "audit_logs" a ${searchJoins} WHERE ${where}`,
        prisma.$queryRaw<ActorRow[]>`
          SELECT kind, id, name FROM (
            SELECT DISTINCT CASE WHEN a."actor_id" IS NULL THEN 'SYSTEM' ELSE 'PERSON' END AS kind,
              a."actor_id" AS id, au."name" AS name
            FROM "audit_logs" a LEFT JOIN "users" au ON au."id" = a."actor_id" ${searchJoins}
            WHERE ${actorsWhere}
          ) actors
          ORDER BY CASE kind WHEN 'PERSON' THEN 0 ELSE 2 END, name, id
          LIMIT ${ACTORS_MAX}`,
      ]);
      return {
        rows: rows.map((row) => ({
          ...toRow(row),
          space:
            row.space_id === null || row.space_name_en === null
              ? null
              : {
                  id: row.space_id,
                  nameEn: row.space_name_en,
                  nameAr: row.space_name_ar,
                  deleted: row.space_deleted ?? false,
                },
        })),
        total: count?.total ?? 0,
        actors,
      };
    },
  };
}
'''
s = s.replace('''import { Prisma } from '../../generated/prisma/client.ts';
''', '''import { Prisma } from '../../generated/prisma/client.ts';
import { platformEventsSql } from './platformEvents.ts';
''', 1)
s = s.replace('''/**
 * The target's current name, by its type''', '''/** The space an entry names, for the admin's log. */
const SPACE_JOIN = Prisma.sql`LEFT JOIN "spaces" es ON es."id" = a."space_id"`;

/**
 * The target's current name, by its type''', 1)
io.open('audit.repository.ts', 'w', encoding='utf-8', newline='').write(s)
print('ok')
