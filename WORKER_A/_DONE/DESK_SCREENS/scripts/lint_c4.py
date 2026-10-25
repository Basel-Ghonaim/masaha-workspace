"""Commit 4's lint fixes: no ref in the check-out's hook; fields spread; small test and type fixes."""
from pathlib import Path

WEB = Path('C:/dev/masaha/app/apps/web/src')


def edit(rel: str, pairs: list[tuple[str, str]]) -> None:
    path = WEB / rel
    text = path.read_text(encoding='utf-8')
    for old, new in pairs:
        if text.count(old) != 1:
            raise SystemExit(f'{rel}: not once: {old[:80]!r}')
        text = text.replace(old, new)
    path.write_bytes(text.encode('utf-8'))


edit('features/desk/hooks/check-in/useVisitDialog.ts', [
    ("      name: { label: words.name, ...form.field('visitorName'), error: form.errors.visitorName },",
     "      name: { label: words.name, field: form.field('visitorName'), error: form.errors.visitorName },"),
])
edit('features/desk/components/visit/VisitDialog.tsx', [
    ("""            <Input
              dir="auto"
              autoComplete="off"
              autoFocus
              name={name.name}
              ref={name.ref}
              onChange={name.onChange}
              onBlur={name.onBlur}
              disabled={name.disabled}
            />""", """            <Input dir="auto" autoComplete="off" autoFocus {...name.field} />"""),
])
edit('features/desk/hooks/check-in/useVisitDialog.component.test.tsx', [
    ("      <button type=\"button\" onClick={() => dialog.setOpen(true)}>",
     "      <button\n        type=\"button\"\n        onClick={() => {\n          dialog.setOpen(true);\n        }}\n      >"),
])
edit('features/occupancy/components/PresentList.tsx', [
    ("const holder = (event.target as HTMLElement).closest<HTMLElement>('[data-present-action]');",
     "const holder = event.target.closest<HTMLElement>('[data-present-action]');"),
])
for rel in ['features/desk/hooks/check-out/useCheckOutDialog.component.test.tsx',
            'features/desk/components/check-out/CheckOutDialog.component.test.tsx']:
    edit(rel, [("const OMAR: PresentPerson = {", "const OMAR: Extract<PresentPerson, { kind: 'VISIT' }> = {")])

hook = 'features/desk/hooks/check-out/useCheckOutDialog.ts'
edit(hook, [
    ("""type Values = {
  customerName: string;
  phone: string;
  charge: { amountAgorot: string; reason: string };
};

/** What the request is built from, as of the last render: the form's resolver is made once. */
type Live = {
  quote: VisitQuote | null;
  money: MoneyBlockView;
  typing: boolean;
  unpriced: boolean;
  needsDebt: boolean;
};
""", """// The form holds what its check reads: the fields, and whether a price is typed and a remainder
// is left to a phone, which the dialog keeps in step (its resolver is made once).
type Values = {
  customerName: string;
  phone: string;
  charge: { amountAgorot: string; reason: string };
  typing: boolean;
  needsDebt: boolean;
};
"""),
    ("""      charge: { amountAgorot: '', reason: '' },
    },""", """      charge: { amountAgorot: '', reason: '' },
      typing: false,
      needsDebt: false,
    },"""),
    ("""    prepare: (values) => {
      const { quote: now, money, needsDebt } = live.current;
      const amount = typeof money.amount === 'string' ? money.amount : money.recorded;
      const reason = values.charge.reason.trim();
      return {
        checkedOutAt: now?.at,
        payment:
          live.current.unpriced || amount === 0
            ? null
            : { amountAgorot: amount, method: money.method?.value ?? 'CASH' },
        ...(needsDebt && values.phone.trim() !== '' ? { phone: values.phone } : {}),
        ...(needsDebt && values.customerName.trim() !== ''
          ? { customerName: values.customerName }
          : {}),
        ...(live.current.typing
          ? {""", """    // The fields the form checks; the quote's time and the payment are added as it is sent.
    prepare: (values) => {
      const reason = values.charge.reason.trim();
      return {
        ...(values.needsDebt && values.phone.trim() !== '' ? { phone: values.phone } : {}),
        ...(values.needsDebt && values.customerName.trim() !== ''
          ? { customerName: values.customerName }
          : {}),
        ...(values.typing
          ? {"""),
    ("""    submit: async (request) => {
      // The contract's rule, said before sending: a part left unpaid on a visit with no customer
      // needs the phone it is left to.
      if (live.current.needsDebt && request.phone === undefined) {""", """    submit: async (fields) => {
      // The contract's rule, said before sending: a part left unpaid on a visit with no customer
      // needs the phone it is left to.
      if (needsDebt && fields.phone === undefined) {"""),
    ("""      let body = request;
      const sent = live.current.quote;
      if (sent !== null && quoteIsStale(sent.at, new Date())) {
        const fresh = (await quoteQuery.refetch()).data?.quote ?? null;
        if (fresh !== null && fresh.chargeAgorot !== sent.chargeAgorot) {
          setQuoteChanged(words.checkOut.quoteChanged({ amount: price(fresh.chargeAgorot ?? 0) }));
          return;
        }
        body = { ...request, checkedOutAt: fresh?.at };
      }""", """      // «المستلم الآن» says itself what it cannot read.
      if (typeof money.amount === 'string') return;
      let body: CheckOutVisitRequest = {
        ...fields,
        checkedOutAt: quote?.at,
        payment:
          unpriced || money.recorded === 0
            ? null
            : { amountAgorot: money.recorded, method: money.method?.value ?? 'CASH' },
      };
      if (quote !== null && quoteIsStale(quote.at, new Date())) {
        const fresh = (await quoteQuery.refetch()).data?.quote ?? null;
        if (fresh !== null && fresh.chargeAgorot !== quote.chargeAgorot) {
          setQuoteChanged(words.checkOut.quoteChanged({ amount: price(fresh.chargeAgorot ?? 0) }));
          return;
        }
        body = { ...body, checkedOutAt: fresh?.at };
      }"""),
    ("""  const live = useRef<Live>({ quote, money, typing, unpriced, needsDebt });
  useEffect(() => {
    live.current = { quote, money, typing, unpriced, needsDebt };
  });
""", """  // The form's check follows what the dialog shows.
  const { setValue } = form.form;
  useEffect(() => {
    setValue('typing', typing);
    setValue('needsDebt', needsDebt);
  }, [setValue, typing, needsDebt]);
"""),
    ("""          amount: {
            label: words.checkOut.typed.amount,
            ...form.field('charge.amountAgorot'),
            error: form.errors['charge.amountAgorot'],
          },
          reason: {
            label: words.checkOut.typed.reason,
            ...form.field('charge.reason'),
            error: form.errors['charge.reason'],
          },""", """          amount: {
            label: words.checkOut.typed.amount,
            field: form.field('charge.amountAgorot'),
            error: form.errors['charge.amountAgorot'],
          },
          reason: {
            label: words.checkOut.typed.reason,
            field: form.field('charge.reason'),
            error: form.errors['charge.reason'],
          },"""),
    ("""              name: { label: words.debt.name, ...form.field('customerName') },""",
     """              name: { label: words.debt.name, field: form.field('customerName') },"""),
    ("""              phone: { label: words.debt.phone, ...form.field('phone') },""",
     """              phone: { label: words.debt.phone, field: form.field('phone') },"""),
    ("import { useEffect, useRef, useState, type BaseSyntheticEvent } from 'react';",
     "import { useEffect, useState, type BaseSyntheticEvent } from 'react';"),
    ("import type { VisitQuote, VisitTerms } from '@masaha/shared/visits';",
     "import type { VisitTerms } from '@masaha/shared/visits';"),
    ("import type { MoneyBlockView } from '../../types/MoneyBlockView';\n", ""),
])

dialog = 'features/desk/components/check-out/CheckOutDialog.tsx'
edit(dialog, [
    ("""                  <Input
                    dir="ltr"
                    inputMode="decimal"
                    autoComplete="off"
                    autoFocus
                    name={typed.amount.name}
                    ref={typed.amount.ref}
                    onChange={typed.amount.onChange}
                    onBlur={typed.amount.onBlur}
                    disabled={typed.amount.disabled}
                  />""", """                  <Input
                    dir="ltr"
                    inputMode="decimal"
                    autoComplete="off"
                    autoFocus
                    {...typed.amount.field}
                  />"""),
    ("""                  <Textarea
                    name={typed.reason.name}
                    ref={typed.reason.ref}
                    onChange={typed.reason.onChange}
                    onBlur={typed.reason.onBlur}
                    disabled={typed.reason.disabled}
                  />""", """                  <Textarea {...typed.reason.field} />"""),
    ("""        <Input
          dir="auto"
          autoComplete="off"
          name={debt.name.name}
          ref={debt.name.ref}
          onChange={debt.name.onChange}
          onBlur={debt.name.onBlur}
          disabled={debt.name.disabled}
        />""", """        <Input dir="auto" autoComplete="off" {...debt.name.field} />"""),
    ("""          aria-required={debt.required}
          name={debt.phone.name}
          ref={debt.phone.ref}
          onChange={debt.phone.onChange}
          onBlur={debt.phone.onBlur}
          disabled={debt.phone.disabled}
        />""", """          aria-required={debt.required}
          {...debt.phone.field}
        />"""),
])
print('ok')
