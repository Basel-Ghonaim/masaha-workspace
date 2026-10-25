### Data reports

A signed-in user tells Masaha that one field group of a listed space's page is wrong; the space's owner, or the admin while the space is unverified, decides the report, and the reporter sees the reply ([data-model › Operations](../architecture/data-model.md#operations)). Resolving a report never edits the space. Built 2026-10-25, #PRNUM.

- **The fields** (`@masaha/shared/data-reports`): `field`, one of `PRICES`, `HOURS`, `CONTACT`, `LOCATION`, `AMENITIES`, `OTHER` (`invalid_choice`); `message`, optional, required for `OTHER` (`required`), and a decision's `note`, each 1–500 characters, NFC-normalised and trimmed, line breaks kept, with no bidirectional or other control characters (`invalid_format`).
- **One open report per user, space and field:** a repeat while one is open answers that one, 200, and writes nothing; once it is decided, a new one may be sent. The database holds the rule ([data-model › Constraints](../architecture/data-model.md#constraints-worth-stating)).
- **The limit:** 10 reports an hour per user, counted before the body is read, a repeat and an invalid body included ([security.md › Rate limits](../backend/security.md#rate-limits-fixed-window)); past it, 429 with `Retry-After`.

```ts
ReportDecision = {
  status: 'RESOLVED' | 'DISMISSED',
  at: string,
  note: string | null,             // the reply to the reporter; a dismissal's is required
  repliedBy: 'SPACE' | 'MASAHA'    // who decided, as stored with the decision: the owner, or the admin
}

SpaceReport = {                    // never who reported it
  id: number,
  field: 'PRICES' | 'HOURS' | 'CONTACT' | 'LOCATION' | 'AMENITIES' | 'OTHER',
  message: string | null,
  createdAt: string,
  status: 'OPEN' | 'RESOLVED' | 'DISMISSED',
  decision: ReportDecision | null  // null while open
}

MyReport = SpaceReport & {
  space: { id: number, slug: string, nameEn: string, nameAr: string | null, listed: boolean }
}
```

#### `POST /spaces/:slug/reports` · 👤
- **Body:** `{ field, message? }`.
- **201:** `MyReport`, `OPEN`, `listed: true`. **200:** the user's open report of that space and field, as it is, writing nothing; two identical reports at once make one (the user's lock, the database's rule behind it).
- **Errors**, each writing nothing: `unauthorized` (401) without a signed-in user; `rate_limit` (429) past the limit, before the body is read; `validation` (422) on the body; `not_found` (404) for a space that is not publicly listed — unknown, hidden, deleted, or in an area not listed — as its page answers.

