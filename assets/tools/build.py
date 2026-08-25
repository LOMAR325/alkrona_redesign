# -*- coding: utf-8 -*-
"""
Сборка HTML-страниц сайта «Алькрона».

    python3 tools/build.py

Шапка, подвал и диалоги описаны здесь один раз и подставляются во все страницы,
поэтому меню и контакты не разъезжаются между index / catalog / care.
Содержимое каталога подставляется в браузере из assets/js/catalog-data.js.

Правьте разметку здесь, а не в готовых .html — они перезаписываются.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
os.chdir(ROOT)

from icons import icon  # noqa: E402

PHONE_HREF = "tel:+375293191844"
PHONE_TXT = "+375 (29) 319-18-44"
MAIL = "alkrona@inbox.ru"
ADDRESS = "микрорайон «Свислочь Новая», г.п. Свислочь, Минская область"
HOURS = "9:00–17:00, воскресенье — выходной"


def _v(path):
    """Метка версии по времени изменения файла — чтобы не жил старый кэш."""
    try:
        return "?v=%d" % os.path.getmtime(path)
    except OSError:
        return ""


# ============================================================ каркас страницы
def head(title, desc):
    return f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#1d4630">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ru_RU">
<link rel="icon" href="assets/img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="assets/img/logo-mark-128.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,400..700;1,7..72,400..600&family=Golos+Text:wght@400..700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css{_v("assets/css/styles.css")}">
</head>
<body>
<a class="skip" href="#main">Перейти к содержимому</a>
'''


NAV = [("catalog.html", "Каталог", "catalog"),
       ("#audience", "Покупателям", ""),
       ("#about", "О питомнике", ""),
       ("#buy", "Доставка и оплата", ""),
       ("care.html", "Уход", "care"),
       ("#contacts", "Контакты", "")]


def header(page="index"):
    cur = ' aria-current="page"'
    items = [(h if (page == "index" or not h.startswith("#")) else "index.html" + h, t, k)
             for h, t, k in NAV]
    links = "".join('<a href="%s"%s>%s</a>' % (h, cur if (k and k == page) else "", t)
                    for h, t, k in items)
    mob = "".join('<a href="%s">%s</a>' % (h, t) for h, t, k in items)
    return f'''
<div class="topbar">
  <div class="wrap">
    <span class="t-note" data-today>{HOURS}</span>
    <span style="display:flex;gap:20px;flex-wrap:wrap;align-items:center">
      <a href="{PHONE_HREF}">{icon("phone", 1.5)}{PHONE_TXT}</a>
      <a href="mailto:{MAIL}">{icon("mail", 1.5)}{MAIL}</a>
    </span>
  </div>
</div>

<header class="header">
  <div class="wrap nav">
    <a class="brand" href="index.html" aria-label="Алькрона — на главную">
      <img src="assets/img/logo-mark-128.png" alt="" width="42" height="41">
      <span class="brand-txt"><b>Алькрона</b><span>питомник растений</span></span>
    </a>
    <nav class="nav-links" aria-label="Основное меню">{links}</nav>
    <div class="nav-actions">
      <button class="icon-btn" data-req-open aria-label="Открыть заявку" aria-haspopup="dialog">
        {icon("bag")}<span class="badge" data-req-count aria-hidden="true">0</span>
      </button>
      <a class="btn btn-primary btn-sm nav-call" href="{PHONE_HREF}">Позвонить</a>
      <button class="icon-btn burger" data-burger aria-label="Меню" aria-expanded="false">{icon("menu")}</button>
    </div>
  </div>
</header>

<nav class="mobile-nav" aria-label="Мобильное меню">
  <div class="m-head">
    <span class="brand-txt"><b>Меню</b></span>
    <button class="icon-btn" data-close-nav aria-label="Закрыть меню">{icon("close")}</button>
  </div>
  {mob}
  <div class="m-foot">
    <a class="btn btn-primary btn-block" href="{PHONE_HREF}">{PHONE_TXT}</a>
    <a class="btn btn-outline btn-block" href="mailto:{MAIL}">{MAIL}</a>
    <p class="small muted">{ADDRESS}<br>{HOURS}</p>
  </div>
</nav>
'''


def footer(page="index"):
    home = "index.html"
    return f'''
<footer class="footer">
  <div class="wrap footer-top">
    <div class="fcol">
      <a class="brand" href="{home}" aria-label="Алькрона — на главную" style="margin-bottom:6px">
        <img src="assets/img/logo-mark-128.png" alt="" width="42" height="41">
        <span class="brand-txt"><b>Алькрона</b><span>питомник растений</span></span>
      </a>
      <p class="small">Питомник декоративных растений в Минской области. Собственное выращивание
         хвойных и лиственных культур для частных участков и объектов озеленения.</p>
      <p class="small">УНП 693278639</p>
    </div>
    <div class="fcol">
      <h3>Каталог</h3>
      <a href="catalog.html?cat=hvojnye-derevya-i-kustarniki">Хвойные</a>
      <a href="catalog.html?cat=listvennye-kustarniki">Лиственные кустарники</a>
      <a href="catalog.html">Весь ассортимент</a>
      <a href="catalog.html?sort=price-asc">Сначала недорогие</a>
    </div>
    <div class="fcol">
      <h3>Покупателям</h3>
      <a href="{home}#audience">Частным лицам</a>
      <a href="{home}#audience">Компаниям и оптом</a>
      <a href="{home}#buy">Самовывоз и доставка</a>
      <a href="{home}#buy">Оплата</a>
      <a href="care.html">Посадка и уход</a>
    </div>
    <div class="fcol">
      <h3>Контакты</h3>
      <a href="{PHONE_HREF}">{PHONE_TXT}</a>
      <a href="mailto:{MAIL}">{MAIL}</a>
      <p class="small">микрорайон «Свислочь Новая»,<br>г.п. Свислочь, Минская область</p>
      <p class="small">{HOURS}</p>
    </div>
  </div>
  <div class="wrap footer-bot">
    <span>© <span data-year>2026</span> Питомник «Алькрона»</span>
    <span>Самовывоз из питомника · доставка по Минску и области</span>
  </div>
</footer>
'''


DIALOGS = f'''
<div class="scrim" data-scrim></div>

<aside class="drawer" data-drawer role="dialog" aria-modal="true" aria-label="Заявка на растения">
  <div class="drawer-head">
    <h2 class="t-minor">Ваша заявка</h2>
    <button class="icon-btn" data-req-close aria-label="Закрыть заявку">{icon("close")}</button>
  </div>
  <div class="drawer-body" data-req-body></div>
  <div class="drawer-foot" data-req-foot></div>
</aside>

<div class="modal" data-modal role="dialog" aria-modal="true" aria-label="Карточка растения">
  <div class="modal-box"></div>
</div>

<div class="lightbox" data-lightbox role="dialog" aria-modal="true" aria-label="Просмотр фотографии">
  <img alt="" width="1600" height="1200">
  <button class="icon-btn round lb-close" aria-label="Закрыть просмотр">{icon("close")}</button>
  <button class="icon-btn round lb-nav lb-prev" aria-label="Предыдущее фото">{icon("chev-l")}</button>
  <button class="icon-btn round lb-nav lb-next" aria-label="Следующее фото">{icon("chev-r")}</button>
  <p class="lb-cap"></p>
</div>
'''

SCRIPTS = '''
<script src="assets/js/catalog-data.js%s" defer></script>
<script src="assets/js/app.js%s" defer></script>
</body>
</html>
''' % (_v("assets/js/catalog-data.js"), _v("assets/js/app.js"))


# ============================================================ схема проезда
def locator():
    """Своя схема проезда: без чужого виджета с его служебными ссылками."""
    trees = "".join(
        f'<g transform="translate({x} {y}) scale({s})" opacity=".72">'
        f'<path d="M0 12V6" stroke="#4a8560" stroke-width="1.6" stroke-linecap="round"/>'
        f'<path d="M0 7c0-4 2-6 6-6 0 4-2 6-6 6z" fill="#7aa887"/>'
        f'<path d="M0 9c0-3.4-1.8-5-5-5 0 3.4 1.8 5 5 5z" fill="#5e9070"/></g>'
        for (x, y, s) in [(96, 236, 2.3), (152, 272, 1.7), (208, 214, 2.0), (588, 186, 2.1),
                          (548, 250, 1.7), (668, 236, 1.8), (326, 306, 1.9), (438, 322, 1.6),
                          (262, 268, 1.5), (500, 300, 1.7)])
    fields = "".join(
        f'<path d="{d}" fill="#e4edd8" stroke="#cfdcbe" stroke-width="1.4"/>'
        for d in ["M40 268q120-26 210 6t250-18 180-40v150H40z",
                  "M40 196q90-20 170 2t150-14 210-30v56q-90 26-200 40t-190-10-140-12z"])
    return f'''<svg viewBox="0 0 720 380" role="img"
     aria-label="Схема проезда: питомник «Алькрона» в г.п. Свислочь, примерно 40 километров юго-восточнее Минска">
  <rect width="720" height="380" fill="#f4f1e6"/>
  {fields}
  <g opacity=".35" stroke="#c9bfa6" stroke-width="1" stroke-dasharray="3 7">
    <path d="M0 90h720M0 180h720M0 270h720M180 0v380M360 0v380M540 0v380"/>
  </g>
  {trees}

  <!-- дорога Минск → Свислочь -->
  <path d="M118 118C230 118 268 176 352 200s188 8 250 62"
        fill="none" stroke="#cdbe9c" stroke-width="13" stroke-linecap="round"/>
  <path d="M118 118C230 118 268 176 352 200s188 8 250 62"
        fill="none" stroke="#fdfbf5" stroke-width="3" stroke-dasharray="10 12" stroke-linecap="round"/>

  <!-- Минск -->
  <g transform="translate(70 78)">
    <circle r="26" fill="#e6ded0" stroke="#c9bfa6" stroke-width="1.6"/>
    <path d="M-11 8v-11h7v11M-2 8v-16h7v16M8 8v-8h5v8" fill="none" stroke="#8a8064" stroke-width="1.8" stroke-linejoin="round"/>
    <text x="0" y="46" text-anchor="middle" font-family="Golos Text, sans-serif"
          font-size="16" font-weight="600" fill="#3b463e">Минск</text>
  </g>

  <!-- расстояние -->
  <g transform="translate(330 156)">
    <rect x="-52" y="-16" width="104" height="30" rx="9" fill="#fffdf8" stroke="#e2d9c6"/>
    <text x="0" y="4" text-anchor="middle" font-family="Golos Text, sans-serif"
          font-size="14" font-weight="600" fill="#ad5334">≈ 40 км</text>
  </g>

  <!-- питомник -->
  <g transform="translate(612 268)">
    <circle r="30" fill="#2f6b45" opacity=".12"/>
    <circle r="19" fill="#2f6b45" opacity=".2"/>
    <path d="M0-30c7.6 0 13.6 6 13.6 13.6C13.6-6.4 0 8 0 8s-13.6-14.4-13.6-24.4C-13.6-24 -7.6-30 0-30z"
          fill="#2f6b45"/>
    <circle cy="-16.4" r="5" fill="#fffdf8"/>
    <text x="0" y="52" text-anchor="middle" font-family="Golos Text, sans-serif"
          font-size="16" font-weight="600" fill="#1d4630">Свислочь</text>
    <text x="0" y="72" text-anchor="middle" font-family="Golos Text, sans-serif"
          font-size="13" fill="#5b665d">питомник «Алькрона»</text>
  </g>

  <!-- север -->
  <g transform="translate(672 56)" opacity=".7">
    <path d="M0-20 6 4 0-2-6 4z" fill="#8a8064"/>
    <text x="0" y="20" text-anchor="middle" font-family="Golos Text, sans-serif"
          font-size="12" font-weight="600" fill="#5b665d">С</text>
  </g>
</svg>'''


# ============================================================ главная
index_main = f'''
<main id="main">

  <!-- ======================= ХИРО ======================= -->
  <section class="hero">
    <div class="hero-media">
      <img src="assets/img/nursery/field-3894-w1920.webp"
           srcset="assets/img/nursery/field-3894-w1200.webp 1200w,
                   assets/img/nursery/field-3894-w1920.webp 1920w"
           sizes="100vw"
           alt="Ряды контейнерных растений в питомнике «Алькрона» под Свислочью"
           width="1920" height="1080" fetchpriority="high" decoding="async">
    </div>
    <div class="wrap hero-inner">
      <div class="hero-copy">
        <span class="hero-kicker">{icon("branch", 1.35)}Свислочь, Минская область</span>
        <h1>Хвойные и <span class="em">лиственные</span><br>для сада, изгороди<br>и озеленения</h1>
        <p class="lede">Выращиваем сами: от укоренения до отгрузки, с проверкой корневой системы
           перед каждой отправкой. Подбираем растения под конкретный участок — частный сад,
           ландшафтный проект или объект.</p>
        <div class="hero-cta">
          <a class="btn btn-primary btn-lg" href="catalog.html">Смотреть каталог {icon("arrow", 1.9)}</a>
          <a class="btn btn-white btn-lg btn-pill" href="#audience">Опт и компаниям</a>
        </div>
      </div>

      <div class="hero-facts">
        <div><b>100<span class="accent">+</span></b><span>видов и сортов в ассортименте</span></div>
        <div><b>40</b><span>позиций в наличии прямо сейчас</span></div>
        <div><b>Своё</b><span>выращивание и уход, без перекупки</span></div>
        <div><b>10–30<span class="accent"> км</span></b><span>доставка в радиусе от Минска</span></div>
      </div>
    </div>
  </section>

  <!-- ======================= ЧТО ВЫРАЩИВАЕМ — асимметричный сплит ======================= -->
  <section class="section" id="categories" style="padding-top:clamp(84px,9vw,132px)">
    <div class="wrap grow">
      <div class="grow-head">
        <span class="mark-num" aria-hidden="true">01</span>
        <h2 class="t-major">Что растёт<br>на наших полях</h2>
        <p class="lede">Хвойные формы держат сад зимой, лиственные дают цвет и объём летом.
           Мы выращиваем и то и другое — и подскажем, что уживётся именно у вас.</p>
        <a class="link-arrow" href="catalog.html">Весь каталог, 40 позиций {icon("arrow", 1.9)}</a>
      </div>

      <a class="grow-lead" href="catalog.html?cat=hvojnye-derevya-i-kustarniki">
        <img src="assets/img/nursery/field-3924-sq.webp"
             alt="Туи и можжевельники на площадке питомника" width="700" height="700"
             loading="lazy" decoding="async">
        <span class="cap">
          <h3>Хвойные деревья и кустарники</h3>
          <p>Туи, можжевельники, сосны — для живых изгородей, акцентов и альпинариев.
             7 позиций в наличии.</p>
        </span>
      </a>
    </div>

    <div class="wrap" style="margin-top:clamp(16px,2vw,24px)">
      <div class="grow-side" style="grid-template-columns:1fr 1fr;display:grid">
        <a class="grow-card" href="catalog.html?cat=listvennye-kustarniki">
          <img src="assets/img/nursery/field-3826-sq.webp" alt="Спиреи в осенней окраске"
               width="700" height="700" loading="lazy" decoding="async">
          <span>
            <h3>Лиственные кустарники</h3>
            <p>Спиреи, дёрен, пузыреплодник, гортензии, лапчатка, форзиция.</p>
            <span class="n">33 позиции</span>
          </span>
        </a>
        <a class="grow-card" href="catalog.html?cat=&amp;sort=height-desc">
          <img src="assets/img/nursery/field-3897-sq.webp" alt="Ряды крупных хвойных"
               width="700" height="700" loading="lazy" decoding="async">
          <span>
            <h3>Крупномер и изгороди</h3>
            <p>Растения от метра высотой — когда результат нужен сразу, а не через пять лет.</p>
            <span class="n">Смотреть по высоте</span>
          </span>
        </a>
      </div>
    </div>
  </section>

  <!-- ======================= ЛЕНТА КАТАЛОГА ======================= -->
  <section class="section-tight section-sand" id="popular" style="overflow:hidden">
    <div class="wrap">
      <div class="ribbon-head">
        <div>
          <h2>В наличии в питомнике</h2>
          <p class="muted small" style="margin-top:6px">Часть позиций — по запросу: цена зависит
             от размера и объёма партии.</p>
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap" role="group" aria-label="Фильтр по типу">
          <button class="chip" data-cat-chip="all" aria-pressed="true">Все</button>
          <button class="chip" data-cat-chip="hvojnye-derevya-i-kustarniki" aria-pressed="false">Хвойные</button>
          <button class="chip" data-cat-chip="listvennye-kustarniki" aria-pressed="false">Лиственные</button>
        </div>
      </div>
    </div>

    <div class="wrap ribbon-wrap">
      <div class="ribbon" data-grid tabindex="0" role="region" aria-label="Растения в наличии"></div>
      <div style="display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between;margin-top:8px">
        <span class="ribbon-hint">{icon("swipe", 1.5)}Листайте вбок — показаны первые десять</span>
        <a class="link-arrow" href="catalog.html">Открыть весь каталог {icon("arrow", 1.9)}</a>
      </div>
    </div>
  </section>

  <!-- ======================= КОМУ ПОДХОДИМ ======================= -->
  <section class="section" id="audience">
    <div class="wrap">
      <div style="max-width:62ch;margin-bottom:clamp(26px,3vw,40px)">
        <span class="mark-num" aria-hidden="true">02</span>
        <h2 class="t-major">Частный сад и объект<br>покупают по-разному</h2>
      </div>

      <div class="aud-grid">
        <div class="aud">
          <span class="aud-mark">{icon("plot", 1.25)}</span>
          <div>
            <h3 class="t-minor">Частным лицам</h3>
            <p class="muted" style="margin-top:6px">Сад у дома, дача, входная зона,
               живая изгородь вдоль забора.</p>
          </div>
          <ul class="aud-list">
            <li>{icon("leafcheck", 1.5)}<span>Любое количество — хоть один куст</span></li>
            <li>{icon("leafcheck", 1.5)}<span>Поможем выбрать вид и размер под освещённость и почву на участке</span></li>
            <li>{icon("leafcheck", 1.5)}<span>Самовывоз: можно посмотреть растения в поле и выбрать конкретный экземпляр</span></li>
            <li>{icon("leafcheck", 1.5)}<span>Рекомендации по посадке и уходу в первые месяцы</span></li>
          </ul>
          <a class="btn btn-primary" href="catalog.html">Перейти в каталог</a>
        </div>

        <div class="aud aud-b">
          <span class="aud-mark">{icon("crates", 1.25)}</span>
          <div>
            <h3 class="t-minor">Ландшафтным компаниям и оптом</h3>
            <p style="margin-top:6px;color:#b9d0c1">Проекты озеленения, благоустройство территорий,
               застройка, садовые центры.</p>
          </div>
          <ul class="aud-list">
            <li>{icon("leafcheck", 1.5)}<span>Оптовые партии и подбор под проект: высота, возраст, форма кроны, плотность посадки</span></li>
            <li>{icon("leafcheck", 1.5)}<span>Подбор под смету и сроки — предложим замену, если позиции нет в нужном объёме</span></li>
            <li>{icon("leafcheck", 1.5)}<span>Безналичный расчёт, УНП 693278639, полный пакет документов</span></li>
            <li>{icon("leafcheck", 1.5)}<span>Регулярные поставки садовым центрам в течение сезона</span></li>
          </ul>
          <a class="btn btn-white" href="#contacts">Запросить прайс и наличие</a>
        </div>
      </div>
    </div>
  </section>

  <!-- ======================= О ПИТОМНИКЕ — полоса во всю ширину ======================= -->
  <section class="band" id="about">
    <div class="band-media">
      <img src="assets/img/nursery/field-3942-w1920.webp"
           srcset="assets/img/nursery/field-3942-w1200.webp 1200w,
                   assets/img/nursery/field-3942-w1920.webp 1920w"
           sizes="100vw"
           alt="Поля питомника «Алькрона» под Свислочью" width="1920" height="1080"
           loading="lazy" decoding="async">
    </div>
    <div class="band-inner">
      <div class="wrap band-wrap">
        <div class="band-copy">
          <span class="mark-leaf" style="color:#e3c08a">{icon("leaf", 1.35)}О питомнике</span>
          <h2 class="t-major">Мы не перепродаём растения —<br>мы их выращиваем</h2>
          <p class="lede">Полный цикл проходит здесь же, в Свислочи: укоренение, регулярный уход,
             пересадка в больший объём. Поэтому мы отвечаем за то, что вы получаете,
             и знаем историю каждой партии.</p>
          <ul class="checks">
            <li>{icon("leafcheck", 1.4)}<div><b>Проверка перед отгрузкой</b>
              <span>Смотрим корневую систему, состояние кроны и побегов у каждого растения —
              от этого зависит приживаемость в первый сезон.</span></div></li>
            <li>{icon("snow", 1.4)}<div><b>Районированный материал</b>
              <span>Растения выращены здесь и привыкли к местной зиме. Никакой акклиматизации
              после импортной поставки не требуется.</span></div></li>
            <li>{icon("sun", 1.4)}<div><b>Подбор под условия участка</b>
              <span>Учитываем состав почвы, освещённость, размер территории, сроки посадки
              и задачу по декоративности.</span></div></li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <div class="wrap">
    <div class="band-stats">
      <div><b>100+</b><span>видов и сортов выращиваем на своих полях</span></div>
      <div><b>4</b><span>типа заказчиков: частные сады, ландшафт, застройка, садовые центры</span></div>
      <div><b>9:00–17:00</b><span>работаем шесть дней в неделю, воскресенье — выходной</span></div>
    </div>
  </div>

  <!-- ======================= КАК КУПИТЬ ======================= -->
  <section class="section" id="buy" style="padding-top:clamp(56px,7vw,96px)">
    <div class="wrap buy">
      <div>
        <span class="mark-num" aria-hidden="true">03</span>
        <h2 class="t-major" style="margin-bottom:18px">Как проходит<br>покупка</h2>
        <ol class="timeline">
          <li><span class="num">1</span>
            <div><b>Соберите заявку</b>
              <p>Добавьте растения из каталога кнопкой «В заявку» — или просто позвоните
                 и опишите задачу словами.</p></div></li>
          <li><span class="num">2</span>
            <div><b>Подтверждаем наличие и цену</b>
              <p>Часть позиций продаётся по запросу: цена зависит от размера растения
                 и объёма партии.</p></div></li>
          <li><span class="num">3</span>
            <div><b>Согласуем самовывоз или доставку</b>
              <p>Дату, время и способ оплаты — наличный или безналичный расчёт.</p></div></li>
          <li><span class="num">4</span>
            <div><b>Проверяем и отгружаем</b>
              <p>Перед отправкой смотрим корневую систему и крону, готовим растения
                 к перевозке.</p></div></li>
        </ol>
      </div>

      <div class="buy-cards">
        <div class="buy-card">
          <h3 class="t-minor">{icon("pin", 1.35)}Самовывоз из питомника</h3>
          <p class="muted">Приезжайте — покажем растения в поле, поможем выбрать конкретные
             экземпляры и погрузим. Самый удобный вариант, если хотите видеть, что берёте.</p>
          <div class="kv">
            <div><span class="k">Адрес</span><span class="v">микрорайон «Свислочь Новая»,<br>г.п. Свислочь, Минская область</span></div>
            <div><span class="k">График</span><span class="v">9:00–17:00<br>воскресенье — выходной</span></div>
            <div><span class="k">Перед приездом</span><span class="v">позвоните — подготовим растения к вашему визиту</span></div>
          </div>
          <a class="btn btn-outline" href="{PHONE_HREF}">{icon("phone", 1.5)}{PHONE_TXT}</a>
        </div>

        <div class="buy-card tight">
          <h3 class="t-minor">{icon("route", 1.35)}Доставка</h3>
          <div class="kv">
            <div><span class="k">Зона</span><span class="v">Минск и радиус 10–30 км от города</span></div>
            <div><span class="k">Условие</span><span class="v">при заказе от 500 руб</span></div>
            <div><span class="k">Стоимость</span><span class="v">согласовывается с менеджером</span></div>
          </div>
        </div>

        <div class="buy-card tight">
          <h3 class="t-minor">{icon("wallet", 1.35)}Оплата</h3>
          <p class="muted">Наличный и безналичный расчёт. Для организаций — полный пакет
             документов, УНП 693278639.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- ======================= УХОД ======================= -->
  <section class="section section-sand" id="care">
    <div class="wrap">
      <div style="display:flex;flex-wrap:wrap;gap:20px;align-items:flex-end;justify-content:space-between;margin-bottom:clamp(24px,3vw,40px)">
        <div style="max-width:46ch">
          <span class="mark-leaf">{icon("watering", 1.35)}После покупки</span>
          <h2 class="t-major" style="margin-top:12px">Чтобы прижилось</h2>
        </div>
        <a class="link-arrow" href="care.html">Подробные рекомендации {icon("arrow", 1.9)}</a>
      </div>

      <div class="care-grid">
        <article class="care">
          <div class="care-media">
            <img src="assets/img/nursery/field-3971-w1200.webp" alt="" width="1200" height="675" loading="lazy" decoding="async">
          </div>
          <div class="care-body">
            <span class="care-ico">{icon("sprout", 1.35)}В день посадки</span>
            <h3>Как посадить куст, чтобы он прижился</h3>
            <ul>
              <li>Яма в 1,5–2 раза шире земляного кома</li>
              <li>Корневая шейка — на уровне почвы, не заглублять</li>
              <li>Обильный полив сразу после посадки, даже в дождь</li>
              <li>Мульча 5–7 см: кора, щепа или торф</li>
            </ul>
          </div>
        </article>
        <article class="care">
          <div class="care-media">
            <img src="assets/img/nursery/field-4154-w1200.webp" alt="" width="1200" height="675" loading="lazy" decoding="async">
          </div>
          <div class="care-body">
            <span class="care-ico">{icon("watering", 1.35)}Первый сезон</span>
            <h3>Полив и подкормка в первый год</h3>
            <ul>
              <li>Полив раз в 5–7 дней, в жару — чаще</li>
              <li>10–20 л под взрослый куст, под корень, не по листу</li>
              <li>Первая подкормка — только следующей весной</li>
              <li>Приствольный круг держать без сорняков</li>
            </ul>
          </div>
        </article>
        <article class="care">
          <div class="care-media">
            <img src="assets/img/nursery/field-3748-w1200.webp" alt="" width="1200" height="675" loading="lazy" decoding="async">
          </div>
          <div class="care-body">
            <span class="care-ico">{icon("snow", 1.35)}Перед морозами</span>
            <h3>Что сделать осенью</h3>
            <ul>
              <li>Влагозарядковый полив в октябре</li>
              <li>Мульчирование корневой зоны на 8–10 см</li>
              <li>Хвойные — притенение от февральского солнца</li>
              <li>Молодые посадки первого года — укрыть лапником</li>
            </ul>
          </div>
        </article>
      </div>
    </div>
  </section>

  <!-- ======================= ГАЛЕРЕЯ ======================= -->
  <section class="section-tight" id="gallery" style="padding-block:clamp(44px,5vw,72px)">
    <div class="wrap">
      <div style="display:flex;flex-wrap:wrap;gap:16px;align-items:baseline;justify-content:space-between;margin-bottom:20px">
        <h2>Как это выглядит вживую</h2>
        <p class="small muted">Наши поля и площадки в Свислочи — снято на месте, в рабочем порядке</p>
      </div>
      <div class="gallery">{{gallery}}</div>
    </div>
  </section>

  <!-- ======================= КОНТАКТЫ ======================= -->
  <section class="section" id="contacts">
    <div class="wrap">
      <div style="max-width:50ch;margin-bottom:clamp(24px,3vw,38px)">
        <span class="mark-num" aria-hidden="true">04</span>
        <h2 class="t-major">Напишите нам</h2>
        <p class="lede" style="margin-top:12px">Ответим в рабочее время. Если вы собрали заявку
           в каталоге, она подставится в сообщение автоматически.</p>
      </div>

      <div class="contact-grid">
        <form class="contact-card form" data-form data-order-form novalidate>
          <div class="two">
            <div class="field">
              <label for="f-name">Как к вам обращаться</label>
              <input id="f-name" name="name" type="text" required autocomplete="name" placeholder="Иван Петрович">
              <span class="msg" aria-live="polite"></span>
            </div>
            <div class="field">
              <label for="f-phone">Телефон</label>
              <input id="f-phone" name="phone" type="tel" required autocomplete="tel" placeholder="+375 29 000 00 00">
              <span class="msg" aria-live="polite"></span>
            </div>
          </div>
          <div class="field">
            <label for="f-email">Электронная почта <span class="muted">— если удобнее письмом</span></label>
            <input id="f-email" name="email" type="email" autocomplete="email" placeholder="name@example.com">
          </div>
          <div class="field">
            <label for="f-who">Вы обращаетесь как</label>
            <select id="f-who" name="who">
              <option>Частное лицо — сад или дача</option>
              <option>Ландшафтная компания — проект</option>
              <option>Застройщик — благоустройство территории</option>
              <option>Садовый центр — закупка партии</option>
            </select>
          </div>
          <div class="field">
            <label for="f-msg">Что нужно</label>
            <textarea id="f-msg" name="message" required
              placeholder="Опишите задачу: какие растения, сколько, на какой участок, к какому сроку."></textarea>
            <span class="msg" aria-live="polite"></span>
          </div>
          <label class="consent">
            <input type="checkbox" name="consent" required>
            <span>Согласен на обработку персональных данных для ответа на заявку</span>
          </label>
          <button class="btn btn-primary btn-lg" type="submit">Отправить заявку</button>
          <div class="form-ok" data-form-done hidden>{icon("check", 2)}
            <span>Заявка отправлена. Перезвоним в рабочее время.</span></div>
        </form>

        <div style="display:grid;gap:clamp(16px,2vw,22px)">
          <div class="contact-card">
            <div class="contact-rows">
              <div class="crow">{icon("phone", 1.35)}<div><b>Телефон</b>
                <a href="{PHONE_HREF}">{PHONE_TXT}</a></div></div>
              <div class="crow">{icon("mail", 1.35)}<div><b>Почта</b>
                <a href="mailto:{MAIL}">{MAIL}</a></div></div>
              <div class="crow">{icon("pin", 1.35)}<div><b>Питомник</b>
                <span>{ADDRESS}</span></div></div>
              <div class="crow">{icon("clock", 1.35)}<div><b>График работы</b>
                <span>{HOURS}</span></div></div>
              <div class="crow">{icon("wallet", 1.35)}<div><b>Реквизиты</b>
                <span>УНП 693278639 · наличный и безналичный расчёт</span></div></div>
            </div>
          </div>

          <div class="locator">
            {{locator}}
            <div class="locator-foot">
              <span><b>г.п. Свислочь, Минская область</b>
                <span>Схема проезда · примерно 40 км юго-восточнее Минска</span></span>
              <a class="btn btn-outline btn-sm" target="_blank" rel="noopener"
                 href="https://yandex.by/maps/?text=Свислочь%20Минская%20область">Открыть в картах</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</main>
'''

GALLERY = [
    ("3894", "Ряды контейнерных растений в питомнике"),
    ("3924", "Туи и можжевельники на площадке"),
    ("3826", "Спиреи в осенней окраске"),
    ("3897", "Живая изгородь из хвойных"),
    ("3942", "Поля питомника под Свислочью"),
    ("3709", "Дёрен и спирея, подготовка к отгрузке"),
    ("3721", "Контейнеры С3 и С5 на площадке"),
    ("3685", "Гортензии и кустарники в поле"),
]


def gallery():
    return "".join(
        f'<button data-shot="assets/img/nursery/field-{fid}-1600.webp" data-cap="{cap}" '
        f'aria-label="Открыть фото: {cap}">'
        f'<img src="assets/img/nursery/field-{fid}-sq.webp" alt="{cap}" '
        f'width="700" height="700" loading="lazy" decoding="async"></button>'
        for fid, cap in GALLERY)


open("index.html", "w", encoding="utf-8").write(
    head("Питомник декоративных растений «Алькрона» — хвойные и кустарники, Минская область",
         "Питомник Алькрона в Свислочи Минской области: собственное выращивание хвойных и "
         "лиственных декоративных кустарников. Каталог, самовывоз и доставка по Минску и области. "
         "Тел. +375 (29) 319-18-44.")
    + header("index")
    + index_main.replace("{gallery}", gallery()).replace("{locator}", locator())
    + footer("index") + DIALOGS + SCRIPTS)
print("index.html")


# ============================================================ каталог
catalog_main = f'''
<main id="main">
  <section class="page-head">
    <div class="wrap">
      <nav class="crumbs" aria-label="Хлебные крошки">
        <a href="index.html">Главная</a><span aria-hidden="true">/</span><span>Каталог</span>
      </nav>
      <h1 class="t-major">Каталог растений</h1>
      <p class="lede" style="margin-top:12px">Хвойные и лиственные декоративные культуры
         собственного выращивания. Отфильтруйте по типу, высоте, размеру горшка и цене —
         или соберите заявку, и мы подтвердим наличие.</p>
    </div>
  </section>

  <section class="section" style="padding-top:clamp(24px,3vw,40px)">
    <div class="wrap wrap-wide catalog-layout">

      <aside class="filters" aria-label="Фильтры каталога">
        <div class="f-head">
          <b>Фильтры</b>
          <button class="icon-btn" data-filters-close aria-label="Закрыть фильтры">{icon("close")}</button>
        </div>
        <div data-filters></div>
      </aside>

      <div>
        <div class="toolbar">
          <label class="search">
            <span class="sr">Поиск по каталогу</span>
            {icon("search", 1.5)}
            <input type="search" data-q placeholder="Поиск: туя, спирея, дёрен, ALK-0021…" autocomplete="off">
          </label>
          <div class="select">
            <label class="sr" for="sort">Сортировка</label>
            <select id="sort" data-sort>
              <option value="default">Сначала в наличии</option>
              <option value="name">По названию, А–Я</option>
              <option value="price-asc">Сначала недорогие</option>
              <option value="price-desc">Сначала дорогие</option>
              <option value="height-desc">Сначала крупные</option>
              <option value="height-asc">Сначала компактные</option>
            </select>
          </div>
          <button class="btn btn-outline btn-sm filters-toggle" data-filters-toggle>
            {icon("filter", 1.6)}Фильтры
          </button>
          <span class="count" data-count aria-live="polite"></span>
        </div>

        <div class="grid-products" data-grid data-full></div>

        <div class="callout" style="margin-top:clamp(26px,3vw,40px)">
          {icon("info", 1.4)}
          <div><b>Часть позиций продаётся по запросу.</b>
            <span> Цена зависит от размера растения и объёма партии — особенно на хвойных
            и крупномере. Соберите заявку или позвоните: {PHONE_TXT}.</span></div>
        </div>
      </div>
    </div>
  </section>
</main>
'''

open("catalog.html", "w", encoding="utf-8").write(
    head("Каталог растений — питомник «Алькрона», Минская область",
         "Каталог питомника Алькрона: хвойные деревья и кустарники, лиственные декоративные "
         "кустарники. Фильтр по типу, высоте, размеру горшка и цене. Самовывоз и доставка.")
    + header("catalog") + catalog_main + footer("catalog") + DIALOGS + SCRIPTS)
print("catalog.html")


# ============================================================ посадка и уход
TOC = [("when", "Когда сажать"), ("planting", "Посадка"), ("water", "Полив"),
       ("mulch", "Мульчирование"), ("feed", "Подкормка"), ("prune", "Обрезка"),
       ("winter", "Подготовка к зиме"), ("mistakes", "Частые ошибки")]

care_main = f'''
<main id="main">
  <section class="page-head">
    <div class="wrap">
      <nav class="crumbs" aria-label="Хлебные крошки">
        <a href="index.html">Главная</a><span aria-hidden="true">/</span><span>Посадка и уход</span>
      </nav>
      <h1 class="t-major">Посадка и уход<br>после покупки</h1>
      <p class="lede" style="margin-top:12px">То, что мы рассказываем покупателям при отгрузке.
         Рекомендации для условий Минской области — хвойные и лиственные декоративные кустарники
         в контейнере и с открытой корневой системой.</p>
    </div>
  </section>

  <section class="section" style="padding-top:clamp(24px,3vw,44px)">
    <div class="wrap doc">
      <nav class="toc" aria-label="Содержание">
        <h4>Содержание</h4>
        {"".join(f'<a href="#{i}">{t}</a>' for i, t in TOC)}
      </nav>

      <div class="doc-body">
        <section id="when">
          <h2>Когда сажать</h2>
          <p>Контейнерные растения (в горшках С2, С3, С5 и больше) можно высаживать весь тёплый
             сезон — с апреля по октябрь, пока земля не промёрзла. Ком не разрушается, корни
             не травмируются, поэтому жёсткого «окна» нет.</p>
          <p>Растения с открытой корневой системой (ОКС) сажают только в состоянии покоя:
             ранней весной до распускания почек или осенью после листопада.</p>
          <div class="callout">{icon("info", 1.4)}
            <div><b>Лучшее время — конец августа и сентябрь.</b>
              <span> Земля ещё тёплая, воздух уже прохладный, дождей больше. Корни успевают
              освоиться до морозов, а надземная часть не тратит силы на жару.</span></div>
          </div>
        </section>

        <section id="planting">
          <h2>Посадка</h2>
          <ol class="num">
            <li><span><b>Яма.</b> В 1,5–2 раза шире земляного кома и примерно на его глубину.
                Стенки лучше разрыхлить, чтобы корни не упирались в плотный грунт.</span></li>
            <li><span><b>Дренаж — по ситуации.</b> На тяжёлой глине и в низинах — 10–15 см щебня
                или керамзита. На нормальной почве дренаж не нужен.</span></li>
            <li><span><b>Достаньте растение аккуратно.</b> Контейнер снимайте, не выдёргивая
                за ствол. Если корни свились плотным войлоком — надрежьте ком по бокам
                в 3–4 местах, иначе корни продолжат расти по кругу.</span></li>
            <li><span><b>Уровень.</b> Корневая шейка — вровень с землёй. Заглубление
                и «посадка в ямку» — самая частая причина гибели хвойных.</span></li>
            <li><span><b>Засыпьте и уплотните.</b> Землю подсыпайте слоями, слегка приминая,
                чтобы не осталось пустот у корней.</span></li>
            <li><span><b>Полейте сразу.</b> 10–20 л на куст, даже если идёт дождь: вода
                уплотняет грунт вокруг корней.</span></li>
            <li><span><b>Замульчируйте.</b> Слой 5–7 см коры, щепы или торфа, не прижимая
                мульчу к стволу.</span></li>
          </ol>
          <div class="callout warn">{icon("warn", 1.4)}
            <div><b>Не вносите свежий навоз и не «удобряйте на всякий случай».</b>
              <span> В первый месяц растению нужна вода и покой, а не питание — свежая
              органика обжигает молодые корни.</span></div>
          </div>
        </section>

        <section id="water">
          <h2>Полив в первый сезон</h2>
          <p>Первый год — самый важный. Пока корни не вышли за пределы посадочной ямы,
             растение полностью зависит от вас.</p>
          <ul class="bul">
            <li>Раз в 5–7 дней, в жару и на песчаных почвах — чаще.</li>
            <li>10–20 л под взрослый куст, 5–10 л под небольшой. Лучше реже, но обильно,
                чем каждый день понемногу.</li>
            <li>Поливать под корень, а не по листу: мокрая листва на солнце получает ожоги,
                а в сырую погоду — грибные болезни.</li>
            <li>Хвойные полезно дождевать по кроне в сухую погоду — рано утром или вечером.</li>
          </ul>
          <div class="callout">{icon("info", 1.4)}
            <div><b>Как проверить.</b>
              <span> Разгребите мульчу и копните на 5–7 см. Земля влажная и лепится —
              полив не нужен, рассыпается — пора поливать.</span></div>
          </div>
        </section>

        <section id="mulch">
          <h2>Мульчирование</h2>
          <p>Мульча удерживает влагу, не даёт почве перегреваться и растрескиваться, подавляет
             сорняки и защищает корни зимой. Для хвойных подходит сосновая кора и щепа,
             для лиственных — кора, щепа, компост.</p>
          <ul class="bul">
            <li>Слой 5–7 см, к зиме под молодыми посадками — до 8–10 см.</li>
            <li>Не насыпать вплотную к стволу: между мульчой и корой оставьте 3–5 см.</li>
            <li>Обновлять раз в 1–2 года, по мере перепревания.</li>
          </ul>
        </section>

        <section id="feed">
          <h2>Подкормка</h2>
          <p>В год посадки растение не подкармливают — в субстрате достаточно питания,
             а лишние удобрения мешают укоренению.</p>
          <ul class="bul">
            <li><b>Весна (апрель–май):</b> комплексное удобрение с преобладанием азота —
                на рост побегов.</li>
            <li><b>Лето (июнь):</b> полное комплексное удобрение, если куст ослаблен
                или сильно цветёт.</li>
            <li><b>Конец лета (август):</b> только калийно-фосфорное. Азот после июля
                не вносить — он гонит молодые побеги, которые не успевают вызреть
                и вымерзают.</li>
            <li>Для хвойных берите специализированные удобрения: им нужен другой баланс
                и слегка кислая реакция почвы.</li>
          </ul>
        </section>

        <section id="prune">
          <h2>Обрезка</h2>
          <ul class="bul">
            <li><b>Санитарная</b> — в любое время: сухие, сломанные и больные ветви.</li>
            <li><b>Спирея японская, лапчатка, пузыреплодник, дёрен</b> цветут на побегах
                текущего года — стригут ранней весной, до распускания почек. Не бойтесь
                короткой обрезки: куст ответит густым приростом.</li>
            <li><b>Спирея серая и Вангутта</b> цветут на прошлогодних побегах — обрезают
                сразу после цветения, иначе останетесь без цветов.</li>
            <li><b>Гортензия метельчатая</b> — весной, укорачивая прошлогодние побеги
                на 2–4 почки.</li>
            <li><b>Дёрен с цветной корой</b> раз в 2–3 года срезают почти на пень:
                яркая кора бывает только у молодых побегов.</li>
            <li><b>Туи и можжевельники</b> стригут в мае–июне и при необходимости
                в августе, снимая не больше трети прироста и не заходя в старую древесину.</li>
          </ul>
        </section>

        <section id="winter">
          <h2>Подготовка к зиме</h2>
          <ul class="bul">
            <li><b>Влагозарядковый полив</b> в октябре, до устойчивых заморозков — особенно
                важен для хвойных, которые испаряют влагу и зимой.</li>
            <li><b>Мульчирование</b> корневой зоны слоем 8–10 см.</li>
            <li><b>Притенение хвойных</b> в конце зимы: в феврале–марте солнце отражается
                от снега и обжигает хвою, пока корни в мёрзлой земле. Спасает притеняющая
                сетка или лапник с южной стороны.</li>
            <li><b>Обвязка колоновидных туй</b> мягким шпагатом — чтобы мокрый снег
                не разваливал крону.</li>
            <li><b>Молодые посадки первого года</b> дополнительно укрывают лапником.</li>
          </ul>
          <div class="callout warn">{icon("warn", 1.4)}
            <div><b>Не укрывайте плёнкой и плотным нетканым материалом наглухо.</b>
              <span> Под ними растения выпревают в оттепель. Укрытие должно дышать.</span></div>
          </div>
        </section>

        <section id="mistakes">
          <h2>Частые ошибки</h2>
          <ul class="bul">
            <li>Заглубление корневой шейки при посадке.</li>
            <li>Частый поверхностный полив вместо редкого и обильного.</li>
            <li>Азотные подкормки в августе — побеги не вызревают и вымерзают.</li>
            <li>Посадка светолюбивых хвойных в тень: крона редеет и теряет форму.</li>
            <li>Мульча, насыпанная вплотную к стволу — кора преет.</li>
            <li>Отсутствие притенения хвойных в конце зимы.</li>
          </ul>
          <div class="callout">{icon("info", 1.4)}
            <div><b>Остались вопросы?</b>
              <span> Позвоните — подскажем по конкретному растению и участку:
              <a href="{PHONE_HREF}">{PHONE_TXT}</a>.</span></div>
          </div>
        </section>

        <div style="display:flex;gap:12px;flex-wrap:wrap">
          <a class="btn btn-primary" href="catalog.html">Перейти в каталог {icon("arrow", 1.9)}</a>
          <a class="btn btn-outline" href="index.html#contacts">Задать вопрос</a>
        </div>
      </div>
    </div>
  </section>
</main>
'''

open("care.html", "w", encoding="utf-8").write(
    head("Посадка и уход за декоративными растениями — питомник «Алькрона»",
         "Как посадить и ухаживать за хвойными и декоративными кустарниками: сроки посадки, "
         "полив, мульчирование, подкормка, обрезка и подготовка к зиме в условиях Минской области.")
    + header("care") + care_main + footer("care") + DIALOGS + SCRIPTS)
print("care.html")


# ============================================================ проверка ссылок
def check_assets():
    """Ни одна картинка на странице не должна вести в пустоту."""
    import re as _re
    missing = []
    for page in ("index.html", "catalog.html", "care.html"):
        html = open(page, encoding="utf-8").read()
        refs = set(_re.findall(r'(?:src|srcset|data-shot)="([^"]+)"', html))
        for group in refs:
            for part in group.split(","):
                path = part.strip().split(" ")[0].split("?")[0]
                if not path or path.startswith(("http", "data:", "#")):
                    continue
                if not os.path.exists(path):
                    missing.append(f"{page}: {path}")
    if missing:
        print("\n!! отсутствуют файлы:")
        for m in missing:
            print("   ", m)
        return 1
    print("все ссылки на файлы на месте")
    return 0


sys.exit(check_assets())
