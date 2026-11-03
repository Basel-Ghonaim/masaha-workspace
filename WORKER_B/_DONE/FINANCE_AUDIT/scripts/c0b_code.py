import io
import os

os.chdir(r'C:\dev\masaha\app-b\apps\api\src\modules\subscriptions\closures')


def edit(path, reps):
    s = io.open(path, encoding='utf-8', newline='').read()
    for a, b in reps:
        assert s.count(a) == 1, (path, a[:90])
        s = s.replace(a, b)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)


edit('closures.repository.ts', [
('''/** A closure's extension as the managed list shows it: its days, how many it moved, who, when. */
export interface ExtensionRow {
  announcementId: number;
''', '''/** A closure's extension as the managed list shows it: its days, how many it moved, who, when. */
export interface ExtensionRow {
  announcementId: number;
  /** The closure's space: a retried key is answered on that space's URL only. */
  spaceId: number;
'''),
('''const EXTENSION = {
  announcementId: true,
''', '''const EXTENSION = {
  announcementId: true,
  announcement: { select: { spaceId: true } },
'''),
('''const toExtensionRow = ({
  announcementId,
  days,
  appliedById,
  createdAt,
  _count,
}: Prisma.ClosureExtensionGetPayload<{ select: typeof EXTENSION }>): ExtensionRow => ({
  announcementId,
''', '''const toExtensionRow = ({
  announcementId,
  announcement,
  days,
  appliedById,
  createdAt,
  _count,
}: Prisma.ClosureExtensionGetPayload<{ select: typeof EXTENSION }>): ExtensionRow => ({
  announcementId,
  spaceId: announcement.spaceId,
'''),
('''    /** The extension this key applied, with the count of its subscriptions; `null` for none. */''',
 '''    /**
     * The extension this key applied, of whichever space (the key is unique on its own), with the
     * count of its subscriptions and its closure's space; `null` for none.
     */'''),
])

edit('closures.service.ts', [
('''   * id): the space's lock; `can()` on the links read under it; the extension this key applied, for
     * a retry, answered as it was (another closure's → `conflict`); the closure, locked (else''',
 '''   * id): the space's lock; `can()` on the links read under it; the extension this key applied, for
     * a retry, answered as it was (another closure's, or another space's, → `conflict`, answering
     * nothing of it); the closure, locked (else'''),
('''        if (recorded) {
          if (recorded.announcementId !== announcementId) {
            throw AppError.conflict(undefined, 'This idempotency key extended another closure');
          }''', '''        if (recorded) {
          // Another space's extension is the same conflict, so the key tells nothing of that space.
          if (recorded.spaceId !== space.id || recorded.announcementId !== announcementId) {
            throw AppError.conflict(undefined, 'This idempotency key extended another closure');
          }'''),
])
print('ok')
