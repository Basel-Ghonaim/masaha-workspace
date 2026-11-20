/* Masaha sign-in: shared behaviour for every direction.
   Strings (both languages), URL-driven states for the mock-ups, validation, the two switches.
   URL: ?lang=ar|en &theme=light|dark &state=wrong|toomany|offline|submitting|google|session|fields &from=<space slug> */
(function () {
  'use strict';

  var STR = {
    ar: {
      docTitle: 'تسجيل الدخول · مساحة',
      logo: 'مساحة',
      title: 'تسجيل الدخول',
      desc: 'سجّل الدخول لحفظ مساحاتك المفضّلة ومتابعة بلاغاتك، أو لإدارة مساحتك.',
      google: 'المواصلة باستخدام Google',
      or: 'أو',
      email: 'البريد الإلكتروني',
      password: 'كلمة المرور',
      forgot: 'نسيت كلمة المرور؟',
      submit: 'تسجيل الدخول',
      submitting: 'جارٍ تسجيل الدخول…',          /* proposal */
      show: 'إظهار', hide: 'إخفاء',                /* proposal */
      showLabel: 'إظهار كلمة المرور', hideLabel: 'إخفاء كلمة المرور',
      noAccount: 'ليس لديك حساب؟',
      create: 'إنشاء حساب',
      owners: 'تدير مساحة عمل؟ حسابات أصحاب المساحات ينشئها فريق مساحة.',
      contact: 'تواصل معنا',
      backHome: 'العودة إلى الرئيسية',
      backTo: 'العودة إلى {s}',
      privacy: 'سياسة الخصوصية',
      langSwitch: 'English', langSwitchLabel: 'English, switch to English',
      themeDark: 'الوضع الداكن', themeLight: 'الوضع الفاتح',
      wrongTitle: 'تعذّر تسجيل الدخول',
      wrongBody: 'البريد الإلكتروني أو كلمة المرور غير صحيحة.',
      tooMany: 'محاولات كثيرة. انتظر قليلًا ثم حاول مرة أخرى.',
      offline: 'لا يوجد اتصال. تحقّق من الإنترنت وحاول مرة أخرى.',
      googleFailed: 'تعذّرت المتابعة باستخدام Google',
      session: 'انتهت جلستك بعد 15 دقيقة دون نشاط. سجّل الدخول من جديد.',
      emailError: 'تحقّق من كتابة البريد الإلكتروني، مثل name@example.com',
      passwordError: 'أدخل كلمة المرور'
    },
    en: {
      docTitle: 'Sign in · Masaha',
      logo: 'Masaha',
      title: 'Sign in',
      desc: 'Sign in to save your favourite spaces and follow your reports, or to run your space.',
      google: 'Continue with Google',
      or: 'or',
      email: 'Email',
      password: 'Password',
      forgot: 'Forgot password?',
      submit: 'Sign in',
      submitting: 'Signing in…',
      show: 'Show', hide: 'Hide',
      showLabel: 'Show password', hideLabel: 'Hide password',
      noAccount: 'No account?',
      create: 'Create account',
      owners: 'Run a coworking space? Space owner accounts are created by the Masaha team.',
      contact: 'Contact us',
      backHome: 'Back to home',
      backTo: 'Back to {s}',
      privacy: 'Privacy policy',
      langSwitch: 'العربية', langSwitchLabel: 'العربية، التبديل إلى العربية',
      themeDark: 'Dark theme', themeLight: 'Light theme',
      wrongTitle: "Couldn't sign in",
      wrongBody: 'The email or password is incorrect.',
      tooMany: 'Too many attempts. Please wait a moment and try again.',
      offline: 'No connection. Check your internet and try again.',
      googleFailed: "Couldn't continue with Google",
      session: 'Your session ended after 15 minutes with no activity. Sign in again.',
      emailError: 'Check the email address, like name@example.com',
      passwordError: 'Enter your password'
    }
  };

  /* The 13 real spaces (materials/spaces.json, snapshot 2026-11-14). */
  var SPACES = [
    { slug: 'al-salam', ar: 'السلام هاب', en: 'Al-Salam Hub', areaAr: 'دير البلح', areaEn: 'Deir al-Balah', lat: 31.42013, lng: 34.34659 },
    { slug: 'branch', ar: 'برانش هاب', en: 'Branch Hub', areaAr: 'الرمال', areaEn: 'Al-Rimal', lat: 31.522347, lng: 34.448569 },
    { slug: 'coma', ar: 'كوما سبيس', en: 'coma,io', areaAr: 'النصيرات', areaEn: 'Nuseirat', lat: 31.44657, lng: 34.39386 },
    { slug: 'elevate', ar: 'إليفييت هاب', en: 'Elevate Hub', areaAr: 'النصيرات', areaEn: 'Nuseirat', lat: 31.4501, lng: 34.3942 },
    { slug: 'focus', ar: 'فوكس هاب', en: 'Focus Hub', areaAr: 'النصر', areaEn: 'An-Nasr', lat: 31.53294, lng: 34.45491 },
    { slug: 'garden', ar: 'جاردن سبييس', en: 'Garden Space', areaAr: 'الدرج', areaEn: 'Al-Daraj', lat: 31.51304, lng: 34.45432 },
    { slug: 'golden', ar: 'جولدن هاب', en: 'Golden Hub', areaAr: 'شمال قطاع غزة', areaEn: 'North Gaza Strip', lat: 31.51483, lng: 34.45052 },
    { slug: 'jreas', ar: 'جريس هاب', en: 'Jreas Hub', areaAr: 'الدرج', areaEn: 'Al-Daraj', lat: 31.51981, lng: 34.45768 },
    { slug: 'masahat', ar: 'مساحات', en: 'Masahat', areaAr: 'الرمال', areaEn: 'Al-Rimal', lat: 31.52788, lng: 34.43792 },
    { slug: 'masar', ar: 'مسار تِك', en: 'Masar Tech', areaAr: 'المواصي', areaEn: 'Al-Mawasi', lat: 31.36569, lng: 34.27055 },
    { slug: 'number-one', ar: 'نمبر ون هاب', en: 'Number One Hub', areaAr: 'النصر', areaEn: 'An-Nasr', lat: 31.52861, lng: 34.45009 },
    { slug: 'pal', ar: 'بال هاب', en: 'Pal Hub', areaAr: 'الرمال', areaEn: 'Al-Rimal', lat: 31.51593, lng: 34.45156 },
    { slug: 'white', ar: 'وايت سبيس', en: 'White Space', areaAr: 'الرمال', areaEn: 'Al-Rimal', lat: 31.51938, lng: 34.4473 }
  ];

  /* materials/strip-outline.json: [lat, lng], north-west corner first, coast to Rafah, then the eastern border back north. */
  var OUTLINE = [[31.5944,34.4898],[31.56,34.463],[31.523,34.43],[31.49,34.403],[31.46,34.376],[31.43,34.341],[31.39,34.294],
    [31.36,34.256],[31.33,34.23],[31.316,34.219],[31.22,34.267],[31.248,34.288],[31.29,34.323],[31.33,34.36],[31.38,34.395],
    [31.425,34.42],[31.46,34.45],[31.495,34.49],[31.525,34.515],[31.552,34.542],[31.588,34.564],[31.5944,34.4898]];

  var params = new URLSearchParams(location.search);
  var root = document.documentElement;
  var listeners = [];
  var state = {
    lang: params.get('lang') === 'en' ? 'en' : 'ar',
    theme: params.get('theme') || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'),
    from: SPACES.filter(function (s) { return s.slug === params.get('from'); })[0] || null,
    attempts: 0
  };
  if (state.theme !== 'dark') state.theme = 'light';

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $all(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }
  function t(key) { var s = STR[state.lang]; return (window.MASAHA_EXTRA && window.MASAHA_EXTRA[state.lang] && window.MASAHA_EXTRA[state.lang][key]) || s[key] || key; }

  function syncUrl() {
    try {
      var p = new URLSearchParams(location.search);
      p.set('lang', state.lang); p.set('theme', state.theme);
      history.replaceState(null, '', '?' + p.toString());
    } catch (e) { /* file:// in some browsers */ }
  }

  function applyLang() {
    root.lang = state.lang;
    root.dir = state.lang === 'ar' ? 'rtl' : 'ltr';
    document.title = t('docTitle');
    $all('[data-t]').forEach(function (el) { el.textContent = t(el.getAttribute('data-t')); });
    $all('[data-t-label]').forEach(function (el) { el.setAttribute('aria-label', t(el.getAttribute('data-t-label'))); });
    var back = $('#back-label');
    if (back) back.textContent = state.from ? t('backTo').replace('{s}', state.from[state.lang]) : t('backHome');
    var lang = $('#lang');
    if (lang) {
      lang.textContent = t('langSwitch');
      lang.setAttribute('lang', state.lang === 'ar' ? 'en' : 'ar');
      lang.setAttribute('hreflang', state.lang === 'ar' ? 'en' : 'ar');
    }
    applyTheme();
    refreshAlerts();
    refreshFieldErrors();
    refreshPasswordToggle();
    refreshBusy();
  }

  function applyTheme() {
    root.setAttribute('data-theme', state.theme);
    var b = $('#theme');
    if (b) {
      b.setAttribute('aria-pressed', state.theme === 'dark' ? 'true' : 'false');
      b.setAttribute('aria-label', t('themeDark'));
      b.setAttribute('title', state.theme === 'dark' ? t('themeLight') : t('themeDark'));
    }
  }

  function emit() { listeners.forEach(function (fn) { try { fn(state); } catch (e) { console.error(e); } }); }

  /* ---------- alerts ---------- */
  var alertKind = null;
  function showAlert(kind, focus) {
    alertKind = kind;
    refreshAlerts();
    var el = kind === 'google' ? $('#google-alert') : $('#alert');
    if (focus && el) el.focus();
  }
  function clearAlerts() { alertKind = null; refreshAlerts(); }
  function refreshAlerts() {
    var a = $('#alert'), g = $('#google-alert');
    if (a) {
      var map = { wrong: ['wrongTitle', 'wrongBody'], toomany: [null, 'tooMany'], offline: [null, 'offline'] }[alertKind];
      a.hidden = !map;
      a.setAttribute('data-kind', alertKind || '');
      if (map) {
        var ti = $('[data-alert-title]', a), bo = $('[data-alert-body]', a);
        ti.hidden = !map[0]; ti.textContent = map[0] ? t(map[0]) : '';
        bo.textContent = t(map[1]);
      }
    }
    if (g) {
      g.hidden = alertKind !== 'google';
      $('[data-alert-title]', g).textContent = t('googleFailed');
    }
    var s = $('#session-note');
    if (s) { s.hidden = !state.session; $('[data-alert-body]', s).textContent = t('session'); }
    root.toggleAttribute('data-has-alert', !!alertKind || !!state.session);
  }

  /* ---------- fields ---------- */
  var touched = { email: false, password: false };
  var errors = { email: false, password: false };
  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  function validate(name) {
    var el = $('#' + name);
    if (!el) return true;
    errors[name] = name === 'email' ? !EMAIL.test(el.value.trim()) : el.value.length === 0;
    return !errors[name];
  }
  function refreshFieldErrors() {
    ['email', 'password'].forEach(function (name) {
      var el = $('#' + name), msg = $('#' + name + '-error');
      if (!el || !msg) return;
      var on = errors[name] && touched[name];
      el.setAttribute('aria-invalid', on ? 'true' : 'false');
      msg.hidden = !on;
      var txt = $('[data-error-text]', msg) || msg;
      /* the example address is an always-LTR value: isolate it inside the sentence */
      var parts = t(name + 'Error').split('name@example.com');
      txt.textContent = parts[0];
      if (parts.length > 1) {
        var b = document.createElement('bdi'); b.dir = 'ltr'; b.textContent = 'name@example.com';
        txt.appendChild(b); txt.appendChild(document.createTextNode(parts[1]));
      }
      var field = el.closest('.field');
      if (field) field.classList.toggle('is-invalid', on);
    });
  }

  /* ---------- password visibility (proposal) ---------- */
  function refreshPasswordToggle() {
    var b = $('#pw-toggle'), p = $('#password');
    if (!b || !p) return;
    var shown = p.type === 'text';
    var lbl = $('[data-pw-label]', b);
    if (lbl) lbl.textContent = t(shown ? 'hide' : 'show');
    b.setAttribute('aria-label', t(shown ? 'hideLabel' : 'showLabel'));
    b.setAttribute('aria-pressed', shown ? 'true' : 'false');
  }

  /* ---------- busy ---------- */
  var busy = false;
  function refreshBusy() {
    var b = $('#submit');
    if (!b) return;
    b.setAttribute('aria-busy', busy ? 'true' : 'false');
    b.setAttribute('aria-disabled', busy ? 'true' : 'false');
    var l = $('[data-submit-label]', b);
    if (l) l.textContent = t(busy ? 'submitting' : 'submit');
    $all('#email, #password').forEach(function (i) { i.readOnly = busy; });
    root.toggleAttribute('data-busy', busy);
  }

  function setBusy(v) { busy = v; refreshBusy(); }

  /* ---------- wiring ---------- */
  function wire() {
    var form = $('#signin');
    var email = $('#email'), pw = $('#password');
    ['email', 'password'].forEach(function (name) {
      var el = $('#' + name);
      if (!el) return;
      el.addEventListener('blur', function () {
        if (el.value.length === 0 && !touched[name]) return; /* blur-first, but don't scold an untouched empty field */
        touched[name] = true; validate(name); refreshFieldErrors();
      });
      el.addEventListener('input', function () {
        if (touched[name] && errors[name]) { validate(name); refreshFieldErrors(); } /* errors clear as soon as fixed */
        if (alertKind && alertKind !== 'google') clearAlerts();
      });
    });

    if (form) form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (busy) return;
      touched.email = touched.password = true;
      var ok1 = validate('email'), ok2 = validate('password');
      refreshFieldErrors();
      if (!ok1 || !ok2) { (ok1 ? pw : email).focus(); return; }
      clearAlerts();
      setBusy(true);
      setTimeout(function () {
        setBusy(false);
        state.attempts += 1;
        if (!navigator.onLine) showAlert('offline', true);
        else showAlert(state.attempts >= 3 ? 'toomany' : 'wrong', true);
      }, 1400);
    });

    var g = $('#google');
    if (g) g.addEventListener('click', function () { showAlert('google', true); });

    var tg = $('#pw-toggle');
    if (tg) tg.addEventListener('click', function () {
      pw.type = pw.type === 'password' ? 'text' : 'password';
      refreshPasswordToggle();
    });

    var th = $('#theme');
    if (th) th.addEventListener('click', function () {
      state.theme = state.theme === 'dark' ? 'light' : 'dark';
      applyTheme(); syncUrl(); emit();
    });

    var lg = $('#lang');
    if (lg) lg.addEventListener('click', function (e) {
      e.preventDefault();
      state.lang = state.lang === 'ar' ? 'en' : 'ar';
      applyLang(); syncUrl(); emit();
    });

    $all('a[href="#"]').forEach(function (a) { if (a.id !== 'lang') a.addEventListener('click', function (e) { e.preventDefault(); }); });
  }

  /* ---------- mock-up states from the URL ---------- */
  function applyUrlState() {
    var s = params.get('state');
    var email = $('#email'), pw = $('#password');
    if (s === 'session') state.session = true;
    if (s === 'wrong' || s === 'toomany' || s === 'offline' || s === 'submitting') {
      email.value = 'name@example.com'; pw.value = 'masaha-2026';
    }
    if (s === 'wrong' || s === 'toomany' || s === 'offline') { alertKind = s; }
    if (s === 'google') { alertKind = 'google'; }
    if (s === 'submitting') { busy = true; }
    if (s === 'fields') {
      email.value = 'name@example'; pw.value = '';
      touched.email = touched.password = true; validate('email'); validate('password');
    }
    applyLang();
    var focusEl = s === 'fields' ? email : (s === 'wrong' || s === 'toomany' || s === 'offline') ? $('#alert') : s === 'google' ? $('#google-alert') : null;
    if (focusEl) focusEl.focus({ preventScroll: true });
  }

  window.Masaha = {
    STR: STR, SPACES: SPACES, OUTLINE: OUTLINE, state: state, t: t,
    onChange: function (fn) { listeners.push(fn); fn(state); }
  };

  function init() {
    if (params.get('capture')) root.setAttribute('data-capture', '');
    wire(); applyUrlState(); emit(); root.classList.add('is-ready');
    /* for the capture tool: the page's real height once fonts are in */
    var mark = function () { root.setAttribute('data-h', String(Math.ceil(document.documentElement.scrollHeight))); };
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { setTimeout(mark, 60); }); else mark();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
