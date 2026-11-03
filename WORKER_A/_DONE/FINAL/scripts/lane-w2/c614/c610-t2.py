import os
os.chdir('C:/dev/masaha/app-lane-w2/apps/web/src/features/data-reports/components')


def edit(p, pairs):
    s = open(p, encoding='utf8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)


edit('space/SpaceReportsList.component.test.tsx', [
("""            <SpaceReportsList spaceId={7} fieldLink={(field) => `/profile#${field}`} />""",
 """            <SpaceReportsList
              spaceId={7}
              fieldLink={(field, reportId) => `/profile?report=${String(reportId)}#${field}`}
            />"""),
("""      '/profile#HOURS',
    );""", """      '/profile?report=41#HOURS',
    );"""),
("""describe('SpaceReportsList', () => {""", """describe('SpaceReportsList', () => {
  it('?open= opens that report’s sheet, read by its id when the page does not show it', async () => {
    const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime.bind(vi) });
    const { router, requests } = renderList((request) =>
      request.url === '/manage/spaces/7/data-reports/99'
        ? ok(spaceReport({ id: 99, field: 'AMENITIES' }))
        : reportsPage([spaceReport()]),
      '?open=99',
    );

    const sheet = await screen.findByRole('dialog', { name: 'Report about Amenities' });
    expect(requests.map(({ url }) => url)).toContain('/manage/spaces/7/data-reports/99');
    await user.click(within(sheet).getByRole('button', { name: 'Close' }));

    await waitFor(() => {
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    });
    expect(router.state.location.search).toBe('');
  });

  it('?open= opens a report the page shows without reading it again', async () => {
    const { requests } = renderList(() => reportsPage([spaceReport()]), '?open=41');

    expect(
      await screen.findByRole('dialog', { name: 'Report about Opening hours' }),
    ).toBeInTheDocument();
    expect(requests.map(({ url }) => url)).not.toContain('/manage/spaces/7/data-reports/41');
  });
"""),
])

edit('admin/AdminReportsList.component.test.tsx', [
("""function renderList(
  search = '',
  answer: Parameters<typeof fakeTransport>[0] = () => reportsPage([adminReport()]),
) {
  fakeTransport(answer);""", """function renderList(
  search = '',
  answer: Parameters<typeof fakeTransport>[0] = () => reportsPage([adminReport()]),
) {
  const requests = fakeTransport(answer);"""),
("""            editorLink={(spaceId) => `/spaces/${String(spaceId)}`}
          />
        ),
      },
    ],
    { initialEntries: [`/reports${search}`] },
  );
  return render(
    <QueryClientProvider client={createQueryClient()}>
      <RouterProvider router={router} />
    </QueryClientProvider>,
  );
}""", """            editorLink={(spaceId, field, reportId) =>
              field === undefined
                ? `/spaces/${String(spaceId)}`
                : `/spaces/${String(spaceId)}?report=${String(reportId)}#${field}`
            }
          />
        ),
      },
    ],
    { initialEntries: [`/reports${search}`] },
  );
  const view = render(
    <QueryClientProvider client={createQueryClient()}>
      <RouterProvider router={router} />
    </QueryClientProvider>,
  );
  return { ...view, router, requests };
}"""),
("""describe('AdminReportsList', () => {""", """describe('AdminReportsList', () => {
  it('?open= opens that report’s sheet, read by its id, «Edit the field» carrying it', async () => {
    const { router, requests } = renderList('?open=99', (request) =>
      request.url === '/admin/data-reports/99'
        ? ok(adminReport({ id: 99, field: 'CONTACT' }))
        : reportsPage([adminReport()]),
    );

    const sheet = await screen.findByRole('dialog', { name: /Contact/ });
    expect(requests.map(({ url }) => url)).toContain('/admin/data-reports/99');
    expect(within(sheet).getByRole('link', { name: 'Edit the field' })).toHaveAttribute(
      'href',
      '/spaces/7?report=99#CONTACT',
    );
    await userEvent.click(within(sheet).getByRole('button', { name: 'Close' }));

    await waitFor(() => {
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    });
    expect(router.state.location.search).toBe('');
  });
"""),
])
print('ok')
