def edit(p, pairs):
    s=open(p,encoding='utf8').read()
    for a,b in pairs:
        assert s.count(a)==1,(p,a)
        s=s.replace(a,b)
    open(p,'w',encoding='utf8',newline='').write(s)
p='features/desk/hooks/check-in/useVisitDialog.component.test.tsx'
s=open(p,encoding='utf8').read()
s=s.replace("const dialog = useVisitDialog({ spaceId: 7, shifts, full: false });","const dialog = useVisitDialog({ spaceId: 7, shifts, full: null });")
s=s.replace("findByRole('checkbox', { name: 'Student' })","findByRole('switch', { name: 'Student' })")
s=s.replace("queryByRole('checkbox', { name: 'Student' })","queryByRole('switch', { name: 'Student' })")
s=s.replace("queryByRole('combobox', { name: /Shift/ })","queryByRole('group', { name: /Shift/ })")
open(p,'w',encoding='utf8',newline='').write(s)
edit(p,[("""describe('useVisitDialog', () => {""","""describe('useVisitDialog', () => {
  it('offers the shifts as chips one may deselect, «Student» a switch, and sends no shift with none', async () => {
    const user = userEvent.setup();
    const requests = serve(() => ok(deskVisit(), 201));
    renderDialog([MORNING]);

    await user.click(screen.getByRole('button', { name: 'Open' }));
    expect(await screen.findByRole('switch', { name: 'Student' })).toBeInTheDocument();
    const morning = await screen.findByRole('radio', { name: 'Morning' });
    expect(morning).toBeChecked();
    expect(screen.queryByRole('radio', { name: 'No shift' })).toBeNull();
    await user.click(morning);
    expect(morning).not.toBeChecked();
    await user.type(screen.getByRole('textbox', { name: 'Name' }), 'Omar');
    await user.click(screen.getByRole('button', { name: 'Check in' }));

    await findToast(heard('Omar checked in'));
    expect(bodyOf(requests.find(({ method }) => method === 'post'))).toEqual({
      visitorName: 'Omar',
      audience: 'GENERAL',
      shiftId: null,
    });
  });
""")])
edit('features/desk/components/check-out/CheckOutDialog.component.test.tsx',[("""describe('CheckOutDialog', () => {""","""function renderQuoted(quote: ReturnType<typeof quotedVisit>) {
  fakeTransport(() => ok(quote));
  render(
    <QueryClientProvider client={createQueryClient()}>
      <CheckOutDialog spaceId={7} person={OMAR} terms={visitTerms()} onClose={() => undefined} />
    </QueryClientProvider>,
  );
}

describe('CheckOutDialog', () => {
  it('names the rate and the amount in its line, the cap with the day price, and a day price alone', async () => {
    const heard = (expected: string) => (content: string) =>
      content.replace(/[⁦-⁩]/g, '') === expected;
    renderQuoted(quotedVisit(1250));
    expect(
      await screen.findByText(heard('2.25 h × ₪5 = ₪12.50 · Rounded up after 15 minutes')),
    ).toBeInTheDocument();
    expect(screen.getByRole('dialog')).toHaveAccessibleDescription('Visit');
    cleanup();
    restoreTransport();

    const capped = quotedVisit(2500);
    renderQuoted({ ...capped, quote: { ...capped.quote!, capApplied: true } });
    expect(
      await screen.findByText(heard('2.25 h × ₪5 · Rounded up after 15 minutes')),
    ).toBeInTheDocument();
    expect(screen.getByText(heard('Cap: the day price ₪25'))).toBeInTheDocument();
    cleanup();
    restoreTransport();

    renderQuoted(quotedVisit(2500, undefined, { hourRateAgorot: null, audience: 'STUDENT' }));
    expect(
      await screen.findByText(heard('No hourly price — the day price ₪25')),
    ).toBeInTheDocument();
    expect(screen.getByRole('dialog')).toHaveAccessibleDescription('Visit · student');
  });
""")])
