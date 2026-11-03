p=r'C:\dev\masaha\app-lane-w3\docs\features\desk.md'
s=open(p,encoding='utf8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,a
    s=s.replace(a,b)
rep("- **A subscriber's «خروج»** is one tap with no key, in the present list and in the search's first group: the toast says how long they stayed and what their subscription still owes, from the answer.","- **A subscriber's «خروج»** is one tap with no key, in the present list and in the search's first group: for a fixed-price subscription the toast says how long they stayed and what their subscription still owes, from the answer; for a usage-based one a dialog opens from the answer (no quote exists for an open check-in, and the web never prices: DI10) — «خرج {name}», «اليوم {h}:{mm} · المدفوع {paid}», «يبقى على اشتراك {subscription}: {balance}» while it owes, the money block filled with the balance, «استلام {amount}», which records it on the subscription with its own key, and `ghost` «لاحقًا».")
rep("the actions' icons, the large search.","the actions' icons, the large search; a usage-based subscriber's due said after the check-out.")
open(p,'w',encoding='utf8',newline='').write(s)
