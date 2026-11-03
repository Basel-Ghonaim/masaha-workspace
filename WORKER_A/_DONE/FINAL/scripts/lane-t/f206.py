p = 'C:/dev/masaha/app-lane-t/docs/architecture/findings/206-the-showcases-chart-fixtures-match-the-builds-library-text.md'
open(p, 'w', encoding='utf8', newline='').write("""# 206. The showcase's chart fixtures match the build's library text

**Status:** Open · **Date:** 2026-10-29

**Evidence:** `check:build` refuses any fixture string of the development-only showcase (`apps/web/src/pages/showcase/fixtures.json`) that the copy catalogues do not also write, wherever it occurs in `apps/web/dist`. The bar chart's and the heatmap's fixtures (#PRNUM) hold single words that a library in the build writes too: the month ticks `يوليو`, `أغسطس`, `سبتمبر`, `Jul`, `Aug`, `Oct` (date-fns' locales, in the `calendar` chunk) and the unit `ILS` (the price formatter's chunk, `Intl`'s currency code). A production build of the integrated branch fails `check:build` with "7 showcase string(s) in the build", though no showcase code is in it: the check's own advice is to reword such a fixture. Found by lane T while proving its `check:build` rules; its own rules pass on the same build.

**Resolves when:** the fixtures hold no single word a library writes (for example, the ticks and the unit as phrases only the showcase writes, or values the copy catalogues already write), and `check:build` passes on a production build.
""")
