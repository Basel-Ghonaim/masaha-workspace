def edit(p, pairs):
    s=open(p,encoding='utf8').read()
    for a,b in pairs:
        assert s.count(a)==1,(p,a)
        s=s.replace(a,b)
    open(p,'w',encoding='utf8',newline='').write(s)
edit('features/desk/hooks/check-out/useCheckOutDialog.ts',[
("""  const rounding = terms.rounding;
  const calc =
    quote === null || quote.chargeAgorot === null
      ? []
      : [
          words.checkOut.billed({
            time: isolate(lengthOf(quote.billedMinutes)),
          }),
          rounding.rule === 'UP_AFTER_MINUTES'
            ? words.checkOut.rounding.UP_AFTER_MINUTES({
                minutes: words.checkOut.minutes({ count: rounding.minutes ?? 0 }),
              })
            : rounding.rule === 'NEAREST_HALF_HOUR'
              ? copy.spaceSettings.pricing.half
              : copy.spaceSettings.pricing.minute,
          ...(quote.capApplied === true ? [words.checkOut.cap] : []),
        ];""","""  const rounding = terms.rounding;
  const roundingLine =
    rounding.rule === 'UP_AFTER_MINUTES'
      ? words.checkOut.rounding.UP_AFTER_MINUTES({
          minutes: words.checkOut.minutes({ count: rounding.minutes ?? 0 }),
        })
      : rounding.rule === 'NEAREST_HALF_HOUR'
        ? copy.spaceSettings.pricing.half
        : copy.spaceSettings.pricing.minute;
  // The lines say how the quote's charge came about, from the visit's own rates; the amount is
  // always the quote's (G13.11, S7): the web never prices.
  const calcOf = (charge: number, minutes: number, capped: boolean | null): string[] => {
    const hourRate = visit?.hourRateAgorot ?? null;
    const dayRate = visit?.dayRateAgorot ?? null;
    if (hourRate === null) {
      return [words.checkOut.dayOnly({ day: price(dayRate ?? charge) })];
    }
    const hours = isolate(String(Math.round((minutes / 60) * 100) / 100));
    if (capped === true) {
      return [
        words.checkOut.billedCapped({ hours, rate: price(hourRate), rounding: roundingLine }),
        words.checkOut.cap({ day: price(dayRate ?? charge) }),
      ];
    }
    return [
      words.checkOut.billed({
        hours,
        rate: price(hourRate),
        amount: price(charge),
        rounding: roundingLine,
      }),
    ];
  };
  const calc =
    quote === null || quote.chargeAgorot === null
      ? []
      : calcOf(quote.chargeAgorot, quote.billedMinutes, quote.capApplied);"""),
])
edit('shared/copy/arabic/desk.ts',[
("""    billed: ({ time }: { time: string }) => `مدة محسوبة ${time}`,
    cap: 'السقف: سعر اليوم',""","""    billed: ({
      hours,
      rate,
      amount,
      rounding,
    }: {
      hours: string;
      rate: string;
      amount: string;
      rounding: string;
    }) => `${hours} س × ${rate} = ${amount} · ${rounding}`,
    billedCapped: ({ hours, rate, rounding }: { hours: string; rate: string; rounding: string }) =>
      `${hours} س × ${rate} · ${rounding}`,
    cap: ({ day }: { day: string }) => `السقف: سعر اليوم ${day}`,
    dayOnly: ({ day }: { day: string }) => `لا يوجد سعر بالساعة — سعر اليوم ${day}`,"""),
])
s=open('shared/copy/english/desk.ts',encoding='utf8').read()
import re
i=s.index("    billed: ({ time }: { time: string }) => `Billed time ${time}`,")
j=s.index("    cap: 'Capped at the day price',")+len("    cap: 'Capped at the day price',")
s=s[:i]+"""    /** How the quote's charge came about: the hours billed by the rate, rounded by the rule. */
    billed: ({
      hours,
      rate,
      amount,
      rounding,
    }: {
      hours: string;
      rate: string;
      amount: string;
      rounding: string;
    }) => `${hours} h × ${rate} = ${amount} · ${rounding}`,
    billedCapped: ({ hours, rate, rounding }: { hours: string; rate: string; rounding: string }) =>
      `${hours} h × ${rate} · ${rounding}`,
    cap: ({ day }: { day: string }) => `Cap: the day price ${day}`,
    dayOnly: ({ day }: { day: string }) => `No hourly price — the day price ${day}`,"""+s[j:]
open('shared/copy/english/desk.ts','w',encoding='utf8',newline='').write(s)
# dialog description and money block layout
edit('features/desk/components/check-out/CheckOutDialog.tsx',[
("""  DialogContent,
  DialogFooter,""","""  DialogContent,
  DialogDescription,
  DialogFooter,"""),
("""        aria-describedby={undefined}
      >
        <DialogHeader>
          <DialogTitle>{dialog.title}</DialogTitle>
          <Badge variant="neutral" className="self-start">
            {dialog.kind}
          </Badge>
        </DialogHeader>""","""      >
        <DialogHeader>
          <DialogTitle>{dialog.title}</DialogTitle>
          {/* The description names the kind: «زيارة» or «زيارة · طالب» (G13.18). */}
          <DialogDescription asChild>
            <div>
              <Badge variant="neutral">{dialog.kind}</Badge>
            </div>
          </DialogDescription>
        </DialogHeader>"""),
])
