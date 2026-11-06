# Owner Space Profile — implementation plan

## Summary

Redesign the Owner space-profile page from an edit-first page into a visitor-facing View page
with six independently editable section Sheets, preserving the existing managed API contracts,
authorization, localization, design-system primitives and server-authoritative behavior.

## Contract

### In scope

- Owner route `/dashboard/spaces/:spaceId/profile`.
- View cards, section navigation, freshness summary and stale confirmation.
- Independent Sheets for profile/location, photos, hours, prices, amenities and contacts.
- Grouped-hours form models serialized to the existing seven-day API shape.
- Accessible drag-and-drop-only photo reordering with server-confirmed auto-save.
- Existing loading, error, success, dirty-close, authorization and localization patterns.
- Required unit, component, API and browser evidence.
- Directly related capability documentation updates.

### Acceptance criteria

- The page opens in View mode with the six sections in the approved order.
- Every editable section opens its own Sheet; Save and Cancel stay inside it.
- Failed saves preserve the draft and keep the Sheet open; successful saves update View and close it.
- Freshness counts distinguish missing and stale groups; photos are excluded.
- Hours support arbitrary groups, Friday, per-day custom mode and one interval per day without
  changing the API contract.
- Prices preserve all supported dimensions, metadata, unavailable values and shift associations.
- Photo reorder sends a complete permutation, is not optimistic, and is accessible without
  pointer-only behavior.
- Owner-only server authorization and existing error semantics remain unchanged.

### Out of scope

Admin-specific redesign, new routes or API/schema contracts, new dependencies without approval,
booking, payment, reviews, QR check-in, public-route redesign, audit changes and unrelated
refactors.

## Reading done

Read the bootstrap and workflow material, the documentation map, the spaces capability and related
lookups/packages/space-settings/announcements material, the API contract, the existing Owner editor
and tests, the design-system Sheet and map patterns, the copy/localization structure, the relevant
resolved findings, and the archived Owner prototype as historical reference. The repository state
was intentionally not changed during this review because the worker began on a dirty non-main
branch under the approved read-only exception.

## Baseline and handoff

- Base: `origin/main` at `077abda3058bf83c9dc4aef52df87f3e62f2380d0` (latest fetched objects; no checkout).
- Implementation branch: `feat/owner-space-profile`, cut from then-current `origin/main`; use the detached-worker convention if this is worker B.
- Owner experience only. No dedicated photos capability document exists: photos are specified in `docs/features/spaces.md` and `docs/api/api-contract.md`.

## Scope and acceptance contract

The Owner profile opens in View mode with six visitor-facing cards, ordered Basics & Location, Photos, Hours, Prices, Amenities, Contact. Each card has Edit and its own section Sheet; page stays visible, Sheet is full-screen on mobile. Save and Cancel remain in the Sheet. Groups save independently. Dirty close uses the existing leave confirmation. Success updates the page, closes the Sheet and uses existing success feedback; failure preserves entered values and keeps the Sheet open with existing error behavior. Add section navigation, one status summary counting groups needing confirmation, stale age with Still correct confirmation without editing, and View public page. Photos remain outside fact freshness, as they are in the existing contract, and reorder by drag-and-drop with auto-save.

Do not widen product scope, alter the public route, audit semantics or authorization model, or redesign shared patterns. Admin-specific behavior is deferred.

## Exact existing routes, files and contracts

Owner URL: `/dashboard/spaces/:spaceId/profile`, mounted by `apps/web/src/pages/dashboard/space/ProfilePage.tsx`. Route and role policy are in `apps/web/src/pages/dashboard/navigation.ts` and `apps/web/src/pages/dashboard/index.ts`. ProfilePage composes `SpaceEditor` from `@features/spaces`, supplying public `AreaSelect` and `AmenityChecklist`; retain those Owner-safe sources.

Refactor/reuse:
- Frame: `apps/web/src/features/spaces/components/editor/{SpaceEditor,OwnerHead,SectionNav,SectionCard,ReadOnlyCard,ReadOnlyRows,MissingChecklist,LeaveDialog,VerifiedNotice,PrivacyNote,EditorLoading,EditorFailure}.tsx`.
- Sections: `components/profile/{ProfileSection,ReadOnlyProfile,BasicsFields,LocationFields}.tsx`; `components/photos/{PhotosSection,PhotosCard,PhotoTile,PhotoUploadTile,PhotoRemoveDialog,ReadOnlyPhotos}.tsx`; `components/hours/{HoursSection,ReadOnlyHours}.tsx`; `components/prices/{PricesSection,ReadOnlyPrices,SpacePricesEditor}.tsx`; `components/amenities/{AmenitiesSection,ReadOnlyAmenities}.tsx`; `components/contacts/{ContactsSection,ReadOnlyContacts}.tsx`.
- Orchestration: `hooks/editor/{useSpaceEditor,useSpaceQuery,useSpaceAnswer,useSectionFrame,useSaveGroup,useLeaveGuard,useSectionInView,useHashLanding,usePricesLink,editorScope,meanwhileLines,sectionName}.ts`; section hooks `hooks/{profile/useProfileSection,profile/useReadOnlyProfile,hours/useHoursSection,hours/useReadOnlyHours,prices/usePricesSection,prices/useReadOnlyPrices,amenities/useAmenitiesSection,amenities/useReadOnlyAmenities,contacts/useContactsSection,contacts/useReadOnlyContacts}.ts`.
- Gallery: `hooks/photos/{usePhotoGallery,usePhotosQuery,usePhotoOrder,usePhotoRemove,usePhotoUploads,useReadOnlyPhotos,staleGallery}.ts`.
- Models/services: `services/{mayEdit,hoursForm,clockTime,pricesForm,amenitiesForm,profileInput,profileChanges}.ts`; `repository/spaceEditorRepository.ts`; `types/{EditorPlace,SectionFrameView,PhotoGalleryView,PhotoTileView,ProfileValues}.ts`.
- Existing tests to extend: `components/editor/SpaceEditor.component.test.tsx`; component tests for Photos, profile, hours, prices, amenities, contacts; `hooks/editor/{useLeaveGuard,useSectionFrame}.component.test.tsx` and corresponding section hook component tests; unit tests `services/{hoursForm,pricesForm,amenitiesForm,profileInput}.unit.test.ts`; `repository/spaceEditorRepository.unit.test.ts`.
- API is already provided by `createSpaceEditorRepository('owner')`: `GET /manage/spaces/:spaceId`, `PATCH /manage/spaces/:spaceId` (profile), `PUT /manage/spaces/:spaceId/{hours|prices|amenities|contacts}`, `POST /manage/spaces/:spaceId/{profile|hours|prices|amenities|contacts}/confirm`, `GET/POST /manage/spaces/:spaceId/photos`, `DELETE /manage/spaces/:spaceId/photos/:photoId`, `PUT /manage/spaces/:spaceId/photos/order` (complete ids list). Existing repository and contracts live in `apps/web/src/features/spaces/repository/spaceEditorRepository.ts`, `packages/shared/src/spaces`, and `docs/api/api-contract.md`. No new endpoint is planned.
- Reuse design-system Sheet, AlertDialog, Dialog, Button, Card, Field, Table, Toast and Meter; `shared/forms`, `shared/map/PointPicker`, `shared/uploads`, and `shared/copy`. Follow frontend architecture, design-system foundation and localisation docs. No DnD implementation was found in scanned `apps/web/src`.

## Component and state structure

Keep one page-level `useSpaceEditor` query and a stable six-item ordered descriptor list. Server answer powers View cards; existing read mappers remain canonical. Add a desktop sticky `ProfileSectionIndex`, compact mobile section menu, `ProfileFreshnessSummary`, and per-card freshness age/Still correct. Index links to card headings and marks section in view. Photos are not a fact group and are omitted from freshness totals.

A single discriminated `activeSheet` identifies the open section. Each Sheet seeds its form from the current answer and owns dirty/pending/failure draft state through existing hooks or small section sheet hooks. Save success consumes returned `AdminSpace`, updates query answer, closes Sheet and invokes existing success feedback. Failure retains draft and Sheet. Cancel, close button, Escape and outside-close requests all use dirty guard; pending writes cannot be discarded accidentally. Keep loading/not-found/authorization states unchanged.

### Basics & Location

View shows visitor-facing name, descriptions, area/address, verification state and small `PlaceMap`. Sheet edits bilingual name/description, area, address and location with larger `PointPicker`. Keep existing schema, Gaza bounds and map patterns. Mixed-language text carries correct `lang` and `dir`.

### Photos

View has an unmistakable first-image cover. Editor supports adding, deleting (existing confirmation) and drag-and-drop reorder only; remove before/after/cover buttons rather than keeping a second interaction. Drop computes a complete order from confirmed server ids, sends once, does not optimistically reorder and locks further reorder until accepted response/refetch. Upload retains existing limit (10), one-at-a-time browser shrink, progress, queue and server-returned row semantics; uploads append last. Delete confirms first and refetches authoritative order. Failed upload/delete/reorder preserves server order and retryable state where supported; 409 refreshes gallery and uses existing conflict feedback. Existing contracts remain. Resolve accessible DnD keyboard operation using a project-supported pattern; no dependency may be added silently.

### Hours

Replace repeated seven-day inputs as primary editor with grouped days over existing contract. Existing indexes are Sunday=0 through Saturday=6; render Saturday first. Default unsaved template is Saturday–Thursday 08:00–18:00, Friday closed. Common path starts with one Saturday–Thursday group and an easy Add Friday action. Owner can choose arbitrary groups (e.g. Saturday–Wednesday and Thursday–Friday), with independent opening/closing values, and move days among groups. “Set hours for each day” converts group values into individual daily groups without data loss; regrouping is reversible. Closed days have no interval. Exactly one continuous interval/day; no breaks or exceptional closures, which remain Announcements.

Serialize to existing `days[7]` shape (open day integer minutes; closed is null) and preserve existing shift ids/order and constraints. Validation bounds follow the shared schema: opening/start 00:00–23:59; closing/end 00:01–24:00, later than opening; 24:00 only allowed as end. Reuse Arabic-Indic parsing and HH:MM normalization. Require each open day in exactly one group; reject duplicates, omissions, empty groups and invalid intervals on their controls. View compacts adjacent days with identical intervals in Saturday-first locale order, e.g. “Saturday–Thursday 08:00–18:00 · Friday closed”; accurately split nonadjacent ranges.

### Prices

View and edit use one clear table, not repeated form rows. Canonical rows are `HOUR, DAY, WEEK, MONTH`; audience columns are contract-supported `GENERAL` (everyone), `STUDENT` (students). A cell supports an existing price or explicit unavailable/empty value, never zero as a substitute. Preserve shift association and custom labels permitted by the contract; if multiple rows can occupy a cell, show a concise contextual list/expansion instead of silently overwriting. Convert amounts through current form helpers to integer agorot; validate positive value, two decimal maximum, uniqueness, supported enums, shift references and contract maximum. Permit empty only as existing contract permits omission. Preserve every row and metadata on round trip.

### Amenities and Contact

Amenities View shows only actually enabled amenities, with existing catalogue icon and localized label. Sheet reuses existing checklist/catalogue/selection pattern and preserves linked retired items marked until intentionally removed. Contacts View shows only enabled/saved contact methods with current icon and label. Sheet adds/edits/removes existing seven types and preserves order; show existing normalized link/number preview while typing. Keep existing format, uniqueness and maximum validations. Each saves independently.

## Freshness, authorization and catalogue

Use server freshness timestamps and thresholds; do not duplicate threshold calculation. Fact groups are profile, hours, prices, amenities, contacts. Summary distinguishes missing/stale counts. Still correct uses existing confirm hook/route, prevents duplicate submit, refreshes answer and follows existing success/error/429 patterns. Photos have no confirmation.

Keep route owner-only. Server is authoritative: active OWNER can mutate managed space; reception and unauthorized/cross-space/ended links retain existing 403/404 semantics. UI hiding does not secure writes. Preserve verified-space read-only/admin behavior outside Owner flow. Admin-specific structure and behavior are deferred.

Reuse existing `copy.spaces.editor` names, validation, success, confirmation and error keys, existing freshness formatter, contact type labels, amenity catalogue labels, prices period/audience labels. Add new typed keys in `apps/web/src/shared/copy/{english,arabic}/spaces.ts` under `ownerProfile` only where necessary. Proposed complete new key set and translations:

| Key | English | Arabic |
|---|---|---|
| viewPublicPage | View public page | عرض الصفحة العامة |
| editSection | Edit {section} | تعديل {section} |
| sectionStatus | {count} sections need confirmation | {count} أقسام تحتاج إلى تأكيد |
| missingStatus | {count} sections are not confirmed yet | لم يتم تأكيد {count} أقسام بعد |
| lastUpdated | Last updated {age} ago | آخر تحديث منذ {age} |
| stillCorrect | Still correct | ما زالت صحيحة |
| save / cancel | Save / Cancel | حفظ / إلغاء |
| groupDays | Days in this group | الأيام في هذه المجموعة |
| addFriday | Add Friday | إضافة الجمعة |
| addHoursGroup | Add hours group | إضافة مجموعة ساعات |
| removeHoursGroup | Remove group | إزالة المجموعة |
| customHours | Set hours for each day | تخصيص ساعات كل يوم |
| groupHours | Group days with the same hours | تجميع الأيام ذات الساعات نفسها |
| hoursRange | {days}: {from}–{to} | {days}: {from}–{to} |
| closedDay | {day} closed | {day} مغلق |
| invalidDayGrouping | Assign each open day to one group | وزّع كل يوم مفتوح على مجموعة واحدة |
| priceUnavailable | Not available | غير متاح |
| dragPhoto | Reorder {photo} | إعادة ترتيب {photo} |
| dropPhotoPosition | Move {photo} to position {position} | نقل {photo} إلى الموضع {position} |
| photoOrderSaved | Photo order saved | تم حفظ ترتيب الصور |
| emptyContact | No contact methods added | لم تتم إضافة وسائل تواصل |
| emptyAmenities | No amenities enabled | لا توجد مرافق مفعّلة |

Reuse existing labels rather than duplicating them. Arabic plural functions must implement all six categories and both catalogues retain identical key/parameter shapes. Arabic wording requires owner approval. No hardcoded visible or assistive copy.

## Design issues

- The legacy gallery exposes movement controls while the approved requirement is drag-and-drop
  only. Replace that interaction rather than preserving conflicting buttons; use an existing
  accessible pattern and stop for approval if none exists.
- The legacy edit-first layout conflicts with the approved View-first structure. Use the existing
  Card, Sheet, focus-management and responsive navigation primitives instead of introducing a
  parallel overlay or page-level save bar.
- The narrow price table must not be allowed to clip at tablet widths. Use the design-system table
  semantics with controlled horizontal scrolling or an explicitly semantic responsive presentation.

These are implementation requirements, not additional design approvals; no design issue is built
outside the approved contract.

## Responsive, visual and accessibility requirements

Manually inspect 390, 768 and 1440 px, RTL/LTR, light/dark. At 1440 use sticky section index; at 768 and 390 use compact menu; 390 Sheets are full-screen. Avoid page overflow. Table remains understandable at phone/tablet using controlled horizontal scroll or semantic responsive table presentation. View map small and edit map larger. Logical properties and semantic tokens only. Record browser screenshots for RTL/LTR, both themes, phone and desktop per workflow.

All controls keyboard reachable with visible focus and explicit labels. Index exposes current item and anchors headings. Use design-system Sheet focus trap, initial focus and return-to-trigger. Close and Escape go through dirty guard. Errors associate with fields and focus first invalid field. Announce save/error/confirmation/upload progress/reorder completion once using established primitives. DnD must be keyboard operable via an existing accessible pattern/alternative; never ship pointer-only. AA contrast and states not color-only. Test correct language/direction for mixed-language content.

## Tests and deliberate breaks

Follow repository lanes, one behavior/one lane. New tests must be seen failing before production changes; don't use jsdom for visual/layout proof.

| Lane / test | Deliberate break caught |
|---|---|
| Unit `ownerProfileView.unit.test.ts` | Omitting group values, wrong freshness counts/public path, or merging distinct hours intervals |
| Unit `hoursForm.unit.test.ts` | Duplicate/missing day group, lossy custom conversion, or allowing 24:00 opening |
| Unit `pricesForm.unit.test.ts` | Dropped supported category/metadata or absent price coerced to zero |
| Unit `photoOrder.unit.test.ts` | Partial/non-permutation ids or optimistic order surviving a failed request |
| Component `SpaceEditor.component.test.tsx` | Non-View default, wrong six section order, missing index/status/public link |
| Component `OwnerProfileSheets.component.test.tsx` | Wrong Sheet, Save outside Sheet, lost draft/closed-on-error, or dirty close not confirmed |
| Component `HoursSection.component.test.tsx` | No Friday path, arbitrary group/custom mode broken, second interval or repeated crowded editor |
| Component `PricesSection.component.test.tsx` | Non-table UI, missing category/empty state, or edit diverges from View model |
| Component `PhotosSection.component.test.tsx` | Non-drag reorder, partial request, parallel stale reorder, or failure corrupts state |
| Component amenities/contacts tests | Disabled amenities shown, wrong catalogue source, contact preview/normalization missing |
| Component `ProfilePage.component.test.tsx` | Wrong route or Reception reaching owner profile |
| Component vitest-axe + keyboard cases | Unlabelled controls, focus leak, inaccessible Sheet or reorder |
| API integration existing managed-space API tests | Any protected route allows USER, other-space OWNER, RECEPTION, or ADMIN beyond contract |
| Browser manual | Visual/interaction problems in required 3 widths × 2 directions × 2 themes |

Extend existing API authorization tests only if existing coverage does not already prove every role/space for affected routes. No new API behavior means no redundant API tests. Use real browser/app requests for managed read and one reversible write/restore or confirmation; mocked component tests do not prove this. Capture requested screenshot matrix. E2E is not the owning lane for these interactions; run critical smoke if current workflow/release requires it.

## Commit sequence

Each is complete and working; subjects are Conventional Commits and ≤50 chars:
1. `feat(spaces): add owner view profile cards`
2. `feat(spaces): edit profile sections in sheets`
3. `feat(spaces): group owner opening hours`
4. `feat(spaces): reorder photos with drag and drop`
5. `test(spaces): cover owner profile redesign`

Fold tests and copy alongside the behavior they prove. Split only if each intermediate commit remains working. Run lint and typecheck for each commit.

## Local verification sequence

No code verification occurs in this planning phase. Implementation worker first reads current `docs/development/setup.md` prerequisites and uses its assigned database/ports. On final head run once, in order: `npm run lint`, `npm run typecheck`, `npm run check:classes`, `npm run test:unit`, `npm run test:component`, `npm run test:api` (isolated PostgreSQL required), `npm run build`, `npm run check:build`, `npm run format:check`, `npm run check:links`, `npm run check:conflicts`. Start configured web/API for a real browser run, verify Owner route and a real managed request, inspect variant matrix, stop servers and confirm ports free. Record exact commands/results, skipped checks and why, browser evidence/screenshots, branch/head, failures and resolutions. Never reset shared or production database.

## Review Focus

Planned tests do not fully exercise visual fidelity across every combination of 390, 768 and
1440 pixels, RTL/LTR, light/dark themes, real browser drag gestures, screen-reader announcement
quality, or behavior against a concurrently changed remote answer. These remain explicit manual
review checks. The browser matrix and one real managed request are required evidence.

## Decisions needed from the owner

None remain for the approved plan. Implementation must stop and ask if no existing accessible
drag-and-drop pattern can satisfy the drag-only requirement, or if the existing contracts prove
insufficient and would require a new dependency, endpoint, schema or shared rule.

## Strong(er) decisions

- Keep existing managed routes and seven-day API shape; group days only in form/view models. Reason: server already validates one interval/day, avoiding schema change. Cost: transformation and round-trip tests. Recommendation: proceed.
- Photos remain outside freshness status; capability/API explicitly define no date or confirmation. Cost: status count is five facts though page has six cards. Recommendation: proceed.
- Keep canonical price dimensions while preserving shift/custom-label data; cells can contain multiple contextual entries if permitted. Cost: cell detail/expansion complexity. Recommendation: proceed.
- Reflect photo order only after server acceptance and serialize order writes, matching current server-authoritative contract. Cost: short pending state. Recommendation: proceed.
- Keep the new Owner profile as the primary editing surface for prices while retaining the existing
  Packages & prices route as a separate capability surface where required by its contract. The two
  surfaces must share the same repository contracts and canonical price model; neither may silently
  overwrite unsupported rows, shifts, labels or unavailable values. Cost: duplicated navigation and
  round-trip coverage. Recommendation: proceed, and update the spaces capability document so the
  ownership of each surface is explicit.
- Treat `docs/design/prototype/Owner space profile.html` as historical clarification only. The current
  prompt, capability document and existing code/contracts win where they differ. Cost: prototype-only
  interaction details may be discarded. Recommendation: proceed.
- The photo requirement remains drag-and-drop only. Do not retain before/after/cover movement buttons
  as a fallback. Implement an existing accessible drag-and-drop pattern if one is available; if none
  exists, stop before implementation and request owner approval for a changed requirement or an
  approved dependency. Cost: this may block the photo slice. Recommendation: proceed without
  pointer-only behavior or silent dependency additions.
- `View public page` belongs in the page header on desktop and in the compact header/menu action on
  narrow screens, avoiding a dense six-card header while keeping the action discoverable. Cost:
  responsive placement must be covered by browser evidence. Recommendation: proceed.
- Update `docs/features/spaces.md` in the same implementation PR because this work changes the
  capability's web behavior and the documented price-editing relationship. Review the deferred
  documents map and update `docs/project/overview.md` only if this work meets its Built-section
  trigger. Cost: documentation changes are part of Done. Recommendation: proceed.

## Related findings

The following open or resolved findings touch this item and must be checked during implementation:

- Finding 36, empty fact groups and freshness: fold its resolved semantics into the
  freshness-summary tests; cost is limited to missing-versus-stale fixtures.
- Finding 43, races around space facts: do not change the resolved server locking contract; fold
  client refetch/authoritative-answer behavior into tests where this item refreshes after writes.
- Finding 63, photo files outliving rows: do not fold; photo storage reclamation is separate API work.
- Finding 67, prices table at narrow widths: fold into the responsive price-table design/test review.
- Finding 69, owner managed route refusal for deleted spaces: do not change the API; preserve the
  existing error mapping and include the route in authorization/error coverage.
- Finding 73, gallery progress component: fold only if the existing upload progress UI is touched;
  otherwise record it as unchanged and do not widen scope.
- Finding 74, outdated gallery limit copy: fold if current copy is changed by the gallery work,
  otherwise preserve the contract-driven limit and avoid unrelated copy cleanup.
- Finding 95, editor-to-public-page wording/link: fold into the public-page action and copy review.

## Files and documentation ownership

Repository implementation files are limited to the existing Owner space editor, its shared
space-editor types/services/hooks/components/tests, the two copy catalogues, and the directly
related `docs/features/spaces.md` documentation. The API and shared package are read-only unless
implementation proves an existing contract is insufficient; a new endpoint, schema, shared rule or
dependency requires owner approval before editing. The design prototype is read-only reference.

## Out of scope

Admin-specific structure, content, permissions and behavior; Admin reuse decision is deferred to a later Work Item. Do not refactor Admin editor except an unavoidable shared contract proposed for approval. No new routes/schema absent an approved necessary contract; no booking, payment, reviews, QR check-in or other Not-in-v1 work.
