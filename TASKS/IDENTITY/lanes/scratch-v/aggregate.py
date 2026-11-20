# Summarises results-*.json of the visual pass into one text digest (aggregate.txt).
import glob
import io
import json
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = 'C:/dev/masaha/workspace/TASKS/IDENTITY/lanes/scratch-v'
files = sys.argv[1:] or sorted(glob.glob(f'{HERE}/results-*.json'))
NOISE = [r'/api/v1/files/spaces/.*\.webp', r'accounts\.google\.com/gsi', r'Failed to load resource: the server responded with a status of 404']

def noisy(text):
    return any(re.search(p, text) for p in NOISE)

for f in files:
    d = json.load(open(f, encoding='utf-8'))
    print(f'######## {f.split("/")[-1].split(chr(92))[-1]}')
    if d.get('notes'):
        print('notes:', d['notes'])
    for name, s in d['screens'].items():
        keys = list(s['variants'].keys())
        print(f'== {name}: {len(keys)} variants: {" ".join(keys)}')
        sea, sheet, sparkT, sparkB, contrast, images, over, status, cons, logos = {}, set(), {}, {}, {}, {}, [], {}, {}, {}
        for k, v in s['variants'].items():
            for h in v.get('sea', {}).get('hits', []):
                sea.setdefault(f"{h['el']} {h['prop']} {h['hex']} painted={h.get('painted')}", []).append(k)
            for h in v.get('sea', {}).get('sheetHits', []):
                sheet.add(h)
            for h in v.get('spark', {}).get('textHits', []):
                sparkT.setdefault(f"{h['el']} «{h['text']}»", []).append(k)
            for h in v.get('spark', {}).get('buttonHits', []):
                sparkB.setdefault(f"{h['el']} «{h['text']}» bg={h['bg']} borders={len(h['borders'])}", []).append(k)
            c = v.get('contrast', {})
            for h in c.get('failures', []):
                contrast.setdefault(f"{h['el']} «{h['text']}» fg {h['fg']} op {h['opacity']} on {h['ground']} {h['layers']} = {h['ratio']} (< {h['min']}, {h['size']}px/{h['weight']})", []).append(k)
            for h in c.get('images', []):
                if h.get('fails'):
                    images.setdefault(f"{h['el']} «{h['text']}» fg {h['fg']}@{h['fgAlpha']:.2f} over {h['image']}: min {h['minRatio']} p10 {h['p10']} median {h['median']} (< {h['min']})", []).append(k)
            if v.get('overflow', {}).get('over'):
                over.append(f"{k}: {v['overflow']['scrollWidth']}>{v['overflow']['clientWidth']} {v['overflow']['offenders'][:3]}")
            st = v.get('status', {})
            for m in st.get('mismatches', []):
                status.setdefault(f"{m['el']} {m['cls']} want {m['want']} got {m['got']}", []).append(k)
            if st.get('tokenMismatch'):
                status.setdefault(f"tokens {st['tokenMismatch']}", []).append(k)
            for m in v.get('console', []):
                if not noisy(m['text']):
                    cons.setdefault(f"{m['kind']}: {m['text'][:200]}", []).append(k)
            for l in v.get('logo', []):
                if l.get('visible'):
                    logos.setdefault(f"{l['where']} {l['cls']} size {l['size']} role={l['role']} label={l['label']} hidden={l['hidden']} transforms={l['transforms']} fills={l['fills']} link={l['link']} dir={l['dir']} startGap={l['startGap']}", []).append(k)
        def dump(title, m):
            if m:
                print(f'  -- {title}')
                for t, ks in m.items():
                    print(f'     {t}  [{len(ks)}: {" ".join(ks[:6])}{" …" if len(ks) > 6 else ""}]')
        dump('SEA', sea)
        if sheet:
            print('  -- SEA in stylesheets', sheet)
        dump('SPARK TEXT', sparkT)
        dump('SPARK BUTTON', sparkB)
        dump('CONTRAST', contrast)
        dump('CONTRAST OVER IMAGE', images)
        if over:
            print('  -- OVERFLOW', over)
        dump('STATUS', status)
        dump('CONSOLE', cons)
        dump('LOGO', logos)
        for k, a in s.get('axe', {}).items():
            for x in a:
                nodes = '; '.join(f"{n['target'][:80]}{(' ' + json.dumps({kk: n['data'][kk] for kk in ('fgColor', 'bgColor', 'contrastRatio') if kk in n['data']})) if n.get('data') and 'fgColor' in n['data'] else ''}" for n in x['nodes'][:4])
                print(f"  -- AXE {k}: {x['id']} ({x['impact']}, {x['count']}): {nodes}")
        for k, fo in s.get('focus', {}).items():
            last = fo['steps'][-1]
            print(f"  -- FOCUS {k}: ok={fo['ok']} third={last.get('el')} «{last.get('text', '')}» outline={last.get('outline')} ring={last.get('ring')} inView={last.get('inView')} fv={last.get('focusVisible')} dialog={last.get('inDialog')} sidebar={last.get('inSidebar')}")
    for h in d.get('hover', []):
        if h.get('missing'):
            print(f"HOVER {h['label']} ({h['theme']}): MISSING")
            continue
        sr = h.get('selRest') or {}
        sh = h.get('selHover') or {}
        print(f"HOVER {h['label']} ({h['theme']}/{h['lang']}): rest {h['rest']['painted']} -> hovered {h['hovered']['painted']} (bg {h['hovered']['bg']}) want {h['want']}; px {h['pixelSample']}" + (f"; selected {sr.get('painted')} bg {sr.get('bgHex')} border {sr.get('border')} before {sr.get('before', {}).get('bgHex')} -> under pointer {sh.get('painted')} bg {sh.get('bgHex')}" if sr else '') + f" :: {h['verdict']}")
    for k, v in d.get('ec', {}).items():
        print(f'EC {k}: {json.dumps(v, ensure_ascii=False)[:1500]}')
    for k in ('blocked', 'loads', 'refreshes', 'chrome', 'httpServer', 'shots', 'selftest'):
        if k in d:
            print(f'{k}: {d[k]}')
