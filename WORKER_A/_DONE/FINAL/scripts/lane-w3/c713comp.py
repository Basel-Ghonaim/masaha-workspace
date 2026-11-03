import os
os.chdir(r'C:\dev\masaha\app-lane-w3\apps\web\src\features\desk')
def edit(p, pairs):
    s=open(p,encoding='utf8').read()
    for a,b in pairs:
        assert s.count(a)==1,(p,a)
        s=s.replace(a,b)
    open(p,'w',encoding='utf8',newline='').write(s)
edit('hooks/sheet/useSubscriptionSheet.ts',[
("""          ? [{ heading: words.groups.published, options: published.map(({ line }) => line) }]
          : []),
        ...(packages.length > 0 ? [{ heading: words.groups.packages, options: packages }] : []),
        ...(customChoice !== null ? [{ heading: null, options: [customChoice] }] : []),""","""          ? [
              {
                heading: words.groups.published,
                options: published.map(({ line }) => line),
                badge: null,
              },
            ]
          : []),
        // The desk's own packages, each marked private: visitors never see them (G16.5).
        ...(packages.length > 0
          ? [{ heading: words.groups.packages, options: packages, badge: words.private }]
          : []),
        ...(customChoice !== null
          ? [{ heading: null, options: [customChoice], badge: null }]
          : []),"""),
])
edit('components/sheet/PackageOptions.tsx',[
("""                          <span dir="auto" className="text-label">
                            {option.title}
                          </span>
                          {option.amount""","""                          <span className="flex flex-wrap items-center gap-2">
                            <span dir="auto" className="text-label">
                              {option.title}
                            </span>
                            {group.badge !== null && <Badge variant="neutral">{group.badge}</Badge>}
                          </span>
                          {option.amount"""),
])
s=open('components/sheet/PackageOptions.tsx',encoding='utf8').read()
import re
m=re.search(r"import \{([^}]*)\} from '@shared/design-system';",s)
names=[n.strip() for n in m.group(1).split(',') if n.strip()]
if 'Badge' not in names:
    names.append('Badge'); names.sort()
    s=s[:m.start()]+"import {\n  "+",\n  ".join(names)+",\n} from '@shared/design-system';"+s[m.end():]
open('components/sheet/PackageOptions.tsx','w',encoding='utf8',newline='').write(s)
edit('components/sheet/PriorDebts.tsx',[
("""import type { SubscriptionSheetView } from '../../hooks/sheet/useSubscriptionSheet';""","""import { Alert, AlertDescription, AlertTitle } from '@shared/design-system';
import type { SubscriptionSheetView } from '../../hooks/sheet/useSubscriptionSheet';"""),
("""    <section className="flex flex-col gap-1.5 rounded-lg border border-border p-3">
      <h3 className="text-label">{prior.title}</h3>
      {prior.items.length > 0 && (
        <ul className="flex flex-col gap-0.5 text-body-sm text-muted-foreground">
          {prior.items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      )}
      <p className="text-caption text-muted-foreground">{prior.note}</p>
    </section>""","""    // A warning (G16.3): what the desk receives goes to these first.
    <Alert variant="warning">
      <AlertTitle>{prior.title}</AlertTitle>
      <AlertDescription>
        {prior.items.length > 0 && (
          <ul className="flex flex-col gap-0.5">
            {prior.items.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        )}
        <p>{prior.note}</p>
      </AlertDescription>
    </Alert>"""),
])
edit('components/sheet/CustomTerms.tsx',[
("""      <Field label={view.price.label} error={view.price.error}>""","""      <Field label={view.price.label} helper={view.price.helper} error={view.price.error}>"""),
("""      <div className="flex flex-col gap-2">
        <p className="text-label">{view.limits.label}</p>""","""      {view.byAttendance !== null && (
        <p className="text-body-sm text-muted-foreground">{view.byAttendance}</p>
      )}
      <div className="flex flex-col gap-2">
        <p className="text-label">{view.limits.label}</p>"""),
])
edit('components/sheet/SubscriptionSheet.tsx',[
("""            <div className="grid grid-cols-2 gap-3">
              <Field label={dates.from.label} error={dates.from.error}>
                <Input type="date" dir="ltr" {...dates.from.field} />
              </Field>
              {dates.to?.kind === 'package' && (
                <Field label={dates.to.label} helper={dates.to.help}>
                  <Input dir="auto" readOnly value={dates.to.text} />
                </Field>
              )}
              {dates.to?.kind === 'custom' && (
                <Field label={dates.to.label} helper={dates.to.help} error={dates.to.error}>
                  <Input type="date" dir="ltr" {...dates.to.field} />
                </Field>
              )}
            </div>
            <MoneyBlock view={view.money} label={view.moneyLabel} calc={[]} disabled={busy}>""","""            <div className="grid grid-cols-2 gap-3">
              <Field label={dates.from.label} error={dates.from.error}>
                <DateField date={dates.from} disabled={busy} />
              </Field>
              {dates.to?.kind === 'package' && (
                // A package's end is said, never chosen: the server sets it (G16.1).
                <div className="flex flex-col gap-1.5">
                  <span className="text-label">{dates.to.label}</span>
                  <span className="text-body-sm">{dates.to.text}</span>
                  <span className="text-caption text-muted-foreground">{dates.to.help}</span>
                </div>
              )}
              {dates.to?.kind === 'custom' && (
                <Field label={dates.to.label} helper={dates.to.help} error={dates.to.error}>
                  <DateField date={dates.to} disabled={busy} />
                </Field>
              )}
            </div>
            <MoneyBlock view={view.money} label={view.moneyLabel} calc={view.calc} disabled={busy}>"""),
])
