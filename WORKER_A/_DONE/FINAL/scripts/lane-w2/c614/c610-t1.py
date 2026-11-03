import os
os.chdir('C:/dev/masaha/app-lane-w2/apps/web/src')


def edit(p, pairs):
    s = open(p, encoding='utf8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)


edit('features/spaces/components/editor/SpaceEditor.component.test.tsx', [
("""  owner = false,
}: {
  read?: () => FakeAnswer | Promise<FakeAnswer>;
  photos?: () => FakeAnswer | Promise<FakeAnswer>;
  write?: (request: Request) => FakeAnswer | Promise<FakeAnswer>;
  owner?: boolean;
} = {}) {""", """  owner = false,
  noticeFor,
  entry = '/spaces/7',
}: {
  read?: () => FakeAnswer | Promise<FakeAnswer>;
  photos?: () => FakeAnswer | Promise<FakeAnswer>;
  write?: (request: Request) => FakeAnswer | Promise<FakeAnswer>;
  owner?: boolean;
  noticeFor?: (group: FactGroup) => ReactNode;
  entry?: string;
} = {}) {"""),
("""            publicLink={(slug) => `/spaces/${slug}`}
          />
        ),
      },
      { path: '/elsewhere', element: <p>Elsewhere</p> },
    ],
    { initialEntries: ['/spaces/7'] },
  );""", """            publicLink={(slug) => `/spaces/${slug}`}
            noticeFor={noticeFor}
          />
        ),
      },
      { path: '/elsewhere', element: <p>Elsewhere</p> },
    ],
    { initialEntries: [entry] },
  );"""),
("""describe('a section of the editor', () => {""", """describe('the editor’s landing and notices', () => {
  it('a report in the address shows its notice above its section', async () => {
    renderEditor({
      noticeFor: (group) => (group === 'hours' ? <p>The report’s notice</p> : null),
    });

    const hours = (await screen.findByRole('heading', { level: 2, name: 'Opening hours' })).closest(
      '[data-slot=card]',
    );
    const marker = screen.getByText('The report’s notice');
    expect(screen.getAllByText('The report’s notice')).toHaveLength(1);
    // Drawn just before the section, inside the sections' column.
    expect(marker.nextElementSibling).toBe(hours);
  });

  it('the editor scrolls to and focuses the card its hash names once drawn', async () => {
    const read = deferred<FakeAnswer>();
    renderEditor({ read: () => read.promise, entry: '/spaces/7?report=5#hours' });

    expect(await screen.findByRole('status')).toBeInTheDocument();
    read.resolve(ok(SPACE));

    const heading = await screen.findByRole('heading', { level: 2, name: 'Opening hours' });
    await waitFor(() => {
      expect(heading).toHaveFocus();
    });
  });

  it('lands on a section’s inner part, and on nothing the page does not hold', async () => {
    renderEditor({ entry: '/spaces/7#location' });

    const location = await screen.findByRole('heading', { level: 3, name: 'Location' });
    await waitFor(() => {
      expect(location).toHaveFocus();
    });
  });
});

describe('a section of the editor', () => {"""),
])
print('ok')
