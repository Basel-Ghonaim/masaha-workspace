def edit(p, pairs):
    s=open(p,encoding='utf8').read()
    for a,b,n in pairs:
        assert s.count(a)==n,(p,a,s.count(a))
        s=s.replace(a,b)
    open(p,'w',encoding='utf8',newline='').write(s)
edit('pages/dashboard/space/desk/DeskPage.tsx',[
("  EllipsisIcon,\n","  EllipsisIcon,\n  LogInIcon,\n",1),
("""              <Button size="sm" onClick={openVisit}>
                {words.actions.checkIn}""","""              <Button size="sm" onClick={openVisit}>
                <LogInIcon aria-hidden />
                {words.actions.checkIn}""",1),
("""        <Button size="lg" className="w-full" onClick={openVisit}>
          {words.actions.checkIn}""","""        <Button size="lg" className="w-full" onClick={openVisit}>
          <LogInIcon aria-hidden />
          {words.actions.checkIn}""",1),
])
edit('features/desk/components/search/DeskSearch.tsx',[
("  Input,\n  SearchIcon,\n","  Input,\n  LogInIcon,\n  SearchIcon,\n  SearchXIcon,\n",1),
("""          {search.checkIn.label}
        </Button>""","""          <LogInIcon aria-hidden />
          {search.checkIn.label}
        </Button>""",1),
("""          <EmptyState title={search.none.title} description={search.none.text}>""","""          <EmptyState
            icon={<SearchXIcon />}
            title={search.none.title}
            description={search.none.text}
          >""",1),
("""        type="search"
        aria-label={search.input.label}""","""        type="search"
        size="lg"
        aria-label={search.input.label}""",1),
])
edit('features/desk/components/card/CustomerCard.tsx',[
("  CardTitle,\n} from '@shared/design-system';","  CardTitle,\n  LogInIcon,\n} from '@shared/design-system';",1),
("""        >
          {checkIn.tap.label}
        </Button>""","""        >
          <LogInIcon aria-hidden />
          {checkIn.tap.label}
        </Button>""",1),
])
edit('features/desk/components/check-out/CheckOutAction.tsx',[
("import { Button } from '@shared/design-system';","import { Button, LogOutIcon } from '@shared/design-system';",1),
("""      >
        {words.open}
      </Button>""","""      >
        <LogOutIcon aria-hidden />
        {words.open}
      </Button>""",1),
("""    >
      {checkOut.label}
    </Button>""","""    >
      <LogOutIcon aria-hidden />
      {checkOut.label}
    </Button>""",1),
])
edit('features/occupancy/components/PresentList.tsx',[
("  EmptyState,\n  WifiOffIcon,\n","  EmptyState,\n  UsersIcon,\n  WifiOffIcon,\n",1),
("empty={<EmptyState title={list.empty.title} description={list.empty.text} />}","empty={\n            <EmptyState\n              icon={<UsersIcon />}\n              title={list.empty.title}\n              description={list.empty.text}\n            />\n          }",1),
])
edit('features/occupancy/components/LiveStatusControl.tsx',[
("  PopoverTrigger,\n","  PopoverTrigger,\n  ChevronDownIcon,\n",1),
("""            {wide ? trigger.label : trigger.word}
          </Button>""","""            {wide ? trigger.label : trigger.word}
            {wide && <ChevronDownIcon aria-hidden />}
          </Button>""",1),
])
