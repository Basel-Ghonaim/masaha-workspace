p='C:/dev/masaha/app-b/docs/api/api-contract.md'
s=open(p,encoding='utf-8',newline='').read()
def rep(a,b):
    global s
    assert s.count(a)==1,a[:60]
    s=s.replace(a,b)
rep("**Last Updated:** 2026-10-22","**Last Updated:** 2026-10-24")
rep("and a subscription's (2026-10-22, #106, [Subscriptions (managed)](#subscriptions-managed)), whose payments take keys derived from its own (SHA-256 of the key and the payment's place, as a UUID), so its retry finds them;",
    "a subscription's (2026-10-22, #106, [Subscriptions (managed)](#subscriptions-managed)), whose payments take keys derived from its own (SHA-256 of the key and the payment's place, as a UUID), so its retry finds them, and an announcement's post (2026-10-24, #PRNUM, [Announcements (managed)](#announcements-managed));")
section = """### Announcements (managed)

What a space tells its users changes: a closure, an outage, an offer, an event or general news ([data-model › Content](../architecture/data-model.md#content)). Its staff post and change them (🧾); a closure running now closes the space's live status ([data-model › Live status](../architecture/data-model.md#live-status)). The endpoints sit under `/manage/spaces/:spaceId` and answer as *Managed spaces* says: without an active `OWNER` or `RECEPTION` link at the live space, `not_found` (404). Each write is refused with `forbidden` (403) before its body is read for whoever may not (`announcements.manage`), and again for an owner or reception whose link ended meanwhile. Built 2026-10-24, #PRNUM.

- **The fields** (`@masaha/shared/announcements`): `type`, one of `GENERAL`, `OUTAGE`, `CLOSURE`, `OFFER`, `EVENT` (`invalid_choice`); `textAr`, required, and `textEn`, optional, each 1–500 characters, NFC-normalised and trimmed, line breaks kept, with no bidirectional or other control characters (`invalid_format`); `startsAt` and `endsAt`, instants with their offset (`invalid_format` otherwise).
- **The period**, each refusal `validation` (422) `out_of_range` on its field, writing nothing: an end after the start; a start at most 30 days back (a closure posted late) and 365 days ahead; an end after now (ending one now is its own route) and at most 365 days after the start. An edit checks against now only what it changes, so an ended announcement's text can still be corrected.
- **The state** (`Announcement.state`), from the instants and the server's clock: `UPCOMING` before the start, `ENDED` from the end, else `RUNNING` (with no end, until it is ended).
- **Audit**, in the change's own transaction ([conventions §6](../backend/conventions.md#6-audit)), with the announcement as the entity and its space as the entry's: `announcement.created` (`after`: `{ type, startsAt, endsAt }`), `announcement.edited` (`before` and `after`: only the fields that changed); an edit that changes nothing writes nothing.

```ts
Announcement = {
  id: number,
  type: 'GENERAL' | 'OUTAGE' | 'CLOSURE' | 'OFFER' | 'EVENT',
  textAr: string,
  textEn: string | null,
  startsAt: string,
  endsAt: string | null,           // none: until it is ended
  state: 'RUNNING' | 'UPCOMING' | 'ENDED'
}
```

#### `POST /manage/spaces/:spaceId/announcements` · 🧾 · `Idempotency-Key`
- **Body:** `{ type, textAr, textEn?, startsAt?, endsAt? }`: no `startsAt`, now («يبدأ الآن»); no `endsAt` (or `null`), no end.
- **201:** `Announcement`; a retry with the same key answers the first announcement as it is now, 201, and writes nothing; two requests with one key at once make one (the space's lock, the key unique within the space behind it).
- **Errors**, each writing nothing: `validation` (422) on `idempotencyKey` (§1), then on the body, before anything is read; `forbidden` (403); `validation` (422) on the period; `not_found` (404), also for a space deleted meanwhile.

#### `PATCH /manage/spaces/:spaceId/announcements/:announcementId` · 🧾
- **Body:** `{ type?, textAr?, textEn?, startsAt?, endsAt? }`: what is absent is kept; `textEn: null` clears the English text and `endsAt: null` removes the end.
- **200:** `Announcement`.
- **Errors**, each writing nothing: `validation` (422) on the body, before anything is read; `forbidden` (403); `not_found` (404) for an announcement that is not the space's, or deleted; `validation` (422) on the period.

### Internal
"""
rep("### Internal\n", section)
open(p,'w',encoding='utf-8',newline='').write(s)
