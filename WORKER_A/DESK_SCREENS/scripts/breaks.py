"""Applies one break at a time, runs its test file, records the output, and restores the file from a copy.

Usage: python breaks.py <name>   (the breaks are listed in BREAKS below; 'all' runs every one of a set)
Writes scripts/break-<name>.txt and prints its last lines. Restores the file whatever happens.
"""
import shutil
import subprocess
import sys
from pathlib import Path

APP = Path('C:/dev/masaha/app')
WEB = APP / 'apps/web/src'
OUT = Path('C:/dev/masaha/workspace/WORKER_A/DESK_SCREENS/scripts')

OCC = 'features/occupancy'
BREAKS = {
    '6a': (f'{OCC}/hooks/now/useStateNowQuery.ts', 'refetchIntervalInBackground: false', 'refetchIntervalInBackground: true', f'src/{OCC}/hooks/now/useStateNowQuery'),
    '6b': (f'{OCC}/hooks/now/useStateNowQuery.ts', "refetchOnWindowFocus: 'always'", 'refetchOnWindowFocus: false', f'src/{OCC}/hooks/now/useStateNowQuery'),
    '7': (f'{OCC}/hooks/now/usePresentList.ts', 'isolate(priceText(person.chargeNowAgorot, language))', 'isolate(priceText(stayDuration(person.since, now).hours * 500, language))', f'src/{OCC}/hooks/now/usePresentList'),
    '8': (f'{OCC}/hooks/now/usePresentList.ts', 'const people = data?.people ?? [];', 'const people = query.isError ? [] : (data?.people ?? []);', f'src/{OCC}/hooks/now/usePresentList'),
    '10': (f'{OCC}/components/PresentList.tsx', 'label={list.label}', 'label={list.heading.title}', f'src/{OCC}/components/PresentList'),
    '12': (f'{OCC}/hooks/status/useLiveStatusControl.ts', "disabled: data?.status === 'CLOSED' && override === null,", 'disabled: false,', f'src/{OCC}/hooks/status/useLiveStatusControl'),
    '13': (f'{OCC}/components/LiveStatusControl.tsx', 'aria-label={trigger.name}', '', f'src/{OCC}/components/LiveStatusControl'),
}


def run(name: str) -> None:
    rel, old, new, test, *lane = BREAKS[name]
    lane = lane[0] if lane else 'component'
    path = WEB / rel
    backup = OUT / f'bak-break-{name}{path.suffix}'
    shutil.copyfile(path, backup)
    try:
        text = path.read_text(encoding='utf-8')
        if text.count(old) != 1:
            raise SystemExit(f'break {name}: the text to break is not there once')
        path.write_text(text.replace(old, new), encoding='utf-8', newline='')
        result = subprocess.run(
            f'npm run test:{lane} -w @masaha/web -- {test}',
            cwd=APP, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace',
        )
        output = result.stdout + result.stderr
        (OUT / f'break-{name}.txt').write_text(output, encoding='utf-8')
        lines = [line for line in output.splitlines() if '×' in line or 'Tests ' in line]
        print(f'break {name} exit {result.returncode}:', *lines[:6], sep='\n  ')
    finally:
        shutil.copyfile(backup, path)
    assert path.read_bytes() == backup.read_bytes()


if __name__ == '__main__':
    names = sys.argv[1:]
    for name in names:
        run(name)
