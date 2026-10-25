p='C:/dev/masaha/app/apps/web/src/features/occupancy/components/PresentList.tsx'
s=open(p,encoding='utf-8',newline='').read()
def rep(old,new,count=1):
    global s
    assert s.count(old)==count, (old[:60], s.count(old))
    s=s.replace(old,new)
rep(" * and on returning to it; a failed refresh keeps the last list and says so.\n */",
    " * and on returning to it; a failed refresh keeps the last list and says so. When the person whose\n * action had the focus leaves the list, the focus goes to the next row's action, else to the\n * heading (S10), never to the page's start.\n */")
rep("import { useEffect, useId, useMemo, useState, type ReactNode } from 'react';",
    "import {\n  useEffect,\n  useId,\n  useMemo,\n  useRef,\n  useState,\n  type FocusEvent,\n  type ReactNode,\n} from 'react';")
rep("""  const list = usePresentList(spaceId, { now });
  const headingId = useId();
""","""  const list = usePresentList(spaceId, { now });
  const headingId = useId();
  const section = useRef<HTMLElement | null>(null);
  const heading = useRef<HTMLHeadingElement | null>(null);
  // The row whose action last had the focus, and its place in the list.
  const focused = useRef<{ key: string; index: number } | null>(null);
  const keys = list.rows.map((row) => row.key);
  const keysKey = keys.join(' ');
  const remember = (event: FocusEvent<HTMLElement>) => {
    const holder = (event.target as HTMLElement).closest<HTMLElement>('[data-present-action]');
    const key = holder?.dataset.presentAction;
    focused.current = key === undefined ? null : { key, index: keys.indexOf(key) };
  };
  useEffect(() => {
    const last = focused.current;
    const rows = keysKey === '' ? [] : keysKey.split(' ');
    if (last === null || rows.includes(last.key)) return;
    focused.current = null;
    // Only a focus the row took with it: one the user moved elsewhere stays there.
    if (document.activeElement !== document.body) return;
    const next = rows[Math.min(last.index, rows.length - 1)];
    const target =
      next === undefined
        ? null
        : section.current?.querySelector<HTMLElement>(
            `[data-present-action="${next}"] button:not([disabled])`,
          );
    (target ?? heading.current)?.focus();
  }, [keysKey]);
""")
rep("""          cell: (info) => action(info.row.original.person),""","""          cell: (info) => (
            <div data-present-action={info.row.original.key}>
              {action(info.row.original.person)}
            </div>
          ),""")
rep("""              {action(row.person)}
            </div>""","""              <div data-present-action={row.key}>{action(row.person)}</div>
            </div>""")
rep("""    <section aria-labelledby={headingId} className="flex flex-col gap-3">
      <h2 id={headingId} className="flex items-baseline gap-2 text-heading-3">""","""    <section
      ref={section}
      aria-labelledby={headingId}
      onFocus={remember}
      className="flex flex-col gap-3"
    >
      <h2
        ref={heading}
        id={headingId}
        tabIndex={-1}
        className="flex items-baseline gap-2 text-heading-3"
      >""")
open(p,'w',encoding='utf-8',newline='').write(s)
