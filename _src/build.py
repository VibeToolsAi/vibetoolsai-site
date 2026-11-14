#!/usr/bin/env python3
"""Generates the static site for getvibetoolsai.com into the repo root.

Run from anywhere:  python3 _src/build.py
No dependencies, no third-party requests in the output (no fonts, analytics or scripts from other hosts).
"""
import html
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from products import COLLECTIONS, STORE  # noqa: E402
from legal import PRIVACY_EN, TERMS_EN, TERMS_PL  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOMAIN = "https://getvibetoolsai.com"
UPDATED = "14 November 2026"
SELLER = ("VibeToolsAI is the trading name of GreenGastro Seweryn Bałchan, NIP 5170419982, "
          "P.O. Box 419, ul. Asnyka 9, 35-001 Rzeszów, Poland")
SELLER_PL = ("VibeToolsAI to marka firmy GreenGastro Seweryn Bałchan, NIP 5170419982, "
             "skrytka pocztowa 419, ul. Asnyka 9, 35-001 Rzeszów")
EMAIL = "hello@getvibetoolsai.com"

e = html.escape


def buy_url(slug, campaign):
    return f"{STORE}{slug}?utm_source=getvibetoolsai&utm_medium=website&utm_campaign={campaign}"


# ---------------------------------------------------------------- layout

def page(*, path, lang, title, description, body, alt=None):
    """path: '/', '/pl/', ... ; alt: path of the other-language page."""
    canonical = DOMAIN + path
    is_pl = lang == "pl"
    nav = [
        ("/kept-kindly/", "Kept Kindly"),
        ("/#ai-prompts", "Prompt packs"),
        ("/#freelancer-money", "Freelancers"),
        ("/pl/", "Po polsku"),
    ]
    if is_pl:
        nav = [
            ("/pl/#ksef", "KSeF"),
            ("/pl/#ai-firma", "AI w firmie"),
            ("/pl/#sport", "Sport"),
            ("/", "English"),
        ]
    nav_html = "".join(
        f'<a href="{href}"{" lang=\"en\"" if (is_pl and href == "/") else ""}'
        f'{" lang=\"pl\"" if (not is_pl and href == "/pl/") else ""}>{e(label)}</a>'
        for href, label in nav)
    alt_link = f'<link rel="alternate" hreflang="{"en" if is_pl else "pl"}" href="{DOMAIN}{alt}">' if alt else ""
    home = "/pl/" if is_pl else "/"
    footer_seller = SELLER_PL if is_pl else SELLER
    legal_links = (
        '<a href="/privacy/" lang="en">Polityka prywatności (EN)</a><a href="/terms/#pl">Regulamin</a>'
        if is_pl else
        '<a href="/privacy/">Privacy policy</a><a href="/terms/">Terms</a>')
    disclaimer = ("Nasze materiały mają charakter informacyjny i organizacyjny. Nie są poradą prawną, podatkową ani finansową."
                  if is_pl else
                  "Our planners, checklists and prompt packs are informational and organizational tools, "
                  "not legal, tax or financial advice.")
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
<meta name="theme-color" content="#1e2a38">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<a class="skip" href="#main">{"Przejdź do treści" if is_pl else "Skip to content"}</a>
<header class="masthead">
  <div class="wrap masthead-in">
    <a class="brand" href="{home}" aria-label="VibeToolsAI home"><span class="brand-mark" aria-hidden="true"></span>VibeToolsAI</a>
    <nav aria-label="{"Główna" if is_pl else "Main"}">{nav_html}</nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <div class="wrap foot-in">
    <p class="foot-seller">{e(footer_seller)} · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <p>{e(disclaimer)}</p>
    <p class="foot-links">{legal_links}<a href="https://vibetoolsai.gumroad.com/?utm_source=getvibetoolsai&amp;utm_medium=website&amp;utm_campaign=footer">{"Sklep na Gumroad" if is_pl else "Shop on Gumroad"}</a></p>
  </div>
</footer>
</body>
</html>
"""


# ---------------------------------------------------------------- components

def product_card(p, campaign, lang):
    buy = "Kup na Gumroad" if lang == "pl" else "Buy on Gumroad"
    was = f' <s aria-label="{"wcześniej" if lang == "pl" else "was"} {e(p["was"])}">{e(p["was"])}</s>' if p.get("was") else ""
    chips = "".join(f"<li>{e(f)}</li>" for f in p["formats"])
    cls = "item featured" if p.get("featured") else "item"
    return f"""<article class="{cls}">
  <h3>{e(p["name"])}</h3>
  <p>{e(p["text"])}</p>
  <ul class="chips" aria-label="{"Format" if lang == "pl" else "What you get"}">{chips}</ul>
  <div class="item-foot"><span class="price">{e(p["price"])}{was}</span>
  <a class="btn" href="{buy_url(p["slug"], campaign)}">{buy}<span class="sr"> – {e(p["name"])}</span></a></div>
</article>"""


def free_list(items, campaign, lang):
    if not items:
        return ""
    head = "Za darmo na start" if lang == "pl" else "Free to try"
    note = ("Podaj cenę 0 zł przy pobraniu albo zapłać, ile chcesz."
            if lang == "pl" else "Enter $0 at checkout, or pay what you like.")
    lis = "".join(f'<li><a href="{buy_url(f["slug"], campaign)}">{e(f["name"])}</a></li>' for f in items)
    return f"""<div class="free">
  <h3>{head}</h3>
  <ul>{lis}</ul>
  <p class="free-note">{note}</p>
</div>"""


def divider(c, campaign, extra=""):
    lang = c["lang"]
    cards = "\n".join(product_card(p, campaign, lang) for p in c["products"])
    return f"""<section class="divider tab-{c["color"]}" id="{c["id"]}" aria-labelledby="{c["id"]}-h">
  <div class="wrap">
    <div class="tab" aria-hidden="true">{e(c["tab"])}</div>
    <div class="divider-head">
      <h2 id="{c["id"]}-h">{e(c["title"])}</h2>
      <p>{e(c["intro"])}</p>
      {extra}
    </div>
    <div class="grid">
{cards}
    </div>
    {free_list(c.get("free"), campaign, lang)}
  </div>
</section>"""


def tab_stack(cols, label):
    links = "".join(
        f'<a class="stack-tab tab-{c["color"]}" href="#{c["id"]}" style="--i:{i}">'
        f'<span>{e(c["tab"])}</span><small>{len(c["products"])} '
        f'{"produkty" if c["lang"] == "pl" else ("products" if len(c["products"]) > 1 else "product")}'
        f'{" + free" if c.get("free") and c["lang"] == "en" else (" + darmowe" if c.get("free") else "")}</small></a>'
        for i, c in enumerate(cols))
    return f'<nav class="stack" aria-label="{e(label)}">{links}</nav>'


def faq(items):
    return "".join(f"<details><summary>{e(q)}</summary><p>{a}</p></details>" for q, a in items)


# ---------------------------------------------------------------- pages

def build_home():
    cols = [c for c in COLLECTIONS if c["lang"] == "en"]
    kk_more = '<p><a class="more" href="/kept-kindly/">See what is inside each Kept Kindly planner</a></p>'
    sections = "\n".join(divider(c, "home", kk_more if c["id"] == "kept-kindly" else "") for c in cols)
    body = f"""
<section class="hero">
  <div class="wrap hero-in">
    <div class="hero-copy">
      <h1>Planners, spreadsheets and prompt packs for the paperwork nobody teaches you.</h1>
      <p class="lede">VibeToolsAI makes small digital tools you buy once and keep: printable planners for family records,
      spreadsheets for freelancers and copy-paste AI prompts for busy professionals. Files download straight after
      checkout on Gumroad.</p>
      <p class="hero-cta"><a class="btn btn-lg" href="/kept-kindly/">Explore Kept Kindly</a>
      <a class="link" href="#ai-prompts">Browse prompt packs</a></p>
    </div>
    {tab_stack(cols, "Collections")}
  </div>
</section>
{sections}
<section class="plain" aria-labelledby="how-h">
  <div class="wrap two">
    <div>
      <h2 id="how-h">How buying works</h2>
      <ol class="steps">
        <li><strong>Pick a product</strong> and check out on Gumroad, our sales platform. Gumroad handles payment and sales tax.</li>
        <li><strong>Download the files</strong> from the receipt email or your Gumroad library. PDFs come in US Letter and A4.</li>
        <li><strong>Print or open</strong> them in Excel, Google Sheets or Numbers. What you write stays on your device.</li>
      </ol>
    </div>
    <div>
      <h2>Who makes these</h2>
      <p>VibeToolsAI is a one-person studio run by Seweryn Bałchan in Rzeszów, Poland. Drafts are written with the help
      of AI tools; every file is then checked, tested and corrected by hand before it goes on sale, and each product
      notes how AI was used.</p>
      <p>Questions or a problem with a file? Email <a href="mailto:{EMAIL}">{EMAIL}</a>. Please describe the issue
      in words and never send pages you have filled in.</p>
    </div>
  </div>
</section>
"""
    return page(path="/", lang="en", alt="/pl/",
                title="VibeToolsAI: printable planners, spreadsheets and AI prompt packs",
                description="Kept Kindly legacy and after-death planners for the US and Canada, freelancer tax spreadsheets "
                            "and ChatGPT prompt packs for realtors, loan officers, teachers and local businesses.",
                body=body)


def build_kept_kindly():
    kk = next(c for c in COLLECTIONS if c["id"] == "kept-kindly")
    cards = "\n".join(product_card(p, "kept-kindly", "en") for p in kk["products"])
    q = [
        ("Is this a will or a legal document?",
         "No. Kept Kindly is an organizer. It helps you collect information and wishes in one place, but it does not "
         "replace a will, power of attorney or advice from a lawyer, accountant or financial adviser in your state or province."),
        ("Does it cover Canada as well as the US?",
         "Yes. The planners are written for households in both countries and remind you to check deadlines with local "
         "authorities, because rules differ by state and province."),
        ("Can I fill it in on a computer?",
         "Yes. Every planner comes with a spreadsheet (.xlsx) that opens in Excel, Google Sheets or Numbers, "
         "alongside the printable PDF in US Letter and A4 sizes."),
        ("Do you see what I write?",
         "No. The files have no tracking and no forms that send data. Everything you write stays on your paper or device. "
         "We recommend never writing down full passwords, PINs or account numbers."),
        ("What if I need help after buying?",
         f'Email <a href="mailto:{EMAIL}">{EMAIL}</a> with your order email and a description of the problem. '
         "Please do not send filled-in pages."),
    ]
    body = f"""
<section class="hero hero-kk">
  <div class="wrap hero-in">
    <div class="hero-copy">
      <p class="crumb"><a href="/">VibeToolsAI</a> / Kept Kindly</p>
      <h1>Write it down once, so your family doesn’t have to guess.</h1>
      <p class="lede">Kept Kindly is a set of printable planners and spreadsheets for households in the United States
      and Canada. One records where everything is and what you want. The other two guide your family and executor
      through the weeks and months after a death.</p>
      <p class="hero-cta"><a class="btn btn-lg" href="{buy_url("before-after-legacy-bundle", "kept-kindly-hero")}">Get the bundle for $32</a>
      <a class="link" href="#planners">Compare the planners</a></p>
    </div>
    <div class="kk-sheet" aria-hidden="true">
      <div class="sheet-row"><span>Who to call first</span><i></i></div>
      <div class="sheet-row"><span>Where the will is kept</span><i></i></div>
      <div class="sheet-row"><span>Bank and pension accounts</span><i></i></div>
      <div class="sheet-row"><span>Insurance policies</span><i></i></div>
      <div class="sheet-row"><span>Pets and who will care for them</span><i></i></div>
      <div class="sheet-row"><span>Wishes for the service</span><i></i></div>
    </div>
  </div>
</section>
<section class="divider tab-plum" id="planners" aria-labelledby="planners-h">
  <div class="wrap">
    <div class="tab" aria-hidden="true">The planners</div>
    <div class="divider-head">
      <h2 id="planners-h">Three planners, one for each stage</h2>
      <p>Buy the one you need now, or all three together and save $10.</p>
    </div>
    <div class="grid">
{cards}
    </div>
  </div>
</section>
<section class="plain" aria-labelledby="stages-h">
  <div class="wrap">
    <h2 id="stages-h">Which one do I need?</h2>
    <ol class="stages">
      <li><strong>Before</strong><span>You want your partner or children to find everything easily one day.
      Start with the <a href="{buy_url("kept-kindly-legacy-planner", "kept-kindly-stages")}">Legacy Planner</a>.</span></li>
      <li><strong>The first weeks</strong><span>Someone close has just died and you need to know what to do first.
      Use the <a href="{buy_url("after-death-checklist", "kept-kindly-stages")}">After Death Checklist</a>.</span></li>
      <li><strong>Settling the estate</strong><span>You are the executor or helping one, and need to track tasks, assets
      and costs. Use the <a href="{buy_url("executor-checklist", "kept-kindly-stages")}">Executor Checklist &amp; Expense Log</a>.</span></li>
    </ol>
  </div>
</section>
<section class="plain faq" aria-labelledby="faq-h">
  <div class="wrap narrow">
    <h2 id="faq-h">Questions</h2>
    {faq(q)}
  </div>
</section>
"""
    return page(path="/kept-kindly/", lang="en",
                title="Kept Kindly: legacy planner, after death checklist and executor tracker (US + Canada)",
                description="Printable end-of-life planner, after death checklist for family and executor checklist with expense log. "
                            "PDF in US Letter and A4 plus Excel and Google Sheets spreadsheets.",
                body=body)


def build_pl():
    cols = [c for c in COLLECTIONS if c["lang"] == "pl"]
    sections = "\n".join(divider(c, "pl") for c in cols)
    body = f"""
<section class="hero">
  <div class="wrap hero-in">
    <div class="hero-copy">
      <h1>Arkusze, przewodniki i prompty dla JDG i małych firm.</h1>
      <p class="lede">Przygotuj firmę na obowiązkowy KSeF od 1 stycznia 2027, uporządkuj współpracę z księgową
      i oddaj powtarzalne teksty AI. Kupujesz raz na Gumroad, pliki pobierasz od razu.</p>
      <p class="hero-cta"><a class="btn btn-lg" href="#ksef">Zobacz materiały o KSeF</a>
      <a class="link" href="{buy_url("free-ksef-licznik-10k", "pl-hero")}">Pobierz darmowy licznik limitu</a></p>
    </div>
    {tab_stack(cols, "Kategorie")}
  </div>
</section>
{sections}
<section class="plain">
  <div class="wrap two">
    <div>
      <h2>Jak wygląda zakup</h2>
      <p>Płatność obsługuje Gumroad, który sprzedaje produkty jako pośrednik (merchant of record). Po zakupie dostajesz e-mail
      z linkiem do plików. Ceny w złotych są cenami brutto widocznymi przy kasie.</p>
    </div>
    <div>
      <h2>Kontakt</h2>
      <p>Pytania i problemy z plikami: <a href="mailto:{EMAIL}">{EMAIL}</a>. Przepisy o KSeF sprawdzamy co tydzień;
      w każdym produkcie jest data, na którą jest aktualny.</p>
    </div>
  </div>
</section>
"""
    return page(path="/pl/", lang="pl", alt="/",
                title="VibeToolsAI po polsku: KSeF dla JDG, AI w małej firmie",
                description="Zestaw wdrożeniowy KSeF, teczka dla księgowego, darmowy licznik limitu 10 000 zł, "
                            "50 procesów AI dla małej firmy i prompty dla agentów nieruchomości.",
                body=body)


def build_legal(path, lang, title, description, content):
    body = f"""<section class="plain legal"><div class="wrap narrow">{content}</div></section>"""
    return page(path=path, lang=lang, title=title, description=description, body=body)


def build_404():
    body = """<section class="hero"><div class="wrap narrow">
<h1>This page isn’t here.</h1>
<p class="lede">The link may be old. Go to the <a href="/">home page</a>, the <a href="/kept-kindly/">Kept Kindly planners</a>
or the <a href="/pl/">Polish products</a>.</p></div></section>"""
    return page(path="/404.html", lang="en", title="Page not found · VibeToolsAI",
                description="Page not found.", body=body)


def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    print("wrote", rel)


def main():
    write("index.html", build_home())
    write("kept-kindly/index.html", build_kept_kindly())
    write("pl/index.html", build_pl())
    write("privacy/index.html", build_legal("/privacy/", "en", "Privacy policy · VibeToolsAI",
                                           "How VibeToolsAI processes personal data.", PRIVACY_EN))
    write("terms/index.html", build_legal("/terms/", "en", "Terms · VibeToolsAI",
                                         "Terms for using getvibetoolsai.com and buying VibeToolsAI products.",
                                         TERMS_EN + TERMS_PL))
    write("404.html", build_404())
    urls = ["/", "/kept-kindly/", "/pl/", "/privacy/", "/terms/"]
    sm = "".join(f"<url><loc>{DOMAIN}{u}</loc></url>" for u in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
    write("CNAME", "getvibetoolsai.com\n")
    write(".nojekyll", "")


if __name__ == "__main__":
    main()
