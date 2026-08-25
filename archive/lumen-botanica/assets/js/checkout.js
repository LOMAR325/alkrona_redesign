/* LUMEN BOTANICA — checkout summary & demo order flow --------------------- */
(function () {
  'use strict';

  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  LB.initCheckout = function () {
    var root = $('[data-checkout]');
    if (!root) return;

    var list  = $('[data-co-list]');
    var sums  = $('[data-co-sums]');
    var form  = $('[data-co-form]');
    var done  = $('[data-co-done]');
    var empty = $('[data-co-empty]');
    var main  = $('[data-co-main]');
    var submit = $('[data-co-submit]');

    function paint() {
      var lines = LB.cart.lines;

      if (!lines.length) {
        if (main) main.hidden = true;
        if (empty) empty.hidden = false;
        return;
      }
      if (main) main.hidden = false;
      if (empty) empty.hidden = true;

      list.innerHTML = lines.map(function (l) {
        var p = LB.cart.product(l.id);
        return '<div class="co-item">' +
          '<img src="' + p.img + '" alt="" loading="lazy" decoding="async">' +
          '<div><b>' + p.name + '</b><span>Qty ' + l.qty + ' · ' + p.latin + '</span></div>' +
          '<span class="price" style="font-size:.95rem">' + LB.money(p.price * l.qty) + '</span>' +
        '</div>';
      }).join('');

      var sub = LB.cart.subtotal(), ship = LB.cart.shipping();
      sums.innerHTML =
        '<div class="sum">' +
          '<div><span>Subtotal</span><span>' + LB.money(sub) + '</span></div>' +
          '<div><span>Shipping (insured, plastic-free)</span><span class="' + (ship === 0 ? 'free' : '') + '">' +
            (ship === 0 ? 'Free' : LB.money(ship)) + '</span></div>' +
          '<div><span>VAT included</span><span>' + LB.money(sub * 0.21 / 1.21) + '</span></div>' +
          '<div class="total"><span>Total</span><span>' + LB.money(sub + ship) + '</span></div>' +
        '</div>';

      if (submit) submit.textContent = 'Place order · ' + LB.money(sub + ship);
    }

    document.addEventListener('cart:change', paint);
    paint();

    if (form) {
      form.addEventListener('form:valid', function () {
        var total = LB.money(LB.cart.total());
        var ref = 'LB-' + String(Date.now()).slice(-6);
        LB.cart.clear();
        if (main) main.hidden = true;
        if (empty) empty.hidden = true;
        if (done) {
          done.hidden = false;
          var r = $('[data-co-ref]', done); if (r) r.textContent = ref;
          var t = $('[data-co-total]', done); if (t) t.textContent = total;
          done.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      });
    }
  };
})();
