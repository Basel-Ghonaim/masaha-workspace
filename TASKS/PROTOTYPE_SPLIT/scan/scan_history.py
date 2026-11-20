# Scan every version of every file ever under docs/design, plus the commit messages that touch it.
# Read-only on the repository. Writes its findings to this folder (scan/out/*.txt).
#   python -I scan_history.py C:/dev/masaha/app
import re, subprocess, sys, collections, os

REPO = sys.argv[1]
PREFIX = sys.argv[2] if len(sys.argv) > 2 else 'docs/design'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), sys.argv[3] if len(sys.argv) > 3 else 'out')
os.makedirs(OUT, exist_ok=True)

def git(*args, data=None):
    return subprocess.run(['git', '-C', REPO, *args], input=data, capture_output=True, check=True).stdout

commits = git('rev-list', 'HEAD', '--', PREFIX).decode().split()
order = {c: i for i, c in enumerate(reversed(commits))}  # 0 = oldest

blobs = {}  # blob -> {'paths': set, 'first': commit}
all_paths = set()
for c in reversed(commits):
    for rec in git('ls-tree', '-r', '-z', c, '--', PREFIX).split(b'\0'):
        if not rec:
            continue
        meta, path = rec.split(b'\t', 1)
        mode, typ, sha = meta.split()
        if typ != b'blob':
            continue
        p = path.decode('utf-8', 'replace')
        all_paths.add(p)
        b = blobs.setdefault(sha.decode(), {'paths': set(), 'first': c})
        b['paths'].add(p)

tip_paths = set(git('ls-tree', '-r', '--name-only', '-z', 'HEAD', '--', PREFIX).decode().split('\0')) - {''}

# read every blob
proc = subprocess.Popen(['git', '-C', REPO, 'cat-file', '--batch'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
contents = {}
for sha in blobs:
    proc.stdin.write((sha + '\n').encode()); proc.stdin.flush()
    header = proc.stdout.readline().split()
    size = int(header[2])
    data = proc.stdout.read(size); proc.stdout.read(1)
    contents[sha] = data
proc.stdin.close(); proc.wait()

def is_binary(d):
    return b'\0' in d[:8000]

PATTERNS = {
    'secret': [
        r'(?i)\b(api[_-]?key|secret|token|passw(?:or)?d|pwd|bearer|authorization|client[_-]?secret)\b\s*["\']?\s*[:=]\s*["\']?([^\s"\',;)}]{4,})',
        r'(?i)\b(postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis|amqp)://[^\s"\'<>]+',
        r'-----BEGIN [A-Z ]*PRIVATE KEY-----',
        r'\bAKIA[0-9A-Z]{16}\b',
        r'\bgh[pousr]_[A-Za-z0-9]{30,}\b',
        r'\bgithub_pat_[A-Za-z0-9_]{20,}',
        r'\bsk-[A-Za-z0-9_-]{20,}',
        r'\bxox[baprs]-[A-Za-z0-9-]{10,}',
        r'\bAIza[0-9A-Za-z_-]{35}\b',
        r'\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}',
        r'\b(DATABASE_URL|DIRECT_URL|JWT_[A-Z_]*SECRET|SEED_ADMIN_[A-Z_]+|GOOGLE_CLIENT_[A-Z_]+|RESEND_[A-Z_]+|SMTP_[A-Z_]+|VERCEL_[A-Z_]+|NEON_[A-Z_]+)\b',
        r'\b[0-9]{6,}-[a-z0-9]{32}\.apps\.googleusercontent\.com\b',
    ],
    'email': [r'[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}'],
    'phone': [
        r'(?<![\w.])(?:\+|00)?(?:970|972)[\s-]?\d[\d\s-]{6,12}\d',
        r'(?<![\w.])0(?:5[0-9]|8)[\s-]?\d[\d\s-]{5,9}\d(?![\w.])',
    ],
    'identity': [r'(?i)university|جامعة|supervisor|مشرف|defen[cs]e|مناقشة|graduat|تخرج|thesis|college|كلية|course|مساق|instructor|دكتور'],
    'owner-name': [r'(?i)basel|ghon[ae]im|ghoneim|باسل|غنيم'],
}
COMPILED = {k: [re.compile(p) for p in v] for k, v in PATTERNS.items()}

hits = collections.defaultdict(list)  # kind -> (first_commit, path, line, text, match)
binaries = collections.Counter()
for sha, data in contents.items():
    info = blobs[sha]
    path = sorted(info['paths'])[0]
    if is_binary(data):
        binaries[os.path.splitext(path)[1].lower()] += 1
        continue
    text = data.decode('utf-8', 'replace')
    # minified vendor bundles: scan, but cap context
    for n, line in enumerate(text.splitlines(), 1):
        for kind, regs in COMPILED.items():
            for r in regs:
                for m in r.finditer(line):
                    s = max(0, m.start() - 60); e = min(len(line), m.end() + 60)
                    hits[kind].append((info['first'][:8], path, n, line[s:e].strip(), m.group(0)))

def mask(v):
    return v[:4] + '…(' + str(len(v)) + ')' if len(v) > 6 else v

with open(os.path.join(OUT, 'blobs.txt'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(f'commits touching docs/design: {len(commits)}\n')
    f.write(f'distinct blobs: {len(contents)}, binary: {sum(binaries.values())} {dict(binaries)}\n')
    f.write(f'distinct paths ever: {len(all_paths)}, at tip: {len(tip_paths)}\n')
    f.write('paths in history but not at tip:\n')
    for p in sorted(all_paths - tip_paths):
        f.write('  ' + p + '\n')

for kind, rows in hits.items():
    with open(os.path.join(OUT, f'{kind}.txt'), 'w', encoding='utf-8', newline='\n') as f:
        # unique by (path, match) keeping the earliest commit
        seen = {}
        for c, p, n, ctx, m in rows:
            key = (p, m, ctx)
            if key not in seen:
                seen[key] = (c, p, n, ctx, m)
        f.write(f'{len(rows)} hits, {len(seen)} unique (path, match, context)\n')
        for c, p, n, ctx, m in sorted(seen.values(), key=lambda r: (r[1], r[2])):
            shown = ctx if kind != 'secret' else ctx.replace(m, mask(m))
            f.write(f'{c} {p}:{n}  [{m if kind != "secret" else mask(m)}]  {shown}\n')
        cnt = collections.Counter(r[4] if kind != 'secret' else mask(r[4]) for r in rows)
        f.write('\nby match:\n')
        for m, k in cnt.most_common():
            f.write(f'  {k:6}  {m}\n')

# commit messages, authors, committers
log = git('log', '--format=%H%x1f%an <%ae>%x1f%cn <%ce>%x1f%B%x1e', 'HEAD', '--', PREFIX).decode('utf-8', 'replace')
people = collections.Counter()
with open(os.path.join(OUT, 'messages.txt'), 'w', encoding='utf-8', newline='\n') as f:
    for rec in log.split('\x1e'):
        rec = rec.strip()
        if not rec:
            continue
        h, a, cm, body = rec.split('\x1f', 3)
        people[a] += 1; people['committer ' + cm] += 1
        for kind, regs in COMPILED.items():
            for r in regs:
                for m in r.finditer(body):
                    f.write(f'{h[:8]} {kind} [{m.group(0) if kind != "secret" else mask(m.group(0))}] {body.splitlines()[0][:80]}\n')
    f.write('\nauthors and committers:\n')
    for p, k in people.most_common():
        f.write(f'  {k:4}  {p}\n')

print(open(os.path.join(OUT, 'blobs.txt'), encoding='utf-8').read())
for kind in PATTERNS:
    path = os.path.join(OUT, f'{kind}.txt')
    print(kind, open(path, encoding='utf-8').readline().strip() if os.path.exists(path) else 'no hits')
