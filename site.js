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
  var words = document.querySelectorAll('.rot-word');
  var calm = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (words.length > 1 && !calm) {
    var i = 0;
    setInterval(function () {
      if (hero && hero.classList.contains('paused')) return;
      words[i].classList.remove('is-on');
      i = (i + 1) % words.length;
      words[i].classList.add('is-on');
    }, 2400);
  }
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
