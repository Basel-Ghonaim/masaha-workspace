p='docs/architecture/findings/153-the-seed-stores-the-contacts-whatsapp-in-a-form-the-phone-rule-does-not.md'
s=open(p,encoding='utf-8',newline='').read()
pairs=[("**Status:** Open · **Date:** 2026-10-28","**Status:** Resolved · **Date:** 2026-10-28"),
("rewrites it as `+97059…` and audits a change no one made.","rewrites it as `+97059…` and audits a change of form the admin did not ask for."),
("The same holds for an email given with capitals: stored as given, lowercased by the first save.","The same holds for an email given with capitals: stored as given, lowercased by the first save. A number the phone rule refuses outright, such as `SEED_CONTACT_WHATSAPP=+201001234567`, is stored, read and answered, but a `PUT` of the card that changes only the email is refused, 422 on `whatsapp`, until the admin retypes the number."),
]
for o,n in pairs:
    assert s.count(o)==1,o
    s=s.replace(o,n)
s=s.rstrip('\n')+"\n\n**Resolution (2026-10-29, #PRNUM):** the seed reads `SEED_CONTACT_EMAIL` and `SEED_CONTACT_WHATSAPP` through `emailSchema` and `phoneSchema` (`apps/api/src/db/seed/seedEnv.ts`), so a seeded contact is stored in its one form, and a number the phone rule refuses fails the seed's environment check, naming its variable.\n"
open(p,'w',encoding='utf-8',newline='').write(s)
