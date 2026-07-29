#!/usr/bin/env python
"""Publish the selected mockup to the production site repo.

Copies website-mockups/option-b2-type-business into the `site` repo (which serves
www.previsiondesign.com via GitHub Pages), rewriting the handful of things that
differ between a mockup and the live site:

  * the floating "← All Mockups" button is dropped
  * `../shared/...` asset paths become `shared/...`, since the page moves from a
    variant subfolder to the site root
  * the contact form's fallback message loses its "Mockup note:" framing

Only the assets the pages actually reference are copied — the shared folder still
holds portfolio stills from earlier rounds that this design no longer uses.

CNAME is left alone: it is what points the domain at Pages, and it lives in the
site repo, not here.

    python scripts/publish-site.py [dest]      # default dest: D:/Dev/site
"""
import io, os, shutil, sys

SRC = os.path.join('website-mockups', 'option-b2-type-business')
SHARED = os.path.join('website-mockups', 'shared', 'images')
DEFAULT_DEST = os.path.join('D:', os.sep, 'Dev', 'site')

PAGES = ['index.html', 'contact.html']
CODE = [os.path.join('css', 'styles.css'), os.path.join('js', 'main.js')]
ASSET_DIRS = ['hero', 'disciplines', 'work']
ASSET_FILES = ['prevision_icon.svg', 'prevision_icon_reverse.svg', 'adam_phillips.jpg',
               'favicon-32.png', 'apple-touch-icon.png', 'icon-512.png', 'og-card.jpg']

SITE_URL = 'https://www.previsiondesign.com'
# Crawlers look for these at the root. Generated here rather than kept by hand so
# they cannot drift from the page list above.
ROBOTS = '''User-agent: *
Allow: /

Sitemap: %s/sitemap.xml
''' % SITE_URL

HUB_BUTTON = '  <a class="back-to-hub" href="https://previsiondesign.github.io/pvd_web/">&larr; All Mockups</a>\n'

# A 503 from the contact endpoint means the Cloudflare function lost its config.
# On a mockup that reads as "not wired up yet"; on the live site it needs to tell
# a real enquirer what to do instead.
DEMO_NOTE = ("Mockup note: no message was actually sent &mdash; the form's "
             "delivery endpoint isn't connected yet.")
LIVE_NOTE = ("We couldn't send that just now &mdash; please email "
             "<a href=\"mailto:info@previsiondesign.com\">info@previsiondesign.com</a> "
             "and we'll pick it up right away.")


def write(path, text):
    io.open(path, 'w', encoding='utf-8', newline='\n').write(text)


def rewrite(text, is_page):
    text = text.replace('../shared/', 'shared/')
    if is_page:
        text = text.replace(HUB_BUTTON, '')
        text = text.replace(DEMO_NOTE, LIVE_NOTE)
    return text


def copy_tree(src, dest):
    """Mirror a directory, reporting the file count and bytes moved."""
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    n = size = 0
    for root, _, files in os.walk(dest):
        for f in files:
            n += 1
            size += os.path.getsize(os.path.join(root, f))
    return n, size


def main():
    dest = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DEST
    if not os.path.isdir(SRC):
        sys.exit('missing %s — run from the repo root' % SRC)
    if not os.path.isdir(dest):
        sys.exit('missing dest %s — clone previsiondesign/site there first' % dest)
    if not os.path.exists(os.path.join(dest, 'CNAME')):
        sys.exit('no CNAME in %s — refusing to publish, the domain would break' % dest)

    for page in PAGES:
        s = io.open(os.path.join(SRC, page), encoding='utf-8').read()
        out = rewrite(s, True)
        assert 'back-to-hub' not in out, 'hub button survived in ' + page
        assert '../shared/' not in out, 'unrewritten asset path in ' + page
        io.open(os.path.join(dest, page), 'w', encoding='utf-8', newline='\n').write(out)
        print('page   %-14s %6.1f KB' % (page, len(out) / 1024))

    for rel in CODE:
        s = io.open(os.path.join(SRC, rel), encoding='utf-8').read()
        out = rewrite(s, False)
        assert '../shared/' not in out, 'unrewritten asset path in ' + rel
        target = os.path.join(dest, rel)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        io.open(target, 'w', encoding='utf-8', newline='\n').write(out)
        print('code   %-14s %6.1f KB' % (rel.replace(os.sep, '/'), len(out) / 1024))

    total_n = total_size = 0
    for d in ASSET_DIRS:
        n, size = copy_tree(os.path.join(SHARED, d),
                            os.path.join(dest, 'shared', 'images', d))
        total_n += n
        total_size += size
        print('assets shared/images/%-8s %3d files %6.2f MB' % (d, n, size / 1048576))

    os.makedirs(os.path.join(dest, 'shared', 'images'), exist_ok=True)
    for f in ASSET_FILES:
        src_f = os.path.join(SHARED, f)
        if not os.path.exists(src_f):
            print('       MISSING asset %s' % f)
            continue
        shutil.copy2(src_f, os.path.join(dest, 'shared', 'images', f))
        total_n += 1
        total_size += os.path.getsize(src_f)
        print('assets shared/images/%-24s %5.0f KB' % (f, os.path.getsize(src_f) / 1024))

    # harmless here, but keeps Pages from ever second-guessing a path
    open(os.path.join(dest, '.nojekyll'), 'w').close()

    # /favicon.ico is requested by crawlers and older browsers whether or not the
    # HTML links it, so it has to sit at the root
    shutil.copy2(os.path.join(SHARED, 'favicon.ico'), os.path.join(dest, 'favicon.ico'))

    write(os.path.join(dest, 'robots.txt'), ROBOTS)
    urls = ''.join(
        '  <url><loc>%s/%s</loc></url>\n' % (SITE_URL, '' if p == 'index.html' else p)
        for p in PAGES)
    write(os.path.join(dest, 'sitemap.xml'),
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          '%s</urlset>\n' % urls)
    print('wrote  robots.txt, sitemap.xml (%d urls), favicon.ico' % len(PAGES))

    print('\n%d asset files, %.2f MB total' % (total_n, total_size / 1048576))
    print('CNAME preserved: %s' % io.open(os.path.join(dest, 'CNAME')).read().strip())


if __name__ == '__main__':
    main()
