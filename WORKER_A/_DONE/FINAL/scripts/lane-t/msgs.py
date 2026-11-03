msgs = {
'c43-msg.txt': """test(web): load the lazy shells before waiting

A route test's first wait for a lazy shell or page also paid its
module graph's first transform, which on a busy machine outlasted the
3 s findBy (findings 55 and 87): the site shell's first test took
3.8 s cold.

Each of the six route test files now loads the modules its tests open
in a beforeAll with a 60 s timeout, through warm(...) in src/test;
app/, which may not import a page's file, warms the routes '/' matches
through routeLoaders. No test's own wait or timeout is raised.
""",
'c44-msg.txt': """build(db): hold the test database's script inline

The init script was a bind mount relative to the folder that ran
db:up, so a second folder's db:up saw another configuration and
recreated the shared container bound to itself (finding 48).

The script is now an inline Compose config, so every folder gives the
same configuration and the container binds no folder. A container
made before this is recreated once by the next db:up; its volume and
data stay.
""",
'c45-msg.txt': """docs: settle the capability documents' size

Seven capability documents had outgrown the 1,200-word guide, and no
rule said what to do then (finding 98). The owner chose to revise the
guide (OD4 (b)): no word ceiling, decisions as they hold today, links
rather than restatements, and what a change need not read kept below
the code map.
""",
'c206-msg.txt': """docs: record finding 206

A production build of the integrated branch fails check:build on
seven showcase fixture strings that a library in the build also
writes (date-fns' month names, the currency code). Lane T does not
own the fixtures, so it records the defect.
""",
}
for n, m in msgs.items():
    open(n, 'w', encoding='utf8', newline='\n').write(m)
