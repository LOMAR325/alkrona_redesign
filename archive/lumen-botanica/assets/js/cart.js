/* LUMEN BOTANICA — cart, drawer, toasts ----------------------------------- */
(function () {
  'use strict';

  var KEY = 'lb.cart.v1';
  var FREE_SHIPPING = 75;
  var SHIPPING = 6.95;

  var fmt = new Intl.NumberFormat(LB.currency.locale, {
    style: 'currency', currency: LB.currency.code, minimumFractionDigits: 2
  });

  /* ---------- state ---------- */
  function read() {
    try {
      var raw = JSON.parse(localStorage.getItem(KEY));
      return Array.isArray(raw) ? raw.filter(function (l) { return byId(l.id); }) : [];
    } catch (e) { return []; }
  }
  function write(lines) {
    try { localStorage.setItem(KEY, JSON.stringify(lines)); } catch (e) {}
    render();
    document.dispatchEvent(new CustomEvent('cart:change', { detail: { lines: lines } }));
  }
  function byId(id) {
    for (var i = 0; i < LB.products.length; i++) if (LB.products[i].id === id) return LB.products[i];
    return null;
  }

  var Cart = {
    lines: read(),
    count: function () {
      return this.lines.reduce(function (n, l) { return n + l.qty; }, 0);
    },
    subtotal: function () {
      return this.lines.reduce(function (n, l) {
        var p = byId(l.id); return n + (p ? p.price * l.qty : 0);
      }, 0);
    },
    shipping: function () {
      if (!this.lines.length) return 0;
      return this.subtotal() >= FREE_SHIPPING ? 0 : SHIPPING;
    },
    total: function () { return this.subtotal() + this.shipping(); },
    add: function (id, qty) {
      var p = byId(id); if (!p) return;
      qty = qty || 1;
      var line = null;
      for (var i = 0; i < this.lines.length; i++) if (this.lines[i].id === id) line = this.lines[i];
      if (line) line.qty = Math.min(99, line.qty + qty);
      else this.lines.push({ id: id, qty: qty });
      write(this.lines);
      toast(p.name + ' added to cart');
      bump();
    },
    setQty: function (id, qty) {
      this.lines = this.lines.filter(function (l) {
        if (l.id !== id) return true;
        l.qty = Math.max(0, Math.min(99, qty));
        return l.qty > 0;
      });
      write(this.lines);
    },
    remove: function (id) {
      this.lines = this.lines.filter(function (l) { return l.id !== id; });
      write(this.lines);
      toast('Removed from cart');
    },
    clear: function () { this.lines = []; write(this.lines); },
    fmt: fmt,
    freeAt: FREE_SHIPPING,
    product: byId
  };
  LB.cart = Cart;
  LB.money = function (n) { return fmt.format(n); };

  /* ---------- icons ---------- */
  var ICON = {
    cart: '<svg viewBox="0 0 24 24"><path d="M3 4h2l2.4 11.2a2 2 0 0 0 2 1.6h7.7a2 2 0 0 0 2-1.6L21 8H6"/><circle cx="10" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/></svg>',
    close: '<svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg>',
    check: '<svg viewBox="0 0 24 24"><path d="M4 12.5l5 5L20 6.5"/></svg>',
    bag: '<svg viewBox="0 0 24 24"><path d="M6 8h12l1 12H5L6 8z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>'
  };

  /* ---------- drawer markup (injected once per page) ---------- */
  var scrim, drawer, body, foot, lastFocus;

  function build() {
    scrim = document.createElement('div');
    scrim.className = 'scrim';
    scrim.hidden = false;

    drawer = document.createElement('aside');
    drawer.className = 'drawer';
    drawer.id = 'cart-drawer';
    drawer.setAttribute('role', 'dialog');
    drawer.setAttribute('aria-modal', 'true');
    drawer.setAttribute('aria-label', 'Shopping cart');
    drawer.innerHTML =
      '<div class="drawer-head">' +
        '<h2>Your cart <span class="tag" data-cart-tag>0</span></h2>' +
        '<button class="icon-btn" data-cart-close aria-label="Close cart">' + ICON.close + '</button>' +
      '</div>' +
      '<div class="drawer-body" data-cart-body></div>' +
      '<div class="drawer-foot" data-cart-foot></div>';

    document.body.appendChild(scrim);
    document.body.appendChild(drawer);

    body = drawer.querySelector('[data-cart-body]');
    foot = drawer.querySelector('[data-cart-foot]');

    scrim.addEventListener('click', close);
    drawer.querySelector('[data-cart-close]').addEventListener('click', close);

    document.addEventListener('keydown', function (e) {
      if (!drawer.classList.contains('open')) return;
      if (e.key === 'Escape') { close(); return; }
      if (e.key === 'Tab') trap(e);
    });

    drawer.addEventListener('click', function (e) {
      var t = e.target.closest('[data-act]');
      if (!t) return;
      var id = t.getAttribute('data-id');
      var act = t.getAttribute('data-act');
      if (act === 'inc') Cart.setQty(id, qtyOf(id) + 1);
      if (act === 'dec') Cart.setQty(id, qtyOf(id) - 1);
      if (act === 'rm') Cart.remove(id);
    });
  }

  function qtyOf(id) {
    for (var i = 0; i < Cart.lines.length; i++) if (Cart.lines[i].id === id) return Cart.lines[i].qty;
    return 0;
  }

  function trap(e) {
    var f = drawer.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
    if (!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  }

  function open() {
    lastFocus = document.activeElement;
    scrim.classList.add('open');
    drawer.classList.add('open');
    document.body.classList.add('no-scroll');
    var btn = drawer.querySelector('[data-cart-close]');
    if (btn) btn.focus();
  }
  function close() {
    scrim.classList.remove('open');
    drawer.classList.remove('open');
    document.body.classList.remove('no-scroll');
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  Cart.open = open;
  Cart.close = close;

  /* ---------- rendering ---------- */
  function render() {
    var n = Cart.count();

    // header badges
    document.querySelectorAll('[data-cart-count]').forEach(function (el) {
      el.textContent = n;
      el.classList.toggle('on', n > 0);
    });
    var tag = drawer && drawer.querySelector('[data-cart-tag]');
    if (tag) tag.textContent = n + (n === 1 ? ' item' : ' items');

    if (!body) return;

    if (!Cart.lines.length) {
      body.innerHTML =
        '<div class="cart-empty">' + ICON.bag +
        '<div><b style="font-family:var(--font-display);display:block;color:var(--text);margin-bottom:4px">Nothing here yet</b>' +
        'Your cart is waiting for something green.</div>' +
        '<a class="btn btn-ghost btn-sm" href="shop.html">Browse the catalog</a></div>';
      foot.innerHTML = '';
      return;
    }

    body.innerHTML = Cart.lines.map(function (l) {
      var p = byId(l.id);
      return '<article class="ci">' +
        '<img src="' + p.img + '" alt="" loading="lazy" decoding="async">' +
        '<div class="ci-main">' +
          '<div class="ci-top"><b>' + p.name + '</b>' +
            '<button class="ci-rm" data-act="rm" data-id="' + p.id + '" aria-label="Remove ' + p.name + '">' + ICON.close + '</button>' +
          '</div>' +
          '<div class="ci-bot">' +
            '<div class="qty">' +
              '<button data-act="dec" data-id="' + p.id + '" aria-label="Decrease quantity of ' + p.name + '">&minus;</button>' +
              '<span aria-live="polite">' + l.qty + '</span>' +
              '<button data-act="inc" data-id="' + p.id + '" aria-label="Increase quantity of ' + p.name + '">+</button>' +
            '</div>' +
            '<span class="price" style="font-size:1rem">' + fmt.format(p.price * l.qty) + '</span>' +
          '</div>' +
        '</div></article>';
    }).join('');

    var sub = Cart.subtotal(), ship = Cart.shipping();
    var away = Math.max(0, FREE_SHIPPING - sub);
    foot.innerHTML =
      '<div class="sum">' +
        '<div><span>Subtotal</span><span>' + fmt.format(sub) + '</span></div>' +
        '<div><span>Shipping</span><span class="' + (ship === 0 ? 'free' : '') + '">' +
          (ship === 0 ? 'Free' : fmt.format(ship)) + '</span></div>' +
        (away > 0 ? '<div style="font-size:.8rem"><span>' + fmt.format(away) + ' more for free shipping</span><span></span></div>' : '') +
        '<div class="total"><span>Total</span><span>' + fmt.format(sub + ship) + '</span></div>' +
      '</div>' +
      '<a class="btn btn-primary btn-block" href="checkout.html">Checkout</a>' +
      '<button class="btn btn-ghost btn-sm btn-block" data-cart-close>Keep shopping</button>';

    foot.querySelectorAll('[data-cart-close]').forEach(function (b) {
      b.addEventListener('click', close);
    });
  }
  Cart.render = render;

  function bump() {
    document.querySelectorAll('[data-cart-count]').forEach(function (el) {
      el.classList.remove('bump');
      void el.offsetWidth;
      el.classList.add('bump');
    });
  }

  /* ---------- toasts ---------- */
  var toastHost;
  function toast(msg) {
    if (!toastHost) {
      toastHost = document.createElement('div');
      toastHost.className = 'toasts';
      toastHost.setAttribute('role', 'status');
      toastHost.setAttribute('aria-live', 'polite');
      document.body.appendChild(toastHost);
    }
    var t = document.createElement('div');
    t.className = 'toast';
    t.innerHTML = ICON.check + '<span></span>';
    t.querySelector('span').textContent = msg;
    toastHost.appendChild(t);
    setTimeout(function () {
      t.classList.add('out');
      setTimeout(function () { t.remove(); }, 340);
    }, 2600);
  }
  LB.toast = toast;

  /* ---------- wiring ---------- */
  function init() {
    build();
    render();

    document.addEventListener('click', function (e) {
      var openBtn = e.target.closest('[data-cart-open]');
      if (openBtn) { e.preventDefault(); open(); return; }

      var add = e.target.closest('[data-add]');
      if (add) {
        e.preventDefault();
        Cart.add(add.getAttribute('data-add'), 1);
        add.classList.add('done');
        var label = add.querySelector('span');
        var prev = label ? label.textContent : '';
        if (label) label.textContent = 'Added';
        setTimeout(function () {
          add.classList.remove('done');
          if (label) label.textContent = prev;
        }, 1400);
      }
    });

    // keep tabs in sync
    window.addEventListener('storage', function (e) {
      if (e.key === KEY) { Cart.lines = read(); render(); }
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
