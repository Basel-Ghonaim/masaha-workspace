W = 'C:/dev/masaha/app/apps/web/src/features/desk/hooks/sheet/useSheetForm.ts'
s = open(W, encoding='utf-8').read()
pairs = [
    ("import { useState } from 'react';", "import { useEffect, useRef, useState } from 'react';"),
    ("""  sheetSchema,
  type SheetRequest,""", """  sheetSchema,
  type PublishedChoice,
  type SheetRequest,"""),
    ("""  shifts,
  renewalOfId,
  submit,
}: {""", """  shifts,
  renewalOfId,
  published,
  customDefaults,
  submit,
}: {"""),
    ("""  renewalOfId?: number;
  submit: (request: SheetRequest) => Promise<unknown>;
}) {""", """  renewalOfId: number | undefined;
  /** The published prices offered, by their choice's value. */
  published: ReadonlyMap<string, PublishedChoice>;
  /** A renewal of custom terms repeats them. */
  customDefaults: Partial<SheetValues['custom']> | null;
  submit: (request: SheetRequest) => Promise<unknown>;
}) {"""),
    ("""  const [schema] = useState(() => sheetSchema(newCustomer));
""", """  const [schema] = useState(() => sheetSchema(newCustomer));
  // The form's check is made once; what it reads that changes while the sheet is open — the renewal
  // and the prices read again — it reads from here when it runs.
  const request = useRef({ renewalOfId, published });
  useEffect(() => {
    request.current = { renewalOfId, published };
  }, [renewalOfId, published]);
"""),
    ("""        totalHours: '',
        reason: '',
      },""", """        totalHours: '',
        reason: '',
        ...customDefaults,
      },"""),
    ("""    prepare: (values) => sheetInput(values, { newCustomer, renewalOfId }),""",
     """    prepare: (values) => sheetInput(values, { newCustomer, ...request.current }),"""),
]
for old, new in pairs:
    assert s.count(old) == 1, old[:60]
    s = s.replace(old, new)
open(W, 'w', encoding='utf-8', newline='').write(s)
print('ok')
