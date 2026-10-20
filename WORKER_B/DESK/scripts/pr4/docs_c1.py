import io, os
os.chdir('C:/dev/masaha/app-b')
def edit(path, pairs):
    t = io.open(path, encoding='utf-8', newline='').read()
    for old, new in pairs:
        assert t.count(old) == 1, (path, old[:70], t.count(old))
        t = t.replace(old, new)
    io.open(path, 'w', encoding='utf-8', newline='').write(t)
edit('docs/architecture/data-model.md', [
("It gains a customer when it is left unpaid. Never deleted.",
 "It gains a customer when it is left unpaid. It may be written off by the owner, with who, when and why, and the write-off undone (2026-10-20, #PRNUM). Never deleted."),
("keeps rounding minutes (1–59) exactly for the \"up after N minutes\" rule, and has no negative rate or charge;",
 "keeps rounding minutes (1–59) exactly for the \"up after N minutes\" rule, has no negative rate or charge, and has a write-off's time, who and non-blank reason together, only once closed and priced (`visits_write_off_check`, 2026-10-20, #PRNUM);"),
("and a visit is paid only once its charge is set (its own constraint, `payments_visit_uncharged`).",
 "and a visit is paid only once its charge is set (its own constraint, `payments_visit_uncharged`), and a written-off visit takes no payment (`payments_visit_written_off`, 2026-10-20, #PRNUM)."),
])
edit('docs/backend/conventions.md', [
("- **The database owns the three payment rules its triggers enforce:** append-only, voided once, and never above the amount due ([data-model.md](../architecture/data-model.md#constraints-worth-stating)).",
 "- **The database owns the four payment rules its triggers enforce:** append-only, voided once, never above the amount due, and a written-off visit takes no payment ([data-model.md](../architecture/data-model.md#constraints-worth-stating))."),
])
edit('docs/api/api-contract.md', [
("""  charge: VisitCharge | null            // null while open, and once closed unpriced
}""", """  charge: VisitCharge | null,           // null while open, and once closed unpriced
  writeOff: { at, byId, reason } | null // set while written off
}"""),
])
edit('docs/features/payments.md', [
("the payments of an item never add up to more than its due; a visit is paid only once its charge is set. The service repeats none of them.",
 "the payments of an item never add up to more than its due; a visit is paid only once its charge is set; a written-off visit takes no payment. The service repeats none of them."),
("- **The constraint is read from the database's message.**",
 "- **A written-off visit's refusal is the trigger's fourth rule (`payments_visit_written_off`), not a check in the desk.** *Why:* the ledger's rules have one owner, so every insert path is covered; the trigger already locks the visit's row, so a write-off and a payment racing are decided there (S1 of the plan). 2026-10-20, #PRNUM.\n- **The constraint is read from the database's message.**"),
])
edit('docs/features/visits.md', [
("- **Owns** the `visits` table; the visit's rates and charge rules (`visitCharge.ts`, pure); the visit's audit entries.",
 "- **Owns** the `visits` table, the write-off's columns included; the visit's rates and charge rules (`visitCharge.ts`, pure); the visit's audit entries."),
])
print('ok')
