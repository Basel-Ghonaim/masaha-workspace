F = 'src/features/announcements/'

BREAKS = [
    {
        'name': 'c1-26-browser-zone',
        'file': F + 'services/periodText.ts',
        'edits': [(
            "    const { date, minute } = gazaClockOf(new Date(instant));\n",
            "    const local = new Date(instant);\n"
            "    const date = `${String(local.getFullYear())}-${String(local.getMonth() + 1).padStart(2, '0')}-${String(local.getDate()).padStart(2, '0')}`;\n"
            "    const minute = local.getHours() * 60 + local.getMinutes();\n",
        )],
        'lane': 'unit',
        'tests': [F + 'services/periodText.unit.test.ts'],
    },
    {
        'name': 'c1-27-closure-neutral',
        'file': F + 'services/typeView.ts',
        'edits': [("const WARNS: readonly AnnouncementType[] = ['OUTAGE', 'CLOSURE'];",
                   "const WARNS: readonly AnnouncementType[] = ['OUTAGE'];")],
        'lane': 'unit',
        'tests': [F + 'services/typeView.unit.test.ts'],
    },
    {
        'name': 'c1-28-tab-not-in-address',
        'file': F + 'services/announcementsQueryOf.ts',
        'edits': [("  if (state !== 'RUNNING') params.set('state', WORDS[state]);\n", "")],
        'lane': 'component',
        'tests': [F + 'hooks/list/useAnnouncementsList.component.test.tsx'],
    },
    {
        'name': 'c1-29-pages-always',
        'file': F + 'hooks/list/useAnnouncementsList.ts',
        'edits': [("      total: answer?.meta.totalPages ?? 0,\n",
                   "      total: Math.max(2, answer?.meta.totalPages ?? 0),\n")],
        'lane': 'component',
        'tests': [F + 'hooks/list/useAnnouncementsList.component.test.tsx'],
    },
    {
        'name': 'c1-30-status-badge',
        'file': F + 'components/list/AnnouncementCard.tsx',
        'edits': [("        <CardDescription>{card.period}</CardDescription>\n",
                   "        <CardDescription>{card.period}</CardDescription>\n"
                   "        <Badge variant=\"success\">Active</Badge>\n")],
        'lane': 'component',
        'tests': [F + 'components/list/AnnouncementsList.component.test.tsx'],
    },
    {
        'name': 'c1-44-placeholder-kept',
        'file': 'src/pages/dashboard/routes.tsx',
        'edits': [("  announcements: async () => {\n"
                   "    const { AnnouncementsPage } = await import('./space/announcements/AnnouncementsPage');\n"
                   "    return <AnnouncementsPage />;\n"
                   "  },\n", "")],
        'lane': 'component',
        'tests': ['src/pages/dashboard/routes.component.test.tsx'],
        'filter': "the space's announcements",
    },
]
