def edit(p, pairs):
    s = open(p, encoding='utf8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)
R = r'C:\dev\masaha\app-lane-a1'
E = R + r'\apps\api\src\modules\auth\email'
edit(E + r'\resetEmail.copy.ts', [
("""  action: string;
  validity: string;""", """  action: string;
  /** Under the button, before the link as text: a mail client may strip the button (AC-021). */
  copyLink: string;
  validity: string;"""),
("""  action: 'Set a new password',
""", """  action: 'Set a new password',
  copyLink: 'If the button doesn’t work, copy this link:',
"""),
("""  action: 'تعيين كلمة مرور جديدة',
""", """  action: 'تعيين كلمة مرور جديدة',
  copyLink: 'إن لم يعمل الزر، انسخ هذا الرابط:',
"""),
])
edit(E + r'\resetEmail.ts', [
("""<p style="clear:both;margin:0;padding-top:24px;font-size:14px;line-height:22px;color:${COLOR.muted};">${ar.validity}</p>""",
"""<p style="clear:both;margin:0;padding-top:24px;font-size:14px;line-height:22px;color:${COLOR.muted};">${ar.copyLink}</p>
${linkAsText}
<p style="margin:0;padding-top:16px;font-size:14px;line-height:22px;color:${COLOR.muted};">${ar.validity}</p>"""),
("""<p style="margin:0 0 8px;font-size:15px;line-height:22px;color:${COLOR.text};">${en.greeting} ${en.request} <a href="${href}" style="color:${COLOR.brand};">${en.action}</a>.</p>
<p style="margin:0;font-size:13px;line-height:20px;color:${COLOR.muted};">${en.validity}</p>""",
"""<p style="margin:0 0 8px;font-size:15px;line-height:22px;color:${COLOR.text};">${en.greeting} ${en.request} <a href="${href}" style="color:${COLOR.brand};">${en.action}</a>.</p>
<p style="margin:0;font-size:13px;line-height:20px;color:${COLOR.muted};">${en.copyLink}</p>
${linkAsText}
<p style="margin:0;padding-top:8px;font-size:13px;line-height:20px;color:${COLOR.muted};">${en.validity}</p>"""),
("""  const href = escapeHtml(link);
""", """  const href = escapeHtml(link);
  // The link as text, left to right whatever the paragraph around it, breaking anywhere: a long
  // link must not widen the card.
  const linkAsText = `<p dir="ltr" style="margin:4px 0 0;text-align:left;font-family:${LATIN_FONT};font-size:13px;line-height:20px;color:${COLOR.brand};word-break:break-all;overflow-wrap:anywhere;">${href}</p>`;
"""),
("""    `${ar.request} ${ar.instruction}`,
    link,
    ar.validity,
    '',
    `${en.greeting} ${en.request}`,
    `${en.action}: ${link}`,
    en.validity,""", """    `${ar.request} ${ar.instruction}`,
    ar.copyLink,
    link,
    ar.validity,
    '',
    `${en.greeting} ${en.request}`,
    en.copyLink,
    link,
    en.validity,"""),
])
