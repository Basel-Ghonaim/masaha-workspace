import os
os.chdir(r'C:\dev\masaha\app-lane-w3\apps\web\src\features\desk')
def edit(p, pairs):
    s=open(p,encoding='utf8').read()
    for a,b in pairs:
        assert s.count(a)==1,(p,a)
        s=s.replace(a,b)
    open(p,'w',encoding='utf8',newline='').write(s)
edit('hooks/sheet/useSheetForm.ts',[
("""  published,
  customDefaults,
  submit,
}: {""","""  published,
  prices,
  customDefaults,
  submit,
}: {"""),
("""  /** A renewal of custom terms repeats them. */""","""  /** The space's published prices: a usage-based custom rate starts from the hour or day one. */
  prices: readonly Price[];
  /** A renewal of custom terms repeats them. */"""),
("""  const [audience, billing, shiftId] = useWatch({
    control,
    name: ['custom.audience', 'custom.billing', 'custom.shiftId'],
  });""","""  const [audience, billing, shiftId, typedRate] = useWatch({
    control,
    name: ['custom.audience', 'custom.billing', 'custom.shiftId', 'custom.priceAgorot'],
  });
  // The published hour or day price for whom and when (G16.4): the shift's, else the space's own.
  const publishedRate = (chosen: string): number | null => {
    const period = chosen === 'PER_HOUR' ? 'HOUR' : chosen === 'PER_DAY' ? 'DAY' : null;
    if (period === null) return null;
    const of = (shift: number | null) =>
      prices.find(
        (one) =>
          one.period === period &&
          one.audience === audience &&
          one.shiftId === shift &&
          one.labelAr === null,
      );
    return (of(shiftId === '' ? null : Number(shiftId)) ?? of(null))?.amountAgorot ?? null;
  };
  const rate = publishedRate(billing);
  const fromPublished = rate !== null && agorotOf(String(typedRate)) === rate;
  const price = (agorot: number) => isolate(priceText(agorot, language));"""),
("""      (value) => {
        if (isBilling(value)) setValue('custom.billing', value);
      },""","""      (value) => {
        if (!isBilling(value)) return;
        setValue('custom.billing', value);
        // A rate from attendance starts at the published one, while none of the desk's is typed.
        const published = publishedRate(value);
        const typed = agorotOf(String(typedRate));
        if (published !== null && (typed === undefined || typed === rate)) {
          setValue('custom.priceAgorot', shekelsOf(published));
        }
      },"""),
("""      label: billing === 'FIXED' ? words.custom.price : words.custom.rate,
      field: form.field('custom.priceAgorot'),
      error: form.errors['custom.priceAgorot'],
    },""","""      label: billing === 'FIXED' ? words.custom.price : words.custom.rate,
      field: form.field('custom.priceAgorot'),
      error: form.errors['custom.priceAgorot'],
      helper: billing !== 'FIXED' && fromPublished ? words.fromPublished : undefined,
    },
    // What attendance is charged at, said under the terms (G16.4).
    byAttendance:
      billing === 'FIXED'
        ? null
        : (() => {
            const typed = agorotOf(String(typedRate));
            return typeof typed === 'number' && typed > 0
              ? words.byAttendance[billing]({ rate: price(typed) })
              : null;
          })(),"""),
])
