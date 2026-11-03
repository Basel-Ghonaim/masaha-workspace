import io

ROOT = 'C:/dev/masaha/app/apps/web/src/features/directory/'


def sub(path, old, new, count=1):
    s = io.open(ROOT + path, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (path, old[:60], s.count(old))
    s = s.replace(old, new)
    io.open(ROOT + path, 'w', encoding='utf-8', newline='').write(s)


# Test 59: a point placed by hand.
sub('hooks/near/useNearMe.component.test.tsx', """  it('stopping keeps the point; clearing drops it and every answer ordered by distance', () => {""",
    """  it('a point placed by hand is kept rounded, from a pin, and sorts by distance; «رجوع» restores the location before', () => {
    const device = fakeGeolocation();
    const { result } = renderNearMe();
    act(() => {
      result.current.near.press();
    });
    act(() => {
      device.succeed(31.5, 34.46, 30);
    });
    act(() => {
      result.current.near.stop();
    });
    const before = result.current.near.state;

    act(() => {
      result.current.near.startPick();
    });
    expect(result.current.near.state.status).toBe('picking');
    act(() => {
      result.current.near.cancelPick();
    });
    expect(result.current.near.state).toEqual(before);

    act(() => {
      result.current.near.startPick();
    });
    act(() => {
      result.current.near.placePin({ lat: 31.523_456, lng: 34.441_789 });
    });
    expect(result.current.near.state).toEqual({
      status: 'granted',
      point: { lat: 31.523, lng: 34.442 },
      source: 'pin',
      sorting: true,
    });
    expect(result.current.search).toBe('');

    act(() => {
      result.current.near.startPick();
    });
    act(() => {
      result.current.near.cancelPick();
    });
    expect(result.current.near.state).toMatchObject({
      status: 'granted',
      point: { lat: 31.523, lng: 34.442 },
      source: 'pin',
    });
  });

  it('stopping keeps the point; clearing drops it and every answer ordered by distance', () => {""")

# Test 60: the map fallback and «تغيير الموقع».
sub('components/near/LocationStatus.component.test.tsx', """  it('the refused states offer «اختر منطقتك», which focuses the place filter from 1024 px', async () => {""",
    """  it('the refused states offer setting the location on the map; a pin’s line offers «تغيير الموقع»', async () => {
    const device = fakeGeolocation();
    const user = userEvent.setup();
    const { router } = renderDirectoryRouter(390);
    await screen.findByRole('link', { name: 'مساحة 1' });
    await user.click(screen.getByRole('button', { name: 'الأقرب إليّ' }));
    act(() => {
      device.fail();
    });
    expect(
      screen.getByText('اختر منطقتك أو حدّد موقعك على الخريطة لنرتّب المساحات حسب المسافة.'),
    ).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: 'حدّد موقعي على الخريطة' }));

    expect(router.state.location.search).toBe('?view=map');
    act(() => {
      nearMeStore.placePin({ lat: 31.52, lng: 34.44 });
    });
    expect(
      screen.getByText(
        `مرتبة حسب المسافة من الموقع الذي حدّدته على الخريطة. المسافات تقريبية بخط مستقيم. ${PRIVACY}`,
      ),
    ).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'تغيير الموقع' }));
    expect(screen.queryByRole('button', { name: 'تغيير الموقع' })).not.toBeInTheDocument();
  });

  it('the refused states offer «اختر منطقتك», which focuses the place filter from 1024 px', async () => {""")
sub('components/near/LocationStatus.component.test.tsx', """/** The directory's list at `width`, the place filter a button the page's slot would draw. */
function renderDirectory(width: number) {""", """/** The directory's list at `width`, the place filter a button the page's slot would draw. */
function renderDirectory(width: number) {
  return renderDirectoryRouter(width).requests;
}

/** The same, with its router, to read the address. */
function renderDirectoryRouter(width: number) {""")
sub('components/near/LocationStatus.component.test.tsx', """  render(
    <Wrapper>
      <RouterProvider router={router} />
    </Wrapper>,
  );
  return requests;
}""", """  render(
    <Wrapper>
      <RouterProvider router={router} />
    </Wrapper>,
  );
  return { requests, router };
}""")
print('ok')
