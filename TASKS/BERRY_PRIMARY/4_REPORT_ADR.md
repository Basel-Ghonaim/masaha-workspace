# ADR 0022 Report

- **PR:** #156
- **PR URL:** https://github.com/Basel-Ghonaim/masaha/pull/156
- **Head commit full SHA:** b7ade2587ec8c01b5500673fb7182c2c338b382b
- **Merge state:** CLEAN

## Checks

- `CodeRabbit`: skipping
- `build`: pass
- `check:classes`: pass
- `check:conflicts`: pass
- `check:links`: pass
- `format:check`: pass
- `lint`: pass
- `test:api`: pass
- `test:component`: pass
- `test:unit`: pass
- `typecheck`: pass

## Step 7 commit statistics

```text
commit b7ade2587ec8c01b5500673fb7182c2c338b382b
Author: Basel-Ghonaim <baselghonaim@gmail.com>
Date:   Tue Nov 24 17:13:54 2026 +0200

    docs(adr): the berry on the main action

    ADR 0019 kept the berry off every action. Built across the site, the
    identity became almost invisible, and the public pages read as grey.

    ADR 0022 gives the main action of each screen the berry, at steps that
    pass AA in both themes, keeps the ink for links, controls and structure,
    keeps content neutral, and lets a few brand surfaces carry the
    berry-to-plum scale. ADR 0019 gains a revised line pointing to it.
    Nothing is built yet: the design system changes in its Work Item.

 docs/README.md                                     |  1 +
 .../decisions/0019-ink-and-spark-brand.md          |  1 +
 .../decisions/0022-the-berry-on-the-main-action.md | 29 ++++++++++++++++++++++
 3 files changed, 31 insertions(+)
```

## Date change

No. The source ADR and revised line already used `2026-11-24`, which matched today's date.

## Deviations

None.
