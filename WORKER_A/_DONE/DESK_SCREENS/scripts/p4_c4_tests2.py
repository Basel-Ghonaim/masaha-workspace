p = 'C:/dev/masaha/app/apps/web/src/features/desk/hooks/sheet/useSubscriptionSheet.component.test.tsx'
s = open(p, encoding='utf-8').read()
rep = [
    ("    statement?: FakeAnswer;", "    statement?: () => FakeAnswer;"),
    ("      return statement ?? ok({});", "      return statement?.() ?? ok({});"),
    ("    const statement = (renewal: { startsOn: string } | null) =>",
     "    const statementOf = (renewal: { startsOn: string } | null) =>"),
    ("        statement: statement({ startsOn: '2026-11-05' }),",
     "        statement: () => statementOf(renewal),"),
    ("    expect(await within(sheet).findByText(/This subscription was already renewed\\./)).toBeVisible();",
     """    expect(
      (await within(sheet).findAllByText(/This subscription was already renewed\\./))[0],
    ).toBeVisible();
    // Read again, the statement says it was renewed: the sheet now makes a new subscription.
    expect(await screen.findByRole('dialog', { name: 'New subscription' })).toBeVisible();"""),
    ("    expect(renewal).toBeNull();\n", ""),
]
for a, b in rep:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
