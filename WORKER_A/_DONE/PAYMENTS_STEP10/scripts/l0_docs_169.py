import io

APP = 'C:/dev/masaha/app/'


def edit(path, pairs):
    p = APP + path
    s = io.open(p, encoding='utf8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old[:60])
        s = s.replace(old, new)
    io.open(p, 'w', encoding='utf8', newline='').write(s)


edit('docs/frontend/design-system/foundation.md', [
    (
        "  data.ts             the second entry: the data components that carry a heavy library (DataTable)\n",
        "  data.ts             the second entry: the data components that carry a heavy library (DataTable)\n"
        "  calendar.ts         the third entry: Calendar and DatePicker, over react-day-picker\n",
    ),
    (
        "The one exception is a second entry, `@shared/design-system/data`, for the data components that carry a heavy library (`DataTable`, over TanStack Table): only the pages that draw them import it, so the library stays out of the site's first download, which `check:build` verifies ([finding 45](../../architecture/findings/45-the-data-tables-library-reaches-the-sites-first-download.md)). Lint allows these entries alone.",
        "The exceptions are two more entries for the components that carry a heavy library: `@shared/design-system/data` for the data components (`DataTable`, over TanStack Table; [finding 45](../../architecture/findings/45-the-data-tables-library-reaches-the-sites-first-download.md)) and `@shared/design-system/calendar` for `Calendar` and `DatePicker` (over react-day-picker and date-fns; [finding 169](../../architecture/findings/169-the-calendar-rides-in-the-sites-first-download.md)). Only the pages that draw them import these entries, so their libraries stay out of the site's first download, which `check:build` verifies. Lint allows these entries alone.",
    ),
])

edit('docs/frontend/architecture.md', [
    (
        "TanStack Table (`data-table`), under the design system's data entry, and Leaflet (`leaflet`), under `shared/map` (§6).",
        "TanStack Table (`data-table`), under the design system's data entry, Leaflet (`leaflet`), under `shared/map` (§6), and react-day-picker with date-fns (`calendar`), under the design system's calendar entry ([finding 169](../architecture/findings/169-the-calendar-rides-in-the-sites-first-download.md)).",
    ),
])

edit('docs/architecture/findings/169-the-calendar-rides-in-the-sites-first-download.md', [
    ("**Status:** Open · **Date:** 2026-10-27", "**Status:** Resolved · **Date:** 2026-10-27"),
    (
        "or the owner accepts the calendar there. The owner scheduled it as an item of its own before PAYMENTS_STEP10's PR 4.\n",
        "or the owner accepts the calendar there. The owner scheduled it as an item of its own before PAYMENTS_STEP10's PR 4.\n"
        "\n"
        "**Resolution (2026-10-28, #PRNUM):** `Calendar` and `DatePicker` left the layer's main entry for an entry of their own, `@shared/design-system/calendar`, which only the ledger's filters and the showcase import; lint allows it as it allows the data entry. react-day-picker and date-fns are a `calendar` chunk (`libraryChunks.ts`) that `check:build` refuses in the site's first download; `@date-fns/tz` stays out of it, since Gaza's clock in `@masaha/shared` reads it on every page. The production build's manifest: the first download 1,140,210 → 1,064,781 bytes (1,055,704 before #127), the `design-system` chunk 361,726 → 281,292, and the calendar a 71,126-byte chunk the ledger loads. Drawn through the main entry again by a site page, the build fails `check:build` (\"_calendar-….js is calendar's chunk in the site's first download\").\n",
    ),
])
print('ok')
