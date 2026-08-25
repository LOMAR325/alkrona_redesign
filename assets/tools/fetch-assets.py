#!/usr/bin/env python3
"""
Pull the live Alkrona catalogue + photography and bake it into local assets.

  python3 tools/fetch-assets.py

Reads the public WooCommerce Store API and WordPress media library on
alkrona.by, then writes:

  assets/img/plants/<slug>-{400,800}.webp   product photography
  assets/img/nursery/<name>-{800,1600}.webp field / greenhouse photography
  assets/data/catalog.json                  normalised catalogue

Images are centre-cropped to square for cards, re-encoded as WebP, and kept
small enough that a 40-card grid stays fast.
"""
import json, os, re, ssl, sys, urllib.request, html as htmllib
from io import BytesIO
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps, ImageStat

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://alkrona.by"
PLANTS = os.path.join(ROOT, "assets/img/plants")
NURSERY = os.path.join(ROOT, "assets/img/nursery")
DATA = os.path.join(ROOT, "assets/data")
# кадры, которые верстка использует как широкие баннеры (хиро и карточки ухода)
BANNERS = {"field-3894", "field-3942", "field-3971", "field-4154", "field-3748"}

CTX = ssl.create_default_context()
CTX.check_hostname = False           # the live cert has expired
CTX.verify_mode = ssl.CERT_NONE

for d in (PLANTS, NURSERY, DATA):
    os.makedirs(d, exist_ok=True)


def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": "alkrona-redesign/1.0"})
    with urllib.request.urlopen(req, context=CTX, timeout=60) as r:
        raw = r.read()
    return raw if binary else json.loads(raw.decode("utf-8"))


def txt(s):
    s = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", s or "")
    s = re.sub(r"(?s)<br\s*/?>|</p>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = htmllib.unescape(s)
    s = re.sub(r"[ \t]+", " ", s)
    return re.sub(r"\n{2,}", "\n", s).strip()




# ---------------------------------------------------------------- цветокоррекция
def grade(im):
    """Единый грейд для фотографий каталога.

    Снимки приходят разномастные: телефонные кадры в поле, студийные фото,
    пересвеченные генерации. Приводим их к одной экспозиции, балансу белого
    и насыщенности, добавляем общий тёплый оттенок и мягкое виньетирование,
    чтобы в сетке карточек они читались как один набор.
    """
    im = im.convert("RGB")
    w, h = im.size

    # --- баланс белого «серым миром», вполсилы: убираем явный цветовой сдвиг,
    #     но не выхолащиваем зелень
    r, g, b = ImageStat.Stat(im).mean
    grey = (r + g + b) / 3
    lut = []
    for ch_mean in (r, g, b):
        k = 1.0 if ch_mean < 1 else (grey / ch_mean)
        k = 1 + (k - 1) * 0.55
        lut += [max(0, min(255, int(round(i * k)))) for i in range(256)]
    im = im.point(lut)

    # --- уровни по перцентилям яркости: одинаковая «плотность» у всех кадров
    hist = im.convert("L").histogram()
    total = sum(hist)
    lo_t, hi_t = total * 0.004, total * 0.996
    acc, lo, hi = 0, 0, 255
    for i, c in enumerate(hist):
        acc += c
        if acc >= lo_t:
            lo = i
            break
    acc = 0
    for i, c in enumerate(hist):
        acc += c
        if acc >= hi_t:
            hi = i
            break
    lo = max(0, lo - 2)
    hi = min(255, max(lo + 40, hi + 2))
    scale = 255.0 / (hi - lo)
    lvl = [max(0, min(255, int(round((i - lo) * scale)))) for i in range(256)]
    im = im.point(lvl * 3)

    # --- насыщенность к общему знаменателю: перенасыщенные гасим, вялые поднимаем
    hsv = im.convert("HSV")
    sat_mean = ImageStat.Stat(hsv).mean[1]
    if sat_mean > 1:
        factor = 1 + (78.0 / sat_mean - 1) * 0.6
        factor = max(0.72, min(1.28, factor))
        im = ImageEnhance.Color(im).enhance(factor)

    im = ImageEnhance.Contrast(im).enhance(1.05)

    # --- тёплый грейд: света чуть в охру, тени чуть в зелень
    warm_r = [min(255, int(i + 9 * (i / 255) ** 1.4)) for i in range(256)]
    warm_g = [min(255, int(i + 3 * (i / 255) ** 1.2 + 2 * (1 - i / 255))) for i in range(256)]
    warm_b = [max(0, int(i - 7 * (i / 255) ** 1.1)) for i in range(256)]
    im = im.point(warm_r + warm_g + warm_b)

    # --- мягкое виньетирование, чтобы карточка не «вытекала» за края
    vig = Image.new("L", (w, h), 0)
    ImageDraw.Draw(vig).ellipse(
        (-w * 0.28, -h * 0.28, w * 1.28, h * 1.28), fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(radius=max(w, h) * 0.18))
    dark = ImageEnhance.Brightness(im).enhance(0.88)
    im = Image.composite(im, dark, vig)

    return im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=42, threshold=3))


def save(raw, path, size, square, q=72, ratio=None, colour=False):
    im = Image.open(BytesIO(raw))
    im = ImageOps.exif_transpose(im)
    if im.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", im.size, (255, 255, 255))
        im = im.convert("RGBA")
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")
    if colour:
        im = grade(im)
    if square:
        im = ImageOps.fit(im, (size, size), Image.LANCZOS, centering=(0.5, 0.42))
    elif ratio:
        im = ImageOps.fit(im, (size, int(size / ratio)), Image.LANCZOS, centering=(0.5, 0.5))
    else:
        im.thumbnail((size, size * 3), Image.LANCZOS)
    im.save(path, "WEBP", quality=q, method=6)
    return os.path.getsize(path)


# ---------------------------------------------------------------- pot sizes
def pots(terms):
    """WooCommerce split 'С1,5' on the comma — stitch it back together."""
    out, skip = [], False
    for i, t in enumerate(terms):
        if skip:
            skip = False
            continue
        t = t.strip()
        nxt = terms[i + 1].strip() if i + 1 < len(terms) else None
        if nxt and re.fullmatch(r"\d", nxt) and re.fullmatch(r"[СC]\d", t):
            out.append(f"{t},{nxt}")
            skip = True
        else:
            out.append(t)
    # normalise Latin C -> Cyrillic С so filters don't split in two
    return [re.sub(r"^C", "С", p) for p in out]


def _pot_key(p):
    """Р9 → мелкие контейнеры → крупные → ОКС в конце."""
    if p == "Р9": return 0
    if p == "ОКС": return 1000
    m = re.findall(r"[\d,]+", p)
    return float(m[0].replace(",", ".")) if m else 500


def heights(terms):
    vals = []
    for t in terms:
        m = re.findall(r"\d+", t)
        if len(m) >= 2:
            vals.append((int(m[0]), int(m[1]), t.strip()))
        elif m:
            vals.append((int(m[0]), int(m[0]), t.strip()))
    return vals


def main():
    print("· catalogue …")
    products = get(f"{SITE}/wp-json/wc/store/v1/products?per_page=100")
    cats = get(f"{SITE}/wp-json/wc/store/v1/products/categories?per_page=100")
    cat_slug = {c["id"]: c["slug"] for c in cats}

    out = []
    for p in products:
        attrs = {a["name"]: [t["name"] for t in a["terms"]] for a in (p.get("attributes") or [])}
        pot = pots(attrs.get("Горшок", []))
        hs = heights(attrs.get("Высота", []))
        price = int(p["prices"]["price"] or 0) / 100
        rng = p["prices"].get("price_range")
        price_min = int(rng["min_amount"]) / 100 if rng else price
        price_max = int(rng["max_amount"]) / 100 if rng else price

        cat = cat_slug.get(p["categories"][0]["id"], "other") if p["categories"] else "other"
        slug = p["slug"]
        imgs = []
        for n, im in enumerate(p["images"][:4]):
            try:
                raw = get(im["src"], binary=True)
            except Exception as e:
                print(f"  ! {slug} image {n}: {e}"); continue
            base = f"{slug}-{n}" if n else slug
            save(raw, os.path.join(PLANTS, f"{base}-800.webp"), 800, True, q=70, colour=True)
            if n == 0:
                save(raw, os.path.join(PLANTS, f"{base}-400.webp"), 400, True, q=64, colour=True)
            imgs.append(base)
        desc = txt(p["description"])
        out.append({
            "id": slug,
            "sku": p.get("sku") or "",
            "name": txt(p["name"]),
            "latin": txt(p["short_description"]),
            "cat": cat,
            "price": price_min,
            "priceMax": price_max if price_max != price_min else None,
            "inStock": bool(p["is_in_stock"]),
            "pots": sorted(dict.fromkeys(pot), key=_pot_key),
            "heights": [h[2] for h in sorted(hs, key=lambda x: x[0])],
            "hMin": min([h[0] for h in hs], default=0),
            "hMax": max([h[1] for h in hs], default=0),
            "desc": desc[:900],
            "img": imgs,
        })
        print(f"  {len(out):>2}/{len(products)} {out[-1]['name'][:38]:<40} {len(imgs)} img")

    if "--plants-only" in sys.argv:
        json.dump(out, open(os.path.join(DATA, "catalog.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print(f"\n{len(out)} товаров -> assets/data/catalog.json (фото питомника пропущены)")
        return

    # ------------------------------------------------------------ nursery
    print("· nursery photography …")
    media = get(f"{SITE}/wp-json/wp/v2/media?per_page=100&_fields=id,source_url,media_details")
    field = [m for m in media if re.search(r"/img_\d+", m["source_url"])]
    field.sort(key=lambda m: m["source_url"])
    seen, shots = set(), []
    for m in field:
        key = re.search(r"img_(\d+)", m["source_url"]).group(1)
        if key in seen:
            continue
        seen.add(key)
        shots.append(m)
    # landscape frames first — they make the best full-bleed banners
    def is_wide(m):
        d = m.get("media_details") or {}
        return (d.get("width") or 0) > (d.get("height") or 1)
    shots.sort(key=lambda m: (not is_wide(m), m["source_url"]))

    for i, m in enumerate(shots[:18]):
        name = "field-" + re.search(r"img_(\d+)", m["source_url"]).group(1)
        try:
            raw = get(m["source_url"], binary=True)
        except Exception as e:
            print(f"  ! {name}: {e}"); continue
        d = m.get("media_details") or {}
        # -sq для сеток и галереи, -1600 для лайтбокса
        save(raw, os.path.join(NURSERY, f"{name}-sq.webp"), 700, True, q=68)
        save(raw, os.path.join(NURSERY, f"{name}-1600.webp"), 1600, False, q=66)
        # широкие кропы 16:9 нужны только тем кадрам, что стоят баннерами
        if name in BANNERS:
            save(raw, os.path.join(NURSERY, f"{name}-w1920.webp"), 1920, False, q=68, ratio=16 / 9)
            save(raw, os.path.join(NURSERY, f"{name}-w1200.webp"), 1200, False, q=68, ratio=16 / 9)
        print(f"  {name}  {d.get('width')}x{d.get('height')}{'  [wide]' if is_wide(m) else ''}")

    json.dump(out, open(os.path.join(DATA, "catalog.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"\n{len(out)} products -> assets/data/catalog.json")


if __name__ == "__main__":
    sys.exit(main())
