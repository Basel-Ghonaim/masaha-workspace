ROOT = 'C:/dev/masaha/app/apps/web/src/shared/routing/focus/'


def edit(p, old, new):
    path = ROOT + p
    s = open(path, encoding='utf8').read()
    assert s.count(old) == 1, (p, old[:60])
    s = s.replace(old, new)
    open(path, 'w', encoding='utf8', newline='').write(s)


edit('useMainFocus.ts', """/** The element a location's hash names, if the page holds one. */
function namedBy(hash: string): HTMLElement | null {
  if (hash.length < 2) return null;
  try {
    return document.getElementById(decodeURIComponent(hash.slice(1)));
  } catch {
    return null;
  }
}""", """/** What takes the focus by itself: a control, a link, or an element given a `tabindex`. */
const FOCUSABLE = 'a[href], button, input, select, textarea, [tabindex]';

/**
 * Where the focus goes for a location's hash, if the page holds the element it names: the element
 * itself when it takes the focus, else its first focusable heading (a card named by the hash, whose
 * heading carries `tabIndex={-1}`); none when neither does.
 */
function namedBy(hash: string): HTMLElement | null {
  if (hash.length < 2) return null;
  let named: HTMLElement | null;
  try {
    named = document.getElementById(decodeURIComponent(hash.slice(1)));
  } catch {
    return null;
  }
  if (named === null || named.matches(FOCUSABLE)) return named;
  return named.querySelector<HTMLElement>(
    ':is(h1, h2, h3, h4, h5, h6)[tabindex], [role="heading"][tabindex]',
  );
}""")

edit('useMainFocus.component.test.tsx', """                <h2 id="contact" tabIndex={-1}>
                  Contact us
                </h2>
              </>""", """                <h2 id="contact" tabIndex={-1}>
                  Contact us
                </h2>
                {/* A card named by the hash, which takes no focus itself: its heading does. */}
                <section id="hours">
                  <h2 tabIndex={-1}>Opening hours</h2>
                </section>
              </>""")
edit('useMainFocus.component.test.tsx', """  it('moves nothing when only the search changes', async () => {""", """  it('focuses the heading of a card the hash names when the card takes no focus itself', async () => {
    const router = renderShells('/about');
    await act(async () => {
      await router.navigate('/about#owners');
    });

    await act(async () => {
      await router.navigate('/about#hours');
    });

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: 'Opening hours' })).toHaveFocus();
    });
  });

  it('moves nothing when only the search changes', async () => {""")
print('ok')
