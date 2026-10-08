#!/usr/bin/env python3
"""Build a client approval page from a spec.

usage: python3 build_approval.py <spec.json> <out_dir>
Writes <out_dir>/index.html (page content for the Artifact tool: no doctype, title and style first),
<out_dir>/assets/* (every image the spec names) and <out_dir>/files.json (paths to publish beside the page).
Stops if the client facing text contains an em or en dash or any phrase in spec["banned"].
See ../references/spec.md for the spec format.
"""
import base64, colorsys, html, json, os, re, shutil, sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "assets", "page.html")


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgb_hex(c):
    return "#" + "".join(f"{max(0, min(255, round(v * 255))):02x}" for v in c)


def mix(a, b, t):
    a, b = hex_rgb(a), hex_rgb(b)
    return rgb_hex(tuple(x + (y - x) * t for x, y in zip(a, b)))


def lighten(h, amount):
    r, g, b = hex_rgb(h)
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    return rgb_hex(colorsys.hls_to_rgb(hh, min(1, ll + amount), ss))


def tokens(b):
    primary, deep, accent, paper = b["primary"], b.get("deep", b["primary"]), b["accent"], b.get("paper", "#faf8f3")
    ink_on_accent = deep
    light = {
        "bg": paper, "paper": "#ffffff", "ink": deep, "text": mix(deep, "#000000", 0.35), "muted": mix(deep, "#8a8a8a", 0.55),
        "line": mix(paper, deep, 0.10), "wash": mix(paper, deep, 0.04), "accent": primary, "on-accent": "#ffffff",
        "sun": accent, "on-sun": ink_on_accent, "band": deep, "on-band": "#ffffff", "band-muted": mix("#ffffff", primary, 0.22),
        "ok": primary, "ok-bg": mix("#ffffff", primary, 0.16), "change": mix(accent, "#000000", 0.45), "change-bg": mix("#ffffff", accent, 0.30),
        "wait-bg": mix(paper, accent, 0.18), "wait": mix(accent, "#000000", 0.6)}
    dark_bg = mix(deep, "#000000", 0.72)
    dark = {
        "bg": dark_bg, "paper": mix(deep, "#000000", 0.6), "ink": "#e6eee8", "text": "#d5dfd8", "muted": "#a2b2a7",
        "line": mix(deep, "#000000", 0.4), "wash": mix(deep, "#000000", 0.52), "accent": lighten(primary, 0.28), "on-accent": dark_bg,
        "band": mix(deep, "#000000", 0.25), "on-band": "#ffffff", "band-muted": mix("#ffffff", primary, 0.3),
        "ok": lighten(primary, 0.32), "ok-bg": mix(deep, "#000000", 0.3), "change": lighten(accent, 0.1), "change-bg": mix(accent, "#000000", 0.75),
        "wait-bg": mix(accent, "#000000", 0.8), "wait": lighten(accent, 0.15)}
    css = lambda d: " ".join(f"--{k}:{v};" for k, v in d.items())
    return css(light), css(dark)


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            if k not in ("src", "link", "script_font", "logo_white"):
                yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


def main(spec_path, out):
    spec = json.load(open(spec_path))
    base = os.path.dirname(os.path.abspath(spec_path))
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(f"{out}/assets")
    files, seen = [], {}

    def asset(p):
        src = p if os.path.isabs(p) else os.path.join(base, p)
        if src not in seen:
            name = f"assets/{len(seen) + 1:03d}_{re.sub(r'[^A-Za-z0-9._]', '_', os.path.basename(src))}"
            shutil.copy(src, f"{out}/{name}")
            seen[src] = name
            files.append(name)
        return seen[src]

    n = 0
    for sec in spec["sections"]:
        for it in sec["items"]:
            n += 1
            it["id"] = f"A{n}"
            for b in it.get("blocks", []):
                for im in b.get("images", []):
                    im["src"] = asset(im["src"])
    brand = spec["brand"]
    logo = asset(brand["logo_white"]) if brand.get("logo_white") else ""

    text = "\n".join(strings({k: v for k, v in spec.items() if k not in ("brand", "banned")}))
    bad = re.findall(r"[–—]", text)
    if bad:
        sys.exit(f"stopped: {len(bad)} em or en dash in the client facing text")
    for phrase in spec.get("banned", []):
        if phrase.lower() in text.lower():
            sys.exit(f"stopped: banned phrase {phrase!r} in the client facing text")

    light, dark = tokens(brand)
    font = brand.get("font", "Montserrat")
    weights = brand.get("font_weights", "400;500;600;700;800")
    face = ""
    if brand.get("script_font"):
        p = brand["script_font"] if os.path.isabs(brand["script_font"]) else os.path.join(base, brand["script_font"])
        face = ("@font-face{font-family:\"BrandScript\";src:url(data:font/woff2;base64," + base64.b64encode(open(p, "rb").read()).decode()
                + ") format(\"woff2\");font-display:block}")
    data = {k: spec.get(k) for k in ("slug", "client", "date_line", "cover", "glance", "sections", "questions", "signoff", "footer")}
    data["prepared_by"] = spec.get("prepared_by", "CEA Marketing")
    data["logo"] = logo
    page = (open(TEMPLATE).read()
            .replace("%%TITLE%%", html.escape(spec["page_title"]))
            .replace("%%FONTLINK%%", f"https://fonts.googleapis.com/css2?family={quote(font)}:wght@{weights}&display=swap")
            .replace("%%FONT%%", font)
            .replace("%%SCRIPTFACE%%", face)
            .replace("%%LIGHT%%", light).replace("%%DARK%%", dark)
            .replace("/*DATA*/null", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")))
    open(f"{out}/index.html", "w").write(page)
    json.dump(files, open(f"{out}/files.json", "w"), indent=0)
    size = sum(os.path.getsize(f"{out}/{f}") for f in files)
    print(f"{out}/index.html {len(page) // 1024} KB, {n} items, {len(spec.get('questions') or [])} questions, {len(files)} images ({size // 1024} KB)")


if __name__ == "__main__":
    main(*sys.argv[1:3])
