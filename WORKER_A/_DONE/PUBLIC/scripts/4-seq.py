import sys, io
path = sys.argv[1]
lines = io.open(path, encoding='utf-8').read().split('\n')
todo = [l for l in lines if l and not l.startswith('#')]
rest = [l for l in lines if not (l and not l.startswith('#'))]
fix = [l for l in todo if 'return the focus to the photo tile' in l]
assert len(fix) == 1
todo.remove(fix[0])
at = next(i for i, l in enumerate(todo) if 'prove the place map lets a phone scroll' in l)
todo.insert(at + 1, fix[0])
io.open(path, 'w', encoding='utf-8', newline='\n').write('\n'.join(todo + rest))
