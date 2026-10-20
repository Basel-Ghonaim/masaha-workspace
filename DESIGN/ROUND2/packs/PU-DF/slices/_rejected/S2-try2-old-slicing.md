# PU-DF · S2 · B09–B22
Images viewed: yes — the header shows “مساحة” with a menu button; “English” with a language icon is on the other side.

## Findings

### S2-01 — English sort label is clipped
- frame: B09-768-en-light   (also: B09-768-en-dark, B09-1440-en-light, B09-1440-en-dark; B11, B12, B14–B22 at 768 and 1440 in English light and dark)
- type: defect · level: page · impact: low
- where: Directory list, default sort, `Directory.html?loc=none`
- fact: `clipped x: span «Sort: Recently updated» — content 154px in 146px`; at 768 and 1440 the sort trigger visibly truncates the final “d” in “updated”.
- proposal: Give the sort `Select` trigger enough inline space for its full label and chevron at tablet and desktop widths, using the existing Field/control sizing and responsive layout tokens.
- why: People can read the active sort without guessing its final word.
- cost: S · rule: foundation §9, Responsive layout

## Decisions in doubt
- None.

## Not judged
- None.
