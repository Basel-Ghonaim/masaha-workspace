# Names each race's table at its call to waitingOnLock / whileHeld, and gives each race test
# RACE_TIMEOUT_MS. The table per test comes from race-map.jsonl (what each race was seen waiting on).
import json, re, sys, collections, os
sys.stdout.reconfigure(encoding='utf8')
ROOT = r'C:\dev\masaha\app-lane-a1\apps\api'
HERE = os.path.dirname(os.path.abspath(__file__))
seen = collections.defaultdict(list)  # file -> [(title, rel)]
for line in open(os.path.join(HERE, 'race-map.jsonl'), encoding='utf8'):
    r = json.loads(line)
    path, title = r['test'].split(' :: ', 1)
    rels = sorted({s['rel'] for s in r['seen'] if s['rel']})
    f = path.replace('\\', '/').split('apps/api/')[-1]
    seen[f].append((title, rels[0] if rels else None, r['on']))

def scan_spans(s):
    """Spans [start, end) of every it( / it.each(...)( call, by bracket counting."""
    spans = []
    for m in re.finditer(r'(?m)^\s*it(\.each)?\(', s):
        start = m.start()
        i = m.end() - 1  # at '('
        if m.group(1):
            i = match(s, i) + 1  # past it.each(...)
            # skip whitespace and the call's '('
            while s[i] != '(':
                i += 1
        end = match(s, i)
        spans.append((start, i, end))
    return spans

def match(s, i):
    """Index of the bracket closing s[i], skipping strings, templates and comments."""
    depth = 0
    n = len(s)
    stack = []
    while i < n:
        c = s[i]
        if c in '([{':
            depth += 1
        elif c in ')]}':
            depth -= 1
            if depth == 0:
                return i
        elif c in '\'"':
            j = i + 1
            while s[j] != c:
                j += 2 if s[j] == '\\' else 1
            i = j
        elif c == '`':
            j = i + 1
            while s[j] != '`':
                if s[j] == '\\':
                    j += 2
                    continue
                if s.startswith('${', j):
                    j = match(s, j + 1) + 1
                    continue
                j += 1
            i = j
        elif s.startswith('//', i):
            i = s.index('\n', i)
            continue
        elif s.startswith('/*', i):
            i = s.index('*/', i) + 1
        i += 1
    raise ValueError('unmatched')

files = sys.argv[1:]
report = []
for f in files:
    p = os.path.join(ROOT, f)
    s = open(p, encoding='utf8').read()
    titles = seen.get(f, [])
    default = collections.Counter(t[1] for t in titles if t[1]).most_common(1)
    default = default[0][0] if default else None
    spans = scan_spans(s)
    edits = []  # (pos, old_len, new_text)
    calls = [m for m in re.finditer(r'\b(waitingOnLock|whileHeld)\(', s)]
    race_spans = set()
    for m in calls:
        enclosing = [sp for sp in spans if sp[0] < m.start() < sp[2]]
        sp = max(enclosing, key=lambda x: x[0]) if enclosing else None
        rel = None
        if sp:
            head = s[sp[1]:sp[1] + 400]
            for title, r, _on in titles:
                if title.split(' > ')[-1][:60] in head:
                    rel = r
            race_spans.add(sp)
        rel = rel or default
        report.append(f'{f}:{s.count(chr(10), 0, m.start()) + 1} {m.group(1)} -> {rel}' + ('' if sp else '  [outside a test]'))
        open_paren = m.end() - 1
        close = match(s, open_paren)
        args = s[open_paren + 1:close]
        if m.group(1) == 'whileHeld':
            edits.append((open_paren + 1, 0, f"'{rel}', "))
        else:
            if args.strip() == '':
                edits.append((open_paren + 1, 0, f"{{ on: '{rel}' }}"))
            elif 'on:' in args:
                pass
            else:
                inner = args.rstrip()
                assert inner.endswith('}'), (f, args)
                k = open_paren + 1 + len(inner) - 1
                edits.append((k, 0, f", on: '{rel}' "))
    # the race tests' timeout
    for start, call_open, end in race_spans:
        body = s[call_open:end]
        tail = re.search(r',\s*([0-9_]+|RACE_TIMEOUT_MS)\s*,?\s*$', body)
        if tail:
            num_start = call_open + tail.start(1)
            edits.append((num_start, len(tail.group(1)), 'RACE_TIMEOUT_MS'))
        else:
            edits.append((end, 0, ', RACE_TIMEOUT_MS'))
    for pos, length, text in sorted(edits, key=lambda e: e[0], reverse=True):
        s = s[:pos] + text + s[pos + length:]
    # the import
    m = re.search(r"import \{([^}]*)\} from '([./]+)test/locks\.ts';", s)
    if m and 'RACE_TIMEOUT_MS' not in m.group(1) and race_spans:
        names = [n.strip() for n in m.group(1).split(',') if n.strip()] + ['RACE_TIMEOUT_MS']
        s = s[:m.start()] + "import { " + ', '.join(names) + " } from '" + m.group(2) + "test/locks.ts';" + s[m.end():]
    open(p, 'w', encoding='utf8', newline='').write(s)
print('\n'.join(report))
