#!/usr/bin/env python
"""Normalise the client logos for the "Trusted By" strip.

The sources are a mix of SVG and PNG at wildly different sizes and aspect ratios
(229x45 to 500x500), so they cannot simply be dropped in at a shared height — a
wide wordmark would tower over a square badge. Each is trimmed to its actual ink,
then fitted into a common box so they read at similar optical weight, and the
page renders them with `object-fit: contain` in that same box.

Colour is kept in the file; the greyscale treatment is CSS, so switching the
strip back to full colour is a one-line change rather than a rebuild.

    python scripts/build-client-logos.py
"""
import glob, io, os, sys

import cairosvg
from PIL import Image

SRC = os.path.join('images', 'logos', 'client_logos')
OUT = os.path.join('website-mockups', 'shared', 'images', 'clients')
BOX = (280, 128)         # 2x the 140x64 cell the page draws
PAD = 2                  # keeps antialiased edges off the boundary

# source stem -> output stem, so the markup does not inherit vendor filenames
NAMES = {
    'esa-logo': 'esa',
    'icf-logo_full': 'icf',
    'logo-swca': 'swca',
    'stantec-logo': 'stantec',
    'tishmanspeyer-logo': 'tishman-speyer',
    'tmg_logo_black': 'tmg-partners',
    'perkins-will-logo': 'perkins-will',
    'UPP+Logo_thick': 'urban-planning-partners',
    'sfplanning-logo': 'sf-planning',
    'sfrpd-logo': 'sf-rec-parks',
    'sf-port-logo': 'port-of-sf',
    'related': 'related-california',
}

# Fitting every mark to the same box makes a wide wordmark's letters tower over a
# square badge's, because one is width-limited and the other height-limited. These
# multipliers pull the *lettering* into a comparable range — tuned by eye against
# the contact sheet, which is the only way to judge it (a circular badge's ink
# height says nothing about the size of the name inside it).
SCALE = {
    'esa': 0.677,
    'icf': 0.677,
    'tishman-speyer': 1.00,
    'sf-rec-parks': 0.677,
    'related-california': 1.00,
    'swca': 0.649,                    # -10% on review 2
    'sf-planning': 0.721,
    'stantec': 0.851,
    'tmg-partners': 0.721,            # -10% on review 2
    'perkins-will': 0.960,            # +10% on review 2
    'urban-planning-partners': 0.871,
    'port-of-sf': 0.871,
}

# Ink luminance multiplier for marks that read too light next to the rest once
# the strip is greyscaled. Applied to RGB only, so the alpha edge stays clean.
DARKEN = {
    'esa': 0.90,
    'urban-planning-partners': 0.90,
}


def load(path):
    """SVGs render at 4x the box; rasters open as-is."""
    if path.lower().endswith('.svg'):
        png = cairosvg.svg2png(url=path, output_width=BOX[0] * 4)
        return Image.open(io.BytesIO(png)).convert('RGBA')
    im = Image.open(path).convert('RGBA')
    return im


def darken_knockout(im, name):
    """A reverse/knockout logo is drawn white for dark backgrounds and vanishes on
    the white Trusted By band. Same artwork, opposite polarity — recolour the ink
    dark and keep the alpha, which is how the mark is meant to read on light.
    """
    px = im.getchannel('A').point(lambda a: 255 if a > 40 else 0)
    ink = im.convert('L')
    vals = [v for v, a in zip(ink.getdata(), px.getdata()) if a]
    if not vals or sum(vals) / len(vals) < 200:
        return im, False
    solid = Image.new('RGBA', im.size, (45, 55, 62, 255))
    solid.putalpha(im.getchannel('A'))
    print('%-26s    knockout logo (white ink) — recoloured dark for the light band' % name)
    return solid, True


def trim(im):
    """Drop transparent or white margin so the fit uses the mark, not the canvas."""
    alpha = im.getchannel('A')
    box = alpha.getbbox()
    if box and alpha.getextrema()[0] < 250:
        return im.crop(box)
    # opaque source: trim near-white instead
    grey = im.convert('L').point(lambda v: 0 if v > 244 else 255)
    box = grey.getbbox()
    return im.crop(box) if box else im


def main():
    if not os.path.isdir(SRC):
        sys.exit('missing %s' % SRC)
    os.makedirs(OUT, exist_ok=True)
    total = 0
    for path in sorted(glob.glob(os.path.join(SRC, '*'))):
        stem = os.path.splitext(os.path.basename(path))[0]
        if stem not in NAMES:
            print('%-26s SKIPPED — add it to NAMES to include it' % stem)
            continue
        im, _ = darken_knockout(load(path), os.path.basename(path))
        im = trim(im)
        d = DARKEN.get(NAMES[stem])
        if d:
            r, g, b, a = im.split()
            im = Image.merge('RGBA', [ch.point(lambda v, k=d: int(v * k)) for ch in (r, g, b)] + [a])
        w, h = im.size
        scale = min((BOX[0] - PAD * 2) / w, (BOX[1] - PAD * 2) / h) * SCALE.get(NAMES[stem], 1.0)
        upscaled = scale > 1
        im = im.resize((max(1, round(w * scale)), max(1, round(h * scale))), Image.LANCZOS)
        canvas = Image.new('RGBA', BOX, (0, 0, 0, 0))
        canvas.paste(im, ((BOX[0] - im.width) // 2, (BOX[1] - im.height) // 2), im)
        dest = os.path.join(OUT, NAMES[stem] + '.webp')
        canvas.save(dest, 'WEBP', quality=90, method=6)
        total += os.path.getsize(dest)
        note = '  !! upscaled %.1fx from %dx%d — ask for a larger source' % (scale, w, h) if upscaled else ''
        print('%-26s -> %-28s %3dx%-3d  scale %.3f%s%s'
              % (os.path.basename(path), NAMES[stem] + '.webp', im.width, im.height,
                 SCALE.get(NAMES[stem], 1.0),
                 '  darkened %.2f' % DARKEN[NAMES[stem]] if NAMES[stem] in DARKEN else '', note))
    print('\n%d logos, %.0f KB' % (len(NAMES), total / 1024))


if __name__ == '__main__':
    main()
