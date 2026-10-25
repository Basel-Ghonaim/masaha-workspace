from pathlib import Path
APP = Path('C:/dev/masaha/app')
def edit(rel, old, new):
    p = APP / rel
    t = p.read_text(encoding='utf-8')
    assert t.count(old) == 1, old
    p.write_bytes(t.replace(old, new).encode('utf-8'))
edit('docs/features/desk.md', " the server's idle sign-out of a reception session is planned (the desk's screen item, its spec C).", " the server's idle sign-out of a reception session is not built yet.")
edit('docs/features/visits.md', "which reads the open visits for *present*. No web screen reads it yet.", "which reads the open visits for *present*; the desk's screen shows them through its state now (2026-10-24, #PRNUM).")
print('ok')
