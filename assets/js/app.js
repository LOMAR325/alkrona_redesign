/* ==========================================================================
   Alkrona — каталог, фильтры, заявка, галерея
   Без зависимостей и сборки. Данные каталога — в catalog-data.js
   ========================================================================== */
(function () {
  'use strict';

  var ALK = window.ALK = window.ALK || {};
  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* ---------- справочники ---------- */
  var CATS = {
    'hvojnye-derevya-i-kustarniki': { label: 'Хвойные', short: 'Хвойные' },
    'listvennye-kustarniki':        { label: 'Лиственные кустарники', short: 'Лиственные' }
  };
  ALK.CATS = CATS;

  var SIZES = [
    { id: 'xs', label: 'До 30 см',      test: function (p) { return p.hMax <= 30; } },
    { id: 's',  label: '30–60 см',      test: function (p) { return p.hMax > 30 && p.hMin <= 60; } },
    { id: 'm',  label: '60–100 см',     test: function (p) { return p.hMax > 60 && p.hMin <= 100; } },
    { id: 'l',  label: 'Более 100 см',  test: function (p) { return p.hMax > 100; } }
  ];
  var PRICES = [
    { id: 'any',     label: 'Любая',            test: function () { return true; } },
    { id: 'lt15',    label: 'До 15 руб',        test: function (p) { return p.price > 0 && p.price < 15; } },
    { id: '15-25',   label: '15–25 руб',        test: function (p) { return p.price >= 15 && p.price <= 25; } },
    { id: 'gt25',    label: 'Дороже 25 руб',    test: function (p) { return p.price > 25; } },
    { id: 'request', label: 'Цена по запросу',  test: function (p) { return !p.price; } }
  ];

  function money(v) {
    return v.toFixed(2).replace('.', ',') + ' руб';
  }
  ALK.money = money;

  function priceHTML(p) {
    if (!p.price) return '<span class="price request">Цена по запросу</span>';
    if (p.priceMax && p.priceMax > p.price) {
      return '<span class="price">от ' + money(p.price) + '<small>до ' + money(p.priceMax) + '</small></span>';
    }
    return '<span class="price">' + money(p.price) + '</span>';
  }

  function img(name, size) { return 'assets/img/plants/' + name + '-' + size + '.webp'; }

  /* ---------- иконки ---------- */
  var A = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"';
  function ic(d, w) { return '<svg ' + A + ' stroke-width="' + (w || 1.4) + '" aria-hidden="true">' + d + '</svg>'; }

  var I = {
    plus:  ic('<path d="M12 5.4v13.2M5.4 12h13.2"/>', 1.7),
    check: ic('<path d="M4.4 12.6 9.6 18 20 6.4"/>', 2),
    close: ic('<path d="M6 6l12 12M18 6 6 18"/>', 1.6),
    zoom:  ic('<circle cx="11" cy="11" r="7"/><path d="m20 20-3.4-3.4M11 8.4v5.2M8.4 11h5.2"/>', 1.5),
    bag:   ic('<path d="M6.2 7.6h11.6L19 20.4H5z"/><path d="M9.2 7.6V6.4a2.8 2.8 0 0 1 5.6 0v1.2"/>', 1.3),
    arrow: ic('<path d="M5 12h14M13 6l6 6-6 6"/>', 1.8),
    // мерки растения — свои, а не дежурные значки
    pot:   ic('<path d="M5.5 13h13l-1.4 6.6a1.6 1.6 0 0 1-1.6 1.3H8.5a1.6 1.6 0 0 1-1.6-1.3z"/>' +
              '<path d="M4.4 10.4h15.2v2.6H4.4z"/>', 1.4),
    ruler: ic('<path d="M12 4v16"/><path d="M8.4 4h7.2M8.4 20h7.2"/><path d="M9.6 8.4 12 6l2.4 2.4M9.6 15.6 12 18l2.4-2.4"/>', 1.4),
    paw:   ic('<path d="M12 21c-3.4 0-5.6-2-5.6-4.2 0-2 1.8-3 3-4.4 1-1.2 1.3-2.8 2.6-2.8s1.6 1.6 2.6 2.8c1.2 1.4 3 2.4 3 4.4C17.6 19 15.4 21 12 21z"/>', 1.3)
  };
  ALK.I = I;

  /* ---------- карточка товара ---------- */
  function cardHTML(p) {
    var tags = '';
    if (!p.inStock) tags += '<span class="pill pill-out">Под заказ</span>';
    else tags += '<span class="pill pill-stock"><span class="dot"></span>В наличии</span>';
    if (p.cat === 'hvojnye-derevya-i-kustarniki') tags += '<span class="pill pill-sand">Хвойное</span>';

    var specs = '';
    if (p.pots.length)    specs += '<i>' + I.pot + 'Горшок ' + p.pots.join(' / ') + '</i>';
    if (p.heights.length) specs += '<i>' + I.ruler + p.heights.join(' / ') + ' см</i>';

    return '' +
    '<article class="card rise">' +
      '<div class="card-media">' +
        '<img src="' + img(p.img[0], 400) + '" alt="' + p.name + '" width="400" height="400" loading="lazy" decoding="async">' +
        '<div class="card-tags">' + tags + '</div>' +
        '<button class="card-zoom" data-open="' + p.id + '" aria-label="Подробнее: ' + p.name + '">' + I.zoom + '</button>' +
      '</div>' +
      '<div class="card-body">' +
        '<div class="card-name"><h3>' + p.name + '</h3>' + (p.latin ? '<em>' + p.latin + '</em>' : '') + '</div>' +
        '<div class="card-specs">' + specs + '</div>' +
        '<div class="card-foot">' + priceHTML(p) +
          '<button class="card-add" data-add="' + p.id + '" aria-label="Добавить «' + p.name + '» в заявку">' +
            I.plus + '<span>В заявку</span></button>' +
        '</div>' +
      '</div>' +
    '</article>';
  }
  ALK.cardHTML = cardHTML;

  function byId(id) {
    for (var i = 0; i < ALK.products.length; i++) if (ALK.products[i].id === id) return ALK.products[i];
    return null;
  }
  ALK.byId = byId;

  /* ======================= шапка и меню ======================= */
  function header() {
    var h = $('.header');
    if (h) {
      var upd = function () { h.classList.toggle('stuck', window.scrollY > 8); };
      upd(); window.addEventListener('scroll', upd, { passive: true });
    }
    var sheet = $('.mobile-nav'), burger = $('[data-burger]');
    if (!sheet || !burger) return;
    var scrim = $('[data-scrim]');
    function close() {
      sheet.classList.remove('open');
      burger.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('lock');
      if (scrim && !$('.drawer.open') && !$('.filters.open')) scrim.classList.remove('open');
    }
    burger.addEventListener('click', function () {
      var open = !sheet.classList.contains('open');
      sheet.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', String(open));
      document.body.classList.toggle('lock', open);
      if (scrim) scrim.classList.toggle('open', open);
      if (open) { var f = sheet.querySelector('a, button'); if (f) f.focus(); }
    });
    $$('a, [data-close-nav]', sheet).forEach(function (a) { a.addEventListener('click', close); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && sheet.classList.contains('open')) close();
    });
    if (scrim) scrim.addEventListener('click', close);
  }

  /* ======================= появление ======================= */
  function reveal() {
    var els = $$('.rise');
    if (reduced.matches || !('IntersectionObserver' in window)) {
      els.forEach(function (e) { e.classList.add('in'); }); return;
    }
    $$('[data-stagger]').forEach(function (g) {
      var step = +g.getAttribute('data-stagger') || 70;
      $$(':scope > .rise', g).forEach(function (e, i) {
        if (!e.style.getPropertyValue('--d')) e.style.setProperty('--d', Math.min(i, 6) * step + 'ms');
      });
    });
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -6% 0px', threshold: .06 });
    els.forEach(function (e) { io.observe(e); });
    ALK.watch = function (scope) { $$('.rise:not(.in)', scope || document).forEach(function (e) { io.observe(e); }); };
  }

  /* ======================= заявка ======================= */
  var KEY = 'alk.request.v1';
  var Req = ALK.request = {
    lines: [],
    load: function () {
      try {
        var r = JSON.parse(localStorage.getItem(KEY));
        this.lines = Array.isArray(r) ? r.filter(function (l) { return byId(l.id); }) : [];
      } catch (e) { this.lines = []; }
    },
    save: function () {
      try { localStorage.setItem(KEY, JSON.stringify(this.lines)); } catch (e) {}
      paintReq();
    },
    count: function () { return this.lines.reduce(function (n, l) { return n + l.qty; }, 0); },
    add: function (id, qty) {
      var line = null;
      this.lines.forEach(function (l) { if (l.id === id) line = l; });
      if (line) line.qty = Math.min(999, line.qty + (qty || 1));
      else this.lines.push({ id: id, qty: qty || 1 });
      this.save();
      toast('«' + byId(id).name + '» — в заявке');
    },
    setQty: function (id, q) {
      this.lines = this.lines.filter(function (l) {
        if (l.id !== id) return true;
        l.qty = Math.max(0, Math.min(999, q));
        return l.qty > 0;
      });
      this.save();
    },
    remove: function (id) { this.lines = this.lines.filter(function (l) { return l.id !== id; }); this.save(); },
    clear: function () { this.lines = []; this.save(); },
    text: function () {
      return this.lines.map(function (l) {
        var p = byId(l.id);
        return '• ' + p.name + (p.sku ? ' (' + p.sku + ')' : '') + ' — ' + l.qty + ' шт';
      }).join('\n');
    }
  };

  var drawer, scrimEl;

  function paintReq() {
    var n = Req.count();
    $$('[data-req-count]').forEach(function (b) {
      b.textContent = n; b.classList.toggle('on', n > 0);
    });
    var body = $('[data-req-body]'), foot = $('[data-req-foot]');
    if (!body) return;

    if (!Req.lines.length) {
      body.innerHTML = '<div class="drawer-empty">' + I.bag +
        '<div><b style="display:block;color:var(--ink);font-family:var(--font-display);font-size:1.05rem;margin-bottom:4px">Заявка пуста</b>' +
        'Добавьте растения из каталога — мы посчитаем стоимость и наличие.</div>' +
        '<a class="btn btn-outline btn-sm" href="catalog.html">Перейти в каталог</a></div>';
      foot.innerHTML = '';
      return;
    }
    body.innerHTML = Req.lines.map(function (l) {
      var p = byId(l.id);
      return '<div class="ri">' +
        '<img src="' + img(p.img[0], 400) + '" alt="" loading="lazy" width="66" height="66">' +
        '<div class="ri-main">' +
          '<div class="ri-top"><b>' + p.name + '</b>' +
            '<button class="ri-rm" data-req="rm" data-id="' + p.id + '" aria-label="Убрать «' + p.name + '»">' + I.close + '</button></div>' +
          '<div class="ri-bot">' +
            '<span class="qty">' +
              '<button data-req="dec" data-id="' + p.id + '" aria-label="Меньше">&minus;</button>' +
              '<span>' + l.qty + '</span>' +
              '<button data-req="inc" data-id="' + p.id + '" aria-label="Больше">+</button>' +
            '</span>' +
            '<span class="muted">' + (p.price ? money(p.price * l.qty) : 'по запросу') + '</span>' +
          '</div>' +
        '</div></div>';
    }).join('');

    var known = Req.lines.reduce(function (s, l) { var p = byId(l.id); return s + (p.price || 0) * l.qty; }, 0);
    var unknown = Req.lines.some(function (l) { return !byId(l.id).price; });
    foot.innerHTML =
      '<div class="kv"><div><span class="k">Позиций</span><span class="v">' + Req.lines.length + '</span></div>' +
      '<div><span class="k">Всего растений</span><span class="v">' + Req.count() + ' шт</span></div>' +
      (known ? '<div><span class="k">Ориентировочно</span><span class="v">' + money(known) +
        (unknown ? ' + по запросу' : '') + '</span></div>' : '') + '</div>' +
      '<a class="btn btn-primary btn-block" href="index.html#contacts" data-req-send>Отправить заявку</a>' +
      '<button class="btn btn-ghost btn-sm" data-req="clear">Очистить</button>';
  }

  function openDrawer() {
    if (!drawer) return;
    drawer.classList.add('open');
    if (scrimEl) scrimEl.classList.add('open');
    document.body.classList.add('lock');
    var c = $('[data-req-close]', drawer); if (c) c.focus();
  }
  function closeDrawer() {
    if (!drawer) return;
    drawer.classList.remove('open');
    if (scrimEl && !$('.filters.open') && !$('.mobile-nav.open')) scrimEl.classList.remove('open');
    document.body.classList.remove('lock');
  }
  ALK.openDrawer = openDrawer;

  function initRequest() {
    drawer = $('[data-drawer]');
    scrimEl = $('[data-scrim]');
    Req.load();
    paintReq();

    document.addEventListener('click', function (e) {
      var t = e.target.closest('[data-add]');
      if (t) {
        Req.add(t.getAttribute('data-add'), 1);
        t.classList.add('in');
        setTimeout(function () { t.classList.remove('in'); }, 1200);
        return;
      }
      if (e.target.closest('[data-req-open]')) { e.preventDefault(); openDrawer(); return; }
      if (e.target.closest('[data-req-close]')) { closeDrawer(); return; }
      var a = e.target.closest('[data-req]');
      if (!a) return;
      var act = a.getAttribute('data-req'), id = a.getAttribute('data-id');
      var cur = 0;
      Req.lines.forEach(function (l) { if (l.id === id) cur = l.qty; });
      if (act === 'inc') Req.setQty(id, cur + 1);
      if (act === 'dec') Req.setQty(id, cur - 1);
      if (act === 'rm') Req.remove(id);
      if (act === 'clear') Req.clear();
    });

    // перенос заявки в форму на странице контактов
    document.addEventListener('click', function (e) {
      if (!e.target.closest('[data-req-send]')) return;
      var f = $('[data-order-form]');
      var note = f && $('[name="message"]', f);
      if (note && Req.lines.length) {
        note.value = 'Заявка на растения:\n' + Req.text();
        closeDrawer();
        setTimeout(function () { note.focus({ preventScroll: true }); }, 400);
      }
    });

    if (scrimEl) scrimEl.addEventListener('click', closeDrawer);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer && drawer.classList.contains('open')) closeDrawer();
    });
    window.addEventListener('storage', function (e) {
      if (e.key === KEY) { Req.load(); paintReq(); }
    });
  }

  /* ======================= модалка товара ======================= */
  function initModal() {
    var m = $('[data-modal]');
    if (!m) return;
    var box = $('.modal-box', m), last = null;

    function open(id) {
      var p = byId(id); if (!p) return;
      last = document.activeElement;
      var specs = [
        ['Артикул', p.sku || '—'],
        ['Тип', (CATS[p.cat] || {}).label || '—'],
        ['Размер горшка', p.pots.length ? p.pots.join(', ') : '—'],
        ['Высота растения', p.heights.length ? p.heights.join(', ') + ' см' : '—'],
        ['Наличие', p.inStock ? 'В наличии в питомнике' : 'Под заказ'],
        ['Цена', p.price ? (p.priceMax && p.priceMax > p.price ? 'от ' + money(p.price) + ' до ' + money(p.priceMax) : money(p.price)) : 'по запросу']
      ];
      box.innerHTML =
        '<div class="modal-media">' +
          '<img src="' + img(p.img[0], 800) + '" alt="' + p.name + '" data-main width="800" height="800">' +
          (p.img.length > 1 ? '<div class="modal-thumbs">' + p.img.map(function (n, i) {
            return '<button data-th="' + n + '" aria-current="' + (i === 0) + '" aria-label="Фото ' + (i + 1) + '">' +
              '<img src="' + img(n, 800) + '" alt="" loading="lazy"></button>';
          }).join('') + '</div>' : '') +
          '<button class="icon-btn modal-close" data-modal-close aria-label="Закрыть">' + I.close + '</button>' +
        '</div>' +
        '<div class="modal-info">' +
          '<div>' +
            (p.inStock ? '<span class="pill pill-stock"><span class="dot"></span>В наличии</span>'
                       : '<span class="pill pill-out">Под заказ</span>') +
            '<h2 style="margin:10px 0 2px;font-size:1.6rem">' + p.name + '</h2>' +
            (p.latin ? '<em class="muted" style="font-family:var(--font-display)">' + p.latin + '</em>' : '') +
          '</div>' +
          '<div class="spec-table">' + specs.map(function (r) {
            return '<div><span class="k">' + r[0] + '</span><span class="v">' + r[1] + '</span></div>';
          }).join('') + '</div>' +
          (p.desc ? '<p class="modal-desc">' + p.desc.replace(/\n/g, '<br>') + '</p>' : '') +
          '<div style="display:flex;gap:10px;flex-wrap:wrap">' +
            '<button class="btn btn-primary" data-add="' + p.id + '">' + I.plus + 'Добавить в заявку</button>' +
            '<a class="btn btn-outline" href="tel:+375293191844">Уточнить по телефону</a>' +
          '</div>' +
        '</div>';
      m.classList.add('open');
      document.body.classList.add('lock');
      var c = $('[data-modal-close]', m); if (c) c.focus();
    }
    function close() {
      m.classList.remove('open');
      document.body.classList.remove('lock');
      if (last && last.focus) last.focus();
    }
    ALK.openProduct = open;

    document.addEventListener('click', function (e) {
      var o = e.target.closest('[data-open]');
      if (o) { e.preventDefault(); open(o.getAttribute('data-open')); return; }
      if (e.target.closest('[data-modal-close]') || e.target === m) close();
      var th = e.target.closest('[data-th]');
      if (th) {
        $('[data-main]', m).src = img(th.getAttribute('data-th'), 800);
        $$('[data-th]', m).forEach(function (b) { b.setAttribute('aria-current', String(b === th)); });
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && m.classList.contains('open')) close();
    });
  }

  /* ======================= каталог ======================= */
  function initCatalog() {
    var grid = $('[data-grid]');
    if (!grid) return;
    var isFull = grid.hasAttribute('data-full');

    var params = new URLSearchParams(location.search);
    var st = {
      q: params.get('q') || '',
      cats: (params.get('cat') ? params.get('cat').split(',') : []).filter(function (c) { return CATS[c]; }),
      sizes: [], pots: [], price: 'any', stock: false,
      sort: params.get('sort') || 'default'
    };

    var elQ = $('[data-q]'), elSort = $('[data-sort]'), elCount = $('[data-count]');

    function match(p) {
      if (st.cats.length && st.cats.indexOf(p.cat) === -1) return false;
      if (st.stock && !p.inStock) return false;
      if (st.sizes.length) {
        var ok = st.sizes.some(function (id) {
          var s = SIZES.filter(function (x) { return x.id === id; })[0];
          return s && s.test(p);
        });
        if (!ok) return false;
      }
      if (st.pots.length && !p.pots.some(function (x) { return st.pots.indexOf(x) > -1; })) return false;
      var pr = PRICES.filter(function (x) { return x.id === st.price; })[0];
      if (pr && !pr.test(p)) return false;
      var q = st.q.trim().toLowerCase();
      if (q) {
        var hay = (p.name + ' ' + p.latin + ' ' + p.sku + ' ' + (CATS[p.cat] || {}).label + ' ' + p.desc).toLowerCase();
        if (hay.indexOf(q) === -1) return false;
      }
      return true;
    }

    var SORTS = {
      default:     function (a, b) { return b.inStock - a.inStock || a.order - b.order; },
      name:        function (a, b) { return a.name.localeCompare(b.name, 'ru'); },
      'price-asc': function (a, b) { return (a.price || 1e9) - (b.price || 1e9); },
      'price-desc':function (a, b) { return (b.price || -1) - (a.price || -1); },
      'height-asc':function (a, b) { return a.hMin - b.hMin; },
      'height-desc':function (a, b) { return b.hMax - a.hMax; }
    };

    function syncURL() {
      if (!isFull) return;
      var p = new URLSearchParams();
      if (st.q) p.set('q', st.q);
      if (st.cats.length) p.set('cat', st.cats.join(','));
      if (st.sort !== 'default') p.set('sort', st.sort);
      var s = p.toString();
      history.replaceState(null, '', s ? '?' + s : location.pathname);
    }

    function render() {
      var list = ALK.products.filter(match).sort(SORTS[st.sort] || SORTS.default);
      if (!isFull) list = list.slice(0, 10);

      if (elCount) {
        elCount.innerHTML = '<b>' + list.length + '</b> ' + plural(list.length, 'растение', 'растения', 'растений');
      }
      grid.innerHTML = list.length ? list.map(cardHTML).join('') :
        '<div class="empty"><h3>Ничего не найдено</h3>' +
        '<p class="muted">Попробуйте убрать часть фильтров или очистить поиск.</p>' +
        '<button class="btn btn-outline btn-sm" data-reset>Сбросить фильтры</button></div>';
      $$('.rise', grid).forEach(function (e, i) { e.style.setProperty('--d', Math.min(i, 5) * 45 + 'ms'); });
      if (ALK.watch) ALK.watch(grid); else $$('.rise', grid).forEach(function (e) { e.classList.add('in'); });
      syncURL();
      updateCounts();
    }

    function plural(n, a, b, c) {
      var m = n % 100, d = n % 10;
      if (m > 10 && m < 20) return c;
      if (d === 1) return a;
      if (d >= 2 && d <= 4) return b;
      return c;
    }

    /* --- построение фильтров --- */
    function countIf(fn) { return ALK.products.filter(fn).length; }

    function buildFilters() {
      var host = $('[data-filters]');
      if (!host) return;
      var potList = [];
      ALK.products.forEach(function (p) {
        p.pots.forEach(function (x) { if (potList.indexOf(x) === -1) potList.push(x); });
      });
      potList.sort(function (a, b) {
        var w = function (s) { return s === 'ОКС' ? 100 : s === 'Р9' ? 0 : parseFloat(s.replace(/[^\d,]/g, '').replace(',', '.')) || 50; };
        return w(a) - w(b);
      });

      host.innerHTML =
        '<div class="f-group"><h4>Тип растения</h4><div class="f-list">' +
          Object.keys(CATS).map(function (c) {
            return '<label class="f-opt"><input type="checkbox" data-f="cat" value="' + c + '">' +
              '<span>' + CATS[c].label + '</span><span class="n" data-n-cat="' + c + '">' +
              countIf(function (p) { return p.cat === c; }) + '</span></label>';
          }).join('') +
        '</div></div>' +

        '<div class="f-group"><h4>Высота</h4><div class="f-list">' +
          SIZES.map(function (s) {
            return '<label class="f-opt"><input type="checkbox" data-f="size" value="' + s.id + '">' +
              '<span>' + s.label + '</span><span class="n">' + countIf(s.test) + '</span></label>';
          }).join('') +
        '</div></div>' +

        '<div class="f-group"><h4>Размер горшка</h4><div class="f-chips">' +
          potList.map(function (x) {
            return '<button class="f-chip" data-f="pot" value="' + x + '" aria-pressed="false">' + x + '</button>';
          }).join('') +
        '</div><p class="small muted" style="margin-top:2px">ОКС — с открытой корневой системой</p></div>' +

        '<div class="f-group"><h4>Цена</h4><div class="f-list">' +
          PRICES.map(function (p, i) {
            return '<label class="f-opt"><input type="radio" name="price" data-f="price" value="' + p.id + '"' +
              (i === 0 ? ' checked' : '') + '><span>' + p.label + '</span>' +
              '<span class="n">' + (p.id === 'any' ? ALK.products.length : countIf(p.test)) + '</span></label>';
          }).join('') +
        '</div></div>' +

        '<div class="f-group"><label class="f-opt"><input type="checkbox" data-f="stock">' +
          '<span>Только в наличии</span><span class="n">' + countIf(function (p) { return p.inStock; }) + '</span></label></div>' +

        '<button class="btn btn-outline btn-sm" data-reset>Сбросить фильтры</button>';

      // восстановить состояние из URL
      st.cats.forEach(function (c) {
        var i = $('[data-f="cat"][value="' + c + '"]', host); if (i) i.checked = true;
      });

      host.addEventListener('change', function (e) {
        var i = e.target.closest('[data-f]'); if (!i) return;
        var f = i.getAttribute('data-f');
        if (f === 'cat' || f === 'size') {
          var key = f === 'cat' ? 'cats' : 'sizes';
          st[key] = $$('[data-f="' + f + '"]:checked', host).map(function (x) { return x.value; });
        }
        if (f === 'price') st.price = i.value;
        if (f === 'stock') st.stock = i.checked;
        render();
      });
      host.addEventListener('click', function (e) {
        var c = e.target.closest('[data-f="pot"]'); if (!c) return;
        var on = c.getAttribute('aria-pressed') !== 'true';
        c.setAttribute('aria-pressed', String(on));
        st.pots = $$('[data-f="pot"][aria-pressed="true"]', host).map(function (x) { return x.getAttribute('value'); });
        render();
      });
    }

    function updateCounts() {
      // счётчик у категорий с учётом остальных фильтров — подсказывает, что даст клик
      Object.keys(CATS).forEach(function (c) {
        var el = $('[data-n-cat="' + c + '"]');
        if (el) el.textContent = ALK.products.filter(function (p) { return p.cat === c && match2(p, c); }).length;
      });
      function match2(p, c) {
        var saved = st.cats; st.cats = [c];
        var r = match(p); st.cats = saved; return r;
      }
    }

    function reset() {
      st.q = ''; st.cats = []; st.sizes = []; st.pots = []; st.price = 'any'; st.stock = false;
      if (elQ) elQ.value = '';
      $$('[data-filters] input[type="checkbox"]').forEach(function (i) { i.checked = false; });
      var any = $('[data-f="price"][value="any"]'); if (any) any.checked = true;
      $$('[data-f="pot"]').forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
      $$('[data-cat-chip]').forEach(function (b) {
        b.setAttribute('aria-pressed', String(b.getAttribute('data-cat-chip') === 'all'));
      });
      render();
    }

    document.addEventListener('click', function (e) { if (e.target.closest('[data-reset]')) reset(); });

    if (elQ) {
      var t;
      elQ.value = st.q;
      elQ.addEventListener('input', function () {
        clearTimeout(t); t = setTimeout(function () { st.q = elQ.value; render(); }, 160);
      });
      elQ.addEventListener('keydown', function (e) { if (e.key === 'Escape') { elQ.value = ''; st.q = ''; render(); } });
    }
    if (elSort) { elSort.value = st.sort; elSort.addEventListener('change', function () { st.sort = elSort.value; render(); }); }

    // чипы категорий на главной
    $$('[data-cat-chip]').forEach(function (b) {
      b.addEventListener('click', function () {
        var v = b.getAttribute('data-cat-chip');
        $$('[data-cat-chip]').forEach(function (o) { o.setAttribute('aria-pressed', String(o === b)); });
        st.cats = v === 'all' ? [] : [v];
        render();
      });
    });

    // мобильная панель фильтров
    var fPanel = $('.filters'), fToggle = $('[data-filters-toggle]');
    if (fPanel && fToggle) {
      fToggle.addEventListener('click', function () {
        fPanel.classList.add('open');
        if (scrimEl) scrimEl.classList.add('open');
        document.body.classList.add('lock');
      });
      var closeF = function () {
        fPanel.classList.remove('open');
        if (scrimEl && !$('.drawer.open') && !$('.mobile-nav.open')) scrimEl.classList.remove('open');
        document.body.classList.remove('lock');
      };
      $$('[data-filters-close]').forEach(function (b) { b.addEventListener('click', closeF); });
      if (scrimEl) scrimEl.addEventListener('click', closeF);
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && fPanel.classList.contains('open')) closeF();
      });
    }

    buildFilters();
    render();
  }

  /* ======================= галерея / лайтбокс ======================= */
  function initGallery() {
    var box = $('[data-lightbox]');
    if (!box) return;
    var shots = $$('[data-shot]'), idx = 0, last = null;
    var imgEl = $('img', box), cap = $('.lb-cap', box);

    function show(i) {
      idx = (i + shots.length) % shots.length;
      var b = shots[idx];
      imgEl.src = b.getAttribute('data-shot');
      imgEl.alt = b.getAttribute('data-cap') || '';
      if (cap) cap.textContent = (b.getAttribute('data-cap') || '') + '  ·  ' + (idx + 1) + ' / ' + shots.length;
    }
    function open(i) {
      last = document.activeElement;
      show(i); box.classList.add('open'); document.body.classList.add('lock');
      var c = $('.lb-close', box); if (c) c.focus();
    }
    function close() {
      box.classList.remove('open'); document.body.classList.remove('lock');
      if (last && last.focus) last.focus();
    }
    shots.forEach(function (b, i) { b.addEventListener('click', function () { open(i); }); });
    box.addEventListener('click', function (e) {
      if (e.target.closest('.lb-close') || e.target === box) return close();
      if (e.target.closest('.lb-prev')) return show(idx - 1);
      if (e.target.closest('.lb-next')) return show(idx + 1);
    });
    document.addEventListener('keydown', function (e) {
      if (!box.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(idx - 1);
      if (e.key === 'ArrowRight') show(idx + 1);
    });
  }

  /* ======================= формы ======================= */
  function initForms() {
    $$('[data-form]').forEach(function (form) {
      form.setAttribute('novalidate', '');
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var ok = true;
        $$('input[required], textarea[required], select[required]', form).forEach(function (i) {
          var field = i.closest('.field') || i.parentElement;
          var msg = $('.msg', field);
          var bad = !i.checkValidity();
          field.classList.toggle('err', bad);
          if (msg) msg.textContent = bad ? (i.type === 'checkbox' ? 'Отметьте согласие' : 'Заполните это поле') : '';
          if (bad && ok) { i.focus(); ok = false; }
        });
        if (!ok) return;
        var done = $('[data-form-done]', form);
        if (done) done.hidden = false;
        form.reset();
        if (form.hasAttribute('data-order-form')) ALK.request.clear();
        toast('Заявка отправлена — перезвоним в рабочее время');
      });
      $$('input, textarea', form).forEach(function (i) {
        i.addEventListener('input', function () {
          var f = i.closest('.field');
          if (f && f.classList.contains('err') && i.checkValidity()) {
            f.classList.remove('err');
            var m = $('.msg', f); if (m) m.textContent = '';
          }
        });
      });
    });
  }

  /* ======================= тосты ======================= */
  var host;
  function toast(text) {
    if (!host) {
      host = document.createElement('div');
      host.className = 'toasts';
      host.setAttribute('role', 'status');
      host.setAttribute('aria-live', 'polite');
      document.body.appendChild(host);
    }
    var t = document.createElement('div');
    t.className = 'toast';
    t.innerHTML = I.check + '<span></span>';
    t.querySelector('span').textContent = text;
    host.appendChild(t);
    setTimeout(function () {
      t.classList.add('out');
      setTimeout(function () { t.remove(); }, 300);
    }, 2600);
  }
  ALK.toast = toast;

  /* ======================= прочее ======================= */
  function misc() {
    $$('[data-year]').forEach(function (e) { e.textContent = new Date().getFullYear(); });
    // подсветка текущего дня в графике
    var d = new Date().getDay();
    $$('[data-today]').forEach(function (e) {
      e.textContent = d === 0 ? 'Сегодня выходной' : 'Сегодня работаем 9:00–17:00';
    });
  }

  function init() {
    ALK.products = (ALK.products || []).map(function (p, i) { p.order = i; return p; });
    header();
    initRequest();
    initModal();
    initCatalog();
    initGallery();
    initForms();
    reveal();
    misc();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
