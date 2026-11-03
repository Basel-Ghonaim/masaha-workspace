import io

W = r'C:\dev\masaha\app-lane-a\apps\web\src\features\announcements' + '\\'


def edit(p, pairs):
    p = W + p
    s = io.open(p, encoding='utf8', newline='').read()
    for a, b in pairs:
        assert s.count(a) == 1, (p, a)
        s = s.replace(a, b)
    io.open(p, 'w', encoding='utf8', newline='').write(s)


edit(r'hooks\list\useAnnouncementsList.ts', [
    ("""import type { Page } from '@shared/api';
import { useCopy } from '@shared/copy';""", """import { gazaClockOf } from '@masaha/shared/core';
import type { Page } from '@shared/api';
import { useCopy, type Catalogue } from '@shared/copy';"""),
    ("""import { paginationView, usePageInRange } from '@shared/lists';
import { useLanguage } from '@shared/localisation';""", """import { dayText } from '@shared/lib';
import { paginationView, usePageInRange } from '@shared/lists';
import { isolate, useLanguage } from '@shared/localisation';"""),
    ("""      closureLine: closureLine(announcement, owner, words.closure),""",
     """      closureLine: closureLine(announcement, owner, words, language),
      // The owner's, on a closure that has started and whose subscriptions were not extended (O11).
      extension:
        owner &&
        announcement.type === 'CLOSURE' &&
        announcement.state !== 'UPCOMING' &&
        (announcement.extension ?? null) === null
          ? { label: words.extension.action }
          : null,"""),
    ("""function closureLine(
  { type, state, extension }: ManagedAnnouncement,
  owner: boolean,
  words: { upcoming: string; reception: string },
): string | null {
  if (type !== 'CLOSURE') return null;
  if (state === 'UPCOMING') return owner ? words.upcoming : null;
  return !owner && (extension ?? null) === null ? words.reception : null;
}""", """function closureLine(
  { type, state, extension }: ManagedAnnouncement,
  owner: boolean,
  words: Catalogue['announcements'],
  language: 'ar' | 'en',
): string | null {
  if (type !== 'CLOSURE') return null;
  // Extended: how many, by how many days, by whom, when — to both roles.
  if (extension !== undefined && extension !== null) {
    return words.extension.line({
      count: words.extension.count({ count: extension.subscriptions }),
      days: words.extension.dayCount({ count: extension.days }),
      name: isolate(extension.appliedBy.name),
      date: dayText(gazaClockOf(new Date(extension.appliedAt)).date, language),
    });
  }
  if (state === 'UPCOMING') return owner ? words.closure.upcoming : null;
  return owner ? null : words.closure.reception;
}"""),
    (""" * A closure's line about its subscriptions' extension (DI-28): the owner's on one not started yet,
 * reception's on one started and not extended; none otherwise.""",
     """ * A closure's line about its subscriptions' extension (DI-28): once extended, how many, by how many
 * days, by whom and when; else the owner's on one not started yet, reception's on one started.""" ),
])

edit(r'types\AnnouncementCardView.ts', [
    ("""  edit: { label: string } | null;
};""", """  edit: { label: string } | null;
  /** «تمديد الاشتراكات», the owner's, on a started closure not extended (O11); else none. */
  extension: { label: string } | null;
};"""),
])
print('ok')
