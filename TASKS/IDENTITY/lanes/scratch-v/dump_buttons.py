import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
d = json.load(open('discover.json', encoding='utf-8'))
for k in sys.argv[1:]:
    v = d[k]
    print('==', k, 'slots:', ' '.join(f'{a}:{b}' for a, b in v['slots'].items() if not a.startswith('sidebar')))
    for b in v['buttons'][:60]:
        if b['slot'] and b['slot'].startswith('sidebar'):
            continue
        print('   ', b['tag'], b['slot'], b['role'], repr(b['text'][:40]), b['label'], b['state'], 'ON' if b['on'] else '', b['current'] or '')
