// Language switcher: the site is built three times, into /en/, /zh/ and /de/.
// Switching keeps the current page and swaps the language segment of the URL.
(function () {
  var langs = [['en', 'English'], ['zh', '中文'], ['de', 'Deutsch']];
  function build() {
    var path = window.location.pathname;
    var m = path.match(/\/(en|zh|de)\//);
    if (!m) return;
    var box = document.createElement('div');
    box.className = 'lang-switch';
    langs.forEach(function (l) {
      var a = document.createElement('a');
      a.textContent = l[1];
      if (l[0] === m[1]) { a.className = 'active'; }
      a.href = path.replace('/' + m[1] + '/', '/' + l[0] + '/') + window.location.hash;
      box.appendChild(a);
    });
    var target = document.querySelector('.article-header-buttons') || document.querySelector('.header-article-items__end');
    if (target) { target.insertBefore(box, target.firstChild); } else { box.classList.add('floating'); document.body.appendChild(box); }
  }
  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', build); } else { build(); }
})();
