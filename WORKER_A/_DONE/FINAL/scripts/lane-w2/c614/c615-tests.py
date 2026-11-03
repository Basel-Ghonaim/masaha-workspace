import os
os.chdir('C:/dev/masaha/app-lane-w2/apps/web/src/features/lookups')


def edit(p, pairs):
    s = open(p, encoding='utf8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)


edit('components/amenities/AmenityChecklist.component.test.tsx', [
("import { render, screen } from '@testing-library/react';",
 "import { render, screen } from '@testing-library/react';\nimport { useState } from 'react';"),
("""  it('has no accessibility violations', async () => {""",
"""  it('the owner’s checklist names a retired amenity, marked, and drops it when unticked', async () => {
    fakeTransport(() =>
      ok({
        governorates: [],
        amenities: [{ id: 1, key: 'internet', nameAr: 'إنترنت', nameEn: 'Internet', icon: 'wifi' }],
      }),
    );
    const onValueChange = vi.fn<(ids: number[]) => void>();
    // The owner's form, holding the value the checklist hands back.
    function OwnerForm() {
      const [value, setValue] = useState([1, 2]);
      return (
        <AmenityChecklist
          source="public"
          label="The list's amenities"
          value={value}
          linked={[1, 2]}
          retired={[{ id: 2, nameAr: 'مولّد', nameEn: 'Generator' }]}
          onValueChange={(ids) => {
            onValueChange(ids);
            setValue(ids);
          }}
          disabled={false}
        />
      );
    }
    const Wrapper = queryWrapper();
    const { container } = render(
      <Wrapper>
        <OwnerForm />
      </Wrapper>,
    );

    const generator = await screen.findByRole('checkbox', {
      name: 'Generator No longer on the platform’s list',
    });
    expect(generator).toBeChecked();
    expect(screen.getAllByRole('checkbox')).toEqual([
      screen.getByRole('checkbox', { name: 'Internet' }),
      generator,
    ]);
    // Named and marked in the list, it needs no count under it.
    expect(container).not.toHaveTextContent(/stays? linked to the space/);

    await userEvent.click(generator);

    expect(onValueChange).toHaveBeenLastCalledWith([1]);
    expect(generator).not.toBeChecked();
    expect(generator).toBeInTheDocument();
    expect(await axe(container)).toHaveNoViolations();
  });

  it('has no accessibility violations', async () => {"""),
])

edit('hooks/amenities/useAmenityChecklist.component.test.tsx', [
("""  answer: () => FakeAnswer = () => ok(AMENITIES),
  source: LookupsSource = 'admin',
) {
  const requests = fakeTransport(answer);
  const onValueChange = vi.fn<(ids: number[]) => void>();
  const rendered = renderHook(() => useAmenityChecklist({ source, value, linked, onValueChange }), {
    wrapper: queryWrapper(),
  });""", """  answer: () => FakeAnswer = () => ok(AMENITIES),
  source: LookupsSource = 'admin',
  retired: { id: number; nameAr: string; nameEn: string }[] = [],
) {
  const requests = fakeTransport(answer);
  const onValueChange = vi.fn<(ids: number[]) => void>();
  const rendered = renderHook(
    () => useAmenityChecklist({ source, value, linked, retired, onValueChange }),
    { wrapper: queryWrapper() },
  );"""),
("""  it('offers an owner the public catalogue’s amenities, keeping a retired linked one in the value and counting it', async () => {
    startPreferences('ar');
    const { result, onValueChange, requests } = renderChecklist(
      [2, 3],
      [2, 3],
      () => ok(CATALOGUE),
      'public',
    );""", """  it('offers an owner the public catalogue’s amenities, then a retired linked one, named and marked', async () => {
    startPreferences('ar');
    const { result, onValueChange, requests } = renderChecklist(
      [2, 3],
      [2, 3],
      () => ok(CATALOGUE),
      'public',
      [{ id: 2, nameAr: 'مولّد', nameEn: 'Generator' }],
    );"""),
("""    expect(
      result.current.items.map(({ id, checked, inactive }) => [id, checked, inactive]),
    ).toEqual([
      [1, false, false],
      [3, true, false],
    ]);
    expect(result.current.retiredKept).toBe(
      'يبقى مرفق واحد لم يعد في قائمة المنصة مرتبطًا بالمساحة.',
    );
    act(() => {
      result.current.items[0]?.toggle(true);
    });
    expect(onValueChange).toHaveBeenLastCalledWith([2, 3, 1]);
    act(() => {
      result.current.items[1]?.toggle(false);
    });
    expect(onValueChange).toHaveBeenLastCalledWith([2]);
  });""", """    expect(
      result.current.items.map(({ id, name, checked, mark }) => [id, name, checked, mark]),
    ).toEqual([
      [1, 'إنترنت', false, null],
      [3, 'طاقة شمسية', true, null],
      [2, 'مولّد', true, 'لم يعد في قائمة المنصة'],
    ]);
    expect(result.current).not.toHaveProperty('retiredKept');
    act(() => {
      result.current.items[0]?.toggle(true);
    });
    expect(onValueChange).toHaveBeenLastCalledWith([2, 3, 1]);
    act(() => {
      result.current.items[2]?.toggle(false);
    });
    expect(onValueChange).toHaveBeenLastCalledWith([3]);
  });"""),
("""  it('counts only the linked amenities the catalogue no longer names, and drops on a toggle one ticked and retired meanwhile', async () => {
    const { result, onValueChange } = renderChecklist([3, 4], [3], () => ok(CATALOGUE), 'public');

    await waitFor(() => {
      expect(result.current.status).toBe('ready');
    });
    expect(result.current.retiredKept).toBeNull();
""", """  it('names no retired amenity the space does not hold, and drops on a toggle one ticked and retired meanwhile', async () => {
    const { result, onValueChange } = renderChecklist([3, 4], [3], () => ok(CATALOGUE), 'public');

    await waitFor(() => {
      expect(result.current.status).toBe('ready');
    });
    expect(result.current.items.map(({ id }) => id)).toEqual([1, 3]);
"""),
])
print('ok')
