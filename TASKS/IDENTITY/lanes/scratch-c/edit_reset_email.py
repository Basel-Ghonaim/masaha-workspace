"""C9: resetEmail.ts's COLOR in ink + berry's neutrals (plan §7.6)."""
P = r"C:\dev\masaha\app-design-lane-c\apps\api\src\modules\auth\email\resetEmail.ts"
s = open(P, encoding="utf-8", newline="").read()


def sub(old, new, count=1):
    global s
    assert s.count(old) == count, (old[:70], s.count(old))
    s = s.replace(old, new)


sub(
    """// The design's colours (docs/design: Reset email.html), written inline: an email client reads no
// stylesheet and no custom property, so the web's tokens cannot reach it (findings).
const COLOR = {
  page: '#f4fcfe',
  card: '#ffffff',
  border: '#dbe6e9',
  brand: '#02787d',
  onBrand: '#ffffff',
  text: '#182022',
  muted: '#5c6567',
} as const;
""",
    """// The identity's colours, ink + berry's neutrals (ADR 0019), as the design draws them (docs/design:
// Reset email.html), written inline: an email client reads no stylesheet and no custom property, so
// the web's tokens cannot reach it, and a change of the brand or the neutrals is carried here by hand
// (finding 19). Each pair is one the web verifies: the primary's label on the primary, the text and
// the muted text on the card and the background. No spark: its dots belong to the logo, not to text.
const COLOR = {
  page: '#f7fbff', // neutral-50, the background
  card: '#ffffff',
  border: '#dde5ed', // neutral-200
  ink: '#1a1f25', // neutral-900, the primary: the brand line, the button and the links
  onInk: '#ffffff', // the primary's label
  text: '#1a1f25', // neutral-900, the foreground: the ink's value, another meaning
  muted: '#5e646a', // neutral-600, the muted text
} as const;
""",
)
# The link as text, the brand line, the button's cell: the ink.
sub("color:${COLOR.brand};word-break:break-all;", "color:${COLOR.ink};word-break:break-all;")
sub("font-weight:700;color:${COLOR.brand};\">${ar.brand}", "font-weight:700;color:${COLOR.ink};\">${ar.brand}")
sub("border-radius:8px;background:${COLOR.brand};", "border-radius:8px;background:${COLOR.ink};")
sub("color:${COLOR.onBrand};text-decoration:none;", "color:${COLOR.onInk};text-decoration:none;")
# The English inline link: ink, underlined (ink beside ink text is told apart by its underline).
sub(
    '<a href="${href}" style="color:${COLOR.brand};">${en.action}</a>',
    '<a href="${href}" style="color:${COLOR.ink};text-decoration:underline;">${en.action}</a>',
)
assert "COLOR.brand" not in s and "onBrand" not in s
open(P, "w", encoding="utf-8", newline="").write(s)
print("ok")
