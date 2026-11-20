"""C7's breaks, made on the working copies (restored afterwards from the backups by copy).

round 1: T18 — the text wordmark back in SiteHeader; T19 — the «م» tile back in AdminLayout.
round 2: T18 — the header's logo without its label; T19 — the sidebar's logo given a label beside
         the sr-only name (the name read twice).
"""
import sys
from pathlib import Path

ROOT = Path(r"C:\dev\masaha\app-design-lane-b\apps\web\src")
HEADER = "pages/site/shell/SiteHeader.tsx"
ADMIN = "pages/dashboard/shell/AdminLayout.tsx"


def edit(relative, old, new):
    path = ROOT / relative
    with open(path, encoding="utf-8", newline="") as handle:
        text = handle.read()
    if text.count(old) != 1:
        raise SystemExit(f"{relative}: expected one match, found {text.count(old)}")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text.replace(old, new))
    print(f"broke {relative}")


LOGO = '<Logo label={copy.site.wordmark} className="h-10" />'

if sys.argv[1] == "1":
    edit(HEADER, LOGO, "{copy.site.wordmark}")
    edit(
        ADMIN,
        """        <SidebarHeader
          mark={<Logo form="mark" className="size-9" />}
          logo={<Logo className="h-9" />}
        >""",
        """        <SidebarHeader
          mark={
            <span aria-hidden className="flex size-9 shrink-0 items-center justify-center rounded-md bg-primary text-label text-primary-foreground">
              {Array.from(copy.site.wordmark)[0]}
            </span>
          }
          logo={
            <span aria-hidden className="flex size-9 shrink-0 items-center justify-center rounded-md bg-primary text-label text-primary-foreground">
              {Array.from(copy.site.wordmark)[0]}
            </span>
          }
        >""",
    )
elif sys.argv[1] == "2":
    edit(HEADER, LOGO, '<Logo className="h-10" />')
    edit(
        ADMIN,
        'logo={<Logo className="h-9" />}',
        'logo={<Logo label={copy.site.wordmark} className="h-9" />}',
    )
else:
    raise SystemExit("usage: c7_breaks.py 1|2")
