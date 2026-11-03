import type { ManagedAnnouncement } from '@masaha/shared/announcements';
import { Button } from '@shared/design-system';
import { useLayoutEffect, useRef, useState } from 'react';
import { ExtensionDialog } from './ExtensionDialog';

/**
 * «تمديد الاشتراكات» (outline), which opens its dialog, mounted anew for each opening (its key is
 * that opening's, S4). Closed, the focus goes back to it; once it is gone with the focus on it — the
 * closure extended, its card now saying so — the card's first other action takes the focus.
 */
export function ExtensionAction({
  spaceId,
  closure,
  label,
}: {
  spaceId: number;
  closure: ManagedAnnouncement;
  label: string;
}) {
  const [opening, setOpening] = useState(0);
  const trigger = useRef<HTMLButtonElement | null>(null);

  // Leaving while it holds the focus, it hands the focus to the card's next action.
  useLayoutEffect(() => {
    const button = trigger.current;
    return () => {
      if (button === null || button !== document.activeElement) return;
      const card = button.closest('[data-card-key]');
      const next = [...(card?.querySelectorAll<HTMLElement>('[data-card-action]') ?? [])].find(
        (action) => action !== button,
      );
      next?.focus();
    };
  }, []);

  return (
    <>
      <Button
        ref={trigger}
        variant="outline"
        className="self-start"
        data-card-action=""
        onClick={() => {
          setOpening((count) => count + 1);
        }}
      >
        {label}
      </Button>
      {opening > 0 && (
        <ExtensionDialog
          key={opening}
          spaceId={spaceId}
          closure={closure}
          onClose={() => {
            setOpening(0);
          }}
          returnFocus={() => {
            if (trigger.current?.isConnected === true) trigger.current.focus();
          }}
        />
      )}
    </>
  );
}
