"""Build round 6's three sign-in directions as standalone HTML (theme via ?theme=dark)."""
import re, pathlib

LOGO_DIR = pathlib.Path(r"C:/dev/masaha/free-round/materials/logo")
OUT = pathlib.Path(r"C:/dev/masaha/workspace/DESIGN/AUTH/round6")
OUT.mkdir(parents=True, exist_ok=True)


def svg(name, prefix, ink, dot, extra=""):
    s = (LOGO_DIR / name).read_text(encoding="utf-8")
    s = re.sub(r"<\?xml[^>]*>", "", s).strip()
    s = s.replace('fill="#1A1F25"', f'fill="{ink}"').replace('fill="#B55BB3"', f'fill="{dot}"')
    s = re.sub(r'id="([a-z]+)"', lambda m: f'id="{prefix}{m.group(1)}"', s)
    s = re.sub(r'url\(#([a-z]+)\)', lambda m: f'url(#{prefix}{m.group(1)})', s)
    return s.replace("<svg ", f'<svg {extra} aria-hidden="true" focusable="false" ', 1)


def logo(prefix, cls="logo"):
    return svg("masaha-logo-berry.svg", prefix, "var(--logo-ink)", "var(--logo-dot)", f'class="{cls}"')


def mark(prefix, cls):
    return svg("masaha-mark-berry.svg", prefix, "var(--mark-body)", "var(--mark-dot)", f'class="{cls}"')


GOOGLE = '<svg width="18" height="18" viewBox="0 0 48 48" aria-hidden="true"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.430 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.450-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.970-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>'
MOON = '<svg class="i-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>'
SUN = '<svg class="i-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
HEART = '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path fill="var(--heart)" stroke="var(--heart)" stroke-width="2" stroke-linejoin="round" d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7Z"/></svg>'
HEART_OFF = HEART.replace('fill="var(--heart)" stroke="var(--heart)"', 'fill="none" stroke="var(--heart-off)"')
CHEV = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 18 6-6-6-6"/></svg>'

HEAD = """<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<script>document.documentElement.dataset.theme = new URLSearchParams(location.search).get('theme') === 'dark' ? 'dark' : 'light';</script>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&amp;display=swap">
<style>
:root {{
  --page:#F7FBFF; --surface:#FFFFFF; --fg:#1A1F25; --muted:#5E646A; --subtle:#6E757C;
  --border:#C9D0D7; --line:#DDE5ED; --primary:#934791; --primary-fg:#FFFFFF;
  --logo-ink:#1A1F25; --logo-dot:#B55BB3; --ring:#1A1F25;
  --success:#1D7146; --success-dot:#2E9E62; --success-bg:#E8F6EE; --heart:#B55BB3; --heart-off:#6E757C;
  --brand:linear-gradient(150deg,#A04E9E 0%,#773A75 38%,#4A2149 72%,#2A0E28 100%);
  --brand-h:linear-gradient(to left,#934791 0%,#6A3268 45%,#2A0E28 100%);
  --on-brand:#F7FBFF; --on-brand-muted:#F3DDF2; --mark-body:rgba(255,255,255,.07); --mark-dot:rgba(247,182,245,.5);
  color-scheme: light;
}}
[data-theme=dark] {{
  --page:#0D1217; --surface:#151B21; --fg:#F7FBFF; --muted:#A9B1B9; --subtle:#8E969E;
  --border:#3A434C; --line:#262E36; --primary:#D27ED0; --primary-fg:#1A0A19;
  --logo-ink:#F7FBFF; --logo-dot:#D27ED0; --ring:#F7FBFF;
  --success:#7FD6A4; --success-dot:#4CC283; --success-bg:#12291D; --heart:#D27ED0; --heart-off:#8E969E;
  --brand:linear-gradient(150deg,#6A3268 0%,#4A2149 38%,#2A0E28 72%,#140612 100%);
  --brand-h:linear-gradient(to left,#6A3268 0%,#3F1B3E 50%,#140612 100%);
  --mark-body:rgba(255,255,255,.05); --mark-dot:rgba(210,126,208,.45);
  color-scheme: dark;
}}
* {{ box-sizing: border-box; }}
html, body {{ margin:0; background:var(--page); color:var(--fg); font-family:'IBM Plex Sans Arabic', system-ui, sans-serif; }}
a {{ color:inherit; text-underline-offset:4px; }}
button {{ font:inherit; color:inherit; cursor:pointer; }}
.on-brand {{ --logo-ink:#F7FBFF; --logo-dot:#F7B6F5; color:var(--on-brand); }}
.i-sun {{ display:none; }} [data-theme=dark] .i-sun {{ display:block; }} [data-theme=dark] .i-moon {{ display:none; }}
.tools {{ display:flex; align-items:center; gap:4px; font-size:14px; font-weight:500; }}
.tools button {{ height:44px; min-width:44px; padding:0 12px; border:0; background:transparent; display:flex; align-items:center; justify-content:center; }}
.logo {{ height:40px; width:auto; display:block; }}
.form {{ display:flex; flex-direction:column; gap:20px; }}
.google {{ height:44px; border:1px solid var(--border); border-radius:8px; background:var(--surface); font-size:15px; font-weight:500; display:flex; align-items:center; justify-content:center; gap:10px; }}
.or {{ display:flex; align-items:center; gap:12px; color:var(--subtle); font-size:13px; }}
.or::before, .or::after {{ content:''; flex:1; height:1px; background:var(--line); }}
.field {{ display:flex; flex-direction:column; gap:8px; font-size:14px; font-weight:500; }}
.field-head {{ display:flex; justify-content:space-between; align-items:baseline; }}
.field-head a {{ font-size:14px; font-weight:500; }}
.input {{ height:48px; border:1px solid var(--border); border-radius:8px; padding:0 14px; background:var(--surface); color:var(--fg); font:inherit; font-size:15px; width:100%; }}
.input.ltr {{ direction:ltr; text-align:right; }}
.input::placeholder {{ color:var(--subtle); }}
.pw {{ position:relative; }}
.pw span {{ position:absolute; inset-inline-end:6px; top:6px; height:36px; padding:0 10px; display:flex; align-items:center; font-size:14px; font-weight:500; color:var(--muted); }}
.primary {{ height:48px; border:0; border-radius:8px; background:var(--primary); color:var(--primary-fg); font-size:16px; font-weight:600; }}
.muted {{ color:var(--muted); }}
{css}
</style>
</head>
<body>
{body}
</body>
</html>
"""

FORM = f"""<form class="form" onsubmit="return false">
<button type="button" class="google">{GOOGLE}المواصلة باستخدام Google</button>
<div class="or">أو</div>
<label class="field">البريد الإلكتروني<input class="input ltr" type="email" placeholder="name@example.com"></label>
<div class="field"><div class="field-head"><label for="pw">كلمة المرور</label><a href="#">نسيت كلمة المرور؟</a></div>
<div class="pw"><input id="pw" class="input" type="password"><span>إظهار</span></div></div>
<button type="submit" class="primary">تسجيل الدخول</button>
</form>"""

TOOLS = f'<div class="tools"><button type="button" lang="en">English</button><button type="button" aria-label="المظهر">{MOON}{SUN}</button></div>'

# ---------------------------------------------------------------- direction 1: B with the berry masthead
D1_CSS = """
.page { min-height:100vh; display:flex; flex-direction:column; }
.mast { background:var(--brand-h); }
.mast-in { max-width:1120px; margin:0 auto; padding:0 24px; }
.mast-top { height:88px; display:flex; align-items:center; justify-content:space-between; }
.mast-title { padding:56px 0 56px; max-width:640px; }
.mast h1 { margin:0 0 12px; font-size:56px; line-height:1.2; font-weight:700; }
.mast p { margin:0; font-size:18px; line-height:1.7; color:var(--on-brand-muted); }
main { flex:1; max-width:1120px; width:100%; margin:0 auto; padding:48px 24px 64px; display:grid; grid-template-columns: 5fr 1fr 6fr; }
.new { grid-column:3; border-inline-start:1px solid var(--line); padding-inline-start:48px; display:flex; flex-direction:column; gap:16px; align-self:start; }
.new h2 { margin:0; font-size:22px; font-weight:600; }
.new p { margin:0; font-size:15px; line-height:1.8; }
.outline { align-self:flex-start; height:44px; padding:0 20px; display:inline-flex; align-items:center; border:1px solid var(--fg); border-radius:8px; text-decoration:none; font-size:15px; font-weight:600; }
.note { margin-top:8px; padding-top:20px; border-top:1px solid var(--line); font-size:14px; line-height:1.7; }
footer { max-width:1120px; width:100%; margin:0 auto; padding:0 24px 24px; font-size:13px; }
@media (max-width: 767px) {
  .mast-in { padding:0 20px; } .mast-top { height:64px; } .logo { height:32px; }
  .mast-title { padding:24px 0 32px; } .mast h1 { font-size:36px; } .mast p { font-size:16px; }
  main { display:flex; flex-direction:column; gap:40px; padding:32px 20px 40px; }
  .new { border-inline-start:0; padding-inline-start:0; border-top:1px solid var(--line); padding-top:32px; }
  footer { padding:0 20px 24px; }
}
"""
D1_BODY = f"""<div class="page">
<header class="mast on-brand"><div class="mast-in">
<div class="mast-top">{logo('a')}{TOOLS}</div>
<div class="mast-title"><h1>تسجيل الدخول</h1><p>لحفظ مساحاتك المفضّلة ومتابعة بلاغاتك، أو لإدارة مساحتك.</p></div>
</div></header>
<main>
<div>{FORM}</div>
<section class="new">
<h2>جديد على مساحة؟</h2>
<p class="muted">أنشئ حسابًا لتحفظ مساحاتك المفضّلة وتتابع البلاغات التي ترسلها.</p>
<a href="#" class="outline">إنشاء حساب</a>
<p class="note muted">تدير مساحة عمل؟ حسابات أصحاب المساحات ينشئها فريق مساحة. <a href="#" style="color:var(--fg);font-weight:500">تواصل معنا</a></p>
</section>
</main>
<footer><a href="#" class="muted">سياسة الخصوصية</a></footer>
</div>"""

# ---------------------------------------------------------------- directions 2 and 3: a brand panel beside the form
SPLIT_CSS = """
.split { min-height:100vh; display:grid; grid-template-columns: minmax(480px, 560px) 1fr; }
.side { padding:32px 72px 32px; display:flex; flex-direction:column; min-height:100vh; }
.side-top { height:56px; display:flex; align-items:center; justify-content:space-between; }
.back { margin-top:40px; display:inline-flex; align-items:center; gap:6px; font-size:14px; font-weight:500; color:var(--muted); text-decoration:none; }
.side h1 { margin:16px 0 8px; font-size:48px; line-height:1.25; font-weight:700; }
.lead { margin:0 0 32px; font-size:17px; line-height:1.7; }
.join { margin-top:32px; padding-top:24px; border-top:1px solid var(--line); display:flex; flex-direction:column; gap:10px; font-size:15px; }
.join a.strong { font-weight:600; }
.join .small { font-size:14px; line-height:1.7; }
.join .small a { white-space:nowrap; }
.side-foot { margin-top:auto; padding-top:32px; font-size:13px; }
.panel { position:relative; overflow:hidden; background:var(--brand); }
.panel-words { position:absolute; inset-inline-start:72px; bottom:72px; max-width:520px; }
.panel-words h2 { margin:0 0 14px; font-size:44px; line-height:1.3; font-weight:700; }
.panel-words p { margin:0; font-size:18px; line-height:1.7; color:var(--on-brand-muted); }
.band { display:none; }
@media (max-width: 767px) {
  .split { display:block; }
  .panel { display:none; }
  .band { display:block; position:relative; overflow:hidden; background:var(--brand); height:148px; padding:12px 20px; }
  .band .side-top { position:relative; z-index:1; }
  .band .logo { height:32px; }
  .side { min-height:0; padding:0 20px 24px; }
  .side > .side-top { display:none; }
  .back { margin-top:20px; }
  .side h1 { font-size:34px; margin-top:12px; }
  .lead { font-size:16px; margin-bottom:24px; }
}
"""
SIDE = """<div class="side">
<div class="side-top">{logo}{tools}</div>
<a href="#" class="back">{chev}العودة إلى الرئيسية</a>
<h1>تسجيل الدخول</h1>
<p class="lead muted">لحفظ مساحاتك المفضّلة ومتابعة بلاغاتك، أو لإدارة مساحتك.</p>
{form}
<div class="join">
<div>ليس لديك حساب؟ <a href="#" class="strong">إنشاء حساب</a></div>
<div class="small muted">تدير مساحة عمل؟ حسابات أصحاب المساحات ينشئها فريق مساحة. <a href="#" style="color:var(--fg);font-weight:500">تواصل معنا</a></div>
</div>
<div class="side-foot"><a href="#" class="muted">سياسة الخصوصية</a></div>
</div>"""


def side(prefix):
    return SIDE.format(logo=logo(prefix), tools=TOOLS, chev=CHEV, form=FORM)


def band(prefix):
    return f'<div class="band on-brand"><div class="side-top">{logo(prefix + "b")}{TOOLS}</div>{mark(prefix + "bm", "band-mark")}</div>'


D2_CSS = SPLIT_CSS + """
.big-mark { position:absolute; height:80%; width:auto; inset-inline-end:-10%; bottom:-26%; }
.panel.d2 .panel-words { top:168px; bottom:auto; }
.band-mark { position:absolute; height:190px; width:auto; inset-inline-end:16px; bottom:-96px; }
"""
D2_BODY = f"""{band('c')}
<div class="split">
{side('d')}
<aside class="panel d2 on-brand" aria-hidden="true">
{mark('e', 'big-mark')}
<div class="panel-words"><h2>مساحة عمل قريبة،<br>ومفتوحة الآن.</h2><p>دليل مساحات العمل في قطاع غزة، بساعاتها وحالتها الآن.</p></div>
</aside>
</div>"""

# ---------------------------------------------------------------- direction 3: a real space card in the panel
D3_CSS = SPLIT_CSS + """
.band-mark { position:absolute; height:190px; width:auto; inset-inline-end:16px; bottom:-96px; }
.cards { position:absolute; inset-inline-start:72px; top:120px; width:460px; }
.from { font-size:14px; font-weight:500; color:var(--on-brand-muted); margin:0 0 16px; }
.card { background:var(--surface); color:var(--fg); border-radius:16px; padding:24px; box-shadow:0 24px 48px rgba(20,6,18,.35); }
.card + .card { margin-top:12px; }
.card.second { margin-inline-start:48px; }
.card-top { display:flex; justify-content:space-between; align-items:flex-start; gap:16px; }
.card h3 { margin:0 0 4px; font-size:22px; font-weight:600; }
.card .area { font-size:15px; color:var(--muted); }
.saved { width:44px; height:44px; border-radius:999px; border:1px solid var(--line); display:flex; align-items:center; justify-content:center; flex:none; }
.status { margin-top:20px; display:inline-flex; align-items:center; gap:8px; height:32px; padding:0 12px; border-radius:999px; background:var(--success-bg); color:var(--success); font-size:14px; font-weight:600; }
.status i { width:8px; height:8px; border-radius:50%; background:var(--success-dot); }
.hours { margin-inline-start:8px; font-size:14px; color:var(--muted); }
.panel-words { bottom:72px; }
"""
CARD = """<div class="card {cls}"><div class="card-top"><div><h3>{name}</h3><div class="area">{area}</div></div>
<div class="saved">{heart}</div></div>
<div><span class="status"><i></i>مفتوحة الآن</span><span class="hours">حتى {until}</span></div></div>"""
D3_BODY = f"""{band('f')}
<div class="split">
{side('g')}
<aside class="panel on-brand" aria-hidden="true">
<div class="cards"><p class="from">من الدليل</p>
<div style="position:relative">
{CARD.format(cls='first', name='السلام هاب', area='دير البلح', heart=HEART, until='6:00 م')}
{CARD.format(cls='second', name='برانش هاب', area='الرمال، غزة', heart=HEART_OFF, until='8:00 م')}
</div></div>
<div class="panel-words"><h2>احفظ مساحاتك المفضّلة،<br>وارجع لها بنقرة.</h2><p>دليل مساحات العمل في قطاع غزة، بساعاتها وحالتها الآن.</p></div>
</aside>
</div>"""

for name, title, css, body in [
    ("dir1-masthead", "الاتجاه 1 — الشريط بلون الهوية", D1_CSS, D1_BODY),
    ("dir2-panel", "الاتجاه 2 — لوحة الهوية", D2_CSS, D2_BODY),
    ("dir3-card", "الاتجاه 3 — بطاقة من الدليل", D3_CSS, D3_BODY),
]:
    (OUT / f"{name}.html").write_text(HEAD.format(title=title, css=css, body=body), encoding="utf-8", newline="\n")
    print(name)

# ---------------------------------------------------------------- direction 4: direction 2's panel, showing what an account gives
D4_CSS = SPLIT_CSS + """
.band-mark { position:absolute; height:190px; width:auto; inset-inline-end:16px; bottom:-96px; }
.big-mark { position:absolute; height:56%; width:auto; inset-inline-end:-240px; bottom:-14%; }
.give { position:absolute; inset:0; padding:72px; display:flex; flex-direction:column; justify-content:center; }
.give-in { width:520px; }
.label { margin:0 0 12px; font-size:15px; font-weight:500; color:var(--on-brand-muted); }
.give h2 { margin:0 0 32px; font-size:40px; line-height:1.3; font-weight:700; }
.rows { display:flex; flex-direction:column; gap:12px; }
.row { background:var(--surface); color:var(--fg); border-radius:14px; padding:20px 20px; display:grid; grid-template-columns:1fr 188px; gap:20px; align-items:center; box-shadow:0 16px 40px rgba(20,6,18,.28); }
.row h3 { margin:0 0 4px; font-size:17px; font-weight:600; }
.row p { margin:0; font-size:14px; line-height:1.65; color:var(--muted); }
.frag { border:1px solid var(--line); border-radius:10px; padding:10px 12px; font-size:13px; background:var(--page); }
.fav { display:flex; align-items:center; justify-content:space-between; gap:8px; }
.fav b { display:block; font-size:14px; font-weight:600; } .fav span { color:var(--muted); }
.chip { display:inline-flex; align-items:center; gap:6px; height:26px; padding:0 10px; border-radius:999px; font-size:12.5px; font-weight:600; }
.chip i { width:7px; height:7px; border-radius:50%; }
.chip.wait { background:var(--warn-bg); color:var(--warn); } .chip.wait i { background:var(--warn-dot); }
.chip.done { background:var(--success-bg); color:var(--success); } .chip.done i { background:var(--success-dot); }
.rep { display:flex; flex-direction:column; gap:6px; align-items:flex-start; } .rep span { color:var(--muted); }
.nav { padding:6px; display:flex; flex-direction:column; gap:2px; }
.nav div { position:relative; height:28px; display:flex; align-items:center; padding-inline-start:12px; border-radius:6px; color:var(--muted); }
.nav div.on { background:var(--sel); color:var(--fg); font-weight:600; }
.nav div.on::before { content:''; position:absolute; inset-inline-start:0; top:5px; bottom:5px; width:3px; border-radius:3px; background:var(--heart); }
:root { --warn:#8A5300; --warn-bg:#FDF3E1; --warn-dot:#D58A14; --sel:#F6E9F5; }
[data-theme=dark] { --warn:#F2C26B; --warn-bg:#2E2210; --warn-dot:#E0A23A; --sel:#2A1A29; }
"""
D4_BODY = f"""{band('h')}
<div class="split">
{side('i')}
<aside class="panel on-brand" aria-hidden="true">
{mark('j', 'big-mark')}
<div class="give"><div class="give-in">
<p class="label">حسابك في مساحة</p>
<h2>كل ما يخصّك في مساحة،<br>في حساب واحد.</h2>
<div class="rows">
<div class="row"><div><h3>المفضّلة</h3><p>احفظ المساحات التي تحبّها، وارجع لها من أي جهاز.</p></div>
<div class="frag fav"><div><b>السلام هاب</b><span>دير البلح</span></div>{HEART}</div></div>
<div class="row"><div><h3>بلاغاتي</h3><p>أبلغ عن معلومة غير صحيحة، وتابع الردّ عليها.</p></div>
<div class="frag rep"><span>ساعات العمل غير صحيحة</span><span class="chip wait"><i></i>قيد المراجعة</span></div></div>
<div class="row"><div><h3>لأصحاب المساحات</h3><p>أدِر مساحتك من لوحة واحدة، أنت وفريق الاستقبال.</p></div>
<div class="frag nav"><div class="on">مكتب الاستقبال</div><div>الزبائن</div><div>الاشتراكات</div></div></div>
</div></div></div>
</aside>
</div>"""
(OUT / "dir4-panel-account.html").write_text(HEAD.format(title="الاتجاه 2، اللوحة: ما يعطيه الحساب", css=D4_CSS, body=D4_BODY), encoding="utf-8", newline="\n")
print("dir4-panel-account")
