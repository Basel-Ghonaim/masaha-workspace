import os
os.chdir(r'C:\dev\masaha\app-lane-w2\docs\design')
def edit(p,pairs):
    s=open(p,encoding='utf8').read()
    for a,b in pairs:
        assert s.count(a)==1,(p,a[:70]); s=s.replace(a,b)
    open(p,'w',encoding='utf8',newline='').write(s)
edit('prototype/masaha/profile-b.jsx',[
("const MAX_BYTES = 5 * 1024 * 1024;","const MAX_BYTES = 4 * 1024 * 1024;"),
("""      const why = !/^image\\/(jpeg|png)$/.test(f.type) ? tr('JPG أو PNG فقط', 'JPG or PNG only') : f.size > MAX_BYTES ? tr('أكبر من 5 ميغابايت', 'Larger than 5 MB') : null;""","""      const why = !/^image\\/(jpeg|png|webp)$/.test(f.type) ? tr('JPEG أو PNG أو WebP فقط', 'JPEG, PNG or WebP only') : f.size > MAX_BYTES ? tr('أكبر من 4 ميغابايت', 'Larger than 4 MB') : null;"""),
("""{tr('حتى 10 صور · JPG أو PNG · حتى 5 ميغابايت لكل صورة. الأولى هي الغلاف. كل تغيير يُحفظ فورًا.', 'Up to 10 photos · JPG or PNG · up to 5 MB each. The first is the cover. Every change is saved at once.')}""","""{tr('حتى 10 صور · JPEG أو PNG أو WebP · حتى 4 ميغابايت للصورة. الأولى هي الغلاف. كل تغيير يُحفظ فورًا.', 'Up to 10 photos · JPEG, PNG or WebP · up to 4 MB each. The first is the cover. Every change is saved at once.')}"""),
("""accept="image/jpeg,image/png" multiple""","""accept="image/jpeg,image/png,image/webp" multiple"""),
])
p='CHANGES.md'
s=open(p,encoding='utf8').read().rstrip('\n')
s+="""

## The build's corrections (2026-10-29)

Corrections the build asked of the living design, each with the decision of the plan that made it.

| Decision | What changed | Where |
|---|---|---|
| **D6.14** (finding 74) | The gallery's line says **the contract's limits**: «حتى 10 صور · JPEG أو PNG أو WebP · حتى 4 ميغابايت للصورة», the file chooser and its refusals the same; an uploading tile keeps its progress bar with its percentage, as the web's `Meter` draws it | `masaha/profile-b.jsx` (`Admin space edit.html`, `Owner space profile.html`) |
"""
open(p,'w',encoding='utf8',newline='').write(s)
