#!/usr/bin/env python3
"""Generates the static site for getvibetoolsai.com into the repo root.

Run:  python3 -B _src/build.py
No dependencies. No third-party requests in the output (no fonts, analytics or scripts from other hosts).
"""
import html
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from products import COLLECTIONS, STORE  # noqa: E402
from details import DETAILS, FREE  # noqa: E402
from legal import PRIVACY_EN, TERMS_EN, TERMS_PL  # noqa: E402
from legal_pl import PRIVACY_PL  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOMAIN = "https://getvibetoolsai.com"
SIZES = json.loads((pathlib.Path(__file__).parent / "imgsizes.json").read_text())
EMAIL = "hello@getvibetoolsai.com"
SELLER = ("VibeToolsAI is the trading name of GreenGastro Seweryn Bałchan, NIP 5170419982, "
          "P.O. Box 419, ul. Asnyka 9, 35-001 Rzeszów, Poland")
SELLER_PL = ("VibeToolsAI to marka firmy GreenGastro Seweryn Bałchan, NIP 5170419982, "
             "skrytka pocztowa 419, ul. Asnyka 9, 35-001 Rzeszów")
e = html.escape

# ------------------------------------------------------------------ catalogue

PRODUCTS = {}  # slug -> dict(name, price, lang, coll, color, free, text, formats)
for c in COLLECTIONS:
    for p in c["products"]:
        PRODUCTS[p["slug"]] = {**p, "lang": c["lang"], "coll": c["id"], "tab": c["tab"], "color": c["color"], "free": False}
    for f in c.get("free", []):
        name, lang, text, upsell = FREE[f["slug"]]
        PRODUCTS[f["slug"]] = {"slug": f["slug"], "name": name, "price": "Free" if lang == "en" else "Za darmo",
                               "formats": ["PDF"] if "xlsx" not in text.lower() else ["Spreadsheet"],
                               "text": text, "lang": lang, "coll": c["id"], "tab": c["tab"], "color": c["color"],
                               "free": True, "upsell": upsell}
PRODUCTS["free-tax-set-aside-calculator"]["formats"] = ["Excel", "Google Sheets"]
PRODUCTS["free-ksef-licznik-10k"]["formats"] = ["Arkusz", "PDF"]


def purl(slug):
    return (f"/pl/produkty/{slug}/" if PRODUCTS[slug]["lang"] == "pl" else f"/products/{slug}/")


def buy_url(slug, campaign):
    return f"{STORE}{slug}?utm_source=getvibetoolsai&utm_medium=website&utm_campaign={campaign}"


def img(name, alt, cls="", eager=False, sizes="(max-width: 40rem) 50vw, 18rem"):
    w, h = SIZES.get(name, (640, 829))
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img class="{cls}" src="/assets/p/{name}.jpg" width="{w}" height="{h}" alt="{e(alt)}" {load}>')


def cover(slug):
    return f"{slug}-1" if f"{slug}-1" in SIZES else None


# ------------------------------------------------------------------ icons (inline SVG)

ICON = {
    "download": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12m0 0-5-5m5 5 5-5M4 19h16" /></svg>',
    "print": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 8V3h10v5M7 17H4v-7h16v7h-3M7 14h10v7H7z" /></svg>',
    "sheet": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4h16v16H4zM4 10h16M4 15h16M10 4v16" /></svg>',
    "lock": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 11h12v9H6zM8 11V8a4 4 0 0 1 8 0v3" /></svg>',
    "search": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m20 20-4.5-4.5M10.5 17a6.5 6.5 0 1 1 0-13 6.5 6.5 0 0 1 0 13z" /></svg>',
    "check": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12 4 4 10-10" /></svg>',
}


# ------------------------------------------------------------------ layout

def page(*, path, lang, title, description, body, alt=None, image=None, jsonld=None, script=False):
    canonical = DOMAIN + path
    pl = lang == "pl"
    nav = ([("/pl/#sklep", "Sklep"), ("/pl/#ksef", "KSeF"), ("/pl/#ai-firma", "AI w firmie"), ("/", "English")] if pl else
           [("/#shop", "Shop"), ("/kept-kindly/", "Kept Kindly"), ("/#ai-prompts", "Prompt packs"), ("/pl/", "Po polsku")])
    nav_html = "".join(
        f'<a href="{h}"{" lang=en" if pl and h == "/" else (" lang=pl" if not pl and h == "/pl/" else "")}>{e(t)}</a>'
        for h, t in nav)
    alt_link = f'<link rel="alternate" hreflang="{"en" if pl else "pl"}" href="{DOMAIN}{alt}">' if alt else ""
    og_img = f'<meta property="og:image" content="{DOMAIN}/assets/p/{image}.jpg">' if image else ""
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    js = '<script src="/assets/shop.js" defer></script>' if script else ""
    legal = ('<a href="/pl/polityka-prywatnosci/">Polityka prywatności</a><a href="/terms/#pl">Regulamin</a>' if pl else
             '<a href="/privacy/">Privacy policy</a><a href="/terms/">Terms</a>')
    disclaimer = ("Materiały mają charakter informacyjny i organizacyjny. Nie są poradą prawną, podatkową ani finansową." if pl else
                  "Planners, checklists and prompt packs are informational and organizational tools, not legal, tax or financial advice.")
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="{lang}" href="{canonical}">
{alt_link}
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="VibeToolsAI">
{og_img}
<meta name="p:domain_verify" content="cafecce7516f0ac8daa4d6f0feb5818b">
<meta name="theme-color" content="#ffffff">
<meta name="color-scheme" content="light">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/site.css">
{ld}{js}
</head>
<body>
<a class="skip" href="#main">{"Przejdź do treści" if pl else "Skip to content"}</a>
<header class="masthead">
  <div class="wrap masthead-in">
    <a class="brand" href="{"/pl/" if pl else "/"}"><span class="brand-word">VibeTools<em>AI</em></span></a>
    <nav aria-label="{"Główna" if pl else "Main"}">{nav_html}</nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <div class="wrap foot-in">
    <div class="foot-brand"><a class="brand" href="{"/pl/" if pl else "/"}"><span class="brand-word">VibeTools<em>AI</em></span></a>
    <p>{"Pliki do pobrania: planery, arkusze i prompty." if pl else "Downloadable planners, spreadsheets and prompt packs."}</p></div>
    <div><p class="foot-seller">{e(SELLER_PL if pl else SELLER)}</p>
    <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <p>{e(disclaimer)}</p>
    <p class="foot-links">{legal}<a href="https://vibetoolsai.gumroad.com/?utm_source=getvibetoolsai&amp;utm_medium=website&amp;utm_campaign=footer">{"Sklep na Gumroad" if pl else "Shop on Gumroad"}</a></p></div>
  </div>
</footer>
</body>
</html>
"""


# ------------------------------------------------------------------ components

def card(slug, campaign):
    p = PRODUCTS[slug]
    pl = p["lang"] == "pl"
    cv = cover(slug)
    pic = img(cv, f'{"Okładka" if pl else "Cover of"} {p["name"]}', "card-img flat" if slug == "before-after-legacy-bundle" else "card-img") if cv else ""
    badge = (f'<span class="badge badge-free">{"Za darmo" if pl else "Free"}</span>' if p["free"] else
             (f'<span class="badge badge-save">{"Oszczędzasz" if pl else "Save"} {"$10" if slug == "before-after-legacy-bundle" else ""}</span>'
              if p.get("was") else ""))
    was = f' <s>{e(p["was"])}</s>' if p.get("was") else ""
    search = e(f'{p["name"]} {p["text"]} {" ".join(p["formats"])} {p["tab"]}'.lower())
    return f"""<article class="card tab-{p["color"]}" data-cat="{p["coll"]}{" free" if p["free"] else ""}" data-q="{search}">
  <a class="card-link" href="{purl(slug)}">
    <div class="card-media">{pic}{badge}</div>
    <h3>{e(p["name"])}</h3>
  </a>
  <p class="card-meta">{e(" · ".join(p["formats"][:2]))}</p>
  <p class="card-price">{e(p["price"])}{was}</p>
</article>"""


def trust(pl=False):
    items = ([("download", "Natychmiastowe pobranie", "Link w mailu od razu po zakupie"),
              ("print", "Do druku i do edycji", "PDF oraz arkusze Excel / Google"),
              ("lock", "Bezpieczna płatność", "Kasa i podatki: Gumroad"),
              ("sheet", "Twoje dane zostają u Ciebie", "Pliki bez śledzenia")] if pl else
             [("download", "Instant digital download", "Files arrive by email right after checkout"),
              ("print", "Print it or fill it in", "PDF in US Letter + A4, plus spreadsheets"),
              ("lock", "Secure checkout", "Payment and sales tax handled by Gumroad"),
              ("sheet", "Your details stay with you", "No tracking inside the files")])
    lis = "".join(f'<li>{ICON[i]}<span><strong>{e(a)}</strong>{e(b)}</span></li>' for i, a, b in items)
    return f'<ul class="trust" aria-label="{"Jak to działa" if pl else "How it works"}">{lis}</ul>'


def shop(slugs, pl=False, filters=None):
    cards = "\n".join(card(s, "pl-shop" if pl else "shop") for s in slugs)
    chips = "".join(f'<button type="button" class="chip{" is-on" if i == 0 else ""}" data-filter="{k}" aria-pressed="{"true" if i == 0 else "false"}">{e(v)}</button>'
                    for i, (k, v) in enumerate(filters))
    return f"""<section class="shop" id="{"sklep" if pl else "shop"}" aria-labelledby="shop-h">
  <div class="wrap">
    <div class="shop-head">
      <h2 id="shop-h">{"Wszystkie produkty" if pl else "All products"}</h2>
      <p class="shop-count" aria-live="polite"><span data-count>{len(slugs)}</span> {"produktów" if pl else "products"}</p>
    </div>
    <div class="chips" role="group" aria-label="{"Filtruj" if pl else "Filter"}">{chips}</div>
    <div class="grid" data-grid>
{cards}
    </div>
    <p class="empty" data-empty hidden>{"Nic nie pasuje. Wyczyść wyszukiwanie albo wybierz „Wszystko”." if pl else "Nothing matches. Clear the search or pick “All”."}</p>
  </div>
</section>"""


def searchbox(pl=False):
    return f"""<form class="search" role="search" action="#{"sklep" if pl else "shop"}" onsubmit="return false">
  <label class="sr" for="q">{"Szukaj produktów" if pl else "Search products"}</label>
  {ICON["search"]}<input id="q" type="search" data-search placeholder="{"Szukaj: KSeF, prompty, śniadania…" if pl else "Search planners, prompts, spreadsheets…"}" autocomplete="off">
  <button type="submit" class="btn search-btn" data-go>{"Szukaj" if pl else "Search"}</button>
</form>"""


def circles(items, pl=False):
    lis = "".join(f'<li><a href="#{"sklep" if pl else "shop"}" data-pick="{k}">'
                  f'<span class="circ">{img(cover(s), "", sizes="5rem")}</span>{e(t)}</a></li>' for k, t, s in items)
    return f'<ul class="circles" aria-label="{"Kategorie" if pl else "Categories"}">{lis}</ul>'


def fan(slugs, label):
    ims = "".join(f'<li style="--k:{i}">{img(cover(s), PRODUCTS[s]["name"], eager=(i == 0), sizes="14rem")}</li>' for i, s in enumerate(slugs))
    return f'<ul class="fan" aria-label="{e(label)}">{ims}</ul>'


# ------------------------------------------------------------------ pages

EN_ORDER = ["before-after-legacy-bundle", "kept-kindly-legacy-planner", "after-death-checklist", "executor-checklist",
            "kept-kindly-caregiver-binder",
            "realtor-ai-playbook", "loan-officer-ai-playbook", "local-business-ai-playbook", "teacher-ai-planner",
            "realtor-mini-25", "freelancer-tax-profit-tracker",
            "free-tax-set-aside-calculator", "listing-prompts-free", "free-realtor-prompts", "free-loan-officer-prompts",
            "free-small-business-prompts", "free-teacher-prompts", "oytvfx", "dmiiwi", "hlzeqi"]
PL_ORDER = ["fzjwvr", "zestaw-wdrozeniowy-ksef", "teczka-ksiegowy-ksef", "ksef-toolkit-jdg", "ai-w-malej-firmie",
            "agent-nieruchomosci-25-promptow", "paliwo-w-15-minut", "zdrowe-sniadania-sportowiec",
            "free-ksef-licznik-10k", "hwdanj", "ogloszenie-ktore-sprzedaje"]


def build_home():
    body = f"""
<section class="hero hero-shop">
  <div class="wrap hero-in">
    <div class="hero-copy">
      <h1>Printable planners and AI prompt packs for the paperwork nobody teaches you.</h1>
      <p class="lede">Family records, estate checklists, freelancer tax sheets and ready-to-paste prompts for realtors,
      loan officers, teachers and local businesses. Buy once, download straight away, keep forever.</p>
      {searchbox()}
      {circles([("kept-kindly", "Family & legacy", "kept-kindly-legacy-planner"), ("ai-prompts", "AI prompt packs", "realtor-ai-playbook"),
                ("freelancer-money", "Freelancers", "free-tax-set-aside-calculator"), ("free", "Free", "oytvfx")])}
    </div>
    {fan(["kept-kindly-legacy-planner", "realtor-ai-playbook", "after-death-checklist", "loan-officer-ai-playbook"], "Product covers")}
  </div>
  <div class="wrap">{trust()}</div>
</section>

<section class="feature tab-plum" aria-labelledby="kk-h">
  <div class="wrap feature-in">
    <div class="feature-pages" aria-hidden="true">
      {img("kept-kindly-legacy-planner-p5", "", "pg pg-1")}
      {img("after-death-checklist-p5", "", "pg pg-2")}
      {img("executor-checklist-p18", "", "pg pg-3")}
    </div>
    <div class="feature-copy">
      <p class="kicker">New collection for the US &amp; Canada</p>
      <h2 id="kk-h">Kept Kindly: write it down once, so your family doesn’t have to guess.</h2>
      <p>A legacy planner for the life you have now, a checklist for the weeks after a death, and an executor’s tracker
      for settling the estate. 94 printable pages and three spreadsheets.</p>
      <ul class="ticks">
        <li>{ICON["check"]}Emergency summary, accounts, insurance, wishes and letters</li>
        <li>{ICON["check"]}Who to notify in the US and in Canada</li>
        <li>{ICON["check"]}Executor expense log with running totals</li>
      </ul>
      <p class="feature-cta"><a class="btn btn-lg" href="/kept-kindly/">See the planners</a>
      <span class="from">Bundle $32 <s>$42</s></span></p>
    </div>
  </div>
</section>

{shop(EN_ORDER, filters=[("all", "All"), ("kept-kindly", "Family & legacy"), ("ai-prompts", "AI prompt packs"),
                         ("freelancer-money", "Freelancer money"), ("free", "Free")])}

<section class="plain" aria-labelledby="who-h" id="ai-prompts">
  <div class="wrap two">
    <div>
      <h2 id="who-h">Made by a small studio, checked by hand</h2>
      <p>VibeToolsAI is run by Seweryn Bałchan in Rzeszów, Poland. Drafts are written with the help of AI tools; every file
      is then tested and corrected by hand before it goes on sale, and each product says how AI was used.</p>
      <p>Something wrong with a file? Email <a href="mailto:{EMAIL}">{EMAIL}</a> and it will be fixed, replaced or refunded.
      Please describe the problem in words and never send pages you have filled in.</p>
    </div>
    <div>
      <h2>How buying works</h2>
      <ol class="steps">
        <li><strong>Pick a product</strong> and check out on Gumroad, our sales platform.</li>
        <li><strong>Download the files</strong> from the receipt email or your Gumroad library.</li>
        <li><strong>Print or open</strong> them in Excel, Google Sheets or Numbers.</li>
      </ol>
      <p><a href="/pl/" lang="pl">Produkty po polsku: KSeF, AI w firmie, sport</a></p>
    </div>
  </div>
</section>
"""
    return page(path="/", lang="en", alt="/pl/", script=True, image="kept-kindly-legacy-planner-1",
                title="VibeToolsAI: printable planners, spreadsheets and AI prompt packs",
                description="Kept Kindly legacy and after-death planners for the US and Canada, freelancer tax spreadsheets "
                            "and ChatGPT prompt packs for realtors, loan officers, teachers and local businesses.",
                body=body)


def build_pl():
    body = f"""
<section class="hero hero-shop">
  <div class="wrap hero-in">
    <div class="hero-copy">
      <h1>Arkusze, ebooki i prompty dla JDG i małych firm.</h1>
      <p class="lede">Przygotuj firmę na obowiązkowy KSeF od 1 stycznia 2027, uporządkuj współpracę z księgową
      i oddaj powtarzalne teksty AI. Kupujesz raz, pliki pobierasz od razu.</p>
      {searchbox(True)}
      {circles([("ksef", "KSeF i JDG", "fzjwvr"), ("ai-firma", "AI w firmie", "ai-w-malej-firmie"),
                ("sport", "Jedzenie i sport", "paliwo-w-15-minut"), ("free", "Za darmo", "hwdanj")], True)}
    </div>
    {fan(["fzjwvr", "ai-w-malej-firmie", "paliwo-w-15-minut", "zestaw-wdrozeniowy-ksef"], "Okładki produktów")}
  </div>
  <div class="wrap">{trust(True)}</div>
</section>
{shop(PL_ORDER, True, filters=[("all", "Wszystko"), ("ksef", "KSeF i JDG"), ("ai-firma", "AI w firmie"),
                               ("sport", "Jedzenie i sport"), ("free", "Za darmo")])}
<section class="plain" id="ksef">
  <div class="wrap two">
    <div>
      <h2>KSeF bez nerwów</h2>
      <p>Od 1 stycznia 2027 każda faktura dla firm idzie przez KSeF. Zacznij od darmowego
      <a href="{purl("free-ksef-licznik-10k")}">licznika limitu</a>, przeczytaj
      <a href="{purl("fzjwvr")}">przewodnik krok po kroku</a>, a porządek trzymaj w
      <a href="{purl("zestaw-wdrozeniowy-ksef")}">zestawie wdrożeniowym</a>. Przepisy sprawdzamy co tydzień; każdy produkt
      podaje datę, na którą jest aktualny.</p>
    </div>
    <div id="ai-firma">
      <h2>Zakup i kontakt</h2>
      <p>Płatność obsługuje Gumroad, który sprzedaje produkty jako pośrednik (merchant of record). Po zakupie dostajesz e-mail
      z linkiem do plików. Pytania i problemy: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    </div>
  </div>
</section>
"""
    return page(path="/pl/", lang="pl", alt="/", script=True, image="fzjwvr-1",
                title="VibeToolsAI po polsku: KSeF dla JDG, AI w małej firmie",
                description="Zestaw wdrożeniowy KSeF, teczka dla księgowego, darmowy licznik limitu 10 000 zł, "
                            "50 procesów AI dla małej firmy i prompty dla agentów nieruchomości.",
                body=body)


def build_kept_kindly():
    q = [
        ("Is this a will or a legal document?",
         "No. Kept Kindly is an organizer. It helps you collect information and wishes in one place, but it does not "
         "replace a will, power of attorney or advice from a lawyer, accountant or financial adviser in your state or province."),
        ("Does it cover Canada as well as the US?",
         "Yes. The planners are written for households in both countries and remind you to check deadlines with local "
         "authorities, because rules differ by state and province."),
        ("Can I fill it in on a computer?",
         "Yes. Every planner comes with a spreadsheet (.xlsx) that opens in Excel, Google Sheets or Numbers, "
         "alongside the printable PDF in US Letter and A4."),
        ("Do you see what I write?",
         "No. The files have no tracking and no forms that send data. We recommend never writing down full passwords, PINs or account numbers."),
        ("What if something is wrong with a file?",
         f'Email <a href="mailto:{EMAIL}">{EMAIL}</a> within 14 days and we will fix, replace or refund it. Please do not send filled-in pages.'),
    ]
    faq = "".join(f"<details><summary>{e(a)}</summary><p>{b}</p></details>" for a, b in q)
    cards = "\n".join(card(s, "kept-kindly") for s in ["before-after-legacy-bundle", "kept-kindly-legacy-planner",
                                                         "after-death-checklist", "executor-checklist",
                                                         "kept-kindly-caregiver-binder", "hlzeqi"])
    body = f"""
<section class="hero hero-kk tab-plum">
  <div class="wrap hero-in">
    <div class="hero-copy">
      <p class="crumb"><a href="/">VibeToolsAI</a> / Kept Kindly</p>
      <h1>Write it down once, so your family doesn’t have to guess.</h1>
      <p class="lede">Printable planners and spreadsheets for households in the United States and Canada: one to record where
      everything is, one to coordinate care for an aging parent, and two to guide your family and executor after a death.</p>
      <p class="hero-cta"><a class="btn btn-lg" href="{buy_url("before-after-legacy-bundle", "kept-kindly-hero")}">Get all three for $32</a>
      <a class="link" href="#planners">Compare the planners</a></p>
    </div>
    {fan(["kept-kindly-legacy-planner", "after-death-checklist", "executor-checklist"], "Kept Kindly covers")}
  </div>
  <div class="wrap">{trust()}</div>
</section>
<section class="shop" id="planners" aria-labelledby="pl-h">
  <div class="wrap">
    <div class="shop-head"><h2 id="pl-h">Four planners, one for each stage</h2></div>
    <div class="grid grid-4">
{cards}
    </div>
  </div>
</section>
<section class="plain" aria-labelledby="stages-h">
  <div class="wrap">
    <h2 id="stages-h">Which one do I need?</h2>
    <ol class="stages">
      <li><strong>Before</strong><span>You want your partner or children to find everything easily one day.
      Start with the <a href="{purl("kept-kindly-legacy-planner")}">Legacy Planner</a>.</span></li>
      <li><strong>While caring</strong><span>You help look after an aging parent and the family needs to share what matters.
      Use the <a href="{purl("kept-kindly-caregiver-binder")}">Caregiver Binder</a>.</span></li>
      <li><strong>The first weeks</strong><span>Someone close has just died and you need to know what to do first.
      Use the <a href="{purl("after-death-checklist")}">After Death Checklist</a>.</span></li>
      <li><strong>Settling the estate</strong><span>You are the executor or helping one, and need to track tasks, assets
      and costs. Use the <a href="{purl("executor-checklist")}">Executor Checklist &amp; Expense Log</a>.</span></li>
    </ol>
    <div class="peek">
      <h3>A look inside</h3>
      <div class="peek-row">
        <figure>{img("kept-kindly-legacy-planner-p5", "Emergency quick-reference summary page")}<figcaption>Emergency summary</figcaption></figure>
        <figure>{img("kept-kindly-legacy-planner-p17", "Bank accounts page")}<figcaption>Bank accounts</figcaption></figure>
        <figure>{img("after-death-checklist-p5", "First 24–48 hours checklist page")}<figcaption>First 24–48 hours</figcaption></figure>
        <figure>{img("executor-checklist-p18", "Executor expense log page")}<figcaption>Executor expense log</figcaption></figure>
      </div>
    </div>
  </div>
</section>
<section class="plain faq" aria-labelledby="faq-h">
  <div class="wrap narrow"><h2 id="faq-h">Questions</h2>{faq}</div>
</section>
"""
    return page(path="/kept-kindly/", lang="en", image="kept-kindly-legacy-planner-1",
                title="Kept Kindly: legacy planner, after death checklist and executor tracker (US + Canada)",
                description="Printable end-of-life planner, after death checklist for family and executor checklist with expense log. "
                            "PDF in US Letter and A4 plus Excel and Google Sheets spreadsheets.",
                body=body)


def price_number(p):
    s = p["price"].replace("$", "").replace("zł", "").strip()
    try:
        return float(s), ("PLN" if "zł" in p["price"] else "USD")
    except ValueError:
        return 0.0, ("PLN" if p["lang"] == "pl" else "USD")


def build_product(slug):
    p = PRODUCTS[slug]
    pl = p["lang"] == "pl"
    d = DETAILS.get(slug)
    if d:
        title, seo, lede, inside, specs, previews, note = (d["title"], d["seo"], d["lede"], d["inside"], d["specs"],
                                                          [x for x in d["previews"] if x in SIZES], d["note"])
    else:
        title, lede = p["name"], p["text"]
        seo = lede
        inside, specs, note = [], p["formats"], ""
        previews = [x for x in (f"{slug}-1", f"{slug}-2") if x in SIZES]
    camp = f"product-{slug}"
    main = previews[0] if previews else None
    thumbs = "".join(
        f'<li><a href="/assets/p/{x}.jpg" data-swap="/assets/p/{x}.jpg">{img(x, f"{title}, page preview {i + 1}", sizes="5rem")}</a></li>'
        for i, x in enumerate(previews)) if len(previews) > 1 else ""
    gallery = (f'<div class="gallery"><div class="gallery-main">{img(main, f"{title}, cover", "main-img", eager=True, sizes="(max-width: 52rem) 100vw, 34rem")}</div>'
               f'{"<ul class=thumbs>" + thumbs + "</ul>" if thumbs else ""}</div>') if main else ""
    was = f' <s>{e(p["was"])}</s>' if p.get("was") else ""
    chips = "".join(f"<li>{e(s)}</li>" for s in specs)
    inside_html = ("<h2>" + ("Co jest w środku" if pl else "What’s inside") + "</h2><ul class=\"inside\">" +
                   "".join(f"<li>{ICON['check']}<span>{e(x)}</span></li>" for x in inside) + "</ul>") if inside else ""
    buy_label = ("Pobierz za darmo" if pl else "Get it free") if p["free"] else ("Kup na Gumroad" if pl else "Buy on Gumroad")
    up = p.get("upsell")
    upsell = ""
    if up:
        u = PRODUCTS[up]
        upsell = (f'<p class="upsell">{"Pełna wersja:" if pl else "Want the full version?"} '
                  f'<a href="{purl(up)}">{e(u["name"])}</a> ({e(u["price"])})</p>')
    lang_req = ""
    if d and d.get("translate"):
        subj = f"{'Wersja językowa' if pl else 'Language version'}: {p['name']}"
        from urllib.parse import quote
        lang_req = (f'<p class="lang-req">{"Potrzebujesz po angielsku albo w innym języku?" if pl else "Need it in Polish or another language?"} '
                    f'<a href="mailto:{EMAIL}?subject={quote(subj)}">{"Napisz do nas" if pl else "Ask us"}</a>. '
                    f'{"Przygotujemy wersję i wyślemy Ci e-mail, gdy będzie gotowa w sklepie." if pl else "We’ll prepare it and email you when it’s ready in the shop."}</p>')
    related = [s for s in (EN_ORDER if not pl else PL_ORDER) if PRODUCTS[s]["coll"] == p["coll"] and s != slug][:4]
    if len(related) < 4:
        related += [s for s in (EN_ORDER if not pl else PL_ORDER) if s not in related and s != slug][:4 - len(related)]
    rel = "\n".join(card(s, f"related-{slug}") for s in related)
    crumb_home = "/pl/" if pl else "/"
    dl = ("Natychmiastowe pobranie" if pl else "Instant digital download")
    pay = ("Płatność i podatki obsługuje Gumroad" if pl else "Secure checkout on Gumroad; sales tax handled for you")
    guarantee = ("Plik nie działa albo nie zgadza się z opisem? Napisz w ciągu 14 dni, poprawimy go lub zwrócimy pieniądze."
                 if pl else "File broken or not as described? Email within 14 days and we’ll fix, replace or refund it.")
    amount, cur = price_number(p)
    ld = {"@context": "https://schema.org", "@type": "Product", "name": title, "description": seo,
          "image": f"{DOMAIN}/assets/p/{main}.jpg" if main else None,
          "brand": {"@type": "Brand", "name": "VibeToolsAI"},
          "offers": {"@type": "Offer", "price": f"{amount:.2f}", "priceCurrency": cur,
                     "availability": "https://schema.org/InStock", "url": f"{STORE}{slug}"}}
    body = f"""
<section class="product tab-{p["color"]}">
  <div class="wrap">
    <p class="crumb"><a href="{crumb_home}">VibeToolsAI</a> / <a href="{crumb_home}#{"sklep" if pl else "shop"}">{e(p["tab"])}</a></p>
    <div class="product-in">
      {gallery}
      <div class="buybox">
        <p class="badge-line"><span class="badge">{ICON["download"]}{"Plik cyfrowy" if pl else "Digital download"}</span></p>
        <h1>{e(title)}</h1>
        <p class="lede">{e(lede)}</p>
        <p class="big-price">{e(p["price"])}{was}</p>
        <a class="btn btn-lg btn-block" href="{buy_url(slug, camp)}">{buy_label}</a>
        <ul class="specs">{chips}</ul>
        <ul class="assure">
          <li>{ICON["download"]}{dl}</li>
          <li>{ICON["lock"]}{pay}</li>
        </ul>
        {upsell}
        {lang_req}
      </div>
    </div>
  </div>
</section>
<section class="plain detail">
  <div class="wrap two two-wide">
    <div>{inside_html}</div>
    <div>
      <details open><summary>{"Jak to działa" if pl else "How it works"}</summary>
        <p>{"Po zakupie Gumroad wysyła e-mail z linkiem do plików. Pliki są też w Twojej bibliotece Gumroad." if pl else
            "After checkout Gumroad emails you a download link, and the files stay in your Gumroad library."}</p></details>
      <details><summary>{"Zwroty" if pl else "Refunds"}</summary><p>{e(guarantee)}</p></details>
      {f'<details><summary>{"Ważne" if pl else "Good to know"}</summary><p>{e(note)}</p></details>' if note else ""}
      <details><summary>{"Sprzedawca" if pl else "Seller"}</summary><p>{e(SELLER_PL if pl else SELLER)}. <a href="mailto:{EMAIL}">{EMAIL}</a></p></details>
    </div>
  </div>
</section>
<section class="shop">
  <div class="wrap">
    <div class="shop-head"><h2>{"Więcej z tego sklepu" if pl else "More from this shop"}</h2></div>
    <div class="grid grid-4">
{rel}
    </div>
  </div>
</section>
"""
    return page(path=purl(slug), lang=p["lang"], image=main, jsonld=ld, script=True,
                title=f"{title} · VibeToolsAI", description=seo, body=body)


def build_legal(path, lang, title, description, content, alt=None):
    return page(path=path, lang=lang, title=title, description=description, alt=alt,
                body=f'<section class="plain legal"><div class="wrap narrow">{content}</div></section>')


def build_404():
    body = """<section class="hero"><div class="wrap narrow">
<h1>This page isn’t here.</h1>
<p class="lede">The link may be old. Go to the <a href="/#shop">shop</a>, the <a href="/kept-kindly/">Kept Kindly planners</a>
or the <a href="/pl/">Polish products</a>.</p></div></section>"""
    return page(path="/404.html", lang="en", title="Page not found · VibeToolsAI", description="Page not found.", body=body)


def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def main():
    write("index.html", build_home())
    write("kept-kindly/index.html", build_kept_kindly())
    write("pl/index.html", build_pl())
    urls = ["/", "/kept-kindly/", "/pl/", "/privacy/", "/pl/polityka-prywatnosci/", "/terms/"]
    for slug in PRODUCTS:
        write(purl(slug).strip("/") + "/index.html", build_product(slug))
        urls.append(purl(slug))
    write("privacy/index.html", build_legal("/privacy/", "en", "Privacy policy · VibeToolsAI",
                                           "How VibeToolsAI processes personal data.", PRIVACY_EN, alt="/pl/polityka-prywatnosci/"))
    write("pl/polityka-prywatnosci/index.html", build_legal("/pl/polityka-prywatnosci/", "pl", "Polityka prywatności · VibeToolsAI",
                                           "Jak VibeToolsAI przetwarza dane osobowe.", PRIVACY_PL, alt="/privacy/"))
    write("terms/index.html", build_legal("/terms/", "en", "Terms · VibeToolsAI",
                                         "Terms for using getvibetoolsai.com and buying VibeToolsAI products.", TERMS_EN + TERMS_PL))
    write("404.html", build_404())
    sm = "".join(f"<url><loc>{DOMAIN}{u}</loc></url>" for u in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
    write("CNAME", "getvibetoolsai.com\n")
    write(".nojekyll", "")
    print(f"built {len(urls)} pages")


if __name__ == "__main__":
    main()
