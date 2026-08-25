/* LUMEN BOTANICA — UI, scroll choreography, content rendering -------------- */
(function () {
  'use strict';

  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* ===================== shared templates ===================== */
  var I = {
    plus:  '<svg viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>',
    star:  '<svg viewBox="0 0 24 24"><path d="M12 2.6l2.9 5.9 6.5.9-4.7 4.6 1.1 6.4-5.8-3-5.8 3 1.1-6.4L2.6 9.4l6.5-.9z"/></svg>',
    heart: '<svg viewBox="0 0 24 24"><path d="M12 20.5l-7.4-7a4.6 4.6 0 0 1 6.5-6.5l.9.9.9-.9a4.6 4.6 0 1 1 6.5 6.5z"/></svg>',
    arrow: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="width:1em;height:1em"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
  };
  LB.icons = I;

  var LIGHT = { bright: 'Bright light', medium: 'Medium light', low: 'Low light' };
  var WATER = { low: 'Low water', medium: 'Weekly water', high: 'Thirsty' };
  var SIZE  = { S: 'Small', M: 'Medium', L: 'Large', XL: 'Extra large' };

  LB.cardHTML = function (p, i) {
    var badge = p.badge
      ? '<span class="tag ' + (p.badge === 'Sale' ? 'rose' : p.cat === 'rare' ? 'violet' : 'lime') + '">' + p.badge + '</span>'
      : '';
    return '' +
    '<article class="card reveal reveal-scale" style="--d:' + ((i % 4) * 70) + 'ms">' +
      '<div class="card-media">' +
        '<img src="' + p.img + '" alt="' + p.name + ' — ' + p.latin + '" loading="lazy" decoding="async" width="640" height="640">' +
        '<div class="card-badges">' + badge + '</div>' +
        '<button class="card-fav" aria-pressed="false" aria-label="Save ' + p.name + ' to wishlist" data-fav="' + p.id + '">' + I.heart + '</button>' +
      '</div>' +
      '<div class="card-body">' +
        '<div class="card-title"><h3>' + p.name + '</h3><em>' + p.latin + '</em></div>' +
        '<div class="card-meta">' +
          '<i>' + LIGHT[p.light] + '</i><i>' + WATER[p.water] + '</i>' +
          (p.petSafe ? '<i>Pet safe</i>' : '') +
        '</div>' +
        '<span class="rating">' + I.star + '<b style="color:var(--text);font-weight:600">' + p.rating.toFixed(1) + '</b> (' + p.reviews + ')</span>' +
        '<div class="card-foot">' +
          '<span class="price">' + LB.money(p.price) + (p.was ? '<s>' + LB.money(p.was) + '</s>' : '') + '</span>' +
          '<button class="add" data-add="' + p.id + '" aria-label="Add ' + p.name + ' to cart">' + I.plus + '<span>Add</span></button>' +
        '</div>' +
      '</div>' +
    '</article>';
  };

  /* ===================== header ===================== */
  function header() {
    var el = $('.header'); if (!el) return;
    var last = 0;
    function upd() {
      var y = window.scrollY;
      el.classList.toggle('stuck', y > 20);
      if (y > 520 && y > last + 6 && !document.body.classList.contains('no-scroll')) el.classList.add('hide');
      else if (y < last - 6 || y < 200) el.classList.remove('hide');
      last = y;
    }
    upd();
    window.addEventListener('scroll', upd, { passive: true });

    var burger = $('[data-burger]'), sheet = $('.mobile-nav');
    if (burger && sheet) {
      burger.addEventListener('click', function () {
        var open = sheet.classList.toggle('open');
        burger.setAttribute('aria-expanded', String(open));
        document.body.classList.toggle('no-scroll', open);
      });
      $$('a', sheet).forEach(function (a) {
        a.addEventListener('click', function () {
          sheet.classList.remove('open');
          burger.setAttribute('aria-expanded', 'false');
          document.body.classList.remove('no-scroll');
        });
      });
    }
  }

  /* ===================== scroll progress ===================== */
  function progress() {
    var bar = $('.progress'); if (!bar) return;
    var ticking = false;
    function upd() {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      var p = h > 0 ? Math.min(1, window.scrollY / h) : 0;
      bar.style.transform = 'scaleX(' + p + ')';
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(upd); }
    }, { passive: true });
    upd();
  }

  /* ===================== reveal on scroll ===================== */
  function reveals() {
    var items = $$('.reveal');
    if (reduced.matches || !('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('in'); });
      return;
    }
    // stagger children of [data-stagger]
    $$('[data-stagger]').forEach(function (group) {
      var step = parseInt(group.getAttribute('data-stagger'), 10) || 80;
      $$(':scope > .reveal', group).forEach(function (el, i) {
        if (!el.style.getPropertyValue('--d')) el.style.setProperty('--d', (i * step) + 'ms');
      });
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
    LB.observeReveals = function (scope) {
      $$('.reveal:not(.in)', scope || document).forEach(function (el) { io.observe(el); });
    };
  }

  /* ===================== parallax ===================== */
  function parallax() {
    var els = $$('[data-par]');
    if (!els.length || reduced.matches) return;
    var ticking = false;
    function upd() {
      var vh = window.innerHeight;
      els.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) return;
        var speed = parseFloat(el.getAttribute('data-par')) || 0.12;
        var mid = r.top + r.height / 2 - vh / 2;
        el.style.transform = 'translate3d(0,' + (-mid * speed).toFixed(2) + 'px,0)';
      });
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(upd); }
    }, { passive: true });
    window.addEventListener('resize', upd);
    upd();
  }

  /* ===================== number counters ===================== */
  function counters() {
    var els = $$('[data-count]');
    if (!els.length) return;
    if (reduced.matches || !('IntersectionObserver' in window)) {
      els.forEach(function (el) { el.textContent = fmtNum(el, +el.getAttribute('data-count')); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        run(e.target); io.unobserve(e.target);
      });
    }, { threshold: 0.4 });
    els.forEach(function (el) { io.observe(el); });

    function fmtNum(el, v) {
      var dec = +(el.getAttribute('data-dec') || 0);
      var s = dec ? v.toFixed(dec) : Math.round(v).toLocaleString('en-GB');
      return (el.getAttribute('data-pre') || '') + s + (el.getAttribute('data-suf') || '');
    }
    function run(el) {
      var target = +el.getAttribute('data-count');
      var dur = 1500, t0 = performance.now();
      (function tick(now) {
        var p = Math.min(1, (now - t0) / dur);
        var e = 1 - Math.pow(1 - p, 3);
        el.textContent = fmtNum(el, target * e);
        if (p < 1) requestAnimationFrame(tick);
      })(t0);
    }
  }

  /* ===================== pinned process section ===================== */
  function pinned() {
    var wrap = $('[data-pin]'); if (!wrap) return;
    var steps = $$('.step', wrap);
    var shots = $$('.pin-visual img', wrap);
    var hud   = $$('.pin-hud i', wrap);
    var cur = -1;
    function set(i) {
      if (i === cur) return;
      cur = i;
      steps.forEach(function (s, n) { s.classList.toggle('on', n === i); });
      shots.forEach(function (s, n) { s.classList.toggle('on', n === i); });
      hud.forEach(function (s, n) { s.classList.toggle('on', n === i); });
    }
    set(0);
    if (reduced.matches) { steps.forEach(function (s) { s.classList.add('on'); }); return; }

    var ticking = false;
    function upd() {
      var r = wrap.getBoundingClientRect();
      var span = r.height - window.innerHeight;
      if (span > 0) {
        var p = Math.min(0.999, Math.max(0, -r.top / span));
        set(Math.floor(p * steps.length));
      }
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(upd); }
    }, { passive: true });
    upd();
  }

  /* ===================== testimonials ===================== */
  function quotes() {
    var root = $('[data-quotes]'); if (!root) return;
    var track = $('.quote-track', root);
    var dots  = $('.dots', root) || $('.dots');
    if (!track || !dots) return;
    var i = 0, n = LB.quotes.length, timer;

    track.innerHTML = LB.quotes.map(function (q) {
      return '<div class="quote" role="group" aria-roledescription="slide" aria-label="Review by ' + q.name + '">' +
        '<blockquote>“' + q.text + '”</blockquote>' +
        '<div class="quote-by"><div class="avatar" aria-hidden="true">' + q.initials + '</div>' +
        '<div><b>' + q.name + '</b><span>' + q.role + '</span></div></div></div>';
    }).join('');

    dots.innerHTML = LB.quotes.map(function (q, k) {
      return '<button type="button" aria-label="Review ' + (k + 1) + ' of ' + n + '"' +
        (k === 0 ? ' aria-current="true"' : '') + ' data-go="' + k + '"></button>';
    }).join('');

    function go(k, user) {
      i = (k + n) % n;
      track.style.transform = 'translateX(' + (-i * 100) + '%)';
      $$('button', dots).forEach(function (b, m) {
        if (m === i) b.setAttribute('aria-current', 'true'); else b.removeAttribute('aria-current');
      });
      if (user) restart();
    }
    function restart() {
      clearInterval(timer);
      if (!reduced.matches) timer = setInterval(function () { go(i + 1); }, 7000);
    }

    dots.addEventListener('click', function (e) {
      var b = e.target.closest('[data-go]'); if (b) go(+b.getAttribute('data-go'), true);
    });
    $$('[data-quote-nav]').forEach(function (b) {
      b.addEventListener('click', function () { go(i + (+b.getAttribute('data-quote-nav')), true); });
    });
    root.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { go(i + 1, true); }
      if (e.key === 'ArrowLeft')  { go(i - 1, true); }
    });
    root.addEventListener('mouseenter', function () { clearInterval(timer); });
    root.addEventListener('mouseleave', restart);
    root.addEventListener('focusin', function () { clearInterval(timer); });

    // touch swipe
    var x0 = null;
    root.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    root.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 45) go(i + (dx < 0 ? 1 : -1), true);
      x0 = null;
    });

    go(0); restart();
  }

  /* ===================== hero particles ===================== */
  function particles() {
    var cv = $('#particles'); if (!cv || reduced.matches) return;
    var ctx = cv.getContext('2d');
    var dpr = Math.min(2, window.devicePixelRatio || 1);
    var w = 0, h = 0, bits = [], running = true, raf;
    var COLORS = ['rgba(124,255,196,', 'rgba(184,255,60,', 'rgba(42,224,208,'];

    function size() {
      w = cv.offsetWidth; h = cv.offsetHeight;
      cv.width = w * dpr; cv.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var target = Math.round(Math.min(42, Math.max(12, w / 36)));
      bits = [];
      for (var k = 0; k < target; k++) bits.push(spawn(true));
    }
    function spawn(any) {
      return {
        x: Math.random() * w,
        y: any ? Math.random() * h : h + 20,
        r: Math.random() * 1.9 + 0.5,
        v: Math.random() * 0.28 + 0.09,
        a: Math.random() * Math.PI * 2,
        sw: Math.random() * 0.55 + 0.18,
        o: Math.random() * 0.34 + 0.1,
        c: COLORS[(Math.random() * COLORS.length) | 0]
      };
    }
    function frame() {
      if (!running) return;
      ctx.clearRect(0, 0, w, h);
      for (var k = 0; k < bits.length; k++) {
        var b = bits[k];
        b.y -= b.v; b.a += 0.008;
        var x = b.x + Math.sin(b.a) * 14;
        ctx.beginPath();
        ctx.arc(x, b.y, b.r, 0, Math.PI * 2);
        ctx.fillStyle = b.c + b.o + ')';
        ctx.shadowBlur = 10; ctx.shadowColor = b.c + '0.7)';
        ctx.fill();
        if (b.y < -20) bits[k] = spawn(false);
      }
      ctx.shadowBlur = 0;
      raf = requestAnimationFrame(frame);
    }
    size(); frame();
    window.addEventListener('resize', debounce(size, 200));

    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (e) {
        running = e[0].isIntersecting;
        if (running) frame(); else cancelAnimationFrame(raf);
      }, { threshold: 0 }).observe(cv);
    }
    document.addEventListener('visibilitychange', function () {
      running = !document.hidden;
      if (running) frame(); else cancelAnimationFrame(raf);
    });
  }

  /* ===================== pointer spotlight ===================== */
  function spotlight() {
    if (window.matchMedia('(hover: none)').matches) return;
    document.addEventListener('pointermove', function (e) {
      var el = e.target.closest('.spot, .card, .coll, .guide');
      if (!el) return;
      var r = el.getBoundingClientRect();
      el.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100).toFixed(1) + '%');
      el.style.setProperty('--my', ((e.clientY - r.top) / r.height * 100).toFixed(1) + '%');
    }, { passive: true });
  }

  /* ===================== wishlist (local only) ===================== */
  function wishlist() {
    var KEY = 'lb.fav.v1', favs;
    try { favs = JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { favs = []; }
    function paint() {
      $$('[data-fav]').forEach(function (b) {
        b.setAttribute('aria-pressed', String(favs.indexOf(b.getAttribute('data-fav')) > -1));
      });
    }
    document.addEventListener('click', function (e) {
      var b = e.target.closest('[data-fav]'); if (!b) return;
      var id = b.getAttribute('data-fav'), k = favs.indexOf(id);
      if (k > -1) favs.splice(k, 1); else favs.push(id);
      try { localStorage.setItem(KEY, JSON.stringify(favs)); } catch (err) {}
      paint();
      LB.toast(k > -1 ? 'Removed from wishlist' : 'Saved to wishlist');
    });
    LB.paintFavs = paint;
    paint();
  }

  /* ===================== forms ===================== */
  function forms() {
    $$('[data-validate]').forEach(function (form) {
      form.setAttribute('novalidate', '');
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var ok = true;
        $$('input[required], textarea[required], select[required]', form).forEach(function (input) {
          var field = input.closest('.field') || input.parentElement;
          var msg = $('.msg', field);
          var bad = !input.checkValidity();
          field.classList.toggle('err', bad);
          if (msg) msg.textContent = bad ? (input.validationMessage || 'Please check this field') : '';
          if (bad && ok) { input.focus(); ok = false; }
        });
        if (!ok) return;
        var done = $('[data-form-done]', form);
        if (done) { done.hidden = false; }
        var action = form.getAttribute('data-validate');
        if (action === 'newsletter') {
          form.reset();
          LB.toast('Check your inbox to confirm');
        } else if (action === 'contact') {
          form.reset();
          LB.toast('Message sent — we reply within one working day');
        } else {
          form.dispatchEvent(new CustomEvent('form:valid', { bubbles: true }));
        }
      });
      $$('input, textarea', form).forEach(function (input) {
        input.addEventListener('input', function () {
          var field = input.closest('.field');
          if (field && field.classList.contains('err') && input.checkValidity()) {
            field.classList.remove('err');
            var m = $('.msg', field); if (m) m.textContent = '';
          }
        });
      });
    });
  }

  /* ===================== home page content ===================== */
  function home() {
    var cGrid = $('[data-collections]');
    if (cGrid) {
      var counts = {};
      LB.products.forEach(function (p) { counts[p.cat] = (counts[p.cat] || 0) + 1; });
      counts.statement = LB.products.filter(function (p) { return p.size === 'XL'; }).length;
      cGrid.innerHTML = LB.collections.map(function (c, i) {
        return '<article class="coll reveal" style="--d:' + (i * 70) + 'ms">' +
          '<img src="' + c.img + '" alt="' + c.title + ' collection" loading="lazy" decoding="async" width="760" height="560">' +
          '<span class="coll-count">' + (counts[c.id] || 4) + ' plants</span>' +
          '<div class="coll-body">' +
            '<h3>' + c.title + '</h3><p>' + c.blurb + '</p>' +
            '<span class="go">Browse collection ' + I.arrow + '</span>' +
          '</div>' +
          '<a class="stretch" href="shop.html?cat=' + c.id + '" aria-label="Browse the ' + c.title + ' collection"></a>' +
        '</article>';
      }).join('');
    }

    var fGrid = $('[data-featured]');
    if (fGrid) {
      var chips = $$('[data-feat-filter]');
      function paint(cat) {
        var list = LB.products.filter(function (p) { return cat === 'all' || p.cat === cat; })
                              .sort(function (a, b) { return b.pop - a.pop; })
                              .slice(0, 8);
        fGrid.innerHTML = list.map(LB.cardHTML).join('');
        $$('.reveal', fGrid).forEach(function (el) { el.classList.add('in'); });
        if (LB.paintFavs) LB.paintFavs();
      }
      chips.forEach(function (c) {
        c.addEventListener('click', function () {
          chips.forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
          c.setAttribute('aria-pressed', 'true');
          paint(c.getAttribute('data-feat-filter'));
        });
      });
      paint('all');
    }

    var gGrid = $('[data-guides]');
    if (gGrid) {
      gGrid.innerHTML = LB.guides.slice(0, 3).map(function (g, i) {
        return '<article class="guide reveal" style="--d:' + (i * 90) + 'ms">' +
          '<div class="guide-media"><img src="' + g.img + '" alt="" loading="lazy" decoding="async" width="760" height="460"></div>' +
          '<div class="guide-body">' +
            '<span class="tag">' + g.cat + '</span>' +
            '<h3>' + g.title + '</h3><p>' + g.excerpt + '</p>' +
            '<div class="guide-foot"><span>' + g.date + '</span><span>·</span><span>' + g.read + ' read</span></div>' +
          '</div>' +
          '<a class="stretch" href="#guides" aria-label="Read: ' + g.title + '" style="position:absolute;inset:0"></a>' +
        '</article>';
      }).join('');
      gGrid.style.position = 'relative';
      $$('.guide', gGrid).forEach(function (el) { el.style.position = 'relative'; });
    }

    var pSteps = $('[data-steps]');
    if (pSteps) {
      pSteps.innerHTML = LB.steps.map(function (s, i) {
        return '<div class="step' + (i === 0 ? ' on' : '') + '">' +
          '<span class="step-n">' + s.n + '</span>' +
          '<div><h3>' + s.title + '</h3><p>' + s.body + '</p></div></div>';
      }).join('');
      var vis = $('[data-step-visual]');
      if (vis) {
        vis.innerHTML =
          LB.steps.map(function (s, i) {
            return '<img src="' + s.img + '" alt="" class="' + (i === 0 ? 'on' : '') + '" loading="lazy" decoding="async">';
          }).join('') +
          '<div class="pin-hud" aria-hidden="true">' +
            LB.steps.map(function (s, i) { return '<i class="' + (i === 0 ? 'on' : '') + '"></i>'; }).join('') +
          '</div>';
      }
    }
  }

  /* ===================== misc ===================== */
  function debounce(fn, ms) {
    var t; return function () { clearTimeout(t); t = setTimeout(fn, ms); };
  }
  function year() {
    $$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
  }
  function toTop() {
    $$('[data-to-top]').forEach(function (b) {
      b.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: reduced.matches ? 'auto' : 'smooth' });
      });
    });
  }

  /* ===================== boot ===================== */
  function init() {
    header(); progress(); home();
    if (LB.initShop) LB.initShop();
    if (LB.initCheckout) LB.initCheckout();
    wishlist(); forms(); quotes(); pinned();
    reveals(); parallax(); counters(); particles(); spotlight();
    year(); toTop();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
