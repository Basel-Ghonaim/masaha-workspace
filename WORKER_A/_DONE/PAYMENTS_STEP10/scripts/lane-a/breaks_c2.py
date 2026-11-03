F = 'src/features/announcements/'
SHEET_TEST = F + 'hooks/sheet/useAnnouncementSheet.component.test.tsx'

BREAKS = [
    {
        'name': 'c2-25-key-dropped',
        'file': F + 'repository/announcementsRepository.ts',
        'edits': [("api.post<Announcement>(pathOf(spaceId), body, withIdempotencyKey(key))",
                   "api.post<Announcement>(pathOf(spaceId), body, key === '' ? withIdempotencyKey(key) : {})")],
        'lane': 'unit',
        'tests': [F + 'repository/announcementsRepository.unit.test.ts'],
    },
    {
        'name': 'c2-31-browser-zone',
        'file': F + 'services/sheetRequest.ts',
        'edits': [("  return gazaInstant(date, minute).toISOString();",
                   "  return new Date(`${date}T${time}:00`).toISOString();")],
        'lane': 'unit',
        'tests': [F + 'services/sheetRequest.unit.test.ts'],
    },
    {
        'name': 'c2-32-renew-each-submit',
        'file': F + 'hooks/sheet/useAnnouncementSheet.ts',
        'edits': [("await create.mutateAsync({ body: body as CreateAnnouncementRequest, key })",
                   "await create.mutateAsync({ body: body as CreateAnnouncementRequest, key: crypto.randomUUID() })")],
        'lane': 'component',
        'tests': [SHEET_TEST],
        'filter': 'posts with one key',
    },
    {
        'name': 'c2-33-field-lines-left-out',
        'file': F + 'hooks/sheet/useAnnouncementSheet.ts',
        'edits': [("    fields: ['type', 'textAr', 'textEn', 'startsAt', 'endsAt'],",
                   "    fields: ['type', 'textAr', 'textEn'],")],
        'lane': 'component',
        'tests': [SHEET_TEST],
        'filter': 'period refusals',
    },
    {
        'name': 'c2-34-tab-not-named',
        'file': F + 'components/toast/announcementToasts.tsx',
        'edits': [("    description: words.toast.inTab({ tab: words.tabs[state] }),\n", "")],
        'lane': 'component',
        'tests': [SHEET_TEST],
        'filter': 'names the tab',
    },
    {
        'name': 'c2-35-focus-on-group',
        'file': F + 'components/sheet/AnnouncementSheet.tsx',
        'edits': [("'[data-slot=\"radio-group-item\"][aria-checked=\"true\"]'",
                   "'[data-slot=\"radio-group-item\"]'")],
        'lane': 'component',
        'tests': [F + 'components/sheet/AnnouncementSheet.component.test.tsx'],
    },
]

BREAKS.append({
    'name': 'c2-25b-edit-not-patch',
    'file': F + 'repository/announcementsRepository.ts',
    'edits': [("api.patch<Announcement>(", "api.put<Announcement>(")],
    'lane': 'unit',
    'tests': [F + 'repository/announcementsRepository.unit.test.ts'],
})
