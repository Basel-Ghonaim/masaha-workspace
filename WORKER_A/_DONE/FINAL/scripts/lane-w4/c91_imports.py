import os, re
root = r'C:\dev\masaha\app-lane-w4\apps\web\src\features\users'
moved_dirs = ['hooks/account','hooks/password-change','hooks/forced-change','hooks/sign-out','components/account-menu','components/forced-change','components/sign-out']
reps = [
  ("'../../../test/", "'../../../../test/"),
  ("'./useSignOutAction'", "'../sign-out/useSignOutAction'"),
  ("'../repository/", "'../../repository/"),
  ("'./useChangePassword'", "'../password-change/useChangePassword'"),
  ("'../types/", "'../../types/"),
  ("'../hooks/useAccount'", "'../../hooks/account/useAccount'"),
  ("'./SignOutFailure'", None),
  ("'../hooks/useForcedPasswordChangeForm'", "'../../hooks/forced-change/useForcedPasswordChangeForm'"),
  ("'../hooks/useSignOutAction'", "'../../hooks/sign-out/useSignOutAction'"),
]
for d in moved_dirs:
    for f in os.listdir(os.path.join(root, d)):
        p = os.path.join(root, d, f)
        s = open(p, encoding='utf8', newline='').read(); o = s
        for a, b in reps:
            if a == "'./SignOutFailure'":
                if d == 'components/account-menu':
                    s = s.replace(a, "'../sign-out/SignOutFailure'")
                continue
            s = s.replace(a, b)
        if s != o:
            open(p, 'w', encoding='utf8', newline='').write(s); print('fixed', d, f)
# index.ts
p = os.path.join(root, 'index.ts'); s = open(p, encoding='utf8', newline='').read()
for a,b in [("'./components/AccountMenu'","'./components/account-menu/AccountMenu'"),("'./components/AccountMenuSection'","'./components/account-menu/AccountMenuSection'"),("'./components/DrawerAccountMenu'","'./components/account-menu/DrawerAccountMenu'"),("'./components/CompactAccountMenu'","'./components/account-menu/CompactAccountMenu'"),("'./components/ForcedPasswordChangeForm'","'./components/forced-change/ForcedPasswordChangeForm'"),("'./components/SignOutButton'","'./components/sign-out/SignOutButton'")]:
    assert a in s, a; s = s.replace(a,b)
open(p,'w',encoding='utf8',newline='').write(s)
