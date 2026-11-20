/* Sign in (and create account, ?register=1) — no floating card: the form sits on the page, in the content column. */
(function () {
  var reg = new URLSearchParams(location.search).get('register') === '1';
  var R = {
    ar: { title: 'إنشاء حساب', description: 'احفظ مساحاتك المفضّلة وتابع البلاغات التي ترسلها.', submit: 'إنشاء الحساب', have: 'لديك حساب؟', signIn: 'تسجيل الدخول', name: 'الاسم', nameErr: 'أدخل اسمك', owner: 'تدير مساحة عمل؟ حسابات أصحاب المساحات ينشئها فريق مساحة.', forgotTitle: 'نسيت كلمة المرور', forgotText: 'أدخل البريد الذي سجّلت به، وسنرسل إليه رابطًا لتعيين كلمة مرور جديدة.' },
    en: { title: 'Create account', description: 'Save your favourite spaces and follow the reports you send.', submit: 'Create account', have: 'Have an account?', signIn: 'Sign in', name: 'Name', nameErr: 'Enter your name', owner: 'Run a coworking space? Space owner accounts are created by the Masaha team.', forgotTitle: 'Forgot password', forgotText: 'Enter the email you signed up with, and we’ll send it a link to set a new password.' }
  };
  function check(el) {
    var a = M.t().auth, r = R[M.lang], msg = '';
    if (el.id === 'f-email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(el.value.trim())) msg = a.emailErr;
    if (el.id === 'f-pass' && !el.value) msg = a.passErr;
    if (el.id === 'f-name' && !el.value.trim()) msg = r.nameErr;
    var er = document.getElementById(el.id + '-err');
    er.textContent = msg; er.hidden = !msg; el.setAttribute('aria-invalid', String(!!msg));
    return !msg;
  }
  M.boot({
    id: 'login',
    title: function () { return reg ? R[M.lang].title : M.t().auth.title; },
    render: function () {
      var t = M.t(), a = t.auth, r = R[M.lang];
      var field = function (id, label, type, ac, extra) {
        return '<div class="field">' + (extra || '<label for="' + id + '">' + label + '</label>') +
          '<input class="input" id="' + id + '" type="' + type + '" autocomplete="' + ac + '"' + (type === 'email' ? ' dir="ltr" placeholder="' + a.emailEx + '"' : '') + ' aria-describedby="' + id + '-err">' +
          '<p class="error" id="' + id + '-err" hidden></p></div>';
      };
      document.getElementById('main').innerHTML = '<div class="wrap page-head"><div class="g login-g">' +
        '<div class="g-start"><p class="t-stand">' + t.tagline + '</p><div style="margin-top:24px">' + M.dateline() + '</div></div>' +
        '<div class="g-main"><h1 class="t-h1">' + (reg ? r.title : a.title) + '</h1><p class="t-body muted" style="margin-top:12px">' + (reg ? r.description : a.description) + '</p>' +
        '<form class="form" id="f" novalidate>' +
        '<button class="btn btn-secondary btn-block" type="button" id="g-btn">' + a.google + '</button><p class="or">' + a.or + '</p>' +
        (reg ? field('f-name', r.name, 'text', 'name') : '') +
        field('f-email', a.email, 'email', 'email') +
        field('f-pass', a.password, 'password', reg ? 'new-password' : 'current-password', reg ? null : '<div class="label-row"><label for="f-pass">' + a.password + '</label><button class="btn-quiet link" type="button" id="forgot" style="background:none;border:0;cursor:pointer;font-size:13px">' + a.forgot + '</button></div>') +
        '<button class="btn btn-primary btn-block" type="submit">' + (reg ? r.submit : a.submit) + '</button></form>' +
        '<p class="after-form">' + (reg ? r.have + ' <a href="login.html">' + r.signIn + '</a>' : a.noAccount + ' <a href="login.html?register=1">' + a.create + '</a>') + '</p>' +
        (reg ? '<p class="t-meta">' + r.owner + '</p>' : '') +
        '<p class="t-meta mock-note">' + a.mock + '</p></div></div></div>';
      var f = document.getElementById('f');
      f.addEventListener('focusout', function (e) { if (e.target.classList.contains('input') && e.target.value) check(e.target); });
      f.addEventListener('input', function (e) { if (e.target.getAttribute('aria-invalid') === 'true') check(e.target); });
      f.addEventListener('submit', function (e) {
        e.preventDefault();
        var bad = [].slice.call(f.querySelectorAll('.input')).filter(function (el) { return !check(el); });
        if (bad.length) { bad[0].focus(); return; }
        M.store('masaha-c-signed', '1'); location.href = 'account.html';
      });
      document.getElementById('g-btn').addEventListener('click', function () { M.store('masaha-c-signed', '1'); location.href = 'account.html'; });
      var fg = document.getElementById('forgot');
      if (fg) fg.addEventListener('click', function () { M.dialog({ title: r.forgotTitle, text: r.forgotText, actions: [{ label: t.dir.close, kind: 'btn-primary' }] }); });
    }
  });
})();
