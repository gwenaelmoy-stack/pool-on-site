#!/usr/bin/env python3
"""Files for the production site, built after i18n.py: 404 page, robots.txt and sitemap.xml."""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(HERE), 'site')
DOMAIN = 'https://www.pool-on.com'
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

not_found()
robots_and_sitemap()
