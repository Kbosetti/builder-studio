#!/usr/bin/env python3
"""Build the Mitchell Fall Campaign Guide page (one self-contained HTML file).

usage: python3 campaign-guide/build.py      writes campaign-guide/out/index.html
Edit src.html, drop new images in img/ and reference them as %%img:<file>%%. Publish out/index.html
to the existing artifact (see CLAUDE.md) so the team's link stays the same.
"""
import base64, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp", ".woff2": "font/woff2"}
EXT = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" '
       'stroke-linejoin="round" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>')

def uri(path):
    return f"data:{MIME[os.path.splitext(path)[1].lower()]};base64," + base64.b64encode(open(path, "rb").read()).decode()

src = open(f"{HERE}/src.html").read()
src = src.replace("%%ext%%", EXT)
src = src.replace("%%charlotte%%", uri(f"{HERE}/../home-portrait/fonts/charlotte.woff2"))
src = re.sub(r"%%img:([\w.-]+)%%", lambda m: uri(f"{HERE}/img/{m.group(1)}"), src)
left = re.findall(r"%%[\w:.-]+%%", src)
assert not left, left
os.makedirs(f"{HERE}/out", exist_ok=True)
open(f"{HERE}/out/index.html", "w").write(src)
print(f"wrote out/index.html, {len(src) // 1024} KB")
