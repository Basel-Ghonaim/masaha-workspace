"""Write apps/web/public/favicon.svg from the owner's masaha-mark-berry.svg (read only).

The words path is defined once in <defs> and drawn twice with <use>; the clip rectangles and the
transforms are the mark file's own. Colours by class, switched by the browser's scheme.
"""
import re
import sys

REPO = r"C:\dev\masaha\app-design-lane-c"
SOURCE = REPO + r"\docs\design\prototype\masaha\logo\masaha-mark-berry.svg"
TARGET = sys.argv[1] if len(sys.argv) > 1 else REPO + r"\apps\web\public\favicon.svg"

with open(SOURCE, encoding="utf-8", newline="") as f:
    src = f.read()

view_box = re.search(r'viewBox="([^"]+)"', src).group(1)
clips = re.findall(r'<clipPath id="(\w)"><rect ([^/]+)/></clipPath>', src)
paths = re.findall(r'<path fill="(#[0-9A-Fa-f]{6})" fill-rule="evenodd" d="([^"]+)"/>', src)
transforms = re.findall(r'<g transform="([^"]+)">', src)

assert view_box == "190 17 778 778", view_box
assert [c[0] for c in clips] == ["h", "d"], clips
assert len(paths) == 3, len(paths)
(ink1, words1), (ink2, words2), (spark, dots) = paths
assert ink1 == ink2 == "#1A1F25" and spark == "#B55BB3", (ink1, ink2, spark)
assert words1 == words2, "the two ink copies differ"
assert transforms == ["translate(1158 0) scale(-1 1)", "translate(-11.5 0)"], transforms
# The structure checked whole: nothing in the source this script does not reproduce.
skeleton = re.sub(r' d="[^"]+"', ' d=""', src)
expected = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="190 17 778 778"><defs>'
    '<clipPath id="h"><rect ' + clips[0][1] + '/></clipPath>'
    '<clipPath id="d"><rect ' + clips[1][1] + '/></clipPath></defs>'
    '<g clip-path="url(#h)"><path fill="#1A1F25" fill-rule="evenodd" d=""/></g>'
    '<g transform="translate(1158 0) scale(-1 1)"><g clip-path="url(#h)"><path fill="#1A1F25" fill-rule="evenodd" d=""/></g></g>'
    '<g transform="translate(-11.5 0)"><g clip-path="url(#d)"><path fill="#B55BB3" fill-rule="evenodd" d=""/></g></g></svg>'
)
assert skeleton.strip() == expected, skeleton[:600]

style = (
    ".ink{fill:#1a1f25}.spark{fill:#b55bb3}"
    "@media (prefers-color-scheme:dark){.ink{fill:#f7fbff}.spark{fill:#d27ed0}}"
)
out = (
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}">\n'
    f"<style>{style}</style>\n"
    "<defs>\n"
    f'<clipPath id="h"><rect {clips[0][1]}/></clipPath>\n'
    f'<clipPath id="d"><rect {clips[1][1]}/></clipPath>\n'
    f'<path id="w" fill-rule="evenodd" d="{words1}"/>\n'
    "</defs>\n"
    '<g clip-path="url(#h)"><use href="#w" class="ink"/></g>\n'
    '<g transform="translate(1158 0) scale(-1 1)"><g clip-path="url(#h)"><use href="#w" class="ink"/></g></g>\n'
    f'<g transform="translate(-11.5 0)"><g clip-path="url(#d)"><path class="spark" fill-rule="evenodd" d="{dots}"/></g></g>\n'
    "</svg>\n"
)
with open(TARGET, "w", encoding="utf-8", newline="") as f:
    f.write(out)
print(TARGET, len(out.encode("utf-8")), "bytes; source", len(src.encode("utf-8")), "bytes")
