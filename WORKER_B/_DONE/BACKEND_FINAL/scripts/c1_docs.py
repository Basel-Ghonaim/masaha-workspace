def edit(p, pairs):
    s = open(p, encoding='utf-8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old, s.count(old))
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)

edit('docs/api/api-contract.md', [
 ("A save that changes nothing writes nothing and answers the card as it is. A refusal writes nothing.",
  "A save that changes no value writes no value and no entry, and answers the card as it is (an unset contact's first save may still insert its rows, `null`, which read as unset). A refusal writes nothing."),
 ("both sent (`required`), `null` clearing one. Each is `null` while unset.",
  "both sent (`required`), `null` clearing one. Each is `null` while unset. A value stored in another form (a seed's) is answered as stored, and the next save stores its one form, audited."),
])
edit('docs/features/platform-settings.md', [
 ("- Writes and audits only what a save changes; a save that changes nothing writes nothing.",
  "- Writes and audits only what a save changes; a save that changes no value writes no value and no entry."),
 ("each save's body is checked by its shared schema, in the browser too.",
  "each save's body is checked by its shared schema."),
 ("- **A save writes and audits only what changed; the same values write nothing.**",
  "- **A save writes and audits only what changed; the same values write no value and no entry.**"),
 ("**Last Updated:** 2026-10-28", "**Last Updated:** 2026-10-29"),
])
