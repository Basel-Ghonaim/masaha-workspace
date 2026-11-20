"""C7's code (plan §7.2): the logo in the site's header, the phone menu, the focus shell and the
admin's sidebar."""
from pathlib import Path

ROOT = Path(r"C:\dev\masaha\app-design-lane-b\apps\web\src")
FOCUS = (
    "rounded-sm focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
)


def edit(relative, old, new):
    path = ROOT / relative
    with open(path, encoding="utf-8", newline="") as handle:
        text = handle.read()
    if text.count(old) != 1:
        raise SystemExit(f"{relative}: expected one match, found {text.count(old)}")
    text = text.replace(old, new)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    print(f"edited {relative}")


# SiteHeader: the home link holds the logo, named, with the layer's one focus style (SD10).
edit(
    "pages/site/shell/SiteHeader.tsx",
    "import { Button, LogInIcon } from '@shared/design-system';",
    "import { Button, LogInIcon, Logo } from '@shared/design-system';",
)
edit(
    "pages/site/shell/SiteHeader.tsx",
    """        <Link to={SITE_PATHS.home} className="text-heading-3 text-primary">
          {copy.site.wordmark}
        </Link>""",
    f"""        <Link to={{SITE_PATHS.home}} className="{FOCUS}">
          <Logo label={{copy.site.wordmark}} className="h-10" />
        </Link>""",
)

# SiteMenu: the drawer's wordmark becomes the logo, at the column's start; the dialog keeps its name.
edit(
    "pages/site/shell/SiteMenu.tsx",
    """import {
  Button,
  LogInIcon,
  MenuIcon,""",
    """import {
  Button,
  LogInIcon,
  Logo,
  MenuIcon,""",
)
edit(
    "pages/site/shell/SiteMenu.tsx",
    """          <p className="text-heading-3 text-primary">{copy.site.wordmark}</p>""",
    """          <Logo label={copy.site.wordmark} className="h-10 self-start" />""",
)

# FocusLayout: as SiteHeader.
edit(
    "pages/site/shell/FocusLayout.tsx",
    "import { SkipLink, useMainFocus } from '@shared/routing';",
    "import { Logo } from '@shared/design-system';\nimport { SkipLink, useMainFocus } from '@shared/routing';",
)
edit(
    "pages/site/shell/FocusLayout.tsx",
    """          <Link to={SITE_PATHS.home} className="text-heading-3 text-primary">
            {copy.site.wordmark}
          </Link>""",
    f"""          <Link to={{SITE_PATHS.home}} className="{FOCUS}">
            <Logo label={{copy.site.wordmark}} className="h-10" />
          </Link>""",
)

# AdminLayout: the logo (the mark on the rail), decorative; the name for assistive technology once,
# beside the caption. The «م» tile goes.
edit(
    "pages/dashboard/shell/AdminLayout.tsx",
    "import { SidebarHeader } from '@shared/design-system';",
    "import { Logo, SidebarHeader } from '@shared/design-system';",
)
edit(
    "pages/dashboard/shell/AdminLayout.tsx",
    """  const reportsForAdmin = useAdminReportsCount();
  const tile = (
    <span
      aria-hidden
      className="flex size-9 shrink-0 items-center justify-center rounded-md bg-primary text-label text-primary-foreground"
    >
      {Array.from(copy.site.wordmark)[0]}
    </span>
  );
""",
    """  const reportsForAdmin = useAdminReportsCount();
""",
)
edit(
    "pages/dashboard/shell/AdminLayout.tsx",
    """        <SidebarHeader mark={tile} logo={tile}>
          <span className="truncate text-label">{copy.site.wordmark}</span>""",
    """        <SidebarHeader
          mark={<Logo form="mark" className="size-9" />}
          logo={<Logo className="h-9" />}
        >
          {/* The logo is decorative: the name is read here, once, before the area. */}
          <span className="sr-only">{copy.site.wordmark}</span>""",
)
