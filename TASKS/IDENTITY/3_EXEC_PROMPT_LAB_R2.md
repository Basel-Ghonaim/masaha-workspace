# IDENTITY — palette lab, round 2 (a note to the same OpenCode session in app-b)

Proposed 2026-11-05; send only on the owner's yes. Paste into the lab worker's session:

```
Owner's note — round 2 of the lab:
1. Add a screen "Status check" to the lab (a page of its own inside the lab, no prototype file edited): side by side, in both themes, a primary Button, a destructive Button, a destructive Alert with text, a success and a warning Badge, a primary link, and the "verified" badge — so primary vs destructive can be judged by eye.
2. Add two palettes next to Sea sunset:
   - "Sea sunset 2": the same neutrals, the brand seed's hue moved toward orange until the hue-clash warning against red-600 disappears (keep amber-500 out of the 25° range too; if both cannot be met, take the hue farthest from both and say so).
   - "Sea sunset 3": Sea sunset's brand unchanged, and the red ramp replaced by a deeper crimson (red-600 hue moved away from the brand by at least 25°, every contrast pair still passing). The lab may override --red-* for this palette only.
3. Fix "copy values": it prints a literal "\n"; output real line breaks, a valid Markdown table.
Fold each change into the lab's commit (backup/palette-lab-1 first, --fixup + autosquash). Both checks, screenshots of Status check for the three sunsets in both themes into C:\Users\basel\Downloads\palette-lab-shots\round2\, then stop and print the URLs.
```
