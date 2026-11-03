import io, sys
p = sys.argv[1]
lines = io.open(p, encoding='utf8').read().split('\n')
picks = [l for l in lines if l.startswith('pick ')]
opt = next(l for l in picks if 'pre-bundle the calendar' in l)
lines.remove(opt)
i = next(k for k, l in enumerate(lines) if l.startswith('pick ') and 'start a range on each click' in l)
lines.insert(i + 1, opt)
io.open(p, 'w', encoding='utf8', newline='').write('\n'.join(lines))
