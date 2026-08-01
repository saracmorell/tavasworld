/* ============================================================
   TAVAS WORLD — MASTER NAVIGATION BEHAVIOUR
   Single source of truth for header behaviour on every page:
   mobile menu toggle, scroll border, and active-page state.
   Edit here once; every page updates.
   ============================================================ */

(function () {
  'use strict';

  var header = document.getElementById('header');
  var navbar = document.getElementById('navbar');
  var toggle = document.getElementById('mobileToggle');

  /* Mobile menu open/close */
  if (toggle && navbar) {
    toggle.addEventListener('click', function () {
      navbar.classList.toggle('show');
    });

    /* Close the menu after tapping a link */
    navbar.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        navbar.classList.remove('show');
      }
    });
  }

  /* Border deepens once the page scrolls */
  if (header) {
    var onScroll = function () {
      header.style.borderBottomColor =
        window.scrollY > 40 ? 'rgba(212,168,83,0.2)' : 'rgba(212,168,83,0.12)';
    };
    window.addEventListener('scroll', onScroll);
    onScroll();
  }

  /* Mark the current page's link as active */
  if (navbar) {
    var current = (window.location.pathname.split('/').pop() || 'index.html').toLowerCase();
    var links = navbar.querySelectorAll('a[href]');

    for (var i = 0; i < links.length; i++) {
      var href = links[i].getAttribute('href');
      if (!href || href.charAt(0) === '#') { continue; }
      if (/^([a-z]+:)?\/\//i.test(href)) { continue; }
      if (href.split('/').pop().toLowerCase() === current) {
        links[i].classList.add('active');
      }
    }
  }
})();
