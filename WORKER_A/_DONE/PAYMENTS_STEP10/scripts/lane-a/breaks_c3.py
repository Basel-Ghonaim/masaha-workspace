F = 'src/features/announcements/'

BREAKS = [
    {
        'name': 'c3-36-undo-on-extended',
        'file': F + 'hooks/actions/useAnnouncementActions.ts',
        'edits': [("          undo: extended\n            ? null\n", "          undo: !extended\n            ? null\n")],
        'lane': 'component',
        'tests': [F + 'hooks/actions/useAnnouncementActions.component.test.tsx'],
        'filter': 'extended closure’s end now',
    },
    {
        'name': 'c3-37-delete-on-extended',
        'file': F + 'hooks/actions/useAnnouncementActions.ts',
        'edits': [("      remove: extended ? null : { label: words.actions.delete },",
                   "      remove: { label: words.actions.delete },")],
        'lane': 'component',
        'tests': [F + 'hooks/actions/useAnnouncementActions.component.test.tsx'],
        'filter': 'never offers',
    },
    {
        'name': 'c3-38-one-text',
        'file': F + 'hooks/actions/useDeleteDialog.ts',
        'edits': [("    text:\n      announcement.state === 'RUNNING'\n",
                   "    text:\n      announcement.state !== 'ENDED' || words.running\n        ? words.running\n        : announcement.state === 'RUNNING'\n")],
        'lane': 'component',
        'tests': [F + 'hooks/actions/useDeleteDialog.component.test.tsx'],
    },
    {
        'name': 'c3-39-focus-on-body',
        'file': F + 'hooks/list/useCardFocus.ts',
        'edits': [("function move(keeper: Keeper, key: string) {\n  keeper.held.current = null;\n",
                   "function move(keeper: Keeper, key: string) {\n  keeper.held.current = null;\n  if (key !== '') return;\n")],
        'lane': 'component',
        'tests': [F + 'components/actions/AnnouncementMenu.component.test.tsx'],
    },
]

BREAKS.append({
    'name': 'c3-25-end-path',
    'file': F + 'repository/announcementsRepository.ts',
    'edits': [("/${String(id)}/end`)", "/${String(id)}/finish`)")],
    'lane': 'unit',
    'tests': [F + 'repository/announcementsRepository.unit.test.ts'],
})
