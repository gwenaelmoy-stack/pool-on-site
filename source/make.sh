#!/bin/sh
# Rebuild the site in ../site: English pages, then French pages (site/fr) and the EN/FR switch.
set -e
cd "$(dirname "$0")"
python3 -c "p='../site/site.css';s=open(p).read();open(p,'w').write(s.split('\n/* ---- multi-page additions ---- */')[0])"
python3 build.py 2>/dev/null
python3 i18n.py
python3 extra.py
