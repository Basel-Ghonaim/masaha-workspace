## Summary

Adds [ADR 0021](docs/architecture/decisions/0021-sign-in-where-the-action-is.md), **Sign in where the action is**, and its line in the documentation map's list of decisions.

An action on the public site that needs an account (saving a favourite, reporting wrong information) will open the sign-in over the page it was pressed on, instead of sending the guest through the sign-in or register page and back. After signing in there, the user stays on the page and the action completes. The sign-in, register and forgotten-password pages keep their addresses for direct visits; the reset link opened from the email stays a page.

## Scope

- Documentation only: the ADR and one line in `docs/README.md`.
- Nothing is built by this PR. The frontend architecture (§2) and the `auth`, `favorites` and `data-reports` capability documents change with the code, in the Work Items that build it.

## Checks

- `npm run check:links`
- `npm run check:conflicts`
- `npm run format:check`
