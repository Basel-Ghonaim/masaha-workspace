# PU-DF · S2 · B09–B22
Images viewed: no

## Findings

### S2-01 — Sort label clipped in English at 768 and 1440
- frame: B09-768-en-light   (also: B09-768-en-dark, B09-1440-en-light, B09-1440-en-dark, B11-768-en-light, B11-768-en-dark, B11-1440-en-light, B11-1440-en-dark, B12-768-en-light, B12-768-en-dark, B12-1440-en-light, B12-1440-en-dark, B14-768-en-light, B14-768-en-dark, B14-1440-en-light, B14-1440-en-dark, B15-768-en-light, B15-768-en-dark, B15-1440-en-light, B15-1440-en-dark, B16-768-en-light, B16-768-en-dark, B16-1440-en-light, B16-1440-en-dark, B17-768-en-light, B17-768-en-dark, B17-1440-en-light, B17-1440-en-dark, B18-768-en-light, B18-768-en-dark, B18-1440-en-light, B18-1440-en-dark, B19-768-en-light, B19-768-en-dark, B19-1440-en-light, B19-1440-en-dark, B20-768-en-light, B20-768-en-dark, B20-1440-en-light, B20-1440-en-dark, B21-768-en-light, B21-768-en-dark, B21-1440-en-light, B21-1440-en-dark, B22-768-en-light, B22-768-en-dark, B22-1440-en-light, B22-1440-en-dark)
- type: defect · level: component · impact: medium
- where: Directory page (list view), `Directory.html?loc=none` and variants, 768 & 1440, English, light & dark
- fact: clipped x: span «Sort: Recently updated» — content 154px in 146px
- proposal: Widen the sort label container by at least 8px, or shorten the English label to "Sort: Recent" (matching the Arabic "الترتيب: الأحدث" which fits), or allow the label to wrap. Use the design system's `text-body-2` token and ensure the container in the toolbar flexes.
- why: The current sort state is unreadable in English at tablet and desktop widths. Users cannot confirm which sort is active.
- cost: S · rule: foundation §9 (responsive), foundation §5 (spacing scale)

## Decisions in doubt
- None.

## Not judged
- B10 (loc=granted) and B13 (loc=manual) at 768/1440 English: these show "Sort: By distance" which fits; not clipped.
- All Arabic frames (390, 768, 1440, light, dark): Arabic label "الترتيب: الأحدث تحديثًا" fits in all measured frames.
- 390 English frames (light, dark): no clipping measured.
- Console errors, horizontal overflow, broken images, offscreen text, side scrollers: none measured in any frame of this slice.
- Map-view bases (B23–B28): outside this slice.
- Space details, About, Error pages (B29–B55): outside this slice.