"""The R2/R3 fixes as cumulative stages, one per home commit. `save` copies every changed file's final
version; `stage <n>` writes the working tree as HEAD plus the changes of stages 1..n (the files of later
stages as at HEAD, or the intermediate texts below); `final` restores everything.
Usage: python stages.py save | stage <1-5> | final"""
import io, os, re, shutil, subprocess, sys

APP = 'C:/dev/masaha/app/'
W = 'apps/web/src/'
SAVE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stages-final')

# Each stage's files, taken whole in their final version (stage: [files]).
WHOLE = {
    1: [W + 'features/data-reports/hooks/space/useSpaceReports.ts',
        W + 'features/data-reports/hooks/decide/useDecideSheet.ts',
        W + 'features/data-reports/components/space/SpaceReportsList.component.test.tsx'],
    2: [W + 'features/data-reports/hooks/admin/useAdminReports.ts',
        W + 'features/data-reports/components/admin/AdminReportsList.tsx',
        W + 'features/data-reports/components/admin/FilterTags.tsx',
        W + 'features/data-reports/components/admin/AdminReportsList.component.test.tsx'],
    3: [W + 'features/data-reports/hooks/intent/reportIntent.ts',
        W + 'features/data-reports/hooks/intent/reportIntent.unit.test.ts',
        W + 'shared/routing/guest/guestLeaving.ts', W + 'shared/routing/index.ts',
        W + 'pages/site/shell/useGuestIntents.ts', W + 'pages/site/shell/SiteLayout.tsx',
        'docs/project/overview.md'],
    4: [W + 'features/favorites/hooks/intent/favoriteIntent.ts',
        W + 'features/favorites/hooks/intent/favoriteIntent.unit.test.ts',
        W + 'features/favorites/components/FavoriteButton.component.test.tsx',
        W + 'features/favorites/hooks/toggle/useFavoriteToggle.component.test.tsx',
        W + 'pages/site/public/space/SpacePage.component.test.tsx'],
    5: [W + 'features/favorites/hooks/toggle/useFavoriteToggle.ts',
        W + 'features/favorites/components/RemoveFavorite.tsx',
        W + 'features/favorites/components/RemoveFavorite.component.test.tsx',
        W + 'features/favorites/components/toast/favoriteToasts.tsx',
        W + 'features/favorites/hooks/favoriteWrite.ts',
        W + 'shared/copy/arabic/favorites.ts', W + 'shared/copy/english/favorites.ts',
        'docs/features/favorites.md', 'docs/features/directory.md',
        'docs/architecture/findings/187-a-favourite-just-removed-cannot-be-saved-again-for-an-undo.md'],
}
# Files whose final text is reached over two stages: (file, first stage, its intermediate text builder).
SPLIT = {}


def head(f):
    r = subprocess.run(['git', 'show', f'bbbeaeb9:{f}'], cwd=APP, capture_output=True)
    return r.stdout if r.returncode == 0 else None


def final(f):
    return io.open(os.path.join(SAVE, f.replace('/', '_')), 'rb').read()


def put(f, data):
    if data is None:
        if os.path.exists(APP + f):
            os.remove(APP + f)
        return
    os.makedirs(os.path.dirname(APP + f), exist_ok=True)
    io.open(APP + f, 'wb').write(data)


def text(b):
    return b.decode('utf8')


def sub1(s, a, b):
    assert s.count(a) == 1, a[:70]
    return s.replace(a, b)


def space_page_stage3():
    """The space page's test: HEAD, plus the transport's `/spaces` and the report's leaving test only."""
    s = text(final(W + 'pages/site/public/space/SpacePage.component.test.tsx'))
    s = re.sub(r"\n    it\('lets the held favourite go: a later sign-in in the tab saves nothing'.*?\n    \}\);\n", "\n", s, count=1, flags=re.S)
    # the heart's one name (stage 4) back to its two names
    s = sub1(s, """    const heart = screen.getByRole('button', {
      name: /^Save .Noor Hub. to favourites$/,
      hidden: true,
    });
    await waitFor(
      () => {
        expect(heart).toHaveAttribute('aria-pressed', 'true');
      },
      { timeout: 4000 },
    );""", """    const heart = await screen.findByRole(
      'button',
      { name: /^Remove .Noor Hub. from favourites$/, hidden: true },
      { timeout: 4000 },
    );
    expect(heart).toHaveAttribute('aria-pressed', 'true');""")
    return s.encode('utf8')


def data_reports_md_stage3():
    s = text(head('docs/features/data-reports.md'))
    return sub1(s, "the held report opens the dialog once they are back signed in, and is let go if they close the sign-in.",
                "the held report opens the dialog once they are back signed in, and is let go if they close the sign-in, after 15 minutes, or once the guest lands on another page of the site (the shell reports each page it shows: `noteSitePage`), so a later visit signed in opens nothing by itself (#129's review).").encode('utf8')


def toggle_stage4():
    s = text(head(W + 'features/favorites/hooks/toggle/useFavoriteToggle.ts'))
    return sub1(s, "    label: pressed ? words.remove({ name }) : words.save({ name }),",
                "    // One name, whatever its state: `aria-pressed` says whether it is saved (WAI-ARIA's toggle\n    // button; #129's review).\n    label: words.save({ name }),").encode('utf8')


def favorites_md_stage4():
    s = text(head('docs/features/favorites.md'))
    s = sub1(s, "named by what it does — «حفظ {name} في المفضّلة» or «إزالة {name} من المفضّلة» — and pressed (`aria-pressed`, the heart filled) while the space is saved;",
             "with one name, «حفظ {name} في المفضّلة», and pressed (`aria-pressed`, the heart filled) while the space is saved — a toggle keeps its name and its state says the rest (WAI-ARIA's button pattern; a departure from §9's two names, #129's review);")
    s = sub1(s, "Closing the sign-in lets the held favourite go.",
             "Closing the sign-in lets the held favourite go, and so do 15 minutes or the guest landing on another page of the site.")
    s = sub1(s, "a link carrying it would let a crafted link save a space for a signed-in user; closing the sign-in lets it go.",
             "a link carrying it would let a crafted link save a space for a signed-in user; closing the sign-in lets it go, and so do 15 minutes or the guest landing on another page of the site (the shell reports each page it shows: `noteSitePage`), so a later sign-in in the tab, maybe someone else's, saves nothing (#129's review).")
    return s.encode('utf8')


# (file, stage where its intermediate applies, builder, stage where its final applies)
INTER = [
    (W + 'pages/site/public/space/SpacePage.component.test.tsx', 3, space_page_stage3, 4),
    ('docs/features/data-reports.md', 3, data_reports_md_stage3, None),
    (W + 'features/favorites/hooks/toggle/useFavoriteToggle.ts', 4, toggle_stage4, 5),
    ('docs/features/favorites.md', 4, favorites_md_stage4, 5),
]
ALL = sorted({f for fs in WHOLE.values() for f in fs} | {f for f, *_ in INTER})

how = sys.argv[1]
if how == 'save':
    os.makedirs(SAVE, exist_ok=True)
    for f in ALL:
        shutil.copyfile(APP + f, os.path.join(SAVE, f.replace('/', '_')))
    print('saved', len(ALL))
elif how == 'final':
    for f in ALL:
        put(f, final(f))
    print('final')
else:
    n = int(sys.argv[2])
    for f in ALL:
        put(f, head(f))
    for stage in range(1, n + 1):
        for f in WHOLE.get(stage, []):
            put(f, final(f))
    for f, at, build, done in INTER:
        if done is not None and n >= done:
            put(f, final(f))
        elif n >= at:
            put(f, build())
    print('stage', n)
