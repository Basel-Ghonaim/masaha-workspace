The plan is approved. Build it, with the answers below.

## Your decisions
- **D1 — approved:** `Switch` gets the `aria-disabled` look too, and `RowControls` drops its local
  classes.
- **D2 — approved:** `RowControls` gains `shown.text` and `switches` (both used by the amenity row;
  the governorates pass neither, output unchanged — their existing tests prove it).
- **D3 — approved:** extract `LookupNameFields`, no behaviour change.
- **D4 — approved:** switching tabs replaces the history entry; the default tab has no parameter.
- **D5 — changed for the icon:** a new amenity starts with **no icon selected**, and the icon is
  **required** (a validation line, "Choose an icon", and the grid takes the focus when it is missing).
  A preselected `wifi` would let an admin save the wrong icon without noticing; the choice should be
  deliberate. Every other field is unchanged; **"In filters" starts on**, as you proposed. (The
  `RadioGroup` still has exactly one checked once the admin chooses, and editing starts from the
  amenity's own icon.)

## Your proposed alternatives
- **T1 refinements — accepted:** the glyph map reuses the declared icon components, and the
  compile-time check is the typed `name={icon}` in `AmenityIcon`; make the break once and show
  `typecheck` failing.
- **T3 — `RadioGroup`, accepted,** for the reasons you gave.
- **T4 — accepted** with D2/D3 and the separate `useAmenityForm`.
- **T5 nuance — accepted:** the arrows don't wait on the row's switch writes (an order sends ids only).
  State this difference from the governorates' rows in `lookups.md`'s decisions, with its reason, so
  the next admin screen knows which to copy.

## The copy
All lines approved as written, both languages, plus the new required-icon line:
- English: "Choose an icon" · Arabic: «اختر أيقونة».

## Related findings
Agreed: 10 folded in; 30 stays accepted; 35 not folded.

Everything else stands: the behaviour, the files, the five commits, the tests with the breaks you
named, the Review Focus, the verification and the PR.
