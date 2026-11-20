"""C10 (plan §7.7, OD5 (a)): berry becomes the prototype's default. Every edit asserts its anchor once."""
import os

D = r"C:\dev\masaha\app-design-lane-c\docs\design"


def edit(rel, pairs):
    path = os.path.join(D, rel)
    with open(path, encoding="utf-8", newline="") as f:
        s = f.read()
    for old, new, count in pairs:
        assert s.count(old) == count, (rel, old[:70], s.count(old))
        s = s.replace(old, new)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("edited", rel)


# 1. i18n.js: no ?identity= is slate-berry; sea is the bundle's own; coral unchanged; a link carries
#    identity only when it is not the default; the tab's icon follows as now.
edit(r"prototype\masaha\i18n.js", [
    (
        """  // Identity trial (ink + spark, 2026-11-11): ?identity= picks a candidate in masaha/identity-ink-spark.css.
  // None, or an unknown one, is today's identity.
  const identity = ['slate-coral', 'slate-berry'].includes(p.get('identity')) ? p.get('identity') : null;
  if (identity) root.dataset.identity = identity;
""",
        """  // The identity (2026-11-12): ink + berry (slate-berry) is the default, as production takes it (ADR 0019).
  // ?identity=sea gives Sea, the first identity (the bundle's own tokens: no data-identity); ?identity=slate-coral
  // the trial's other candidate (masaha/identity-ink-spark.css). None, or an unknown one, is berry. A link
  // carries the identity only when it is not the default.
  const DEFAULT_IDENTITY = 'slate-berry';
  const chosen = ['sea', 'slate-coral', 'slate-berry'].includes(p.get('identity')) ? p.get('identity') : DEFAULT_IDENTITY;
  const identity = chosen === 'sea' ? null : chosen;
  if (identity) root.dataset.identity = identity;
""",
        1,
    ),
    (
        "    if (identity && !q.has('identity')) q.set('identity', identity);\n",
        "    if (chosen !== DEFAULT_IDENTITY && !q.has('identity')) q.set('identity', chosen);\n",
        1,
    ),
])

# 2. identity-ink-spark.css: its header comment.
edit(r"prototype\masaha\identity-ink-spark.css", [
    (
        """/* Identity trial — "ink + spark" (2026-11-11). The owner adopted slate-berry (2026-11-11); slate-coral stays to
   compare. Until foundation.md takes it, foundation §4–§5 (Sea) still rule and stay the default.
   Loaded last on every app page. It does nothing unless <html data-identity="…"> is set, which i18n.js does
   from ?identity=slate-coral | slate-berry (carried on every link). Without it the page is Sea.
""",
        """/* Identity — "ink + spark" (trial 2026-11-11). The owner adopted slate-berry (2026-11-11) and production now
   takes it (foundation §4–§5 and §16, ADR 0019), so it is the prototype's default; slate-coral stays to
   compare, and Sea, the first identity, is ?identity=sea.
   Loaded last on every app page. It does nothing unless <html data-identity="…"> is set, which i18n.js does:
   slate-berry without ?identity= (or with an unknown one), slate-coral from ?identity=slate-coral, carried on
   every link. ?identity=sea sets none, and the page is the bundle's own Sea.
""",
        1,
    ),
])

# 3. Reset email.html: its inline hexes to production's (plan §7.6).
edit(r"prototype\Reset email.html", [
    ("#f4fcfe", "#f7fbff", 3),
    ("#dbe6e9", "#dde5ed", 2),
    ("#02787d", "#1a1f25", 7),
    ("#182022", "#1a1f25", 2),
    ("#5c6567", "#5e646a", 5),
])

# 4. CHANGES.md: a section «Berry, the default (2026-11-12)», after the trial's.
edit("CHANGES.md", [
    (
        "| **The covers in dark** |",
        "| **The covers in dark** |",
        1,
    ),
])
path = os.path.join(D, "CHANGES.md")
with open(path, encoding="utf-8", newline="") as f:
    s = f.read()
assert s.endswith("| the same stylesheet |\n"), repr(s[-60:])
s += """
## Berry, the default (2026-11-12)

Production takes ink + berry ([ADR 0019](../architecture/decisions/0019-ink-and-spark-brand.md); [foundation](../frontend/design-system/foundation.md) §4, §5 and §16), so the prototype draws it by default, and the design source shows what the site shows. *Sea*, the first identity, and `slate-coral`, the trial's other candidate, stay behind `?identity=` to compare.

| What | What changed | Where |
|---|---|---|
| **The default** | No `?identity=`, or an unknown one, is `slate-berry`; `?identity=sea` is *Sea*, the bundle's own tokens, with no `data-identity`; `?identity=slate-coral` is unchanged. A link carries `identity` only when it is not the default. The tab's icon follows the identity as before: berry's small mark by default, *Sea*'s «م» tile under `?identity=sea` | `masaha/i18n.js` |
| **The stylesheet's header** | Production takes berry (ADR 0019); without `?identity=` the page is berry; *Sea* is `?identity=sea` | `masaha/identity-ink-spark.css` |
| **The reset email** | Production's colours, ink + berry's neutrals: the page `#f7fbff`, the card `#ffffff`, the borders `#dde5ed`, the brand line, the button and the links in the ink `#1a1f25`, the text `#1a1f25`, the muted lines `#5e646a`; no spark | `Reset email.html` |
| **The documents** | The `?identity=` row; the `Wordmark.html` line: option A superseded by the logo | `INDEX.md`, `SCREENS.md` |
"""
with open(path, "w", encoding="utf-8", newline="") as f:
    f.write(s)
print("appended CHANGES.md")

# 5. INDEX.md: the ?identity= row.
edit("INDEX.md", [
    (
        "| `?identity=slate-coral` · `slate-berry` | every app page, carried on its links | a **trial** identity (`slate-berry` adopted by the owner, 2026-11-11; `slate-coral` kept to compare): ink actions, a spark for what matters now and the candidate's logo ([CHANGES.md](CHANGES.md#identity-trial--ink--spark-2026-11-11)); without it, *Sea* |\n",
        "| `?identity=sea` · `slate-coral` | every app page, carried on its links | without it, or with an unknown one, **ink + berry** (`slate-berry`), production's identity ([CHANGES.md](CHANGES.md#berry-the-default-2026-11-12)); `sea`: *Sea*, the first identity; `slate-coral`: the trial's other candidate, kept to compare ([CHANGES.md](CHANGES.md#identity-trial--ink--spark-2026-11-11)). `?identity=slate-berry` is the same as none |\n",
        1,
    ),
])

# 6. SCREENS.md: Wordmark.html's option A, superseded by the logo.
edit("SCREENS.md", [
    (
        "- `Wordmark.html`: the three wordmark options; **option A (plain word, «م» favicon) was chosen**.\n",
        "- `Wordmark.html`: the three wordmark options; option A (plain word, «م» favicon) was chosen, then **superseded by the logo** ([foundation §16](../frontend/design-system/foundation.md#16-the-logo); its files in `prototype/masaha/logo/`).\n",
        1,
    ),
])
