root = 'C:/dev/masaha/app-lane-t/'
def rep(rel, old, new):
    p = root + rel; s = open(p, encoding='utf8').read()
    assert s.count(old) == 1, (rel, old[:60])
    open(p, 'w', encoding='utf8', newline='').write(s.replace(old, new))
D = 'docs/architecture/documentation.md'
rep(D, "· **Last Updated:** 2026-10-10 ·", "· **Last Updated:** 2026-10-29 ·")
rep(D, "- **About 1,200 words at most,** so it can be read whole before a change.",
 "- **Short where it is read before a change** (OD4, 2026-10-29, #PRNUM): a capability document holds the decisions as they hold today and links rather than restates; it has no word ceiling, but a part that a change to the capability need not read (its *History*, a superseded decision's record) moves below its *Code map*, so the part read before a change stays short.")
p = root + 'docs/architecture/findings/98-the-capability-documents-outgrow-their-size-guide.md'
import glob
p = glob.glob(root + 'docs/architecture/findings/98-*.md')[0]
s = open(p, encoding='utf8').read()
old = '**Status:** Open · **Date:** 2026-10-20'
assert s.count(old) == 1
s = s.replace(old, '**Status:** Resolved · **Date:** 2026-10-20', 1)
s = s.rstrip('\n') + "\n\n**Resolution (2026-10-29, #PRNUM):** the owner chose to revise the guide (OD4 (b)): [documentation §5](../documentation.md#5-capability-documents) drops the word ceiling; a capability document holds its decisions as they hold today, links rather than restates, and keeps what a change need not read (its *History*, a superseded decision's record) below its *Code map*.\n"
open(p, 'w', encoding='utf8', newline='').write(s)
