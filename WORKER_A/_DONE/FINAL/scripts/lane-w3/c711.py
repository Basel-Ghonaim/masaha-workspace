import re
def edit(p, pairs, count=1):
    s=open(p,encoding='utf8').read()
    for a,b in pairs:
        assert s.count(a)==count,(p,a,s.count(a))
        s=s.replace(a,b)
    open(p,'w',encoding='utf8',newline='').write(s)
# 1. deskFailure
edit('features/desk/services/deskRefusal.ts',[
(""" * before its reason; too many attempts keep their countdown. `refused` is the refusal as
 * `useRefusalView` read it.""",""" * before its reason; too many attempts keep their countdown, and — in a money dialog, which passes
 * `limited` — say nothing was recorded and a retry will not record it twice (G13.13). `refused` is
 * the refusal as `useRefusalView` read it."""),
("""  lines: { title: string; lost: string; nothing: string; retryLabel: string; retry: () => void },""","""  lines: {
    title: string;
    lost: string;
    nothing: string;
    retryLabel: string;
    retry: () => void;
    limited?: string;
  },"""),
("""  return refused;
}""","""  if (refused?.kind === 'rateLimit' && lines.limited !== undefined) {
    return { ...refused, message: `${refused.message} ${lines.limited}` };
  }
  return refused;
}"""),
])
for p in ['features/desk/hooks/check-in/useVisitDialog.ts','features/desk/hooks/check-out/useCheckOutDialog.ts','features/desk/hooks/collect/useCollectDialog.ts','features/desk/hooks/pay/usePayDialog.ts','features/desk/hooks/sheet/useSubscriptionSheet.ts']:
    s=open(p,encoding='utf8').read()
    m=re.search(r"deskFailure\([^{]*\{\n(\s*)title:", s)
    assert m, p
    ind=m.group(1)
    i=m.end()-len('title:')
    s=s[:i]+"limited: words.failure.limited,\n"+ind+s[i:] if "const words = copy.desk;" in s or "words = copy.desk\n" in s else s[:i]+"limited: copy.desk.failure.limited,\n"+ind+s[i:]
    open(p,'w',encoding='utf8',newline='').write(s)
edit('shared/copy/arabic/desk.ts',[("""    nothing: 'لم يُسجَّل شيء.',""","""    nothing: 'لم يُسجَّل شيء.',
    limited: 'لم يُسجَّل شيء. إعادة المحاولة بعد ذلك لن تسجّله مرتين.',""")])
edit('shared/copy/english/desk.ts',[("""    nothing: 'Nothing was recorded.',""","""    nothing: 'Nothing was recorded.',
    /** Too many attempts, in a money dialog: nothing landed, and the key keeps a retry single. */
    limited: 'Nothing was recorded. Trying again after that won’t record it twice.',""")])
# 2. phone placeholders
edit('shared/copy/arabic/desk.ts',[("""    newCustomer: 'زبون جديد بهذا الرقم',""","""    newCustomer: 'زبون جديد بهذا الرقم',
    phonePlaceholder: '+970 59 000 0000',""")])
edit('shared/copy/english/desk.ts',[("""    newCustomer: 'A new customer with this number',""","""    newCustomer: 'A new customer with this number',
    /** Every phone field's example (G13.14). */
    phonePlaceholder: '+970 59 000 0000',""")])
