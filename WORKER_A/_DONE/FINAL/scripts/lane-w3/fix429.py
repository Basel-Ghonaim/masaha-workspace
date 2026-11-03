p=r'C:\dev\masaha\app-lane-w3\apps\web\src\features\desk\hooks\collect\useCollectDialog.component.test.tsx'
s=open(p,encoding='utf8').read()
a=r"""    expect(await screen.findByRole('alert')).toHaveTextContent(
      /Nothing was recorded\. Trying again after that won’t record it twice\.$/,
    );"""
assert s.count(a)==1
s=s.replace(a,r"""    // Too many attempts is a warning, not an alert; in a money dialog it says nothing landed.
    expect(
      await screen.findByText(/Nothing was recorded\. Trying again after that won’t record it twice\.$/),
    ).toBeVisible();""")
open(p,'w',encoding='utf8',newline='').write(s)
