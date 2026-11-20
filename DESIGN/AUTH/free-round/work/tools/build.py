"""Build each direction's self-contained page: work/src/<dir>.html -> work/<dir>/index.html.
Inlines the logo, the Google G and the shared script, so every page opens from a double-click."""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / 'work' / 'src'
LOGO = (ROOT / 'materials' / 'logo' / 'masaha-logo-berry.svg').read_text(encoding='utf-8')

paths = re.findall(r'<path([^>]*)/?>', LOGO)
def pd(p): return re.search(r' d="([^"]*)"', p).group(1)
ink = next(pd(p) for p in paths if '#1A1F25' in p)
berry = next(pd(p) for p in paths if '#B55BB3' in p)

def logo_svg(cls='logo', view='263 45 2473 903'):
    return (f'<svg class="{cls}" viewBox="{view}" aria-hidden="true" focusable="false">'
            f'<path class="logo-ink" fill-rule="evenodd" d="{ink}"/>'
            f'<path class="logo-berry" fill-rule="evenodd" d="{berry}"/></svg>')

G = ('<svg class="g-logo" viewBox="0 0 48 48" aria-hidden="true" focusable="false">'
     '<path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>'
     '<path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>'
     '<path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>'
     '<path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>'
     '</svg>')

SHARED = (SRC / 'shared.js').read_text(encoding='utf-8')

def build(name):
    src = (SRC / f'{name}.html').read_text(encoding='utf-8')
    out = (src.replace('<!--@logo-->', logo_svg())
              .replace('<!--@mark-->', logo_svg('mark', '190 17 778 778'))
              .replace('<!--@g-->', G)
              .replace('/*@shared*/', SHARED))
    for m in re.findall(r'<!--@include ([\w.-]+)-->', out):
        out = out.replace(f'<!--@include {m}-->', (SRC / m).read_text(encoding='utf-8'))
    dest = ROOT / 'work' / name / 'index.html'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out, encoding='utf-8')
    print(f'{name}: {len(out.encode("utf-8"))/1024:.1f} KB -> {dest.relative_to(ROOT)}')

if __name__ == '__main__':
    for n in (sys.argv[1:] or [p.stem for p in SRC.glob('*.html')]):
        build(n)
