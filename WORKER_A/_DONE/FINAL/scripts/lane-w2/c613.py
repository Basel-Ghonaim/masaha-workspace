import os
os.chdir(r'C:\dev\masaha\app-lane-w2\apps\web\src')
def edit(p,pairs):
    s=open(p,encoding='utf8').read()
    for a,b in pairs:
        assert s.count(a)==1,(p,a[:70]); s=s.replace(a,b)
    open(p,'w',encoding='utf8',newline='').write(s)

# 1. headers visually hidden
edit('features/space-links/components/owners-list/OwnersList.tsx',[
("""          id: 'actions',
          header: headers.actions,""","""          id: 'actions',
          header: () => <span className="sr-only">{headers.actions}</span>,"""),
("""        empty={<ListState list={list} />}""","""        empty={
          <ListState
            list={list}
            emptyAction={
              // The page's add sheet opens on `?sheet=add` (D6.11).
              <Button asChild>
                <Link to="?sheet=add">{list.addOwner}</Link>
              </Button>
            }
          />
        }"""),
])
s=open('features/space-links/components/owners-list/OwnersList.tsx',encoding='utf8').read()
print(s[:900])
