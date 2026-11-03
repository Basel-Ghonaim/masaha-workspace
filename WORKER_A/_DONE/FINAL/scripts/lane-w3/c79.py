def edit(p, pairs):
    s=open(p,encoding='utf8').read()
    for a,b in pairs:
        assert s.count(a)==1,(p,a)
        s=s.replace(a,b)
    open(p,'w',encoding='utf8',newline='').write(s)
edit('features/desk/hooks/check-in/useVisitDialog.ts',[
("const NO_SHIFT = 'none';\n",""),
("""  /** The space is full now, as the desk's state now says. */
  full: boolean;""","""  /** How many are present and the capacity, when the count fills it (G13.9); `null` otherwise. */
  full: { present: number; capacity: number } | null;"""),
("  const shiftOf = (value: string) => (value === NO_SHIFT ? null : Number(value));","  // The chips may all be off: no shift (G13.10).\n  const shiftOf = (value: string) => (value === '' ? null : Number(value));"),
("    full: full ? words.full : null,","    full:\n      full === null\n        ? null\n        : words.full({ ratio: isolate(`${String(full.present)}/${String(full.capacity)}`) }),"),
("""              value: shiftId === null ? NO_SHIFT : String(shiftId),
              options: [
                ...spaceShifts.map((shift) => ({
                  value: String(shift.id),
                  label: language === 'en' ? (shift.nameEn ?? shift.nameAr) : shift.nameAr,
                })),
                { value: NO_SHIFT, label: words.noShift },
              ],""","""              value: shiftId === null ? '' : String(shiftId),
              options: spaceShifts.map((shift) => ({
                value: String(shift.id),
                label: language === 'en' ? (shift.nameEn ?? shift.nameAr) : shift.nameAr,
              })),"""),
("      label: full ? words.submitAnyway : words.submit,","      label: full !== null ? words.submitAnyway : words.submit,"),
])
edit('components/visit/VisitDialog.tsx' if False else 'features/desk/components/visit/VisitDialog.tsx',[
("""  Button,
  Checkbox,
  Dialog,""","""  Button,
  Dialog,"""),
("""  Input,
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@shared/design-system';""","""  Input,
  Switch,
  ToggleGroup,
  ToggleGroupItem,
} from '@shared/design-system';"""),
("""              <Checkbox
                checked={student.checked}
                onCheckedChange={(checked) => {
                  student.change(checked === true);
                }}
                disabled={dialog.submit.busy}
              />""","""              <Switch
                checked={student.checked}
                onCheckedChange={student.change}
                disabled={dialog.submit.busy}
              />"""),
("""              <Select
                value={shift.value}
                onValueChange={shift.change}
                disabled={dialog.submit.busy}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {shift.options.map((option) => (
                    <SelectItem key={option.value} value={option.value}>
                      {option.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>""","""              {/* One chip or none: a chosen chip pressed again leaves no shift. */}
              <ToggleGroup
                type="single"
                value={shift.value}
                onValueChange={shift.change}
                disabled={dialog.submit.busy}
                className="flex-wrap justify-start"
              >
                {shift.options.map((option) => (
                  <ToggleGroupItem key={option.value} value={option.value}>
                    {option.label}
                  </ToggleGroupItem>
                ))}
              </ToggleGroup>"""),
])
edit('pages/dashboard/space/desk/DeskPage.tsx',[
("""  const full = now?.status === 'FULL';""","""  // Full by the count, not by the status a manual override may set (G13.9).
  const full =
    now !== undefined && now.capacity !== null && now.present >= now.capacity
      ? { present: now.present, capacity: now.capacity }
      : null;"""),
])
edit('shared/copy/arabic/desk.ts',[("    full: 'المساحة ممتلئة؛ يمكنك التسجيل على أي حال، وتبقى حالتها للزوار «ممتلئ».',","    full: ({ ratio }: { ratio: string }) =>\n      `المساحة ممتلئة ${ratio}؛ يمكنك التسجيل على أي حال، وتبقى حالتها للزوار «ممتلئ».`,")])
edit('shared/copy/english/desk.ts',[("    full: 'The space is full; you can still check in, and visitors keep seeing “Full”.',","    full: ({ ratio }: { ratio: string }) =>\n      `The space is full ${ratio}; you can still check in, and visitors keep seeing “Full”.`,")])
