(function () {
  'use strict';

  /* ── 1. AOS init ── */
  AOS.init({
    duration: 750,
    easing: 'ease-out-cubic',
    once: true,
    offset: 60
  });

  /* ── 2. Preloader ── */
  (function preloader() {
    var loader  = document.querySelector('.loader');
    var overlay = document.getElementById('overlayer');

    function fadeOut(el) {
      if (!el) return;
      el.style.opacity = '1';
      (function fade() {
        var op = parseFloat(el.style.opacity);
        if (op <= 0) {
          el.style.display = 'none';
        } else {
          el.style.opacity = (op - 0.08).toString();
          requestAnimationFrame(fade);
        }
      })();
    }

    function hide() {
      setTimeout(function () {
        fadeOut(loader);
        fadeOut(overlay);
      }, 600);
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', hide);
    } else {
      hide();
    }
  })();

  /* ── 3. Custom Cursor ── */
  (function initCursor() {
    var dot  = document.getElementById('cursor-dot');
    var ring = document.getElementById('cursor-ring');
    if (!dot || !ring) return;
    if (!window.matchMedia('(pointer: fine)').matches) return;

    var mx = -100, my = -100;
    var rx = -100, ry = -100;

    document.addEventListener('mousemove', function (e) {
      mx = e.clientX;
      my = e.clientY;
      dot.style.left = mx + 'px';
      dot.style.top  = my + 'px';
    });

    (function animRing() {
      rx += (mx - rx) * 0.12;
      ry += (my - ry) * 0.12;
      ring.style.left = rx + 'px';
      ring.style.top  = ry + 'px';
      requestAnimationFrame(animRing);
    })();

    /* Enlarge ring on hover of interactive elements */
    document.querySelectorAll('a, button, [role="button"], input[type="submit"], label, select').forEach(function (el) {
      el.addEventListener('mouseenter', function () { ring.classList.add('hover'); });
      el.addEventListener('mouseleave', function () { ring.classList.remove('hover'); });
    });
  })();

  /* ── 4. Nav scroll class ── */
  (function initNavScroll() {
    var nav = document.getElementById('site-nav');
    if (!nav) return;

    function toggle() {
      if (window.scrollY > 60) {
        nav.classList.add('nav-scrolled');
      } else {
        nav.classList.remove('nav-scrolled');
      }
    }

    window.addEventListener('scroll', toggle, { passive: true });
    toggle();
  })();

  /* ── 5. TinySlider ── */
  (function initSliders() {
    /* Hero fullscreen slider (index.html) */
    var heroBgEl = document.getElementById('hero-bg-slider');
    if (heroBgEl) {
      var heroSlider = tns({
        container: '#hero-bg-slider',
        items: 1,
        mode: 'carousel',
        speed: 1400,
        autoplay: true,
        autoplayTimeout: 7500,
        autoplayButtonOutput: false,
        controls: false,
        nav: false,
        loop: true,
        preventScrollOnTouch: 'auto'
      });

      /* Reset Ken Burns on each new slide */
      if (heroSlider) {
        heroSlider.events.on('transitionEnd', function (info) {
          var slides = document.querySelectorAll('.hero-bg-slide');
          slides.forEach(function (s) {
            s.style.animation = 'none';
            s.offsetHeight; // force reflow
          });
          var active = info.slideItems[info.index];
          if (active) {
            active.style.animation = 'ken-burns 9s ease-out forwards';
          }
        });
      }
    }

    /* Image property slider */
    if (document.querySelector('.img-property-slide')) {
      tns({
        container: '.img-property-slide',
        mode: 'carousel',
        speed: 700,
        items: 1,
        autoplay: true,
        controls: false,
        nav: true,
        autoplayButtonOutput: false
      });
    }

    /* Property slider (3 items) */
    if (document.querySelector('.property-slider')) {
      tns({
        container: '.property-slider',
        mode: 'carousel',
        speed: 700,
        items: 3,
        autoplay: true,
        autoplayButtonOutput: false,
        controlsContainer: '#property-nav',
        responsive: { 0: { items: 1 }, 700: { items: 2 }, 900: { items: 3 } }
      });
    }

    /* Testimonial center slider */
    if (document.getElementById('testimonial-center')) {
      tns({
        container: '#testimonial-center',
        items: 1,
        mode: 'carousel',
        slideBy: 1,
        nav: true,
        controls: true,
        autoplay: true,
        autoplayTimeout: 5500,
        autoplayButtonOutput: false,
        gutter: 50,
        edgePadding: 0,
        center: true,
        controlsContainer: '#testimonial-nav',
        autoplayHoverPause: true,
        loop: true,
        swipeAngle: false,
        speed: 700,
        responsive: {
          350:  { gutter: 10,  items: 1 },
          500:  { gutter: 20,  items: 1 },
          700:  { gutter: 50,  edgePadding: 20, items: 2 },
          1000: { gutter: 50,  edgePadding: 50, items: 2 }
        }
      });
    }
  })();

  /* ── 6. GLightbox ── */
  GLightbox({ selector: '.glightbox' });

  /* ── 7. GSAP animations ── */
  (function initGSAP() {
    if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') return;
    gsap.registerPlugin(ScrollTrigger);

    /* Hero headline stagger (index.html) */
    var heroSpans = document.querySelectorAll('.hero-content .display-heading span');
    if (heroSpans.length) {
      gsap.fromTo(heroSpans,
        { opacity: 0, y: 70 },
        { opacity: 1, y: 0, duration: 1.1, ease: 'power3.out', stagger: 0.18, delay: 0.7 }
      );
    }

    var heroEyebrow = document.querySelector('.hero-content .eyebrow');
    if (heroEyebrow) {
      gsap.fromTo(heroEyebrow,
        { opacity: 0, y: 20 },
        { opacity: 1, y: 0, duration: 0.8, ease: 'power2.out', delay: 0.5 }
      );
    }

    var heroRule = document.querySelector('.hero-content .hero-rule');
    if (heroRule) {
      gsap.fromTo(heroRule,
        { scaleX: 0, transformOrigin: 'left' },
        { scaleX: 1, duration: 0.7, ease: 'power2.out', delay: 1.4 }
      );
    }

    var heroDesc = document.querySelector('.hero-content .hero-desc');
    if (heroDesc) {
      gsap.fromTo(heroDesc,
        { opacity: 0, y: 24 },
        { opacity: 1, y: 0, duration: 0.8, ease: 'power2.out', delay: 1.6 }
      );
    }

    var heroCta = document.querySelector('.hero-content .hero-cta');
    if (heroCta) {
      gsap.fromTo(heroCta,
        { opacity: 0, y: 20 },
        { opacity: 1, y: 0, duration: 0.7, ease: 'power2.out', delay: 1.9 }
      );
    }

    /* [data-reveal] scroll reveal */
    gsap.utils.toArray('[data-reveal]').forEach(function (el) {
      gsap.fromTo(el,
        { opacity: 0, y: 48 },
        {
          opacity: 1, y: 0,
          duration: 0.9,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: el,
            start: 'top 90%',
            toggleActions: 'play none none none'
          }
        }
      );
    });

    /* Parallax images */
    gsap.utils.toArray('[data-parallax]').forEach(function (el) {
      gsap.to(el, {
        y: '-18%',
        ease: 'none',
        scrollTrigger: {
          trigger: el.closest('.hero-2') || el.parentElement,
          start: 'top top',
          end: 'bottom top',
          scrub: true
        }
      });
    });

    /* Project grid wipe-reveal (clip-path) */
    gsap.utils.toArray('.single-portfolio').forEach(function (el) {
      gsap.fromTo(el,
        { clipPath: 'inset(100% 0 0 0)' },
        {
          clipPath: 'inset(0% 0 0 0)',
          duration: 0.85,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: el,
            start: 'top 90%',
            toggleActions: 'play none none none'
          }
        }
      );
    });

    /* Process line draw */
    var processRow = document.querySelector('.process-steps-row');
    var processLine = document.querySelector('.process-line-draw');
    if (processRow && processLine) {
      gsap.fromTo(processLine,
        { width: '0%' },
        {
          width: '100%',
          ease: 'none',
          scrollTrigger: {
            trigger: processRow,
            start: 'top 70%',
            end: 'top 20%',
            scrub: 0.8
          }
        }
      );
    }
  })();

  /* ── 8. Stats counter ── */
  (function initStats() {
    var statsAnimated = false;
    var statsBar = document.querySelector('.stats-bar');

    function animateStats() {
      if (statsAnimated) return;
      statsAnimated = true;
      document.querySelectorAll('.stat-number[data-count]').forEach(function (el) {
        var target    = parseInt(el.getAttribute('data-count'), 10);
        var duration  = 1800;
        var fps       = 60;
        var total     = Math.round(duration / (1000 / fps));
        var frame     = 0;
        var hasSuffix = target === 100 ? false : true;

        var timer = setInterval(function () {
          frame++;
          var progress = frame / total;
          var eased    = progress * (2 - progress);
          var current  = Math.round(target * eased);
          el.textContent = current + (hasSuffix ? '+' : '');
          if (frame >= total) {
            el.textContent = target + (hasSuffix ? '+' : '');
            clearInterval(timer);
          }
        }, 1000 / fps);
      });
    }

    if (statsBar) {
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (entries, obs) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) { animateStats(); obs.disconnect(); }
          });
        }, { threshold: 0.3 }).observe(statsBar);
      } else {
        animateStats();
      }
    }
  })();

  /* ── 9. Project filter ── */
  document.querySelectorAll('.filter-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      document.querySelectorAll('.filter-btn').forEach(function (b) { b.classList.remove('active'); });
      this.classList.add('active');
      var filter = this.dataset.filter;
      document.querySelectorAll('#projects-grid [data-category]').forEach(function (item) {
        item.style.display = (filter === 'all' || item.dataset.category === filter) ? '' : 'none';
      });
    });
  });

})();
