import os, re
os.chdir(r'C:\dev\masaha\app-lane-w2\docs')
def edit(p,pairs):
    s=open(p,encoding='utf8').read()
    for a,b in pairs:
        assert s.count(a)==1,(p,a[:70]); s=s.replace(a,b)
    open(p,'w',encoding='utf8',newline='').write(s)
edit('features/spaces.md',[
("""then the layer's `Spinner` with its own percentage («جارٍ الرفع 45٪») — there is no progress component in the layer and none is added — then,""","""then the layer's `Meter` as a progress bar, named «جارٍ رفع الصورة {n}» by its place in the gallery, its value «45٪», with «جارٍ الرفع 45٪» as its caption (D6.14, 2026-10-29, #PRNUM), then,"""),
("""- **A pending tile is the layer's `Spinner` with its percentage as text;** there is no progress component and none is added. *Why:* the design drew a `role="progressbar"` bar, which is a CSS class and a style outside the layer ([finding 73](../architecture/findings/73-the-gallerys-per-tile-progress-has-no-component-in-the-layer.md)). 2026-10-17, #85.""","""- **An uploading tile is the layer's `Meter` as a progress bar** (D6.14, superseding #85's spinner): the layer has the component since this PR, so the design's bar is drawn with it, its percentage as the caption; a file still being prepared keeps the `Spinner` ([finding 73](../architecture/findings/73-the-gallerys-per-tile-progress-has-no-component-in-the-layer.md)). 2026-10-29, #PRNUM."""),
("""- [73](../architecture/findings/73-the-gallerys-per-tile-progress-has-no-component-in-the-layer.md): the gallery's per-tile progress has no component in the layer.
""",""),
("""- [74](../architecture/findings/74-the-designs-gallery-copy-states-limits-the-contract-no-longer-has.md): the design's gallery copy states limits the contract no longer has.
""",""),
])
p='features/spaces.md'
s=open(p,encoding='utf8').read().rstrip('\n')+"\n- #PRNUM — an uploading photo's tile drawn as the layer's progress bar (finding 73); the design's gallery line says the contract's limits (finding 74).\n"
open(p,'w',encoding='utf8',newline='').write(s)
for f, res in [('73-the-gallerys-per-tile-progress-has-no-component-in-the-layer.md',"The layer's `Meter` draws each tile's progress (D3.1, D6.14): `kind=\"progress\"`, named «جارٍ رفع الصورة {n}», its value «{p}٪», the percentage its caption."),
               ('74-the-designs-gallery-copy-states-limits-the-contract-no-longer-has.md',"The prototype's gallery line says the contract's limits (D6.14): «حتى 10 صور · JPEG أو PNG أو WebP · حتى 4 ميغابايت للصورة», its chooser and refusals the same; `docs/design/CHANGES.md` has the row.")]:
    p='architecture/findings/'+f
    s=open(p,encoding='utf8').read()
    s=s.replace("**Status:** Open · **Date:** 2026-10-17","**Status:** Resolved · **Date:** 2026-10-17 · **Resolved:** 2026-10-29")
    s=s.rstrip('\n')+"\n\n**Resolution (#PRNUM):** "+res+"\n"
    open(p,'w',encoding='utf8',newline='').write(s)
