#!/usr/bin/env python3
"""
TAVAS WORLD — navigation and footer synchroniser.

This file is the master for both the site header and the site footer.
Running it rewrites those two blocks on every page so they stay
identical everywhere, and points each page at the shared stylesheet
and script.

Usage:  python3 tools/sync-nav.py
"""

import re
import sys
import os

# ── The master navigation. Edit HERE and re-run to update every page. ──
NAV_ITEMS = [
    ('https://play.google.com/store/apps/details?id=com.shineon.journal', 'Tavas App',     '_blank', ''),
    ('https://tavascompass.com',                                          'Tavas Compass', '',       ''),
    ('books.html',                                                        'Library',       '',       ''),
    ('about.html',                                                        'About',         '',       ''),
    ('connect.html',                                                      'Work With Sara', '',      'nav-cta'),
]

# ── The master footer. Edit HERE and re-run to update every page. ──
# There is no primary navigation row: it repeated the header link for link,
# and the header is where navigation belongs. The footer carries the brand
# lockup, the tagline, the utility row and the copyright.

# Utility row. Support is the mailto the old footers already used; Terms and
# Privacy are the Tavas World legal pages in this repository. Refunds is not
# listed: this site takes no payments, so it has no refund policy of its own.
FOOTER_UTILITY = [
    ('mailto:support@tavasworld.com?subject=Tavas World Support', 'Support', ''),
    ('terms.html',                                                'Terms',   ''),
    ('privacy.html',                                              'Privacy', ''),
]

FOOTER_TAGLINE = 'Navigating life with intention.'
FOOTER_COPY = '&copy; 2026 Tavas World LLC. All rights reserved.'

LOGO_HREF = 'index.html'
LOGO_IMG = 'assets/img/TWLogoNewTrans.png'
LOGO_ALT = 'Tavas World'
LOGO_TEXT = 'TAVAS <span>WORLD</span>'

CSS_HREF = 'assets/css/site-nav.css'
JS_SRC = 'assets/js/site-nav.js'

PAGES = [
    'index.html',
    'about.html',
    'books.html',
    'connect.html',
    'services.html',
    'thankyou.html',
    'terms.html',
    'privacy.html',
]

# Selectors owned by the shared stylesheet. Any inline rule matching these
# is removed from the page so there is exactly one definition site-wide.
OWNED = re.compile(
    r'^\s*(?:/\*.*?\*/\s*)*'
    r'(?:#header|\.header-logo-wrap|\.header-logo-img|\.header-logo-text(?:\s+span)?'
    r'|footer|\.footer-inner|\.footer-brand(?:-name)?|\.footer-brand\s+img'
    r'|\.footer-tagline|\.footer-links(?:\s+a(?::hover)?)?|\.footer-copy'
    r'|#navbar(?:\s+a)?(?:\.show|:hover|\.active)?'
    r'|\.nav-cta(?::hover)?|\.mobile-nav-toggle|\.mobile-menu\s+\.nav-cta)'
    r'(?:\s*,\s*(?:#navbar\s+a(?::hover|\.active)?|\.nav-cta|\.mobile-nav-toggle))*\s*$',
    re.S,
)


def build_header(indent='  '):
    i = indent
    out = [f'{i}<header id="header">']
    out.append(f'{i}  <a href="{LOGO_HREF}" class="header-logo-wrap">')
    out.append(f'{i}    <img src="{LOGO_IMG}" alt="{LOGO_ALT}" class="header-logo-img">')
    out.append(f'{i}    <span class="header-logo-text">{LOGO_TEXT}</span>')
    out.append(f'{i}  </a>')
    out.append(f'{i}  <nav id="navbar">')
    for href, label, target, cls in NAV_ITEMS:
        attrs = f'href="{href}"'
        if target:
            attrs += f' target="{target}"'
        if cls:
            attrs += f' class="{cls}"'
        out.append(f'{i}    <a {attrs}>{label}</a>')
    out.append(f'{i}  </nav>')
    out.append(f'{i}  <button class="mobile-nav-toggle" id="mobileToggle" aria-label="Toggle navigation">')
    out.append(f'{i}    <i class="bi bi-list"></i>')
    out.append(f'{i}  </button>')
    out.append(f'{i}</header>')
    return '\n'.join(out)


def build_footer(indent='  '):
    i = indent
    out = [f'{i}<footer class="site-footer">']
    out.append(f'{i}  <div class="footer-inner">')
    out.append(f'{i}    <div class="footer-top">')
    out.append(f'{i}      <div>')
    out.append(f'{i}        <a href="{LOGO_HREF}" class="footer-logo-wrap" aria-label="Tavas World home">')
    out.append(f'{i}          <img src="{LOGO_IMG}" alt="" class="footer-logo-img">')
    out.append(f'{i}          <span class="footer-logo-text">{LOGO_TEXT}</span>')
    out.append(f'{i}        </a>')
    if FOOTER_TAGLINE:
        out.append(f'{i}        <p class="footer-tagline">{FOOTER_TAGLINE}</p>')
    out.append(f'{i}      </div>')
    out.append(f'{i}    </div>')
    out.append(f'{i}    <div class="footer-bottom">')
    out.append(f'{i}      <nav class="footer-utility" aria-label="Support and legal">')
    for href, label, target in FOOTER_UTILITY:
        attrs = f'href="{href}"'
        if target:
            attrs += f' target="{target}" rel="noopener"'
        out.append(f'{i}        <a {attrs}>{label}</a>')
    out.append(f'{i}      </nav>')
    out.append(f'{i}      <p class="footer-copy">{FOOTER_COPY}</p>')
    out.append(f'{i}    </div>')
    out.append(f'{i}  </div>')
    out.append(f'{i}</footer>')
    return '\n'.join(out)


def strip_owned_css(css):
    """Remove header rules from an inline <style> block, including inside media queries."""
    removed = []

    def scrub(block):
        def repl(m):
            sel, body = m.group(1), m.group(2)
            if OWNED.match(sel):
                removed.append(sel.strip()[:60])
                return ''
            return m.group(0)
        return re.sub(r'([^{}]+)\{([^{}]*)\}', repl, block)

    def media_repl(m):
        head, body = m.group(1), m.group(2)
        new_body = scrub(body)
        if not new_body.strip():
            return ''
        return head + '{' + new_body + '}'

    css = re.sub(r'(@media[^{]*)\{((?:[^{}]|\{[^{}]*\})*)\}', media_repl, css)
    css = scrub(css)
    css = re.sub(r'\n{3,}', '\n\n', css)
    return css, removed


def process(path):
    with open(path, 'r', encoding='utf-8', newline='') as f:
        raw = f.read()

    crlf = '\r\n' in raw
    s = raw.replace('\r\n', '\n')
    notes = []

    # 1. Replace the header block
    m = re.search(r'[ \t]*<header id="header">.*?</header>', s, re.S)
    if not m:
        return None, [f'{path}: NO <header id="header"> FOUND — skipped']
    s = s[:m.start()] + build_header() + s[m.end():]
    notes.append('header block replaced')

    # 1b. Replace the footer block
    fm = re.search(r'[ \t]*<footer[^>]*>.*?</footer>', s, re.S)
    if fm:
        s = s[:fm.start()] + build_footer() + s[fm.end():]
        notes.append('footer block replaced')
    else:
        notes.append('NO <footer> FOUND — footer skipped')

    # 2. Strip inline header CSS
    def style_repl(sm):
        inner, removed = strip_owned_css(sm.group(2))
        if removed:
            notes.append(f'{len(removed)} inline CSS rules removed')
        return sm.group(1) + inner + sm.group(3)

    s = re.sub(r'(<style[^>]*>)(.*?)(</style>)', style_repl, s, flags=re.S)

    # 3. Link the shared stylesheet (last in <head> so it is authoritative)
    if CSS_HREF not in s:
        s = s.replace('</head>', f'  <link href="{CSS_HREF}" rel="stylesheet">\n</head>', 1)
        notes.append('shared stylesheet linked')

    # 4. Remove inline nav behaviour that would double-bind the toggle
    before = len(s)
    s = re.sub(
        r'\n[ \t]*document\.getElementById\(([\'"])mobileToggle\1\)'
        r'\.addEventListener\([\'"]click[\'"],\s*function\s*\(\)\s*\{.*?\}\);',
        '', s, flags=re.S)
    s = re.sub(
        r'\n[ \t]*window\.addEventListener\([\'"]scroll[\'"],\s*function\s*\(\)\s*\{'
        r'(?:(?!\}\);).)*?getElementById\([\'"]header[\'"]\).*?\}\);',
        '', s, flags=re.S)
    if len(s) != before:
        notes.append('inline nav JS removed')

    # 5. Load the shared script
    if JS_SRC not in s:
        s = s.replace('</body>', f'  <script src="{JS_SRC}"></script>\n</body>', 1)
        notes.append('shared script linked')

    # 6. Tidy any <script> block left empty
    s = re.sub(r'\n[ \t]*<script>\s*</script>', '', s)

    if crlf:
        s = s.replace('\n', '\r\n')

    if s != raw:
        with open(path, 'w', encoding='utf-8', newline='') as f:
            f.write(s)
        return True, notes
    return False, ['no change needed']


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)
    for page in PAGES:
        if not os.path.exists(page):
            print(f'{page:16} MISSING')
            continue
        changed, notes = process(page)
        flag = 'updated' if changed else 'unchanged'
        print(f'{page:16} {flag:10} {"; ".join(notes)}')


if __name__ == '__main__':
    main()
