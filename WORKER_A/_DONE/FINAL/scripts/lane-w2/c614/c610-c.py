import os
os.chdir('C:/dev/masaha/app-lane-w2/apps/web/src')


def edit(p, pairs):
    s = open(p, encoding='utf8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)


def write(p, text):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf8', newline='').write(text)


S = 'features/spaces/'
write(S + 'hooks/editor/useHashLanding.ts', """import { useEffect, useRef } from 'react';
import { useLocation } from 'react-router';

/**
 * The element a hash names, as the focus takes it: the heading a section is titled by (it carries
 * `tabIndex={-1}`), or the element itself when it takes the focus.
 */
function landingOf(hash: string): HTMLElement | null {
  if (hash.length < 2) return null;
  let named: HTMLElement | null;
  try {
    named = document.getElementById(decodeURIComponent(hash.slice(1)));
  } catch {
    return null;
  }
  if (named === null) return null;
  return named.hasAttribute('tabindex')
    ? named
    : (named.querySelector<HTMLElement>('h2[tabindex], h3[tabindex]') ?? null);
}

/**
 * Lands the editor on the section the address's hash names (184): once its cards have drawn
 * (`drawn`, the read answered), it scrolls to it and focuses its heading — once per opening of the
 * page; a later change of the hash alone is the shell's (`useMainFocus`). The cards and the report's
 * notice draw only after the read, so the browser's own jump to the hash found nothing.
 */
export function useHashLanding(drawn: boolean): void {
  const { hash } = useLocation();
  const landed = useRef(false);

  useEffect(() => {
    if (!drawn || landed.current) return;
    landed.current = true;
    const target = landingOf(hash);
    if (target === null) return;
    target.scrollIntoView({ block: 'start' });
    target.focus({ preventScroll: true });
  }, [drawn, hash]);
}
""")

edit(S + 'components/editor/SpaceEditor.tsx', [
("""import { useRef } from 'react';
import { useSpaceEditor } from '../../hooks/editor/useSpaceEditor';""",
 """import type { FactGroup } from '@masaha/shared/spaces';
import { useRef, type ReactNode } from 'react';
import { useHashLanding } from '../../hooks/editor/useHashLanding';
import { useSpaceEditor } from '../../hooks/editor/useSpaceEditor';"""),
(""" * owner of a verified space, the link on an unverified one.
 */""", """ * owner of a verified space, the link on an unverified one. A page may set a notice above a section
 * (`noticeFor`, by its fact group), such as an open report's (`data-reports`). Once the cards have
 * drawn, the editor lands on the section the address's hash names (184).
 */"""),
("""  publicLink,
}: {
  spaceId: number;
  place: AdminPlace | OwnerPlace;
  areaField: AreaField;
  amenitiesField: AmenitiesField;
  publicLink: (slug: string) => string;
}) {
  const editor = useSpaceEditor(place.kind, spaceId);""", """  publicLink,
  noticeFor,
}: {
  spaceId: number;
  place: AdminPlace | OwnerPlace;
  areaField: AreaField;
  amenitiesField: AmenitiesField;
  publicLink: (slug: string) => string;
  /** What the page sets above a section of the editable editor, if anything. */
  noticeFor?: (group: FactGroup) => ReactNode;
}) {
  const editor = useSpaceEditor(place.kind, spaceId);
  useHashLanding(editor.state === 'ready');"""),
("""            <>
              <ProfileSection""", """            <>
              {noticeFor?.('profile')}
              <ProfileSection"""),
("""              <HoursSection""", """              {noticeFor?.('hours')}
              <HoursSection"""),
("""              {place.kind === 'owner' && editor.pricesLink ? (""",
 """              {noticeFor?.('prices')}
              {place.kind === 'owner' && editor.pricesLink ? ("""),
("""              <AmenitiesSection""", """              {noticeFor?.('amenities')}
              <AmenitiesSection"""),
("""              <ContactsSection""", """              {noticeFor?.('contacts')}
              <ContactsSection"""),
])

edit(S + 'components/editor/SectionCard.tsx', [
("""          <h2>{frame.title}</h2>""", """          {/* A link's hash lands on it (184). */}
          <h2 tabIndex={-1} className="outline-none">
            {frame.title}
          </h2>"""),
])
edit(S + 'components/editor/PricesLinkCard.tsx', [
("""          <h2>{view.title}</h2>""", """          <h2 tabIndex={-1} className="outline-none">
            {view.title}
          </h2>"""),
])
edit(S + 'components/profile/ProfileSection.tsx', [
("""        <h3 id="location-title" className="text-label">""",
 """        <h3 id="location-title" tabIndex={-1} className="text-label outline-none">"""),
])
print('ok')
