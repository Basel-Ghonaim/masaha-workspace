"""Commit 6: the directory carries the page's announcements and offers two slots."""
import io

D = 'C:/dev/masaha/app/apps/web/src/features/directory/'


def edit(path, pairs):
    p = D + path
    s = io.open(p, encoding='utf8', newline='').read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, a[:60])
        s = s.replace(a, b)
    io.open(p, 'w', encoding='utf8', newline='').write(s)
    print('ok', path)


edit('types/SpacePageView.ts', [
    ("import type { PhotoUrls } from '@masaha/shared/spaces';\n",
     "import type { PhotoUrls } from '@masaha/shared/spaces';\nimport type { PublicAnnouncement } from '@masaha/shared/directory';\n"),
    ("  photos: PhotoUrls[];\n",
     "  photos: PhotoUrls[];\n"
     "  /** The space's running and upcoming announcements, as the API answers them; the page's slots draw them. */\n"
     "  announcements: PublicAnnouncement[];\n"),
])

edit('hooks/page/useSpacePage.ts', [
    ("    photos: space?.photos ?? [],\n",
     "    photos: space?.photos ?? [],\n    announcements: space?.announcements ?? [],\n"),
])

edit('components/page/SpaceDetails.tsx', [
    ("import { Badge, Button, cn, EmptyState } from '@shared/design-system';\n",
     "import type { PublicAnnouncement } from '@masaha/shared/directory';\nimport { Badge, Button, cn, EmptyState } from '@shared/design-system';\n"),
    (" * A space's public page (screen 3), in U8's order at every width: the head, an unverified space's\n"
     " * notice, the status (a card below 1024 px), the prices,",
     " * A space's public page (screen 3), in U8's order at every width: a running closure's notice at the\n"
     " * top, the head, an unverified space's notice, the status (a card below 1024 px), the space's\n"
     " * announcements, the prices,"),
    (" * The page sets the area's name, the link back to the directory and the platform's contact, the\n"
     " * heart beside the name, and the report of wrong information, drawn last in the main column (U8).\n",
     " * The page sets the area's name, the link back to the directory and the platform's contact, the\n"
     " * heart beside the name, the closure's notice and the announcements, and the report of wrong\n"
     " * information, drawn last in the main column (U8).\n"),
    ("  heart,\n  report,\n}: {",
     "  heart,\n  notice,\n  announcements,\n  report,\n}: {"),
    ("  heart?: (space: ActionSpace) => ReactNode;\n",
     "  heart?: (space: ActionSpace) => ReactNode;\n"
     "  /** A running closure's notice, above the page (U8: «the closure Alert stays at the top»). */\n"
     "  notice?: (items: PublicAnnouncement[]) => ReactNode;\n"
     "  /** The space's announcements, after the status and before the prices (U8). */\n"
     "  announcements?: (items: PublicAnnouncement[]) => ReactNode;\n"),
    ("      <div className=\"flex min-w-0 flex-col gap-10 lg:col-span-8\">\n",
     "      {notice !== undefined && (\n"
     "        // Empty when no closure runs: hidden, so it takes no gap.\n"
     "        <div className=\"empty:hidden lg:col-span-12\">{notice(view.announcements)}</div>\n"
     "      )}\n"
     "      <div className=\"flex min-w-0 flex-col gap-10 lg:col-span-8\">\n"),
    ("        {!view.wide && panelShown && <StatusPanel panel={panel} />}\n",
     "        {!view.wide && panelShown && <StatusPanel panel={panel} />}\n"
     "        {announcements?.(view.announcements)}\n"),
])
