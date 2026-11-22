// Shop filter, search and product gallery. No tracking, no storage.
(function () {
  var grid = document.querySelector('[data-grid]');
  if (grid) {
    var cards = Array.prototype.slice.call(grid.querySelectorAll('.card'));
    var chips = Array.prototype.slice.call(document.querySelectorAll('.chip'));
    var input = document.querySelector('[data-search]');
    var count = document.querySelector('[data-count]');
    var empty = document.querySelector('[data-empty]');
    var filter = 'all';
    var apply = function () {
      var q = (input && input.value || '').trim().toLowerCase();
      var n = 0;
      cards.forEach(function (c) {
        var cats = c.getAttribute('data-cat').split(' ');
        var ok = (filter === 'all' || cats.indexOf(filter) > -1) && (!q || c.getAttribute('data-q').indexOf(q) > -1);
        c.hidden = !ok;
        if (ok) n++;
      });
      if (count) count.textContent = n;
      if (empty) empty.hidden = n > 0;
    };
    chips.forEach(function (b) {
      b.addEventListener('click', function () {
        filter = b.getAttribute('data-filter');
        chips.forEach(function (x) { var on = x === b; x.classList.toggle('is-on', on); x.setAttribute('aria-pressed', on); });
        apply();
      });
    });
    Array.prototype.slice.call(document.querySelectorAll('[data-pick]')).forEach(function (a) {
      a.addEventListener('click', function () {
        var chip = document.querySelector('.chip[data-filter="' + a.getAttribute('data-pick') + '"]');
        if (chip) chip.click();
      });
    });
    var go = document.querySelector('[data-go]');
    if (go) go.addEventListener('click', function () {
      var shop = document.getElementById('shop') || document.getElementById('sklep');
      if (shop) shop.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
    });
    if (input) {
      input.addEventListener('input', function () {
        apply();
      });
      input.addEventListener('keydown', function (ev) {
        if (ev.key === 'Enter') {
          ev.preventDefault();
          var shop = document.getElementById('shop') || document.getElementById('sklep');
          if (shop) shop.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
        }
      });
    }
  }
  var main = document.querySelector('.main-img');
  var thumbs = Array.prototype.slice.call(document.querySelectorAll('[data-swap]'));
  if (main && thumbs.length) {
    thumbs[0].setAttribute('aria-current', 'true');
    thumbs.forEach(function (a) {
      a.addEventListener('click', function (ev) {
        ev.preventDefault();
        var im = a.querySelector('img');
        main.src = a.getAttribute('data-swap');
        main.width = im.width ? im.naturalWidth || im.width : main.width;
        main.height = im.naturalHeight || main.height;
        main.alt = im.alt;
        thumbs.forEach(function (t) { t.removeAttribute('aria-current'); });
        a.setAttribute('aria-current', 'true');
      });
    });
  }
})();

// MailerLite sign-up form (free products). Posts to the consent form only if the separate box is ticked.
(function () {
  var f = document.querySelector('form.signup');
  if (!f) return;
  var pl = document.documentElement.lang === 'pl';
  var msg = f.querySelector('.su-msg');
  var btn = f.querySelector('button');
  f.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var email = f.email.value.trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      msg.textContent = pl ? 'Wpisz poprawny adres e-mail.' : 'Please enter a valid email address.';
      f.email.focus();
      return;
    }
    var url = f.consent.checked ? f.getAttribute('data-ml-consent') : f.getAttribute('data-ml-plain');
    var fd = new FormData();
    fd.append('fields[email]', email);
    fd.append('ml-submit', '1');
    fd.append('anticsrf', 'true');
    btn.disabled = true;
    msg.textContent = pl ? 'Wysyłanie…' : 'Sending…';
    fetch(url, { method: 'POST', body: fd })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (d && d.success) {
          f.querySelectorAll('input, label').forEach(function (el) { el.hidden = true; });
          btn.hidden = true;
          msg.textContent = pl ? 'Gotowe! Sprawdź skrzynkę i kliknij link potwierdzający (zajrzyj też do spamu).'
                               : 'Done! Check your inbox and click the confirmation link (check spam too).';
        } else {
          btn.disabled = false;
          msg.textContent = pl ? 'Nie udało się zapisać. Sprawdź adres i spróbuj ponownie.' : 'That didn’t work. Check the address and try again.';
        }
      })
      .catch(function () {
        btn.disabled = false;
        msg.textContent = pl ? 'Błąd połączenia. Spróbuj ponownie.' : 'Connection error. Please try again.';
      });
  });
})();
