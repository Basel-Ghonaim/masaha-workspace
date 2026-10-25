"""DESK_SCREENS PR 2's breaks: each made on a copy, its lane run, the file restored and checked."""
import filecmp
import io
import shutil
import subprocess
import sys

S = 'C:/dev/masaha/workspace/WORKER_A/DESK_SCREENS/scripts'
W = 'C:/dev/masaha/app/apps/web/src/features/desk/'
NL = '\n'

BREAKS = [
    ('52', 'services/openItems.ts',
     "    .filter(({ balanceAgorot }) => balanceAgorot !== null)" + NL, "",
     ['unit', 'src/features/desk/services/openItems']),
    ('53', 'hooks/pay/usePayDialog.ts',
     "      choose: setChosenKey,",
     "      choose: (key: string) => {" + NL + "        setChosenKey(key);" + NL
     + "        money.received.change(null as unknown as string);" + NL + "      },",
     ['component', 'src/features/desk/hooks/pay']),
    ('45', 'hooks/search/useDeskSearch.ts',
     "        : answer === undefined" + NL + "          ? ('failed' as const)" + NL + "          : ('ready' as const);",
     "        : ('ready' as const);",
     ['component', 'src/features/desk/hooks/search']),
    ('46', 'hooks/search/useDeskSearch.ts',
     "      autoFocus: wide,", "      autoFocus: wide || true,",
     ['component', 'src/features/desk/components/search']),
    ('47', 'services/balanceView.ts',
     "  return { label: words.settled, tone: 'neutral' };",
     "  return null as unknown as BalanceView;",
     ['unit', 'src/features/desk/services/balanceView']),
    ('48a', 'hooks/subscriber/useSubscriberCheckIn.ts',
     "  const runs = current?.status === 'ACTIVE' || current?.status === 'ENDING_SOON';",
     "  const runs = false as boolean;",
     ['component', 'src/features/desk/hooks/subscriber/useSubscriberCheckIn']),
    ('48b', 'hooks/subscriber/useSubscriberCheckIn.ts',
     "      subscriberKey.renew();" + NL, "",
     ['component', 'src/features/desk/hooks/subscriber/useSubscriberCheckIn']),
    ('49', 'hooks/subscriber/useSubscriberCheckIn.ts',
     "      toastSubscriberIn(row.name, answer.meta?.warnings);" + NL + "      done();",
     "      toastSubscriberIn(row.name, answer.meta?.warnings);",
     ['component', 'src/features/desk/hooks/subscriber/useSubscriberCheckIn']),
    ('50', 'hooks/subscriber/useCheckOutSubscriber.ts',
     "        toastSubscriberOut(person.name, answer);",
     "        toastSubscriberOut(person.name, answer);" + NL
     + "        (document.activeElement as HTMLElement | null)?.blur();",
     ['component', 'src/features/desk/hooks/subscriber/useCheckOutSubscriber']),
]


def run(name, rel, before, after, lane, path):
    f = W + rel
    bak = f'{S}/bak-pr2-break-{name}'
    shutil.copyfile(f, bak)
    s = io.open(f, encoding='utf-8', newline='').read()
    assert s.count(before) == 1, (name, before)
    io.open(f, 'w', encoding='utf-8', newline='').write(s.replace(before, after))
    try:
        out = subprocess.run(f'npm run test:{lane} -w @masaha/web -- {path}', shell=True,
                             capture_output=True, text=True, encoding='utf-8', errors='replace',
                             cwd='C:/dev/masaha/app')
    finally:
        shutil.copyfile(bak, f)
        assert filecmp.cmp(f, bak, shallow=False)
    text = out.stdout + out.stderr
    io.open(f'{S}/break-pr2-{name}.txt', 'w', encoding='utf-8').write(text)
    lines = [line for line in text.splitlines() if '×' in line or 'Tests ' in line]
    print(f'break {name}:', *lines, 'restored', sep=NL + '  ')


only = sys.argv[1:]
for b in BREAKS:
    if not only or b[0] in only:
        run(*b[:4], *b[4])
