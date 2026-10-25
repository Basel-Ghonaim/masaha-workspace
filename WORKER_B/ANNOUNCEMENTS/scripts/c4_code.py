R = 'C:/dev/masaha/app-b/'


def ed(p, pairs):
    s = open(R + p, encoding='utf-8', newline='').read()
    for a, b in pairs:
        assert s.count(a) == 1, (p, a[:80])
        s = s.replace(a, b)
    open(R + p, 'w', encoding='utf-8', newline='').write(s)


ed('packages/shared/src/directory/responses.ts', [
("import type { AmenityIconKey } from '../lookups/index.ts';",
 "import type { AnnouncementType } from '../announcements/index.ts';\nimport type { AmenityIconKey } from '../lookups/index.ts';"),
("""/** A space's public page. */
export interface PublicSpace {""", """/** The most announcements a space's page carries. */
export const PUBLIC_ANNOUNCEMENTS_MAX = 20;

/** An announcement as a space's page shows it: running or upcoming; instants with their offset. */
export interface PublicAnnouncement {
  id: number;
  type: AnnouncementType;
  textAr: string;
  textEn: string | null;
  startsAt: string;
  endsAt: string | null;
}

/** A space's public page. */
export interface PublicSpace {"""),
("""  /** Its photos in the gallery's order, the cover first, each in both sizes; none: a caption. */
  photos: PhotoUrls[];
}""", """  /** Its photos in the gallery's order, the cover first, each in both sizes; none: a caption. */
  photos: PhotoUrls[];
  /** Its running and upcoming announcements, by start then id, at most `PUBLIC_ANNOUNCEMENTS_MAX`. */
  announcements: PublicAnnouncement[];
}"""),
])

ed('apps/api/src/modules/announcements/announcements.repository.ts', [
("""    update(
      id: number,""", """    /**
     * The space's announcements the public sees at `now`: not deleted, not ended (running or
     * upcoming), by start, then id, at most `take`.
     */
    publicOf(spaceId: number, now: Date, take: number): Promise<AnnouncementRow[]> {
      return prisma.announcement.findMany({
        where: { spaceId, deletedAt: null, OR: [{ endsAt: null }, { endsAt: { gt: now } }] },
        orderBy: [{ startsAt: 'asc' }, { id: 'asc' }],
        take,
        select: ANNOUNCEMENT,
      });
    },

    update(
      id: number,"""),
])

ed('apps/api/src/modules/announcements/announcements.service.ts', [
("""    /** How many of the space's announcements are in each state at `at`, in one query. */""",
"""    /**
     * The space's running and upcoming announcements now, by start then id, at most `take`: what its
     * public page shows. Read without a lock.
     */
    async publicOf(spaceId: number, take: number): Promise<Announcement[]> {
      const at = now();
      const rows = await repository.publicOf(spaceId, at, take);
      return rows.map((row) => toAnnouncement(row, at));
    },

    /** How many of the space's announcements are in each state at `at`, in one query. */"""),
])

ed('apps/api/src/modules/directory/directory.service.ts', [
("""interface Dependencies {
  lookups: LookupsService;""", """interface Dependencies {
  announcements: AnnouncementsService;
  lookups: LookupsService;"""),
("""      const [[area], amenities] = await Promise.all([
        lookups.areaNamesFor([view.areaId]),
        view.amenityIds.length === 0 ? [] : lookups.activeAmenitiesNamed(view.amenityIds),
      ]);""", """      // Read after the space's share lock: an announcement is no fact group, and one posted between
      // the two reads shows on the next.
      const [[area], amenities, shownAnnouncements] = await Promise.all([
        lookups.areaNamesFor([view.areaId]),
        view.amenityIds.length === 0 ? [] : lookups.activeAmenitiesNamed(view.amenityIds),
        announcements.publicOf(view.id, PUBLIC_ANNOUNCEMENTS_MAX),
      ]);"""),
("""        photos: view.photos,
      };
    },
  };
}""", """        photos: view.photos,
        announcements: shownAnnouncements.map(
          ({ id, type, textAr, textEn, startsAt, endsAt }) => ({
            id,
            type,
            textAr,
            textEn,
            startsAt,
            endsAt,
          }),
        ),
      };
    },
  };
}"""),
])

ed('apps/api/src/app.ts', [
("""  const directory = createDirectoryService({
    lookups,""", """  const directory = createDirectoryService({
    announcements,
    lookups,"""),
])
print('ok')
