/* LUMEN BOTANICA — catalog search, filter, sort --------------------------- */
(function () {
  'use strict';

  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  LB.initShop = function () {
    var grid = $('[data-shop-grid]');
    if (!grid) return;

    var params = new URLSearchParams(location.search);
    var state = {
      q:    params.get('q') || '',
      cat:  params.get('cat') || 'all',
      sort: params.get('sort') || 'popular',
      light: 'any',
      diff: 'any',
      petSafe: false,
      max: 400
    };
    // "statement" is a size-based pseudo-collection
    var pseudo = state.cat === 'statement';
    if (pseudo) state.cat = 'all';

    var elQ      = $('[data-shop-q]');
    var elSort   = $('[data-shop-sort]');
    var elCount  = $('[data-shop-count]');
    var elMax    = $('[data-shop-max]');
    var elMaxOut = $('[data-shop-max-out]');
    var elClear  = $('[data-shop-clear]');

    if (elQ) elQ.value = state.q;
    if (elSort) elSort.value = state.sort;

    function matches(p) {
      if (pseudo && p.size !== 'XL') return false;
      if (state.cat !== 'all' && p.cat !== state.cat) return false;
      if (state.light !== 'any' && p.light !== state.light) return false;
      if (state.diff !== 'any' && p.diff !== state.diff) return false;
      if (state.petSafe && !p.petSafe) return false;
      if (p.price > state.max) return false;
      var q = state.q.trim().toLowerCase();
      if (q) {
        var hay = (p.name + ' ' + p.latin + ' ' + p.cat + ' ' + p.blurb).toLowerCase();
        if (hay.indexOf(q) === -1) return false;
      }
      return true;
    }

    var SORTS = {
      popular:  function (a, b) { return b.pop - a.pop; },
      newest:   function (a, b) { return b.added - a.added; },
      'price-asc':  function (a, b) { return a.price - b.price; },
      'price-desc': function (a, b) { return b.price - a.price; },
      rating:   function (a, b) { return b.rating - a.rating || b.reviews - a.reviews; },
      name:     function (a, b) { return a.name.localeCompare(b.name); }
    };

    function sync() {
      var p = new URLSearchParams();
      if (state.q) p.set('q', state.q);
      if (state.cat !== 'all') p.set('cat', state.cat);
      if (pseudo) p.set('cat', 'statement');
      if (state.sort !== 'popular') p.set('sort', state.sort);
      var qs = p.toString();
      history.replaceState(null, '', qs ? '?' + qs : location.pathname);
    }

    function render() {
      var list = LB.products.filter(matches).sort(SORTS[state.sort] || SORTS.popular);

      if (elCount) {
        elCount.innerHTML = '<b>' + list.length + '</b> ' +
          (list.length === 1 ? 'plant' : 'plants') +
          (state.q ? ' matching “' + escapeHTML(state.q) + '”' : '');
      }

      grid.innerHTML = list.length
        ? list.map(LB.cardHTML).join('')
        : '<div class="empty">' +
            '<h3>No plants match those filters</h3>' +
            '<p class="lede" style="text-align:center">Try widening the price range, or clear the filters to see all ' +
            LB.products.length + ' plants.</p>' +
            '<button class="btn btn-ghost btn-sm" data-shop-clear>Clear all filters</button>' +
          '</div>';

      $$('.reveal', grid).forEach(function (el, i) {
        el.style.setProperty('--d', ((i % 4) * 60) + 'ms');
      });
      if (LB.observeReveals) LB.observeReveals(grid); else $$('.reveal', grid).forEach(function (el) { el.classList.add('in'); });
      if (LB.paintFavs) LB.paintFavs();
      sync();
    }

    function escapeHTML(s) {
      return String(s).replace(/[&<>"']/g, function (c) {
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
      });
    }

    /* ---- controls ---- */
    if (elQ) {
      var t;
      elQ.addEventListener('input', function () {
        clearTimeout(t);
        t = setTimeout(function () { state.q = elQ.value; render(); }, 180);
      });
      elQ.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') { elQ.value = ''; state.q = ''; render(); }
      });
    }
    if (elSort) elSort.addEventListener('change', function () { state.sort = elSort.value; render(); });

    if (elMax) {
      var syncMax = function () {
        state.max = +elMax.value;
        if (elMaxOut) elMaxOut.textContent = state.max >= 400 ? 'Any price' : 'Up to ' + LB.money(state.max);
        render();
      };
      elMax.addEventListener('input', syncMax);
      syncMax();
    }

    function group(sel, key) {
      var chips = $$(sel);
      chips.forEach(function (c) {
        var val = c.getAttribute(sel.replace(/[\[\]]/g, '').split('=')[0]);
        c.addEventListener('click', function () {
          chips.forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
          c.setAttribute('aria-pressed', 'true');
          state[key] = val;
          if (key === 'cat') pseudo = false;
          render();
        });
        if (state[key] === val) c.setAttribute('aria-pressed', 'true');
        else c.setAttribute('aria-pressed', 'false');
      });
    }
    group('[data-cat]', 'cat');
    group('[data-light]', 'light');
    group('[data-diff]', 'diff');

    var elPet = $('[data-pet]');
    if (elPet) elPet.addEventListener('change', function () { state.petSafe = elPet.checked; render(); });

    document.addEventListener('click', function (e) {
      if (!e.target.closest('[data-shop-clear]')) return;
      state.q = ''; state.cat = 'all'; state.light = 'any'; state.diff = 'any';
      state.petSafe = false; state.max = 400; pseudo = false;
      if (elQ) elQ.value = '';
      if (elPet) elPet.checked = false;
      if (elMax) elMax.value = 400;
      if (elMaxOut) elMaxOut.textContent = 'Any price';
      $$('[data-cat]').forEach(function (c) { c.setAttribute('aria-pressed', String(c.getAttribute('data-cat') === 'all')); });
      $$('[data-light]').forEach(function (c) { c.setAttribute('aria-pressed', String(c.getAttribute('data-light') === 'any')); });
      $$('[data-diff]').forEach(function (c) { c.setAttribute('aria-pressed', String(c.getAttribute('data-diff') === 'any')); });
      render();
    });

    if (elClear) { /* handled by delegation above */ }

    render();
  };
})();
