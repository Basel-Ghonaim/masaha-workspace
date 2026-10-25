"""Commit 4's breaks: one at a time, its test file run, the output kept, the file restored from a copy."""
import sys
import breaks

D = 'features/desk'
S = f'src/{D}'
breaks.BREAKS.update({
    '14': (f'{D}/services/visitRates.ts', 'return (rowOf(terms, shiftId)?.student ?? null) !== null;', 'return true;', f'{S}/services/visitRates', 'unit'),
    '15': (f'{D}/services/currentShift.ts', 'const { minute } = gazaClockOf(now);', 'const minute = now.getUTCHours() * 60 + now.getUTCMinutes() + 0 * gazaClockOf(now).minute;', f'{S}/services/currentShift', 'unit'),
    '16': (f'{D}/services/moneyOf.ts', 'recorded: Math.min(received, due),', 'recorded: received,', f'{S}/services/moneyOf', 'unit'),
    '17': (f'{D}/services/quoteAge.ts', '> STALE_AFTER_MS', '>= STALE_AFTER_MS + 60_000', f'{S}/services/quoteAge', 'unit'),
    '18': (f'{D}/services/warningLines.ts', 'return (warnings ?? []).map((code) => errors[code]);', 'return [...(warnings ?? [])].sort().map((code) => errors[code]);', f'{S}/services/warningLines', 'unit'),
    '19': (f'{D}/repository/deskRepository.ts', 'body,\n        withIdempotencyKey(key),\n      ),\n  };', 'body,\n      ),\n  };', f'{S}/repository', 'unit'),
    '20': (f'{D}/hooks/check-in/useVisitDialog.ts', 'const answer = await checkIn.mutateAsync({ body: request, key });', 'renew();\n        const answer = await checkIn.mutateAsync({ body: request, key });', f'{S}/hooks/check-in', 'component'),
    '21': (f'{D}/hooks/check-in/useVisitDialog.ts', 'toastCheckedIn(request.visitorName, answer.meta?.warnings);', 'toastCheckedIn(request.visitorName, undefined);', f'{S}/hooks/check-in', 'component'),
    '22': (f'{D}/hooks/money/useMoneyBlock.ts', 'const parsed = typed === null ? due : agorotOf(typed);', 'const parsed = typed === null || typed !== \'\' ? due : agorotOf(typed);', f'{S}/hooks/money', 'component'),
    '23': (f'{D}/hooks/check-out/useCheckOutDialog.ts', "const amount = typeof money.amount === 'string' ? money.amount : money.recorded;", 'const amount = money.amount;', f'{S}/hooks/check-out', 'component'),
    '24': (f'{D}/hooks/check-out/useCheckOutDialog.ts', 'if (needsDebt && !debtShown) setDebtShown(true);', 'if (needsDebt !== debtShown) setDebtShown(needsDebt);', f'{S}/hooks/check-out', 'component'),
    '25': (f'{D}/hooks/check-out/useCheckOutDialog.ts', 'if (sent !== null && quoteIsStale(sent.at, new Date())) {', 'if (sent !== null && quoteIsStale(sent.at, new Date()) && Date.now() < 0) {', f'{S}/hooks/check-out', 'component'),
    '26': (f'{D}/hooks/check-out/useCheckOutDialog.ts', '...(live.current.typing', '...(live.current.typing && Date.now() < 0', f'{S}/hooks/check-out', 'component'),
    '27': (f'{D}/hooks/check-out/useCheckOutDialog.ts', 'failureLines: words.refusals,', '', f'{S}/hooks/check-out', 'component'),
    '28': (f'{D}/components/check-out/CheckOutDialog.tsx', '{dialog.failure !== null && <FormFailure view={dialog.failure} />}', "{dialog.failure !== null && <p>{dialog.failure.kind === 'refused' ? dialog.failure.message : ''}</p>}", f'{S}/components/check-out', 'component'),
    '29': ('pages/dashboard/space/desk/useSwitchStaff.ts', '    await signOut();\n', '    const next0 = new URLSearchParams({ next: spaceDeskPath(spaceId) });\n    await navigate(`${SIGN_IN_PATH}?${next0.toString()}`, { replace: true });\n    await signOut();\n', 'src/pages/dashboard/space/desk', 'component'),
    '30': ('pages/dashboard/routes.tsx', "  desk: async () => {\n    const { DeskPage } = await import('./space/desk/DeskPage');\n    return <DeskPage />;\n  },\n", '', 'src/pages/dashboard/routes', 'component'),
    'S10': ('features/occupancy/components/PresentList.tsx', '(target ?? heading.current)?.focus();', 'void target;', 'src/features/occupancy/components/PresentList', 'component'),
})

if __name__ == '__main__':
    for name in sys.argv[1:]:
        breaks.run(name)
