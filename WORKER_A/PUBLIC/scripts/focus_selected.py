import io

ROOT = 'C:/dev/masaha/app/apps/web/src/shared/map/'


def sub(path, old, new, count=1):
    s = io.open(ROOT + path, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (path, old[:60], s.count(old))
    s = s.replace(old, new)
    io.open(ROOT + path, 'w', encoding='utf-8', newline='').write(s)


sub('types/MarkerMapProps.ts', """  /** Brings the visitor's point into view. */
  showUser: () => void;
};""", """  /** Brings the visitor's point into view. */
  showUser: () => void;
  /** Moves the focus to the selected mark, as when its card closes. */
  focusSelected: () => void;
};""")
sub('components/LeafletMarkerMap.tsx', """            showUser: () => {
              if (user) map.setView(user.point, Math.max(map.getZoom(), USER_ZOOM));
            },""", """            showUser: () => {
              if (user) map.setView(user.point, Math.max(map.getZoom(), USER_ZOOM));
            },
            focusSelected: () => {
              map
                .getContainer()
                .querySelector<HTMLElement>('[role="button"][aria-pressed="true"]')
                ?.focus();
            },""")
sub('components/MarkerMap.component.test.tsx', """    expect(screen.getByRole('application', { name: LABEL })).toBeInTheDocument();
    expect(screen.getByText('Legend')).toBeInTheDocument();
""", """    expect(screen.getByRole('application', { name: LABEL })).toBeInTheDocument();
    expect(screen.getByText('Legend')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Back to the selected mark' }));
    expect(sea).toHaveFocus();
""")
sub('components/MarkerMap.component.test.tsx', """      overlay={() => <p>Legend</p>}""", """      overlay={(map) => (
        <>
          <p>Legend</p>
          <button type="button" onClick={map.focusSelected}>
            Back to the selected mark
          </button>
        </>
      )}""")
print('ok')
