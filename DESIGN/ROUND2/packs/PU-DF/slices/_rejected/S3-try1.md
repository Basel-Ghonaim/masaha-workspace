# PU-DF · S3 · B23–B29, B56
Images viewed: yes — the top bar shows “English,” “مساحة,” and the menu button.

## Findings

### S3-01 — The Arabic map legend exceeds its phone container
- frame: B24-390-ar-light
- type: defect · level: page · impact: low
- where: Directory map with Focus Hub selected, `Directory.html?view=map&selected=focus&loc=none`
- fact: the JSON measures `clipped x: content 382px in 356px`; the overflowing element contains the map status labels.
- proposal: let the map legend wrap within the map width, keeping each status mark and label together.
- why: Arabic users can read the complete status legend without content being cut off at the phone width.
- cost: S · rule: foundation §8 (direction); foundation §9 (responsive)

### S3-02 — The English sort label is clipped
- frame: B56-768-en-light   (also: B56-768-en-dark, B56-1440-en-light, B56-1440-en-dark)
- type: defect · level: page · impact: low
- where: Directory list with the filter sheet open and an inverted price range, `Directory.html?loc=none&sheet=filters&period=day&priceMin=30&priceMax=10`
- fact: the JSON measures `clipped x: span «Sort: Recently updated» — content 154px in 146px`.
- proposal: give the sort `Button` enough inline space for its label, allowing the filter controls to reflow at 768px.
- why: the sort choice remains readable in the Directory’s English interface at tablet and desktop widths.
- cost: S · rule: foundation §9 (responsive)

## Decisions in doubt
- None.

## Not judged
- All requested frames were checked in JSON; visual review was limited to the gate image and the listed screenshots. Other frame images were not opened individually, so image-only defects in them could not be judged.
