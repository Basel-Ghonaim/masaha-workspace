import io
import os
import re

os.chdir(r'C:\dev\masaha\app-b\apps\api\src\modules\audit')
p = 'audit.repository.ts'
s = io.open(p, encoding='utf-8', newline='').read()

start = s.index('/**\n * The target\'s current name, by its type')
end = s.index('/** An entry\'s columns as the page selects them. */')
new_block = '''/**
 * The target, joined by its type (one join each, its type in the condition, so at most one matches;
 * a payment and a data report have none). Joins, not a lateral subquery per entry: a search over a
 * year's entries reads each table once (§12.2's measure).
 */
const TARGET_JOINS = Prisma.sql`
  LEFT JOIN "spaces" ts ON a."entity_type" = 'space' AND ts."id" = a."entity_id"
  LEFT JOIN "users" tu ON a."entity_type" = 'user' AND tu."id" = a."entity_id"
  LEFT JOIN "governorates" tg ON a."entity_type" = 'governorate' AND tg."id" = a."entity_id"
  LEFT JOIN "areas" tar ON a."entity_type" = 'area' AND tar."id" = a."entity_id"
  LEFT JOIN "amenities" tam ON a."entity_type" = 'amenity' AND tam."id" = a."entity_id"
  LEFT JOIN "customers" tc ON a."entity_type" = 'customer' AND tc."id" = a."entity_id"
  LEFT JOIN "subscriptions" tsu ON a."entity_type" = 'subscription' AND tsu."id" = a."entity_id"
  LEFT JOIN "packages" tp ON a."entity_type" = 'package' AND tp."id" = a."entity_id"
  LEFT JOIN "visits" tv ON a."entity_type" = 'visit' AND tv."id" = a."entity_id"
  LEFT JOIN "customers" tvc ON tvc."id" = tv."customer_id"
  LEFT JOIN "check_ins" tci ON a."entity_type" = 'checkIn' AND tci."id" = a."entity_id"
  LEFT JOIN "customers" tcc ON tcc."id" = tci."customer_id"
  LEFT JOIN "announcements" tan ON a."entity_type" = 'announcement' AND tan."id" = a."entity_id"`;

/**
 * The target's current name: a space's and a lookup's English (their Arabic apart); a person's, a
 * customer's, a subscription's, a package's; a visit's visitor, else its customer; a check-in's
 * customer.
 */
const TARGET_NAME = Prisma.sql`coalesce(ts."name_en", tu."name", tg."name_en", tar."name_en",
  tam."name_en", tc."name", tsu."name", tp."name", tv."visitor_name", tvc."name", tcc."name")`;
const TARGET_NAME_AR = Prisma.sql`coalesce(ts."name_ar", tg."name_ar", tar."name_ar", tam."name_ar")`;
/** A soft-deleted space or announcement. */
const TARGET_DELETED = Prisma.sql`coalesce(ts."deleted_at", tan."deleted_at") IS NOT NULL`;

/**
 * `q` against the target's names, and any other names given, as the directory searches
 * (`masaha_search_text`).
 */
const matches = (q: string, others: Prisma.Sql = Prisma.empty) =>
  Prisma.sql`strpos(masaha_search_text(concat_ws(' ', ${TARGET_NAME}, ${TARGET_NAME_AR}${others})),
    masaha_search_text(${q})) > 0`;

'''
s = s[:start] + new_block + s[end:]

reps = [
('''  target_deleted: boolean | null;
}''', '''  target_deleted: boolean;
}'''),
('''const ENTRY_COLUMNS = Prisma.sql`a."id", a."created_at", a."action", a."entity_type", a."entity_id",
  a."before", a."after", a."actor_id", t.name AS target_name, t.name_ar AS target_name_ar,
  t.deleted AS target_deleted`;''', '''const ENTRY_COLUMNS = Prisma.sql`a."id", a."created_at", a."action", a."entity_type", a."entity_id",
  a."before", a."after", a."actor_id", ${TARGET_NAME} AS target_name,
  ${TARGET_NAME_AR} AS target_name_ar, ${TARGET_DELETED} AS target_deleted`;'''),
('''  targetDeleted: row.target_deleted ?? false,
});''', '''  targetDeleted: row.target_deleted,
});'''),
]
for a, b in reps:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
n = len(re.findall(r'\bTARGET_JOIN\b', s))
s = re.sub(r'\bTARGET_JOIN\b', 'TARGET_JOINS', s)
assert ' t.' not in s and 't.name' not in s, 'a t. reference is left'
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok, renamed', n)
