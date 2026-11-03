p=r'C:\dev\masaha\app-lane-w3\docs\features\desk.md'
s=open(p,encoding='utf8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,a
    s=s.replace(a,b)
rep("A lost answer says a retry is safe; a refusal says nothing was recorded, before its reason.","A lost answer says a retry is safe; a refusal says nothing was recorded, before its reason; too many attempts (429) in a money dialog — the visit's check-in and check-out, «تحصيل», «استلام دفعة», the sheet — say after their wait «لم يُسجَّل شيء. إعادة المحاولة بعد ذلك لن تسجّله مرتين.». Every phone field shows «+970 59 000 0000»; «تسجيل زيارة» and «حضور» carry their sign-in icon, «خروج» its sign-out icon; the search is the large field.")
rep("the file a typed phone adds to.","the file a typed phone adds to; a 429 in a money dialog said to have recorded nothing, the phone fields' example, the actions' icons, the large search.")
open(p,'w',encoding='utf8',newline='').write(s)
