#!/usr/bin/env python3
"""Post-process site/ (built by build.py): add the EN/FR switch, browser-language default and the French pages in site/fr/."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fr import FR, JS_FR

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(HERE), 'site')
PAGES = ['index', 'solutions', 'content', 'technology', 'references', 'contact', 'legal']

LANG_CSS = """
/* ---- language switch ---- */
.lang { display: inline-grid; place-items: center; min-width: 2.4rem; height: 2.4rem; padding: 0 .6rem; border: 1px solid var(--line); border-radius: 999px; font: 600 .8rem var(--f-mono); letter-spacing: .08em; color: var(--muted); text-decoration: none; }
.lang:hover { color: var(--fg); border-color: var(--fg); }
"""

def detect_script(target):
    # EN pages only: send French-speaking browsers to the French page, unless the visitor chose a language.
    return ("<script>(function(){var k='poolon-lang',p=null;try{p=localStorage.getItem(k)}catch(e){}"
            "if(/[?&]lang=en\\b/.test(location.search)){try{localStorage.setItem(k,'en')}catch(e){}return}"
            "if(p==='en')return;"
            "var l=(navigator.languages&&navigator.languages[0])||navigator.language||'';"
            f"if(p==='fr'||/^fr\\b/i.test(l))location.replace('{target}');}})();</script>\n")

REMEMBER = ("<script>document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[data-lang]');"
            "if(a){try{localStorage.setItem('poolon-lang',a.dataset.lang)}catch(_){}}});</script>\n")

def tr_text(html):
    def t(m):
        raw = m.group(1)
        s = raw.strip()
        if s in FR:
            lead = raw[:len(raw) - len(raw.lstrip())]
            trail = raw[len(raw.rstrip()):]
            return '>' + lead + FR[s] + trail + '<'
        return m.group(0)
    html = re.sub(r'>([^<>]+)<', t, html)
    def ta(m):
        v = m.group(2)
        return '%s="%s"' % (m.group(1), FR.get(v, v))
    html = re.sub(r'\b(alt|title|placeholder|aria-label|data-title|content)="([^"]*)"', ta, html)
    for a, b in JS_FR:
        html = html.replace(a, b)
    return html

def en_page(html, page, fragment):
    fr_href = 'fr/%s.html' % page
    html = html.replace('<div class="social"', '<a class="lang" href="%s" hreflang="fr" lang="fr" data-lang="fr" title="Version française">FR</a>\n    <div class="social"' % fr_href, 1)
    alt = '<link rel="alternate" hreflang="fr" href="%s">\n<link rel="alternate" hreflang="en" href="%s">\n' % (fr_href, './' if page == 'index' else page + '.html')
    head_add = alt + detect_script(fr_href)
    if fragment:
        html = head_add + html
    else:
        html = html.replace('</head>', head_add + '</head>', 1)
    return html.replace('</body>', REMEMBER + '</body>') if not fragment else html + REMEMBER

def fr_page(html, page):
    html = html.replace('<html lang="en">', '<html lang="fr">')
    html = re.sub(r'\b(src|poster)="assets/', r'\1="../assets/', html)
    html = html.replace('href="site.css"', 'href="../site.css"')
    html = html.replace('<a class="logo" href="./"', '<a class="logo" href="index.html"')
    en_href = ('../?lang=en' if page == 'index' else '../%s.html?lang=en' % page)
    html = html.replace('<div class="social"', '<a class="lang" href="%s" hreflang="en" lang="en" data-lang="en" title="English version">EN</a>\n    <div class="social"' % en_href, 1)
    alt = '<link rel="alternate" hreflang="en" href="%s">\n<link rel="alternate" hreflang="fr" href="%s.html">\n' % ('../' if page == 'index' else '../%s.html' % page, page)
    html = html.replace('</head>', alt + '</head>', 1)
    html = html.replace('</body>', REMEMBER + '</body>')
    return tr_text(html)

def main():
    css_p = os.path.join(SITE, 'site.css')
    css = open(css_p).read()
    if '/* ---- language switch ---- */' not in css:
        open(css_p, 'w').write(css + LANG_CSS)
    os.makedirs(os.path.join(SITE, 'fr'), exist_ok=True)
    for page in PAGES:
        p = os.path.join(SITE, page + '.html')
        en = open(p).read()
        open(os.path.join(SITE, 'fr', page + '.html'), 'w').write(fr_page(en, page))
        open(p, 'w').write(en_page(en, page, False))
    frag_p = os.path.join(HERE, 'artifact-index.html')
    open(frag_p, 'w').write(en_page(open(frag_p).read(), 'index', True))
    # report untranslated visible text on FR pages
    left = set()
    for page in PAGES:
        h = open(os.path.join(SITE, 'fr', page + '.html')).read()
        h = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', h, flags=re.S)
        for m in re.finditer(r'>([^<>]+)<', h):
            s = m.group(1).strip()
            if re.search(r'\b(the|and|your|with|for|our)\b', s, re.I):
                left.add(s)
    print('untranslated?', sorted(left))

main()
