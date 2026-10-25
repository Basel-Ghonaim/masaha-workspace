R = 'C:/dev/masaha/app-b/docs/'


def ed(p, pairs):
    s = open(R + p, encoding='utf-8', newline='').read()
    for a, b in pairs:
        assert s.count(a) == 1, (p, a[:80])
        s = s.replace(a, b)
    open(R + p, 'w', encoding='utf-8', newline='').write(s)


ed('api/api-contract.md', [
("""  photos: PhotoUrls[]                      // in the gallery's order, the cover first; none: the page shows a caption
}""", """  photos: PhotoUrls[],                     // in the gallery's order, the cover first; none: the page shows a caption
  announcements: PublicAnnouncement[]      // running and upcoming, by start then id, at most 20
}

PublicAnnouncement = {
  id: number,
  type: 'GENERAL' | 'OUTAGE' | 'CLOSURE' | 'OFFER' | 'EVENT',
  textAr: string, textEn: string | null,
  startsAt: string, endsAt: string | null  // none: until it is ended
}"""),
("""- **200:** `PublicSpace`. Read whole, as the admin's read is, so a save in progress is never half shown.""",
"""- **200:** `PublicSpace`. Read whole, as the admin's read is, so a save in progress is never half shown. Its `announcements` are the space's running and upcoming ones, never an ended or a deleted one, read after the space's facts: one posted between the two reads shows on the next; an announcement that starts or ends shows within the answer's 30 seconds (2026-10-24, #PRNUM)."""),
("""- the open check-ins (`GET /manage/spaces/:spaceId/check-ins?open=true`), bounded by who is present (§5, *Front desk (managed)*; 2026-10-22, #109).""",
"""- the open check-ins (`GET /manage/spaces/:spaceId/check-ins?open=true`), bounded by who is present (§5, *Front desk (managed)*; 2026-10-22, #109);
- a space's announcements on its page (`GET /spaces/:slug`), its running and upcoming ones, at most 20: a space posts tens at most, and the page shows them together (§5, *Directory (public)*; 2026-10-24, #PRNUM)."""),
])
print('ok')
