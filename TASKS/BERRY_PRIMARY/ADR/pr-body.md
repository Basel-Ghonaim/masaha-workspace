## Summary

Adds [ADR 0022](docs/architecture/decisions/0022-the-berry-on-the-main-action.md), **The berry on the main action**, a dated *Revised* line on [ADR 0019](docs/architecture/decisions/0019-ink-and-spark-brand.md) pointing to it, and its line in the documentation map's list of decisions.

Each screen's main action takes the berry, at a step that passes AA in both themes (white text on the light theme's darker step, dark text on the dark theme's lighter step). The ink keeps secondary actions, links, controls, focus and structure; content and work surfaces stay neutral; a few brand surfaces carry the berry-to-plum scale; the dashboard stays quieter. ADR 0019's measured criteria remain the tests a berry must pass.

## Scope

- Documentation only: the ADR, one *Revised* line in ADR 0019, and one line in `docs/README.md`.
- Nothing is built by this PR. The design system and its documents change in the Work Item that builds it.

## Checks

- `npm run check:links`
- `npm run check:conflicts`
- `npm run format:check`
