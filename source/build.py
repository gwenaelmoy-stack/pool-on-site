#!/usr/bin/env python3
"""Generate the multi-page Pool-On static site into site/ from shared header/footer."""
import os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)          # repository root
OUT = os.path.join(ROOT, 'site')      # published folder (assets live in site/assets)
os.makedirs(OUT, exist_ok=True)

EXTRA_CSS = r"""
/* ---- multi-page additions ---- */
nav.main a[aria-current="page"] { color: var(--fg); text-decoration: underline; text-decoration-color: var(--lumen); text-underline-offset: .45em; text-decoration-thickness: 2px; }
.page-hero { position: relative; overflow: hidden; border-bottom: 1px solid var(--line); }
.page-hero .bgimg { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; }
.page-hero::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, var(--bg) 0%, color-mix(in srgb, var(--bg) 85%, transparent) 45%, color-mix(in srgb, var(--bg) 15%, transparent) 100%); }
@media (max-width: 760px) { .page-hero::after { background: linear-gradient(180deg, color-mix(in srgb, var(--bg) 50%, transparent), var(--bg) 90%); } }
.page-hero .wrap { position: relative; z-index: 1; display: grid; gap: 1.1rem; padding-block: clamp(3.5rem, 9vw, 6.5rem); }
.page-hero h1 { font-size: clamp(2.6rem, 7vw, 5rem); text-transform: uppercase; max-width: 14ch; }
.page-hero h1 em { font-style: normal; color: var(--lumen-ink); }
.page-hero p { font-size: 1.15rem; max-width: 52ch; }
.split { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: clamp(1.5rem, 4vw, 3.5rem); align-items: center; }
.split.rev > :first-child { order: 2; }
@media (max-width: 760px) { .split { grid-template-columns: 1fr; } .split.rev > :first-child { order: 0; } }
.split img, .split video { width: 100%; aspect-ratio: 4 / 3; object-fit: cover; display: block; border: 1px solid var(--line); }
.split .txt { display: grid; gap: .9rem; align-content: center; }
.split .txt ul { margin: 0; padding-left: 1.1rem; color: var(--muted); display: grid; gap: .35rem; }
.split .tagline { font-family: var(--f-display); font-size: 1.5rem; font-weight: 600; color: var(--lumen-ink); text-transform: uppercase; }
.stack { display: grid; gap: clamp(3rem, 7vw, 5rem); }
.benefits { display: grid; grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr)); gap: 1.5rem; }
.benefit { border-left: 3px solid var(--lumen); padding-left: 1rem; display: grid; gap: .5rem; align-content: start; }
.benefit p { color: var(--muted); }
.steps { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(13rem, 1fr)); gap: 1.5rem; counter-reset: s; }
.steps li { counter-increment: s; display: grid; gap: .4rem; border-top: 1px solid var(--line); padding-top: 1rem; }
.steps li::before { content: "0" counter(s); font-family: var(--f-display); font-weight: 800; font-size: 2.6rem; line-height: 1; color: var(--cyan); }
.steps p { color: var(--muted); }
.teasers { display: grid; grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr)); gap: 1.25rem; }
.teaser { display: grid; gap: .6rem; text-decoration: none; min-width: 0; }
.teaser img { width: 100%; aspect-ratio: 4 / 3; object-fit: cover; display: block; border: 1px solid var(--line); transition: transform .3s; }
.teaser:hover img { transform: scale(1.02); }
.teaser .tag { font-family: var(--f-mono); font-size: .75rem; color: var(--cyan); letter-spacing: .1em; text-transform: uppercase; }
.teaser h3 { font-size: 1.4rem; }
.teaser p { color: var(--muted); font-size: .95rem; }
.more { font-weight: 700; color: var(--lumen-ink); text-decoration: none; }
.more:hover { text-decoration: underline; }
.cta-band { background: var(--bg-2); border-bottom: 1px solid var(--line); }
.cta-band .wrap { display: flex; flex-wrap: wrap; gap: 1.5rem; align-items: center; justify-content: space-between; padding-block: clamp(2.5rem, 6vw, 4rem); }
.cta-band h2 { font-size: clamp(1.9rem, 4.5vw, 3rem); }
.videos { display: grid; grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr)); gap: 1.25rem; }
.yt { position: relative; aspect-ratio: 16 / 9; border: 1px solid var(--line); background: #000; overflow: hidden; }
.yt button { all: unset; cursor: pointer; position: absolute; inset: 0; display: grid; place-items: center; }
.yt button img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: .75; }
.yt button::before { content: '▶'; position: relative; z-index: 1; display: grid; place-items: center; width: 3.4rem; height: 3.4rem; border-radius: 50%; background: var(--lumen); color: var(--on-lumen); font-size: 1.1rem; padding-left: .2rem; box-sizing: border-box; }
.yt button span { position: absolute; left: 0; right: 0; bottom: 0; padding: 2.2rem 1rem .8rem; background: linear-gradient(transparent, rgba(0, 0, 0, .85)); color: #fff; font-weight: 700; line-height: 1.3; }
.yt button:focus-visible::before { outline: 3px solid #fff; outline-offset: 3px; }
.yt iframe { position: absolute; inset: 0; width: 100%; height: 100%; border: 0; }
.legal { display: grid; gap: 2rem; max-width: 48rem; }
.legal section { display: grid; gap: .6rem; }
.legal h2 { font-size: clamp(1.6rem, 3.5vw, 2.2rem); }
.legal dl { margin: 0; display: grid; grid-template-columns: auto minmax(0, 1fr); gap: .5rem 1.2rem; }
.legal dt { color: var(--muted); }
.legal dd { margin: 0; overflow-wrap: anywhere; min-width: 0; }
.legal .todo, .contact .todo { white-space: normal; }
.legal p { color: var(--muted); }
/* Home hero: the PO-1.2 YouTube film from the current site, full-bleed behind the title */
.hero-yt { min-height: min(88vh, 52rem); display: grid; align-items: center; background: #000; }
.hero-yt .yt-bg { position: absolute; inset: 0; overflow: hidden; pointer-events: none; opacity: 0; transition: opacity .8s; }
.hero-yt .yt-bg.playing { opacity: 1; }
.hero-yt .wrap { width: 100%; }
.hero-yt .vid-toggle { display: none; }
.hero-yt.has-film .vid-toggle { display: block; }
.hero-yt .yt-bg iframe { position: absolute; top: 50%; left: 50%; width: max(100%, calc(100vh * 16 / 9 * 1.0)); height: max(100%, calc(100vw * 9 / 16)); min-width: 177.78vh; transform: translate(-50%, -50%); border: 0; }
.hero-yt::after { z-index: 0; }
.hero-yt .wrap { z-index: 1; }
.vid-toggle { position: absolute; right: max(16px, env(safe-area-inset-right, 0px)); bottom: 1rem; z-index: 2; font: 600 .8rem var(--f-mono); color: #fff; background: rgba(0,0,0,.45); border: 1px solid rgba(255,255,255,.4); border-radius: 999px; padding: .4rem .8rem; cursor: pointer; }
.vid-toggle:hover { background: rgba(0,0,0,.65); }
footer .cols { display: flex; flex-wrap: wrap; gap: .4rem 1.2rem; }
footer a { color: var(--fg); }
"""

INSTA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.8.1 3.3.1 4.8 1.7 4.9 4.9.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 3.2-1.7 4.8-4.9 4.9-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-3.3-.1-4.8-1.7-4.9-4.9C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8C2.4 3.9 3.9 2.4 7.2 2.3 8.4 2.2 8.8 2.2 12 2.2zM12 0C8.7 0 8.3 0 7.1.1 2.7.3.3 2.7.1 7.1 0 8.3 0 8.7 0 12s0 3.7.1 4.9c.2 4.4 2.6 6.8 7 7 1.2.1 1.6.1 4.9.1s3.7 0 4.9-.1c4.4-.2 6.8-2.6 7-7 .1-1.2.1-1.6.1-4.9s0-3.7-.1-4.9c-.2-4.4-2.6-6.8-7-7C15.7 0 15.3 0 12 0zm0 5.8a6.2 6.2 0 1 0 0 12.4 6.2 6.2 0 0 0 0-12.4zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.4-11.8a1.4 1.4 0 1 0 0 2.9 1.4 1.4 0 0 0 0-2.9z"/></svg>'
LINKEDIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.4 20.5h-3.6v-5.6c0-1.3 0-3-1.8-3s-2.1 1.4-2.1 2.9v5.7H9.4V9h3.4v1.6h.1c.5-.9 1.6-1.8 3.4-1.8 3.6 0 4.3 2.4 4.3 5.5v6.2zM5.3 7.4a2.1 2.1 0 1 1 0-4.2 2.1 2.1 0 0 1 0 4.2zM7.1 20.5H3.6V9h3.5v11.5zM22.2 0H1.8C.8 0 0 .8 0 1.7v20.6c0 .9.8 1.7 1.8 1.7h20.4c1 0 1.8-.8 1.8-1.7V1.7C24 .8 23.2 0 22.2 0z"/></svg>'
YOUTUBE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4.5A3 3 0 0 0 .5 6.2 31.4 31.4 0 0 0 0 12a31.4 31.4 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1A31.4 31.4 0 0 0 24 12a31.4 31.4 0 0 0-.5-5.8zM9.6 15.6V8.4l6.3 3.6-6.3 3.6z"/></svg>'

NAV = [('solutions.html', 'Solutions'), ('content.html', 'Content'), ('technology.html', 'Technology'),
       ('references.html', 'References'), ('contact.html', 'Contact')]

def header(cur):
    links = '\n'.join('      <a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == cur else '', t) for h, t in NAV)
    return f'''<header class="top">
  <div class="wrap">
    <a class="logo" href="./" aria-label="Pool-On home"><img class="logo-w" src="assets/logo-white.png" alt="Pool-On" width="480" height="119"><img class="logo-c" src="assets/logo-color.png" alt="Pool-On" width="480" height="124"></a>
    <nav class="main" aria-label="Main">
{links}
    </nav>
    <div class="social" aria-label="Pool-On on social media">
      <a href="https://www.instagram.com/pool_on_experience/" aria-label="Pool-On on Instagram" title="Instagram">{INSTA}</a>
      <a href="https://www.linkedin.com/company/pool-on" aria-label="Pool-On on LinkedIn" title="LinkedIn">{LINKEDIN}</a>
      <a href="https://www.youtube.com/@pool-on2405" aria-label="Pool-On on YouTube" title="YouTube">{YOUTUBE}</a>
    </div>
    <a class="btn btn-primary" href="contact.html">Book a demo</a>
  </div>
</header>
'''

FOOTER = '''
<footer>
  <div class="wrap">
    <div class="foot-logo"><img class="logo-w" src="assets/logo-full-white.png" alt="Pool-On, Unlimited Emotions" width="520" height="164"><img class="logo-c" src="assets/logo-full-color.png" alt="Pool-On, Unlimited Emotions" width="520" height="169"></div>
    <span>Pool-On SAS · 943 voie Antiope, 13600 La Ciotat, France · RCS Marseille 909 766 222</span>
    <span>POOL-ON is a registered EU trademark (EUIPO no. 018650491). Optoma and DuraCore are trademarks of their respective owner.</span>
    <div class="cols">
      <a href="solutions.html">Solutions</a><a href="content.html">Content</a><a href="technology.html">Technology</a><a href="references.html">References</a><a href="contact.html">Contact</a><a href="legal.html">Legal notice &amp; privacy</a>
    </div>
    <span>Follow us: <a href="https://www.instagram.com/pool_on_experience/">Instagram</a> · <a href="https://www.linkedin.com/company/pool-on">LinkedIn</a> · <a href="https://www.youtube.com/@pool-on2405">YouTube</a></span>
  </div>
</footer>
'''

FONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;800&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=JetBrains+Mono:wght@400;600&display=swap">
<link rel="stylesheet" href="site.css">'''

SCRIPT = '''
<script>
(function () {
  document.querySelectorAll('.yt button').forEach(function (b) {
    b.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + b.dataset.id + '?autoplay=1';
      f.title = b.dataset.title; f.allow = 'autoplay; encrypted-media; picture-in-picture'; f.allowFullscreen = true;
      b.replaceWith(f);
    });
  });
  var yt = document.getElementById('hero-yt'), t = document.getElementById('hero-toggle');
  if (yt && t) {
    var paused = false;
    var send = function (f) { yt.contentWindow.postMessage(JSON.stringify({ event: 'command', func: f, args: [] }), '*'); };
    var setLabel = function () { t.textContent = paused ? 'Play video' : 'Pause video'; t.setAttribute('aria-pressed', paused ? 'true' : 'false'); };
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { yt.parentNode.remove(); t.remove(); }
    else {
      // Show the film only once YouTube reports it is playing; otherwise the photo stays.
      yt.addEventListener('load', function () { yt.contentWindow.postMessage(JSON.stringify({ event: 'listening', id: 'hero' }), '*'); });
      window.addEventListener('message', function (e) {
        if (!/youtube(-nocookie)?\.com$/.test(new URL(e.origin).hostname)) return;
        var d; try { d = JSON.parse(e.data); } catch (_) { return; }
        var st = d && d.info && d.info.playerState;
        if (st === 1) { yt.parentNode.classList.add('playing'); yt.closest('.hero').classList.add('has-film'); }
      });
      t.addEventListener('click', function () { paused = !paused; send(paused ? 'pauseVideo' : 'playVideo'); setLabel(); });
    }
  }
  var form = document.getElementById('demo-form');
  if (!form) return;
  var note = document.getElementById('form-note');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var name = document.getElementById('f-name').value.trim();
    var email = document.getElementById('f-email').value.trim();
    if (!name || !/^\\S+@\\S+\\.\\S+$/.test(email)) { note.textContent = 'Please add your name and a valid work email.'; return; }
    // No server: open the visitor's email app with the request ready to send.
    var lines = [];
    form.querySelectorAll('label').forEach(function (l) {
      var f = l.querySelector('input, select, textarea');
      if (f && f.value.trim()) lines.push(l.firstChild.textContent.trim() + ' : ' + f.value.trim());
    });
    var org = document.getElementById('f-org').value.trim();
    var subject = 'Pool-On demo request · ' + name + (org ? ' (' + org + ')' : '');
    location.href = 'mailto:contact@pool-on.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\\n'));
    note.textContent = 'Your email app should open with the request ready to send. If nothing happens, write to contact@pool-on.com.';
  });
})();
</script>
'''

def page(fname, title, desc, cur, body, standalone=True):
    head = f'<title>{title}</title>\n<meta name="description" content="{desc}">\n<meta name="claude:viewport-fit-sides" content="cover">\n{FONTS}\n'
    html = header(cur) + '\n<main id="top">\n' + body + '\n</main>\n' + FOOTER + SCRIPT
    frag = head + html
    if not standalone:
        open(os.path.join(HERE, 'artifact-index.html'), 'w').write(frag)
    if True:
        html = '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n' + head + '</head>\n<body>\n' + html + '</body>\n</html>\n'
    open(os.path.join(OUT, fname), 'w').write(html)

def cta(title='See it in your pool', text='We bring a unit to your pool for a live demo.'):
    return f'''
  <div class="cta-band"><div class="wrap">
    <div><h2>{title}</h2><p style="margin-top:.6rem;color:var(--muted)">{text}</p></div>
    <a class="btn btn-primary" href="contact.html">Book a demo</a>
  </div></div>'''

def phero(img, eyebrow, h1, text, pos='50% 50%'):
    return f'''
  <section class="page-hero">
    <img class="bgimg" src="assets/{img}" alt="" style="object-position:{pos}">
    <div class="wrap">
      <span class="eyebrow">{eyebrow}</span>
      <h1>{h1}</h1>
      <p>{text}</p>
    </div>
  </section>'''

PARTNERS = [('optoma', 'Optoma'), ('microsoft', 'Microsoft'), ('bpifrance', 'Bpifrance'), ('credit-agricole', 'Crédit Agricole'),
            ('french-tech', 'La French Tech'), ('fpp', 'Fédération des Professionnels de la Piscine et du Spa'),
            ('piscine-de-demain', 'La piscine de demain'), ('cosmo-av', 'Cosmo AV'), ('sportech', 'Sportech')]
def partners():
    lis = '\n'.join(f'          <li><img src="assets/partners/{f}.webp" alt="{a}" loading="lazy"></li>' for f, a in PARTNERS)
    return f'''
      <div class="partners" aria-label="Partners and support">
        <span class="eyebrow">Partners and support</span>
        <ul>
{lis}
        </ul>
      </div>'''

MODES = [
    ('enjoy', 'Enjoy', 'fish.webp', 'A projected tropical fish on the pool floor', 'Share the pool',
     'Games and immersive scenes for everyone in the water: explore a lagoon, swim through outer space or visit an art gallery.',
     ['Lagoon, ocean and space scenes', 'Art gallery series, from Van Gogh to street art', 'Family games for all ages']),
    ('learn', 'Learn', 'lesson-kids.webp', 'Children at the pool edge ready for a projected swim lesson', 'Learning has never been that fun!',
     'Gamified swim lessons, designed with national swimming coaches, that build water confidence step by step.',
     ['Progressive lessons for schools and swim schools', 'Water-confidence games for beginners', 'Content built with national coaches']),
    ('workout', 'Work out', 'timer.webp', 'A projected race timer on a pool lane, next to the Pool-On unit', 'Push your limits with our avatars!',
     'Immersive workouts: follow an avatar pacer, take on challenges and race the clock projected in your lane.',
     ['Avatar pacers per lane', 'Timed sets and challenges', 'Projected race timer']),
    ('coach', 'Coach groups', 'aquabike.webp', 'An aquabike class over a projected workout grid', 'Upgrade your aquatic fitness activities!',
     'Dedicated programmes for aquabike, aquagym and aquatraining. Every participant follows the same on-screen coach.',
     ['Aquabike and aquagym classes', 'Aquatraining circuits', 'Rehabilitation and gentle sessions']),
    ('entertain', 'Entertain', 'vangogh-night.webp', 'A Van Gogh painting projected into a hotel pool at night', 'Create never-seen-before events all year long!',
     'Turn the pool into a stage for MICE events: team building, corporate evenings and sponsored sessions.',
     ['Evening shows by the pool', 'Team-building challenges', 'Sponsored sessions']),
    ('broadcast', 'Open broadcast', 'vangogh-kids.webp', 'Children swimming over a projected Van Gogh artwork', 'Your pool, your content',
     'Upload your own videos, logos and brand content to personalise the experience in your pool.',
     ['Your logo and visuals under the water', 'Your own video playlists', 'Brand activations and launches']),
]

MARKETS = [
    ('public', 'Public pools · aquatic centres', 'Fill the off-peak hours', 'coach.webp', 'A coach runs a projected swim lesson from a tablet at the pool edge',
     'Gamified sessions bring families, schools and clubs back between the busy slots, and give your staff new tools to teach.',
     ['Swim lessons built with national swimming coaches', 'Themed family sessions at weekends and holidays', 'A paid add-on to the standard ticket', 'Rehabilitation and senior programmes']),
    ('hotels', 'Hotels · resorts · campsites', 'A pool guests talk about', 'hotel-event.webp', 'Guests dining around a hotel pool at night while a Pool-On unit projects images under the water',
     'Evening shows, kids\' clubs and a visual signature for the pool area that guests share on social media.',
     ['Lagoon, space and art gallery scenes', 'Kids\' club programmes', 'Night shows for the bar and terrace', 'Your own branded content']),
    ('fitness', 'Aquafitness · clubs', 'Coach a full class', 'aquabike.webp', 'An aquabike class over a projected workout grid',
     'Guided aquabike, aquagym and aquatraining, with an on-screen coach every participant can follow.',
     ['Avatar-led workouts', 'Timed training sets in each lane', 'Group programmes updated over time']),
    ('events', 'Events · MICE', 'Rent the pool as a stage', 'festival-night.webp', 'Pool-On units projecting festival content into a pool at night, in front of an open-air cinema screen',
     'Team building, corporate evenings and sponsored sessions, with your logo and content under the water. Several units can run together.',
     ['Team challenges', 'Sponsored broadcasts', 'Multi-unit shows for large pools', 'Live or recorded content']),
]

def build():
    css = open(os.path.join(ROOT, 'site', 'site.css')).read()
    if '/* ---- multi-page additions ---- */' not in css:
        open(os.path.join(OUT, 'site.css'), 'w').write(css + EXTRA_CSS)

    # ---------- Home ----------
    teasers = '\n'.join(f'''        <a class="teaser" href="solutions.html#{k}"><img src="assets/{img}" alt="{alt}" loading="lazy"><span class="tag">{tag}</span><h3>{h}</h3><p>{txt.split('. ')[0].rstrip('.')}.</p></a>'''
                        for k, tag, h, img, alt, txt, _ in MARKETS)
    modes = '\n'.join(f'''        <a class="mode" href="content.html#{k}" style="text-decoration:none"><img src="assets/{img}" alt="{alt}" loading="lazy"><h3>{t}</h3><p>{tl}</p></a>'''
                      for k, t, img, alt, tl, _, _ in MODES)
    home = f'''  <section class="hero hero-yt" aria-labelledby="hero-title">
    <img class="bgimg" src="assets/hero-swimmer.webp" alt="" width="1600" height="900">
    <div class="yt-bg" aria-hidden="true">
      <iframe id="hero-yt" src="https://www.youtube-nocookie.com/embed/P-LIjyV7Huk?autoplay=1&amp;mute=1&amp;loop=1&amp;playlist=P-LIjyV7Huk&amp;controls=0&amp;rel=0&amp;playsinline=1&amp;modestbranding=1&amp;iv_load_policy=3&amp;disablekb=1&amp;enablejsapi=1" title="Pool-On PO-1.2 film" allow="autoplay; encrypted-media" tabindex="-1"></iframe>
    </div>
    <button class="vid-toggle" type="button" id="hero-toggle" aria-pressed="false">Pause video</button>
    <div class="wrap">
      <span class="eyebrow">The world-first underwater video projector</span>
      <h1 id="hero-title">Turn your pool into a <em>new playground</em></h1>
      <p class="lede">Pool-On projects games, swim lessons and guided workouts onto the bottom of the pool. It clamps onto the edge, needs no construction work and runs from a tablet.</p>
      <div class="actions">
        <a class="btn btn-primary" href="contact.html">Book a demo in your pool</a>
        <a class="btn btn-ghost" href="solutions.html">See what it does</a>
      </div>
      <span class="credit">Patented system · Laser projection technology by Optoma</span>
    </div>
  </section>

  <div class="proof">
    <div class="wrap">
      <div><b>0.80–2.00 m</b><small>Pool depth range covered</small></div>
      <div><b>18 kg</b><small>Mobile unit, universal edge mount</small></div>
      <div><b>24 / 7</b><small>Low voltage, rated for continuous use</small></div>
    </div>
  </div>

  <section class="block" aria-labelledby="intro-title">
    <div class="wrap split">
      <video class="unit-video" autoplay muted loop playsinline poster="assets/po11-branded-poster.webp" aria-label="The Pool-On PO-1.2 unit turning, with the Pool-On logo"><source src="assets/po11-branded.webm" type="video/webm"><source src="assets/po11-branded.mp4" type="video/mp4"></video>
      <div class="txt">
        <span class="eyebrow">The new PO-1.2</span>
        <h2 id="intro-title">Live never-seen-before experiences</h2>
        <p>A mobile projector that sits on the pool edge and turns the water into a screen, to play, learn, work out, recover and relax.</p>
        <a class="more" href="technology.html">Discover the technology →</a>
      </div>
    </div>
  </section>

  <section class="block" aria-labelledby="benef-title">
    <div class="wrap">
      <div class="head">
        <span class="eyebrow">Why Pool-On</span>
        <h2 id="benef-title">Reveal the full potential of your pool</h2>
      </div>
      <div class="benefits">
        <div class="benefit"><h3>Never seen before</h3><p>Unique experiences that bring visitors back, raise average spend and renew the appeal of the pool for users and staff.</p></div>
        <div class="benefit"><h3>For all</h3><p>Suited to every age and purpose: water confidence, health, training and leisure. Accessible to everyone.</p></div>
        <div class="benefit"><h3>Easy to set up &amp; use</h3><p>Non-invasive. A universal fastening system on the pool edge, and everything runs from the mobile app.</p></div>
      </div>
    </div>
  </section>

  <section class="block" aria-labelledby="sol-title">
    <div class="wrap">
      <div class="head">
        <span class="eyebrow">Solutions</span>
        <h2 id="sol-title">More visits, longer sessions, new revenue</h2>
        <p>One unit turns an ordinary pool into a venue people come back to. Each market uses it differently.</p>
      </div>
      <div class="teasers">
{teasers}
      </div>
    </div>
  </section>

  <section class="block" aria-labelledby="content-title">
    <div class="wrap">
      <div class="head">
        <span class="eyebrow">Content platform</span>
        <h2 id="content-title">Turn your pool into an augmented playfield</h2>
        <p>Every unit comes with a content library, updated over time and launched from the app.</p>
      </div>
      <div class="modes">
{modes}
      </div>
      <a class="more" href="content.html">Explore the content →</a>
    </div>
  </section>

  <section class="block" aria-labelledby="ref-title">
    <div class="wrap">
      <div class="head">
        <span class="eyebrow">References</span>
        <h2 id="ref-title">Already in the water</h2>
      </div>
      <div class="refs">
        <article class="ref"><img src="assets/hotel-event.webp" alt="Guests dining around a hotel pool at night while a Pool-On unit projects images under the water" loading="lazy"><div class="body"><b>Hotel event</b><small>Evening dinner around the pool</small></div></article>
        <article class="ref"><img src="assets/festival-night.webp" alt="Pool-On units projecting festival content into a pool at night, in front of an open-air cinema screen" loading="lazy"><div class="body"><b>Film festival</b><small>Multi-unit night show · 2025</small></div></article>
        <article class="ref"><img src="assets/lane-coach.webp" alt="A coach watches a swimmer follow a projected pacer in a lane" loading="lazy"><div class="body"><b>Swim lesson trial</b><small>Club pool · 2025</small></div></article>
      </div>
      <a class="more" href="references.html">All references and press →</a>
{partners()}
    </div>
  </section>
{cta()}'''
    page('index.html', 'Pool-On · Underwater projection that turns your pool into a playground', 'Pool-On turns any pool into a new playground with underwater video projection: games, swim lessons, workouts and events.', 'index.html', home, standalone=False)

    # ---------- Solutions ----------
    rows = []
    for i, (k, tag, h, img, alt, txt, lst) in enumerate(MARKETS):
        lis = ''.join(f'<li>{x}</li>' for x in lst)
        rows.append(f'''      <article class="split{' rev' if i % 2 else ''}" id="{k}">
        <img src="assets/{img}" alt="{alt}" loading="lazy">
        <div class="txt"><span class="eyebrow">{tag}</span><h2>{h}</h2><p>{txt}</p><ul>{lis}</ul></div>
      </article>''')
    sol = phero('beam.webp', 'Solutions', 'One pool, <em>many new uses</em>', 'Public pools, hotels, fitness clubs and event agencies use Pool-On to bring people back to the water.') + f'''
  <section class="block">
    <div class="wrap stack">
{chr(10).join(rows)}
    </div>
  </section>

  <section class="block" aria-labelledby="dist-title">
    <div class="wrap split">
      <img src="assets/unit-beam.webp" alt="Pool-On unit clamped on the edge of a tiled pool" loading="lazy">
      <div class="txt">
        <span class="eyebrow">Distributors · pool builders</span>
        <h2 id="dist-title">Add Pool-On to your offer</h2>
        <p>We work with pool builders, AV integrators and distributors in France and abroad. Ask for the partner kit: pricing, demo unit and sales material.</p>
        <a class="more" href="contact.html">Ask for the partner kit →</a>
      </div>
    </div>
  </section>
{cta()}'''
    page('solutions.html', 'Solutions · Pool-On', 'Pool-On for public pools, hotels and resorts, aquafitness clubs and events.', 'solutions.html', sol)

    # ---------- Content ----------
    rows = []
    for i, (k, t, img, alt, tl, txt, lst) in enumerate(MODES):
        lis = ''.join(f'<li>{x}</li>' for x in lst)
        rows.append(f'''      <article class="split{' rev' if i % 2 else ''}" id="{k}">
        <img src="assets/{img}" alt="{alt}" loading="lazy">
        <div class="txt"><span class="eyebrow">0{i+1} · {t}</span><h2>{t}</h2><p class="tagline">{tl}</p><p>{txt}</p><ul>{lis}</ul></div>
      </article>''')
    vids = [('WRbjczqsS3s', 'swimmer-reef.webp', 'For every kind of swimmer'),
            ('z55A_94QFq4', 'kid-ocean.webp', 'Balance and propulsion at any age'),
            ('EmmPKbM0njA', 'aquagym.webp', 'The art of making people swim more'),
            ('5GvZ9gLcAc8', 'lesson-kids.webp', 'Kids more at ease in the water'),
            ('QUObB2R9hnM', 'vangogh-kids.webp', 'As seen on M6, 12.45 news'),
            ('TDs6DKlaLJk', 'mountain.webp', 'France 3 Provence-Alpes-Côte d’Azur report')]
    vhtml = '\n'.join(f'''        <div class="yt"><button type="button" data-id="{v}" data-title="{t}"><img src="assets/{p}" alt="" loading="lazy"><span>{t}</span></button></div>''' for v, p, t in vids)
    cont = phero('mountain.webp', 'Content platform', 'An <em>augmented playfield</em>', 'Six ways to use the water, from a family lagoon to a timed workout. New content is added over time and launched from the app.', '50% 40%') + f'''
  <section class="block">
    <div class="wrap">
      <div class="shots">
        <figure><img src="assets/turtle.webp" alt="A sea turtle scene projected onto the floor of an indoor pool" loading="lazy"><figcaption>Enjoy · ocean scene, indoor pool</figcaption></figure>
        <figure><img src="assets/kid-ocean.webp" alt="A child swims over a projected seabed with starfish" loading="lazy"><figcaption>Learn · treasure hunt</figcaption></figure>
        <figure><img src="assets/swimmer-reef.webp" alt="A swimmer glides over a projected coral reef" loading="lazy"><figcaption>Swim · coral reef</figcaption></figure>
      </div>
      <div class="stack">
{chr(10).join(rows)}
      </div>
    </div>
  </section>

  <section class="block" aria-labelledby="vid-title">
    <div class="wrap">
      <div class="head">
        <span class="eyebrow">Videos</span>
        <h2 id="vid-title">See it in the water</h2>
        <p>Videos load from YouTube only when you press play.</p>
      </div>
      <div class="videos">
{vhtml}
      </div>
      <a class="more" href="https://www.youtube.com/@pool-on2405">All videos on our YouTube channel →</a>
    </div>
  </section>
{cta('Try the content in your pool', 'We bring a unit and run a session with your team.')}'''
    page('content.html', 'Content · Pool-On', 'The Pool-On content platform: enjoy, learn, work out, coach groups, entertain and broadcast your own content.', 'content.html', cont)

    # ---------- Technology ----------
    tech = phero('unit-beam.webp', 'Technology', 'Built for <em>chlorinated water</em> and daily use', 'A patented, mobile underwater projection system with an Optoma laser engine, rated for continuous use.', '50% 60%') + '''
  <section class="block" aria-labelledby="spec-title">
    <div class="wrap">
      <div class="head"><span class="eyebrow">PO-1.2</span><h2 id="spec-title">Specifications</h2></div>
      <div class="tech">
        <video class="unit-video" autoplay muted loop playsinline poster="assets/po11-branded-poster.webp" aria-label="The Pool-On PO-1.2 unit turning"><source src="assets/po11-branded.webm" type="video/webm"><source src="assets/po11-branded.mp4" type="video/mp4"></video>
        <div>
          <table class="specs">
            <tbody>
              <tr><th scope="row">Pool depth</th><td>0.80 m to 2.00 m</td></tr>
              <tr><th scope="row">Weight</th><td>18 kg, mobile</td></tr>
              <tr><th scope="row">Mounting</th><td>Universal edge mount, no construction work</td></tr>
              <tr><th scope="row">Light source</th><td>Optoma DuraCore laser, Full HD</td></tr>
              <tr><th scope="row">Brightness</th><td>5,000 lm</td></tr>
              <tr><th scope="row">Resolution</th><td>1920 × 1080 Full HD</td></tr>
              <tr><th scope="row">Protection</th><td>IP5X · IP69K</td></tr>
              <tr><th scope="row">Power</th><td>Low voltage, rated 24/7</td></tr>
              <tr><th scope="row">Control</th><td>Tablet and smartphone app</td></tr>
              <tr><th scope="row">Content</th><td>Platform access + your own content</td></tr>
            </tbody>
          </table>
          <div class="cta-row"><a class="btn btn-ghost" href="contact.html">Request the spec sheet (PDF)</a></div>
        </div>
      </div>
    </div>
  </section>

  <section class="block" aria-labelledby="setup-title">
    <div class="wrap">
      <div class="head"><span class="eyebrow">Installation</span><h2 id="setup-title">Easy to set up, in a snap, on any poolside</h2></div>
      <ol class="steps">
        <li><h3>Clamp</h3><p>The universal fastening system fits the pool edge. No drilling, no construction work.</p></li>
        <li><h3>Plug</h3><p>Low-voltage power supply, safe around water and rated for 24/7 use.</p></li>
        <li><h3>Play</h3><p>Pick a programme in the app and the show starts on the bottom of the pool.</p></li>
      </ol>
      <figure class="setup">
        <img src="assets/timer.webp" alt="Pool-On unit on the edge of a lane, projecting a race timer" loading="lazy">
        <figcaption><strong>On the pool edge, ready in minutes.</strong> One unit covers a lane or a play area.</figcaption>
      </figure>
    </div>
  </section>

  <section class="block" aria-labelledby="pat-title">
    <div class="wrap">
      <div class="head"><span class="eyebrow">Intellectual property</span><h2 id="pat-title">Patented in France, filed worldwide</h2></div>
      <div class="patent">
        <div class="no"><small>Pool-On system</small>Patented</div>
        <div>
          <p>The Pool-On projection system is protected by a granted French patent, with international applications under the PCT. POOL-ON is a registered EU trademark.</p>
          <ul aria-label="Patent coverage"><li>FR · granted</li><li>EP · pending</li><li>US · pending</li><li>CN · pending</li><li>AU · pending</li></ul>
        </div>
      </div>
    </div>
  </section>
''' + cta()
    page('technology.html', 'Technology · Pool-On', 'PO-1.2 specifications: 0.80 to 2 m depth, 18 kg, Optoma laser, IP5X and IP69K, 24/7 low voltage, patented.', 'technology.html', tech)

    # ---------- References ----------
    refs = phero('vangogh-night.webp', 'References', 'Already <em>in the water</em>', 'Hotels, events and pools where Pool-On has already been installed or shown.', '50% 60%') + f'''
  <section class="block">
    <div class="wrap">
      <div class="stack">
        <article class="split">
          <img src="assets/hotel-event.webp" alt="Guests dining around a hotel pool at night while a Pool-On unit projects images under the water" loading="lazy">
          <div class="txt"><span class="eyebrow">Hotel · Event</span><h2>Hotel event</h2><p>An evening dinner around the hotel pool: the Pool-On unit sits on the edge and turns the water into a screen for the guests.</p></div>
        </article>
        <article class="split rev">
          <img src="assets/festival-night.webp" alt="Pool-On units projecting festival content into a pool at night, in front of an open-air cinema screen" loading="lazy">
          <div class="txt"><span class="eyebrow">Event · 2025</span><h2>Film festival</h2><p>A multi-unit night show: festival branding and content projected across the pool.</p></div>
        </article>
        <article class="split">
          <img src="assets/lane-coach.webp" alt="A coach watches a swimmer follow a projected pacer" loading="lazy">
          <div class="txt"><span class="eyebrow">Swim club · 2025</span><h2>Swim lesson trial</h2><p>Coaches tested avatar pacers and projected drills with club swimmers.</p></div>
        </article>
      </div>
      <div class="shots">
        <figure><img src="assets/unit-beam.webp" alt="Pool-On unit clamped on the edge of a tiled pool" loading="lazy"><figcaption>PO-1.2 on the pool edge</figcaption></figure>
        <figure><img src="assets/vangogh-night.webp" alt="A Van Gogh painting projected into a pool at night" loading="lazy"><figcaption>Van Gogh night show · 2025</figcaption></figure>
        <figure><img src="assets/aquagym.webp" alt="An aquagym session over projected content" loading="lazy"><figcaption>Aquagym session · 2025</figcaption></figure>
      </div>
    </div>
  </section>

  <section class="block" aria-labelledby="press-title">
    <div class="wrap">
      <div class="head"><span class="eyebrow">Talking about us</span><h2 id="press-title">News and press</h2></div>
      <div class="news" aria-label="News">
        <a href="https://www.b2match.com/e/ise-2026-open-innovation-challenge/participations/669459"><time>2026</time><span><b>ISE 2026 Open Innovation Challenge</b><br><small>Pool-On in the Open Innovation Challenge at Integrated Systems Europe</small></span></a>
        <a href="https://www.piscine-global.com/en/news/innovation/Pool-On-innovative-digital-solution-that-enhances-swimming-experience"><time>Mar 2023</time><span><b>Piscine Global: an innovative digital solution for swimming</b><br><small>Trade press feature</small></span></a>
      </div>
{partners()}
    </div>
  </section>
''' + cta('Your pool could be next')
    page('references.html', 'References · Pool-On', 'Pool-On references: hotels, events and swimming pools, plus news and partners.', 'references.html', refs)

    # ---------- Contact ----------
    contact = phero('festival-night.webp', 'Contact', 'See it in <em>your pool</em>', 'Tell us about your pool. We can bring a unit for a live demo on site.') + '''
  <section class="block" aria-labelledby="contact-title">
    <div class="wrap contact">
      <div>
        <h2 id="contact-title">Talk to us</h2>
        <dl>
          <dt>Email</dt><dd><a href="mailto:contact@pool-on.com">contact@pool-on.com</a></dd>
          <dt>Office</dt><dd>943 voie Antiope, 13600 La Ciotat, France</dd>
          <dt>Distributors</dt><dd>Ask for the partner kit</dd>
        </dl>
      </div>
      <form id="demo-form" novalidate>
        <div class="row2">
          <label for="f-name">Name<input id="f-name" name="name" autocomplete="name" required></label>
          <label for="f-org">Organisation<input id="f-org" name="org" autocomplete="organization"></label>
        </div>
        <div class="row2">
          <label for="f-email">Work email<input id="f-email" name="email" type="email" autocomplete="email" required></label>
          <label for="f-type">You are
            <select id="f-type" name="type">
              <option>Public pool / aquatic centre</option>
              <option>Hotel / resort / campsite</option>
              <option>Fitness club / swim school</option>
              <option>Events agency</option>
              <option>Distributor / pool builder / sales agent</option>
              <option>Individual</option>
              <option>Other</option>
            </select>
          </label>
        </div>
        <label for="f-src">How did you hear about us?
          <select id="f-src" name="source"><option>Trade show or event</option><option>LinkedIn</option><option>Instagram</option><option>Recommendation</option><option>Email</option><option>Other</option></select>
        </label>
        <label for="f-msg">Your pool and your project<textarea id="f-msg" name="message" placeholder="Pool size, depth, number of visitors, timing…"></textarea></label>
        <p style="font-size:.85rem;color:var(--muted)">We use this information only to answer your request. See our <a href="legal.html">privacy notice</a>.</p>
        <div><button class="btn btn-primary" type="submit">Send request</button></div>
        <p class="form-note" id="form-note" role="status"></p>
      </form>
    </div>
  </section>'''
    page('contact.html', 'Contact · Pool-On', 'Book a Pool-On demo in your pool or ask for the distributor kit.', 'contact.html', contact)

    # ---------- Legal ----------
    legal = '''
  <section class="block">
    <div class="wrap legal">
      <div class="head"><span class="eyebrow">Legal</span><h1 style="font-size:clamp(2.4rem,6vw,4rem);text-transform:uppercase">Legal notice &amp; privacy</h1></div>
      <section><h2>Publisher</h2>
        <dl>
          <dt>Company</dt><dd>Pool-On SAS, share capital €1,155.80</dd>
          <dt>Registered office</dt><dd>943 voie Antiope, 13600 La Ciotat, France</dd>
          <dt>Registration</dt><dd>RCS Marseille 909 766 222</dd>
          <dt>VAT</dt><dd>FR75 909 766 222</dd>
          <dt>Publication director</dt><dd>Gwénaël Moy, President</dd>
          <dt>Contact</dt><dd>contact@pool-on.com</dd>
        </dl>
      </section>
      <section><h2>Hosting</h2><p>Cloudflare, Inc., 101 Townsend Street, San Francisco, CA 94107, United States. www.cloudflare.com</p></section>
      <section><h2>Intellectual property</h2><p>POOL-ON is a registered EU trademark (EUIPO no. 018650491). The Pool-On system is protected by a French patent. All content on this site belongs to Pool-On unless stated otherwise. Optoma and DuraCore are trademarks of their respective owner.</p></section>
      <section><h2>Personal data</h2><p>Information sent through the contact form is used only to answer your request and manage the commercial relationship. It is kept for no longer than three years after our last contact. You can ask to access, correct or delete your data by writing to contact@pool-on.com. You can also file a complaint with the CNIL.</p></section>
      <section><h2>Cookies</h2><p>This site sets no advertising or tracking cookies. YouTube videos load only after you press play.</p></section>
    </div>
  </section>'''
    page('legal.html', 'Legal notice · Pool-On', 'Legal notice, privacy and cookies for pool-on.com.', 'legal.html', legal)

build()
print('ok')
