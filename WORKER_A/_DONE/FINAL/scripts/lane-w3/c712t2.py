p=r'C:\dev\masaha\app-lane-w3\apps\web\src\pages\dashboard\space\desk\DeskPage.component.test.tsx'
s=open(p,encoding='utf8').read()
a="""    expect(dialog).toHaveAccessibleDescription(plain('Today 2:05 · paid ₪60') === 'Today 2:05 · paid ₪60' ? /Today .*2:05.* · paid .*₪60/ : '');"""
assert s.count(a)==1
s=s.replace(a,"""    expect(dialog).toHaveAccessibleDescription(/^Today \W?2:05\W? · paid \W?₪60\W?$/u);""")
open(p,'w',encoding='utf8',newline='').write(s)
