p = 'C:/dev/masaha/app/apps/web/src/features/desk/components/menu/CustomerActions.component.test.tsx'
s = open(p, encoding='utf-8').read()
rep = [
    ("""import { act, render, screen, waitFor, within } from '@testing-library/react';""",
     """import { act, render, screen, waitFor, within } from '@testing-library/react';
import { useRef, useState } from 'react';"""),
    ("""import { CustomerActions } from './CustomerActions';""",
     """import { SubscriptionSheet } from '../sheet/SubscriptionSheet';
import type { SheetEntry } from '../../types/SheetEntry';
import { CustomerActions } from './CustomerActions';"""),
]
for a, b in rep:
    assert s.count(a) == 1, a
    s = s.replace(a, b)

TESTS = """
  it('gives the focus back to «⋯» once the subscription sheet it opened is closed', async () => {
    const user = userEvent.setup();
    fakeTransport(() => ok(null));
    /** A page holding the one sheet, as the dashboard's pages do. */
    function Page() {
      const [entry, setEntry] = useState<SheetEntry | null>(null);
      const from = useRef<HTMLElement | null>(null);
      return (
        <main>
          <CustomerActions
            spaceId={7}
            customer={SARA}
            debtAgorot={0}
            owner={false}
            fileLink={null}
            subscribe={(next, trigger) => {
              from.current = trigger;
              setEntry(next);
            }}
          />
          {entry !== null && (
            <SubscriptionSheet
              spaceId={7}
              entry={entry}
              choices={{
                state: 'ready',
                packages: [],
                retry: vi.fn(),
                prices: { state: 'ready', list: [], refresh: vi.fn() },
                shifts: [],
              }}
              returnFocus={() => from.current}
              onClose={() => {
                setEntry(null);
              }}
            />
          )}
        </main>
      );
    }
    render(
      <QueryClientProvider client={createQueryClient()}>
        <MemoryRouter>
          <Page />
        </MemoryRouter>
      </QueryClientProvider>,
    );
    const trigger = screen.getByRole('button', { name: /More actions: .Sara Khalid./ });

    await user.click(trigger);
    await user.click(await screen.findByRole('menuitem', { name: 'New subscription' }));
    await screen.findByRole('dialog');
    await user.keyboard('{Escape}');

    await waitFor(() => {
      expect(screen.queryByRole('dialog')).toBeNull();
    });
    expect(trigger).toHaveFocus();
  });
});
"""
s = s.rstrip()
assert s.endswith('});')
s = s[:-3].rstrip() + '\n' + TESTS
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
