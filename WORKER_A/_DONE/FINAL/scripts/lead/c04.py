import os
import shutil

APP = 'C:/dev/masaha/app/'
ROOT = APP + 'apps/web/src/'
STAGE = 'C:/dev/masaha/workspace/WORKER_A/FINAL/scripts/lead/c04/'


def edit(p, old, new):
    path = ROOT + p
    s = open(path, encoding='utf8').read()
    assert s.count(old) == 1, (p, old[:60])
    s = s.replace(old, new)
    open(path, 'w', encoding='utf8', newline='').write(s)


os.makedirs(ROOT + 'shared/routing/focus', exist_ok=True)
for name in ('firstPage.ts', 'useMainFocus.ts', 'useMainFocus.component.test.tsx'):
    shutil.copyfile(STAGE + name, ROOT + 'shared/routing/focus/' + name)
# The skip link moves as it is (git mv keeps its history).
os.system(f'cd {APP} && git mv apps/web/src/pages/site/shell/SkipLink.tsx apps/web/src/shared/routing/focus/SkipLink.tsx')
os.system(f'cd {APP} && git rm -q apps/web/src/pages/site/shell/useMainFocus.ts')

edit('shared/routing/focus/SkipLink.tsx', """/**
 * The shell's first focusable element: a link past the header to the page's `main`, hidden until the
 * keyboard reaches it (SH-018).
 */""", """/**
 * Every shell's first focusable element: a link past the header (or the sidebar) to the page's
 * `main`, hidden until the keyboard reaches it (SH-018, finding 130).
 */""")
edit('shared/routing/index.ts', """export { showActionBar, useActionBarShown } from './actionBar/actionBarShown';""", """export { showActionBar, useActionBarShown } from './actionBar/actionBarShown';
export { SkipLink } from './focus/SkipLink';
export { useMainFocus } from './focus/useMainFocus';""")

# --- the site's shell
edit('pages/site/shell/SiteLayout.tsx', """import { ResumeFavorite } from '@features/favorites';
import { useState } from 'react';""", """import { ResumeFavorite } from '@features/favorites';
import { SkipLink, useMainFocus } from '@shared/routing';
import { useState } from 'react';""")
edit('pages/site/shell/SiteLayout.tsx', """import { SkipLink } from './SkipLink';
""", '')
edit('pages/site/shell/SiteLayout.tsx', """import { useMainFocus } from './useMainFocus';
""", '')

# --- the focus shell
edit('pages/site/shell/FocusLayout.tsx', """import { useCopy } from '@shared/copy';""", """import { useCopy } from '@shared/copy';
import { SkipLink, useMainFocus } from '@shared/routing';""")
edit('pages/site/shell/FocusLayout.tsx', """ * a tablet up. No footer.
 */
export function FocusLayout({ actions }: { actions?: ReactNode }) {
  const copy = useCopy();

  return (
    <div className="flex min-h-dvh flex-col">
      <header""", """ * a tablet up. No footer. The skip link comes first, and its `main` takes the focus as every shell's
 * does (`useMainFocus`).
 */
export function FocusLayout({ actions }: { actions?: ReactNode }) {
  const copy = useCopy();
  useMainFocus();

  return (
    <div className="flex min-h-dvh flex-col">
      <SkipLink />
      <header""")
edit('pages/site/shell/FocusLayout.tsx', """      <main className="flex flex-1 flex-col px-4 py-6 md:items-center md:justify-center md:px-8 md:py-16">""", """      <main
        id="main"
        tabIndex={-1}
        className="flex flex-1 flex-col px-4 py-6 outline-none md:items-center md:justify-center md:px-8 md:py-16"
      >""")

# --- the dashboard's shell
edit('pages/dashboard/shell/DashboardLayout.tsx', """import { cn } from '@shared/design-system';""", """import { cn } from '@shared/design-system';
import { SkipLink, useMainFocus } from '@shared/routing';""")
edit('pages/dashboard/shell/DashboardLayout.tsx', """ * is drawn only while a page fills it, and the content then makes room for it.
 */""", """ * is drawn only while a page fills it, and the content then makes room for it. The skip link comes
 * before the sidebar, and the page's `main` takes the focus on a page change (`useMainFocus`).
 */""")
edit('pages/dashboard/shell/DashboardLayout.tsx', """  const action = useMemo(() => ({ target: bar, fill }), [bar, fill]);

  return (
    <SidebarProvider className="bg-background text-foreground">
      <Sidebar label={label}>""", """  const action = useMemo(() => ({ target: bar, fill }), [bar, fill]);
  useMainFocus();

  return (
    <SidebarProvider className="bg-background text-foreground">
      <SkipLink />
      <Sidebar label={label}>""")
edit('pages/dashboard/shell/DashboardLayout.tsx', """        <main
          className={cn(
            'flex flex-1 flex-col gap-6 px-4 py-6 md:px-8',""", """        <main
          id="main"
          tabIndex={-1}
          className={cn(
            'flex flex-1 flex-col gap-6 px-4 py-6 outline-none md:px-8',""")

# --- tests: the dashboard's and the focus shell's skip link
edit('pages/dashboard/shell/DashboardLayout.component.test.tsx', """import { render, screen } from '@testing-library/react';""", """import { act, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';""")
edit('pages/dashboard/shell/DashboardLayout.component.test.tsx', """    { initialEntries: [path] },
  );
  render(
    <>
      <RouterProvider router={router} />
      <BarProbe />
    </>,
  );
}""", """    { initialEntries: [path] },
  );
  render(
    <>
      <RouterProvider router={router} />
      <BarProbe />
    </>,
  );
  return router;
}

describe("the dashboard's skip link and focus", () => {
  it('offers «Skip to content» first, before the sidebar, leading to main', async () => {
    stubScreenWidth(1280);
    const user = userEvent.setup();
    renderShell('/plain');
    await screen.findByText('A page');

    await user.tab();

    const skip = screen.getByRole('link', { name: 'Skip to content' });
    expect(skip).toHaveFocus();
    expect(skip).toHaveAttribute('href', '#main');
    expect(screen.getByRole('main')).toHaveAttribute('id', 'main');
  });

  it('moves the focus to main when another page opens, not on the first', async () => {
    stubScreenWidth(1280);
    const router = renderShell('/plain');
    await screen.findByText('A page');
    expect(screen.getByRole('main')).not.toHaveFocus();

    await act(async () => {
      await router.navigate('/desk');
    });

    await waitFor(() => {
      expect(screen.getByRole('main')).toHaveFocus();
    });
  });
});""")
edit('pages/site/shell/SiteLayout.component.test.tsx', """  it('moves the focus to the main content when another page opens, not on the first load nor when only the search changes', async () => {""", """  it('offers «Skip to content» first in the focus shell too, leading to its main', async () => {
    const user = userEvent.setup();
    await renderSite('/login');

    await user.tab();

    const skip = screen.getByRole('link', { name: 'Skip to content' });
    expect(skip).toHaveFocus();
    expect(skip).toHaveAttribute('href', '#main');
    expect(screen.getByRole('main')).toHaveAttribute('id', 'main');
  });

  it('moves the focus to the main content when another page opens, not on the first load nor when only the search changes', async () => {""")
print('done')
