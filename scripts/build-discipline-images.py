#!/usr/bin/env python
"""Crop the discipline-card snippets from the masters in projects/Disciplines.

The service cards carry a wide banner strip instead of a line icon, greyscale
until the card is hovered. The masters (~27 MB) stay local and gitignored; this
writes ~5 WebP files into website-mockups/shared/images/disciplines/.

BANNER is 2x the widest the card ever gets (340px in the 1180px desktop frame,
~390px full-bleed on a phone), so the strip stays sharp on retina.

Crops are given as (centre x, centre y, width) in fractions of the master, not
pixels, so they survive a master being re-exported at another size. Each one is
chosen to put the recognisable part of the analysis in a 4.2:1 letterbox — the
plume on the duration map, the sunlit patches on the daylight render — because
at this size a centred crop of the whole sheet reads as noise.

Run from the repo root:  python scripts/build-discipline-images.py
"""
from PIL import Image
import os, sys

SRC = os.path.join('projects', 'Disciplines')
OUT = os.path.join('website-mockups', 'shared', 'images', 'disciplines')
BANNER = (800, 190)          # 4.21:1
QUALITY = 82

# The banner as it renders in the 1180px desktop frame. NUDGE values below are in
# these units — the pixels you actually see on the card — so a review note like
# "down 31px, left 38px" can be typed in as-is and the script scales it into the
# master's coordinates.
BANNER_CSS = (338, 80)

# master -> (output stem, centre x, centre y, width) — fractions of the master
CROPS = {
    'shadow.png':         ('shadow-studies',  0.55, 0.42, 0.68),
    'shadow_shaping.png': ('shadow-shaping',  0.50, 0.32, 1.00),
    # the story here is the warm shaft running from the french doors down to the
    # wall base — a centred crop lands on empty floor
    'daylighting.png':    ('daylight-studies', 0.42, 0.57, 0.80),
    'vis_sims.png':       ('visual-studies',  0.50, 0.55, 1.00),
    'peer_review.png':    ('peer-review',     0.49, 0.50, 0.95),
}

# stem -> (dx, dy) in BANNER_CSS px: which way the visible content should move.
# Positive dx is right, positive dy is down. Adam's review, 2026-07-28.
NUDGE = {
    'shadow-studies':   (-38, 58),   # +11 on review 2, +16 on review 3
    'shadow-shaping':   (0, 28),     # +6, then +10
    'daylight-studies': (4, -9),
    'visual-studies':   (0, 26),     # +6, then +10
    'peer-review':      (0, 0),
}


def crop_box(size, cx, cy, wfrac, nudge=(0, 0)):
    """Widest 4.2:1 box at this centre that still fits inside the master.

    Moving the visible content one way means moving the crop window the other,
    hence the inverted nudge.
    """
    w, h = size
    bw = w * wfrac
    bh = bw * BANNER[1] / BANNER[0]
    if bh > h:                       # too tall to fit — fall back to full height
        bh = h
        bw = bh * BANNER[0] / BANNER[1]
    left = cx * w - bw / 2 - (nudge[0] / BANNER_CSS[0]) * bw
    top = cy * h - bh / 2 - (nudge[1] / BANNER_CSS[1]) * bh
    clamped = tuple(round(v) for v in (
        max(0, min(left, w - bw)), max(0, min(top, h - bh))))
    # a silently clamped nudge would look like the request was ignored
    short = (round(clamped[0] - left), round(clamped[1] - top))
    return clamped[0], clamped[1], clamped[0] + round(bw), clamped[1] + round(bh), short


def main():
    if not os.path.isdir(SRC):
        sys.exit('missing %s — run from the repo root' % SRC)
    os.makedirs(OUT, exist_ok=True)
    total_in = total_out = 0
    for name, (stem, cx, cy, wfrac) in sorted(CROPS.items()):
        path = os.path.join(SRC, name)
        if not os.path.exists(path):
            print('skip (missing): %s' % name)
            continue
        im = Image.open(path).convert('RGB')
        nudge = NUDGE.get(stem, (0, 0))
        l, t, r, b, short = crop_box(im.size, cx, cy, wfrac, nudge)
        im = im.crop((l, t, r, b)).resize(BANNER, Image.LANCZOS)
        dest = os.path.join(OUT, stem + '.webp')
        im.save(dest, 'WEBP', quality=QUALITY, method=6)
        si, so = os.path.getsize(path), os.path.getsize(dest)
        total_in += si
        total_out += so
        note = ''
        if any(short):
            note = '  !! hit the master edge, nudge short by %s px of master' % (short,)
        print('%-22s -> %-22s nudge %-10s crop %-24s %4.0f KB%s'
              % (name, stem + '.webp', str(nudge), str((l, t, r, b)), so / 1024, note))
    print('\n%.1f MB -> %.0f KB' % (total_in / 1048576, total_out / 1024))


if __name__ == '__main__':
    main()
