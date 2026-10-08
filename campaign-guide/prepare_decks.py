#!/usr/bin/env python3
"""Turn an exported deck into slide images and notes for the guide's deck viewer.

usage: python3 campaign-guide/prepare_decks.py <key> <deck.pdf> [<notes>]
  <notes> is the deck's .pptx export (Google Slides) or a JSON list of notes, one per slide (Canva).
Writes decks/<key>/NN.jpg (1600 wide), decks/<key>/tNN.jpg (thumbnail) and decks/<key>.json, which
build.py folds into the page. decks/edits.json lists the behind-the-scenes slides, boxes and notes the
sales team version leaves out. Re-run after re-exporting a deck; deck titles live in src.html.
"""
import json, os, re, sys, zipfile
from urllib.parse import parse_qs, urlparse
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
# concept pages that still carry reviewer build notes; never linked from the guide
SKIP_HOSTS = ("cea-mitchell-landing-pages-cea-marketing.vercel.app",)

def pptx_notes(path):
    z = zipfile.ZipFile(path)
    rels = lambda p: {a["Id"]: a["Target"] for a in (dict(re.findall(r'(\w+)="([^"]*)"', m))
                      for m in re.findall(r"<Relationship ([^>]+)/>", z.read(p).decode()))} if p in z.namelist() else {}
    prels = rels("ppt/_rels/presentation.xml.rels")
    order = [prels[r] for r in re.findall(r'<p:sldId [^>]*r:id="(\w+)"', z.read("ppt/presentation.xml").decode())]
    notes = []
    for target in order:
        n = next((t for t in rels(f"ppt/slides/_rels/{os.path.basename(target)}.rels").values() if "notesSlide" in t), None)
        text = ""
        if n:
            xml = z.read(os.path.normpath(f"ppt/slides/{n}")).decode()
            paras = []
            for p in re.findall(r"<a:p>.*?</a:p>", xml, flags=re.S):
                p = re.sub(r"<a:br/>|<a:br>.*?</a:br>", "<a:t>\n</a:t>", p, flags=re.S)
                paras.append("".join(re.findall(r"<a:t>([^<]*)</a:t>", p)))
            text = "\n".join(x for x in paras if x.strip() and x.strip() != "‹#›" and not x.strip().isdigit())
        for a, b in (("&amp;", "&"), ("&quot;", '"'), ("&apos;", "'"), ("&lt;", "<"), ("&gt;", ">")):
            text = text.replace(a, b)
        notes.append(re.sub(r"\n{3,}", "\n\n", text).strip())
    return notes

def cover_rect(page, text, mode):
    hit = page.search_for(text)
    if not hit:
        sys.exit(f"cover: '{text}' not found on slide {page.number + 1}")
    hit = hit[0]
    if mode == "block":
        return next(pymupdf.Rect(b[:4]) for b in page.get_text("blocks") if pymupdf.Rect(b[:4]).intersects(hit))
    boxes = [d["rect"] for d in page.get_drawings()
             if d.get("fill") is not None and d["rect"].contains(hit) and d["rect"].width < page.rect.width * .95]
    if not boxes:
        sys.exit(f"cover: no box around '{text}' on slide {page.number + 1}")
    return (max if mode == "outer" else min)(boxes, key=lambda b: b.get_area())

def paint_over(page, rect):
    # fill with the colour that surrounds the box, so the slide reads as if it was never there
    r = pymupdf.Rect(rect) + (-2, -2, 2, 2)
    pix = page.get_pixmap()
    pts = [(x, y) for x in range(int(r.x0) - 3, int(r.x1) + 4, 6) for y in (int(r.y0) - 3, int(r.y1) + 3)]
    pts += [(x, y) for y in range(int(r.y0), int(r.y1), 6) for x in (int(r.x0) - 3, int(r.x1) + 3)]
    seen = [pix.pixel(min(max(x, 0), pix.width - 1), min(max(y, 0), pix.height - 1)) for x, y in pts]
    fill = max(set(seen), key=seen.count)
    page.draw_rect(r, color=None, fill=[c / 255 for c in fill[:3]], overlay=True)

def main(key, pdf, notes_src=None):
    out = f"{HERE}/decks/{key}"
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):  # start clean so dropped slides do not linger
        os.remove(f"{out}/{f}")
    edits = json.load(open(f"{HERE}/decks/edits.json")).get(key, {})
    hide = set(edits.get("hide", []))
    doc = pymupdf.open(pdf)
    if notes_src and notes_src.endswith(".pptx"):
        notes = pptx_notes(notes_src)
    elif notes_src:
        notes = json.load(open(notes_src))
    else:
        notes = []
    for k, v in edits.get("notes", {}).items():
        notes[int(k) - 1] = v
    slides = []
    for i, page in enumerate(doc):
        if i + 1 in hide:
            continue
        for c in edits.get("cover", {}).get(str(i + 1), []):
            paint_over(page, cover_rect(page, c["text"], c["mode"]))
        n = len(slides) + 1
        for name, width, q in ((f"{n:02d}.jpg", 1600, 80), (f"t{n:02d}.jpg", 360, 72)):
            z = width / page.rect.width
            page.get_pixmap(matrix=pymupdf.Matrix(z, z)).save(f"{out}/{name}", jpg_quality=q)
        links = []
        for l in page.get_links():
            u = l.get("uri") or ""
            if u.startswith("https://www.google.com/url?"):  # Google Slides wraps every link in a redirect
                u = parse_qs(urlparse(u).query).get("q", [""])[0]
            u = u.rstrip(".")
            if u.startswith("http") and not any(h in u for h in SKIP_HOSTS) and u not in links:
                links.append(u)
        slides.append({"notes": notes[i] if i < len(notes) else "", "links": links})
    json.dump({"count": len(slides), "slides": slides}, open(f"{HERE}/decks/{key}.json", "w"), indent=1, ensure_ascii=False)
    size = sum(os.path.getsize(f"{out}/{f}") for f in os.listdir(out))
    print(f"{key}: {len(slides)} slides, {size // 1024} KB, notes on {sum(1 for s in slides if s['notes'])}")

if __name__ == "__main__":
    main(*sys.argv[1:])
