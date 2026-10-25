p='C:/dev/masaha/app/apps/web/src/features/occupancy/components/PresentList.component.test.tsx'
s=open(p,encoding='utf-8',newline='').read()
old='''    act(() => {
      screen.getByRole('button', { name: 'Check out Omar' }).focus();
    });
    await act(async () => {
      await screen.findByRole('button', { name: 'Check out Omar' });
    });
    screen.getByRole('button', { name: 'Check out Omar' }).focus();'''
assert s.count(old)==1
s=s.replace(old,'''    const omar = await screen.findByRole('button', { name: 'Check out Omar' });
    act(() => {
      omar.focus();
    });''')
open(p,'w',encoding='utf-8',newline='').write(s)
