// Black Friday 2026 banner (EN pages only). Shows automatically 27 Nov 07:00 – 1 Dec 08:59 Warsaw time.
(function () {
  var start = Date.parse('2026-11-27T06:00:00Z'), end = Date.parse('2026-12-01T07:59:00Z'), now = Date.now();
  if (now < start || now >= end) return;
  function show() {
    if (document.querySelector('.bf-banner')) return;
    var d = document.createElement('div');
    d.className = 'bf-banner';
    d.setAttribute('role', 'region');
    d.setAttribute('aria-label', 'Black Friday offer');
    d.innerHTML = '<strong>Black Friday, Nov 27–30:</strong> 30% off the ' +
      '<a href="/products/before-after-legacy-bundle/?utm_source=site&amp;utm_medium=banner&amp;utm_campaign=bf2026">Before &amp; After Legacy Bundle</a> ' +
      '(US and Canada). $22.40 with code <strong>BF30</strong> at checkout (regular $32). ' +
      '<span class="bf-note">Informational and organizational only, not legal, tax or financial advice.</span>';
    document.body.insertBefore(d, document.body.firstChild);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', show); else show();
})();
