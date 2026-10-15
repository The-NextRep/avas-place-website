(function () {
  var btn = document.querySelector('.nav-toggle');
  var links = document.getElementById('nav-links');
  if (btn && links) {
    btn.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    links.addEventListener('click', function (e) {
      if (e.target.tagName === 'A' && links.classList.contains('open')) {
        links.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
        btn.setAttribute('aria-label', 'Open menu');
      }
    });
  }
  var hero = document.querySelector('.hero-marquee');
  var toggle = document.querySelector('.marquee-toggle');
  if (hero && toggle) {
    toggle.addEventListener('click', function () {
      var paused = hero.classList.toggle('paused');
      toggle.setAttribute('aria-pressed', paused ? 'true' : 'false');
      toggle.setAttribute('aria-label', paused ? 'Play moving images' : 'Pause moving images');
      toggle.querySelector('path').setAttribute('d', paused ? 'M8 5l11 7-11 7z' : 'M8 5v14M16 5v14');
    });
  }
  var rot = document.querySelector('.rot-word[data-words]');
  var calm = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (rot && !calm) {
    var list = rot.getAttribute('data-words').split('|'), k = 0;
    setInterval(function () {
      if (hero && hero.classList.contains('paused')) return;
      rot.classList.remove('is-on');
      setTimeout(function () {
        k = (k + 1) % list.length;
        rot.textContent = list[k];
        rot.classList.add('is-on');
      }, 350);
    }, 2600);
  }
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
(function () {
  // Certificate preview
  var n = document.getElementById('cert-name'), c = document.getElementById('cert-course'), d = document.getElementById('cert-date');
  if (n && c && d) {
    d.valueAsDate = new Date();
    var upd = function () {
      document.getElementById('out-name').textContent = n.value.trim() || 'Your Name';
      document.getElementById('out-course').textContent = c.value;
      var dt = d.value ? new Date(d.value + 'T12:00:00') : null;
      document.getElementById('out-date').textContent = dt ? dt.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }) : '';
    };
    [n, c, d].forEach(function (el) { el.addEventListener('input', upd); el.addEventListener('change', upd); });
    upd();
  }
  // School / Title I request form -> pre-filled email
  var f = document.getElementById('req-form');
  if (f) {
    var type = document.getElementById('r-type');
    var pick = function () {
      var h = location.hash;
      if (h === '#title-i-apply') type.value = 'Title I school application';
      if (h === '#sponsor') type.value = 'Sponsoring a Title I school';
    };
    pick(); window.addEventListener('hashchange', pick);
    f.addEventListener('submit', function (ev) {
      ev.preventDefault();
      if (!f.reportValidity()) return;
      var lines = [];
      Array.prototype.forEach.call(f.elements, function (el) {
        if (el.name && el.value.trim()) lines.push(el.name + ': ' + el.value.trim());
      });
      var subject = "Ava's Place: " + type.value + ' — ' + (document.getElementById('r-org').value || '');
      location.href = 'mailto:' + f.getAttribute('data-to') + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'));
    });
  }
})();
