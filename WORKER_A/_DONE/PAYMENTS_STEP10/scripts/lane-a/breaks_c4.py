F = 'src/features/announcements/'
DIALOG_TEST = F + 'hooks/extension/useExtensionDialog.component.test.tsx'

BREAKS = [
    {
        'name': 'c4-25-extension-key-dropped',
        'file': F + 'repository/announcementsRepository.ts',
        'edits': [("        withIdempotencyKey(key),\n", "        key === '' ? withIdempotencyKey(key) : {},\n")],
        'lane': 'unit',
        'tests': [F + 'repository/announcementsRepository.unit.test.ts'],
    },
    {
        'name': 'c4-40-proposal-sent',
        'file': F + 'hooks/extension/useExtensionDialog.ts',
        'edits': [("const done = await extending.mutateAsync({ body, key });",
                   "const done = await extending.mutateAsync({\n          body: { days: answer?.proposedDays ?? body.days },\n          key,\n        });")],
        'lane': 'component',
        'tests': [DIALOG_TEST],
        'filter': 'reads the preview on opening',
    },
    {
        'name': 'c4-41-closed-on-failure',
        'file': F + 'hooks/extension/useExtensionDialog.ts',
        'edits': [("        setRefusal(failure);\n        throw error;\n",
                   "        setRefusal(failure);\n        onDone();\n        throw error;\n")],
        'lane': 'component',
        'tests': [DIALOG_TEST],
        'filter': 'keeps a failure in the dialog',
    },
    {
        'name': 'c4-42-action-to-reception',
        'file': F + 'hooks/list/useAnnouncementsList.ts',
        'edits': [("        owner &&\n        announcement.type === 'CLOSURE' &&",
                   "        announcement.type === 'CLOSURE' &&")],
        'lane': 'component',
        'tests': [DIALOG_TEST],
        'filter': 'reception reads its line instead',
    },
    {
        'name': 'c4-43-count-left-out',
        'file': F + 'hooks/extension/useExtensionDialog.ts',
        'edits': [("      label: words.submit({ count: answer?.subscriptions ?? 0 }),",
                   "      label: words.action,")],
        'lane': 'component',
        'tests': [F + 'components/extension/ExtensionDialog.component.test.tsx'],
    },
]
