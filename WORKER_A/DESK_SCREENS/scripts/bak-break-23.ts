import { gazaClockOf } from '@masaha/shared/core';
import { checkOutVisitSchema, type CheckOutVisitRequest } from '@masaha/shared/desk';
import type { PresentPerson } from '@masaha/shared/occupancy';
import type { VisitQuote, VisitTerms } from '@masaha/shared/visits';
import { useIntentKey } from '@shared/api';
import { useCopy } from '@shared/copy';
import { AppError, toAppError } from '@shared/errors';
import { useServerForm } from '@shared/forms';
import { agorotOf, clockOf, priceText } from '@shared/lib';
import { isolate, useLanguage } from '@shared/localisation';
import { useQueryClient } from '@tanstack/react-query';
import { useEffect, useRef, useState, type BaseSyntheticEvent } from 'react';
import { useWatch } from 'react-hook-form';
import { toastCheckedOut } from '../../components/toast/deskToasts';
import { deskFailure } from '../../services/deskRefusal';
import { quoteIsStale } from '../../services/quoteAge';
import type { MoneyBlockView } from '../../types/MoneyBlockView';
import { useMoneyBlock } from '../money/useMoneyBlock';
import { deskKeys } from '../queryKeys';
import { useCheckOutVisit } from './useCheckOutVisit';
import { useQuoteQuery } from './useQuoteQuery';

type Values = {
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

const MINUTE_MS = 60_000;

/**
 * A visit's check-out (K2), ready to render, over the server's quote, read on opening and each
 * minute while open: the visitor, their stay and how it was billed; the money block filled with the
 * due; a visit with no rate asks a typed price and its reason of whoever may type one (DI-10), and
 * closes unpriced for whoever may not (DI-28); a remainder on a visit with no customer asks a name and
 * a phone, which stay once shown (DI-13). It sends the quote's time and the recorded amount, never a
 * figure above the due; a quote older than 4 minutes is read again first, and a changed due stops the
 * send with its line. One opening is one intent and one key (S4). Done, the toast speaks from the
 * answer (S8) and `onDone` closes it.
 */
export function useCheckOutDialog({
  spaceId,
  person,
  terms,
  onDone,
}: {
  spaceId: number;
  person: Extract<PresentPerson, { kind: 'VISIT' }>;
  terms: VisitTerms;
  onDone: () => void;
}) {
  const copy = useCopy();
  const words = copy.desk;
  const language = useLanguage() === 'en' ? 'en' : 'ar';
  const client = useQueryClient();
  const quoteQuery = useQuoteQuery(spaceId, person.id);
  const checkOut = useCheckOutVisit(spaceId, person.id);
  const { key } = useIntentKey();
  const [refusal, setRefusal] = useState<AppError | null>(null);
  const [quoteChanged, setQuoteChanged] = useState<string | null>(null);
  const [debtShown, setDebtShown] = useState(false);

  const visit = quoteQuery.data;
  const quote = visit?.quote ?? null;
  const noRate = quote !== null && quote.chargeAgorot === null;
  const typing = noRate && terms.mayTypePrice;
  const unpriced = noRate && !terms.mayTypePrice;
  const customer = visit?.customer ?? null;
  const price = (agorot: number) => isolate(priceText(agorot, language));

  const form = useServerForm<Values, CheckOutVisitRequest>({
    schema: checkOutVisitSchema,
    defaultValues: {
      customerName: person.name,
      phone: '',
      charge: { amountAgorot: '', reason: '' },
    },
    fields: ['charge.amountAgorot', 'charge.reason', 'customerName', 'phone'],
    prepare: (values) => {
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
          ? {
              charge: {
                amountAgorot: agorotOf(values.charge.amountAgorot),
                reason: reason === '' ? undefined : reason,
              },
            }
          : {}),
      };
    },
    submit: async (request) => {
      // The contract's rule, said before sending: a part left unpaid on a visit with no customer
      // needs the phone it is left to.
      if (live.current.needsDebt && request.phone === undefined) {
        throw new AppError({
          type: 'validation',
          status: 422,
          errors: { phone: ['required'] },
          message: 'A phone is required for the part left unpaid.',
        });
      }
      let body = request;
      const sent = live.current.quote;
      if (sent !== null && quoteIsStale(sent.at, new Date())) {
        const fresh = (await quoteQuery.refetch()).data?.quote ?? null;
        if (fresh !== null && fresh.chargeAgorot !== sent.chargeAgorot) {
          setQuoteChanged(words.checkOut.quoteChanged({ amount: price(fresh.chargeAgorot ?? 0) }));
          return;
        }
        body = { ...request, checkedOutAt: fresh?.at };
      }
      try {
        const answer = await checkOut.mutateAsync({ body, key });
        toastCheckedOut(person.name, answer);
        onDone();
      } catch (error) {
        const failure = toAppError(error);
        if (failure.errors?.checkedOutAt !== undefined) {
          // The quote's time is too old or in the future: read it again, and say what is due now.
          const fresh = (await quoteQuery.refetch()).data?.quote ?? null;
          setQuoteChanged(words.checkOut.quoteChanged({ amount: price(fresh?.chargeAgorot ?? 0) }));
          return;
        }
        if (failure.code === 'PAYMENT_EXCEEDS_DUE') void quoteQuery.refetch();
        if (failure.code === 'PRICE_TYPING_NOT_ALLOWED') {
          void client.invalidateQueries({ queryKey: deskKeys.terms(spaceId) });
        }
        setRefusal(failure);
        throw error;
      }
    },
    failureTitle: words.checkOut.failed,
    fieldLines: {
      'charge.amountAgorot': {
        invalid_format: words.money.amountInvalid,
        out_of_range: words.money.amountZero,
      },
      phone: { required: words.debt.phoneRequired },
    },
    failureLines: words.refusals,
  });

  const [typedAmount, debtName] = useWatch({
    control: form.form.control,
    name: ['charge.amountAgorot', 'customerName'],
  });
  const typedAgorot = agorotOf(typedAmount);
  const due = typing
    ? typeof typedAgorot === 'number'
      ? typedAgorot
      : 0
    : (quote?.chargeAgorot ?? 0);
  const money = useMoneyBlock({
    due,
    open: false,
    none: true,
    owesTo: customer?.name ?? (debtName.trim() === '' ? null : debtName),
  });
  const needsDebt = customer === null && (unpriced || money.left > 0);
  // Once asked in this opening, the name and the phone stay, empty or not (DI-13).
  if (needsDebt && !debtShown) setDebtShown(true);

  const live = useRef<Live>({ quote, money, typing, unpriced, needsDebt });
  useEffect(() => {
    live.current = { quote, money, typing, unpriced, needsDebt };
  });

  // A new attempt starts with no failure and no changed due, also when the browser's check stops it.
  const send = (event?: BaseSyntheticEvent) => {
    setRefusal(null);
    setQuoteChanged(null);
    form.submit(event);
  };

  const timeOf = (instant: string) => clockOf(gazaClockOf(new Date(instant)).minute);
  const stay =
    visit === undefined || quote === null
      ? null
      : Math.max(
          0,
          Math.floor(
            (new Date(quote.at).getTime() - new Date(visit.checkedInAt).getTime()) / MINUTE_MS,
          ),
        );
  const present = copy.occupancy.present;
  const rounding = terms.rounding;
  const calc =
    quote === null || quote.chargeAgorot === null
      ? []
      : [
          words.checkOut.billed({
            time: isolate(clockOf(quote.billedMinutes)),
          }),
          rounding.rule === 'UP_AFTER_MINUTES'
            ? words.checkOut.rounding.UP_AFTER_MINUTES({
                minutes: words.checkOut.minutes({ count: rounding.minutes ?? 0 }),
              })
            : rounding.rule === 'NEAREST_HALF_HOUR'
              ? copy.spaceSettings.pricing.half
              : copy.spaceSettings.pricing.minute,
          ...(quote.capApplied === true ? [words.checkOut.cap] : []),
        ];
  const hasVisitCustomerRefusal = refusal?.code === 'VISIT_HAS_CUSTOMER';
  const failure = deskFailure(hasVisitCustomerRefusal ? null : refusal, form.failure, {
    title: words.checkOut.failed,
    lost: words.failure.lost,
    nothing: words.failure.nothing,
    retryLabel: copy.status.retry,
    retry: () => {
      send();
    },
  });

  return {
    title: words.checkOut.title({ name: isolate(person.name) }),
    kind: visit?.audience === 'STUDENT' ? words.checkOut.studentVisit : words.checkOut.visit,
    state: quoteQuery.isPending
      ? ('loading' as const)
      : quote === null
        ? ('failed' as const)
        : ('ready' as const),
    quoteFailed: words.checkOut.quoteFailed,
    rows:
      visit === undefined || quote === null || stay === null
        ? []
        : [
            { label: words.checkOut.rows.in, value: timeOf(visit.checkedInAt) },
            { label: words.checkOut.rows.out, value: timeOf(quote.at) },
            {
              label: words.checkOut.rows.duration,
              value:
                stay < 60
                  ? present.minutes({ minutes: stay })
                  : present.duration({ hours: Math.floor(stay / 60), minutes: stay % 60 }),
            },
          ],
    calc,
    money: unpriced ? null : money,
    groupLabel: words.money.group,
    typed: typing
      ? {
          amount: {
            label: words.checkOut.typed.amount,
            ...form.field('charge.amountAgorot'),
            error: form.errors['charge.amountAgorot'],
          },
          reason: {
            label: words.checkOut.typed.reason,
            ...form.field('charge.reason'),
            error: form.errors['charge.reason'],
          },
          badge: words.checkOut.typed.badge,
          help: words.checkOut.typed.help,
        }
      : null,
    unpriced: unpriced ? words.checkOut.unpriced : null,
    debt:
      customer !== null
        ? unpriced || money.left > 0
          ? { kind: 'customer' as const, line: words.debt.adds({ name: isolate(customer.name) }) }
          : null
        : debtShown
          ? {
              kind: 'fields' as const,
              name: { label: words.debt.name, ...form.field('customerName') },
              nameError: form.errors.customerName,
              phone: { label: words.debt.phone, ...form.field('phone') },
              phoneError: hasVisitCustomerRefusal
                ? words.refusals.VISIT_HAS_CUSTOMER
                : form.errors.phone,
              required: needsDebt,
            }
          : null,
    quoteChanged,
    submit: {
      label:
        unpriced || money.recorded === 0
          ? words.checkOut.submitNone
          : words.checkOut.submit({ amount: price(money.recorded) }),
      run: send,
      busy: form.isPending,
      blocked: form.blocked || quote === null,
    },
    failure,
  };
}

/** A visit's check-out, ready to render. */
export type CheckOutDialogView = ReturnType<typeof useCheckOutDialog>;
