import os
os.chdir('C:/dev/masaha/app-lane-w2/apps/web/src/features/lookups')


def edit(p, pairs):
    s = open(p, encoding='utf8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)


edit('hooks/useAmenityForm.ts', [
("""import { useController, useWatch, type DefaultValues } from 'react-hook-form';
import type { AmenityFormView } from '../types/AmenityFormView';
""", """import { useController, type DefaultValues } from 'react-hook-form';
import type { Positioned } from '../services/withPosition';
import type { AmenityFormView } from '../types/AmenityFormView';
import type { RowPlace } from '../types/RowPlace';
import { useRowPosition } from './useRowPosition';
"""),
("""/**
 * Every value an amenity's form may hold. Each form sets the ones its request takes, and its schema
 * keeps only those: the Active switch only when editing. A new amenity has no icon until one is
 * chosen.
 */
type AmenityValues = {
  nameAr: string;
  nameEn: string;
  icon: AmenityIconKey | undefined;
  isActive: boolean;
};""", """/**
 * Every value an amenity's form may hold: its names, its icon, and the position, typed, which is
 * its list's. A new amenity has no icon until one is chosen.
 */
type AmenityValues = {
  nameAr: string;
  nameEn: string;
  icon: AmenityIconKey | undefined;
  position: string;
};"""),
("""/**
 * What an amenity's forms share, on the one form pattern (`useServerForm`): the two names, then the
 * icon, chosen from the shared keys, each named; and when `editing`, the Active
 * switch, since a new amenity is always active. The save sends the request (`save`), then closes the
 * sheet (`onSaved`) once the list shows the change.
 */""", """/**
 * What an amenity's forms share, on the one form pattern (`useServerForm`): the two names, then the
 * icon, chosen from the shared keys, each named; and, editing an amenity of a list of more than ten
 * (`place`), its position. Its switch stays in its row, the one control of whether it is offered.
 * The save sends the request (`save`), then the new position, if any, then closes the sheet
 * (`onSaved`) once the list shows the change.
 */"""),
("""  defaultValues,
  editing,
  save,
  onSaved,
}: {
  schema: ServerFormOptions<AmenityValues, Request>['schema'];
  defaultValues: DefaultValues<AmenityValues>;
  editing: boolean;
  save: (request: Request) => Promise<unknown>;
  onSaved: () => void;
}): AmenityFormView {
  const copy = useCopy();
  const lines = copy.lookups.sheet;
  const { field, submit, isPending, blocked, errors, failure, form } = useServerForm<
    AmenityValues,
    Request
  >({
    schema,
    defaultValues,
    fields: ['nameAr', 'nameEn', 'icon'],
    submit: async (request) => {
      await save(request);
      onSaved();
    },""", """  defaultValues,
  save,
  onSaved,
  place,
}: {
  schema: ServerFormOptions<AmenityValues, Request>['schema'];
  defaultValues: DefaultValues<AmenityValues>;
  save: (request: Request) => Promise<unknown>;
  onSaved: () => void;
  place?: RowPlace;
}): AmenityFormView {
  const copy = useCopy();
  const lines = copy.lookups.sheet;
  const position = useRowPosition(place);
  const { field, submit, isPending, blocked, errors, failure, form } = useServerForm<
    AmenityValues,
    Positioned<Request>
  >({
    schema: position.schema(schema),
    defaultValues: { ...defaultValues, position: position.defaultValue },
    fields: ['nameAr', 'nameEn', 'icon', 'position'],
    prepare: (values) => ({ ...values, position: position.input(values.position) }),
    submit: async ({ position: to, ...request }) => {
      await save(request as Request);
      await position.save(to);
      onSaved();
    },"""),
("""      icon: lines.fieldErrors.icon,
    },
  });
  const isActive = useWatch({ control: form.control, name: 'isActive' });
""", """      icon: lines.fieldErrors.icon,
      position: position.lines,
    },
  });
"""),
("""    ...(editing && {
      active: {
        label: lines.amenityActive,
        hint: lines.amenityActiveHint,
        checked: isActive,
        disabled: isPending,
        toggle: (checked: boolean) => {
          form.setValue('isActive', checked, { shouldDirty: true });
        },
      },
    }),
  };""", """    ...(positionField && { position: positionField }),
  };"""),
("""  const { field: icon } = useController({ control: form.control, name: 'icon' });
""", """  const { field: icon } = useController({ control: form.control, name: 'icon' });
  const positionField = position.view(field('position'), errors.position);
"""),
])

edit('types/AmenityFormView.ts', [
("""import type { LookupNameField } from './LookupFormView';

/** One of a sheet's switches, ready to render: its label, its hint and its state. */
type SwitchFieldView = {
  label: string;
  hint: string;
  checked: boolean;
  disabled: boolean;
  toggle: (checked: boolean) => void;
};

/**
 * An amenity's form in the sheet, ready to render: its two names, its icon chosen from a grid, and
 * when editing its Active switch (a new one is always active), with their labels,
 * errors and states. Its key is never shown: the server derives it.
 */""", """import type { LookupNameField } from './LookupFormView';
import type { PositionFieldView } from './PositionFieldView';

/**
 * An amenity's form in the sheet, ready to render: its two names, its icon chosen from a grid, and
 * when editing an amenity of a list of more than ten its position, with their labels, errors and
 * states. Its key is never shown: the server derives it; whether it is offered is its row's switch.
 */"""),
("""  active?: SwitchFieldView;
};""", """  position?: PositionFieldView;
};"""),
])

OLD_BLOCK = """        {form.active && (
          <Field orientation="horizontal" label={form.active.label} helper={form.active.hint}>
            <Switch
              checked={form.active.checked}
              disabled={form.active.disabled}
              onCheckedChange={form.active.toggle}
            />
          </Field>
        )}"""
edit('components/sheet/LookupForm.tsx', [
    ("import { Button, Field, SheetBody, SheetFooter, Switch } from '@shared/design-system';",
     "import { Button, SheetBody, SheetFooter } from '@shared/design-system';"),
    (OLD_BLOCK, "        {form.position && <PositionField position={form.position} />}"),
    ("import { LookupNameFields } from './LookupNameFields';",
     "import { LookupNameFields } from './LookupNameFields';\nimport { PositionField } from './PositionField';"),
    (" * the Active switch when editing, and Save at the sheet's foot.",
     " * the position when editing a row of a list of more than ten, and Save at the sheet's foot. The\n * row's switch stays in its row."),
])
edit('components/sheet/AmenityForm.tsx', [
    ("import { Button, Field, SheetBody, SheetFooter, Switch } from '@shared/design-system';",
     "import { Button, SheetBody, SheetFooter } from '@shared/design-system';"),
    (OLD_BLOCK, "        {form.position && <PositionField position={form.position} />}"),
    ("import { LookupNameFields } from './LookupNameFields';",
     "import { LookupNameFields } from './LookupNameFields';\nimport { PositionField } from './PositionField';"),
    (""" * An amenity's form, inside its sheet: the failure, the Arabic and English names, the icon, the
 * Active switch when editing, and Save at the sheet's foot.""", """ * An amenity's form, inside its sheet: the failure, the Arabic and English names, the icon, the
 * position when editing an amenity of a list of more than ten, and Save at the sheet's foot. The
 * amenity's switch stays in its row."""),
])

for p in ['hooks/add/useAddAmenityForm.ts', 'hooks/add/useAddAreaForm.ts', 'hooks/add/useAddGovernorateForm.ts']:
    edit(p, [('    editing: false,\n', '')])
print('ok')
