#!/usr/bin/env python
"""Rebuild web-ready hero images from the masters in projects/Headline Images.

The masters (~137 MB of PNGs) stay local and gitignored; this writes ~2 MB of
WebP into website-mockups/shared/images/hero/, which is what the site ships.

Widths differ by role, because the hero displays them differently:
  photos / massing  -> full-bleed (object-fit: cover), so they need to be wide
  plan exhibits     -> letterboxed (object-fit: contain) at roughly half width

Filenames encode the per-frame hold time (`_2s`), which the hero JS mirrors in
each frame's data-dur. Run from the repo root:  python scripts/build-hero-images.py
"""
from PIL import Image
import os, glob, re, sys

SRC = os.path.join('projects', 'Headline Images')
OUT = os.path.join('website-mockups', 'shared', 'images', 'hero')
QUALITY = 82

# stem prefix -> (output basename, target width)
ROLES = {
    'HL01': ('hl01-ob', 1800),   # Old Bayshore, existing (photo, full-bleed)
    'HL02': ('hl02-ob', 1800),   # Old Bayshore, proposed (photo, full-bleed)
    'HL16': ('hl16-ss', 900),    # shadow shaping placeholder (already small)
}
for i in range(3, 9):
    ROLES['HL%02d' % i] = ('hl%02d-ppp' % i, 1200)   # shadow duration exhibits
for i in range(10, 16):
    ROLES['HL%02d' % i] = ('hl%02d-fc' % i, 1600)    # daylight analysis frames


def main():
    if not os.path.isdir(SRC):
        sys.exit('missing %s — run from the repo root' % SRC)
    os.makedirs(OUT, exist_ok=True)
    total_in = total_out = 0
    for path in sorted(glob.glob(os.path.join(SRC, '*.png'))):
        stem = os.path.basename(path)
        key = stem.split('_')[0]
        if key not in ROLES:
            print('skip (no role): %s' % stem)
            continue
        base, width = ROLES[key]
        im = Image.open(path).convert('RGB')
        if im.width > width:
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        dest = os.path.join(OUT, base + '.webp')
        im.save(dest, 'WEBP', quality=QUALITY, method=6)
        si, so = os.path.getsize(path), os.path.getsize(dest)
        total_in += si
        total_out += so
        dur = re.search(r'_(\d+)s', stem)
        print('%-20s -> %-16s %sx%-5s %6.2f MB -> %5.0f KB  hold %ss'
              % (stem, base + '.webp', im.width, im.height, si / 1048576, so / 1024,
                 dur.group(1) if dur else '?'))

    # video is copied as-is: no ffmpeg here. Compress it before launch.
    for mp4 in glob.glob(os.path.join(SRC, '*.mp4')):
        dest = os.path.join(OUT, 'hl09-sfmta.mp4')
        if not os.path.exists(dest) or os.path.getmtime(mp4) > os.path.getmtime(dest):
            with open(mp4, 'rb') as f, open(dest, 'wb') as g:
                g.write(f.read())
        print('%-20s -> %-16s %6.2f MB (uncompressed — see HANDOFF)'
              % (os.path.basename(mp4), 'hl09-sfmta.mp4', os.path.getsize(dest) / 1048576))

    print('\nimages: %.1f MB -> %.2f MB' % (total_in / 1048576, total_out / 1048576))


if __name__ == '__main__':
    main()
