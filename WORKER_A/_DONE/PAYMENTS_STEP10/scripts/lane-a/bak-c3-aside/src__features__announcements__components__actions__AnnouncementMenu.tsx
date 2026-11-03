import {
  Button,
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  EllipsisVerticalIcon,
} from '@shared/design-system';
import { useLayoutEffect, useRef, useState } from 'react';
import type { AnnouncementActionsView } from '../../hooks/actions/useAnnouncementActions';
import type { AnnouncementCardView } from '../../types/AnnouncementCardView';
import { DeleteDialog } from './DeleteDialog';

/**
 * A card's «⋯», named by its announcement («إجراءات أخرى: {type} · {period}»), holding «حذف…»,
 * destructive, which opens its dialog. Closed, the focus goes back to the «⋯»; once the «⋯» is gone
 * with the focus on it — the announcement deleted, its card gone — `onGone` places it.
 */
export function AnnouncementMenu({
  spaceId,
  card,
  menu,
  onGone,
}: {
  spaceId: number;
  card: AnnouncementCardView;
  menu: AnnouncementActionsView['menu'] & {
    remove: NonNullable<AnnouncementActionsView['menu']['remove']>;
  };
  onGone: () => void;
}) {
  const [open, setOpen] = useState(false);
  const trigger = useRef<HTMLButtonElement | null>(null);
  const gone = useRef(onGone);
  useLayoutEffect(() => {
    gone.current = onGone;
  });

  // Leaving while it holds the focus, it hands the focus on, before the browser drops it on the body.
  useLayoutEffect(() => {
    const button = trigger.current;
    return () => {
      if (button !== null && button === document.activeElement) gone.current();
    };
  }, []);

  return (
    <>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            ref={trigger}
            variant="ghost"
            size="icon"
            aria-label={menu.label}
            data-card-action=""
          >
            <EllipsisVerticalIcon aria-hidden />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" aria-label={menu.label}>
          <DropdownMenuItem
            variant="destructive"
            onSelect={() => {
              setOpen(true);
            }}
          >
            {menu.remove.label}
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
      {open && (
        <DeleteDialog
          spaceId={spaceId}
          card={card}
          onClose={() => {
            setOpen(false);
          }}
          returnFocus={() => {
            if (trigger.current?.isConnected === true) trigger.current.focus();
            else onGone();
          }}
        />
      )}
    </>
  );
}
