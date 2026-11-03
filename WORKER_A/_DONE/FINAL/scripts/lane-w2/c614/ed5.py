base = 'C:/dev/masaha/app-lane-w2/apps/web/src/features/lookups/hooks/'
def edit(rel, pairs):
    p = base + rel
    s = open(p, encoding='utf8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (rel, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)

edit('edit/useEditAmenityForm.component.test.tsx', [
 ("it('starts from the amenity as it stands: its icon chosen, its Active switch alone'", "it('starts from the amenity as it stands: its icon chosen, and no switch'"),
 ("    expect(result.current.active).toMatchObject({ label: 'Active', checked: true });\n", "    expect(result.current).not.toHaveProperty('active');\n"),
 ("it('saves its names, icon and Active flag, and closes", "it('saves its names and icon, never its Active flag, and closes"),
 ("        return ok({ ...INTERNET, icon: 'coffee', isActive: false });", "        return ok({ ...INTERNET, icon: 'coffee' });"),
 ("      result.current.form.icon.choose('coffee');\n      result.current.form.active?.toggle(false);\n", "      result.current.form.icon.choose('coffee');\n"),
 ("      icon: 'coffee',\n      isActive: false,\n    });", "      icon: 'coffee',\n    });"),
])
edit('edit/useEditAreaForm.component.test.tsx', [
 ("""  it('saves the area as it stands with its switch turned on, restoring it', async () => {
    const onSaved = vi.fn();
    const requests = fakeTransport((request) =>
      request.method === 'get' ? ok([]) : ok({ ...SHUJAIYYA, isActive: true }),
    );
    const { result } = renderHook(() => useEditAreaForm({ area: SHUJAIYYA, onSaved }), {
      wrapper: queryWrapper(),
    });
    expect(result.current.active?.checked).toBe(false);

    act(() => {
      result.current.active?.toggle(true);
    });
    act(() => {""", """  it('saves the area’s names as they stand, and never its Active flag', async () => {
    const onSaved = vi.fn();
    const requests = fakeTransport((request) =>
      request.method === 'get' ? ok([]) : ok(SHUJAIYYA),
    );
    const { result } = renderHook(() => useEditAreaForm({ area: SHUJAIYYA, onSaved }), {
      wrapper: queryWrapper(),
    });
    expect(result.current).not.toHaveProperty('active');

    act(() => {"""),
 ("""    expect(bodyOf(requests[0])).toEqual({
      nameAr: 'الشجاعية',
      nameEn: 'Ash-Shuja’iyya',
      isActive: true,
    });""", """    expect(bodyOf(requests.find(({ method }) => method === 'patch'))).toEqual({
      nameAr: 'الشجاعية',
      nameEn: 'Ash-Shuja’iyya',
    });"""),
 ("    fakeTransport(() => refused(409, { type: 'conflict', errors: { nameAr: ['not_unique'] } }));",
  "    fakeTransport((request) =>\n      request.method === 'get'\n        ? ok([])\n        : refused(409, { type: 'conflict', errors: { nameAr: ['not_unique'] } }),\n    );"),
])
edit('edit/useEditGovernorateForm.component.test.tsx', [
 ("""  it('starts from the governorate as it stands, its Active switch with its hint', () => {
    fakeTransport(() => ok([]));
    const { result } = renderHook(
      () => useEditGovernorateForm({ governorate: RAFAH, onSaved: vi.fn() }),
      { wrapper: queryWrapper() },
    );

    expect(result.current.active).toMatchObject({
      label: 'Active',
      hint: 'Hidden: not shown in filters and forms.',
      checked: false,
      disabled: false,
    });
  });""", """  it('starts from the governorate as it stands, with no switch', () => {
    fakeTransport(() => ok([]));
    const { result } = renderHook(
      () => useEditGovernorateForm({ governorate: RAFAH, onSaved: vi.fn() }),
      { wrapper: queryWrapper() },
    );

    expect(result.current).not.toHaveProperty('active');
    expect(result.current).not.toHaveProperty('position');
  });"""),
 ("it('saves its names with the switch as isActive, and closes the sheet'", "it('saves its names, never its Active flag, and closes the sheet'"),
 ("        : ok({ ...RAFAH, nameEn: 'Rafah Governorate', isActive: true }),", "        : ok({ ...RAFAH, nameEn: 'Rafah Governorate' }),"),
 ("""    act(() => {
      result.current.active?.toggle(true);
    });
    expect(result.current.active?.checked).toBe(true);
""", ""),
 ("""    expect(bodyOf(requests[0])).toEqual({
      nameAr: 'محافظة رفح',
      nameEn: 'Rafah Governorate',
      isActive: true,
    });""", """    expect(bodyOf(requests.find(({ method }) => method === 'patch'))).toEqual({
      nameAr: 'محافظة رفح',
      nameEn: 'Rafah Governorate',
    });"""),
])
edit('add/useAddAmenityForm.component.test.tsx', [
 ("expect(result.current.form.active).toBeUndefined();", "expect(result.current.form).not.toHaveProperty('active');"),
])
edit('add/useAddAreaForm.component.test.tsx', [
 ("expect(form().active).toBeUndefined();", "expect(form()).not.toHaveProperty('active');"),
])
print('ok')
