/* «إعدادات حسابي» — a typeset form: each setting's label at the start, its control beside it, rules between. */
(function () {
  var pwOpen = false;
  M.boot({
    id: 'account', signedIn: true,
    title: function () { return M.t().acc.title; },
    render: function () {
      var t = M.t(), a = t.acc, u = M.user, nm = M.lang === 'ar' ? u.name : u.nameEn;
      var seg = function (name, opts, cur) { return '<div class="seg" role="radiogroup" aria-labelledby="' + name + '-k" aria-describedby="' + name + '-h">' + opts.map(function (o) { return '<label' + (o[2] ? ' lang="' + o[2] + '"' : '') + '><input type="radio" name="' + name + '" value="' + o[0] + '"' + (cur === o[0] ? ' checked' : '') + '><span>' + o[1] + '</span></label>'; }).join('') + '</div>'; };
      var pw = pwOpen
        ? '<div class="pw-form"><div class="field"><label for="pw-cur">' + a.current + '</label><input class="input" id="pw-cur" type="password" autocomplete="current-password"></div>' +
          '<div class="field"><label for="pw-new">' + a.newPass + '</label><input class="input" id="pw-new" type="password" autocomplete="new-password"></div>' +
          '<p class="help">' + a.othersLine + '</p><div class="save-row" style="padding-top:0"><button class="btn btn-primary" type="button" id="pw-save">' + a.savePass + '</button><button class="btn btn-quiet" type="button" id="pw-back">' + a.back + '</button></div></div>'
        : '<p class="line">' + a.passwordLine + '</p><button class="btn btn-secondary" type="button" id="pw-change" aria-expanded="false">' + a.change + '</button>';
      document.getElementById('main').innerHTML = '<div class="wrap">' +
        '<header class="page-head g"><div class="g-start"></div><div class="g-main"><h1 class="t-h1">' + a.title + '</h1></div></header>' +
        '<div class="g" style="margin-top:40px"><div class="g-start">' + M.accountNav('settings') + '</div><div class="g-main settings">' +
        '<section aria-labelledby="pf-h"><h2 id="pf-h">' + a.profile + '</h2><form id="pf" novalidate>' +
        '<div class="srow"><label class="k" for="pf-name">' + a.name + '</label><div class="v"><input class="input" id="pf-name" value="' + M.esc(nm) + '" autocomplete="name" aria-describedby="pf-name-err"><p class="error" id="pf-name-err" hidden>' + a.nameErr + '</p></div></div>' +
        '<div class="srow"><p class="k">' + a.email + '</p><div class="v"><p class="line">' + M.ltr(u.email) + '</p><p class="help">' + a.emailNote + '</p></div></div>' +
        '<div class="save-row"><button class="btn btn-primary" type="submit">' + a.save + '</button></div></form></section>' +
        '<section aria-labelledby="pr-h"><h2 id="pr-h">' + a.prefs + '</h2><p class="t-meta sec-note">' + a.prefsNote + '</p>' +
        '<div class="srow"><p class="k" id="lang-k">' + a.language + '</p><div class="v">' + seg('lang', [['ar', 'العربية', 'ar'], ['en', 'English', 'en']], M.lang) + '<p class="help" id="lang-h">' + a.languageHelper + '</p></div></div>' +
        '<div class="srow"><p class="k" id="theme-k">' + a.theme + '</p><div class="v">' + seg('theme', [['light', a.themes.light], ['dark', a.themes.dark], ['system', a.themes.system]], M.themePref) + '<p class="help" id="theme-h">' + a.themeHelper + '</p></div></div></section>' +
        '<section aria-labelledby="si-h"><h2 id="si-h">' + a.signIn + '</h2><p class="t-meta sec-note">' + a.signInNote + '</p>' +
        '<div class="srow"><p class="k">' + a.google + '</p><div class="v"><p class="line">' + a.googleLine(M.ltr(u.email)) + '</p><p class="linked">' + M.icon('check') + a.linked + '</p></div></div>' +
        '<div class="srow"><p class="k">' + a.password + '</p><div class="v" id="pw-slot">' + pw + '</div></div></section>' +
        '</div></div></div>';
      document.getElementById('pf').addEventListener('submit', function (e) {
        e.preventDefault(); var i = document.getElementById('pf-name'), ok = !!i.value.trim();
        document.getElementById('pf-name-err').hidden = ok; i.setAttribute('aria-invalid', String(!ok));
        if (ok) M.toast(a.saved); else i.focus();
      });
      document.getElementById('main').addEventListener('change', function (e) {
        if (e.target.name === 'lang') { M.setLang(e.target.value); var r = document.querySelector('input[name=lang]:checked'); if (r) r.focus(); }
        if (e.target.name === 'theme') { M.setTheme(e.target.value); var r2 = document.querySelector('input[name=theme]:checked'); if (r2) r2.focus(); }
      });
      var slot = document.getElementById('pw-slot');
      slot.addEventListener('click', function (e) {
        if (e.target.closest('#pw-change')) { pwOpen = true; M.page.render(); document.getElementById('pw-cur').focus(); }
        else if (e.target.closest('#pw-back')) { pwOpen = false; M.page.render(); document.getElementById('pw-change').focus(); }
        else if (e.target.closest('#pw-save')) { pwOpen = false; M.page.render(); M.toast(M.lang === 'ar' ? 'تم تغيير كلمة المرور، وسُجّل خروجك من الأجهزة الأخرى' : 'Password changed, and you were signed out on your other devices'); document.getElementById('pw-change').focus(); }
      });
    }
  });
})();
