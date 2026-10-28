#!/usr/bin/env python3
"""Files for the production site, built after i18n.py: 404 page, SEO tags, robots.txt, sitemap.xml and llms.txt."""
import os, re, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(HERE), 'site')
DOMAIN = 'https://pool-on.com'
PAGES = ['index', 'solutions', 'content', 'technology', 'references', 'contact', 'legal']

NOT_FOUND = '''<main id="top">
  <section class="block legal">
    <div class="wrap">
      <span class="eyebrow">404</span>
      <h1>This page is not in the pool</h1>
      <p>The page you are looking for has moved or no longer exists.</p>
      <p lang="fr">La page que vous cherchez a été déplacée ou n'existe plus.</p>
      <div class="actions">
        <a class="btn btn-primary" href="/">Pool-On home</a>
        <a class="btn btn-ghost" href="/fr/" lang="fr">Accueil en français</a>
      </div>
    </div>
  </section>
</main>'''

def not_found():
    # Served for any missing URL, so every link must be absolute.
    h = open(os.path.join(SITE, 'legal.html')).read()
    h = re.sub(r'<main id="top">.*?</main>', NOT_FOUND, h, flags=re.S)
    h = re.sub(r'<link rel="alternate"[^>]*>\n', '', h)
    h = re.sub(r"<script>\(function\(\)\{var k='poolon-lang'.*?</script>\n", '', h, flags=re.S)
    h = re.sub(r'<title>.*?</title>', '<title>Page not found · Pool-On</title>', h)
    h = re.sub(r'<meta name="description"[^>]*>', '<meta name="robots" content="noindex">', h)
    h = re.sub(r'\b(href|src|poster)="(?!https?:|mailto:|#|/)(\./)?', r'\1="/', h)
    h = h.replace('href="/legal.html" aria-current="page"', 'href="/legal.html"')
    h = h.replace('href="/fr/legal.html"', 'href="/fr/"')
    open(os.path.join(SITE, '404.html'), 'w').write(h)

def robots_and_sitemap():
    open(os.path.join(SITE, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % DOMAIN)
    urls = []
    for p in PAGES:
        en = DOMAIN + ('/' if p == 'index' else '/%s.html' % p)
        fr = DOMAIN + ('/fr/' if p == 'index' else '/fr/%s.html' % p)
        alt = ('    <xhtml:link rel="alternate" hreflang="en" href="%s"/>\n'
               '    <xhtml:link rel="alternate" hreflang="fr" href="%s"/>\n') % (en, fr)
        for loc in (en, fr):
            urls.append('  <url>\n    <loc>%s</loc>\n%s  </url>' % (loc, alt))
    open(os.path.join(SITE, 'sitemap.xml'), 'w').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + '\n'.join(urls) + '\n</urlset>\n')

SOCIAL = ['https://www.instagram.com/pool_on_experience/', 'https://www.linkedin.com/company/pool-on',
          'https://www.youtube.com/@pool-on2405']

def url(page, lang):
    if page == 'index':
        return DOMAIN + ('/fr/' if lang == 'fr' else '/')
    return DOMAIN + ('/fr/' if lang == 'fr' else '/') + page + '.html'

def structured_data(lang):
    desc = {'en': 'Mobile underwater video projector for swimming pools: games, swim lessons, workouts and events.',
            'fr': 'Vidéoprojecteur subaquatique mobile pour piscines : jeux, cours de natation, entraînements et événements.'}[lang]
    org = {'@type': 'Organization', '@id': DOMAIN + '/#org', 'name': 'Pool-On', 'legalName': 'SAS Pool-On',
           'url': DOMAIN + '/', 'logo': DOMAIN + '/assets/logo-full-color.png', 'email': 'contact@pool-on.com', 'telephone': '+33 6 51 92 72 02',
           'slogan': 'Unlimited Emotions', 'vatID': 'FR75909766222', 'taxID': '909766222',
           'address': {'@type': 'PostalAddress', 'streetAddress': '943 voie Antiope', 'postalCode': '13600',
                       'addressLocality': 'La Ciotat', 'addressCountry': 'FR'},
           'sameAs': SOCIAL}
    product = {'@type': 'Product', 'name': 'Pool-On PO-1.2', 'description': desc,
               'brand': {'@id': DOMAIN + '/#org'}, 'manufacturer': {'@id': DOMAIN + '/#org'},
               'image': DOMAIN + '/assets/unit-beam.webp', 'url': url('technology', lang)}
    site = {'@type': 'WebSite', '@id': DOMAIN + '/#site', 'name': 'Pool-On', 'url': DOMAIN + '/',
            'inLanguage': ['en', 'fr'], 'publisher': {'@id': DOMAIN + '/#org'}}
    data = {'@context': 'https://schema.org', '@graph': [org, site, product]}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>\n'

def seo():
    # Absolute alternates, canonical and share previews on every page, both languages.
    for lang in ('en', 'fr'):
        for p in PAGES:
            f = os.path.join(SITE, 'fr' if lang == 'fr' else '', p + '.html')
            h = open(f).read()
            h = re.sub(r'<link rel="alternate" hreflang="[a-z]+" href="[^"]*">\n', '', h)
            title = html.unescape(re.search(r'<title>(.*?)</title>', h).group(1))
            desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', h).group(1))
            esc = lambda v: html.escape(v, quote=True)
            tags = [
                '<link rel="canonical" href="%s">' % url(p, lang),
                '<link rel="alternate" hreflang="en" href="%s">' % url(p, 'en'),
                '<link rel="alternate" hreflang="fr" href="%s">' % url(p, 'fr'),
                '<link rel="alternate" hreflang="x-default" href="%s">' % url(p, 'en'),
                '<meta property="og:type" content="website">',
                '<meta property="og:site_name" content="Pool-On">',
                '<meta property="og:locale" content="%s">' % ('fr_FR' if lang == 'fr' else 'en_GB'),
                '<meta property="og:title" content="%s">' % esc(title),
                '<meta property="og:description" content="%s">' % esc(desc),
                '<meta property="og:url" content="%s">' % url(p, lang),
                '<meta property="og:image" content="%s/assets/og-image.jpg">' % DOMAIN,
                '<meta name="twitter:card" content="summary_large_image">',
            ]
            block = '\n'.join(tags) + '\n' + (structured_data(lang) if p == 'index' else '')
            h = h.replace('</head>', block + '</head>', 1)
            open(f, 'w').write(h)

def llms():
    open(os.path.join(SITE, 'llms.txt'), 'w').write("""# Pool-On

> Pool-On (SAS Pool-On, La Ciotat, France) makes the PO-1.2, a mobile underwater video projector that sits on the edge of a swimming pool and turns the water into a screen, to play, learn, work out, recover and relax. Patented system, laser projection technology by Optoma. POOL-ON is a registered EU trademark.

## Who it is for
- Public pools and aquatic centres: swim lessons, aquagym, events that bring people back to the water.
- Hotels, resorts and campsites: night shows and family entertainment around the pool.
- Fitness clubs and swim schools: pacers, timed workouts and coaching content on the pool floor.
- Event agencies: brand content and shows projected into the pool.

## Key facts
- Pool depth covered: 0.80 to 2.00 m.
- Weight: 18 kg, mobile, universal edge mount.
- Low voltage, rated for continuous 24/7 use; brightness 5,000 lm; Full HD.
- Content platform with games, immersive scenes, lessons and workouts, launched from a tablet or smartphone app; customers can add their own videos and logos.

## Pages
- [Solutions](%(d)s/solutions.html): uses by type of venue.
- [Content](%(d)s/content.html): the six ways to use the water, with videos.
- [Technology](%(d)s/technology.html): specifications and intellectual property.
- [References](%(d)s/references.html): installations, events and press.
- [Contact](%(d)s/contact.html): book a demo in your pool. Email: contact@pool-on.com. Phone: +33 6 51 92 72 02.
- French version: %(d)s/fr/
""" % {'d': DOMAIN})

SKIP = ('script', 'style', 'title', 'option', 'textarea')

def no_break(h):
    # Wrap the brand name in visible text so it never wraps at its hyphen.
    out, skip = [], None
    for part in re.split(r'(<[^>]+>)', h):
        if part.startswith('<'):
            m = re.match(r'<(/?)([a-zA-Z0-9]+)', part)
            if m and m.group(2).lower() in SKIP:
                skip = None if m.group(1) else m.group(2).lower()
        elif skip is None:
            part = re.sub(r'(Pool-On|POOL-ON)', r'<span class="nw">\1</span>', part)
        out.append(part)
    return ''.join(out)

def new_tab(h):
    # Links to other sites (social networks, press, YouTube) open in a new tab.
    def fix(m):
        tag = m.group(0)
        if 'target=' in tag or 'pool-on.com' in tag:
            return tag
        return tag[:-1] + ' target="_blank" rel="noopener">'
    return re.sub(r'<a\s[^>]*href="https?://[^"]*"[^>]*>', fix, h)

def wrap_brand():
    files = [os.path.join(SITE, 'fr' if l == 'fr' else '', p + '.html') for l in ('en', 'fr') for p in PAGES]
    files += [os.path.join(SITE, '404.html'), os.path.join(HERE, 'artifact-index.html')]
    for f in files:
        h = open(f).read()
        open(f, 'w').write(new_tab(no_break(h)))

not_found()
wrap_brand()
seo()
robots_and_sitemap()
llms()
