/* إعدادات حسابي: the account tabs, then one settings form — label column (4/12), control column (8/12). */
(function () {
  'use strict';
  var pwOpen = false, name = A.USER.name, nameErr = false, rules = [false, false, false];

  function tabs(cur) {
    var w = A.t().acc;
    return '<nav class="tabs" aria-label="' + w.nav + '"><a href="' + A.href('favorites.html') + '"' + (cur === 'fav' ? ' aria-current="page"' : '') + '>' + w.favorites + '</a>' +
      '<a href="#" data-act="notbuilt">' + w.reports + '</a><a href="' + A.href('account.html') + '"' + (cur === 'set' ? ' aria-current="page"' : '') + '>' + w.settings + '</a></nav>';
  }
  A.accountTabs = tabs;

  function seg(name, label, opts, cur) {
    return '<div class="seg" role="radiogroup" aria-labelledby="' + name + '-l">' + opts.map(function (o) {
      return '<button type="button" role="radio" data-' + name + '="' + o[0] + '" aria-checked="' + (o[0] === cur) + '" tabindex="' + (o[0] === cur ? 0 : -1) + '"' + (o[2] ? ' lang="' + o[2] + '"' : '') + '>' + o[1] + '</button>';
    }).join('') + '</div>';
  }

  A.page({
    nav: '', signedIn: true,
    title: function () { return A.t().users.title; },
    render: function () {
      var w = A.t(), u = w.users;
      var pw = pwOpen
        ? '<div class="pwform"><div class="field"><label for="pwc">' + u.current + '</label><input class="input" id="pwc" type="password" autocomplete="current-password" dir="ltr"></div>' +
          '<div class="field"><label for="pwn">' + u.newPw + '</label><input class="input" id="pwn" type="password" autocomplete="new-password" dir="ltr" aria-describedby="pwr">' +
          '<ul class="rules" id="pwr" aria-label="' + u.rulesLabel + '">' + u.rules.map(function (r, i) { return '<li class="' + (rules[i] ? 'ok' : '') + '">' + A.icon(rules[i] ? 'check' : 'minus') + r + '<span class="sr">' + (rules[i] ? u.met : u.notMet) + '</span></li>'; }).join('') + '</ul></div>' +
          '<p class="help">' + u.othersLine + '</p><div style="display:flex;gap:8px;flex-wrap:wrap"><button type="button" class="btn btn-primary" data-pwsave>' + u.savePw + '</button><button type="button" class="btn btn-secondary" data-pwback>' + u.back + '</button></div></div>'
        : '<p>' + u.passwordLine + '</p><div><button type="button" class="btn btn-secondary" data-pwopen>' + u.change + '</button></div>';
      return '<div class="wrap page-head"><h1 class="t-h1">' + u.title + '</h1></div>' +
        '<div class="wrap">' + tabs('set') +
        '<form class="settings" novalidate onsubmit="return false">' +
        '<div class="srow"><div class="k"><label class="label" for="nm">' + u.name + '</label></div><div class="v"><div class="inline-save"><input class="input" id="nm" value="' + A.esc(name) + '" autocomplete="name"' + (nameErr ? ' aria-invalid="true" aria-describedby="nm-e"' : '') + '><button type="button" class="btn btn-primary" data-savename>' + u.save + '</button></div>' + (nameErr ? '<p class="err" id="nm-e">' + u.nameEmpty + '</p>' : '') + '</div></div>' +
        '<div class="srow"><div class="k"><span class="label">' + u.email + '</span></div><div class="v"><p class="w5">' + A.ltr(A.USER.email) + '</p><p class="help">' + u.emailNote + '</p></div></div>' +
        '<div class="srow"><div class="k"><span class="label" id="lang-l">' + u.language + '</span><span class="help">' + u.languageHelper + '</span></div><div class="v">' + seg('lang', u.language, [['ar', 'العربية', 'ar'], ['en', 'English', 'en']], A.state.lang) + '</div></div>' +
        '<div class="srow"><div class="k"><span class="label" id="theme-l">' + u.theme + '</span><span class="help">' + u.themeHelper + ' · ' + u.prefsDescription + '</span></div><div class="v">' + seg('theme', u.theme, [['light', u.themes.light], ['dark', u.themes.dark], ['system', u.themes.system]], A.state.themePref) + '</div></div>' +
        '<div class="srow"><div class="k"><span class="label">' + u.password + '</span><span class="help">' + u.signInDescription + '</span></div><div class="v">' + pw + '</div></div>' +
        '</form></div>';
    },
    mount: function () {
      var u = A.t().users;
      function radios(sel, fn) {
        var rs = Array.prototype.slice.call(document.querySelectorAll('[' + sel + ']'));
        rs.forEach(function (b, i) {
          b.onclick = function () { fn(b.getAttribute(sel)); };
          b.onkeydown = function (e) { var rtl = A.state.lang === 'ar', d = 0; if (e.key === 'ArrowRight') d = rtl ? -1 : 1; else if (e.key === 'ArrowLeft') d = rtl ? 1 : -1; else return; e.preventDefault(); rs[(i + d + rs.length) % rs.length].click(); };
        });
      }
      radios('data-lang', function (l) { if (l !== A.state.lang) { A.setLang(l); var b = document.querySelector('[data-lang="' + l + '"]'); if (b) b.focus(); } });
      radios('data-theme', function (t) { A.setTheme(t); var b = document.querySelector('[data-theme="' + t + '"]'); if (b) b.focus(); });
      document.querySelector('[data-savename]').onclick = function () {
        var v = document.getElementById('nm').value.trim();
        nameErr = !v; if (!nameErr) name = v;
        A.render(); if (nameErr) document.getElementById('nm').focus(); else { document.querySelector('[data-savename]').focus(); A.toast(u.saved); }
      };
      var po = document.querySelector('[data-pwopen]'); if (po) po.onclick = function () { pwOpen = true; A.render(); document.getElementById('pwc').focus(); };
      var pb = document.querySelector('[data-pwback]'); if (pb) pb.onclick = function () { pwOpen = false; rules = [false, false, false]; A.render(); document.querySelector('[data-pwopen]').focus(); };
      var ps = document.querySelector('[data-pwsave]'); if (ps) ps.onclick = function () { if (rules.every(Boolean) && document.getElementById('pwc').value) { pwOpen = false; rules = [false, false, false]; A.render(); document.querySelector('[data-pwopen]').focus(); A.toast(u.pwSaved); } else document.getElementById(document.getElementById('pwc').value ? 'pwn' : 'pwc').focus(); };
      var pn = document.getElementById('pwn');
      if (pn) pn.oninput = function () {
        var v = pn.value; rules = [v.length >= 8, /\p{L}/u.test(v), /\d/.test(v)];
        document.querySelectorAll('#pwr li').forEach(function (li, i) { li.className = rules[i] ? 'ok' : ''; li.innerHTML = A.icon(rules[i] ? 'check' : 'minus') + u.rules[i] + '<span class="sr">' + (rules[i] ? u.met : u.notMet) + '</span>'; });
      };
    }
  });
})();
