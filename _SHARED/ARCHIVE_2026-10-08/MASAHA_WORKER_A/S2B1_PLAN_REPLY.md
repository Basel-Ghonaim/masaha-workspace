The plan is approved. Build it, with the answers below.

## Your proposed alternatives
1. **Descriptions with line breaks — build it now, not in S2b-4.** The admin's create form (S2b-3) is
   web-only and has the description textarea, so the API must accept a paragraph before then. Add
   `paragraphSchema` to `@masaha/shared/core`: the same rules as `textSchema` (NFC, trimmed, bidi and
   other control characters refused), except that line breaks are allowed (`\r\n` normalised to
   `\n`; no other separator). Use it for the two descriptions only; names, addresses and landmarks
   keep `textSchema`. Unit-test it beside `textSchema`, and add one line to conventions.md §3.
2. **"Last update" = the latest of the five group dates — accepted** as you stated it.

## The finding you flagged
Record **finding 36** as you proposed: a new space's empty fact groups (no hours, no prices yet)
count as fresh, because their dates start at creation. Evidence only; it is S2b-2's to weigh.

Everything else stands as planned: the endpoints and shapes, the modules and files, the migration,
the tests, the documents, the six commits and the verification. After the merge, the analyst applies
the migration to the other worker's database.
