"""Build the persona campaign's all-sizes package for the media team (White Glove).

Usage: python3 make_sizes.py <deck.pdf>

<deck.pdf> is the Four Buyers banner ads deck (Canva DAHUJwduW5o) exported as PDF at pro quality.
Every ad in it is a vector frame, so each one is cut out at its exact edges, rendered at twice the
final size and scaled down to the platform size. Card 5 is the no-incentive SimplyMitchell card
(carousel-card5-no-incentive.jpg); the reels come from the Builder Studio media library.
Writes out/sizes/ and out/Mitchell-Persona-Ads-All-Sizes.zip. Needs pymupdf, pillow and numpy.
"""
import io
import os
import shutil
import sys
import urllib.request
import zipfile

import numpy as np
import pymupdf
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
SIZES = os.path.join(OUT, "sizes")
CACHE = os.path.join(OUT, ".cache")
ROOT = "Mitchell-Persona-Ads-All-Sizes"
CARD5 = os.path.join(HERE, "carousel-card5-no-incentive.jpg")
GUIDE_IMG = os.path.join(HERE, "..", "..", "..", "campaign-guide", "img")
LIB = "https://assets.cdn.filesafe.space/5o5zLlUPPizy6Ajp61oF/media/"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}

# Deck positions in PDF points (x, y, w, h); each is refined to the frame's exact edges.
CARD_X = (65.2, 330.8, 596.2, 861.8)
PERSONAS = [
    {"key": "value-unlocker", "name": "1 Value Unlocker", "url": "https://simplymitchellhomes.com/land",
     "reel": "22810412-bb99-4059-a322-1c42e6e0c50e.mp4",
     "cards": [(p, (75, 75, 660, 660)) for p in (8, 9, 10, 11)],
     "singles": [("Single image", 14, (75, 170.9, 420, 420), (1080, 1080)),
                 ("Story", 14, (528, 170.9, 236.3, 420.2), (1080, 1920))],
     "display": [(15, (75, 169.4, 450, 235.5), (1200, 628)),
                 (15, (561.8, 169.4, 224.9, 187.5), (300, 250)),
                 (15, (823.5, 169.4, 120, 450), (160, 600))]},
    {"key": "planner", "name": "2 Planner", "url": "https://simplymitchellhomes.com/math",
     "reel": "c09d779d-c541-4ed8-b713-46c917722945.mp4",
     "cards": [(17, (x, 307.7, 247.5, 247.5)) for x in CARD_X],
     "singles": [("Story", 20, (841.5, 184.6, 187.5, 333.2), (1080, 1920))],
     "display": [(20, (58.2, 185.5, 390, 204.1), (1200, 628)),
                 (20, (468, 184.6, 209.9, 175), (300, 250)),
                 (20, (703.5, 184.6, 93.8, 351.8), (160, 600))]},
    {"key": "transitioner", "name": "3 Transitioner (hold until legal approves)", "url": "https://simplymitchellhomes.com/math",
     "reel": "a19a3a8f-8d1c-4c29-9127-dc3eed3adbc3.mp4",
     "cards": [(21, (x, 278.4, 247.5, 247.5)) for x in CARD_X],
     "singles": [("Story", 23, (841.5, 184.6, 187.5, 333.2), (1080, 1920))],
     "display": [(23, (67.5, 184.6, 375, 196.1), (1200, 628)),
                 (23, (468, 184.6, 209.9, 175), (300, 250)),
                 (23, (703.5, 184.6, 93.8, 351.8), (160, 600))]},
    {"key": "grounded-dreamer", "name": "4 Grounded Dreamer", "url": "https://simplymitchellhomes.com/math",
     "reel": "e9548a4b-7493-40af-8b94-21ed23f6057a.mp4",
     "cards": [(26, (x, 293.4, 247.5, 247.5)) for x in CARD_X],
     "singles": [],
     "display": []},
]
GOOGLE_MAX = 150 * 1024  # Google Ads uploaded image ads


def refine(page, rect):
    """Snap an approximate frame to its exact edges against the page background."""
    x, y, w, h = rect
    m, z = 8, 12
    clip = pymupdf.Rect(x - m, y - m, x + w + m, y + h + m)
    pix = page.get_pixmap(matrix=pymupdf.Matrix(z, z), clip=clip, alpha=False)
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3).astype(int)
    ring = np.concatenate([a[:3].reshape(-1, 3), a[-3:].reshape(-1, 3), a[:, :3].reshape(-1, 3), a[:, -3:].reshape(-1, 3)])
    bg = np.median(ring, axis=0)
    mask = np.abs(a - bg).max(axis=2) > 18
    inner = slice(m * z + 4 * z, -(m * z + 4 * z))

    def run(profile, lo, hi):
        on = profile > 0.6
        c = (lo + hi) // 2
        s = e = c
        while s > 0 and on[s - 1]:
            s -= 1
        while e < len(on) - 1 and on[e + 1]:
            e += 1
        return s, e + 1

    rows = mask[:, inner].mean(axis=1)
    cols = mask[inner, :].mean(axis=0)
    r0, r1 = run(rows, m * z, pix.height - m * z)
    c0, c1 = run(cols, m * z, pix.width - m * z)
    nx, ny = clip.x0 + c0 / z, clip.y0 + r0 / z
    nw, nh = (c1 - c0) / z, (r1 - r0) / z
    if abs(nw - w) > 3 or abs(nh - h) > 3:  # edge finder lost the frame; trust the deck position
        nx, ny, nw, nh = x, y, w, h
    t = 0.2  # step inside the anti-aliased edge so no slide background shows
    return pymupdf.Rect(nx + t, ny + t, nx + nw - t, ny + nh - t)


def cut(doc, pn, rect, size):
    page = doc[pn - 1]
    r = refine(page, rect)
    z = 2 * size[0] / r.width
    pix = page.get_pixmap(matrix=pymupdf.Matrix(z, z), clip=r, alpha=False)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    return im.resize(size, Image.LANCZOS), r


def save_jpg(im, path, limit=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    for q in (92, 88, 84, 80, 76, 72):
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
        if not limit or buf.tell() <= limit:
            break
    with open(path, "wb") as f:
        f.write(buf.getvalue())
    return buf.tell()


def fetch(name):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, name)
    if not os.path.exists(path):
        with urllib.request.urlopen(urllib.request.Request(LIB + name, headers=UA), timeout=120) as r, open(path + ".part", "wb") as f:
            shutil.copyfileobj(r, f)
        os.replace(path + ".part", path)
    return path


def likeness(a, b):
    """0 means identical; used to confirm a cut matches the approved card on the approval page."""
    s = (48, 48)
    x = np.asarray(a.convert("L").resize(s), dtype=float)
    y = np.asarray(b.convert("L").resize(s), dtype=float)
    return float(np.abs(x - y).mean())


def main(pdf):
    doc = pymupdf.open(pdf)
    if os.path.isdir(SIZES):
        shutil.rmtree(SIZES)
    base = os.path.join(SIZES, ROOT)
    card5 = Image.open(CARD5).convert("RGB")
    previews = []
    for p in PERSONAS:
        folder = os.path.join(base, p["name"])
        tiles = []
        for i, (pn, rect) in enumerate(p["cards"], 1):
            im, r = cut(doc, pn, rect, (1080, 1080))
            approved = os.path.join(GUIDE_IMG, f"buyers-{p['key']}-{i}.jpg")
            note = f"likeness to approved card {likeness(im, Image.open(approved)):.1f}" if os.path.exists(approved) else ""
            save_jpg(im, os.path.join(folder, "Meta carousel", f"Card {i} (1080x1080).jpg"))
            print(p["key"], "card", i, "page", pn, [round(v, 1) for v in r], note)
            tiles.append(im)
        save_jpg(card5.resize((1080, 1080), Image.LANCZOS), os.path.join(folder, "Meta carousel", "Card 5 (1080x1080).jpg"))
        tiles.append(card5)
        for label, pn, rect, size in p["singles"]:
            im, r = cut(doc, pn, rect, size)
            save_jpg(im, os.path.join(folder, f"Meta {label.lower()}", f"{label} ({size[0]}x{size[1]}).jpg"))
            print(p["key"], label, "page", pn, [round(v, 1) for v in r])
            tiles.append(im)
        for pn, rect, size in p["display"]:
            im, r = cut(doc, pn, rect, size)
            n = save_jpg(im, os.path.join(folder, "Google display", f"{size[0]}x{size[1]}.jpg"), GOOGLE_MAX)
            print(p["key"], "display", size, "page", pn, [round(v, 1) for v in r], f"{n // 1024} KB")
            tiles.append(im)
        reel_dir = os.path.join(folder, "Reel")
        os.makedirs(reel_dir, exist_ok=True)
        shutil.copy(fetch(p["reel"]), os.path.join(reel_dir, "Reel (1080x1920).mp4"))
        previews.append((p["name"], tiles))
    write_preview(previews, os.path.join(base, "Preview of every ad.jpg"))
    write_guide(os.path.join(base, "READ ME, upload guide and Meta copy.txt"))
    # The full set runs past Gmail's 25 MB limit, so a second zip leaves out the reels (the guide links them).
    for name, keep in ((ROOT, lambda f: True), (f"{ROOT}-Images-Only", lambda f: not f.endswith(".mp4"))):
        zpath = os.path.join(OUT, f"{name}.zip")
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
            for d, _, files in os.walk(base):
                for f in sorted(files):
                    full = os.path.join(d, f)
                    if keep(f):
                        z.write(full, os.path.relpath(full, SIZES))
        print("wrote", zpath, f"{os.path.getsize(zpath) / 1e6:.1f} MB")


def write_preview(rows, path):
    h, gap, label = 260, 16, 46
    widths = [sum(int(t.width * h / t.height) + gap for t in tiles) for _, tiles in rows]
    sheet = Image.new("RGB", (max(widths) + gap, len(rows) * (h + label + gap) + gap), (243, 242, 238))
    from PIL import ImageDraw
    d = ImageDraw.Draw(sheet)
    y = gap
    for name, tiles in rows:
        d.text((gap, y + 12), name.upper(), fill=(30, 79, 51))
        x = gap
        for t in tiles:
            w = int(t.width * h / t.height)
            sheet.paste(t.resize((w, h), Image.LANCZOS), (x, y + label))
            x += w + gap
        y += h + label + gap
    sheet.save(path, "JPEG", quality=85)


def write_guide(path):
    shutil.copy(os.path.join(HERE, "upload_guide.txt"), path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
