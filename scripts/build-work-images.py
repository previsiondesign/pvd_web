#!/usr/bin/env python
"""Build the Featured Work card images from projects/Featured Work.

Each project folder holds a `*_main.png` — the still the card shows at rest —
plus numbered frames that cross-fade as a slideshow while the card is hovered.
The masters are ~940 MB and stay local (projects/ is gitignored); this writes
web-ready WebP into website-mockups/shared/images/work/.

Cards are 4:3 and never render wider than ~390px (one column on a phone), so
CARD at 800x600 is a shade over 2x for retina.

Frames are capped: a hover slideshow does not need 27 steps, and shipping them
would mean megabytes fetched on one mouseover. Where a project has more, frames
are sampled evenly across the sequence — keeping first and last, so a shadow
progression still reads start-to-finish — and the script reports what it dropped.

Run from the repo root:  python scripts/build-work-images.py
"""
from PIL import Image, ImageOps
import glob, os, shutil, subprocess, sys

SRC = os.path.join('projects', 'Featured Work')
OUT = os.path.join('website-mockups', 'shared', 'images', 'work')
CARD = (800, 600)
MAX_FRAMES = 10
Q_MAIN, Q_FRAME = 82, 76
VIDEO_CRF = 27

# folder -> (output stem, focus x, focus y). Focus is where the 4:3 crop centres,
# in fractions of the master; the shadow sheets put their plume above centre.
PROJECTS = {
    'shadow_Potrero Power Plant_San Francisco': ('ppp', 0.5, 0.44),
    'daylighting_Foster City_California':       ('fc',  0.5, 0.50),
    'sims_HousingElement_San Francisco':        ('he',  0.5, 0.50),
    'sims_OldBayshore_Burlingame':              ('ob',  0.5, 0.52),
    'sims_ValenciaStreet_San Francisco':        ('val', 0.5, 0.50),
    'shadow shaper':                            ('ss',  0.5, 0.42),
}


def sample(frames):
    """Evenly spaced subset, first and last always kept."""
    n = len(frames)
    if n <= MAX_FRAMES:
        return frames
    idx = [round(i * (n - 1) / (MAX_FRAMES - 1)) for i in range(MAX_FRAMES)]
    return [frames[i] for i in sorted(set(idx))]


def render(path, dest, focus, quality):
    im = Image.open(path).convert('RGB')
    im = ImageOps.fit(im, CARD, Image.LANCZOS, centering=focus)
    im.save(dest, 'WEBP', quality=quality, method=6)
    return os.path.getsize(path), os.path.getsize(dest)


def encode_video(src, dest):
    """The card is 4:3, so crop to that here rather than letting CSS throw the
    sides away — no point spending bits on pixels that never get shown. Source
    is 852x480; the centre 640x480 is what the card displays.
    """
    if not shutil.which('ffmpeg'):
        print('    video SKIPPED — ffmpeg not on PATH (`scoop install ffmpeg`)')
        return
    subprocess.run([
        'ffmpeg', '-v', 'error', '-y', '-i', src,
        '-vf', 'crop=ih*4/3:ih',
        '-c:v', 'libx264', '-profile:v', 'high', '-crf', str(VIDEO_CRF),
        '-preset', 'slow', '-pix_fmt', 'yuv420p',
        '-an',                      # plays silently under the cursor
        '-movflags', '+faststart',
        dest,
    ], check=True)
    print('    video %-22s %5.2f MB -> %4.2f MB'
          % (os.path.basename(dest), os.path.getsize(src) / 1048576,
             os.path.getsize(dest) / 1048576))


def main():
    if not os.path.isdir(SRC):
        sys.exit('missing %s — run from the repo root' % SRC)
    os.makedirs(OUT, exist_ok=True)
    total_in = total_out = 0

    for folder in sorted(os.listdir(SRC)):
        path = os.path.join(SRC, folder)
        if not os.path.isdir(path):
            continue
        if folder not in PROJECTS:
            print('%-46s SKIPPED — add it to PROJECTS to include it' % folder)
            continue
        stem, fx, fy = PROJECTS[folder]
        focus = (fx, fy)
        pngs = sorted(glob.glob(os.path.join(path, '*.png')))

        # The still is the "main" image: `XX_main.png` in most folders, a bare
        # `main.png` in others, or a `poster.png` where the project is a video.
        def is_main(p):
            s = os.path.splitext(os.path.basename(p))[0].lower()
            return s == 'main' or s.endswith('_main') or s == 'poster'

        mains = [p for p in pngs if is_main(p)]
        if not mains:
            print('%-46s SKIPPED — no main.png / *_main.png / poster.png' % folder)
            continue

        si, so = render(mains[0], os.path.join(OUT, stem + '-main.webp'), focus, Q_MAIN)
        total_in += si
        total_out += so

        frames = [p for p in pngs if p not in mains]
        kept = sample(frames)
        for n, f in enumerate(kept, 1):
            si, so = render(f, os.path.join(OUT, '%s-%02d.webp' % (stem, n)), focus, Q_FRAME)
            total_in += si
            total_out += so

        note = '%d frames' % len(kept)
        if len(kept) < len(frames):
            note += ' (sampled from %d — %d dropped)' % (len(frames), len(frames) - len(kept))
        if not frames:
            note = 'no frames — card stays static'
        print('%-46s -> %-5s main + %s' % (folder, stem, note))

        for mp4 in sorted(glob.glob(os.path.join(path, '*.mp4'))):
            encode_video(mp4, os.path.join(OUT, stem + '-options.mp4'))

    print('\nimages: %.1f MB -> %.2f MB' % (total_in / 1048576, total_out / 1048576))


if __name__ == '__main__':
    main()
