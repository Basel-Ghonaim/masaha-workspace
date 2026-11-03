def edit(p, pairs):
    s=open(p,encoding='utf8').read()
    for a,b in pairs:
        assert s.count(a)==1,(p,a)
        s=s.replace(a,b)
    open(p,'w',encoding='utf8',newline='').write(s)
edit('features/desk/hooks/check-out/useCheckOutDialog.ts',[
("  const [typedAmount, debtName] = useWatch({","  const typedPhone = useWatch({ control: form.form.control, name: 'phone' });\n  const phoneOwner = usePhoneOwner(spaceId, typedPhone);\n  const [typedAmount, debtName] = useWatch({"),
("              phone: { label: words.debt.phone, field: form.field('phone') },","              phone: { label: words.debt.phone, field: form.field('phone') },\n              owner: phoneOwner,"),
])
s=open('features/desk/hooks/check-out/useCheckOutDialog.ts',encoding='utf8').read()
i=s.index("import { useDeskWrite }") if "import { useDeskWrite }" in s else None
open('features/desk/hooks/check-out/useCheckOutDialog.ts','w',encoding='utf8',newline='').write(s)
edit('features/desk/hooks/debt/useDebtDialog.ts',[
("import { useState, type BaseSyntheticEvent } from 'react';","import { useState, type BaseSyntheticEvent } from 'react';\nimport { useWatch } from 'react-hook-form';"),
("import { useDeskWrite } from '../useDeskWrite';","import { usePhoneOwner } from '../phone/usePhoneOwner';\nimport { useDeskWrite } from '../useDeskWrite';"),
("  const send = (event?: BaseSyntheticEvent) => {","  const owner = usePhoneOwner(spaceId, useWatch({ control: form.form.control, name: 'phone' }));\n\n  const send = (event?: BaseSyntheticEvent) => {"),
("    phone: { label: words.debt.phone, field: form.field('phone'), error: form.errors.phone },","    phone: {\n      label: words.debt.phone,\n      field: form.field('phone'),\n      error: form.errors.phone,\n      owner,\n    },"),
])
edit('features/desk/components/debt/DebtDialog.tsx',[
("""            <Input type="tel" dir="ltr" autoComplete="off" aria-required {...dialog.phone.field} />
          </Field>""","""            <Input type="tel" dir="ltr" autoComplete="off" aria-required {...dialog.phone.field} />
          </Field>
          <p aria-live="polite" className="text-body-sm text-muted-foreground empty:hidden">
            {dialog.phone.owner}
          </p>"""),
])
edit('features/desk/components/check-out/CheckOutDialog.tsx',[
("""          {...debt.phone.field}
        />
      </Field>""","""          {...debt.phone.field}
        />
      </Field>
      {/* Whose file the phone adds to, said as it is found (G13.12). */}
      <p aria-live="polite" className="text-body-sm text-muted-foreground empty:hidden">
        {debt.owner}
      </p>"""),
])
edit('shared/copy/arabic/desk.ts',[("""    adds: ({ name }: { name: string }) => `يُضاف إلى ملف ${name}`,""","""    adds: ({ name }: { name: string }) => `يُضاف إلى ملف ${name}`,
    newCustomer: 'زبون جديد بهذا الرقم',""")])
edit('shared/copy/english/desk.ts',[("""    adds: ({ name }: { name: string }) => `Added to ${name}’s file`,""","""    adds: ({ name }: { name: string }) => `Added to ${name}’s file`,
    /** A typed phone no customer holds yet: the write makes their file. */
    newCustomer: 'A new customer with this number',""")])
