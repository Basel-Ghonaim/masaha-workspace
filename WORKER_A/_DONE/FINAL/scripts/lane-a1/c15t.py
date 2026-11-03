p = r'C:\dev\masaha\app-lane-a1\apps\api\src\modules\auth\email\resetEmail.unit.test.ts'
s = open(p, encoding='utf8').read()
old = """  it('escapes the link it is given', () => {"""
new = """  it('the reset email holds the link as text in both parts and languages', () => {
    const escaped = (text: string) => text.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&');
    for (const words of [ARABIC.copyLink, ENGLISH.copyLink]) {
      // Under the button, the words, then the link as text a reader can copy, left to right.
      expect(email.html).toMatch(
        new RegExp(`${escaped(words)}</p>\\\\s*<p dir="ltr"[^>]*>${escaped(link)}</p>`),
      );
      expect(email.text).toContain(`${words}\\n${link}`);
    }
  });

""" + old
assert s.count(old) == 1
s = s.replace(old, new)
open(p, 'w', encoding='utf8', newline='').write(s)
