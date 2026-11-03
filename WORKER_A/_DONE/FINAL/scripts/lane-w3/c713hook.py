import os
os.chdir(r'C:\dev\masaha\app-lane-w3\apps\web\src\features\desk')
def edit(p, pairs):
    s=open(p,encoding='utf8').read()
    for a,b in pairs:
        assert s.count(a)==1,(p,a)
        s=s.replace(a,b)
    open(p,'w',encoding='utf8',newline='').write(s)
edit('hooks/sheet/useSubscriptionSheet.ts',[
("import { endOf } from '../../services/endOf';","import { endNote } from '../../services/endNote';\nimport { endOf } from '../../services/endOf';"),
("""    published: requests,
    customDefaults:""","""    published: requests,
    prices: choices.prices.list,
    customDefaults:"""),
("""  const [choice, startsOn, typedName, typedPrice, billing, endsOn] = useWatch({
    control,
    name: ['choice', 'startsOn', 'name', 'custom.priceAgorot', 'custom.billing', 'custom.endsOn'],
  });""","""  const [
    choice,
    startsOn,
    typedName,
    typedPrice,
    billing,
    endsOn,
    customName,
    totalDays,
    totalHours,
  ] = useWatch({
    control,
    name: [
      'choice',
      'startsOn',
      'name',
      'custom.priceAgorot',
      'custom.billing',
      'custom.endsOn',
      'custom.name',
      'custom.totalDays',
      'custom.totalHours',
    ],
  });"""),
("""  const needsPhone = known === null && created === null && money.left > 0;""","""  const needsPhone = known === null && created === null && money.left > 0;
  // Over earlier debts, the block lists each, then the new one, and its due is their total (G16.3).
  const priorShown = known !== null && priorTotal > 0;
  const chosenName =
    chosenPackage?.name ?? chosenPrice?.line.title ?? (isCustom ? customName.trim() : '');
  const calc = priorShown
    ? [
        ...prior.map((item) =>
          words.calcItem({ item: isolate(item.label), balance: price(item.leftAgorot) }),
        ),
        ...(chosenName === ''
          ? []
          : [
              (renewing ? words.calcRenewal : words.calcNew)({
                name: isolate(chosenName),
                price: price(newPrice),
              }),
            ]),
      ]
    : [];"""),
("""    dates: {
      from: { label: words.from, field: form.field('startsOn'), error: form.errors.startsOn },""","""    dates: {
      from: {
        label: words.from,
        value: startsOn,
        text: startsOn === '' ? '' : dayText(startsOn, language),
        choose: (date: string) => {
          setValue('startsOn', date, { shouldDirty: true });
        },
        error: form.errors.startsOn,
      },"""),
("""                field: form.field('custom.endsOn'),
                error: form.errors['custom.endsOn'],
                help: endsOn === '' ? words.noEnd : undefined,""","""                value: endsOn,
                text: endsOn === '' ? words.clearEnd : dayText(endsOn, language),
                choose: (date: string) => {
                  setValue('custom.endsOn', date, { shouldDirty: true });
                },
                clear: {
                  label: words.clearEnd,
                  run: () => {
                    setValue('custom.endsOn', '', { shouldDirty: true });
                  },
                },
                error: form.errors['custom.endsOn'],
                // What ends it, by the limits set (DK-008).
                help:
                  endNote(
                    { endsOn, totalDays, totalHours },
                    {
                      noEnd: words.noEnd,
                      noEndLimit: words.noEndLimit,
                      endOrLimit: words.endOrLimit,
                      days: words.limitDays,
                      hours: words.limitHours,
                    },
                    (date) => dayText(date, language),
                  ) ?? undefined,"""),
("""    money,
    moneyLabel: copy.desk.money.group,""","""    money: priorShown ? { ...money, due: { ...money.due, label: words.total } } : money,
    calc,
    moneyLabel: copy.desk.money.group,"""),
])
