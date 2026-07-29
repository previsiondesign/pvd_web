#!/usr/bin/env python
"""Rebuild web-ready hero media from the masters in projects/Headline Images.

The masters (~146 MB of PNG + MP4) stay local and gitignored; this writes ~5 MB
into website-mockups/shared/images/hero/, which is what the site ships.

The video needs ffmpeg on PATH (`scoop install ffmpeg`); without it the existing
copy is left alone rather than being replaced by the uncompressed master.

Every series is full-bleed (object-fit: cover), so all of them are sized for the
full hero width; 1800 covers a 1440px hero with room to spare. HL16's master is
only 900px wide, so it stays there rather than being upscaled.

Filenames encode the per-frame hold time (`_2s`), which the hero JS mirrors in
each frame's data-dur. Run from the repo root:  python scripts/build-hero-images.py
"""
from PIL import Image
import os, glob, re, shutil, subprocess, sys

SRC = os.path.join('projects', 'Headline Images')
OUT = os.path.join('website-mockups', 'shared', 'images', 'hero')
QUALITY = 82
VIDEO_CRF = 23
VIDEO_SECONDS = 6.05   # the series holds 6s; the rest is never shown

# stem prefix -> (output basename, target width)
WIDTH = 1800
ROLES = {
    'HL01': ('hl01-ob', WIDTH),  # Old Bayshore, existing (master is 1473 wide)
    'HL02': ('hl02-ob', WIDTH),  # Old Bayshore, proposed
    'HL16': ('hl16-ss', 900),    # shadow shaping placeholder (master is 900)
}
for i in range(3, 9):
    ROLES['HL%02d' % i] = ('hl%02d-ppp' % i, WIDTH)  # shadow duration exhibits
for i in range(10, 16):
    ROLES['HL%02d' % i] = ('hl%02d-fc' % i, WIDTH)   # daylight analysis frames


def encode_video(src, dest):
    """The master is 9.6 Mbps with an audio track the hero never plays.

    CRF 23 lands ~2 MB at SSIM 0.97 against the source (CRF 26 saves 600 KB but
    drops to 0.96 — not worth it on the one moving element of the page). Trimmed
    to VIDEO_SECONDS because the series only ever holds 6 s and the hero resets
    currentTime to 0 each time, so the tail is never seen.
    """
    if not shutil.which('ffmpeg'):
        print('%-20s -> SKIPPED, ffmpeg not on PATH (`scoop install ffmpeg`)'
              % os.path.basename(src))
        return
    subprocess.run([
        'ffmpeg', '-v', 'error', '-y', '-i', src,
        '-t', str(VIDEO_SECONDS),
        '-c:v', 'libx264', '-profile:v', 'high', '-crf', str(VIDEO_CRF),
        '-preset', 'slow', '-pix_fmt', 'yuv420p',
        '-an',                        # muted in the hero
        '-movflags', '+faststart',    # metadata first, so it can start streaming
        dest,
    ], check=True)
    print('%-20s -> %-16s %6.2f MB -> %5.2f MB'
          % (os.path.basename(src), os.path.basename(dest),
             os.path.getsize(src) / 1048576, os.path.getsize(dest) / 1048576))


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

    for mp4 in glob.glob(os.path.join(SRC, '*.mp4')):
        encode_video(mp4, os.path.join(OUT, 'hl09-sfmta.mp4'))

    print('\nimages: %.1f MB -> %.2f MB' % (total_in / 1048576, total_out / 1048576))


if __name__ == '__main__':
    main()
