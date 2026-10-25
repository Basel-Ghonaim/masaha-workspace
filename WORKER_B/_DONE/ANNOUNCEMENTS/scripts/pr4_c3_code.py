import io

R = 'C:/dev/masaha/app-b/'


def edit(path, pairs):
    p = R + path
    s = io.open(p, encoding='utf-8', newline='').read()
    for a, b in pairs:
        n = s.count(a)
        assert n == 1, (path, n, a[:70])
        s = s.replace(a, b)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)


# shared: the request, the answer, the code
edit('packages/shared/src/announcements/requests.ts', [
    ("export type AnnouncementsQuery = z.infer<typeof announcementsQuerySchema>;\n",
     """export type AnnouncementsQuery = z.infer<typeof announcementsQuerySchema>;

/** A closure's extension: the days every covered subscription's end moves, whole, 1–365 (S5). */
export const extendSubscriptionsSchema = z.object({
  days: z.number().int().min(1).max(EXTENSION_MAX_DAYS),
});
export type ExtendSubscriptionsRequest = z.infer<typeof extendSubscriptionsSchema>;
"""),
])
edit('packages/shared/src/announcements/responses.ts', [
    ("/**\n * A started closure's extension, before it is applied:",
     """/** A closure's extension as applied: the closure, its days, how many it moved, by whom, when. */
export type ClosureExtension = ExtensionApplied & { announcementId: number };

/**
 * A started closure's extension, before it is applied:"""),
])
edit('packages/shared/src/core/errors.ts', [
    ("  'CLOSURE_EXTENDED',\n",
     "  'CLOSURE_EXTENDED',\n  // a closure's subscriptions extended already, under another key (subscriptions)\n  'CLOSURE_ALREADY_EXTENDED',\n"),
])
edit('apps/web/src/shared/copy/arabic/errors.ts', [
    ("    'مُدّدت الاشتراكات بسبب هذا الإغلاق، فلا يمكن حذفه ولا تغيير نوعه أو بدايته ولا تأخير نهايته.',\n",
     "    'مُدّدت الاشتراكات بسبب هذا الإغلاق، فلا يمكن حذفه ولا تغيير نوعه أو بدايته ولا تأخير نهايته.',\n  CLOSURE_ALREADY_EXTENDED: 'مُدّدت اشتراكات هذا الإغلاق من قبل.',\n"),
])
edit('apps/web/src/shared/copy/english/errors.ts', [
    ("    'Subscriptions were extended for this closure: it is not deleted, and its type, start and later end stay as they are.',\n",
     "    'Subscriptions were extended for this closure: it is not deleted, and its type, start and later end stay as they are.',\n  CLOSURE_ALREADY_EXTENDED: \"This closure's subscriptions were already extended.\",\n"),
])

# announcements: the closure locked
edit('apps/api/src/modules/announcements/announcements.service.ts', [
    ("    /** The ids of the space's closures, not deleted, started by `at` and not before `since`. */",
     """    /**
     * Locks the space's closure's row (`FOR UPDATE`), not deleted, for its extension, and answers
     * it: else `not_found`. The caller holds the space's lock first (conventions §13).
     */
    async lockClosure(spaceId: number, id: number, tx: Tx): Promise<AnnouncementRow> {
      const row = await repository.lockIn(spaceId, id, tx);
      if (row?.type !== 'CLOSURE') throw AppError.notFound(undefined, 'Closure not found');
      return row;
    },

    /** The ids of the space's closures, not deleted, started by `at` and not before `since`. */"""),
])
print('ok')
